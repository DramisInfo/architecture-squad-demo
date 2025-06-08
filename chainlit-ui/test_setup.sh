#!/bin/bash
# Test script for Chainlit app with MCP diagram generation

echo "🧪 Testing Chainlit App with MCP Integration"
echo "============================================"

cd /home/ubuntu/repos/architecture-squad-demo/chainlit-ui

echo "📁 Checking directory structure..."
ls -la public/diagrams/ 2>/dev/null || echo "Creating public/diagrams directory..."
mkdir -p public/diagrams

echo "🔧 Checking environment variables..."
if [ -z "$GITHUB_TOKEN" ]; then
    echo "⚠️  Warning: GITHUB_TOKEN not set"
else
    echo "✅ GITHUB_TOKEN is set"
fi

echo "📦 Testing imports..."
python -c "
import sys
from pathlib import Path
sys.path.append(str(Path('.').parent / 'architecture-squad'))

try:
    from utils import create_kernel, create_architecture_group_chat_async
    print('✅ Architecture squad modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')

try:
    import chainlit as cl
    print('✅ Chainlit imported successfully')
except ImportError as e:
    print(f'❌ Chainlit import error: {e}')
"

echo "🚀 To start the Chainlit app:"
echo "   cd /home/ubuntu/repos/architecture-squad-demo/chainlit-ui"
echo "   chainlit run app.py --host 0.0.0.0 --port 8000"
echo ""
echo "Then open: http://localhost:8000"
echo ""
echo "🎯 Test with this example requirement:"
echo "   'Design a microservices architecture for an e-commerce platform on Azure'"
echo ""
echo "✅ Setup complete! The app will:"
echo "   - Initialize Architecture Squad with MCP diagram generation"
echo "   - Generate visual architecture diagrams"
echo "   - Display diagrams inline with documentation"
echo "   - Save diagrams to public/diagrams/ directory"
