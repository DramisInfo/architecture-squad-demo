# Diagram Generator MCP Server - Modular Structure

## Overview
The Diagram Generator MCP Server has been reorganized into a clean, modular structure for better maintainability and scalability.

## Folder Structure

```
diagram-generator/
├── server.py                          # Main MCP server entry point
├── requirements.txt                   # Dependencies
├── README.md                         # Documentation
├── .env.example                      # Environment template
│
├── core/                             # Core functionality
│   ├── __init__.py
│   ├── config.py                     # Configuration and constants
│   └── utils.py                      # Utility functions
│
├── diagram_generators/               # Diagram generation modules
│   ├── __init__.py
│   ├── simple_diagram.py            # Simple diagrams
│   ├── clustered_diagram.py         # Clustered diagrams
│   ├── aws_diagrams.py              # AWS-specific templates
│   ├── kubernetes_diagrams.py       # Kubernetes templates
│   └── microservices_diagrams.py    # Microservices templates
│
└── tests/                            # Test modules
    ├── __init__.py
    └── test_server.py                # MCP server tests
```

## Module Responsibilities

### Core Module (`core/`)

#### `config.py`
- **Purpose**: Central configuration and imports
- **Contains**: 
  - Library imports (diagrams, fastmcp, etc.)
  - Component mappings for all cloud providers
  - Global constants (volume mount paths, etc.)
  - Logging configuration

#### `utils.py`
- **Purpose**: Shared utility functions
- **Contains**:
  - `generate_unique_filename()` - Creates unique filenames for diagrams
  - `get_component_class()` - Retrieves diagram component classes
  - `list_available_components()` - Lists all available components

### Diagram Generators Module (`diagram_generators/`)

#### `simple_diagram.py`
- **Purpose**: Basic diagram generation
- **Function**: `generate_simple_diagram()`
- **Features**: Simple component layouts with connections

#### `clustered_diagram.py`
- **Purpose**: Grouped/clustered diagram generation
- **Function**: `generate_clustered_diagram()`
- **Features**: Components organized in logical clusters

#### `aws_diagrams.py`
- **Purpose**: AWS-specific diagram templates
- **Function**: `generate_aws_web_app_diagram()`
- **Features**: Pre-configured AWS web application architecture

#### `kubernetes_diagrams.py`
- **Purpose**: Kubernetes-specific diagram templates
- **Function**: `generate_kubernetes_diagram()`
- **Features**: Pod, service, and deployment layouts

#### `microservices_diagrams.py`
- **Purpose**: Microservices architecture templates
- **Function**: `generate_microservices_diagram()`
- **Features**: Multi-cloud microservices patterns

### Tests Module (`tests/`)

#### `test_server.py`
- **Purpose**: Comprehensive MCP server testing
- **Features**: 
  - Official MCP SDK test patterns
  - All tool functionality tests
  - Error handling validation

## Import Structure

The new modular structure uses clean imports:

```python
# Main server (server.py)
from core.config import logger
from core.utils import list_available_components
from diagram_generators.simple_diagram import generate_simple_diagram
from diagram_generators.clustered_diagram import generate_clustered_diagram
# ... etc

# Diagram generators
from core.config import Diagram, Edge, logger
from core.utils import generate_unique_filename, get_component_class

# Tests
from diagram_generators.simple_diagram import generate_simple_diagram
from core.utils import list_available_components
```

## Benefits of New Structure

### 1. **Separation of Concerns**
- Configuration isolated in `core/config.py`
- Utilities separated from business logic
- Each diagram type has its own module

### 2. **Maintainability**
- Small, focused files (< 100 lines each)
- Clear module boundaries
- Easy to locate and modify specific functionality

### 3. **Scalability**
- Easy to add new diagram types
- Simple to extend existing functionality
- Clear patterns for new contributors

### 4. **Testing**
- Isolated modules are easier to test
- Clear import structure for test setup
- Each module can be tested independently

### 5. **Code Organization**
- Related functionality grouped together
- Consistent naming conventions
- Clear dependency management

## Usage

The server maintains the same external API while providing improved internal organization:

```python
# Start the server
python server.py

# All tools remain available:
# - generate_simple_diagram
# - generate_clustered_diagram  
# - generate_aws_web_app_diagram
# - generate_kubernetes_diagram
# - generate_microservices_diagram
# - list_available_components
```

## Development Workflow

### Adding New Diagram Types
1. Create new file in `diagram_generators/`
2. Import required dependencies from `core/`
3. Implement diagram generation function
4. Register function in `server.py`
5. Add tests in `tests/test_server.py`

### Adding New Cloud Providers
1. Update component mappings in `core/config.py`
2. Create provider-specific diagram modules
3. Update utility functions if needed
4. Add comprehensive tests

### Extending Functionality
1. Add utilities to `core/utils.py`
2. Update configuration in `core/config.py` 
3. Modify relevant diagram generators
4. Ensure tests cover new functionality

This modular structure makes the codebase much more maintainable while preserving all existing functionality and providing a clear path for future enhancements.
