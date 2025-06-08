# Diagram Generator MCP Server Tests

This directory contains comprehensive tests for the Diagram Generator MCP server, organized into focused test modules for better maintainability and clarity.

## Test Organization

### Master Test Runner
- **`../test_all.py`** - Master test runner at the project root that orchestrates all tests

### Individual Test Modules
- **`test_server_initialization.py`** - Server startup and basic functionality tests
- **`test_component_listing.py`** - Component listing and discovery tests
- **`test_simple_diagrams.py`** - Simple diagram generation tests
- **`test_clustered_diagrams.py`** - Clustered diagram generation tests
- **`test_aws_diagrams.py`** - AWS-specific diagram tests
- **`test_kubernetes_diagrams.py`** - Kubernetes diagram tests
- **`test_microservices_diagrams.py`** - Microservices architecture diagram tests
- **`test_error_handling.py`** - Error handling and edge case tests
- **`test_tool_validation.py`** - Tool metadata and validation tests

### Base Classes
- **`base_test.py`** - Common test utilities and base classes

### Legacy Files
- **`test_server.py`** - ⚠️ Legacy combined test file (deprecated)

## Running Tests

### Option 1: Master Test Runner (Recommended)
```bash
# Run all tests
python test_all.py

# Run basic tests only
python test_all.py --fast

# Run with verbose output
python test_all.py --verbose

# Run component tests only
python test_all.py --component

# Run integration tests only
python test_all.py --integration
```

### Option 2: Individual Test Modules
```bash
# Run specific test categories
python -m pytest tests/test_simple_diagrams.py -v
python -m pytest tests/test_aws_diagrams.py -v
python -m pytest tests/test_error_handling.py -v

# Run all tests in the tests directory
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Option 3: Legacy Combined Tests
```bash
# Run the legacy combined test file
python -m pytest tests/test_server.py -v

# Or run directly
cd tests && python test_server.py
```

## Test Structure

### Base Test Class
All test classes inherit from `BaseMCPTest` which provides:
- `create_test_server()` - Creates MCP server instance for testing
- `call_tool_and_verify_success()` - Helper for calling tools and verifying responses
- `verify_diagram_response()` - Helper for validating diagram generation responses

### Test Categories

#### Server Initialization Tests
- Server startup and initialization
- Tool discovery and listing
- Basic server capabilities

#### Component Tests
- Available component listing
- Component type validation
- Provider and category verification

#### Diagram Generation Tests
- Simple diagrams with components and connections
- Clustered diagrams with grouped components
- Predefined architecture patterns (AWS, Kubernetes, Microservices)
- Custom parameters and options
- Different output formats

#### Error Handling Tests
- Invalid component types
- Missing required parameters
- Empty or malformed inputs
- Edge cases and boundary conditions

#### Tool Validation Tests
- Tool metadata verification
- Input schema validation
- Parameter validation
- Response format consistency

## Test Dependencies

The tests require:
- `pytest` - Test framework
- `mcp` - Model Context Protocol SDK
- All diagram generator dependencies

Install test dependencies:
```bash
pip install -r requirements.txt
pip install pytest pytest-asyncio pytest-cov
```

## Test Configuration

### Environment Variables
Tests can be configured with environment variables:
- `TEST_OUTPUT_DIR` - Directory for test diagram outputs (default: `/tmp/`)
- `TEST_TIMEOUT` - Test timeout in seconds (default: 30)

### Docker Volume Mounting
The tests assume diagrams are saved to `/tmp/` which should be mounted as a Docker volume in production.

## Coverage Reports

Generate test coverage reports:
```bash
# HTML coverage report
python -m pytest tests/ --cov=. --cov-report=html

# Terminal coverage report
python -m pytest tests/ --cov=. --cov-report=term-missing

# Coverage data file
python -m pytest tests/ --cov=. --cov-report=xml
```

## Adding New Tests

When adding new tests:

1. **Create focused test files** for new functionality
2. **Inherit from `BaseMCPTest`** for common functionality
3. **Use async test methods** with `@pytest.mark.asyncio`
4. **Add to master test runner** in `test_all.py`
5. **Include error handling tests** for edge cases
6. **Document test purpose** with clear docstrings

### Example Test Structure
```python
from .base_test import AsyncMCPTest

class TestNewFeature(AsyncMCPTest):
    """Test suite for new feature."""
    
    async def test_basic_functionality(self):
        """Test basic functionality of new feature."""
        mcp = self.create_test_server()
        # ... test implementation
    
    async def test_error_cases(self):
        """Test error handling for new feature."""
        # ... error test implementation
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running tests from the project root
2. **MCP Server Not Starting**: Check server dependencies and configuration
3. **Tool Not Found**: Verify tool registration in server.py
4. **Timeout Errors**: Increase test timeout or check server performance

### Debug Mode
Run tests with additional debugging:
```bash
python test_all.py --verbose
python -m pytest tests/ -v -s --tb=long
```
