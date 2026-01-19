# Quick Start: LLM Topic Analysis

## Prerequisites

1. **OpenAI API Key**: Get one from https://platform.openai.com/api-keys
2. **Python Package**: `pip install openai`
3. **Structural Analysis**: Run `python analyze_power_dynamics.py` first (generates topics)

## Setup (One Time)

### Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="sk-your-key-here"
```

### Linux/Mac:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

## Run Analysis

```bash
python run_llm_analysis.py
```

**Note**: By default, analyzes first 10 topics to control costs. Edit `run_llm_analysis.py` to change `sample_size` or remove limit.

## What It Does

1. Loads topics from structural analysis (similarity-based)
2. For each topic, calls LLM to analyze:
   - Topic emergence (semantic frame discontinuity)
   - Speaker orientations (taken_up, reframed, resisted, ignored, etc.)
   - Topic status (emerged, failed, transformed, recycled, closed)
3. Saves structured annotations to `llm_topic_annotations.json`

## Output

- **`llm_topic_annotations.json`**: Structured LLM annotations
- Each annotation includes:
  - Topic boundaries (turn indices, timestamps)
  - Speaker orientations with justifications
  - Confidence levels
  - Traceability to specific turns

## Integration

After LLM analysis, integrate with structural analysis:

```python
from integrate_llm_results import create_hybrid_topic_report, export_llm_to_d3

# Load data
from analyze_power_dynamics import analyze_topic_lifecycle, compute_turn_taking, load_transcript
segments = load_transcript('amuta_2026-01-12_1.json')
turns, _ = compute_turn_taking(segments)
topics = analyze_topic_lifecycle(segments, turns)

from llm_topic_analysis import load_annotations
llm_annotations = load_annotations('llm_topic_annotations.json')

# Create hybrid report
create_hybrid_topic_report(topics, llm_annotations)

# Add to D3 data
export_llm_to_d3(llm_annotations)
```

## Cost Estimate

- **Model**: `gpt-4o-mini` (default, cost-efficient)
- **Per Topic**: ~500-1000 tokens
- **152 Topics**: ~$0.50-$1.00 (estimated)
- **Alternative**: `gpt-4o` (better analysis, ~10x cost)

## Next Steps

1. Review `llm_topic_annotations.json` for LLM interpretations
2. Run `integrate_llm_results.py` to create hybrid analysis
3. Compare structural vs LLM classifications
4. Use LLM annotations to enhance interactive visualizations
