# LLM-Based Topic-Interaction Analysis

This module provides LLM-based analysis of topics and speaker orientations, complementing the structural analysis with interpretive insights grounded in observable turn sequences.

## Overview

The LLM analysis agent:
- Treats topics as **interactional objects**, not abstract themes
- Analyzes how speakers orient to topics (taken_up, reframed, resisted, ignored, etc.)
- Provides structured annotations with traceability to specific turns
- Marks uncertainty explicitly
- Complements (does not replace) structural similarity analysis

## Setup

### 1. Install Dependencies

```bash
pip install openai
```

### 2. Set API Key

**Windows:**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or create a `.env` file (not recommended for production, but convenient for testing).

### 3. Run Analysis

```bash
python run_llm_analysis.py
```

## How It Works

### Input
- **Topics from structural analysis** (similarity-based topic detection)
- **Turn sequences** with timestamps and speaker IDs
- **Segment data** with full text

### Process
1. For each topic candidate, the LLM analyzes:
   - Whether it represents topic emergence (semantic frame discontinuity)
   - How other speakers orient to it (uptake, reframing, resistance, etc.)
   - Topic status (emerged, failed, transformed, recycled, closed)
   - Who closes it (if applicable)

2. LLM uses constrained system prompt to:
   - Ground all judgments in observable turn sequences
   - Use fixed vocabulary for relations
   - Mark uncertainty explicitly
   - Avoid inferring intentions or authority

### Output
- **Structured JSON annotations** (`llm_topic_annotations.json`)
- Each annotation includes:
  - Topic boundaries (turn indices, timestamps)
  - Speaker orientations with justifications
  - Confidence levels
  - Traceability to specific turns

## Fixed Vocabulary

Speaker-topic relations:
- **introduced**: Speaker who first introduces the topic
- **taken_up**: Speaker continues/elaborates the topic
- **reframed**: Speaker preserves relevance but alters semantic framing
- **resisted**: Speaker actively resists or challenges the topic
- **ignored**: Speaker does not respond (silence is meaningful)
- **recycled**: Topic reintroduced by different speaker after initial failure
- **closed**: Speaker ends the topic (with or without contest)

## Integration with Structural Analysis

The LLM analysis **complements** structural analysis:

| Aspect | Structural Analysis | LLM Analysis |
|--------|-------------------|--------------|
| Topic Detection | Semantic similarity thresholds | Contextual frame discontinuity |
| Speaker Orientation | Similarity scores | Interpretive classification (taken_up, reframed, etc.) |
| Topic Status | Stabilized/Failed (binary) | Emerged/Failed/Transformed/Recycled/Closed |
| Traceability | Turn indices, timestamps | Turn indices, timestamps + justifications |

## Cost Considerations

- **Model**: Default is `gpt-4o-mini` (cost-efficient)
- **Alternative**: `gpt-4o` (better analysis, higher cost)
- **Rate Limiting**: Built-in delays between batches
- **Sample Size**: By default, analyzes first 10 topics (remove limit to analyze all)

## Output Format

```json
{
  "annotations": [
    {
      "topic_id": "TOPIC_0",
      "start_turn_index": 5,
      "end_turn_index": 8,
      "start_time": 95.58,
      "end_time": 121.04,
      "introducer": "SPEAKER_14",
      "status": "failed",
      "confidence": "high",
      "justification": "Topic introduced but no speakers responded within 30 seconds...",
      "speaker_orientations": [
        {
          "speaker": "SPEAKER_14",
          "relation": "introduced",
          "turn_index": 5,
          "justification": "Turn 5 introduces topic about E-M..."
        },
        {
          "speaker": "SPEAKER_15",
          "relation": "ignored",
          "turn_index": 6,
          "justification": "Turn 6 shifts to unrelated topic without addressing E-M..."
        }
      ]
    }
  ],
  "total_topics_analyzed": 152,
  "model_used": "gpt-4o-mini"
}
```

## Usage in Code

```python
from llm_topic_analysis import integrate_llm_analysis

# Load your structural analysis data
topics = [...]  # From analyze_power_dynamics
turns = [...]   # From analyze_power_dynamics
segments = [...] # From transcript

# Run LLM analysis
annotations = integrate_llm_analysis(
    structural_topics=topics,
    turns=turns,
    segments=segments,
    api_key="your-key",  # Or set env var
    model="gpt-4o-mini",
    output_file="llm_topic_annotations.json"
)
```

## Epistemic Discipline

The system:
- **Marks uncertainty** rather than guessing
- **Prefers false negatives** over false positives
- **Treats silence as meaningful** (not absence of data)
- **Grounds all outputs** in observable turn sequences
- **Does not infer** intentions, authority, or psychological traits

## Limitations

1. **API Costs**: Each topic requires an API call
2. **Rate Limits**: OpenAI API has rate limits
3. **Context Window**: Limited by model context window (analyzes ~10 turns around each topic)
4. **Interpretive**: Still interpretive, though constrained by system prompt

## Next Steps

1. **Compare Results**: Use `compare_with_structural_analysis()` to see agreements/disagreements
2. **Integrate Visualizations**: Add LLM annotations to interactive visualizations
3. **Hybrid Analysis**: Combine structural metrics with LLM interpretations
4. **Validation**: Human analyst reviews LLM justifications for accuracy
