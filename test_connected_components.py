import unittest
import pandas as pd
import tempfile
import os

from connected_components import (
    find_connected_components,
    create_output_dataframe,
    main,
)
import functions as fl


class TestConnectedComponents(unittest.TestCase):

    def setUp(self):
        """Set up test data before each test method"""
        # Simple test case with two connected components
        self.simple_data = pd.DataFrame(
            {"LEFT_SIDE": ["A|1", "B|2", "D|4"], "RIGHT_SIDE": ["B|2", "C|3", "E|5"]}
        )

        # Test case with a single connected component
        self.single_component_data = pd.DataFrame(
            {"LEFT_SIDE": ["A|1", "B|2", "C|3"], "RIGHT_SIDE": ["B|2", "C|3", "D|4"]}
        )

        # Test case with no connections (each node is its own component) using self-loops
        self.disconnected_data = pd.DataFrame(
            {
                "LEFT_SIDE": ["A|1", "B|2", "C|3", "D|4", "E|5", "F|6"],
                "RIGHT_SIDE": ["A|1", "B|2", "C|3", "D|4", "E|5", "F|6"],
            }
        )

        # Test case with self-references
        self.self_reference_data = pd.DataFrame(
            {"LEFT_SIDE": ["A|1", "A|1", "B|2"], "RIGHT_SIDE": ["A|1", "B|2", "C|3"]}
        )

    def test_find_connected_components_simple(self):
        """Test finding connected components in a simple graph"""
        components = find_connected_components(self.simple_data)

        # Should have 2 connected components
        self.assertEqual(len(components), 2)

        # First component should contain A|1, B|2, C|3
        self.assertIn("A|1", components[0])
        self.assertIn("B|2", components[0])
        self.assertIn("C|3", components[0])

        # Second component should contain D|4, E|5
        self.assertIn("D|4", components[1])
        self.assertIn("E|5", components[1])

    def test_find_connected_components_single(self):
        """Test finding connected components in a fully connected graph"""
        components = find_connected_components(self.single_component_data)

        # Should have 1 connected component
        self.assertEqual(len(components), 1)

        # Component should contain all nodes
        all_nodes = set(self.single_component_data.LEFT_SIDE) | set(
            self.single_component_data.RIGHT_SIDE
        )
        self.assertEqual(len(components[0]), len(all_nodes))
        for node in all_nodes:
            self.assertIn(node, components[0])

    def test_find_connected_components_disconnected(self):
        """Test finding connected components in a disconnected graph"""
        components = find_connected_components(self.disconnected_data)

        # Should have 6 connected components (each node is separate)
        self.assertEqual(len(components), 6)

        # Each component should have exactly one node
        for component in components:
            self.assertEqual(len(component), 1)

    def test_find_connected_components_self_reference(self):
        """Test finding connected components with self-references"""
        components = find_connected_components(self.self_reference_data)

        # Should have 1 connected component (A|1, B|2, C|3)
        self.assertEqual(len(components), 1)
        self.assertEqual(len(components[0]), 3)
        self.assertIn("A|1", components[0])
        self.assertIn("B|2", components[0])
        self.assertIn("C|3", components[0])

    def test_create_output_dataframe(self):
        """Test creating output DataFrame from connected components"""
        components = [["A|1", "B|2"], ["C|3"]]
        df = create_output_dataframe(components)

        # Should have 3 rows
        self.assertEqual(len(df), 3)

        # Check columns
        self.assertIn("ID_UNIQUE", df.columns)
        self.assertIn("SOURCE", df.columns)
        self.assertIn("IDI", df.columns)
        self.assertIn("TIM_PROCESSED", df.columns)

        # Check component assignments
        self.assertEqual(df[df.IDI == "1"]["ID_UNIQUE"].iloc[0], 0)
        self.assertEqual(df[df.IDI == "2"]["ID_UNIQUE"].iloc[0], 0)
        self.assertEqual(df[df.IDI == "3"]["ID_UNIQUE"].iloc[0], 1)

        # Check source parsing
        self.assertEqual(df[df.IDI == "1"]["SOURCE"].iloc[0], "A")
        self.assertEqual(df[df.IDI == "2"]["SOURCE"].iloc[0], "B")
        self.assertEqual(df[df.IDI == "3"]["SOURCE"].iloc[0], "C")

    def test_main_function(self):
        """Test the main function with a temporary file"""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("LEFT_SIDE,RIGHT_SIDE\n")
            f.write("A|1,B|2\n")
            f.write("B|2,C|3\n")
            input_file = f.name

        try:
            # Create a temporary output file
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".csv", delete=False
            ) as f:
                output_file = f.name

            # Run the main function
            result_df = main(input_file, output_file)

            # Check the result
            self.assertEqual(len(result_df), 3)
            self.assertEqual(
                len(result_df["ID_UNIQUE"].unique()), 1
            )  # All should be in same component

            # Check that output file was created
            self.assertTrue(os.path.exists(output_file))

            # Read the output file and verify its contents
            output_df = pd.read_csv(output_file)
            self.assertEqual(len(output_df), 3)

        finally:
            # Clean up temporary files
            if os.path.exists(input_file):
                os.unlink(input_file)
            if os.path.exists(output_file):
                os.unlink(output_file)

    def test_missing_columns(self):
        """Test error handling for missing required columns"""
        invalid_data = pd.DataFrame({"COL1": ["A|1", "B|2"], "COL2": ["B|2", "C|3"]})

        with self.assertRaises(ValueError):
            find_connected_components(invalid_data)

    def test_empty_data(self):
        """Test handling of empty input data"""
        empty_data = pd.DataFrame(columns=["LEFT_SIDE", "RIGHT_SIDE"])
        components = find_connected_components(empty_data)
        self.assertEqual(len(components), 0)


class TestFunctionsModule(unittest.TestCase):

    def test_make_equivalence_classes(self):
        """Test the make_equivalence_classes function with symmetric input"""
        iterable = ["A", "B", "C", "D"]
        # Create symmetric closure of the relation
        tuples = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]

        classes = fl.make_equivalence_classes(iterable, tuples)

        # Should have 2 classes: [A,B,C] and [D]
        self.assertEqual(len(classes), 2)

        # Check class sizes
        class_sizes = sorted([len(cls) for cls in classes])
        self.assertEqual(class_sizes, [1, 3])

        # Check that classes contain expected elements
        classes_sorted = [sorted(cls) for cls in classes]
        self.assertIn(["A", "B", "C"], classes_sorted)
        self.assertIn(["D"], classes_sorted)

    def test_dfs_transitive_closure(self):
        """Test the dfs_transitive_closure function"""
        iterable = ["A", "B", "C"]
        tuples = [("A", "B"), ("B", "C")]

        closure = fl.dfs_transitive_closure(iterable, tuples)

        # Should include all transitive relations
        expected_relations = [
            ("A", "A"),
            ("A", "B"),
            ("A", "C"),
            ("B", "B"),
            ("B", "C"),
            ("C", "C"),
        ]

        for relation in expected_relations:
            self.assertIn(relation, closure)


if __name__ == "__main__":
    unittest.main()
