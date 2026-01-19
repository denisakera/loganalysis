import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns
from collections import defaultdict, Counter
from datetime import timedelta
import warnings
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')

# Set style for neutral, legible visualizations
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_transcript(filepath):
    """Load and parse the JSON transcript file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['segments']

def is_filler(text):
    """Check if text is a filler token."""
    text_clean = text.strip()
    return text_clean in ['.', '...', '', ' .', '. '] or len(text_clean) == 0

def get_speaker(seg):
    """Extract speaker from segment, handling various formats."""
    # Try segment-level speaker first
    if 'speaker' in seg and seg['speaker']:
        return seg['speaker']
    # Try to get from words array (most common speaker)
    if 'words' in seg and seg['words']:
        speaker_counts = Counter([w.get('speaker') for w in seg['words'] if w.get('speaker')])
        if speaker_counts:
            return speaker_counts.most_common(1)[0][0]
    return 'UNKNOWN'

def compute_speaking_time(segments):
    """Compute total speaking time per speaker."""
    speaker_times = defaultdict(float)
    total_meeting_time = 0
    
    for seg in segments:
        start = seg['start']
        end = seg['end']
        speaker = get_speaker(seg)
        duration = end - start
        
        # Only count non-filler segments for speaking time
        if not is_filler(seg['text']):
            speaker_times[speaker] += duration
        
        # Track total meeting time (from first to last timestamp)
        if end > total_meeting_time:
            total_meeting_time = end
    
    return dict(speaker_times), total_meeting_time

def compute_turn_taking(segments):
    """Analyze turn-taking structure."""
    turns = []
    current_speaker = None
    current_turn_start = None
    current_turn_end = None
    
    for seg in segments:
        speaker = get_speaker(seg)
        start = seg['start']
        end = seg['end']
        
        if speaker != current_speaker:
            # New turn
            if current_speaker is not None:
                turns.append({
                    'speaker': current_speaker,
                    'start': current_turn_start,
                    'end': current_turn_end,
                    'duration': current_turn_end - current_turn_start
                })
            current_speaker = speaker
            current_turn_start = start
            current_turn_end = end
        else:
            # Same speaker continues
            current_turn_end = end
    
    # Add last turn
    if current_speaker is not None:
        turns.append({
            'speaker': current_speaker,
            'start': current_turn_start,
            'end': current_turn_end,
            'duration': current_turn_end - current_turn_start
        })
    
    # Aggregate by speaker
    turn_stats = defaultdict(lambda: {'count': 0, 'total_duration': 0, 'durations': []})
    for turn in turns:
        speaker = turn['speaker']
        turn_stats[speaker]['count'] += 1
        turn_stats[speaker]['total_duration'] += turn['duration']
        turn_stats[speaker]['durations'].append(turn['duration'])
    
    # Calculate averages
    for speaker in turn_stats:
        count = turn_stats[speaker]['count']
        turn_stats[speaker]['avg_duration'] = turn_stats[speaker]['total_duration'] / count if count > 0 else 0
    
    return turns, dict(turn_stats)

def detect_interruptions(segments, threshold=0.5):
    """Detect potential interruptions and overlaps."""
    interruptions = []
    overlaps = []
    
    for i in range(len(segments) - 1):
        current = segments[i]
        next_seg = segments[i + 1]
        
        current_end = current['end']
        next_start = next_seg['start']
        current_speaker = get_speaker(current)
        next_speaker = get_speaker(next_seg)
        
        # Check for overlap
        if current['end'] > next_seg['start']:
            overlap_duration = current['end'] - next_seg['start']
            overlaps.append({
                'speaker1': current_speaker,
                'speaker2': next_speaker,
                'overlap_duration': overlap_duration,
                'time': current['end']
            })
        
        # Check for rapid turn-taking (potential interruption)
        if current_speaker != next_speaker:
            gap = next_start - current_end
            if gap < threshold:
                interruptions.append({
                    'interrupted': current_speaker,
                    'interrupter': next_speaker,
                    'gap': gap,
                    'time': current_end
                })
    
    return interruptions, overlaps

def build_interaction_graph(segments):
    """Build directed graph of speaker transitions."""
    transitions = defaultdict(int)
    transition_durations = defaultdict(list)
    
    for i in range(len(segments) - 1):
        current = segments[i]
        next_seg = segments[i + 1]
        
        current_speaker = get_speaker(current)
        next_speaker = get_speaker(next_seg)
        
        if current_speaker != next_speaker:
            edge = (current_speaker, next_speaker)
            transitions[edge] += 1
            transition_durations[edge].append(next_seg['start'] - current['end'])
    
    return dict(transitions), dict(transition_durations)

def build_response_oriented_graph(segments, turns):
    """Build graph where edges represent responses, showing who orients to whom.
    Edge weight encodes duration of response chains, capturing capacity to elicit extended uptake."""
    responses = defaultdict(lambda: {'count': 0, 'total_duration': 0, 'durations': []})
    
    # Map segments to turns
    turn_map = {}
    for turn in turns:
        for seg in segments:
            seg_speaker = get_speaker(seg)
            if seg_speaker == turn['speaker'] and seg['start'] >= turn['start'] and seg['end'] <= turn['end']:
                turn_map[id(seg)] = turn
    
    # Find response chains: when speaker B responds to speaker A
    for i in range(len(segments) - 1):
        current = segments[i]
        next_seg = segments[i + 1]
        
        current_speaker = get_speaker(current)
        next_speaker = get_speaker(next_seg)
        
        if current_speaker != next_speaker:
            # This is a response: B responds to A
            edge = (current_speaker, next_speaker)
            
            # Calculate response chain duration: how long does B's response continue?
            response_duration = 0
            j = i + 1
            while j < len(segments):
                seg = segments[j]
                if get_speaker(seg) == next_speaker:
                    response_duration += seg['end'] - seg['start']
                    j += 1
                else:
                    break
            
            responses[edge]['count'] += 1
            responses[edge]['total_duration'] += response_duration
            responses[edge]['durations'].append(response_duration)
    
    # Calculate average response chain duration
    response_graph = {}
    for edge, data in responses.items():
        response_graph[edge] = {
            'frequency': data['count'],
            'total_duration': data['total_duration'],
            'avg_duration': data['total_duration'] / data['count'] if data['count'] > 0 else 0,
            'max_duration': max(data['durations']) if data['durations'] else 0
        }
    
    return response_graph

def detect_failed_interruptions(segments, interruptions, turns):
    """Detect failed interruptions: interruption attempts where floor is maintained.
    Interruption tolerance = who is interrupted without losing the floor."""
    failed_interruptions = []
    interruption_tolerance = defaultdict(lambda: {'attempts': 0, 'maintained_floor': 0})
    
    # Create turn timeline
    turn_timeline = sorted(turns, key=lambda x: x['start'])
    
    for inter in interruptions:
        inter_time = inter['time']
        interrupted_speaker = inter['interrupted']
        interrupter = inter['interrupter']
        
        # Find the turn that was interrupted
        interrupted_turn = None
        for turn in turn_timeline:
            if turn['speaker'] == interrupted_speaker and turn['start'] <= inter_time <= turn['end']:
                interrupted_turn = turn
                break
        
        if interrupted_turn:
            # Check if interrupted speaker continues after interruption
            # Look for next segment by interrupted speaker after interruption
            continued = False
            continuation_time = None
            
            for seg in segments:
                seg_speaker = get_speaker(seg)
                if seg_speaker == interrupted_speaker and seg['start'] > inter_time:
                    # Check if this is continuation of same turn or new turn
                    if interrupted_turn['end'] > seg['start'] or (seg['start'] - interrupted_turn['end']) < 2.0:
                        continued = True
                        continuation_time = seg['start']
                        break
            
            interruption_tolerance[interrupted_speaker]['attempts'] += 1
            
            if continued:
                failed_interruptions.append({
                    'interrupted': interrupted_speaker,
                    'interrupter': interrupter,
                    'time': inter_time,
                    'maintained_floor': True,
                    'continuation_time': continuation_time,
                    'gap': continuation_time - inter_time if continuation_time else None
                })
                interruption_tolerance[interrupted_speaker]['maintained_floor'] += 1
            else:
                failed_interruptions.append({
                    'interrupted': interrupted_speaker,
                    'interrupter': interrupter,
                    'time': inter_time,
                    'maintained_floor': False
                })
    
    # Calculate tolerance rates
    tolerance_rates = {}
    for speaker, data in interruption_tolerance.items():
        if data['attempts'] > 0:
            tolerance_rates[speaker] = {
                'attempts': data['attempts'],
                'maintained': data['maintained_floor'],
                'tolerance_rate': data['maintained_floor'] / data['attempts']
            }
        else:
            tolerance_rates[speaker] = {
                'attempts': 0,
                'maintained': 0,
                'tolerance_rate': 0
            }
    
    return failed_interruptions, tolerance_rates

def create_floor_holding_timeline(segments, interruptions, failed_interruptions, speaker_times):
    """Create timeline showing floor holding with interruption attempts marked.
    Shows uninterrupted stretches in relation to attempted interruptions."""
    top_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:10]
    top_speaker_set = set([s[0] for s in top_speakers])
    
    # Create timeline data with interruption markers
    timeline_data = []
    interruption_markers = []
    
    for seg in segments:
        speaker = get_speaker(seg)
        if speaker in top_speaker_set and not is_filler(seg['text']):
            timeline_data.append({
                'speaker': speaker,
                'start': seg['start'],
                'end': seg['end'],
                'duration': seg['end'] - seg['start']
            })
    
    # Mark interruptions
    for inter in interruptions:
        interrupted = inter['interrupted']
        if interrupted in top_speaker_set:
            # Check if floor was maintained
            failed = next((f for f in failed_interruptions if 
                          f['interrupted'] == interrupted and 
                          abs(f['time'] - inter['time']) < 0.1), None)
            
            interruption_markers.append({
                'time': inter['time'],
                'interrupted': interrupted,
                'interrupter': inter['interrupter'],
                'maintained': failed['maintained_floor'] if failed else False
            })
    
    return timeline_data, interruption_markers

def identify_conversational_attractors(response_graph, speaker_times):
    """Identify conversational attractors: speakers who elicit extended responses.
    Based on response chain duration, not just frequency."""
    attractor_scores = defaultdict(lambda: {'incoming_responses': 0, 'total_response_duration': 0, 
                                            'avg_response_duration': 0, 'max_response_duration': 0})
    
    for (source, target), data in response_graph.items():
        # Source attracts responses from target
        attractor_scores[source]['incoming_responses'] += data['frequency']
        attractor_scores[source]['total_response_duration'] += data['total_duration']
        if data['max_duration'] > attractor_scores[source]['max_response_duration']:
            attractor_scores[source]['max_response_duration'] = data['max_duration']
    
    # Calculate averages
    for speaker, scores in attractor_scores.items():
        if scores['incoming_responses'] > 0:
            scores['avg_response_duration'] = scores['total_response_duration'] / scores['incoming_responses']
    
    return dict(attractor_scores)

def extract_text_from_segment(seg):
    """Extract clean text from segment."""
    text = seg.get('text', '').strip()
    # Remove excessive punctuation and normalize
    text = re.sub(r'\.{3,}', '...', text)
    text = re.sub(r'\s+', ' ', text)
    return text

def compute_semantic_similarity(texts, similarity_threshold=0.3):
    """Compute semantic similarity matrix using TF-IDF and cosine similarity."""
    if len(texts) < 2:
        return np.array([[1.0]])
    
    # Filter out empty texts
    filtered_texts = [t for t in texts if t and len(t.strip()) > 0]
    if len(filtered_texts) < 2:
        # Fallback: simple word overlap
        similarity_matrix = np.zeros((len(texts), len(texts)))
        for i, text1 in enumerate(texts):
            words1 = set(text1.lower().split()) if text1 else set()
            for j, text2 in enumerate(texts):
                words2 = set(text2.lower().split()) if text2 else set()
                if words1 and words2:
                    overlap = len(words1 & words2) / len(words1 | words2) if (words1 | words2) else 0
                    similarity_matrix[i, j] = overlap
                elif i == j:
                    similarity_matrix[i, j] = 1.0
        return similarity_matrix
    
    # Use TF-IDF vectorization
    try:
        vectorizer = TfidfVectorizer(max_features=100, stop_words='english', 
                                    ngram_range=(1, 2), min_df=1, token_pattern=r'\b\w+\b')
        tfidf_matrix = vectorizer.fit_transform(filtered_texts)
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # Map back to original indices if some texts were filtered
        if len(filtered_texts) < len(texts):
            full_matrix = np.zeros((len(texts), len(texts)))
            filtered_idx = 0
            for i, text in enumerate(texts):
                if text and len(text.strip()) > 0:
                    full_idx = 0
                    for j, text2 in enumerate(texts):
                        if text2 and len(text2.strip()) > 0:
                            full_matrix[i, j] = similarity_matrix[filtered_idx, full_idx]
                            full_idx += 1
                    filtered_idx += 1
            return full_matrix
        
        return similarity_matrix
    except Exception as e:
        # Fallback: simple word overlap
        similarity_matrix = np.zeros((len(texts), len(texts)))
        for i, text1 in enumerate(texts):
            words1 = set(text1.lower().split()) if text1 else set()
            for j, text2 in enumerate(texts):
                words2 = set(text2.lower().split()) if text2 else set()
                if words1 and words2:
                    overlap = len(words1 & words2) / len(words1 | words2) if (words1 | words2) else 0
                    similarity_matrix[i, j] = overlap
                elif i == j:
                    similarity_matrix[i, j] = 1.0
        return similarity_matrix

def detect_topic_proposals(segments, turns, similarity_threshold=0.25, window_size=5):
    """Detect topic proposals: turns that introduce new lexical clusters not present in preceding turns."""
    topic_proposals = []
    
    # Get turn texts with full content
    turn_texts = []
    turn_full_texts = []  # Store full text for each turn
    for turn in turns:
        # Collect all segment texts for this turn
        turn_segments = [s for s in segments if 
                        get_speaker(s) == turn['speaker'] and
                        turn['start'] <= s['start'] <= turn['end']]
        turn_text = ' '.join([extract_text_from_segment(s) for s in turn_segments 
                              if not is_filler(s.get('text', ''))])
        turn_texts.append(turn_text)
        turn_full_texts.append(turn_text)  # Store full text
    
    # Compare each turn with preceding window
    for i, turn in enumerate(turns):
        if i < window_size:
            # Early turns: compare with all preceding
            preceding_texts = turn_texts[:i]
        else:
            # Later turns: compare with window
            preceding_texts = turn_texts[i-window_size:i]
        
        if not preceding_texts or not turn_texts[i]:
            continue
        
        # Compute similarity with preceding turns
        comparison_texts = preceding_texts + [turn_texts[i]]
        similarity_matrix = compute_semantic_similarity(comparison_texts)
        
        # Check if current turn is similar to any preceding turn
        current_idx = len(comparison_texts) - 1
        max_similarity = max([similarity_matrix[current_idx, j] 
                             for j in range(len(preceding_texts))]) if preceding_texts else 0
        
        # If similarity is low, this is a potential topic proposal
        if max_similarity < similarity_threshold and len(turn_texts[i].split()) > 3:
            topic_proposals.append({
                'topic_id': f'TOPIC_{len(topic_proposals)}',
                'proposer': turn['speaker'],
                'start_time': turn['start'],
                'end_time': turn['end'],
                'text': turn_full_texts[i],  # FULL TEXT, not truncated
                'text_sample': turn_full_texts[i][:200],  # Sample for display
                'similarity_to_preceding': max_similarity,
                'turn_index': i
            })
    
    return topic_proposals

def check_topic_stabilization(topic_proposal, segments, turns, similarity_threshold=0.3, response_window=30):
    """Check if topic is stabilized: at least one other speaker responds with semantic overlap."""
    proposal_text = topic_proposal['text']
    proposal_time = topic_proposal['start_time']
    proposer = topic_proposal['proposer']
    
    # Find turns after proposal within response window
    subsequent_turns = [t for t in turns 
                       if t['start'] > proposal_time and 
                       t['start'] < proposal_time + response_window and
                       t['speaker'] != proposer]
    
    if not subsequent_turns:
        return {'stabilized': False, 'reason': 'no_response', 'responders': []}
    
    # Get texts of subsequent turns WITH FULL CONTENT
    subsequent_texts = []
    for turn in subsequent_turns:
        turn_segments = [s for s in segments if 
                        get_speaker(s) == turn['speaker'] and
                        turn['start'] <= s['start'] <= turn['end']]
        turn_text = ' '.join([extract_text_from_segment(s) for s in turn_segments 
                              if not is_filler(s.get('text', ''))])
        subsequent_texts.append((turn, turn_text))
    
    # Check semantic overlap
    responders = []
    for turn, text in subsequent_texts:
        if not text:
            continue
        comparison_texts = [proposal_text, text]
        similarity_matrix = compute_semantic_similarity(comparison_texts)
        similarity = similarity_matrix[0, 1]
        
        if similarity >= similarity_threshold:
            responders.append({
                'speaker': turn['speaker'],
                'time': turn['start'],
                'similarity': similarity,
                'response_delay': turn['start'] - proposal_time,
                'response_text': text,  # FULL RESPONSE TEXT
                'response_duration': turn['duration']
            })
        else:
            # Also track non-uptake responses for analysis
            responders.append({
                'speaker': turn['speaker'],
                'time': turn['start'],
                'similarity': similarity,
                'response_delay': turn['start'] - proposal_time,
                'response_text': text,
                'response_duration': turn['duration'],
                'uptake': False  # Mark as non-uptake
            })
    
    # Filter to only uptake responses for stabilization check
    uptake_responders = [r for r in responders if r.get('similarity', 0) >= similarity_threshold]
    
    if uptake_responders:
        return {
            'stabilized': True,
            'reason': 'uptake',
            'responders': uptake_responders,
            'all_responses': responders,  # Include all responses for analysis
            'first_response_time': min([r['time'] for r in uptake_responders]),
            'first_response_delay': min([r['response_delay'] for r in uptake_responders])
        }
    else:
        return {
            'stabilized': False,
            'reason': 'no_semantic_overlap',
            'responders': [],
            'all_responses': responders  # Track all responses even if no uptake
        }

def analyze_topic_lifecycle(segments, turns, similarity_threshold=0.25, stabilization_threshold=0.3):
    """Analyze complete topic lifecycle: emergence, stabilization, decay."""
    # Detect topic proposals
    proposals = detect_topic_proposals(segments, turns, similarity_threshold)
    
    topics = []
    for proposal in proposals:
        # Check stabilization
        stabilization = check_topic_stabilization(proposal, segments, turns, stabilization_threshold)
        
        # Determine topic status
        if stabilization['stabilized']:
            status = 'stabilized'
        else:
            # Check if followed by silence, interruption, or unrelated speech
            subsequent_turns = [t for t in turns if t['start'] > proposal['end_time']]
            if not subsequent_turns or (subsequent_turns[0]['start'] - proposal['end_time']) > 5.0:
                status = 'failed_silence'
            else:
                status = 'failed_no_uptake'
        
        topic = {
            'topic_id': proposal['topic_id'],
            'proposer': proposal['proposer'],
            'start_time': proposal['start_time'],
            'end_time': proposal['end_time'],
            'status': status,
            'stabilization': stabilization,
            'text': proposal['text'],  # FULL TEXT
            'text_sample': proposal.get('text_sample', proposal['text'][:200]),
            'similarity_to_preceding': proposal.get('similarity_to_preceding', 0)
        }
        topics.append(topic)
    
    return topics

def analyze_speaker_orientation_to_topics(topics, segments, turns, similarity_threshold=0.3):
    """Analyze how speakers orient to topics: uptake, redirection, monopolization."""
    speaker_orientations = defaultdict(lambda: {
        'topics_proposed': [],
        'topics_responded_to': [],
        'uptake_delays': [],
        'redirections': [],
        'monopolizations': []
    })
    
    for topic in topics:
        proposer = topic['proposer']
        speaker_orientations[proposer]['topics_proposed'].append(topic['topic_id'])
        
        if topic['status'] == 'stabilized':
            # Track responders
            for responder in topic['stabilization']['responders']:
                speaker = responder['speaker']
                speaker_orientations[speaker]['topics_responded_to'].append(topic['topic_id'])
                speaker_orientations[speaker]['uptake_delays'].append(responder['response_delay'])
            
            # Check for redirection/reframing
            # (Simplified: if response similarity is moderate, might be redirection)
            for responder in topic['stabilization']['responders']:
                if 0.3 <= responder['similarity'] < 0.6:
                    speaker_orientations[responder['speaker']]['redirections'].append(topic['topic_id'])
        
        # Check for monopolization (proposer extends own topic without others)
        if topic['status'] == 'stabilized':
            # Count how many times proposer speaks about this topic
            topic_turns = [t for t in turns if 
                          t['speaker'] == proposer and
                          topic['start_time'] <= t['start'] <= topic['end_time'] + 30]
            other_turns = [t for t in turns if
                          t['speaker'] != proposer and
                          topic['start_time'] <= t['start'] <= topic['end_time'] + 30]
            
            if len(topic_turns) > len(other_turns) * 2:
                speaker_orientations[proposer]['monopolizations'].append(topic['topic_id'])
    
    return dict(speaker_orientations)

def create_topic_timeline(topics, turns, total_time):
    """Create temporal visualization of topic emergence, stabilization, and decay."""
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Group topics by status
    stabilized = [t for t in topics if t['status'] == 'stabilized']
    failed_silence = [t for t in topics if t['status'] == 'failed_silence']
    failed_no_uptake = [t for t in topics if t['status'] == 'failed_no_uptake']
    
    y_pos = 0
    y_positions = {}
    
    # Assign y positions to topics
    for topic in topics:
        y_positions[topic['topic_id']] = y_pos
        y_pos += 1
    
    # Color map
    color_map = {
        'stabilized': 'green',
        'failed_silence': 'red',
        'failed_no_uptake': 'orange'
    }
    
    # Draw topic bars
    for topic in topics:
        y = y_positions[topic['topic_id']]
        color = color_map.get(topic['status'], 'gray')
        duration = topic['end_time'] - topic['start_time']
        
        ax.barh(y, duration, left=topic['start_time'], height=0.6,
               color=color, alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # Mark first response if stabilized
        if topic['status'] == 'stabilized' and topic['stabilization'].get('first_response_time'):
            ax.scatter(topic['stabilization']['first_response_time'], y,
                      c='blue', s=100, marker='*', zorder=5, edgecolors='black')
    
    # Labels
    topic_labels = [f"{t['topic_id']} ({t['proposer']})" for t in topics]
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(topic_labels, fontsize=8)
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_title('Topic Timeline: Emergence, Stabilization, and Decay\n(Green=Stabilized, Orange=Failed (no uptake), Red=Failed (silence), Blue*=First Response)', 
                 fontsize=14, pad=15)
    ax.grid(axis='x', alpha=0.3)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='green', label='Stabilized (uptake)'),
        Patch(facecolor='orange', label='Failed (no uptake)'),
        Patch(facecolor='red', label='Failed (silence)'),
        plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='blue', 
                  markersize=10, label='First Response')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('topic_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_speaker_topic_network(topics, speaker_orientations, speaker_times):
    """Create bipartite graph linking speakers to topics, weighted by uptake duration."""
    G = nx.Graph()
    
    # Add speaker nodes
    for speaker in speaker_times.keys():
        G.add_node(speaker, node_type='speaker', size=speaker_times[speaker])
    
    # Add topic nodes
    for topic in topics:
        G.add_node(topic['topic_id'], node_type='topic', status=topic['status'])
    
    # Add edges: speaker-topic relationships
    for speaker, orientation in speaker_orientations.items():
        # Proposer edges
        for topic_id in orientation['topics_proposed']:
            topic = next((t for t in topics if t['topic_id'] == topic_id), None)
            if topic:
                duration = topic['end_time'] - topic['start_time']
                G.add_edge(speaker, topic_id, 
                          relationship='proposed',
                          weight=duration,
                          duration=duration)
        
        # Responder edges
        for topic_id in orientation['topics_responded_to']:
            topic = next((t for t in topics if t['topic_id'] == topic_id), None)
            if topic and topic['status'] == 'stabilized':
                # Find this speaker's response
                responder = next((r for r in topic['stabilization']['responders'] 
                                 if r['speaker'] == speaker), None)
                if responder:
                    G.add_edge(speaker, topic_id,
                              relationship='responded',
                              weight=responder['similarity'] * 10,  # Weight by similarity
                              response_delay=responder['response_delay'],
                              similarity=responder['similarity'])
    
    # Create visualization
    plt.figure(figsize=(16, 12))
    
    # Separate nodes by type
    speaker_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'speaker']
    topic_nodes = [n for n, d in G.nodes(data=True) if d.get('node_type') == 'topic']
    
    # Layout: speakers on left, topics on right
    pos = {}
    
    # Position speakers (left side)
    speaker_y_positions = np.linspace(0, 10, len(speaker_nodes))
    for i, speaker in enumerate(speaker_nodes):
        pos[speaker] = (0, speaker_y_positions[i])
    
    # Position topics (right side)
    topic_y_positions = np.linspace(0, 10, len(topic_nodes))
    for i, topic in enumerate(topic_nodes):
        pos[topic] = (10, topic_y_positions[i])
    
    # Draw edges
    proposed_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('relationship') == 'proposed']
    responded_edges = [(u, v) for u, v, d in G.edges(data=True) if d.get('relationship') == 'responded']
    
    nx.draw_networkx_edges(G, pos, edgelist=proposed_edges, 
                          edge_color='blue', alpha=0.3, width=1, style='solid')
    nx.draw_networkx_edges(G, pos, edgelist=responded_edges,
                          edge_color='green', alpha=0.5, width=2, style='dashed')
    
    # Draw nodes
    max_time = max(speaker_times.values()) if speaker_times else 1
    speaker_sizes = [speaker_times.get(n, 0) / max_time * 1000 for n in speaker_nodes]
    
    nx.draw_networkx_nodes(G, pos, nodelist=speaker_nodes, 
                          node_size=speaker_sizes, node_color='lightblue',
                          alpha=0.7, edgecolors='black')
    
    # Color topics by status
    topic_colors = []
    for topic in topic_nodes:
        status = G.nodes[topic].get('status', 'unknown')
        if status == 'stabilized':
            topic_colors.append('green')
        elif status == 'failed_silence':
            topic_colors.append('red')
        elif status == 'failed_no_uptake':
            topic_colors.append('orange')
        else:
            topic_colors.append('gray')
    
    nx.draw_networkx_nodes(G, pos, nodelist=topic_nodes,
                          node_size=800, node_color=topic_colors,
                          alpha=0.7, edgecolors='black')
    
    # Labels
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    plt.title('Speaker-Topic Network\n(Blue=Proposed, Green=Dashed=Responded, Square=Topic, Circle=Speaker)', 
              fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('speaker_topic_network.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return G

def create_topic_trajectory(topics, segments, turns):
    """For each topic, show how it travels between speakers or stalls. Shows ALL topics."""
    # Show all topics, not just stabilized ones, and not just first 6
    all_topics = topics  # Show all topics
    
    if not all_topics:
        return
    
    # Create figure with subplots for all topics (limit to reasonable number for visualization)
    n_topics = min(len(all_topics), 30)  # Show up to 30 topics, or create scrollable view
    fig, axes = plt.subplots(n_topics, 1, figsize=(16, 2 * n_topics))
    if n_topics == 1:
        axes = [axes]
    
    for idx, topic in enumerate(all_topics[:n_topics]):  # Show ALL topics up to limit
        ax = axes[idx] if n_topics > 1 else axes[0]
        
        # Get all turns related to this topic
        topic_turns = [t for t in turns if 
                      topic['start_time'] <= t['start'] <= topic['end_time'] + 30]
        
        # Track speaker sequence
        speaker_sequence = []
        for turn in topic_turns:
            speaker_sequence.append({
                'speaker': turn['speaker'],
                'time': turn['start'],
                'duration': turn['duration']
            })
        
        # Create timeline
        speakers = list(set([s['speaker'] for s in speaker_sequence]))
        y_positions = {s: i for i, s in enumerate(speakers)}
        
        # Draw bars
        for seq in speaker_sequence:
            y = y_positions[seq['speaker']]
            ax.barh(y, seq['duration'], left=seq['time'], height=0.6,
                   alpha=0.7, edgecolor='black', linewidth=0.5)
        
        ax.set_yticks(list(y_positions.values()))
        ax.set_yticklabels(list(y_positions.keys()), fontsize=8)
        ax.set_xlabel('Time (seconds)', fontsize=10)
        # Include topic text in title (truncated if too long)
        topic_text_preview = topic.get('text', topic.get('text_sample', ''))[:80]
        ax.set_title(f"{topic['topic_id']} - {topic['proposer']} ({topic['status']}): {topic_text_preview}...", 
                    fontsize=10, pad=10)
        ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('topic_trajectories.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Also create a detailed text report of all topics
    create_topic_content_report(topics, segments, turns)

def create_topic_content_report(topics, segments, turns):
    """Create detailed text report with full topic content and speaker engagement."""
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("TOPIC EMERGENCE CONTENT ANALYSIS")
    report_lines.append("=" * 80)
    report_lines.append(f"\nTotal Topics Detected: {len(topics)}\n")
    
    # Group by status
    stabilized = [t for t in topics if t['status'] == 'stabilized']
    failed_no_uptake = [t for t in topics if t['status'] == 'failed_no_uptake']
    failed_silence = [t for t in topics if t['status'] == 'failed_silence']
    
    report_lines.append(f"Stabilized Topics: {len(stabilized)}")
    report_lines.append(f"Failed (No Uptake): {len(failed_no_uptake)}")
    report_lines.append(f"Failed (Silence): {len(failed_silence)}")
    report_lines.append("\n" + "=" * 80 + "\n")
    
    # Detailed topic analysis
    for topic in topics:
        report_lines.append(f"\n{topic['topic_id']}")
        report_lines.append("-" * 80)
        report_lines.append(f"Proposer: {topic['proposer']}")
        report_lines.append(f"Time: {topic['start_time']:.2f}s - {topic['end_time']:.2f}s")
        report_lines.append(f"Status: {topic['status']}")
        report_lines.append(f"Similarity to Preceding: {topic.get('similarity_to_preceding', 0):.3f}")
        report_lines.append(f"\nTOPIC CONTENT:")
        report_lines.append(f"{topic.get('text', topic.get('text_sample', 'N/A'))}")
        
        if topic['status'] == 'stabilized' and topic['stabilization'].get('responders'):
            report_lines.append(f"\nSTABILIZATION - Uptake Received:")
            for responder in topic['stabilization']['responders']:
                report_lines.append(f"\n  Responder: {responder['speaker']}")
                report_lines.append(f"  Response Time: {responder['time']:.2f}s")
                report_lines.append(f"  Response Delay: {responder['response_delay']:.2f}s")
                report_lines.append(f"  Semantic Similarity: {responder['similarity']:.3f}")
                report_lines.append(f"  Response Duration: {responder.get('response_duration', 0):.2f}s")
                report_lines.append(f"  Response Text: {responder.get('response_text', 'N/A')[:300]}...")
        elif topic['stabilization'].get('all_responses'):
            report_lines.append(f"\nRESPONSES (No Uptake):")
            for response in topic['stabilization']['all_responses']:
                report_lines.append(f"\n  Speaker: {response['speaker']}")
                report_lines.append(f"  Response Time: {response['time']:.2f}s")
                report_lines.append(f"  Semantic Similarity: {response['similarity']:.3f} (below threshold)")
                report_lines.append(f"  Response Text: {response.get('response_text', 'N/A')[:300]}...")
        else:
            report_lines.append(f"\nNo responses detected within response window.")
        
        report_lines.append("\n" + "=" * 80 + "\n")
    
    # Speaker summary
    report_lines.append("\n" + "=" * 80)
    report_lines.append("SPEAKER TOPIC ENGAGEMENT SUMMARY")
    report_lines.append("=" * 80 + "\n")
    
    proposer_counts = Counter([t['proposer'] for t in topics])
    for speaker, count in proposer_counts.most_common():
        speaker_topics = [t for t in topics if t['proposer'] == speaker]
        stabilized_count = len([t for t in speaker_topics if t['status'] == 'stabilized'])
        report_lines.append(f"{speaker}:")
        report_lines.append(f"  Topics Proposed: {count}")
        stabilization_pct = (stabilized_count/count*100) if count > 0 else 0.0
        report_lines.append(f"  Stabilized: {stabilized_count} ({stabilization_pct:.1f}%)")
        report_lines.append(f"  Failed: {count - stabilized_count}")
        report_lines.append("")
    
    # Write report
    with open('topic_content_analysis.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("  - topic_content_analysis.txt exported")

def create_topic_content_visualization(topics, speaker_times):
    """Create visualization showing topic content and speaker engagement."""
    # Create a detailed table/chart showing topic content
    stabilized_topics = [t for t in topics if t['status'] == 'stabilized']
    
    if not stabilized_topics:
        return
    
    fig, ax = plt.subplots(figsize=(20, max(10, len(stabilized_topics) * 0.5)))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = []
    headers = ['Topic ID', 'Proposer', 'Time (s)', 'Status', 'Topic Content (first 150 chars)', 
               'Responders', 'First Response Delay']
    
    for topic in stabilized_topics:
        responders_str = ', '.join([r['speaker'] for r in topic['stabilization'].get('responders', [])])
        delay = topic['stabilization'].get('first_response_delay', 0)
        topic_text = topic.get('text', topic.get('text_sample', ''))[:150]
        
        table_data.append([
            topic['topic_id'],
            topic['proposer'],
            f"{topic['start_time']:.1f}-{topic['end_time']:.1f}",
            topic['status'],
            topic_text,
            responders_str if responders_str else 'None',
            f"{delay:.2f}s" if delay else 'N/A'
        ])
    
    table = ax.table(cellText=table_data, colLabels=headers, 
                    cellLoc='left', loc='center',
                    colWidths=[0.08, 0.08, 0.1, 0.08, 0.4, 0.15, 0.11])
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 2)
    
    # Color code by status
    for i in range(len(table_data)):
        if table_data[i][3] == 'stabilized':
            for j in range(len(headers)):
                table[(i+1, j)].set_facecolor('#d4edda')
    
    plt.title('Stabilized Topics: Full Content and Speaker Engagement', fontsize=14, pad=20)
    plt.tight_layout()
    plt.savefig('topic_content_table.png', dpi=300, bbox_inches='tight')
    plt.close()

def detect_topic_closure_authority(topics, segments, turns, similarity_threshold=0.3):
    """Detect topic closure authority: who can end topics without contest.
    Power is visible in who shifts away from ongoing theme and others follow without repair."""
    closures = []
    
    # For each topic, check what happens after it ends
    for topic in topics:
        topic_end = topic['end_time']
        topic_text = topic.get('text', topic.get('text_sample', ''))
        
        # Find turns after topic ends (within 60 seconds)
        subsequent_turns = [t for t in turns if 
                           t['start'] > topic_end and 
                           t['start'] < topic_end + 60]
        
        if not subsequent_turns:
            continue
        
        # Check if next speaker shifts topic (low similarity)
        first_subsequent = subsequent_turns[0]
        first_speaker = first_subsequent['speaker']
        
        # Get text of first subsequent turn
        first_turn_segments = [s for s in segments if
                              get_speaker(s) == first_speaker and
                              first_subsequent['start'] <= s['start'] <= first_subsequent['end']]
        first_turn_text = ' '.join([extract_text_from_segment(s) for s in first_turn_segments
                                   if not is_filler(s.get('text', ''))])
        
        if not first_turn_text:
            continue
        
        # Check semantic similarity
        comparison_texts = [topic_text, first_turn_text]
        similarity_matrix = compute_semantic_similarity(comparison_texts)
        similarity = similarity_matrix[0, 1] if similarity_matrix.shape[0] > 1 else 0
        
        # If similarity is low, topic was closed/shifted
        if similarity < similarity_threshold:
            # Check if others follow (no repair/resistance)
            followers = []
            for turn in subsequent_turns[1:5]:  # Check next 4 turns
                turn_segments = [s for s in segments if
                               get_speaker(s) == turn['speaker'] and
                               turn['start'] <= s['start'] <= turn['end']]
                turn_text = ' '.join([extract_text_from_segment(s) for s in turn_segments
                                     if not is_filler(s.get('text', ''))])
                
                if turn_text:
                    # Check if they continue new topic or return to old
                    turn_comparison = [topic_text, turn_text]
                    turn_sim_matrix = compute_semantic_similarity(turn_comparison)
                    turn_similarity = turn_sim_matrix[0, 1] if turn_sim_matrix.shape[0] > 1 else 0
                    
                    if turn_similarity < similarity_threshold:
                        followers.append({
                            'speaker': turn['speaker'],
                            'time': turn['start'],
                            'similarity_to_old_topic': turn_similarity
                        })
            
            closures.append({
                'closed_topic': topic['topic_id'],
                'closed_by': topic['proposer'],
                'shifted_by': first_speaker,
                'shift_time': first_subsequent['start'],
                'closure_delay': first_subsequent['start'] - topic_end,
                'similarity_to_closed_topic': similarity,
                'followers': followers,
                'followers_count': len(followers),
                'uncontested': len(followers) > 0  # Others followed without repair
            })
    
    return closures

def detect_asymmetric_topical_accountability(topics, segments, turns):
    """Detect asymmetric topical accountability: who is asked to clarify/justify vs who isn't.
    Uneven demand for elaboration signals differential epistemic standing."""
    accountability_patterns = defaultdict(lambda: {
        'topics_proposed': [],
        'clarification_requests': 0,
        'justification_requests': 0,
        'evidence_requests': 0,
        'total_accountability_demands': 0
    })
    
    # Keywords/phrases indicating accountability demands
    clarification_indicators = ['what do you mean', 'can you clarify', 'what does that mean',
                               'can you explain', 'I don\'t understand', 'what are you saying',
                               'could you elaborate', 'what do you expect']
    justification_indicators = ['why', 'how do you know', 'what makes you think',
                               'on what basis', 'what evidence', 'how can you say']
    evidence_indicators = ['show me', 'prove it', 'where is the evidence', 'can you show',
                          'do you have proof', 'what proof']
    
    for topic in topics:
        proposer = topic['proposer']
        accountability_patterns[proposer]['topics_proposed'].append(topic['topic_id'])
        
        topic_start = topic['start_time']
        topic_end = topic['end_time']
        
        # Find responses within 30 seconds after topic
        responses = [t for t in turns if
                    t['start'] > topic_start and
                    t['start'] < topic_end + 30 and
                    t['speaker'] != proposer]
        
        for response_turn in responses:
            # Get response text
            response_segments = [s for s in segments if
                               get_speaker(s) == response_turn['speaker'] and
                               response_turn['start'] <= s['start'] <= response_turn['end']]
            response_text = ' '.join([extract_text_from_segment(s) for s in response_segments
                                     if not is_filler(s.get('text', ''))]).lower()
            
            # Check for accountability demands
            if any(indicator in response_text for indicator in clarification_indicators):
                accountability_patterns[proposer]['clarification_requests'] += 1
                accountability_patterns[proposer]['total_accountability_demands'] += 1
            
            if any(indicator in response_text for indicator in justification_indicators):
                accountability_patterns[proposer]['justification_requests'] += 1
                accountability_patterns[proposer]['total_accountability_demands'] += 1
            
            if any(indicator in response_text for indicator in evidence_indicators):
                accountability_patterns[proposer]['evidence_requests'] += 1
                accountability_patterns[proposer]['total_accountability_demands'] += 1
    
    # Calculate rates
    for speaker, data in accountability_patterns.items():
        topic_count = len(data['topics_proposed'])
        if topic_count > 0:
            data['accountability_rate'] = data['total_accountability_demands'] / topic_count
        else:
            data['accountability_rate'] = 0
    
    return dict(accountability_patterns)

def detect_topic_recycling(topics, segments, turns, similarity_threshold=0.4):
    """Detect topic recycling: topics initially ignored that gain traction when reintroduced by different speaker.
    Reveals authority as relational rather than propositional."""
    recycled_topics = []
    
    # Compare all topic pairs
    for i, topic1 in enumerate(topics):
        topic1_text = topic1.get('text', topic1.get('text_sample', ''))
        topic1_status = topic1['status']
        topic1_proposer = topic1['proposer']
        
        # Skip if first topic was successful
        if topic1_status == 'stabilized':
            continue
        
        # Look for similar topics later by different speakers
        for j, topic2 in enumerate(topics[i+1:], start=i+1):
            topic2_text = topic2.get('text', topic2.get('text_sample', ''))
            topic2_proposer = topic2['proposer']
            topic2_status = topic2['status']
            
            # Must be different speaker
            if topic1_proposer == topic2_proposer:
                continue
            
            # Check semantic similarity
            comparison_texts = [topic1_text, topic2_text]
            similarity_matrix = compute_semantic_similarity(comparison_texts)
            similarity = similarity_matrix[0, 1] if similarity_matrix.shape[0] > 1 else 0
            
            # If similar and second topic succeeded where first failed
            if similarity >= similarity_threshold:
                # Check if second topic had better outcome
                if topic2_status == 'stabilized' and topic1_status != 'stabilized':
                    recycled_topics.append({
                        'original_topic': topic1['topic_id'],
                        'original_proposer': topic1_proposer,
                        'original_status': topic1_status,
                        'recycled_topic': topic2['topic_id'],
                        'recycled_proposer': topic2_proposer,
                        'recycled_status': topic2_status,
                        'similarity': similarity,
                        'time_gap': topic2['start_time'] - topic1['end_time'],
                        'power_shift': True  # Authority shifted through speaker change
                    })
                elif topic2_status != 'stabilized' and topic2.get('stabilization', {}).get('responders'):
                    # Even if not fully stabilized, check if it got more responses
                    topic1_responses = len(topic1.get('stabilization', {}).get('all_responses', []))
                    topic2_responses = len(topic2.get('stabilization', {}).get('all_responses', []))
                    
                    if topic2_responses > topic1_responses:
                        recycled_topics.append({
                            'original_topic': topic1['topic_id'],
                            'original_proposer': topic1_proposer,
                            'original_status': topic1_status,
                            'recycled_topic': topic2['topic_id'],
                            'recycled_proposer': topic2_proposer,
                            'recycled_status': topic2_status,
                            'similarity': similarity,
                            'time_gap': topic2['start_time'] - topic1['end_time'],
                            'power_shift': True,
                            'response_increase': topic2_responses - topic1_responses
                        })
    
    return recycled_topics

def detect_topic_hijacking_vs_alignment(topics, segments, turns, similarity_threshold=0.3):
    """Detect topic hijacking vs alignment: reframing while preserving legitimacy.
    Aligns with Goffman's footing shifts - repositioning within interaction."""
    hijackings = []
    
    for topic in topics:
        topic_text = topic.get('text', topic.get('text_sample', ''))
        topic_proposer = topic['proposer']
        
        # Get responses to this topic
        responses = topic.get('stabilization', {}).get('all_responses', [])
        
        for response in responses:
            responder = response['speaker']
            response_text = response.get('response_text', '')
            similarity = response.get('similarity', 0)
            
            if not response_text:
                continue
            
            # Moderate similarity (0.3-0.6) suggests reframing/hijacking
            # Low similarity (<0.3) suggests complete shift
            # High similarity (>0.6) suggests alignment
            
            if 0.3 <= similarity < 0.6:
                # Potential hijacking: reframing while preserving legitimacy
                hijackings.append({
                    'topic_id': topic['topic_id'],
                    'topic_proposer': topic_proposer,
                    'hijacked_by': responder,
                    'original_text': topic_text[:200],
                    'response_text': response_text[:200],
                    'similarity': similarity,
                    'type': 'hijacking' if similarity < 0.45 else 'reframing',
                    'preserves_legitimacy': True  # Still semantically connected
                })
            elif similarity < 0.3:
                # Complete shift (not hijacking, just ignoring)
                hijackings.append({
                    'topic_id': topic['topic_id'],
                    'topic_proposer': topic_proposer,
                    'hijacked_by': responder,
                    'original_text': topic_text[:200],
                    'response_text': response_text[:200],
                    'similarity': similarity,
                    'type': 'shift',
                    'preserves_legitimacy': False
                })
            elif similarity >= 0.6:
                # Alignment: maintains topic frame
                hijackings.append({
                    'topic_id': topic['topic_id'],
                    'topic_proposer': topic_proposer,
                    'hijacked_by': responder,
                    'original_text': topic_text[:200],
                    'response_text': response_text[:200],
                    'similarity': similarity,
                    'type': 'alignment',
                    'preserves_legitimacy': True
                })
    
    return hijackings

def analyze_topic_engagement_and_power(topics, speaker_orientations, speaker_times, total_time):
    """Analyze which topics attracted most attention and reveal power dynamics."""
    report_lines = []
    report_lines.append("=" * 100)
    report_lines.append("TOPIC ENGAGEMENT ANALYSIS: TOPICS DISCUSSED AND POWER DYNAMICS")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    # Calculate engagement metrics for each topic
    topic_engagement = []
    for topic in topics:
        engagement_score = 0
        response_count = 0
        responder_list = []
        total_response_duration = 0
        avg_similarity = 0
        similarities = []
        
        # Count all responses (including non-uptake)
        all_responses = topic.get('stabilization', {}).get('all_responses', [])
        uptake_responses = topic.get('stabilization', {}).get('responders', [])
        
        for response in all_responses:
            response_count += 1
            responder_list.append(response['speaker'])
            total_response_duration += response.get('response_duration', 0)
            similarities.append(response.get('similarity', 0))
        
        if similarities:
            avg_similarity = sum(similarities) / len(similarities)
        
        # Engagement score: weighted combination
        # Higher weight for uptake responses, response count, and duration
        engagement_score = (
            len(uptake_responses) * 10 +  # Uptake responses weighted heavily
            len(all_responses) * 2 +       # All responses count
            total_response_duration / 10 + # Duration contribution
            avg_similarity * 5            # Average similarity
        )
        
        topic_engagement.append({
            'topic': topic,
            'engagement_score': engagement_score,
            'response_count': response_count,
            'uptake_count': len(uptake_responses),
            'responders': responder_list,
            'unique_responders': len(set(responder_list)),
            'total_response_duration': total_response_duration,
            'avg_similarity': avg_similarity,
            'status': topic['status']
        })
    
    # Sort by engagement score
    topic_engagement.sort(key=lambda x: x['engagement_score'], reverse=True)
    
    # Section 1: Most Discussed Topics (Top 20)
    report_lines.append("=" * 100)
    report_lines.append("SECTION 1: MOST DISCUSSED TOPICS (Ranked by Engagement)")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    for idx, te in enumerate(topic_engagement[:20], 1):
        topic = te['topic']
        report_lines.append(f"RANK #{idx}: {topic['topic_id']}")
        report_lines.append("-" * 100)
        report_lines.append(f"Proposer: {topic['proposer']}")
        report_lines.append(f"Status: {topic['status']}")
        report_lines.append(f"Engagement Score: {te['engagement_score']:.2f}")
        report_lines.append(f"Total Responses: {te['response_count']}")
        report_lines.append(f"Uptake Responses: {te['uptake_count']}")
        report_lines.append(f"Unique Responders: {te['unique_responders']}")
        report_lines.append(f"Total Response Duration: {te['total_response_duration']:.2f}s")
        report_lines.append(f"Average Semantic Similarity: {te['avg_similarity']:.3f}")
        report_lines.append("")
        report_lines.append(f"TOPIC CONTENT:")
        report_lines.append(f"{topic.get('text', topic.get('text_sample', 'N/A'))[:500]}")
        report_lines.append("")
        
        if te['responders']:
            report_lines.append("RESPONDERS:")
            responder_counts = Counter(te['responders'])
            for responder, count in responder_counts.most_common():
                report_lines.append(f"  - {responder}: {count} response(s)")
        else:
            report_lines.append("RESPONDERS: None")
        
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append("")
    
    # Section 2: Topics by Status
    report_lines.append("=" * 100)
    report_lines.append("SECTION 2: TOPICS BY STATUS")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    stabilized_topics = [te for te in topic_engagement if te['status'] == 'stabilized']
    failed_uptake = [te for te in topic_engagement if te['status'] == 'failed_no_uptake']
    failed_silence = [te for te in topic_engagement if te['status'] == 'failed_silence']
    
    report_lines.append(f"STABILIZED TOPICS (Successful Agenda Setting): {len(stabilized_topics)}")
    report_lines.append("-" * 100)
    for te in stabilized_topics:
        topic = te['topic']
        report_lines.append(f"  {topic['topic_id']} - {topic['proposer']}")
        report_lines.append(f"    Content: {topic.get('text', topic.get('text_sample', ''))[:150]}...")
        report_lines.append(f"    Responders: {', '.join(set(te['responders']))}")
        report_lines.append(f"    Engagement Score: {te['engagement_score']:.2f}")
        report_lines.append("")
    
    report_lines.append(f"FAILED TOPICS (No Uptake): {len(failed_uptake)}")
    report_lines.append("-" * 100)
    report_lines.append(f"Top 10 Failed Topics by Engagement:")
    for te in failed_uptake[:10]:
        topic = te['topic']
        report_lines.append(f"  {topic['topic_id']} - {topic['proposer']}")
        report_lines.append(f"    Content: {topic.get('text', topic.get('text_sample', ''))[:150]}...")
        report_lines.append(f"    Responses: {te['response_count']} (but no uptake)")
        report_lines.append(f"    Responders: {', '.join(set(te['responders'])) if te['responders'] else 'None'}")
        report_lines.append("")
    
    report_lines.append(f"FAILED TOPICS (Silence): {len(failed_silence)}")
    report_lines.append("-" * 100)
    for te in failed_silence:
        topic = te['topic']
        report_lines.append(f"  {topic['topic_id']} - {topic['proposer']}")
        report_lines.append(f"    Content: {topic.get('text', topic.get('text_sample', ''))[:150]}...")
        report_lines.append("")
    
    # Section 3: Speaker Engagement Patterns
    report_lines.append("=" * 100)
    report_lines.append("SECTION 3: SPEAKER ENGAGEMENT PATTERNS")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    # Who responds to topics most
    all_responders = []
    for te in topic_engagement:
        all_responders.extend(te['responders'])
    
    responder_counts = Counter(all_responders)
    report_lines.append("MOST ACTIVE RESPONDERS (Who engages with topics most):")
    report_lines.append("-" * 100)
    for speaker, count in responder_counts.most_common(15):
        report_lines.append(f"  {speaker}: {count} responses to topics")
    report_lines.append("")
    
    # Who proposes topics that attract responses
    proposer_engagement = defaultdict(list)
    for te in topic_engagement:
        proposer = te['topic']['proposer']
        proposer_engagement[proposer].append(te['engagement_score'])
    
    report_lines.append("TOPIC PROPOSERS RANKED BY AVERAGE ENGAGEMENT SCORE:")
    report_lines.append("-" * 100)
    proposer_avg_engagement = {
        proposer: sum(scores) / len(scores) if scores else 0
        for proposer, scores in proposer_engagement.items()
    }
    for proposer, avg_score in sorted(proposer_avg_engagement.items(), 
                                     key=lambda x: x[1], reverse=True)[:15]:
        topic_count = len(proposer_engagement[proposer])
        stabilized_count = len([te for te in topic_engagement 
                               if te['topic']['proposer'] == proposer and 
                               te['status'] == 'stabilized'])
        report_lines.append(f"  {proposer}:")
        report_lines.append(f"    Topics Proposed: {topic_count}")
        report_lines.append(f"    Average Engagement Score: {avg_score:.2f}")
        report_lines.append(f"    Stabilized Topics: {stabilized_count}")
        report_lines.append("")
    
    # Section 4: Power Dynamics Analysis
    report_lines.append("=" * 100)
    report_lines.append("SECTION 4: POWER DYNAMICS REVEALED THROUGH TOPIC ENGAGEMENT")
    report_lines.append("=" * 100)
    report_lines.append("")
    
    # Power indicator 1: Agenda Setting Capacity
    report_lines.append("4.1 AGENDA SETTING CAPACITY (Whose Topics Attract Attention)")
    report_lines.append("-" * 100)
    report_lines.append("")
    report_lines.append("High Engagement Topics (Top 10):")
    for idx, te in enumerate(topic_engagement[:10], 1):
        topic = te['topic']
        report_lines.append(f"  {idx}. {topic['topic_id']} by {topic['proposer']}")
        report_lines.append(f"     Engagement: {te['engagement_score']:.2f}, Responses: {te['response_count']}, "
                          f"Uptake: {te['uptake_count']}")
        report_lines.append(f"     Content: {topic.get('text', topic.get('text_sample', ''))[:100]}...")
        report_lines.append("")
    
    # Power indicator 2: Response Attraction
    report_lines.append("4.2 RESPONSE ATTRACTION (Who Attracts Responses)")
    report_lines.append("-" * 100)
    report_lines.append("")
    report_lines.append("Speakers whose topics receive most responses:")
    proposer_response_counts = defaultdict(int)
    for te in topic_engagement:
        proposer_response_counts[te['topic']['proposer']] += te['response_count']
    
    for proposer, count in sorted(proposer_response_counts.items(), 
                                  key=lambda x: x[1], reverse=True)[:10]:
        topic_count = len([t for t in topics if t['proposer'] == proposer])
        avg_responses = count / topic_count if topic_count > 0 else 0
        report_lines.append(f"  {proposer}: {count} total responses across {topic_count} topics "
                          f"(avg: {avg_responses:.1f} per topic)")
    report_lines.append("")
    
    # Power indicator 3: Uptake Success
    report_lines.append("4.3 UPTAKE SUCCESS (Whose Topics Achieve Semantic Uptake)")
    report_lines.append("-" * 100)
    report_lines.append("")
    proposer_uptake = defaultdict(int)
    for te in topic_engagement:
        if te['uptake_count'] > 0:
            proposer_uptake[te['topic']['proposer']] += te['uptake_count']
    
    for proposer, uptake_count in sorted(proposer_uptake.items(), 
                                        key=lambda x: x[1], reverse=True):
        topic_count = len([t for t in topics if t['proposer'] == proposer])
        stabilized = len([t for t in topics if t['proposer'] == proposer and t['status'] == 'stabilized'])
        report_lines.append(f"  {proposer}: {uptake_count} uptake responses, "
                          f"{stabilized} stabilized topics out of {topic_count} proposed")
    report_lines.append("")
    
    # Power indicator 4: Speaking Time vs. Topic Engagement
    report_lines.append("4.4 SPEAKING TIME vs. TOPIC ENGAGEMENT (Power Decoupling)")
    report_lines.append("-" * 100)
    report_lines.append("")
    report_lines.append("High Speaking Time Speakers:")
    top_speakers_by_time = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:10]
    for speaker, time in top_speakers_by_time:
        topic_count = len([t for t in topics if t['proposer'] == speaker])
        stabilized = len([t for t in topics if t['proposer'] == speaker and t['status'] == 'stabilized'])
        avg_engagement = proposer_avg_engagement.get(speaker, 0)
        report_lines.append(f"  {speaker}:")
        report_lines.append(f"    Speaking Time: {time:.1f}s ({time/total_time*100:.1f}%)")
        report_lines.append(f"    Topics Proposed: {topic_count}")
        stabilization_rate = (stabilized/topic_count*100) if topic_count > 0 else 0.0
        report_lines.append(f"    Stabilized: {stabilized} ({stabilization_rate:.1f}%)")
        report_lines.append(f"    Avg Engagement Score: {avg_engagement:.2f}")
        report_lines.append("")
    
    # Power indicator 5: Topic Themes That Succeed
    report_lines.append("4.5 TOPIC THEMES THAT ATTRACT ATTENTION")
    report_lines.append("-" * 100)
    report_lines.append("")
    report_lines.append("Successful Topics (Stabilized):")
    for te in stabilized_topics:
        topic = te['topic']
        report_lines.append(f"  {topic['topic_id']}: {topic.get('text', topic.get('text_sample', ''))[:200]}")
        report_lines.append(f"    Proposer: {topic['proposer']}, Responders: {', '.join(set(te['responders']))}")
        report_lines.append("")
    
    report_lines.append("High Engagement Failed Topics (Attracted Responses but No Uptake):")
    high_engagement_failed = [te for te in failed_uptake if te['response_count'] > 0]
    high_engagement_failed.sort(key=lambda x: x['engagement_score'], reverse=True)
    for te in high_engagement_failed[:10]:
        topic = te['topic']
        report_lines.append(f"  {topic['topic_id']}: {topic.get('text', topic.get('text_sample', ''))[:200]}")
        report_lines.append(f"    Proposer: {topic['proposer']}, Responses: {te['response_count']}, "
                          f"Responders: {', '.join(set(te['responders']))}")
        report_lines.append("")
    
    # Write report
    with open('topic_engagement_power_analysis.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("  - topic_engagement_power_analysis.txt exported")
    
    return topic_engagement

def create_fine_grained_topic_power_report(topic_closures, accountability_patterns, 
                                           recycled_topics, topic_hijackings, topics, speaker_times):
    """Create comprehensive report on fine-grained topic-speaker relations revealing power."""
    report_lines = []
    report_lines.append("=" * 100)
    report_lines.append("FINE-GRAINED TOPIC-SPEAKER RELATIONS: POWER AS INTERACTIONAL STRUCTURE")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("This analysis examines power as an interactional structure rather than semantic property,")
    report_lines.append("focusing on four key phenomena:")
    report_lines.append("1. Topic Closure Authority")
    report_lines.append("2. Asymmetric Topical Accountability")
    report_lines.append("3. Topic Recycling")
    report_lines.append("4. Topic Hijacking vs Alignment")
    report_lines.append("")
    
    # Section 1: Topic Closure Authority
    report_lines.append("=" * 100)
    report_lines.append("SECTION 1: TOPIC CLOSURE AUTHORITY")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("Power is visible in who can end topics without contest.")
    report_lines.append("When a speaker shifts away from ongoing theme and others follow without repair,")
    report_lines.append("this indicates capacity to delimit relevance.")
    report_lines.append("")
    
    uncontested_closures = [c for c in topic_closures if c['uncontested']]
    report_lines.append(f"Total Topic Closures Detected: {len(topic_closures)}")
    report_lines.append(f"Uncontested Closures (Others Followed): {len(uncontested_closures)}")
    report_lines.append("")
    
    # Who closes topics most successfully
    closure_by_speaker = defaultdict(lambda: {'total': 0, 'uncontested': 0})
    for closure in topic_closures:
        closer = closure['shifted_by']
        closure_by_speaker[closer]['total'] += 1
        if closure['uncontested']:
            closure_by_speaker[closer]['uncontested'] += 1
    
    report_lines.append("Topic Closure Authority (Who Can End Topics Without Contest):")
    report_lines.append("-" * 100)
    for speaker, data in sorted(closure_by_speaker.items(), 
                               key=lambda x: x[1]['uncontested'], reverse=True):
        success_rate = (data['uncontested'] / data['total'] * 100) if data['total'] > 0 else 0
        report_lines.append(f"  {speaker}:")
        report_lines.append(f"    Total Closures: {data['total']}")
        report_lines.append(f"    Uncontested: {data['uncontested']} ({success_rate:.1f}%)")
        report_lines.append("")
    
    report_lines.append("Top 10 Uncontested Closures:")
    report_lines.append("-" * 100)
    for closure in sorted(uncontested_closures, 
                         key=lambda x: x['followers_count'], reverse=True)[:10]:
        topic = next((t for t in topics if t['topic_id'] == closure['closed_topic']), None)
        if topic:
            report_lines.append(f"  Topic: {closure['closed_topic']} (proposed by {closure['closed_by']})")
            report_lines.append(f"    Closed by: {closure['shifted_by']}")
            report_lines.append(f"    Followers: {closure['followers_count']}")
            report_lines.append(f"    Topic Content: {topic.get('text', topic.get('text_sample', ''))[:150]}...")
            report_lines.append(f"    Closure Delay: {closure['closure_delay']:.1f}s")
            report_lines.append("")
    
    # Section 2: Asymmetric Topical Accountability
    report_lines.append("=" * 100)
    report_lines.append("SECTION 2: ASYMMETRIC TOPICAL ACCOUNTABILITY")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("Uneven demand for clarification/justification signals differential epistemic standing.")
    report_lines.append("Some speakers are routinely asked to clarify, justify, or provide evidence,")
    report_lines.append("while others are not.")
    report_lines.append("")
    
    report_lines.append("Accountability Patterns by Speaker:")
    report_lines.append("-" * 100)
    for speaker, data in sorted(accountability_patterns.items(),
                               key=lambda x: x[1]['accountability_rate'], reverse=True):
        topic_count = len(data['topics_proposed'])
        if topic_count == 0:
            continue
        
        report_lines.append(f"  {speaker}:")
        report_lines.append(f"    Topics Proposed: {topic_count}")
        report_lines.append(f"    Clarification Requests: {data['clarification_requests']}")
        report_lines.append(f"    Justification Requests: {data['justification_requests']}")
        report_lines.append(f"    Evidence Requests: {data['evidence_requests']}")
        report_lines.append(f"    Total Accountability Demands: {data['total_accountability_demands']}")
        report_lines.append(f"    Accountability Rate: {data['accountability_rate']:.2f} per topic")
        report_lines.append("")
    
    # High vs Low accountability
    high_accountability = [s for s, d in accountability_patterns.items() 
                          if d['accountability_rate'] > 0.5]
    low_accountability = [s for s, d in accountability_patterns.items() 
                         if d['accountability_rate'] == 0 and len(d['topics_proposed']) > 0]
    
    report_lines.append("High Accountability Speakers (Routinely Asked to Clarify/Justify):")
    report_lines.append("-" * 100)
    for speaker in high_accountability:
        data = accountability_patterns[speaker]
        report_lines.append(f"  {speaker}: {data['accountability_rate']:.2f} demands per topic")
    report_lines.append("")
    
    report_lines.append("Low Accountability Speakers (Never Asked to Clarify/Justify):")
    report_lines.append("-" * 100)
    for speaker in low_accountability:
        data = accountability_patterns[speaker]
        report_lines.append(f"  {speaker}: {len(data['topics_proposed'])} topics, 0 accountability demands")
    report_lines.append("")
    
    # Section 3: Topic Recycling
    report_lines.append("=" * 100)
    report_lines.append("SECTION 3: TOPIC RECYCLING")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("Power appears when topics initially ignored gain traction after reintroduction")
    report_lines.append("by different speaker. Authority is relational rather than propositional.")
    report_lines.append("")
    
    report_lines.append(f"Total Topic Recycling Cases Detected: {len(recycled_topics)}")
    report_lines.append("")
    
    if recycled_topics:
        report_lines.append("Topic Recycling Cases:")
        report_lines.append("-" * 100)
        for recycle in recycled_topics:
            original_topic = next((t for t in topics if t['topic_id'] == recycle['original_topic']), None)
            recycled_topic = next((t for t in topics if t['topic_id'] == recycle['recycled_topic']), None)
            
            if original_topic and recycled_topic:
                report_lines.append(f"  Original Topic: {recycle['original_topic']}")
                report_lines.append(f"    Proposer: {recycle['original_proposer']}")
                report_lines.append(f"    Status: {recycle['original_status']}")
                report_lines.append(f"    Content: {original_topic.get('text', original_topic.get('text_sample', ''))[:150]}...")
                report_lines.append("")
                report_lines.append(f"  Recycled Topic: {recycle['recycled_topic']}")
                report_lines.append(f"    Proposer: {recycle['recycled_proposer']}")
                report_lines.append(f"    Status: {recycle['recycled_status']}")
                report_lines.append(f"    Content: {recycled_topic.get('text', recycled_topic.get('text_sample', ''))[:150]}...")
                report_lines.append(f"    Similarity: {recycle['similarity']:.3f}")
                report_lines.append(f"    Time Gap: {recycle['time_gap']:.1f}s")
                if 'response_increase' in recycle:
                    report_lines.append(f"    Response Increase: +{recycle['response_increase']}")
                report_lines.append("")
        
        # Who benefits from recycling
        recycler_benefits = defaultdict(int)
        for recycle in recycled_topics:
            recycler_benefits[recycle['recycled_proposer']] += 1
        
        report_lines.append("Speakers Who Benefit from Topic Recycling:")
        report_lines.append("-" * 100)
        for speaker, count in sorted(recycler_benefits.items(), key=lambda x: x[1], reverse=True):
            report_lines.append(f"  {speaker}: {count} topics gained traction when recycled")
        report_lines.append("")
    
    # Section 4: Topic Hijacking vs Alignment
    report_lines.append("=" * 100)
    report_lines.append("SECTION 4: TOPIC HIJACKING vs ALIGNMENT")
    report_lines.append("=" * 100)
    report_lines.append("")
    report_lines.append("Reframing topics while preserving legitimacy exercises subtle control over meaning.")
    report_lines.append("Aligns with Goffman's footing shifts - repositioning within interaction.")
    report_lines.append("")
    
    hijackings_by_type = defaultdict(list)
    for hijack in topic_hijackings:
        hijackings_by_type[hijack['type']].append(hijack)
    
    report_lines.append(f"Total Topic Responses Analyzed: {len(topic_hijackings)}")
    report_lines.append(f"  Hijacking/Reframing (0.3-0.6 similarity): {len(hijackings_by_type['hijacking']) + len(hijackings_by_type['reframing'])}")
    report_lines.append(f"  Complete Shift (<0.3 similarity): {len(hijackings_by_type['shift'])}")
    report_lines.append(f"  Alignment (>0.6 similarity): {len(hijackings_by_type['alignment'])}")
    report_lines.append("")
    
    # Who hijacks most
    hijacker_counts = defaultdict(lambda: {'hijacking': 0, 'reframing': 0, 'shift': 0, 'alignment': 0})
    for hijack in topic_hijackings:
        hijacker = hijack['hijacked_by']
        hijacker_counts[hijacker][hijack['type']] += 1
    
    report_lines.append("Topic Control Patterns by Speaker:")
    report_lines.append("-" * 100)
    for speaker, counts in sorted(hijacker_counts.items(),
                                  key=lambda x: x[1]['hijacking'] + x[1]['reframing'], reverse=True):
        total = sum(counts.values())
        if total > 0:
            report_lines.append(f"  {speaker}:")
            report_lines.append(f"    Hijacking/Reframing: {counts['hijacking'] + counts['reframing']}")
            report_lines.append(f"    Complete Shifts: {counts['shift']}")
            report_lines.append(f"    Alignment: {counts['alignment']}")
            report_lines.append(f"    Total Responses: {total}")
            report_lines.append("")
    
    # Examples
    report_lines.append("Examples of Topic Hijacking/Reframing:")
    report_lines.append("-" * 100)
    hijacking_examples = [h for h in topic_hijackings if h['type'] in ['hijacking', 'reframing']]
    for hijack in hijacking_examples[:10]:
        report_lines.append(f"  Topic: {hijack['topic_id']} (proposed by {hijack['topic_proposer']})")
        report_lines.append(f"    Hijacked/Reframed by: {hijack['hijacked_by']}")
        report_lines.append(f"    Type: {hijack['type']}")
        report_lines.append(f"    Similarity: {hijack['similarity']:.3f}")
        report_lines.append(f"    Original: {hijack['original_text'][:100]}...")
        report_lines.append(f"    Response: {hijack['response_text'][:100]}...")
        report_lines.append("")
    
    # Write report
    with open('fine_grained_topic_power_analysis.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print("  - fine_grained_topic_power_analysis.txt exported")

def create_speaker_topic_engagement_matrix(topics, speaker_orientations, speaker_times):
    """Create heatmap showing how each speaker engages with each topic."""
    speakers = sorted(speaker_times.keys())
    topic_ids = [t['topic_id'] for t in topics]
    
    # Create engagement matrix
    # Values: 2 = proposed, 1 = responded with uptake, 0.5 = responded without uptake, 0 = no engagement
    engagement_matrix = np.zeros((len(speakers), len(topic_ids)))
    
    for i, speaker in enumerate(speakers):
        orientation = speaker_orientations.get(speaker, {})
        
        for j, topic_id in enumerate(topic_ids):
            topic = next((t for t in topics if t['topic_id'] == topic_id), None)
            if not topic:
                continue
            
            # Check if proposed
            if topic_id in orientation.get('topics_proposed', []):
                engagement_matrix[i, j] = 2.0
            # Check if responded with uptake
            elif topic_id in orientation.get('topics_responded_to', []):
                engagement_matrix[i, j] = 1.0
            # Check if responded without uptake
            elif topic.get('stabilization', {}).get('all_responses'):
                for response in topic['stabilization']['all_responses']:
                    if response['speaker'] == speaker and not response.get('uptake', True):
                        engagement_matrix[i, j] = 0.5
                        break
    
    # Create heatmap
    plt.figure(figsize=(max(20, len(topic_ids) * 0.3), max(10, len(speakers) * 0.4)))
    sns.heatmap(engagement_matrix, 
                xticklabels=[f"{tid}\n({topics[i]['proposer']})" for i, tid in enumerate(topic_ids)],
                yticklabels=speakers,
                cmap='RdYlGn',
                cbar_kws={'label': 'Engagement Level'},
                annot=False,
                fmt='.1f')
    plt.title('Speaker-Topic Engagement Matrix\n(2.0=Proposed, 1.0=Responded with Uptake, 0.5=Responded without Uptake, 0.0=No Engagement)', 
              fontsize=12, pad=15)
    plt.xlabel('Topics', fontsize=10)
    plt.ylabel('Speakers', fontsize=10)
    plt.xticks(rotation=90, ha='right', fontsize=7)
    plt.yticks(rotation=0, fontsize=8)
    plt.tight_layout()
    plt.savefig('speaker_topic_engagement_matrix.png', dpi=300, bbox_inches='tight')
    plt.close()

def identify_agenda_control(segments, turns, silence_threshold=2.0):
    """Identify speakers who introduce new topics after silence."""
    agenda_introductions = []
    
    for i, turn in enumerate(turns):
        if i == 0:
            # First turn is always an introduction
            agenda_introductions.append({
                'speaker': turn['speaker'],
                'time': turn['start'],
                'preceding_silence': turn['start']
            })
        else:
            prev_turn = turns[i - 1]
            silence = turn['start'] - prev_turn['end']
            
            if silence >= silence_threshold:
                agenda_introductions.append({
                    'speaker': turn['speaker'],
                    'time': turn['start'],
                    'preceding_silence': silence
                })
    
    return agenda_introductions

def create_network_graph(speaker_times, transitions):
    """Create network visualization of speaker interactions."""
    G = nx.DiGraph()
    
    # Add nodes with speaking time as attribute
    for speaker, time in speaker_times.items():
        G.add_node(speaker, speaking_time=time)
    
    # Add edges with transition frequency
    for (source, target), count in transitions.items():
        if source in speaker_times and target in speaker_times:
            G.add_edge(source, target, weight=count)
    
    # Calculate node sizes (normalized)
    max_time = max(speaker_times.values()) if speaker_times else 1
    node_sizes = [speaker_times.get(node, 0) / max_time * 3000 for node in G.nodes()]
    
    # Calculate edge widths (normalized)
    max_weight = max([d['weight'] for u, v, d in G.edges(data=True)]) if G.edges() else 1
    edge_widths = [d['weight'] / max_weight * 5 for u, v, d in G.edges(data=True)]
    
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                           node_color='lightblue', alpha=0.7, edgecolors='black')
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.5, 
                           edge_color='gray', arrows=True, arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    plt.title('Speaker Interaction Network\n(Node size = Speaking time, Edge thickness = Transition frequency)',
              fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('speaker_network.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_timeline_chart(speaker_times, total_time):
    """Create timeline/bar chart of speaking time distribution."""
    speakers = list(speaker_times.keys())
    times = list(speaker_times.values())
    percentages = [t / total_time * 100 for t in times]
    
    # Sort by speaking time
    sorted_data = sorted(zip(speakers, times, percentages), key=lambda x: x[1], reverse=True)
    speakers, times, percentages = zip(*sorted_data)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Bar chart
    bars = ax1.barh(range(len(speakers)), times, color='steelblue', alpha=0.7)
    ax1.set_yticks(range(len(speakers)))
    ax1.set_yticklabels(speakers)
    ax1.set_xlabel('Total Speaking Time (seconds)', fontsize=12)
    ax1.set_title('Speaking Time Distribution by Speaker', fontsize=14, pad=15)
    ax1.grid(axis='x', alpha=0.3)
    
    # Add percentage labels
    for i, (time, pct) in enumerate(zip(times, percentages)):
        ax1.text(time, i, f' {pct:.1f}%', va='center', fontsize=9)
    
    # Pie chart
    ax2.pie(percentages, labels=speakers, autopct='%1.1f%%', startangle=90)
    ax2.set_title('Speaking Time Percentage Distribution', fontsize=14, pad=15)
    
    plt.tight_layout()
    plt.savefig('speaking_time_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_transition_heatmap(transitions, speakers):
    """Create heatmap of speaker-to-speaker transitions."""
    # Create matrix
    transition_matrix = np.zeros((len(speakers), len(speakers)))
    speaker_to_idx = {speaker: i for i, speaker in enumerate(speakers)}
    
    for (source, target), count in transitions.items():
        if source in speaker_to_idx and target in speaker_to_idx:
            i = speaker_to_idx[source]
            j = speaker_to_idx[target]
            transition_matrix[i, j] = count
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(transition_matrix, 
                xticklabels=speakers, 
                yticklabels=speakers,
                annot=True, 
                fmt='.0f',
                cmap='YlOrRd',
                cbar_kws={'label': 'Transition Frequency'})
    plt.title('Speaker-to-Speaker Transition Heatmap', fontsize=14, pad=15)
    plt.xlabel('Target Speaker', fontsize=12)
    plt.ylabel('Source Speaker', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig('transition_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_timeline_visualization(segments, speaker_times):
    """Create timeline showing speaking activity over the course of the meeting."""
    # Get top speakers for clarity
    top_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:10]
    top_speaker_set = set([s[0] for s in top_speakers])
    
    # Create timeline data
    timeline_data = []
    for seg in segments:
        speaker = get_speaker(seg)
        if speaker in top_speaker_set and not is_filler(seg['text']):
            timeline_data.append({
                'speaker': speaker,
                'start': seg['start'],
                'end': seg['end'],
                'duration': seg['end'] - seg['start']
            })
    
    if not timeline_data:
        return
    
    df = pd.DataFrame(timeline_data)
    
    # Create color map
    unique_speakers = df['speaker'].unique()
    colors = plt.cm.tab20(np.linspace(0, 1, len(unique_speakers)))
    color_map = dict(zip(unique_speakers, colors))
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    y_pos = 0
    y_positions = {}
    for speaker in unique_speakers:
        y_positions[speaker] = y_pos
        y_pos += 1
    
    for _, row in df.iterrows():
        speaker = row['speaker']
        start = row['start']
        end = row['end']
        y = y_positions[speaker]
        
        ax.barh(y, end - start, left=start, height=0.8, 
               color=color_map[speaker], alpha=0.7, edgecolor='black', linewidth=0.5)
    
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(y_positions.keys()))
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_title('Speaking Activity Timeline (Top 10 Speakers)', fontsize=14, pad=15)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('speaking_timeline.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_cumulative_speaking_time(segments, speaker_times, total_time):
    """Create cumulative speaking time over the course of the meeting."""
    top_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:8]
    top_speaker_set = set([s[0] for s in top_speakers])
    
    # Create time bins
    time_bins = np.linspace(0, total_time, 100)
    cumulative_data = {speaker: np.zeros(len(time_bins)) for speaker, _ in top_speakers}
    
    for seg in segments:
        speaker = get_speaker(seg)
        if speaker in top_speaker_set and not is_filler(seg['text']):
            duration = seg['end'] - seg['start']
            # Add to all bins after this segment starts
            start_idx = np.searchsorted(time_bins, seg['start'])
            cumulative_data[speaker][start_idx:] += duration
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    for speaker, _ in top_speakers:
        ax.plot(time_bins, cumulative_data[speaker], label=speaker, linewidth=2, alpha=0.8)
    
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_ylabel('Cumulative Speaking Time (seconds)', fontsize=12)
    ax.set_title('Cumulative Speaking Time Over Meeting Duration', fontsize=14, pad=15)
    ax.legend(loc='upper left', fontsize=9, ncol=2)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('cumulative_speaking_time.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_turn_length_distribution(turn_stats):
    """Create histogram of turn length distribution."""
    all_turn_lengths = []
    speaker_labels = []
    
    for speaker, stats in turn_stats.items():
        all_turn_lengths.extend(stats['durations'])
        speaker_labels.extend([speaker] * len(stats['durations']))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Overall distribution
    ax1.hist(all_turn_lengths, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Turn Length (seconds)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Distribution of Turn Lengths (All Speakers)', fontsize=14, pad=15)
    ax1.axvline(np.median(all_turn_lengths), color='red', linestyle='--', 
                label=f'Median: {np.median(all_turn_lengths):.2f}s')
    ax1.axvline(np.mean(all_turn_lengths), color='green', linestyle='--', 
                label=f'Mean: {np.mean(all_turn_lengths):.2f}s')
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Box plot by speaker (top speakers)
    top_speakers = sorted(turn_stats.items(), 
                         key=lambda x: x[1]['total_duration'], reverse=True)[:10]
    data_for_box = [stats['durations'] for _, stats in top_speakers]
    labels_for_box = [speaker for speaker, _ in top_speakers]
    
    ax2.boxplot(data_for_box, labels=labels_for_box, vert=True)
    ax2.set_ylabel('Turn Length (seconds)', fontsize=12)
    ax2.set_xlabel('Speaker', fontsize=12)
    ax2.set_title('Turn Length Distribution by Speaker (Top 10)', fontsize=14, pad=15)
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('turn_length_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_interruption_network(interruptions, speaker_times):
    """Create network graph specifically for interruption patterns."""
    G = nx.DiGraph()
    
    # Add nodes
    for speaker in speaker_times.keys():
        G.add_node(speaker)
    
    # Add interruption edges
    interruption_counts = defaultdict(int)
    for inter in interruptions:
        source = inter['interrupter']
        target = inter['interrupted']
        interruption_counts[(source, target)] += 1
    
    for (source, target), count in interruption_counts.items():
        if source in speaker_times and target in speaker_times:
            G.add_edge(source, target, weight=count)
    
    if not G.edges():
        return
    
    # Node sizes based on interruption activity
    interrupt_out = defaultdict(int)
    interrupt_in = defaultdict(int)
    for inter in interruptions:
        interrupt_out[inter['interrupter']] += 1
        interrupt_in[inter['interrupted']] += 1
    
    node_sizes = []
    for node in G.nodes():
        activity = interrupt_out[node] + interrupt_in[node]
        node_sizes.append(max(activity * 50, 300))
    
    # Edge widths
    max_weight = max([d['weight'] for u, v, d in G.edges(data=True)]) if G.edges() else 1
    edge_widths = [d['weight'] / max_weight * 8 for u, v, d in G.edges(data=True)]
    
    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                           node_color='lightcoral', alpha=0.7, edgecolors='black')
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6, 
                           edge_color='darkred', arrows=True, arrowsize=25)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    plt.title('Interruption Network\n(Node size = Interruption activity, Edge = Interruption direction)', 
              fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('interruption_network.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_gap_analysis(segments):
    """Analyze gaps (silence) between speaker transitions."""
    gaps = []
    gap_types = []
    
    for i in range(len(segments) - 1):
        current = segments[i]
        next_seg = segments[i + 1]
        current_speaker = get_speaker(current)
        next_speaker = get_speaker(next_seg)
        
        gap = next_seg['start'] - current['end']
        gaps.append(gap)
        
        if current_speaker == next_speaker:
            gap_types.append('Same Speaker')
        else:
            gap_types.append('Speaker Change')
    
    gaps = np.array(gaps)
    gaps = gaps[gaps >= 0]  # Remove negative gaps (overlaps)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Histogram of gaps
    ax1.hist(gaps, bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Gap Duration (seconds)', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('Distribution of Gaps Between Utterances', fontsize=14, pad=15)
    ax1.axvline(np.median(gaps), color='red', linestyle='--', 
                label=f'Median: {np.median(gaps):.2f}s')
    ax1.set_xlim(0, min(10, np.percentile(gaps, 95)))  # Focus on most common gaps
    ax1.legend()
    ax1.grid(alpha=0.3)
    
    # Box plot by gap type
    same_speaker_gaps = [gaps[i] for i in range(len(gaps)) if i < len(gap_types) and gap_types[i] == 'Same Speaker']
    speaker_change_gaps = [gaps[i] for i in range(len(gaps)) if i < len(gap_types) and gap_types[i] == 'Speaker Change']
    
    ax2.boxplot([same_speaker_gaps, speaker_change_gaps], 
                labels=['Same Speaker', 'Speaker Change'], vert=True)
    ax2.set_ylabel('Gap Duration (seconds)', fontsize=12)
    ax2.set_title('Gap Duration by Transition Type', fontsize=14, pad=15)
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('gap_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return {
        'median_gap': np.median(gaps),
        'mean_gap': np.mean(gaps),
        'same_speaker_median': np.median(same_speaker_gaps) if same_speaker_gaps else 0,
        'speaker_change_median': np.median(speaker_change_gaps) if speaker_change_gaps else 0
    }

def create_participation_heatmap(segments, speaker_times, total_time, n_segments=20):
    """Create heatmap showing speaker participation across time segments."""
    # Get top speakers
    top_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:15]
    top_speaker_set = set([s[0] for s in top_speakers])
    
    # Create time segments
    segment_duration = total_time / n_segments
    time_segments = [(i * segment_duration, (i + 1) * segment_duration) 
                     for i in range(n_segments)]
    
    # Calculate speaking time per segment per speaker
    heatmap_data = []
    speaker_list = [s[0] for s in top_speakers]
    
    for speaker in speaker_list:
        row = []
        for seg_start, seg_end in time_segments:
            time_in_segment = 0
            for seg in segments:
                if get_speaker(seg) == speaker and not is_filler(seg['text']):
                    overlap_start = max(seg['start'], seg_start)
                    overlap_end = min(seg['end'], seg_end)
                    if overlap_start < overlap_end:
                        time_in_segment += overlap_end - overlap_start
            row.append(time_in_segment)
        heatmap_data.append(row)
    
    heatmap_array = np.array(heatmap_data)
    
    plt.figure(figsize=(16, 10))
    sns.heatmap(heatmap_array, 
                xticklabels=[f'{i+1}' for i in range(n_segments)],
                yticklabels=speaker_list,
                cmap='YlOrRd',
                cbar_kws={'label': 'Speaking Time (seconds)'},
                fmt='.1f')
    plt.xlabel('Time Segment', fontsize=12)
    plt.ylabel('Speaker', fontsize=12)
    plt.title(f'Speaker Participation Across Meeting (Divided into {n_segments} Segments)', 
              fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig('participation_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def calculate_inequality_metrics(speaker_times):
    """Calculate Gini coefficient and other inequality metrics."""
    times = list(speaker_times.values())
    times = sorted(times, reverse=True)
    n = len(times)
    
    if n == 0 or sum(times) == 0:
        return {}
    
    # Gini coefficient
    cumsum = np.cumsum(times)
    gini = (2 * np.sum((np.arange(1, n + 1)) * times)) / (n * np.sum(times)) - (n + 1) / n
    
    # Top 10% share
    top_10_pct_count = max(1, int(n * 0.1))
    top_10_share = sum(times[:top_10_pct_count]) / sum(times) * 100
    
    # Top 3 share
    top_3_share = sum(times[:3]) / sum(times) * 100 if n >= 3 else 100
    
    # Entropy (Shannon entropy)
    proportions = np.array(times) / sum(times)
    proportions = proportions[proportions > 0]  # Remove zeros
    entropy = -np.sum(proportions * np.log2(proportions))
    max_entropy = np.log2(n)
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
    
    return {
        'gini_coefficient': gini,
        'top_10_percent_share': top_10_share,
        'top_3_share': top_3_share,
        'shannon_entropy': entropy,
        'normalized_entropy': normalized_entropy,
        'max_possible_entropy': max_entropy
    }

def create_response_oriented_network(response_graph, speaker_times):
    """Create network graph where edges represent responses, weighted by duration of response chains."""
    G = nx.DiGraph()
    
    # Add nodes
    for speaker in speaker_times.keys():
        G.add_node(speaker, speaking_time=speaker_times[speaker])
    
    # Add edges with duration-weighted response chains
    for (source, target), data in response_graph.items():
        if source in speaker_times and target in speaker_times:
            G.add_edge(source, target, 
                      weight=data['frequency'],
                      duration=data['avg_duration'],
                      total_duration=data['total_duration'])
    
    if not G.edges():
        return
    
    # Node sizes based on speaking time
    max_time = max(speaker_times.values()) if speaker_times else 1
    node_sizes = [speaker_times.get(node, 0) / max_time * 3000 for node in G.nodes()]
    
    # Edge widths based on average response duration (capacity to elicit extended uptake)
    max_duration = max([d.get('duration', 0) for u, v, d in G.edges(data=True)]) if G.edges() else 1
    edge_widths = [max(d.get('duration', 0) / max_duration * 8, 1) for u, v, d in G.edges(data=True)]
    
    # Edge colors based on frequency (darker = more frequent responses)
    max_freq = max([d.get('weight', 0) for u, v, d in G.edges(data=True)]) if G.edges() else 1
    edge_colors = [plt.cm.Blues(d.get('weight', 0) / max_freq) for u, v, d in G.edges(data=True)]
    
    plt.figure(figsize=(16, 12))
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, 
                           node_color='lightblue', alpha=0.7, edgecolors='black')
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.6, 
                           edge_color=edge_colors, arrows=True, arrowsize=25)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    plt.title('Response-Oriented Network\n(Node size = Speaking time, Edge thickness = Response chain duration,\nEdge color = Response frequency)', 
              fontsize=14, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('response_oriented_network.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_floor_holding_with_interruptions(timeline_data, interruption_markers, speaker_times, total_time):
    """Create timeline showing floor holding with interruption attempts marked.
    Shows tolerance asymmetries: who maintains floor despite interruptions."""
    top_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:10]
    top_speaker_set = set([s[0] for s in top_speakers])
    
    # Filter data
    filtered_timeline = [d for d in timeline_data if d['speaker'] in top_speaker_set]
    filtered_markers = [m for m in interruption_markers if m['interrupted'] in top_speaker_set]
    
    speakers = sorted(set([d['speaker'] for d in filtered_timeline]), 
                     key=lambda x: speaker_times[x], reverse=True)
    
    fig, ax = plt.subplots(figsize=(16, 8))
    
    # Create y positions
    y_positions = {speaker: i for i, speaker in enumerate(speakers)}
    
    # Color map
    colors = plt.cm.tab20(np.linspace(0, 1, len(speakers)))
    color_map = dict(zip(speakers, colors))
    
    # Draw floor holding bars
    for d in filtered_timeline:
        speaker = d['speaker']
        y = y_positions[speaker]
        ax.barh(y, d['duration'], left=d['start'], height=0.6, 
               color=color_map[speaker], alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Mark interruptions
    for marker in filtered_markers:
        speaker = marker['interrupted']
        y = y_positions[speaker]
        color = 'red' if not marker['maintained'] else 'orange'
        marker_size = 100 if marker['maintained'] else 80
        ax.scatter(marker['time'], y, c=color, s=marker_size, 
                  marker='x' if not marker['maintained'] else 'o', 
                  zorder=5, edgecolors='black', linewidths=1)
    
    ax.set_yticks(list(y_positions.values()))
    ax.set_yticklabels(list(y_positions.keys()))
    ax.set_xlabel('Time (seconds)', fontsize=12)
    ax.set_title('Floor Holding with Interruption Attempts\n(Red X = Floor lost, Orange O = Floor maintained)', 
                 fontsize=14, pad=15)
    ax.grid(axis='x', alpha=0.3)
    
    # Legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', label='Interruption: Floor lost'),
        Patch(facecolor='orange', label='Interruption: Floor maintained'),
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig('floor_holding_interruptions.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_tolerance_asymmetry_visualization(tolerance_rates, speaker_times):
    """Visualize interruption tolerance: who maintains floor despite interruptions."""
    # Filter speakers with interruption attempts
    speakers_with_attempts = {k: v for k, v in tolerance_rates.items() if v['attempts'] > 0}
    
    if not speakers_with_attempts:
        return
    
    speakers = list(speakers_with_attempts.keys())
    attempts = [speakers_with_attempts[s]['attempts'] for s in speakers]
    maintained = [speakers_with_attempts[s]['maintained'] for s in speakers]
    rates = [speakers_with_attempts[s]['tolerance_rate'] for s in speakers]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Bar chart: attempts vs maintained
    x = np.arange(len(speakers))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, attempts, width, label='Interruption Attempts', color='lightcoral', alpha=0.7)
    bars2 = ax1.bar(x + width/2, maintained, width, label='Floor Maintained', color='lightgreen', alpha=0.7)
    
    ax1.set_xlabel('Speaker', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('Interruption Tolerance: Attempts vs. Floor Maintenance', fontsize=14, pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(speakers, rotation=45, ha='right')
    ax1.legend()
    ax1.grid(axis='y', alpha=0.3)
    
    # Tolerance rate chart
    colors_rate = ['green' if r > 0.5 else 'orange' if r > 0.25 else 'red' for r in rates]
    bars = ax2.barh(speakers, rates, color=colors_rate, alpha=0.7, edgecolor='black')
    ax2.axvline(0.5, color='gray', linestyle='--', alpha=0.5, label='50% threshold')
    ax2.set_xlabel('Tolerance Rate (Floor Maintained / Attempts)', fontsize=12)
    ax2.set_title('Interruption Tolerance Rates', fontsize=14, pad=15)
    ax2.set_xlim(0, 1)
    ax2.legend()
    ax2.grid(axis='x', alpha=0.3)
    
    # Add value labels
    for i, (bar, rate) in enumerate(zip(bars, rates)):
        ax2.text(rate, i, f' {rate:.2f}', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('interruption_tolerance.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_attractor_visualization(attractor_scores, speaker_times):
    """Visualize conversational attractors: who elicits extended responses."""
    # Sort by average response duration
    sorted_attractors = sorted(attractor_scores.items(), 
                              key=lambda x: x[1]['avg_response_duration'], reverse=True)
    
    if not sorted_attractors:
        return
    
    speakers = [s[0] for s in sorted_attractors[:15]]
    avg_durations = [s[1]['avg_response_duration'] for s in sorted_attractors[:15]]
    total_durations = [s[1]['total_response_duration'] for s in sorted_attractors[:15]]
    frequencies = [s[1]['incoming_responses'] for s in sorted_attractors[:15]]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Average response duration
    bars1 = ax1.barh(speakers, avg_durations, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Average Response Chain Duration (seconds)', fontsize=12)
    ax1.set_title('Conversational Attractors\n(Average Response Duration)', fontsize=14, pad=15)
    ax1.grid(axis='x', alpha=0.3)
    
    # Scatter: frequency vs duration
    ax2.scatter(frequencies, avg_durations, s=100, alpha=0.6, edgecolors='black')
    for i, speaker in enumerate(speakers):
        ax2.annotate(speaker, (frequencies[i], avg_durations[i]), 
                    fontsize=8, alpha=0.7)
    ax2.set_xlabel('Response Frequency', fontsize=12)
    ax2.set_ylabel('Average Response Duration (seconds)', fontsize=12)
    ax2.set_title('Attractor Profile: Frequency vs. Duration', fontsize=14, pad=15)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('conversational_attractors.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_inequality_visualization(speaker_times):
    """Create Lorenz curve for speaking time inequality."""
    times = sorted(speaker_times.values(), reverse=True)
    n = len(times)
    total = sum(times)
    
    if total == 0:
        return
    
    # Cumulative proportions
    cum_times = np.cumsum(times)
    cum_prop_time = cum_times / total
    
    # Cumulative proportion of speakers
    cum_prop_speakers = np.arange(1, n + 1) / n
    
    # Perfect equality line
    perfect_equality = cum_prop_speakers
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    ax.plot(cum_prop_speakers, cum_prop_time, 'b-', linewidth=2, label='Actual Distribution')
    ax.plot(cum_prop_speakers, perfect_equality, 'r--', linewidth=2, label='Perfect Equality')
    ax.fill_between(cum_prop_speakers, cum_prop_time, perfect_equality, alpha=0.3)
    
    ax.set_xlabel('Cumulative Proportion of Speakers', fontsize=12)
    ax.set_ylabel('Cumulative Proportion of Speaking Time', fontsize=12)
    ax.set_title('Lorenz Curve: Speaking Time Inequality', fontsize=14, pad=15)
    ax.legend()
    ax.grid(alpha=0.3)
    
    # Calculate and display Gini
    gini = calculate_inequality_metrics(speaker_times).get('gini_coefficient', 0)
    ax.text(0.6, 0.2, f'Gini Coefficient: {gini:.3f}', 
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
            fontsize=12)
    
    plt.tight_layout()
    plt.savefig('inequality_lorenz_curve.png', dpi=300, bbox_inches='tight')
    plt.close()

def export_d3_data(segments, speaker_times, turns, turn_stats, interruptions, 
                  overlaps, transitions, agenda_introductions, inequality_metrics, 
                  gap_stats, total_time, response_graph, failed_interruptions,
                  tolerance_rates, attractor_scores, timeline_data, interruption_markers,
                  topics, speaker_orientations, topic_closures=None, accountability_patterns=None,
                  recycled_topics=None, topic_hijackings=None):
    """Export data in D3-friendly JSON format for interactive visualizations."""
    
    # Prepare network graph data
    nodes = []
    links = []
    
    for speaker, time in speaker_times.items():
        nodes.append({
            'id': speaker,
            'speaking_time': time,
            'percentage': (time / total_time * 100) if total_time > 0 else 0,
            'turn_count': turn_stats.get(speaker, {}).get('count', 0),
            'avg_turn_length': turn_stats.get(speaker, {}).get('avg_duration', 0)
        })
    
    for (source, target), count in transitions.items():
        if source in speaker_times and target in speaker_times:
            links.append({
                'source': source,
                'target': target,
                'value': count
            })
    
    network_data = {'nodes': nodes, 'links': links}
    
    # Prepare timeline data (all segments)
    all_timeline_data = []
    for seg in segments:
        speaker = get_speaker(seg)
        if not is_filler(seg['text']):
            all_timeline_data.append({
                'speaker': speaker,
                'start': seg['start'],
                'end': seg['end'],
                'duration': seg['end'] - seg['start']
            })
    
    # Prepare cumulative data
    cumulative_data = []
    time_bins = np.linspace(0, total_time, 100)
    top_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:8]
    top_speaker_set = set([s[0] for s in top_speakers])
    
    for speaker, _ in top_speakers:
        cumulative = []
        current_total = 0
        for seg in segments:
            if get_speaker(seg) == speaker and not is_filler(seg['text']):
                current_total += seg['end'] - seg['start']
        cumulative_data.append({
            'speaker': speaker,
            'cumulative_time': current_total
        })
    
    # Prepare interruption network
    interruption_nodes = []
    interruption_links = []
    
    interrupt_out = defaultdict(int)
    interrupt_in = defaultdict(int)
    for inter in interruptions:
        interrupt_out[inter['interrupter']] += 1
        interrupt_in[inter['interrupted']] += 1
    
    for speaker in speaker_times.keys():
        activity = interrupt_out[speaker] + interrupt_in[speaker]
        interruption_nodes.append({
            'id': speaker,
            'interruptions_initiated': interrupt_out[speaker],
            'interruptions_received': interrupt_in[speaker],
            'total_activity': activity
        })
    
    interruption_edges = defaultdict(int)
    for inter in interruptions:
        key = (inter['interrupter'], inter['interrupted'])
        interruption_edges[key] += 1
    
    for (source, target), count in interruption_edges.items():
        if source in speaker_times and target in speaker_times:
            interruption_links.append({
                'source': source,
                'target': target,
                'value': count
            })
    
    interruption_network = {
        'nodes': interruption_nodes,
        'links': interruption_links
    }
    
    # Prepare transition matrix
    all_speakers = sorted(set(speaker_times.keys()))
    transition_matrix = []
    for source in all_speakers:
        row = []
        for target in all_speakers:
            count = transitions.get((source, target), 0)
            row.append(count)
        transition_matrix.append({
            'source': source,
            'targets': row
        })
    
    # Prepare turn length data
    turn_length_data = []
    for speaker, stats in turn_stats.items():
        for duration in stats.get('durations', []):
            turn_length_data.append({
                'speaker': speaker,
                'duration': duration
            })
    
    # Prepare participation heatmap data
    n_segments = 20
    segment_duration = total_time / n_segments
    heatmap_data = []
    top_speakers_heatmap = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)[:15]
    
    for speaker, _ in top_speakers_heatmap:
        row = []
        for i in range(n_segments):
            seg_start = i * segment_duration
            seg_end = (i + 1) * segment_duration
            time_in_segment = 0
            for seg in segments:
                if get_speaker(seg) == speaker and not is_filler(seg['text']):
                    overlap_start = max(seg['start'], seg_start)
                    overlap_end = min(seg['end'], seg_end)
                    if overlap_start < overlap_end:
                        time_in_segment += overlap_end - overlap_start
            row.append({
                'segment': i,
                'time': time_in_segment
            })
        heatmap_data.append({
            'speaker': speaker,
            'segments': row
        })
    
    # Prepare gaps data
    gaps_data = []
    for i in range(len(segments) - 1):
        current = segments[i]
        next_seg = segments[i + 1]
        current_speaker = get_speaker(current)
        next_speaker = get_speaker(next_seg)
        gap = next_seg['start'] - current['end']
        if gap >= 0:
            gaps_data.append({
                'gap': gap,
                'type': 'same_speaker' if current_speaker == next_speaker else 'speaker_change',
                'time': current['end']
            })
    
    # Prepare Lorenz curve data
    times = sorted(speaker_times.values(), reverse=True)
    n = len(times)
    total = sum(times)
    cum_times = np.cumsum(times)
    cum_prop_time = cum_times / total if total > 0 else cum_times
    cum_prop_speakers = np.arange(1, n + 1) / n
    
    lorenz_data = []
    for i in range(n):
        lorenz_data.append({
            'cumulative_speakers': float(cum_prop_speakers[i]),
            'cumulative_time': float(cum_prop_time[i]),
            'perfect_equality': float(cum_prop_speakers[i])
        })
    
    # Prepare response-oriented network
    response_nodes = []
    response_links = []
    for speaker in speaker_times.keys():
        response_nodes.append({
            'id': speaker,
            'speaking_time': speaker_times[speaker]
        })
    
    for (source, target), data in response_graph.items():
        if source in speaker_times and target in speaker_times:
            response_links.append({
                'source': source,
                'target': target,
                'frequency': data['frequency'],
                'avg_duration': data['avg_duration'],
                'total_duration': data['total_duration']
            })
    
    response_network = {
        'nodes': response_nodes,
        'links': response_links
    }
    
    # Prepare tolerance data
    tolerance_data = []
    for speaker, rates in tolerance_rates.items():
        tolerance_data.append({
            'speaker': speaker,
            'attempts': rates['attempts'],
            'maintained': rates['maintained'],
            'tolerance_rate': rates['tolerance_rate']
        })
    
    # Prepare attractor data
    attractor_data = []
    for speaker, scores in attractor_scores.items():
        attractor_data.append({
            'speaker': speaker,
            'incoming_responses': scores['incoming_responses'],
            'total_response_duration': scores['total_response_duration'],
            'avg_response_duration': scores['avg_response_duration'],
            'max_response_duration': scores['max_response_duration']
        })
    
    # Compile all data
    d3_data = {
        'metadata': {
            'meeting_duration': total_time,
            'total_speakers': len(speaker_times),
            'total_segments': len(segments),
            'total_turns': len(turns)
        },
        'network': network_data,
        'timeline': all_timeline_data,
        'cumulative': cumulative_data,
        'interruption_network': interruption_network,
        'transition_matrix': {
            'speakers': all_speakers,
            'matrix': transition_matrix
        },
        'turn_lengths': turn_length_data,
        'participation_heatmap': {
            'n_segments': n_segments,
            'segment_duration': segment_duration,
            'data': heatmap_data
        },
        'gaps': gaps_data,
        'lorenz_curve': lorenz_data,
        'inequality_metrics': inequality_metrics,
        'gap_statistics': gap_stats,
        'speaker_times': {k: float(v) for k, v in speaker_times.items()},
        'agenda_control': {
            'introductions': [
                {'speaker': a['speaker'], 'time': a['time'], 'silence': a['preceding_silence']}
                for a in agenda_introductions
            ]
        },
        'relational_interaction': {
            'response_network': response_network,
            'failed_interruptions': failed_interruptions,
            'tolerance_rates': tolerance_data,
            'attractor_scores': attractor_data,
            'floor_holding_timeline': timeline_data,
            'interruption_markers': interruption_markers
        },
        'topic_emergence': {
            'topics': topics,
            'speaker_orientations': speaker_orientations,
            'topic_summary': {
                'total_topics': len(topics),
                'stabilized': len([t for t in topics if t['status'] == 'stabilized']),
                'failed_silence': len([t for t in topics if t['status'] == 'failed_silence']),
                'failed_no_uptake': len([t for t in topics if t['status'] == 'failed_no_uptake'])
            },
            'topic_content': {
                # Include full text for all topics
                'topics_with_content': [
                    {
                        'topic_id': t['topic_id'],
                        'proposer': t['proposer'],
                        'start_time': t['start_time'],
                        'end_time': t['end_time'],
                        'status': t['status'],
                        'full_text': t.get('text', t.get('text_sample', '')),
                        'responders': [
                            {
                                'speaker': r['speaker'],
                                'time': r['time'],
                                'similarity': r['similarity'],
                                'delay': r['response_delay'],
                                'response_text': r.get('response_text', ''),
                                'uptake': bool(r.get('similarity', 0) >= 0.3)
                            }
                            for r in t.get('stabilization', {}).get('all_responses', [])
                        ]
                    }
                    for t in topics
                ]
            },
            'fine_grained_relations': {
                'topic_closures': topic_closures if topic_closures else [],
                'accountability_patterns': accountability_patterns if accountability_patterns else {},
                'recycled_topics': recycled_topics if recycled_topics else [],
                'topic_hijackings': topic_hijackings if topic_hijackings else []
            }
        },
        'fine_grained_relations': {
            'topic_closures': topic_closures if topic_closures else [],
            'accountability_patterns': accountability_patterns if accountability_patterns else {},
            'recycled_topics': recycled_topics if recycled_topics else [],
            'topic_hijackings': topic_hijackings if topic_hijackings else []
        }
    }
    
    # Save to JSON
    # Convert numpy types to native Python types for JSON serialization
    def convert_to_native(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_native(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_native(item) for item in obj]
        elif isinstance(obj, bool):
            return bool(obj)
        return obj
    
    d3_data = convert_to_native(d3_data)
    
    with open('d3_visualization_data.json', 'w', encoding='utf-8') as f:
        json.dump(d3_data, f, indent=2, ensure_ascii=False)
    
    print("  - d3_visualization_data.json exported")

def generate_summary_report(speaker_times, total_time, turn_stats, interruptions, 
                           overlaps, transitions, agenda_introductions):
    """Generate structured summary report."""
    report = {
        'meeting_duration': total_time,
        'speaking_time_dominance': {},
        'turn_taking_structure': {},
        'interruption_patterns': {
            'total_interruptions': len(interruptions),
            'interruption_by_speaker': Counter([i['interrupter'] for i in interruptions]),
            'interrupted_by_speaker': Counter([i['interrupted'] for i in interruptions])
        },
        'overlap_patterns': {
            'total_overlaps': len(overlaps),
            'overlap_duration_total': sum([o['overlap_duration'] for o in overlaps])
        },
        'interaction_graph': {
            'total_transitions': sum(transitions.values()),
            'unique_transitions': len(transitions)
        },
        'agenda_control': {
            'total_introductions': len(agenda_introductions),
            'introductions_by_speaker': Counter([a['speaker'] for a in agenda_introductions])
        }
    }
    
    # Speaking time dominance
    for speaker, time in speaker_times.items():
        report['speaking_time_dominance'][speaker] = {
            'total_seconds': time,
            'percentage': (time / total_time * 100) if total_time > 0 else 0
        }
    
    # Turn-taking structure
    for speaker, stats in turn_stats.items():
        report['turn_taking_structure'][speaker] = {
            'turn_count': stats['count'],
            'total_duration': stats['total_duration'],
            'average_turn_length': stats['avg_duration']
        }
    
    return report

def main():
    print("Loading transcript...")
    segments = load_transcript('amuta_2026-01-12_1.json')
    print(f"Loaded {len(segments)} segments")
    
    print("Computing speaking time...")
    speaker_times, total_time = compute_speaking_time(segments)
    
    print("Analyzing turn-taking...")
    turns, turn_stats = compute_turn_taking(segments)
    
    print("Detecting interruptions and overlaps...")
    interruptions, overlaps = detect_interruptions(segments, threshold=0.5)
    
    print("Building interaction graph...")
    transitions, transition_durations = build_interaction_graph(segments)
    
    print("Building response-oriented graph...")
    response_graph = build_response_oriented_graph(segments, turns)
    
    print("Detecting failed interruptions and tolerance...")
    failed_interruptions, tolerance_rates = detect_failed_interruptions(segments, interruptions, turns)
    
    print("Identifying conversational attractors...")
    attractor_scores = identify_conversational_attractors(response_graph, speaker_times)
    
    print("Creating floor holding timeline...")
    timeline_data, interruption_markers = create_floor_holding_timeline(
        segments, interruptions, failed_interruptions, speaker_times)
    
    print("Identifying agenda control...")
    agenda_introductions = identify_agenda_control(segments, turns, silence_threshold=2.0)
    
    print("Analyzing topic emergence and lifecycle...")
    topics = analyze_topic_lifecycle(segments, turns, similarity_threshold=0.25, stabilization_threshold=0.3)
    
    print("Analyzing speaker orientation to topics...")
    speaker_orientations = analyze_speaker_orientation_to_topics(topics, segments, turns, similarity_threshold=0.3)
    
    print("Generating visualizations...")
    create_network_graph(speaker_times, transitions)
    create_timeline_chart(speaker_times, total_time)
    
    # Get all unique speakers for heatmap
    all_speakers = sorted(set(speaker_times.keys()))
    create_transition_heatmap(transitions, all_speakers)
    
    print("Generating additional visualizations...")
    create_timeline_visualization(segments, speaker_times)
    create_cumulative_speaking_time(segments, speaker_times, total_time)
    create_turn_length_distribution(turn_stats)
    create_interruption_network(interruptions, speaker_times)
    gap_stats = create_gap_analysis(segments)
    create_participation_heatmap(segments, speaker_times, total_time, n_segments=20)
    create_inequality_visualization(speaker_times)
    
    print("Generating relational interaction visualizations...")
    create_response_oriented_network(response_graph, speaker_times)
    create_floor_holding_with_interruptions(timeline_data, interruption_markers, speaker_times, total_time)
    create_tolerance_asymmetry_visualization(tolerance_rates, speaker_times)
    create_attractor_visualization(attractor_scores, speaker_times)
    
    print("Generating topic emergence visualizations...")
    create_topic_timeline(topics, turns, total_time)
    speaker_topic_network = create_speaker_topic_network(topics, speaker_orientations, speaker_times)
    create_topic_trajectory(topics, segments, turns)
    create_topic_content_visualization(topics, speaker_times)
    create_speaker_topic_engagement_matrix(topics, speaker_orientations, speaker_times)
    
    print("Analyzing topic engagement and power dynamics...")
    topic_engagement = analyze_topic_engagement_and_power(topics, speaker_orientations, speaker_times, total_time)
    
    print("Analyzing fine-grained topic-speaker relations...")
    topic_closures = detect_topic_closure_authority(topics, segments, turns, similarity_threshold=0.3)
    accountability_patterns = detect_asymmetric_topical_accountability(topics, segments, turns)
    recycled_topics = detect_topic_recycling(topics, segments, turns, similarity_threshold=0.4)
    topic_hijackings = detect_topic_hijacking_vs_alignment(topics, segments, turns, similarity_threshold=0.3)
    
    print("Generating fine-grained power dynamics report...")
    create_fine_grained_topic_power_report(topic_closures, accountability_patterns, 
                                          recycled_topics, topic_hijackings, topics, speaker_times)
    
    # Calculate inequality metrics
    inequality_metrics = calculate_inequality_metrics(speaker_times)
    
    print("Generating summary report...")
    report = generate_summary_report(speaker_times, total_time, turn_stats, 
                                     interruptions, overlaps, transitions, 
                                     agenda_introductions)
    
    # Add new metrics to report
    report['inequality_metrics'] = inequality_metrics
    report['gap_statistics'] = gap_stats
    
    # Save report
    with open('power_dynamics_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    # Export data for D3/Observable visualizations
    print("Exporting data for interactive visualizations...")
    export_d3_data(segments, speaker_times, turns, turn_stats, interruptions, 
                   overlaps, transitions, agenda_introductions, inequality_metrics, 
                   gap_stats, total_time, response_graph, failed_interruptions, 
                   tolerance_rates, attractor_scores, timeline_data, interruption_markers,
                   topics, speaker_orientations, topic_closures, accountability_patterns,
                   recycled_topics, topic_hijackings)
    
    # Print summary
    print("\n" + "="*80)
    print("POWER DYNAMICS ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nMeeting Duration: {total_time:.2f} seconds ({total_time/60:.2f} minutes)")
    print(f"Number of Speakers: {len(speaker_times)}")
    print(f"Total Segments: {len(segments)}")
    print(f"Total Turns: {len(turns)}")
    
    print("\n--- Speaking Time Dominance ---")
    sorted_speakers = sorted(speaker_times.items(), key=lambda x: x[1], reverse=True)
    for speaker, time in sorted_speakers:
        pct = (time / total_time * 100) if total_time > 0 else 0
        print(f"{speaker}: {time:.2f}s ({pct:.1f}%)")
    
    print("\n--- Turn-Taking Structure ---")
    for speaker in sorted(speaker_times.keys(), key=lambda x: speaker_times[x], reverse=True):
        if speaker in turn_stats:
            stats = turn_stats[speaker]
            print(f"{speaker}: {stats['count']} turns, avg length: {stats['avg_duration']:.2f}s")
    
    print("\n--- Interruption Patterns ---")
    print(f"Total potential interruptions: {len(interruptions)}")
    if interruptions:
        interrupter_counts = Counter([i['interrupter'] for i in interruptions])
        print("Top interrupters:")
        for speaker, count in interrupter_counts.most_common(5):
            print(f"  {speaker}: {count}")
    
    print("\n--- Overlap Patterns ---")
    print(f"Total overlaps: {len(overlaps)}")
    if overlaps:
        total_overlap_time = sum([o['overlap_duration'] for o in overlaps])
        print(f"Total overlap duration: {total_overlap_time:.2f}s")
    
    print("\n--- Interaction Graph ---")
    print(f"Total transitions: {sum(transitions.values())}")
    print(f"Unique transition pairs: {len(transitions)}")
    
    print("\n--- Agenda Control ---")
    agenda_counts = Counter([a['speaker'] for a in agenda_introductions])
    print("Topic introductions by speaker:")
    for speaker, count in agenda_counts.most_common():
        print(f"  {speaker}: {count}")
    
    print("\n--- Topic Emergence Analysis ---")
    print(f"Total topics detected: {len(topics)}")
    stabilized = len([t for t in topics if t['status'] == 'stabilized'])
    failed_silence = len([t for t in topics if t['status'] == 'failed_silence'])
    failed_no_uptake = len([t for t in topics if t['status'] == 'failed_no_uptake'])
    print(f"  Stabilized (uptake): {stabilized}")
    print(f"  Failed (silence): {failed_silence}")
    print(f"  Failed (no uptake): {failed_no_uptake}")
    
    print("\nTopic proposers:")
    proposer_counts = Counter([t['proposer'] for t in topics])
    for speaker, count in proposer_counts.most_common():
        stabilized_by_speaker = len([t for t in topics if t['proposer'] == speaker and t['status'] == 'stabilized'])
        print(f"  {speaker}: {count} topics ({stabilized_by_speaker} stabilized)")
    
    print("\nSpeaker orientation to topics:")
    for speaker, orientation in sorted(speaker_orientations.items(), 
                                       key=lambda x: len(x[1]['topics_proposed']), reverse=True)[:10]:
        print(f"  {speaker}:")
        print(f"    Proposed: {len(orientation['topics_proposed'])}")
        print(f"    Responded to: {len(orientation['topics_responded_to'])}")
        if orientation['uptake_delays']:
            avg_delay = np.mean(orientation['uptake_delays'])
            print(f"    Avg response delay: {avg_delay:.2f}s")
        print(f"    Redirections: {len(orientation['redirections'])}")
        print(f"    Monopolizations: {len(orientation['monopolizations'])}")
    
    print("\n--- Gap Analysis ---")
    if gap_stats:
        print(f"Median gap between utterances: {gap_stats['median_gap']:.2f}s")
        print(f"Mean gap between utterances: {gap_stats['mean_gap']:.2f}s")
        print(f"Same speaker gap (median): {gap_stats['same_speaker_median']:.2f}s")
        print(f"Speaker change gap (median): {gap_stats['speaker_change_median']:.2f}s")
    
    print("\n--- Inequality Metrics ---")
    if inequality_metrics:
        print(f"Gini Coefficient: {inequality_metrics['gini_coefficient']:.3f}")
        print(f"Top 10% share: {inequality_metrics['top_10_percent_share']:.1f}%")
        print(f"Top 3 share: {inequality_metrics['top_3_share']:.1f}%")
        print(f"Normalized Entropy: {inequality_metrics['normalized_entropy']:.3f}")
        print(f"  (1.0 = perfect equality, 0.0 = maximum inequality)")
    
    print("\n" + "="*80)
    print("Visualizations saved:")
    print("  - speaker_network.png")
    print("  - speaking_time_distribution.png")
    print("  - transition_heatmap.png")
    print("  - speaking_timeline.png")
    print("  - cumulative_speaking_time.png")
    print("  - turn_length_distribution.png")
    print("  - interruption_network.png")
    print("  - gap_analysis.png")
    print("  - participation_heatmap.png")
    print("  - inequality_lorenz_curve.png")
    print("  - response_oriented_network.png")
    print("  - floor_holding_interruptions.png")
    print("  - interruption_tolerance.png")
    print("  - conversational_attractors.png")
    print("  - topic_timeline.png")
    print("  - speaker_topic_network.png")
    print("  - topic_trajectories.png")
    print("  - power_dynamics_report.json")
    print("="*80)
    
    # Generate methodological note
    methodological_note = """
METHODOLOGICAL NOTE: OPERATIONALIZING POWER DYNAMICS

This analysis operationalizes interactional power dynamics through structural features
of conversation, not through semantic interpretation or assumptions about authority.

Key Operationalizations:

1. Speaking Time Dominance: Measured as total duration of non-filler utterances per
   speaker, expressed as absolute time and percentage of total meeting duration.

2. Turn-Taking Structure: Quantifies the number of turns per speaker and average turn
   length. Asymmetries emerge when some speakers have many short turns while others
   have few long turns, indicating different interactional strategies.

3. Interruption Proxy: Detects rapid turn-taking (gaps < 0.5s) between different
   speakers as a proxy for interruption behavior. This is a structural indicator,
   not a claim about intentionality.

4. Overlap Detection: Identifies temporal overlaps in speech timestamps, indicating
   simultaneous speech events.

5. Directed Interaction Graph: Constructs a weighted directed graph where edges
   represent immediate speaker transitions. Edge weights indicate frequency of
   transitions, revealing patterns of who responds to whom.

6. Agenda Control Indicators: Identifies speakers who initiate new conversational
   segments after silence periods (≥2s), operationalizing topic introduction
   behavior.

Interpretive Constraints:
- No claims are made about speaker intentions, authority, or argumentative quality.
- Metrics describe structural patterns only.
- Normative interpretation (dominant, marginal, aggressive, passive) is left to
  the human analyst.
- Speaker labels are treated as unique nodes without identity inference.

All visualizations use neutral color schemes and prioritize legibility over
aesthetic embellishment.
"""
    
    with open('methodological_note.txt', 'w', encoding='utf-8') as f:
        f.write(methodological_note)
    
    print("\nMethodological note saved to: methodological_note.txt")

if __name__ == '__main__':
    main()
