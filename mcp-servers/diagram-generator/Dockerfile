FROM python:3.11-slim

# Install graphviz (required for diagrams library)
RUN apt-get update && \
    apt-get install -y --no-install-recommends graphviz && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set the output directory for diagrams
ENV DIAGRAM_OUTPUT_DIR=/tmp

# Run the MCP server
CMD ["python", "server.py"]
