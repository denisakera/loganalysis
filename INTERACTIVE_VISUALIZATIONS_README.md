# Interactive Power Dynamics Visualizations

This directory contains interactive D3.js visualizations as a parallel component to the static analysis report.

## Files

- **`d3_visualization_data.json`**: All analysis data in D3-friendly JSON format (auto-generated)
- **`interactive_visualizations.html`**: Standalone HTML file with interactive visualizations (structural metrics)
- **`relational_interaction_visualizations.html`**: **NEW** - Dedicated interactive visualization for relational interaction analysis
- **`observable_notebook.md`**: Observable notebook cells for cloud-based visualization

## Quick Start

### Option 1: Standalone HTML (Easiest)

**Main Analysis (`interactive_visualizations.html`):**
1. Ensure `d3_visualization_data.json` is in the same directory
2. Open `interactive_visualizations.html` in any modern web browser
3. No server required - works locally!

**Features:**
- Interactive network graph (drag nodes)
- Timeline with hover details
- Participation heatmap
- Lorenz curve for inequality
- Cumulative speaking time chart
- Speaker filtering controls

**Relational Interaction Analysis (`relational_interaction_visualizations.html`):**
1. Ensure `d3_visualization_data.json` is in the same directory
2. Open `relational_interaction_visualizations.html` in any modern web browser
3. Explores power as enacted moment-by-moment

**Features:**
- **Response-Oriented Network**: Drag nodes, explore who orients to whom
  - Edge thickness = Duration of response chains
  - Edge color = Response frequency
  - Hover to see response details
- **Floor Holding Timeline**: Temporal view with interruption markers
  - Red X = Floor lost
  - Orange O = Floor maintained (tolerance)
  - Hover over markers for details
- **Interruption Tolerance**: Interactive exploration of tolerance rates
  - Who maintains floor despite interruptions
  - Color-coded by tolerance level
- **Conversational Attractors**: Who elicits extended responses
  - Duration-weighted measure
  - Hover for detailed statistics
- **Layered View**: Compare tolerance and attractor patterns together
  - Side-by-side visualization
  - Power as pattern across dimensions

### Option 2: Observable Notebook

1. Go to [observablehq.com](https://observablehq.com) and create a free account
2. Create a new notebook
3. Upload `d3_visualization_data.json` as a file attachment
4. Copy cells from `observable_notebook.md` into your notebook
5. The visualizations will automatically render

**Benefits:**
- Cloud-based, shareable via URL
- Real-time collaboration
- Easy embedding in websites
- Version control

## Interactive Features

### Network Graph
- **Drag nodes** to rearrange the network layout
- **Hover over nodes** to see speaker details (speaking time, percentage, turn count)
- **Node size** = speaking time
- **Edge thickness** = transition frequency

### Timeline
- **Hover over bars** to see episode details (speaker, time range, duration)
- Shows when each speaker was active throughout the meeting
- Top 10 speakers displayed

### Participation Heatmap
- **Hover over cells** to see segment-specific information
- **Color intensity** indicates speaking time (darker = more time)
- 20 time segments across meeting duration
- Top 15 speakers displayed

### Lorenz Curve
- Visual representation of speaking time inequality
- **Blue line** = actual distribution
- **Red dashed line** = perfect equality
- **Shaded area** = inequality magnitude
- Gini coefficient displayed

### Cumulative Chart
- **Hover over lines** to see speaker totals
- Shows how speaking time accumulates over the meeting
- Top 8 speakers tracked
- Color-coded legend

## Data Structure

The `d3_visualization_data.json` file contains:

```json
{
  "metadata": {
    "meeting_duration": 6855.06,
    "total_speakers": 27,
    "total_segments": 1119,
    "total_turns": 263
  },
  "network": {
    "nodes": [...],  // Speaker nodes with speaking time, turn count
    "links": [...]   // Transitions between speakers
  },
  "timeline": [...],           // All speaking episodes
  "cumulative": [...],          // Cumulative speaking time data
  "interruption_network": {...}, // Interruption patterns
  "transition_matrix": {...},   // Speaker transition matrix
  "turn_lengths": [...],        // Turn length distribution
  "participation_heatmap": {...}, // Temporal participation data
  "gaps": [...],                // Gap analysis data
  "lorenz_curve": [...],       // Inequality curve data
  "inequality_metrics": {...},  // Gini, entropy, etc.
  "gap_statistics": {...},      // Gap statistics
  "speaker_times": {...},       // Speaking time per speaker
  "agenda_control": {...}      // Topic introduction data
}
```

## Regenerating Data

The data file is automatically generated when you run:

```bash
python analyze_power_dynamics.py
```

This will:
1. Analyze the transcript
2. Generate static PNG visualizations
3. Export `d3_visualization_data.json` for interactive visualizations

## Customization

### Modifying Colors

In `interactive_visualizations.html`, change the color scales:

```javascript
const color = d3.scaleOrdinal(d3.schemeCategory20);  // Network/timeline
const color = d3.scaleSequential(d3.interpolateYlOrRd);  // Heatmap
```

### Adjusting Sizes

Modify the `width` and `height` variables in each visualization function.

### Adding Filters

The speaker filter controls can be extended to filter other visualizations. See the `createSpeakerControls()` function.

## Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Internet Explorer: ❌ Not supported (uses D3 v7)

## Troubleshooting

**Visualizations don't load:**
- Ensure `d3_visualization_data.json` is in the same directory
- Check browser console for errors
- Verify the JSON file is valid (not corrupted)

**Network graph nodes overlap:**
- Drag nodes to rearrange
- The force simulation will automatically adjust

**Data not updating:**
- Regenerate `d3_visualization_data.json` by running the Python script
- Clear browser cache and reload

## Integration with Report

These interactive visualizations complement the static PNG images in `power_structures_report.md`:

- **Static PNGs**: For documentation, printing, PDFs
- **Interactive HTML - Main Analysis**: For exploration of structural metrics (speaking time, transitions, etc.)
- **Interactive HTML - Relational Analysis**: For exploration of relational interaction patterns (tolerance, attractors, responses)
- **Observable Notebook**: For collaboration, embedding, version control

Both approaches use the same underlying data and metrics, ensuring consistency.

## Two Analysis Layers

The visualizations are organized into two complementary layers:

1. **Structural Metrics** (`interactive_visualizations.html`):
   - Speaking time dominance
   - Turn-taking structure
   - Transition patterns
   - Participation distribution
   - Inequality measures

2. **Relational Interaction** (`relational_interaction_visualizations.html`):
   - Response-oriented networks (who orients to whom)
   - Interruption tolerance (who maintains floor despite disruption)
   - Conversational attractors (who elicits extended responses)
   - Layered power patterns (reading power across dimensions)

These layers can be explored separately or together to understand power as both structural and relational.

## License

Same license as the main analysis project.
