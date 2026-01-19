"""
Script to run LLM-based topic analysis on the debate transcript.

This integrates LLM analysis with the existing structural analysis.
"""

import json
import os
from llm_topic_analysis import integrate_llm_analysis, TopicInteractionAnalyzer

def load_structural_analysis_data():
    """Load topics, turns, and segments from existing analysis."""
    print("Loading structural analysis data...")
    
    # Import structural analysis functions
    from analyze_power_dynamics import (
        load_transcript, compute_turn_taking, analyze_topic_lifecycle,
        get_speaker
    )
    
    # Load transcript
    print("  Loading transcript...")
    segments = load_transcript('amuta_2026-01-12_1.json')
    
    # Compute turns
    print("  Computing turns...")
    turns, turn_stats = compute_turn_taking(segments)
    
    # Detect topics
    print("  Detecting topics...")
    topics = analyze_topic_lifecycle(segments, turns, 
                                    similarity_threshold=0.25, 
                                    stabilization_threshold=0.3)
    
    # Add turn_index to topics for LLM analysis
    for topic in topics:
        if 'turn_index' not in topic:
            # Find turn index from start time
            for j, turn in enumerate(turns):
                if turn['start'] <= topic['start_time'] <= turn['end']:
                    topic['turn_index'] = j
                    break
            else:
                topic['turn_index'] = 0
    
    return topics, turns, segments

def main():
    """Main function to run LLM analysis."""
    print("=" * 80)
    print("LLM Topic-Interaction Analysis")
    print("=" * 80)
    print()
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print("Or on Windows: set OPENAI_API_KEY=your-key-here")
        return
    
    # Load data
    topics, turns, segments = load_structural_analysis_data()
    
    if topics is None or turns is None:
        print("\nGenerating structural analysis first...")
        # Import and run structural analysis
        from analyze_power_dynamics import (
            load_transcript, compute_turn_taking, analyze_topic_lifecycle
        )
        
        print("Loading transcript...")
        segments = load_transcript('amuta_2026-01-12_1.json')
        
        print("Computing turns...")
        turns, turn_stats = compute_turn_taking(segments)
        
        print("Detecting topics...")
        topics = analyze_topic_lifecycle(segments, turns, 
                                        similarity_threshold=0.25, 
                                        stabilization_threshold=0.3)
        
        print(f"Found {len(topics)} topics from structural analysis")
    
    # Option: Analyze all topics or sample
    print(f"\nFound {len(topics)} topics from structural analysis")
    
    # Analyze a representative sample (mix of stabilized and failed topics)
    # This provides meaningful analysis while controlling costs
    stabilized = [t for t in topics if t['status'] == 'stabilized']
    failed = [t for t in topics if t['status'] != 'stabilized']
    
    # Sample: all stabilized + sample of failed topics
    sample_size = 30  # Total topics to analyze
    sample_failed = sample_size - len(stabilized)
    
    if sample_failed > 0 and len(failed) > sample_failed:
        # Take first N failed topics (they're already sorted by time)
        sampled_failed = failed[:sample_failed]
        topics_to_analyze = stabilized + sampled_failed
        print(f"Analyzing {len(stabilized)} stabilized topics + {len(sampled_failed)} failed topics = {len(topics_to_analyze)} total")
    else:
        topics_to_analyze = topics[:sample_size] if len(topics) > sample_size else topics
        print(f"Analyzing {len(topics_to_analyze)} topics")
    
    topics = topics_to_analyze
    
    # Run LLM analysis
    print("\nStarting LLM analysis...")
    print("Note: This will make API calls to OpenAI. Costs will depend on model and topic count.")
    
    annotations = integrate_llm_analysis(
        structural_topics=topics,
        turns=turns,
        segments=segments,
        api_key=api_key,
        model="gpt-4o-mini",  # Use gpt-4o-mini for cost efficiency, or gpt-4o for better analysis
        output_file="llm_topic_annotations.json"
    )
    
    print(f"\nAnalysis complete! Generated {len(annotations)} annotations.")
    print("Results saved to: llm_topic_annotations.json")
    
    # Generate comparison report
    analyzer = TopicInteractionAnalyzer(api_key=api_key)
    analyzer.annotations = annotations
    comparison = analyzer.compare_with_structural_analysis(topics)
    
    print("\n" + "=" * 80)
    print("Analysis Summary")
    print("=" * 80)
    print(f"Topics analyzed: {len(annotations)}")
    print(f"\nStatus distribution:")
    for status, count in comparison['status_distribution'].items():
        print(f"  {status}: {count}")
    print(f"\nRelation distribution:")
    for relation, count in comparison['relation_distribution'].items():
        print(f"  {relation}: {count}")

if __name__ == "__main__":
    main()
