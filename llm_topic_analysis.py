"""
LLM-Based Topic–Interaction Analysis Agent

This module orchestrates LLM calls to analyze topics and speaker orientations
as interactional objects, complementing the structural analysis.

The agent treats topics as interactional objects, not abstract themes.
All outputs are grounded in observable turn sequences and timestamps.
"""

import json
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import time

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: OpenAI library not installed. Install with: pip install openai")

# Fixed vocabulary for speaker-topic relations
TOPIC_RELATIONS = [
    "introduced",
    "taken_up",
    "reframed",
    "resisted",
    "ignored",
    "recycled",
    "closed"
]

@dataclass
class TopicAnnotation:
    """Structured annotation for a topic identified by LLM."""
    topic_id: str
    start_turn_index: int
    end_turn_index: int
    start_time: float
    end_time: float
    introducer: str
    status: str  # emerged, failed, transformed, recycled, closed
    confidence: str  # high, medium, low, uncertain
    justification: str  # Observable turn sequence evidence
    speaker_orientations: List[Dict[str, Any]]  # List of {speaker, relation, turn_index, justification}
    
@dataclass
class TurnContext:
    """Context for a single turn in the conversation."""
    turn_index: int
    speaker: str
    start_time: float
    end_time: float
    text: str
    is_interruption: bool = False
    has_overlap: bool = False
    follows_silence: bool = False

class TopicInteractionAnalyzer:
    """
    LLM-based analyzer for topic emergence and speaker orientations.
    
    Treats topics as interactional objects, not abstract themes.
    All outputs grounded in observable turn sequences.
    """
    
    SYSTEM_PROMPT = """You are an analytic language model agent operating on preprocessed debate interaction data. You do not perform transcription, diarization, timing extraction, or speaker identification. All segmentation, timestamps, and turn adjacency have been computed externally and must be treated as authoritative.

Your task is interpretive but constrained: to identify emergent topics and to characterize how speakers orient to those topics through interactional sequence.

You must treat topics as interactional objects, not as abstract themes, opinions, or subject matters. A topic exists only insofar as it is oriented to by participants through uptake, resistance, reframing, silence, or closure.

You must not evaluate the correctness, importance, truth value, or moral status of any topic. You must not infer speaker intentions, authority, status, expertise, or psychological traits.

Analytic tasks:

Topic emergence:
Identify candidate topic onsets where a turn introduces a semantic frame that is not continuous with the immediately preceding interaction. This judgment must be comparative and contextual. Do not rely on keyword novelty alone.

Topic uptake:
For each candidate topic, determine whether and how other speakers orient to it. Orientation includes continuation, elaboration, questioning, reframing, or resistance. Uptake must be grounded in observable sequential response.

Topic failure:
Mark topics that receive no substantive uptake and decay through silence, interruption, or unrelated continuation. Absence of response is an interactional outcome and must be treated as meaningful.

Topic transformation:
Detect cases where a responding speaker preserves the conversational relevance of a topic while altering its semantic framing. Label these events explicitly as reframing rather than agreement or disagreement.

Topic recycling:
Detect cases where a topic initially fails but later gains uptake when reintroduced by a different speaker or in a different interactional position.

Topic closure:
Identify when a topic ends, especially when closure occurs without explicit agreement, resolution, or contest. Note which speaker initiates closure and whether others align with it.

Output constraints:

You do not summarize debates.
You do not rank speakers.
You do not compute or infer dominance, authority, or influence scores.

You output only:

Topic identifiers with temporal boundaries
Speaker–topic relations, labeled using a fixed vocabulary: introduced, taken_up, reframed, resisted, ignored, recycled, closed
Brief justifications grounded strictly in observable turn sequence and adjacency

Every output element must be traceable to specific turns and timestamps.

Epistemic discipline:

When uncertain, explicitly mark uncertainty rather than guessing.
Prefer false negatives over false positives.
Treat silence, delay, and non response as analytically significant interactional events.

You assist a human analyst. You do not determine where power lies. You surface interactional structures through which power may be enacted.

Output format: JSON with the following structure:
{
  "topics": [
    {
      "topic_id": "TOPIC_X",
      "start_turn_index": N,
      "end_turn_index": M,
      "start_time": T,
      "end_time": T,
      "introducer": "SPEAKER_ID",
      "status": "emerged|failed|transformed|recycled|closed",
      "confidence": "high|medium|low|uncertain",
      "justification": "Observable turn sequence evidence",
      "speaker_orientations": [
        {
          "speaker": "SPEAKER_ID",
          "relation": "introduced|taken_up|reframed|resisted|ignored|recycled|closed",
          "turn_index": N,
          "justification": "Specific turn sequence evidence"
        }
      ]
    }
  ]
}"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini"):
        """
        Initialize the analyzer.
        
        Args:
            api_key: OpenAI API key. If None, reads from OPENAI_API_KEY env var.
            model: OpenAI model to use (default: gpt-4o-mini for cost efficiency)
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI library required. Install with: pip install openai")
        
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.annotations: List[TopicAnnotation] = []
        
    def prepare_turn_context(self, turns: List[Dict], segments: List[Dict]) -> List[TurnContext]:
        """
        Prepare turn context from existing analysis data.
        
        Args:
            turns: List of turn dictionaries from analyze_power_dynamics
            segments: List of segment dictionaries from transcript
            
        Returns:
            List of TurnContext objects
        """
        turn_contexts = []
        
        for i, turn in enumerate(turns):
            # Get all segments for this turn
            turn_segments = [s for s in segments if
                           self._get_speaker(s) == turn['speaker'] and
                           turn['start'] <= s['start'] <= turn['end']]
            
            # Combine text
            text = ' '.join([s.get('text', '').strip() for s in turn_segments 
                           if s.get('text', '').strip()])
            
            # Check for interruptions/overlaps (simplified - would need full interruption data)
            is_interruption = False  # Would need to check against interruption data
            has_overlap = False  # Would need to check against overlap data
            
            # Check if follows silence (gap > 2 seconds)
            follows_silence = False
            if i > 0:
                prev_turn = turns[i-1]
                gap = turn['start'] - prev_turn['end']
                follows_silence = gap > 2.0
            
            turn_context = TurnContext(
                turn_index=i,
                speaker=turn['speaker'],
                start_time=turn['start'],
                end_time=turn['end'],
                text=text,
                is_interruption=is_interruption,
                has_overlap=has_overlap,
                follows_silence=follows_silence
            )
            turn_contexts.append(turn_context)
        
        return turn_contexts
    
    def _get_speaker(self, seg: Dict) -> str:
        """Extract speaker from segment."""
        if 'speaker' in seg and seg['speaker']:
            return seg['speaker']
        # Fallback to word-level speaker
        if 'words' in seg and seg['words']:
            speakers = [w.get('speaker') for w in seg['words'] if w.get('speaker')]
            if speakers:
                from collections import Counter
                return Counter(speakers).most_common(1)[0][0]
        return 'UNKNOWN'
    
    def format_turns_for_llm(self, turn_contexts: List[TurnContext], 
                             window_start: int = 0, window_end: Optional[int] = None) -> str:
        """
        Format turn contexts for LLM analysis.
        
        Args:
            turn_contexts: List of turn contexts
            window_start: Start index for analysis window
            window_end: End index for analysis window (None = all)
            
        Returns:
            Formatted string for LLM
        """
        if window_end is None:
            window_end = len(turn_contexts)
        
        formatted = "TURN SEQUENCE:\n"
        formatted += "=" * 80 + "\n\n"
        
        for turn in turn_contexts[window_start:window_end]:
            formatted += f"Turn {turn.turn_index}: {turn.speaker}\n"
            formatted += f"  Time: {turn.start_time:.2f}s - {turn.end_time:.2f}s\n"
            if turn.follows_silence:
                formatted += f"  [Follows silence]\n"
            if turn.is_interruption:
                formatted += f"  [Interruption]\n"
            if turn.has_overlap:
                formatted += f"  [Overlap]\n"
            formatted += f"  Text: {turn.text[:500]}\n"  # Limit text length
            formatted += "\n"
        
        return formatted
    
    def analyze_topic_window(self, turn_contexts: List[TurnContext],
                            topic_candidate: Dict,
                            context_window: int = 5) -> Optional[TopicAnnotation]:
        """
        Analyze a single topic candidate using LLM.
        
        Args:
            turn_contexts: All turn contexts
            topic_candidate: Topic candidate from structural analysis
            context_window: Number of turns before/after to include for context
            
        Returns:
            TopicAnnotation or None if analysis fails
        """
        topic_start_idx = topic_candidate.get('turn_index', 0)
        topic_start_time = topic_candidate['start_time']
        topic_end_time = topic_candidate['end_time']
        
        # Find end turn index
        topic_end_idx = topic_start_idx
        for i, turn in enumerate(turn_contexts):
            if turn.start_time <= topic_end_time <= turn.end_time:
                topic_end_idx = i
                break
        
        # Expand context window
        window_start = max(0, topic_start_idx - context_window)
        window_end = min(len(turn_contexts), topic_end_idx + context_window + 1)
        
        # Format turns for LLM
        formatted_turns = self.format_turns_for_llm(turn_contexts, window_start, window_end)
        
        # Create analysis prompt
        user_prompt = f"""Analyze the following topic candidate in the context of surrounding turns.

TOPIC CANDIDATE:
- Introduced by: {topic_candidate['proposer']}
- Start time: {topic_start_time:.2f}s (Turn {topic_start_idx})
- End time: {topic_end_time:.2f}s (Turn {topic_end_idx})
- Text: {topic_candidate.get('text', topic_candidate.get('text_sample', ''))[:300]}

{formatted_turns}

Analyze this topic as an interactional object:
1. Does this represent a topic emergence? (semantic frame not continuous with preceding interaction)
2. How do other speakers orient to it? (taken_up, reframed, resisted, ignored)
3. What is the topic's status? (emerged, failed, transformed, recycled, closed)
4. Which speaker closes it (if applicable)?

Output JSON following the specified format. Be explicit about uncertainty."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent analysis
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Parse result into TopicAnnotation
            if result.get('topics') and len(result['topics']) > 0:
                topic_data = result['topics'][0]
                return TopicAnnotation(
                    topic_id=topic_data.get('topic_id', topic_candidate.get('topic_id', 'UNKNOWN')),
                    start_turn_index=topic_data.get('start_turn_index', topic_start_idx),
                    end_turn_index=topic_data.get('end_turn_index', topic_end_idx),
                    start_time=topic_data.get('start_time', topic_start_time),
                    end_time=topic_data.get('end_time', topic_end_time),
                    introducer=topic_data.get('introducer', topic_candidate['proposer']),
                    status=topic_data.get('status', 'uncertain'),
                    confidence=topic_data.get('confidence', 'uncertain'),
                    justification=topic_data.get('justification', ''),
                    speaker_orientations=topic_data.get('speaker_orientations', [])
                )
            
        except Exception as e:
            print(f"Error analyzing topic {topic_candidate.get('topic_id', 'UNKNOWN')}: {e}")
            return None
    
    def analyze_all_topics(self, topics: List[Dict], turns: List[Dict], 
                          segments: List[Dict], batch_size: int = 10,
                          delay_between_batches: float = 1.0) -> List[TopicAnnotation]:
        """
        Analyze all topic candidates using LLM.
        
        Args:
            topics: List of topic candidates from structural analysis
            turns: List of turn dictionaries
            segments: List of segment dictionaries
            batch_size: Number of topics to analyze before pausing
            delay_between_batches: Seconds to wait between batches (rate limiting)
            
        Returns:
            List of TopicAnnotation objects
        """
        print(f"Preparing turn contexts for {len(turns)} turns...")
        turn_contexts = self.prepare_turn_context(turns, segments)
        
        print(f"Analyzing {len(topics)} topics using LLM...")
        annotations = []
        
        for i, topic in enumerate(topics):
            if i > 0 and i % batch_size == 0:
                print(f"  Processed {i}/{len(topics)} topics. Pausing for rate limiting...")
                time.sleep(delay_between_batches)
            
            print(f"  Analyzing topic {i+1}/{len(topics)}: {topic.get('topic_id', 'UNKNOWN')}")
            
            # Add turn_index to topic if not present
            if 'turn_index' not in topic:
                # Find turn index from start time
                for j, turn in enumerate(turns):
                    if turn['start'] <= topic['start_time'] <= turn['end']:
                        topic['turn_index'] = j
                        break
                else:
                    topic['turn_index'] = 0
            
            annotation = self.analyze_topic_window(turn_contexts, topic)
            if annotation:
                annotations.append(annotation)
            else:
                print(f"    Warning: Failed to analyze topic {topic.get('topic_id', 'UNKNOWN')}")
        
        self.annotations = annotations
        return annotations
    
    def save_annotations(self, filepath: str):
        """Save annotations to JSON file."""
        data = {
            'annotations': [asdict(ann) for ann in self.annotations],
            'total_topics_analyzed': len(self.annotations),
            'model_used': self.model
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.annotations)} annotations to {filepath}")
    
    def load_annotations(self, filepath: str) -> List[TopicAnnotation]:
        """Load annotations from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        self.annotations = [
            TopicAnnotation(**ann) for ann in data['annotations']
        ]
        return self.annotations
    
    def compare_with_structural_analysis(self, structural_topics: List[Dict]) -> Dict[str, Any]:
        """
        Compare LLM annotations with structural analysis results.
        
        Args:
            structural_topics: Topics from structural similarity analysis
            
        Returns:
            Comparison statistics
        """
        comparison = {
            'structural_topics_count': len(structural_topics),
            'llm_annotations_count': len(self.annotations),
            'agreement_on_emergence': 0,
            'disagreement_on_emergence': 0,
            'llm_identified_additional': 0,
            'structural_only': 0,
            'status_distribution': defaultdict(int),
            'relation_distribution': defaultdict(int)
        }
        
        # Create mapping by time windows
        structural_by_time = {}
        for topic in structural_topics:
            time_key = (topic['start_time'], topic['end_time'])
            structural_by_time[time_key] = topic
        
        llm_by_time = {}
        for ann in self.annotations:
            time_key = (ann.start_time, ann.end_time)
            llm_by_time[time_key] = ann
        
        # Compare
        for ann in self.annotations:
            comparison['status_distribution'][ann.status] += 1
            for orientation in ann.speaker_orientations:
                comparison['relation_distribution'][orientation['relation']] += 1
        
        return comparison


def integrate_llm_analysis(structural_topics: List[Dict], turns: List[Dict],
                          segments: List[Dict], api_key: Optional[str] = None,
                          model: str = "gpt-4o-mini", output_file: str = "llm_topic_annotations.json"):
    """
    Main function to run LLM analysis on structural topics.
    
    Args:
        structural_topics: Topics from structural analysis
        turns: Turn data from structural analysis
        segments: Segment data from transcript
        api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        model: Model to use
        output_file: Where to save annotations
        
    Returns:
        List of TopicAnnotation objects
    """
    analyzer = TopicInteractionAnalyzer(api_key=api_key, model=model)
    
    annotations = analyzer.analyze_all_topics(structural_topics, turns, segments)
    
    analyzer.save_annotations(output_file)
    
    comparison = analyzer.compare_with_structural_analysis(structural_topics)
    print("\nComparison with Structural Analysis:")
    print(f"  Structural topics: {comparison['structural_topics_count']}")
    print(f"  LLM annotations: {comparison['llm_annotations_count']}")
    print(f"  Status distribution: {dict(comparison['status_distribution'])}")
    print(f"  Relation distribution: {dict(comparison['relation_distribution'])}")
    
    return annotations


if __name__ == "__main__":
    # Example usage
    print("LLM Topic-Interaction Analysis Agent")
    print("=" * 80)
    print("\nThis module requires:")
    print("1. OpenAI API key (set OPENAI_API_KEY environment variable)")
    print("2. Structural analysis data (topics, turns, segments)")
    print("\nTo use:")
    print("  from llm_topic_analysis import integrate_llm_analysis")
    print("  annotations = integrate_llm_analysis(structural_topics, turns, segments)")
