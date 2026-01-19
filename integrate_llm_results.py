"""
Integration of LLM analysis results with structural analysis.

Combines LLM annotations with structural metrics for hybrid analysis.
"""

import json
from collections import defaultdict
from llm_topic_analysis import TopicAnnotation

def load_llm_annotations(filepath: str = "llm_topic_annotations.json"):
    """Load LLM annotations from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    annotations = [
        TopicAnnotation(**ann) for ann in data['annotations']
    ]
    return annotations

def compare_structural_vs_llm(structural_topics: list, llm_annotations: list):
    """
    Compare structural analysis results with LLM annotations.
    
    Returns comparison statistics and alignment mapping.
    """
    comparison = {
        'structural_count': len(structural_topics),
        'llm_count': len(llm_annotations),
        'status_distribution': defaultdict(int),
        'relation_distribution': defaultdict(int),
        'confidence_distribution': defaultdict(int),
        'aligned_topics': [],
        'llm_only': [],
        'structural_only': []
    }
    
    # Create time-based mapping for alignment
    structural_by_time = {}
    for topic in structural_topics:
        time_key = (round(topic['start_time'], 1), round(topic['end_time'], 1))
        structural_by_time[time_key] = topic
    
    llm_by_time = {}
    for ann in llm_annotations:
        time_key = (round(ann.start_time, 1), round(ann.end_time, 1))
        llm_by_time[time_key] = ann
    
    # Find alignments (topics detected by both)
    for time_key, struct_topic in structural_by_time.items():
        if time_key in llm_by_time:
            llm_ann = llm_by_time[time_key]
            comparison['aligned_topics'].append({
                'structural': struct_topic,
                'llm': llm_ann,
                'status_match': struct_topic['status'] == llm_ann.status
            })
        else:
            comparison['structural_only'].append(struct_topic)
    
    for time_key, llm_ann in llm_by_time.items():
        if time_key not in structural_by_time:
            comparison['llm_only'].append(llm_ann)
    
    # Aggregate statistics
    for ann in llm_annotations:
        comparison['status_distribution'][ann.status] += 1
        comparison['confidence_distribution'][ann.confidence] += 1
        for orientation in ann.speaker_orientations:
            comparison['relation_distribution'][orientation['relation']] += 1
    
    return comparison

def create_hybrid_topic_report(structural_topics: list, llm_annotations: list,
                               output_file: str = "hybrid_topic_analysis.txt"):
    """
    Create a hybrid report combining structural and LLM analyses.
    """
    comparison = compare_structural_vs_llm(structural_topics, llm_annotations)
    
    report_lines = []
    report_lines.append("=" * 100)
    report_lines.append("HYBRID TOPIC ANALYSIS: STRUCTURAL + LLM INTERPRETIVE")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    report_lines.append("COMPARISON SUMMARY")
    report_lines.append("-" * 100)
    report_lines.append(f"Structural Analysis Topics: {comparison['structural_count']}")
    report_lines.append(f"LLM Analysis Annotations: {comparison['llm_count']}")
    report_lines.append(f"Aligned Topics (detected by both): {len(comparison['aligned_topics'])}")
    report_lines.append(f"Structural Only: {len(comparison['structural_only'])}")
    report_lines.append(f"LLM Only: {len(comparison['llm_only'])}")
    report_lines.append("")
    
    report_lines.append("LLM STATUS DISTRIBUTION")
    report_lines.append("-" * 100)
    for status, count in sorted(comparison['status_distribution'].items(), 
                               key=lambda x: x[1], reverse=True):
        report_lines.append(f"  {status}: {count}")
    report_lines.append("")
    
    report_lines.append("SPEAKER-TOPIC RELATIONS (LLM Classification)")
    report_lines.append("-" * 100)
    for relation, count in sorted(comparison['relation_distribution'].items(),
                                 key=lambda x: x[1], reverse=True):
        report_lines.append(f"  {relation}: {count}")
    report_lines.append("")
    
    report_lines.append("CONFIDENCE DISTRIBUTION")
    report_lines.append("-" * 100)
    for confidence, count in sorted(comparison['confidence_distribution'].items(),
                                   key=lambda x: x[1], reverse=True):
        report_lines.append(f"  {confidence}: {count}")
    report_lines.append("")
    
    # Detailed aligned topics
    report_lines.append("=" * 100)
    report_lines.append("ALIGNED TOPICS (Structural + LLM Analysis)")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    for i, aligned in enumerate(comparison['aligned_topics'][:20], 1):  # Show first 20
        struct = aligned['structural']
        llm = aligned['llm']
        
        report_lines.append(f"TOPIC {i}: {llm.topic_id}")
        report_lines.append("-" * 100)
        report_lines.append(f"Time: {llm.start_time:.2f}s - {llm.end_time:.2f}s")
        report_lines.append(f"Introducer: {llm.introducer}")
        report_lines.append("")
        
        report_lines.append("STRUCTURAL ANALYSIS:")
        report_lines.append(f"  Status: {struct['status']}")
        report_lines.append(f"  Similarity to Preceding: {struct.get('similarity_to_preceding', 0):.3f}")
        report_lines.append("")
        
        report_lines.append("LLM ANALYSIS:")
        report_lines.append(f"  Status: {llm.status}")
        report_lines.append(f"  Confidence: {llm.confidence}")
        report_lines.append(f"  Justification: {llm.justification[:200]}...")
        report_lines.append("")
        
        report_lines.append("SPEAKER ORIENTATIONS (LLM):")
        for orientation in llm.speaker_orientations:
            report_lines.append(f"  {orientation['speaker']}: {orientation['relation']}")
            report_lines.append(f"    Turn {orientation['turn_index']}: {orientation['justification'][:150]}...")
        report_lines.append("")
        
        report_lines.append("=" * 100)
        report_lines.append("")
    
    # Write report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"Hybrid report saved to {output_file}")
    return comparison

def export_llm_to_d3(llm_annotations: list, output_file: str = "d3_visualization_data.json"):
    """
    Add LLM annotations to existing D3 visualization data.
    """
    # Load existing D3 data
    with open(output_file, 'r', encoding='utf-8') as f:
        d3_data = json.load(f)
    
    # Add LLM annotations
    d3_data['llm_analysis'] = {
        'annotations': [
            {
                'topic_id': ann.topic_id,
                'start_turn_index': ann.start_turn_index,
                'end_turn_index': ann.end_turn_index,
                'start_time': ann.start_time,
                'end_time': ann.end_time,
                'introducer': ann.introducer,
                'status': ann.status,
                'confidence': ann.confidence,
                'justification': ann.justification,
                'speaker_orientations': ann.speaker_orientations
            }
            for ann in llm_annotations
        ],
        'total_annotations': len(llm_annotations),
        'status_distribution': {},
        'relation_distribution': {}
    }
    
    # Add distributions
    status_dist = defaultdict(int)
    relation_dist = defaultdict(int)
    
    for ann in llm_annotations:
        status_dist[ann.status] += 1
        for orientation in ann.speaker_orientations:
            relation_dist[orientation['relation']] += 1
    
    d3_data['llm_analysis']['status_distribution'] = dict(status_dist)
    d3_data['llm_analysis']['relation_distribution'] = dict(relation_dist)
    
    # Save updated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(d3_data, f, indent=2, ensure_ascii=False)
    
    print(f"LLM annotations added to {output_file}")

if __name__ == "__main__":
    print("LLM-Structural Analysis Integration")
    print("=" * 80)
    print("\nThis script integrates LLM analysis results with structural analysis.")
    print("Run after completing LLM analysis (run_llm_analysis.py)")
