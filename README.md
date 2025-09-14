# Connected Components Analysis Tool

A Python-based tool for identifying connected components in graph data represented by CSV files. This tool processes pairs of connected nodes and groups them into equivalence classes (connected components) using an efficient transitive closure algorithm.

## Features

- **Efficient Graph Processing**: Uses depth-first search (DFS) for transitive closure computation
- **Scalable**: Handles large datasets using sparse matrix representations
- **Flexible Input**: Works with any CSV containing node pairs
- **Comprehensive Output**: Generates component IDs with source tracking and timestamps

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone git@github.com:juanmalagon/transitive_closure_.git
cd transitive_closure_
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Command Line Usage

```bash
python connected_components.py input.csv
```

This will process `input.csv` and create an output file named `connected_components_output.csv`.

### Advanced Options

```bash
python connected_components.py input.csv -o custom_output.csv
```

### Input File Format

Your input CSV file must contain at least these two columns:
- `LEFT_SIDE`: Node identifiers (format: "SOURCE|ID")
- `RIGHT_SIDE`: Node identifiers (format: "SOURCE|ID")

Example input:
```csv
LEFT_SIDE,RIGHT_SIDE
SOURCE_A|123,SOURCE_B|456
SOURCE_B|456,SOURCE_C|789
SOURCE_D|101,SOURCE_E|112
```

### Output Format

The tool generates a CSV file with the following columns:
- `ID_UNIQUE`: Unique identifier for each connected component
- `SOURCE`: The source system of the node
- `IDI`: The identifier within the source system
- `TIM_PROCESSED`: Timestamp when processing occurred

Example output:
```csv
ID_UNIQUE,SOURCE,IDI,TIM_PROCESSED
0,SOURCE_A,123,2023-08-15 14:30:45.123456
0,SOURCE_B,456,2023-08-15 14:30:45.123456
0,SOURCE_C,789,2023-08-15 14:30:45.123456
1,SOURCE_D,101,2023-08-15 14:30:45.123456
1,SOURCE_E,112,2023-08-15 14:30:45.123456
```

## Algorithm Details

The tool uses a two-phase approach to identify connected components:

1. **Graph Construction**: Builds a directed graph from the input pairs
2. **Transitive Closure**: Computes the transitive closure using DFS to identify all connected nodes
3. **Equivalence Classes**: Groups nodes that are mutually reachable into components

The implementation uses SciPy's sparse matrices for memory efficiency with large graphs.

## Project Structure

```
connected-components-tool/
├── connected_components.py  # Main executable script
├── functions.py            # Graph algorithms implementation
├── requirements.txt        # Python dependencies
├── LICENSE                 # Apache 2.0 License
└── README.md              # This file
```

## Development

### Code Style

This project follows PEP 8 guidelines with comprehensive type hints and docstrings. To ensure code quality:

1. Install development requirements:
```bash
pip install -r requirements-dev.txt
```

2. Run linting:
```bash
flake8 connected_components.py functions.py
```

3. Run type checking:
```bash
mypy connected_components.py functions.py
```

### Extending Functionality

The code is structured to be easily extensible:

1. **Adding New Relation Types**: Modify the `is_related` function in `connected_components.py`
2. **Custom Output Formats**: Extend the `create_output_dataframe` function
3. **Alternative Algorithms**: Implement new algorithms in `functions.py`

## Performance Considerations

- For very large graphs (>1M nodes), consider increasing available memory
- The algorithm has O(V²) time complexity in worst case but uses sparse matrices for efficiency
- Memory usage is optimized through sparse matrix representations

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For questions or issues, please open an issue in the GitHub repository with:
1. A description of the problem
2. Steps to reproduce
3. Example input data (if possible)
4. Error messages or unexpected outputs

## Acknowledgments

- Uses Pandas for data manipulation
- Uses SciPy for efficient sparse matrix operations
- Algorithm based on standard graph theory approaches for connected components