#!/usr/bin/env python3
"""
Test script to verify Chainlit image display functionality
"""

import asyncio
import os
from pathlib import Path
import chainlit as cl

# Test data
TEST_DIAGRAM_FILES = [
    "/home/ubuntu/repos/architecture-squad-demo/chainlit-ui/public/diagrams/Azure_APIM_Self-Hosted_Gateway_on_OpenShift_20250608_013901_2f363c1f.png",
    "/home/ubuntu/repos/architecture-squad-demo/chainlit-ui/public/diagrams/Azure_API_Management_Self-hosted_Gateway_on_OpenShift_-_Deployment_Architecture_20250608_014504_e6012570.png"
]


def test_url_path_conversion():
    """Test the URL path conversion logic"""
    print("🧪 Testing URL path conversion...")

    for diagram_path in TEST_DIAGRAM_FILES:
        if os.path.exists(diagram_path):
            filename = os.path.basename(diagram_path)
            url_path = f"/public/diagrams/{filename}"

            print(f"✅ Original path: {diagram_path}")
            print(f"✅ Converted URL: {url_path}")
            print(f"✅ File exists: {os.path.exists(diagram_path)}")
            print("---")
        else:
            print(f"❌ File not found: {diagram_path}")


def test_chainlit_image_element_creation():
    """Test Chainlit Image element creation"""
    print("\n🎨 Testing Chainlit Image element creation...")

    for diagram_path in TEST_DIAGRAM_FILES:
        if os.path.exists(diagram_path):
            filename = os.path.basename(diagram_path)
            url_path = f"/public/diagrams/{filename}"

            try:
                # This is how the image element should be created
                image_element = cl.Image(
                    path=url_path,
                    name=filename,
                    display="inline"
                )
                print(f"✅ Image element created successfully for: {filename}")
                print(f"   - Path: {image_element.path}")
                print(f"   - Name: {image_element.name}")
                print(f"   - Display: {image_element.display}")
                print("---")
            except Exception as e:
                print(f"❌ Error creating image element for {filename}: {e}")


def main():
    """Run all tests"""
    print("🔍 Testing Chainlit Image Display Fix\n")

    # Check if diagram files exist
    public_dir = Path(
        "/home/ubuntu/repos/architecture-squad-demo/chainlit-ui/public/diagrams")
    print(f"📁 Public diagrams directory: {public_dir}")
    print(f"📁 Directory exists: {public_dir.exists()}")

    if public_dir.exists():
        diagram_files = list(public_dir.glob("*.png"))
        print(f"📊 Found {len(diagram_files)} diagram files")
        for file in diagram_files:
            print(f"   - {file.name}")

    print("\n" + "="*60 + "\n")

    # Run tests
    test_url_path_conversion()
    test_chainlit_image_element_creation()

    print("\n✅ All tests completed!")
    print("\n🌐 To test in browser:")
    print("1. Make sure Chainlit server is running: chainlit run app.py")
    print("2. Open browser to: http://localhost:8000")
    print("3. Test direct image access:")
    for diagram_path in TEST_DIAGRAM_FILES:
        if os.path.exists(diagram_path):
            filename = os.path.basename(diagram_path)
            print(f"   - http://localhost:8000/public/diagrams/{filename}")


if __name__ == "__main__":
    main()
