"""
Main module for finding connected components in a graph representation of data.

This module processes input data, identifies connected components using an
equivalence relation, and generates output with component identifiers.
"""

import argparse
import datetime
import time
from typing import List, Any, Tuple
import pandas as pd

import functions as fl


def find_connected_components(input_df: pd.DataFrame) -> List[List[Any]]:
    """Find connected components in a graph defined by LEFT_SIDE and RIGHT_SIDE columns.

    This function processes a DataFrame containing pairs of connected nodes,
    creates a symmetric relation, and identifies all connected components
    (equivalence classes) in the graph.

    Args:
        input_df: DataFrame with at least two columns: LEFT_SIDE and RIGHT_SIDE

    Returns:
        A list of connected components, where each component is a list of nodes

    Example:
        >>> df = pd.DataFrame({
        ...     'LEFT_SIDE': ['A|1', 'B|2'],
        ...     'RIGHT_SIDE': ['B|2', 'C|3']
        ... })
        >>> find_connected_components(df)
        [['A|1', 'B|2', 'C|3']]
    """

    def is_related(a: Any, b: Any) -> bool:
        """Check if two elements are related based on the input tuples."""
        return (a, b) in relation_tuples

    def create_symmetric_closure(
        tuples: List[Tuple[Any, Any]],
    ) -> List[Tuple[Any, Any]]:
        """Create symmetric closure of a relation by adding all reverse pairs.

        Args:
            tuples: List of relation tuples

        Returns:
            Symmetric closure of the input relation
        """
        closure = set(tuples)
        # Create a copy to avoid modifying while iterating
        original_tuples = closure.copy()
        # Add reverse of each tuple to make symmetric
        closure.update((y, x) for x, y in original_tuples)
        return list(closure)

    # Validate input columns first
    required_columns = {"LEFT_SIDE", "RIGHT_SIDE"}
    if not required_columns.issubset(input_df.columns):
        missing = required_columns - set(input_df.columns)
        raise ValueError(f"Input DataFrame missing required columns: {missing}")

    # Extract the relevant columns and convert to tuples
    relation_data = input_df[["LEFT_SIDE", "RIGHT_SIDE"]]
    relation_tuples = [tuple(x) for x in relation_data.to_numpy()]

    # Get all unique nodes from both columns
    all_nodes = set(relation_data.LEFT_SIDE).union(set(relation_data.RIGHT_SIDE))

    # Create symmetric closure of the relation
    symmetric_relations = create_symmetric_closure(relation_tuples)

    # Find equivalence classes (connected components)
    return fl.make_equivalence_classes(all_nodes, symmetric_relations)


def create_output_dataframe(connected_components: List[List[Any]]) -> pd.DataFrame:
    """Create output DataFrame from connected components.

    Args:
        connected_components: List of connected components where each component
                            is a list of node identifiers

    Returns:
        DataFrame with columns: ID_UNIQUE, SOURCE, IDI, TIM_PROCESSED
    """
    # Flatten the list of components while preserving component IDs
    records = []
    for component_id, component in enumerate(connected_components):
        for node in component:
            # Split node into source and ID parts if it contains a separator
            if "|" in node:
                source, idi = node.split("|", 1)
            else:
                source, idi = "UNKNOWN", node

            records.append(
                {
                    "ID_UNIQUE": component_id,
                    "SOURCE": source,
                    "IDI": idi,
                    "TIM_PROCESSED": datetime.datetime.now(),
                }
            )

    return pd.DataFrame(records)


def main(input_file: str, output_file: str = None) -> pd.DataFrame:
    """Main function to execute the connected components pipeline.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file (optional)

    Returns:
        DataFrame with connected components information

    Raises:
        FileNotFoundError: If input_file doesn't exist
        ValueError: If input file doesn't contain required columns
    """
    # Read input data
    print(f"Reading input data from {input_file}")
    input_table = pd.read_csv(input_file)

    # Validate input columns
    required_columns = {"LEFT_SIDE", "RIGHT_SIDE"}
    if not required_columns.issubset(input_table.columns):
        missing = required_columns - set(input_table.columns)
        raise ValueError(f"Input file missing required columns: {missing}")

    # Find connected components and measure execution time
    print("Finding connected components...")
    start_time = time.time()
    connected_components = find_connected_components(input_table)
    end_time = time.time()

    elapsed_time = end_time - start_time
    print(f"Elapsed time finding connected components: {elapsed_time:.2f} seconds")
    print(f"Found {len(connected_components)} connected components")

    # Create output DataFrame
    output_table = create_output_dataframe(connected_components)

    # Save output if file path provided
    if output_file:
        output_table.to_csv(output_file, index=False)
        print(f"Output saved to {output_file}")

    print("Connected components processing completed successfully")
    return output_table


if __name__ == "__main__":
    # Set up command line interface
    parser = argparse.ArgumentParser(
        description="Find connected components in a graph representation of data"
    )
    parser.add_argument(
        "input_file", help="Input CSV file with LEFT_SIDE and RIGHT_SIDE columns"
    )
    parser.add_argument(
        "-o",
        "--output",
        default="connected_components_output.csv",
        help="Output CSV file path (default: connected_components_output.csv)",
    )

    args = parser.parse_args()

    # Execute main function
    main(args.input_file, args.output)
