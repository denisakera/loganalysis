"""
Generate comprehensive report from LLM analysis results.
"""

import json
from integrate_llm_results import (
    load_llm_annotations, compare_structural_vs_llm, create_hybrid_topic_report,
    export_llm_to_d3
)
from analyze_power_dynamics import (
    load_transcript, compute_turn_taking, analyze_topic_lifecycle
)

def main():
    print("=" * 80)
    print("Generating LLM Analysis Report")
    print("=" * 80)
    print()
    
    # Load structural analysis
    print("Loading structural analysis...")
    segments = load_transcript('amuta_2026-01-12_1.json')
    turns, turn_stats = compute_turn_taking(segments)
    structural_topics = analyze_topic_lifecycle(segments, turns, 
                                                similarity_threshold=0.25, 
                                                stabilization_threshold=0.3)
    
    # Filter to same topics analyzed by LLM
    print("Loading LLM annotations...")
    llm_annotations = load_llm_annotations('llm_topic_annotations.json')
    
    # Match topics by time windows
    structural_by_id = {t['topic_id']: t for t in structural_topics}
    analyzed_structural = []
    for ann in llm_annotations:
        if ann.topic_id in structural_by_id:
            analyzed_structural.append(structural_by_id[ann.topic_id])
    
    print(f"Matched {len(analyzed_structural)} structural topics with LLM annotations")
    
    # Create hybrid report
    print("\nCreating hybrid report...")
    comparison = create_hybrid_topic_report(
        analyzed_structural, 
        llm_annotations,
        output_file="llm_hybrid_analysis_report.txt"
    )
    
    # Export to D3 format
    print("\nExporting to D3 format...")
    export_llm_to_d3(llm_annotations)
    
    # Create summary report
    print("\nCreating summary report...")
    create_summary_report(comparison, llm_annotations, analyzed_structural)
    
    print("\n" + "=" * 80)
    print("Report Generation Complete!")
    print("=" * 80)
    print("\nFiles created:")
    print("  - llm_hybrid_analysis_report.txt")
    print("  - llm_analysis_summary_report.md")
    print("  - d3_visualization_data.json (updated with LLM data)")

def create_summary_report(comparison, llm_annotations, structural_topics):
    """Create markdown summary report."""
    
    report_lines = []
    report_lines.append("# LLM Topic-Interaction Analysis Report")
    report_lines.append("")
    report_lines.append("**Analysis Date:** Generated from LLM analysis")
    report_lines.append(f"**Topics Analyzed:** {len(llm_annotations)}")
    report_lines.append("")
    report_lines.append("---")
    report_lines.append("")
    
    # Executive Summary
    report_lines.append("## Executive Summary")
    report_lines.append("")
    report_lines.append("This report presents LLM-based interpretive analysis of topics as interactional objects.")
    report_lines.append("The analysis complements structural similarity-based detection with nuanced classification")
    report_lines.append("of speaker orientations and topic status.")
    report_lines.append("")
    
    # Status Distribution
    report_lines.append("### Topic Status Distribution (LLM Classification)")
    report_lines.append("")
    for status, count in sorted(comparison['status_distribution'].items(), 
                               key=lambda x: x[1], reverse=True):
        pct = (count / len(llm_annotations) * 100) if llm_annotations else 0
        report_lines.append(f"- **{status}**: {count} ({pct:.1f}%)")
    report_lines.append("")
    
    # Relation Distribution
    report_lines.append("### Speaker-Topic Relations (LLM Classification)")
    report_lines.append("")
    total_relations = sum(comparison['relation_distribution'].values())
    for relation, count in sorted(comparison['relation_distribution'].items(),
                                 key=lambda x: x[1], reverse=True):
        pct = (count / total_relations * 100) if total_relations > 0 else 0
        report_lines.append(f"- **{relation}**: {count} ({pct:.1f}%)")
    report_lines.append("")
    
    # Confidence Distribution
    report_lines.append("### Confidence Distribution")
    report_lines.append("")
    for confidence, count in sorted(comparison['confidence_distribution'].items(),
                                   key=lambda x: x[1], reverse=True):
        pct = (count / len(llm_annotations) * 100) if llm_annotations else 0
        report_lines.append(f"- **{confidence}**: {count} ({pct:.1f}%)")
    report_lines.append("")
    
    # Detailed Topic Analysis
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Detailed Topic Analysis")
    report_lines.append("")
    
    # Group by status
    by_status = {}
    for ann in llm_annotations:
        if ann.status not in by_status:
            by_status[ann.status] = []
        by_status[ann.status].append(ann)
    
    for status in sorted(by_status.keys(), key=lambda x: len(by_status[x]), reverse=True):
        topics = by_status[status]
        report_lines.append(f"### {status.upper()} Topics ({len(topics)})")
        report_lines.append("")
        
        for ann in topics[:10]:  # Show first 10 of each status
            report_lines.append(f"**{ann.topic_id}** - Introduced by {ann.introducer}")
            report_lines.append(f"- Time: {ann.start_time:.1f}s - {ann.end_time:.1f}s")
            report_lines.append(f"- Confidence: {ann.confidence}")
            report_lines.append(f"- Justification: {ann.justification[:200]}...")
            report_lines.append("")
            report_lines.append("Speaker Orientations:")
            for orientation in ann.speaker_orientations[:5]:  # First 5 orientations
                report_lines.append(f"  - {orientation['speaker']}: **{orientation['relation']}**")
                report_lines.append(f"    Turn {orientation['turn_index']}: {orientation['justification'][:150]}...")
            report_lines.append("")
        
        if len(topics) > 10:
            report_lines.append(f"*... and {len(topics) - 10} more {status} topics*")
        report_lines.append("")
    
    # Comparison with Structural Analysis
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Comparison: Structural vs LLM Analysis")
    report_lines.append("")
    report_lines.append(f"- **Structural Topics Detected**: {comparison['structural_count']}")
    report_lines.append(f"- **LLM Annotations Generated**: {comparison['llm_count']}")
    report_lines.append(f"- **Aligned Topics**: {len(comparison['aligned_topics'])}")
    report_lines.append("")
    
    # Key Insights
    report_lines.append("---")
    report_lines.append("")
    report_lines.append("## Key Insights")
    report_lines.append("")
    
    # Most common relations
    top_relations = sorted(comparison['relation_distribution'].items(),
                          key=lambda x: x[1], reverse=True)[:3]
    report_lines.append("### Most Common Speaker Orientations")
    for relation, count in top_relations:
        report_lines.append(f"- **{relation}**: {count} instances")
    report_lines.append("")
    
    # Status insights
    report_lines.append("### Topic Status Insights")
    if 'failed' in comparison['status_distribution']:
        failed_count = comparison['status_distribution']['failed']
        report_lines.append(f"- {failed_count} topics classified as failed (no uptake)")
    if 'emerged' in comparison['status_distribution']:
        emerged_count = comparison['status_distribution']['emerged']
        report_lines.append(f"- {emerged_count} topics classified as emerged (successful)")
    if 'transformed' in comparison['status_distribution']:
        transformed_count = comparison['status_distribution']['transformed']
        report_lines.append(f"- {transformed_count} topics classified as transformed (reframed)")
    report_lines.append("")
    
    # Write report
    with open('llm_analysis_summary_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("Summary report saved to llm_analysis_summary_report.md")

if __name__ == "__main__":
    main()
