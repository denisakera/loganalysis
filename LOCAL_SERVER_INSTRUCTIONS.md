# How to View Interactive Visualizations Locally

## Problem

Modern browsers block local file access via `fetch()` due to CORS (Cross-Origin Resource Sharing) security restrictions. When you open HTML files directly (file://), you'll see:

```
Error: Could not load d3_visualization_data.json. Please ensure the file is in the same directory.
```

## Solution: Use Local Server

### Quick Start

1. **Generate Data** (if not already done):
   ```bash
   python analyze_power_dynamics.py
   ```

2. **Start Local Server**:
   ```bash
   python start_local_server.py
   ```

3. **Open in Browser**:
   - The server will automatically open your browser
   - Or manually navigate to: http://localhost:8000/interactive_visualizations.html

### Available Visualizations

Once the server is running, access:

- **Main Analysis**: http://localhost:8000/interactive_visualizations.html
- **Relational Interaction**: http://localhost:8000/relational_interaction_visualizations.html
- **Topic Emergence**: http://localhost:8000/topic_emergence_visualizations.html
- **Fine-Grained Power**: http://localhost:8000/fine_grained_power_visualizations.html

### Stop Server

Press `Ctrl+C` in the terminal to stop the server.

## Alternative: Python HTTP Server

If `start_local_server.py` doesn't work, use Python's built-in server:

```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Then open: http://localhost:8000/interactive_visualizations.html

## Why This Is Needed

Browsers enforce CORS to prevent malicious websites from accessing local files. A local HTTP server makes the files available via HTTP protocol, which browsers allow.
