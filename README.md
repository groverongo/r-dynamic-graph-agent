# Graph Analysis Agent

A Python-based agent for analyzing and explaining graph structures using LangChain and Google's Gemini model. This tool allows you to interactively explore graph properties and get explanations about graph theory concepts.

## Features

- Analyze graph structures using adjacency lists
- Interactive Q&A about graph properties
- Built-in tools for graph analysis (degree, connectivity, etc.)
- Powered by Google's Gemini AI model
- Easy integration with custom graphs

## Prerequisites

- Python 3.13 or higher
- Google API key for Gemini

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/graph-agent.git
   cd graph-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root and add your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

## Usage

### Running the Agent

```bash
poe start
```

### Using a Custom Graph

You can analyze your own graph by modifying the `__main__` section in `main.py`:

```python
if __name__ == "__main__":
    # Define your custom graph as an adjacency list
    custom_graph = {
        'a': ['b', 'd'],
        'b': ['a', 'c'],
        'c': ['b', 'd', 'e'],
        'd': ['a', 'c', 'e'],
        'e': ['c', 'd']
    }
    run_graph_agent(custom_graph)
```

## Available Tools

The agent comes with the following built-in tools:

- `graph_details`: Provides basic information about the graph including:
  - Maximum and minimum degree
  - Number of vertices
  - Number of edges

## Development

### Running Tests

```bash
poe test
```

### Linting

```bash
poe lint
```

## Dependencies

- langchain-google-genai: For Google's Gemini model integration
- langgraph: For building and managing the agent's workflow
- ruff: For code linting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.