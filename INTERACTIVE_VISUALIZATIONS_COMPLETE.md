# Complete Interactive Visualizations Guide

## ✅ All Analysis Now Available Interactively

All analyses, including the **fine-grained topic-speaker relations**, are now available as interactive visualizations!

## 🚀 Quick Start

### Step 1: Generate Data
```bash
python analyze_power_dynamics.py
```
This creates `d3_visualization_data.json` with ALL analysis data.

### Step 2: Start Local Server
```bash
python start_local_server.py
```
This starts a local HTTP server (required due to browser CORS restrictions).

### Step 3: Open Visualizations
The server will automatically open your browser. Or manually navigate to:

- **Main Analysis**: http://localhost:8000/interactive_visualizations.html
- **Relational Interaction**: http://localhost:8000/relational_interaction_visualizations.html  
- **Topic Emergence**: http://localhost:8000/topic_emergence_visualizations.html
- **Fine-Grained Power**: http://localhost:8000/fine_grained_power_visualizations.html ⭐ **NEW**

## 📊 Available Interactive Visualizations

### 1. Main Interactive Visualizations (`interactive_visualizations.html`)
**Structural Power Dynamics:**
- Interactive network graph (drag nodes)
- Timeline with hover details
- Participation heatmap
- Lorenz curve for inequality
- Cumulative speaking time chart
- Speaker filtering controls

### 2. Relational Interaction Visualizations (`relational_interaction_visualizations.html`)
**Power as Enacted Moment-by-Moment:**
- Response-Oriented Network (drag nodes, explore who orients to whom)
- Floor Holding Timeline (interruption markers)
- Interruption Tolerance (who maintains floor despite interruptions)
- Conversational Attractors (who elicits extended responses)
- Layered View (compare tolerance and attractor patterns)

### 3. Topic Emergence Visualizations (`topic_emergence_visualizations.html`)
**Topics as Emergent Interactional Objects:**
- Topic Timeline (interactive with hover details, filter by status)
- Speaker-Topic Network (drag nodes, explore proposal and response relationships)
- Topic Trajectories (see how topics travel between speakers)
- Stabilization Rates (agenda setting success)
- Orientation Patterns (who responds to which topics, with what delay)

### 4. Fine-Grained Power Visualizations (`fine_grained_power_visualizations.html`) ⭐ **NEW**
**Power as Interactional Structure:**
- **Topic Closure Authority**: Who can end topics without contest
  - Interactive bars showing uncontested closure rates
  - Hover for detailed statistics
- **Asymmetric Topical Accountability**: Who is asked to clarify/justify
  - Color-coded by accountability level (red=high, green=low)
  - Reveals epistemic standing
- **Topic Hijacking vs Alignment**: Who reframes topics while preserving legitimacy
  - Stacked bars showing hijacking/reframing/shift/alignment patterns
  - Subtle control vs complete shifts
- **Topic Recycling**: Topics that gain traction when repositioned
  - Shows authority as relational rather than propositional

## 🔧 Troubleshooting

### Error: "Could not load d3_visualization_data.json"

**Solution:** Use the local server:
```bash
python start_local_server.py
```

Then open the HTML files via http://localhost:8000/...

### Why Local Server is Needed

Modern browsers block local file access (`file://`) via `fetch()` due to CORS security. A local HTTP server makes files available via HTTP protocol, which browsers allow.

### Alternative: Python Built-in Server

If `start_local_server.py` doesn't work:
```bash
python -m http.server 8000
```

## 📁 Data Structure

The `d3_visualization_data.json` file contains:

- `metadata`: Meeting duration, speaker count, etc.
- `network`: Speaker network graph data
- `timeline`: All segments with timestamps
- `relational_interaction`: Response networks, tolerance rates, attractors
- `topic_emergence`: Topics, speaker orientations, content
- `fine_grained_relations`: ⭐ **NEW**
  - `topic_closures`: Closure authority data
  - `accountability_patterns`: Epistemic standing patterns
  - `recycled_topics`: Topic recycling cases
  - `topic_hijackings`: Hijacking/reframing patterns

## 🎯 All Analyses Now Interactive

✅ Structural metrics (speaking time, turn counts)  
✅ Relational interaction (response patterns, tolerance)  
✅ Topic emergence (topics as interactional objects)  
✅ Fine-grained relations (closure authority, accountability, hijacking, recycling) ⭐

Everything is now available interactively!
