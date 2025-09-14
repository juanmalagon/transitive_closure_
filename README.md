# Connected Components Analysis Tool

A high-performance Python tool for identifying connected components in graph data represented by CSV files. This tool processes relationships between entities and groups them into equivalence classes using an optimized transitive closure algorithm.

## Features

- **Efficient Graph Processing**: Uses depth-first search (DFS) with sparse matrix operations
- **Symmetric Relation Handling**: Automatically creates symmetric closure of input relations
- **Flexible Input Format**: Supports various identifier formats with automatic parsing
- **Comprehensive Output**: Generates component identifiers with source tracking and processing timestamps
- **Robust Error Handling**: Validates input data and provides clear error messages

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Dependencies

```bash
pip install pandas scipy
```

## Usage

### Command Line Interface

```bash
python connected_components.py input.csv -o output.csv
```

### Required Input Format

Input CSV must contain these exact column names:
- `LEFT_SIDE`: Entity identifiers (format: "SOURCE|ID" or simple identifiers)
- `RIGHT_SIDE`: Related entity identifiers (same format as LEFT_SIDE)

Example input:
```csv
LEFT_SIDE,RIGHT_SIDE
A|1,B|2
B|2,C|3
D|4,E|5
```

### Output Format

The tool generates a CSV file with these columns:
- `ID_UNIQUE`: Unique identifier for each connected component
- `SOURCE`: Source system extracted from the entity identifier
- `IDI`: Local identifier within the source system
- `TIM_PROCESSED`: Processing timestamp

Example output:
```csv
ID_UNIQUE,SOURCE,IDI,TIM_PROCESSED
0,A,1,2023-08-15 14:30:45.123456
0,B,2,2023-08-15 14:30:45.123456
0,C,3,2023-08-15 14:30:45.123456
1,D,4,2023-08-15 14:30:45.123456
1,E,5,2023-08-15 14:30:45.123456
```

## Algorithm Implementation

The tool implements a three-phase approach:

1. **Graph Construction**: Builds directed graph from input pairs
2. **Symmetric Closure**: Creates bidirectional relationships between all connected nodes
3. **Transitive Closure**: Computes reachability using DFS with sparse matrix optimization
4. **Equivalence Classes**: Groups mutually reachable nodes into components

Key implementation details:
- Uses SciPy's sparse matrices for memory efficiency
- Handles self-references and circular relationships
- Processes nodes with or without source identifiers
- Efficiently manages large graphs through optimized DFS

## Project Structure

```
.
├── connected_components.py  # Main processing pipeline
├── functions.py            # Core graph algorithms
├── test_connected_components.py  # Comprehensive test suite
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```

## Performance Characteristics

- Time Complexity: O(V²) worst-case, optimized for sparse graphs
- Memory Efficiency: Uses sparse matrix representation (LIL format)
- Scalability: Suitable for graphs with up to 10^5 nodes on standard hardware

## Testing

Run the comprehensive test suite:
```bash
python -m unittest test_connected_components.py
```

Tests cover:
- Basic connected component detection
- Edge cases (self-references, disconnected graphs)
- Error handling (missing columns, empty input)
- Integration tests with file I/O

## Error Handling

The tool validates:
- Presence of required columns (LEFT_SIDE, RIGHT_SIDE)
- Proper file format and accessibility
- Correct identifier parsing and processing

## Example Use Cases

1. **Data Integration**: Identifying equivalent entities across different systems
2. **Network Analysis**: Finding connected devices or users in network graphs
3. **Entity Resolution**: Grouping duplicate records in database systems
4. **Social Network Analysis**: Discovering communities and relationships

## License

Apache License 2.0 - See LICENSE file for details.

## Support

For issues and questions:
1. Check existing tests for usage examples
2. Ensure input format matches requirements
3. Verify all dependencies are installed

## Contributing

1. Follow existing code style and patterns
2. Add tests for new functionality
3. Update documentation for changes
4. Ensure all tests pass before submitting
