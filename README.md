# Organizational Power Dynamics Analysis

A comprehensive analysis system for examining interactional power dynamics in organizational meetings through computational linguistics, network analysis, and conversation analysis methods.

## Overview

This project analyzes time-aligned debate transcripts to extract, quantify, and visualize interactional power dynamics. It examines how speakers relate to each other, how they engage with topics, and how power is enacted through conversational structure rather than formal authority.

**Key Finding:** Power in organizations is **decoupled from speaking time**. The most vocal participants do not necessarily control the agenda or influence decisions. Power appears through **agenda-setting capacity**, **structural control**, and **epistemic authority**.

## Repository Structure

```
loganalysis/
│
├── 📊 DATA FILES
│   ├── amuta_2026-01-12_1.json          # Original time-aligned transcript data
│   ├── d3_visualization_data.json        # Processed data for D3.js visualizations
│   ├── llm_topic_annotations.json       # LLM-generated topic annotations
│   ├── power_dynamics_report.json       # Structured power dynamics metrics
│   ├── topic_content_analysis.txt       # Full topic content analysis
│   ├── fine_grained_topic_power_analysis.txt  # Fine-grained topic-speaker relations
│   ├── topic_engagement_power_analysis.txt    # Topic engagement patterns
│   └── llm_hybrid_analysis_report.txt    # Combined structural + LLM analysis
│
├── 🐍 PYTHON SCRIPTS
│   ├── analyze_power_dynamics.py        # Main analysis script (structural analysis)
│   ├── llm_topic_analysis.py            # LLM-based topic analysis module
│   ├── integrate_llm_results.py         # Integration of structural + LLM analysis
│   ├── run_llm_analysis.py              # Orchestrates LLM analysis workflow
│   ├── generate_llm_report.py           # Generates reports from LLM analysis
│   └── start_local_server.py            # Local HTTP server for interactive visualizations
│
├── 📄 MAIN REPORTS
│   ├── ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md  # ⭐ Comprehensive organizational report
│   ├── SPEAKER_ANIMAL_METAPHORS.md               # Animal metaphors for power dynamics
│   ├── power_structures_report.md                 # Detailed power structures analysis
│   ├── FINE_GRAINED_POWER_SUMMARY.md             # Fine-grained topic-speaker relations
│   └── TOPIC_ENGAGEMENT_SUMMARY.md                # Topic engagement patterns
│
├── 🤖 LLM ANALYSIS REPORTS
│   ├── LLM_ANALYSIS_COMPREHENSIVE_REPORT.md      # Full LLM analysis findings
│   ├── LLM_ANALYSIS_EXECUTIVE_SUMMARY.md          # Executive summary of LLM analysis
│   └── llm_analysis_summary_report.md             # Summary of LLM insights
│
├── 📖 DOCUMENTATION
│   ├── LLM_ANALYSIS_README.md                    # LLM analysis system documentation
│   ├── QUICK_START_LLM.md                        # Quick start guide for LLM analysis
│   ├── INTERACTIVE_VISUALIZATIONS_COMPLETE.md     # Complete guide to interactive visualizations
│   ├── INTERACTIVE_VISUALIZATIONS_README.md       # Interactive visualizations overview
│   ├── LOCAL_SERVER_INSTRUCTIONS.md               # Instructions for local server
│   └── methodological_note.txt                    # Methodological notes
│
├── 🎨 VISUALIZATIONS (PNG)
│   ├── speaking_time_distribution.png            # Speaking time distribution
│   ├── speaking_timeline.png                     # Temporal speaking patterns
│   ├── cumulative_speaking_time.png             # Cumulative speaking time
│   ├── turn_length_distribution.png             # Turn-taking patterns
│   ├── transition_heatmap.png                   # Speaker-to-speaker transitions
│   ├── participation_heatmap.png                # Participation patterns
│   ├── speaker_network.png                      # Speaker interaction network
│   ├── interruption_network.png                  # Interruption patterns
│   ├── interruption_tolerance.png               # Interruption tolerance analysis
│   ├── floor_holding_interruptions.png           # Floor holding patterns
│   ├── response_oriented_network.png             # Response-oriented network
│   ├── conversational_attractors.png             # Conversational attractors
│   ├── speaker_topic_network.png                 # Speaker-topic bipartite network
│   ├── speaker_topic_engagement_matrix.png       # Engagement matrix
│   ├── topic_timeline.png                        # Topic emergence timeline
│   ├── topic_trajectories.png                    # Topic trajectory visualization
│   ├── topic_content_table.png                   # Topic content visualization
│   ├── inequality_lorenz_curve.png              # Inequality metrics (Lorenz curve)
│   └── gap_analysis.png                          # Gap analysis
│
├── 🌐 INTERACTIVE VISUALIZATIONS (HTML)
│   ├── [interactive_visualizations.html](interactive_visualizations.html)          # Main interactive dashboard
│   ├── [relational_interaction_visualizations.html](relational_interaction_visualizations.html)  # Relational interaction views
│   ├── [topic_emergence_visualizations.html](topic_emergence_visualizations.html)       # Topic emergence interactive
│   └── [fine_grained_power_visualizations.html](fine_grained_power_visualizations.html)    # Fine-grained power relations
│
├── 📝 ADDITIONAL FILES
│   ├── observable_notebook.md                   # Observable notebook format
│   └── topic_emergence_methodology.txt           # Topic detection methodology
│
└── ⚙️ CONFIGURATION
    ├── .gitignore                                # Git ignore rules (excludes .env, __pycache__)
    └── .env                                      # Environment variables (NOT in repo - API keys)
```

## Quick Start

### 1. Structural Analysis (No API Keys Required)

Run the main power dynamics analysis:

```bash
python analyze_power_dynamics.py
```

This generates:
- All PNG visualizations
- JSON data files
- Text analysis reports
- HTML interactive visualizations

### 2. Interactive Visualizations

Start the local server to view interactive D3.js visualizations:

```bash
python start_local_server.py
```

Then open `http://localhost:8000/interactive_visualizations.html` in your browser.

### 3. LLM Analysis (Requires OpenAI API Key)

Set up your API key in `.env`:
```
OPENAI_API_KEY=your_key_here
```

Run LLM analysis:
```bash
python run_llm_analysis.py
```

Generate reports:
```bash
python generate_llm_report.py
```

## Key Reports

### 📊 Main Organizational Report
**[`ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md`](ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md)** - Comprehensive summary covering:
- Speaker-to-speaker relations
- Speaker-topic relations
- Overall power dynamics
- Animal metaphors (how speakers imagine the organizational "jungle")
- Institutional imagination analysis
- Recommendations for organizational development

### 🦁 Animal Metaphors
**[`SPEAKER_ANIMAL_METAPHORS.md`](SPEAKER_ANIMAL_METAPHORS.md)** - Ironic, fable-like descriptions of speakers:
- **🦅 Eagles & 🐺 Wolves:** Strategic hunters (successful agenda setters)
- **🦁 Lions & 🐘 Elephants:** Dominant presence but unsuccessful hunters
- **🐆 Leopards:** Stealthy success despite minimal presence
- **🐒 Monkeys & 🦊 Foxes:** Agile and responsive
- **🐢 Tortoises & 🦎 Lizards:** Vulnerable, frequently challenged
- **🐁 Mice:** Marginalized, rarely heard

### 🔍 Fine-Grained Analysis
**[`FINE_GRAINED_POWER_SUMMARY.md`](FINE_GRAINED_POWER_SUMMARY.md)** - Detailed topic-speaker relations:
- Topic closure authority
- Asymmetric topical accountability
- Topic recycling patterns
- Topic hijacking vs. alignment

### 🤖 LLM Analysis Reports
- **[`LLM_ANALYSIS_COMPREHENSIVE_REPORT.md`](LLM_ANALYSIS_COMPREHENSIVE_REPORT.md)** - Full interpretive analysis using GPT-4o-mini
- **[`LLM_ANALYSIS_EXECUTIVE_SUMMARY.md`](LLM_ANALYSIS_EXECUTIVE_SUMMARY.md)** - Executive summary of LLM findings
- **[`llm_analysis_summary_report.md`](llm_analysis_summary_report.md)** - Summary of LLM insights

### 📋 Additional Reports
- **[`power_structures_report.md`](power_structures_report.md)** - Detailed power structures analysis
- **[`TOPIC_ENGAGEMENT_SUMMARY.md`](TOPIC_ENGAGEMENT_SUMMARY.md)** - Topic engagement patterns

## Analysis Components

### 1. Structural Analysis (`analyze_power_dynamics.py`)

**Metrics Computed:**
- Speaking time dominance (total time, percentage)
- Turn-taking structure (turn count, average length)
- Interruption patterns (rapid turn-taking, overlaps)
- Directed interaction graphs (speaker transitions)
- Topic emergence (TF-IDF, cosine similarity)
- Topic stabilization (uptake patterns)
- Fine-grained topic-speaker relations

**Outputs:**
- PNG visualizations (20+ charts)
- JSON data files
- Text analysis reports
- HTML interactive visualizations

### 2. LLM Analysis (`llm_topic_analysis.py`)

**Capabilities:**
- Topic proposal detection
- Speaker orientation analysis (taken_up, ignored, reframed, resisted)
- Topic transformation detection
- Topic recycling identification
- Topic closure analysis

**Outputs:**
- `llm_topic_annotations.json` - Structured annotations
- Comprehensive LLM reports
- Hybrid analysis combining structural + LLM insights

### 3. Interactive Visualizations

**D3.js Interactive Dashboards:**
- Speaker network graphs
- Topic timeline with interactions
- Fine-grained power relations
- Relational interaction views

**Usage:**
1. Run `python start_local_server.py`
2. Open HTML files in browser at `http://localhost:8000/`
3. Explore interactive visualizations

## Key Findings

### Power Decoupling
**Speaking Time ≠ Power**
- Top speakers (SPEAKER_09: 18.9%, SPEAKER_18: 15.9%) have **0% topic stabilization**
- Strategic speakers (SPEAKER_19: 5.8%, SPEAKER_02: 6.0%) achieve **6.2% stabilization**
- Low-participation speaker (SPEAKER_17: <1%) achieves **100% stabilization**

### Topic Success Rate
- **152 topics** detected across meeting
- **Only 3 topics stabilized** (2.0% success rate)
- Highly competitive discourse environment

### Power Dimensions
1. **Floor Control** (Speaking Time): SPEAKER_09, SPEAKER_18, SPEAKER_25
2. **Agenda-Setting Capacity** (Topic Stabilization): SPEAKER_17, SPEAKER_02, SPEAKER_19
3. **Structural Control** (Topic Closure): SPEAKER_19 (100%), SPEAKER_02 (92.9%)
4. **Epistemic Authority** (Accountability): SPEAKER_09, SPEAKER_19 (never challenged)
5. **Response Attraction** (Conversational Attractors): Variable across speakers

### Institutional Imagination
Speakers imagine the organization differently:
- **As a vessel/tool** (SPEAKER_18, SPEAKER_09) - 0% success
- **Through problems** (SPEAKER_02, SPEAKER_17) - Successful agenda setting
- **As open/accessible** (SPEAKER_18) - 0% success
- **As vulnerable** (SPEAKER_02, SPEAKER_09) - Mixed success

**Key Insight:** Those who imagine the institution through **concrete problems** succeed. Those who imagine it through **structure, vessel, or openness** struggle with agenda setting.

## Dependencies

### Python Libraries
```
pandas
numpy
matplotlib
seaborn
networkx
scikit-learn
openai (for LLM analysis)
```

### JavaScript Libraries (for interactive visualizations)
- D3.js (loaded via CDN)
- Observable Plot (optional)

## Methodology

### Power Operationalization
Power is operationalized through **interactional features**, not intentions or authority:
- **Speaking time dominance** - Floor control
- **Turn-taking structure** - Interaction patterns
- **Interruption patterns** - Tolerance asymmetries
- **Topic stabilization** - Agenda-setting capacity
- **Closure authority** - Structural control
- **Accountability patterns** - Epistemic authority

### Topic Detection
- **TF-IDF vectorization** for text representation
- **Cosine similarity** for semantic similarity
- **Topic proposal detection** - New lexical clusters
- **Topic stabilization** - Substantive responses
- **Topic decay** - Unadopted topics

### Relational Framework
Power as **enacted moment-by-moment**, not owned:
- Turns as relations, not possessions
- Duration-weighted response chains
- Interruption tolerance (capacity to continue despite disruption)
- Topic closure authority (uncontested topic shifts)

## File Descriptions

### Core Analysis Scripts

**`analyze_power_dynamics.py`**
- Main analysis orchestrator
- Computes all structural metrics
- Generates visualizations and reports
- Exports data for D3.js

**`llm_topic_analysis.py`**
- LLM-based topic analysis module
- Uses GPT-4o-mini for interpretive analysis
- Structured output parsing
- Rate limiting and batch processing

**`integrate_llm_results.py`**
- Combines structural + LLM analysis
- Creates hybrid reports
- Compares analyses
- Exports integrated data

### Data Files

**`amuta_2026-01-12_1.json`**
- Original transcript with word-level timestamps
- Speaker identifiers
- Utterance boundaries

**`d3_visualization_data.json`**
- Processed data for interactive visualizations
- Includes all metrics, topics, speaker relations
- Formatted for D3.js consumption

**`power_dynamics_report.json`**
- Structured power dynamics metrics
- Speaker statistics
- Topic engagement data

### Reports

**`ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md`**
- Main comprehensive report
- Suitable for organizational presentation
- Covers all analyses and findings

**`SPEAKER_ANIMAL_METAPHORS.md`**
- Ironic, fable-like animal metaphors
- Explains power positions through jungle metaphors
- Includes institutional imagination analysis

## Usage Examples

### Generate All Analyses
```bash
# Structural analysis
python analyze_power_dynamics.py

# LLM analysis (requires API key)
python run_llm_analysis.py
python generate_llm_report.py
```

### View Interactive Visualizations
```bash
# Start local server
python start_local_server.py

# Open in browser:
# http://localhost:8000/interactive_visualizations.html
# http://localhost:8000/relational_interaction_visualizations.html
# http://localhost:8000/topic_emergence_visualizations.html
# http://localhost:8000/fine_grained_power_visualizations.html
```

### Generate Specific Reports
```bash
# Main organizational report (already generated)
# View: [ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md](ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md)

# Animal metaphors (already generated)
# View: [SPEAKER_ANIMAL_METAPHORS.md](SPEAKER_ANIMAL_METAPHORS.md)

# LLM comprehensive report
python generate_llm_report.py
# View: [LLM_ANALYSIS_COMPREHENSIVE_REPORT.md](LLM_ANALYSIS_COMPREHENSIVE_REPORT.md)
```

### View All Reports
- **[Main Organizational Report](ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md)** - Comprehensive analysis
- **[Animal Metaphors](SPEAKER_ANIMAL_METAPHORS.md)** - Power dynamics as organizational jungle
- **[Fine-Grained Analysis](FINE_GRAINED_POWER_SUMMARY.md)** - Detailed topic-speaker relations
- **[Topic Engagement Summary](TOPIC_ENGAGEMENT_SUMMARY.md)** - Topic engagement patterns
- **[Power Structures Report](power_structures_report.md)** - Power structures analysis
- **[LLM Comprehensive Report](LLM_ANALYSIS_COMPREHENSIVE_REPORT.md)** - Full LLM analysis
- **[LLM Executive Summary](LLM_ANALYSIS_EXECUTIVE_SUMMARY.md)** - LLM executive summary
- **[LLM Summary Report](llm_analysis_summary_report.md)** - LLM insights summary

## Output Structure

### Visualizations
- **20+ PNG files** - Static visualizations for reports
- **4 HTML files** - Interactive D3.js visualizations

### Reports
- **[ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md](ORGANIZATIONAL_POWER_DYNAMICS_SUMMARY.md)** - Main comprehensive report
- **[SPEAKER_ANIMAL_METAPHORS.md](SPEAKER_ANIMAL_METAPHORS.md)** - Animal metaphors analysis
- **[FINE_GRAINED_POWER_SUMMARY.md](FINE_GRAINED_POWER_SUMMARY.md)** - Fine-grained analysis
- **[TOPIC_ENGAGEMENT_SUMMARY.md](TOPIC_ENGAGEMENT_SUMMARY.md)** - Topic engagement summary
- **[power_structures_report.md](power_structures_report.md)** - Power structures report
- **[LLM_ANALYSIS_COMPREHENSIVE_REPORT.md](LLM_ANALYSIS_COMPREHENSIVE_REPORT.md)** - LLM comprehensive report
- **[LLM_ANALYSIS_EXECUTIVE_SUMMARY.md](LLM_ANALYSIS_EXECUTIVE_SUMMARY.md)** - LLM executive summary
- **[llm_analysis_summary_report.md](llm_analysis_summary_report.md)** - LLM summary report
- **Multiple text files** - Detailed analysis outputs:
  - [topic_content_analysis.txt](topic_content_analysis.txt)
  - [fine_grained_topic_power_analysis.txt](fine_grained_topic_power_analysis.txt)
  - [topic_engagement_power_analysis.txt](topic_engagement_power_analysis.txt)
  - [llm_hybrid_analysis_report.txt](llm_hybrid_analysis_report.txt)

### Data Files
- **[amuta_2026-01-12_1.json](amuta_2026-01-12_1.json)** - Original transcript data
- **[d3_visualization_data.json](d3_visualization_data.json)** - Processed data for D3.js
- **[llm_topic_annotations.json](llm_topic_annotations.json)** - LLM annotations
- **[power_dynamics_report.json](power_dynamics_report.json)** - Power dynamics metrics

## Contributing

This is an analysis project. To extend:

1. **Add new metrics** - Modify `analyze_power_dynamics.py`
2. **Add visualizations** - Extend visualization functions
3. **Improve LLM analysis** - Modify prompts in `llm_topic_analysis.py`
4. **Add new reports** - Create new report generation scripts

## License

Analysis code and methodology. Data files contain organizational meeting transcripts.

## Citation

If using this analysis methodology, please cite:
- Power dynamics operationalized through interactional features
- Topic emergence through TF-IDF and cosine similarity
- Relational framework for power as enacted moment-by-moment

## Contact

Repository: https://github.com/denisakera/loganalysis

---

**Note:** This analysis is **descriptive and structural**. Interpretations of what these patterns mean for organizational effectiveness are matters for organizational leadership and participants to determine.
