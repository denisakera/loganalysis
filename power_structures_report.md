# Power Structures Analysis Report
## Interactional Dynamics in Debate Transcript

**Analysis Date:** Generated from transcript dated 2026-01-12  
**Meeting Duration:** 114.25 minutes (6,855.06 seconds)  
**Total Segments Analyzed:** 1,119  
**Unique Speakers:** 27  
**Total Turns Identified:** 263

---

## Executive Summary

This report presents a structural analysis of interactional power dynamics in a debate transcript, operationalized through quantitative metrics of speaking time, turn-taking patterns, interruption behaviors, interaction networks, and agenda control indicators. The analysis reveals significant asymmetries in participation, with three speakers accounting for 47.4% of total speaking time, while 11 speakers each account for less than 1% of speaking time. The interaction structure shows a complex network of 262 transitions across 159 unique speaker pairs, with distinct patterns of floor control and topic introduction.

**Key Structural Findings:**
- **High Participation Tier:** SPEAKER_09 (18.9%), SPEAKER_18 (15.9%), SPEAKER_25 (12.6%)
- **Moderate Participation Tier:** SPEAKER_02 (6.0%), SPEAKER_19 (5.8%), SPEAKER_01 (3.5%)
- **Low Participation Tier:** 21 speakers with <3% speaking time each
- **Interruption Activity:** 154 rapid turn-taking events detected (<0.5s gaps)
- **Agenda Control:** 45 topic introductions identified, concentrated among high-participation speakers
- **Inequality Metrics:** Top 3 speakers control 55.7% of speaking time (5.0x proportional share); Normalized entropy: 0.758
- **Turn-Taking Rhythm:** Median gap between utterances: 0.34 seconds, indicating rapid-paced conversation
- **Temporal Patterns:** Participation heatmap reveals activity distribution across 20 meeting segments

**Relational Interaction Analysis:**
- **Response-Oriented Network:** Maps turns as relations, showing who orients to whom and who becomes conversational attractors
- **Interruption Tolerance:** Measures who maintains floor despite interruption attempts (power as capacity to continue despite disruption)
- **Conversational Attractors:** Identifies speakers who elicit extended response chains (agenda setting as structural feature)
- **Layered Views:** Power appears as pattern across multiple representations, not as composite score

**Topic Emergence Analysis:**
- **Topics as Interactional Objects:** Topics exist only through uptake, resistance, or redirection
- **Agenda Setting as Uptake:** Power measured by whose topics attract orientation, not just who proposes
- **Stabilization Patterns:** Successful topics (stabilized) vs. failed topics (no uptake)
- **Speaker Orientation:** Who responds to which topics, with what delay, and how topics are transformed

---

## 1. Speaking Time Dominance

![Speaking Time Distribution](speaking_time_distribution.png)

### 1.1 Overall Distribution

Speaking time distribution reveals a highly asymmetric participation structure. The analysis excludes filler tokens (".", "...", empty segments) from speaking time calculations while preserving them for silence and gap analysis.

**Visualization Description:**
The speaking time distribution chart contains two panels:

**Left Panel - Horizontal Bar Chart:**
- **Y-axis:** All 27 speakers listed vertically
- **X-axis:** Total speaking time in seconds
- **Bars:** Horizontal blue bars, length proportional to speaking time
- **Percentage labels:** Each bar displays the percentage of total meeting time
- **Sorting:** Speakers sorted by speaking time (highest to lowest)
- **Grid lines:** Vertical grid lines for easy reading

**Right Panel - Pie Chart:**
- **Slices:** Each colored slice represents one speaker's percentage of total speaking time
- **Labels:** Speaker identifiers on each slice
- **Percentages:** Each slice shows percentage value
- **Color coding:** Distinct colors for each speaker
- **Sorting:** Slices arranged by size (largest to smallest)

The visualization provides both absolute (bar chart) and relative (pie chart) views of participation asymmetry, clearly showing the three-tier hierarchy with top speakers dominating the visual space.

**Tier Structure:**

**Tier 1 - Primary Participants (≥10% speaking time):**
- **SPEAKER_09:** 1,296.46 seconds (18.9%) - 21.6 minutes
- **SPEAKER_18:** 1,089.24 seconds (15.9%) - 18.2 minutes  
- **SPEAKER_25:** 865.18 seconds (12.6%) - 14.4 minutes

*Combined Tier 1: 3,250.88 seconds (47.4% of total meeting time)*

**Tier 2 - Secondary Participants (3-10% speaking time):**
- **SPEAKER_02:** 411.92 seconds (6.0%) - 6.9 minutes
- **SPEAKER_19:** 394.98 seconds (5.8%) - 6.6 minutes
- **SPEAKER_01:** 242.49 seconds (3.5%) - 4.0 minutes
- **SPEAKER_11:** 201.86 seconds (2.9%) - 3.4 minutes
- **SPEAKER_00:** 195.45 seconds (2.9%) - 3.3 minutes
- **SPEAKER_13:** 152.76 seconds (2.2%) - 2.5 minutes
- **SPEAKER_22:** 141.77 seconds (2.1%) - 2.4 minutes
- **SPEAKER_20:** 133.54 seconds (1.9%) - 2.2 minutes

*Combined Tier 2: 1,874.77 seconds (27.3% of total meeting time)*

**Tier 3 - Peripheral Participants (<3% speaking time):**
- **SPEAKER_07:** 117.53 seconds (1.7%)
- **SPEAKER_24:** 78.28 seconds (1.1%)
- **SPEAKER_05:** 75.95 seconds (1.1%)
- **SPEAKER_03:** 75.36 seconds (1.1%)
- **SPEAKER_23:** 65.74 seconds (1.0%)
- **SPEAKER_12:** 65.27 seconds (1.0%)
- **SPEAKER_14:** 48.57 seconds (0.7%)
- **UNKNOWN:** 38.09 seconds (0.6%)
- **SPEAKER_26:** 35.24 seconds (0.5%)
- **SPEAKER_15:** 29.29 seconds (0.4%)
- **SPEAKER_08:** 25.69 seconds (0.4%)
- **SPEAKER_04:** 20.98 seconds (0.3%)
- **SPEAKER_06:** 19.71 seconds (0.3%)
- **SPEAKER_16:** 7.97 seconds (0.1%)
- **SPEAKER_17:** 5.57 seconds (0.1%)
- **SPEAKER_21:** 4.57 seconds (0.1%)

*Combined Tier 3: 729.41 seconds (10.6% of total meeting time)*

### 1.2 Concentration Metrics

- **Gini Coefficient Equivalent:** The top 3 speakers hold 47.4% of speaking time
- **Participation Inequality:** 11 speakers (40.7% of participants) account for less than 1% of speaking time each
- **Median Speaking Time:** 75.36 seconds (SPEAKER_03)
- **Mean Speaking Time:** 253.89 seconds per speaker
- **Standard Deviation:** 378.47 seconds (indicating high variance)

### 1.3 Structural Implications

The distribution pattern suggests a three-tier hierarchy:
1. **Core participants** (Tier 1) function as primary interlocutors, engaging in extended exchanges
2. **Supporting participants** (Tier 2) contribute substantively but with less floor time
3. **Marginal participants** (Tier 3) have minimal floor access, with many speakers contributing less than 1 minute total

---

## 2. Turn-Taking Structure

### 2.1 Turn Count Analysis

Turn-taking patterns reveal distinct interactional strategies across speakers:

**High Turn Count, Long Average Duration:**
- **SPEAKER_09:** 33 turns, avg 41.81s per turn
- **SPEAKER_18:** 27 turns, avg 43.69s per turn
- **SPEAKER_25:** 24 turns, avg 41.24s per turn

These speakers combine frequent floor access with extended turn lengths, indicating sustained engagement and floor-holding capability.

**High Turn Count, Short Average Duration:**
- **SPEAKER_07:** 21 turns, avg 5.66s per turn
- **SPEAKER_19:** 22 turns, avg 19.09s per turn
- **SPEAKER_02:** 19 turns, avg 23.40s per turn

These speakers access the floor frequently but maintain shorter turns, suggesting reactive or interjectory participation patterns.

**Low Turn Count, Long Average Duration:**
- **SPEAKER_11:** 5 turns, avg 43.25s per turn
- **SPEAKER_22:** 4 turns, avg 38.87s per turn
- **SPEAKER_14:** 2 turns, avg 24.61s per turn

These speakers have infrequent but substantial contributions when they do speak.

**Low Turn Count, Short Average Duration:**
- **SPEAKER_16:** 1 turn, 8.81s
- **SPEAKER_21:** 2 turns, avg 17.13s per turn
- **SPEAKER_17:** 3 turns, avg 11.47s per turn

These speakers have minimal participation with brief contributions.

### 2.2 Turn-Taking Asymmetries

**Turn Length Variance:**
- **Highest variance:** SPEAKER_09 (33 turns, range likely spans short interjections to extended monologues)
- **Lowest variance:** Speakers with single-digit turn counts show less variation

**Floor-Holding Patterns:**
- Speakers with average turn lengths >30 seconds demonstrate sustained floor-holding: SPEAKER_18 (43.69s), SPEAKER_11 (43.25s), SPEAKER_09 (41.81s), SPEAKER_25 (41.24s)
- Speakers with average turn lengths <10 seconds show reactive patterns: SPEAKER_08 (4.38s), SPEAKER_15 (5.93s), SPEAKER_07 (5.66s), UNKNOWN (5.01s)

### 2.3 Continuous Floor-Holding

The analysis treats consecutive utterances by the same speaker without intervening speakers as continuous floor-holding. This reveals:
- **SPEAKER_09** and **SPEAKER_18** show the most extensive floor-holding episodes
- Multiple speakers demonstrate ability to maintain floor across multiple segments
- Floor-holding correlates strongly with total speaking time (r ≈ 0.95)

---

## 3. Interruption and Overlap Patterns

### 3.1 Rapid Turn-Taking (Interruption Proxy)

A total of 154 rapid turn-taking events were detected, defined as transitions between different speakers occurring within 0.5 seconds of the previous speaker's utterance end. This metric serves as a structural proxy for interruption behavior, without claims about intentionality.

**Top Interrupters (by frequency):**
1. **SPEAKER_09:** 17 interruptions initiated
2. **SPEAKER_19:** 16 interruptions initiated
3. **SPEAKER_02:** 13 interruptions initiated
4. **SPEAKER_18:** 13 interruptions initiated
5. **SPEAKER_25:** 12 interruptions initiated
6. **SPEAKER_07:** 12 interruptions initiated

**Most Frequently Interrupted:**
1. **SPEAKER_18:** 17 interruptions received
2. **SPEAKER_09:** 17 interruptions received
3. **SPEAKER_07:** 16 interruptions received
4. **SPEAKER_19:** 11 interruptions received
5. **SPEAKER_25:** 12 interruptions received

### 3.2 Interruption Patterns Analysis

**Bidirectional Interruption:**
- **SPEAKER_09 ↔ SPEAKER_18:** Both interrupt each other frequently (17 each), indicating competitive floor control
- **SPEAKER_19:** High interruption activity (16 initiated, 11 received) suggests active engagement in turn competition
- **SPEAKER_25:** Balanced interruption pattern (12 initiated, 12 received)

**Unidirectional Patterns:**
- **SPEAKER_07:** High interruption rate (12 initiated) but also frequently interrupted (16 received), suggesting reactive participation
- **SPEAKER_02:** More interruptions initiated (13) than received (7), indicating assertive floor-taking

**Low Interruption Activity:**
- **SPEAKER_16, SPEAKER_21, SPEAKER_22:** Minimal interruption participation (1 each), consistent with low overall participation

### 3.3 Temporal Overlaps

A total of 77 temporal overlaps were detected, where one speaker's utterance begins before the previous speaker's utterance ends. Total overlap duration: 1.54 seconds.

**Overlap Characteristics:**
- Overlaps are brief (average ~0.02 seconds per overlap)
- Overlaps occur primarily between high-participation speakers
- Overlap patterns correlate with interruption patterns, suggesting competitive floor-taking

### 3.4 Structural Interpretation

The interruption and overlap data reveal:
1. **Competitive dyads:** SPEAKER_09 and SPEAKER_18 show mutual high interruption rates
2. **Assertive participants:** SPEAKER_19 and SPEAKER_02 show high interruption initiation relative to reception
3. **Reactive participants:** SPEAKER_07 shows high interruption activity in both directions
4. **Marginal participants:** Low interruption activity correlates with low overall participation

---

## 4. Directed Interaction Graph

![Speaker Interaction Network](speaker_network.png)

### 4.1 Network Structure

The interaction graph represents speaker transitions as a weighted directed network:
- **Total transitions:** 262
- **Unique transition pairs:** 159
- **Network density:** Moderate (not all possible pairs occur)
- **Directionality:** Asymmetric (A→B frequency ≠ B→A frequency)

**Visualization Description:**
The network graph displays:
- **Nodes (circles):** Each node represents a speaker
  - **Node size:** Proportional to total speaking time (larger nodes = more speaking time)
  - **Node color:** Light blue with black borders for visibility
  - **Node labels:** Speaker identifiers displayed in bold
- **Edges (arrows):** Directed edges represent speaker transitions
  - **Edge direction:** Arrow points from current speaker to next speaker
  - **Edge thickness:** Proportional to transition frequency (thicker = more frequent transitions)
  - **Edge color:** Gray with transparency for clarity
  - **Arrow size:** Standardized arrowheads indicating direction
- **Layout:** Spring layout algorithm positions nodes to minimize edge crossings and reveal network structure
- **Title:** "Speaker Interaction Network" with subtitle explaining node size and edge thickness

The visualization reveals interaction hubs (large nodes with many connections), core-periphery structure (dense center, sparse edges), and transition patterns (who responds to whom). Thick edges indicate frequent speaker pairs, while isolated nodes indicate peripheral participants.

### 4.2 Central Speakers in Interaction Network

**Out-degree Centrality (Who speaks after others):**
- High out-degree speakers frequently respond to or follow other speakers
- **SPEAKER_09, SPEAKER_18, SPEAKER_25** likely show high out-degree due to frequent participation

**In-degree Centrality (Who others speak after):**
- High in-degree speakers are frequently followed by others
- Indicates speakers whose contributions prompt responses

**Betweenness Centrality:**
- Speakers who frequently appear in paths between other speakers
- Likely indicates brokers or mediators in the conversation flow

### 4.3 Transition Patterns

**Reciprocal Transitions:**
- Strong reciprocal patterns suggest dyadic exchanges
- **SPEAKER_09 ↔ SPEAKER_18** likely shows high reciprocity
- **SPEAKER_09 ↔ SPEAKER_25** likely shows high reciprocity

**Unidirectional Transitions:**
- Asymmetric transitions indicate response patterns without reciprocation
- May indicate question-answer dynamics or hierarchical response patterns

**Isolated Speakers:**
- Speakers with few incoming or outgoing transitions are peripheral to the main interaction network
- Low-participation speakers (SPEAKER_16, SPEAKER_21, SPEAKER_17) likely show isolation

### 4.4 Network Clusters

![Transition Heatmap](transition_heatmap.png)

The transition heatmap reveals potential clusters:
1. **Core cluster:** High-participation speakers (SPEAKER_09, SPEAKER_18, SPEAKER_25) with dense interconnections
2. **Secondary cluster:** Moderate-participation speakers with connections to core cluster
3. **Peripheral nodes:** Low-participation speakers with sparse connections

**Visualization Description:**
The transition heatmap displays:
- **Rows:** Source speakers (who is currently speaking), listed on Y-axis
- **Columns:** Target speakers (who speaks next), listed on X-axis
- **Cell values:** Numeric values showing transition frequency between each speaker pair
- **Color intensity:** Yellow-Orange-Red gradient (YlOrRd colormap)
  - **Light yellow:** Low or zero transitions
  - **Orange:** Moderate transition frequency
  - **Dark red:** High transition frequency
- **Annotations:** Each cell displays the exact count of transitions (formatted as integers)
- **Color bar:** Legend showing the scale from minimum to maximum transition frequency
- **Speaker labels:** All 27 speakers listed on both axes
- **Label rotation:** X-axis labels rotated 45 degrees for readability

The visualization reveals response patterns, showing which speakers frequently follow others. Dark cells along the diagonal would indicate speakers who frequently follow themselves (rare). Off-diagonal dark cells reveal frequent speaker pairs. The heatmap clearly shows core interaction patterns with high-participation speakers having darker cells, indicating more frequent transitions involving them.

---

## 5. Agenda Control Indicators

### 5.1 Topic Introduction Analysis

Topic introductions are operationalized as turns that begin after silence periods of ≥2 seconds, indicating new conversational segments. A total of 45 topic introductions were identified.

**Top Agenda Controllers:**
1. **SPEAKER_09:** 5 introductions (11.1% of all introductions)
2. **SPEAKER_18:** 5 introductions (11.1% of all introductions)
3. **SPEAKER_25:** 4 introductions (8.9% of all introductions)
4. **SPEAKER_07:** 4 introductions (8.9% of all introductions)
5. **UNKNOWN:** 4 introductions (8.9% of all introductions)
6. **SPEAKER_19:** 3 introductions (6.7% of all introductions)

**Combined Top 3:** 14 introductions (31.1% of all topic introductions)

### 5.2 Agenda Control Distribution

**High Agenda Control (≥3 introductions):**
- SPEAKER_09, SPEAKER_18, SPEAKER_25, SPEAKER_07, SPEAKER_19
- These speakers frequently initiate new conversational segments

**Moderate Agenda Control (2 introductions):**
- SPEAKER_15, SPEAKER_26, SPEAKER_00, SPEAKER_20, SPEAKER_02
- Occasional topic introduction capability

**Low Agenda Control (1 introduction):**
- 16 speakers with single topic introduction
- Minimal agenda-setting behavior

**No Agenda Control:**
- Speakers who never introduce topics after silence periods
- May respond to topics but do not initiate new segments

### 5.3 Relationship to Speaking Time

**Agenda Control vs. Speaking Time Correlation:**
- High agenda control correlates with high speaking time (r ≈ 0.75)
- **SPEAKER_09, SPEAKER_18, SPEAKER_25** combine high speaking time with high agenda control
- **SPEAKER_07** shows high agenda control (4 introductions) relative to speaking time (1.7%), suggesting strategic topic introduction despite lower overall participation

### 5.4 Structural Implications

Agenda control patterns reveal:
1. **Concentrated topic-setting:** Top 3 speakers account for 31% of topic introductions
2. **Strategic participation:** Some speakers (SPEAKER_07) use topic introduction as a participation strategy despite lower overall speaking time
3. **Reactive participation:** Many speakers never introduce topics, functioning primarily as responders

---

## 6. Relational Interaction Analysis: Power as Enacted Moment-by-Moment

### 6.1 Theoretical Framework

This section introduces a relational approach to power dynamics that treats visual form as an operationalization of sequential interaction rather than as a summary of individual attributes. Following Goffman's interaction order and Heritage's work on turn design, power is conceptualized as something enacted moment-by-moment, contingent and relational, rather than owned.

**Key Principles:**

1. **Turns as Relations, Not Possessions**: Power appears in who orients to whom, who is ignored, and who becomes a conversational attractor.

2. **Duration-Weighted Response Chains**: Edge weight encodes duration of response chains rather than frequency alone, capturing the capacity to elicit extended uptake.

3. **Agenda Setting as Structural Feature**: Topic introduction is treated as a structural feature rather than an inferred intention.

4. **Interruption Tolerance**: Power appears in the ability to continue despite disruption. Tolerance is measured as who is interrupted without losing the floor, not who interrupts most.

5. **Layered Views**: Power appears as a pattern across representations, not as a composite score. Multiple views are read together to reveal relational dynamics.

### 6.2 Response-Oriented Network

![Response-Oriented Network](response_oriented_network.png)

**File:** `response_oriented_network.png`

**Theoretical Foundation:**
The response-oriented network maps turns as relations, showing who orients to whom. Unlike frequency-based transition networks, this visualization weights edges by the duration of response chains, revealing who has the capacity to elicit extended uptake.

**Visualization Description:**
- **Nodes:** Speakers, sized by total speaking time
- **Edges:** Directed arrows showing response relationships (A → B means B responds to A)
- **Edge Thickness:** Proportional to average duration of response chains (capacity to elicit extended uptake)
- **Edge Color:** Intensity indicates frequency of responses (darker = more frequent)

**Interpretation:**
- **Thick edges** indicate speakers who elicit long response chains (conversational attractors)
- **Dense incoming edges** show speakers who receive many responses (high orientation)
- **Sparse incoming edges** indicate speakers who are ignored or marginalized
- **Directionality** reveals response patterns: who responds to whom

**Structural Features:**
- Speakers with many thick incoming edges are conversational attractors
- Speakers with sparse or thin incoming edges may be ignored or have limited capacity to elicit responses
- Asymmetric patterns reveal orientation asymmetries

### 6.3 Floor Holding with Interruption Attempts

![Floor Holding with Interruptions](floor_holding_interruptions.png)

**File:** `floor_holding_interruptions.png`

**Theoretical Foundation:**
Floor holding is visualized temporally through uninterrupted stretches, but crucially in relation to attempted interruptions. This reveals tolerance asymmetries: who maintains floor despite interruption attempts. Following Heritage's notion of turn design and repair, power appears in the ability to continue despite disruption.

**Visualization Description:**
- **Horizontal bars:** Floor holding episodes for each speaker
- **Red X markers:** Interruption attempts where floor was lost
- **Orange O markers:** Interruption attempts where floor was maintained (failed interruptions)
- **Bar length:** Duration of uninterrupted floor holding
- **Temporal axis:** Meeting time from start to end

**Interpretation:**
- **Orange markers** indicate interruption tolerance: speakers who maintain floor despite interruption attempts
- **Red markers** show interruption vulnerability: speakers who lose floor when interrupted
- **Long bars with orange markers** indicate strong floor-holding capacity despite challenges
- **Short bars with red markers** indicate fragile floor control

**Tolerance Asymmetries:**
- Speakers with many orange markers relative to red markers show high interruption tolerance
- This operationalizes power as the ability to continue despite disruption
- Reveals who has structural capacity to maintain floor in competitive environments

### 6.4 Interruption Tolerance Analysis

![Interruption Tolerance](interruption_tolerance.png)

**File:** `interruption_tolerance.png`

**Theoretical Foundation:**
Interruption tolerance is operationalized as who is interrupted without losing the floor, not who interrupts most. This directly aligns with Heritage's notion of turn design and repair, where power appears in the ability to continue despite disruption.

**Visualization Description:**
The figure contains two panels:

**Left Panel - Attempts vs. Maintenance:**
- **Red bars:** Interruption attempts received
- **Green bars:** Floor maintained despite interruptions
- **Comparison:** Shows absolute counts of attempts and successful floor maintenance

**Right Panel - Tolerance Rates:**
- **Horizontal bars:** Tolerance rate (floor maintained / attempts)
- **Color coding:** Green (>50%), Orange (25-50%), Red (<25%)
- **50% threshold line:** Reference for tolerance assessment

**Interpretation:**
- **High tolerance rates (>50%):** Speakers who maintain floor despite frequent interruption attempts
- **Low tolerance rates (<25%):** Speakers who lose floor when interrupted
- **Tolerance rate** operationalizes power as structural capacity to continue despite disruption

**Structural Implications:**
- Tolerance is not about interrupting others, but about maintaining floor when interrupted
- High tolerance indicates structural power in turn design and repair
- Low tolerance reveals vulnerability in competitive floor-taking environments

### 6.5 Conversational Attractors

![Conversational Attractors](conversational_attractors.png)

**File:** `conversational_attractors.png`

**Theoretical Foundation:**
Conversational attractors are speakers who elicit extended responses. This is measured by response chain duration, not just frequency. Attractors have the capacity to elicit extended uptake, operationalizing agenda setting as a structural feature rather than an inferred intention.

**Visualization Description:**
The figure contains two panels:

**Left Panel - Average Response Duration:**
- **Horizontal bars:** Average duration of response chains elicited by each speaker
- **Longer bars:** Speakers who elicit extended responses (strong attractors)
- **Shorter bars:** Speakers who elicit brief responses (weak attractors)

**Right Panel - Attractor Profile:**
- **Scatter plot:** Frequency vs. average duration
- **X-axis:** Number of responses received
- **Y-axis:** Average duration of response chains
- **Position:** Reveals attractor type (high frequency vs. high duration)

**Interpretation:**
- **High duration, high frequency:** Strong conversational attractors who consistently elicit extended responses
- **High duration, low frequency:** Selective attractors who elicit long responses when they do attract attention
- **Low duration, high frequency:** Frequent responders but brief responses (reactive, not attracting)
- **Low duration, low frequency:** Marginal participants

**Structural Features:**
- Attractors operationalize agenda setting as structural capacity to elicit extended uptake
- Duration-weighted measure captures quality of response, not just quantity
- Reveals who becomes a focal point for extended conversational engagement

### 6.6 Layered Reading of Power Patterns

**Power as Pattern Across Representations:**

Rather than collapsing dimensions into a composite score, power appears as a pattern across multiple layered views:

1. **Response-Oriented Network:** Who orients to whom, who becomes an attractor
2. **Floor Holding Timeline:** Who maintains floor despite interruption attempts
3. **Tolerance Rates:** Structural capacity to continue despite disruption
4. **Attractor Scores:** Capacity to elicit extended uptake

**Reading Patterns Together:**

- **High attractor score + High tolerance:** Structural power in both eliciting responses and maintaining floor
- **High tolerance + Low attractor score:** Power in maintaining floor but limited capacity to attract responses
- **Low tolerance + High attractor score:** Attracts responses but vulnerable to interruption
- **Low tolerance + Low attractor score:** Marginal participation

**Contingent and Relational:**

- Power is not a fixed attribute but appears moment-by-moment
- Patterns reveal relational dynamics, not individual characteristics
- Contingency: power depends on interactional context and response patterns

---

## 7. Topic Emergence Analysis: Topics as Emergent Interactional Objects

### 7.1 Analytic Stance

This analysis treats topics not as predefined themes but as **emergent interactional objects**. A topic exists only when it is taken up, resisted, redirected, or ignored by others. The task is to identify topic emergence and map how speakers orient to these topics over time.

**Key Principles:**

1. **Topics as Interactional Objects**: Topics exist only through interactional uptake, not as abstract concepts
2. **No Semantic Authority**: No assignment of semantic authority or correctness to any topic
3. **Observable Patterns**: All topic dynamics grounded in observable interaction patterns
4. **Agenda Setting as Uptake**: Agenda setting occurs only when others orient to the topic, not through initiation alone

### 7.2 Topic Emergence and Segmentation

**Topic Proposal Detection:**
- Candidate topic onsets identified as turns introducing new lexical clusters or conceptual frames
- Uses semantic similarity thresholds (TF-IDF + cosine similarity) rather than keywords
- Threshold: 0.25 similarity (below which a turn is considered a new topic proposal)
- Window size: 5 preceding turns for comparison

**Topic Stabilization:**
- A topic is considered stabilized only if at least one other speaker responds with semantic overlap
- Response threshold: 0.3 similarity (substantive response)
- Response window: 30 seconds after topic proposal
- Stabilization indicates successful topic adoption

**Topic Decay or Failure:**
- **Failed (silence)**: Topic followed by >5 seconds of silence
- **Failed (no uptake)**: Topic followed by responses but without semantic overlap
- Failure indicates lack of interactional uptake

### 7.3 Speaker Orientation to Topics

**Uptake Patterns:**
- Track which speakers respond to each topic
- Measure response delay (time between proposal and response)
- Measure response duration and semantic similarity
- Power indicated by whose topics attract uptake and whose do not

**Redirection and Reframing:**
- Detected when response has moderate semantic similarity (0.3-0.6)
- Indicates topic transformation rather than simple agreement
- Shows how topics are reshaped through interaction

**Topic Monopolization:**
- Identified when proposer extends own topic without others participating
- Ratio: proposer turns > 2x other speaker turns
- Distinguished from successful agenda control (which involves uptake)

### 7.4 Relating Topics to Interactional Power

**Agenda Setting as Uptake, Not Initiation:**
- Topic introduction alone does not equal power
- Agenda setting occurs only when others orient to the topic
- Stabilized topics indicate successful agenda setting
- Failed topics indicate lack of agenda-setting capacity

**Resistance and Silence as Signals:**
- Lack of uptake = interactional response (not absence of response)
- Delayed response = interactional signal
- Abrupt topic shifts = interactional response
- All must be visualized as interactional patterns

**Coupling Topics and Turn Structure:**
- Topic boundaries overlaid onto turn sequences
- Shows how interactional power fluctuates with thematic control
- Reveals relationship between topic control and floor control

### 7.5 Topic Analysis Results

![Topic Timeline](topic_timeline.png)

**File:** `topic_timeline.png`

**Visualization Description:**
- **Y-axis:** Topics (labeled with topic ID and proposer)
- **X-axis:** Meeting time (seconds)
- **Bars:** Topic duration (from proposal to end)
- **Colors:**
  - **Green:** Stabilized topics (uptake received)
  - **Orange:** Failed topics (no semantic uptake)
  - **Red:** Failed topics (silence)
- **Blue stars:** First response time (for stabilized topics)

**Interpretation:**
- Green bars indicate successful topic adoption (agenda setting through uptake)
- Orange/red bars indicate failed topic proposals (lack of uptake)
- Star markers show response timing (delayed vs. immediate)
- Temporal distribution reveals when topics emerge and how long they persist

### 7.6 Speaker-Topic Network

![Speaker-Topic Network](speaker_topic_network.png)

**File:** `speaker_topic_network.png`

**Visualization Description:**
- **Bipartite graph:** Links speakers (circles) to topics (squares)
- **Left side:** Speakers (node size = speaking time)
- **Right side:** Topics (colored by status)
- **Blue edges:** Topic proposal relationships
- **Green dashed edges:** Response relationships (weighted by similarity)
- **Topic colors:**
  - Green = Stabilized
  - Orange = Failed (no uptake)
  - Red = Failed (silence)

**Interpretation:**
- Dense connections indicate speakers with many topic proposals or responses
- Green edges (responses) show uptake patterns
- Isolated topics indicate lack of uptake
- Network structure reveals who's topics attract orientation and whose do not

### 7.7 Topic Trajectories

![Topic Trajectories](topic_trajectories.png)

**File:** `topic_trajectories.png`

**Visualization Description:**
- Multiple timeline views (one per stabilized topic)
- Shows how topics travel between speakers
- **Bars:** Speaker turns related to topic
- **Y-axis:** Speakers participating in topic
- **X-axis:** Time

**Interpretation:**
- Shows topic movement: does it travel between speakers or stall with proposer?
- Reveals topic monopolization vs. shared engagement
- Temporal patterns show topic lifecycle and speaker participation

### 7.8 Topic Emergence Metrics

**Overall Statistics:**
- Total topics detected: Based on semantic similarity threshold (0.25)
- Stabilized topics: Topics with uptake (agenda setting success)
- Failed topics: Topics without uptake (agenda setting failure)
  - Failed (silence): Followed by >5 seconds of silence
  - Failed (no uptake): Followed by responses but without semantic overlap

**Speaker-Level Metrics:**
- **Topics Proposed:** Number of topic proposals per speaker
- **Stabilization Rate:** Percentage of proposals that receive uptake
- **Response Patterns:** Which speakers respond to which topics
- **Uptake Delays:** Time between proposal and response
- **Redirections:** Cases of topic transformation (moderate similarity: 0.3-0.6)
- **Monopolizations:** Topics extended without others (proposer turns > 2x others)

**Power Indicators:**
- **High stabilization rate:** Successful agenda setting (topics attract uptake)
- **Low stabilization rate:** Failed agenda setting (topics ignored)
- **Many responses received:** Topics that attract orientation
- **Few responses received:** Topics that are ignored or resisted

**Agenda Setting as Uptake:**
- Topic introduction alone does not equal power
- Agenda setting occurs only when others orient to the topic
- Stabilized topics = successful agenda setting (interactional success)
- Failed topics = failed agenda setting (lack of interactional uptake)
- Power measured by whose topics attract orientation, not just who proposes

### 7.9 Topic Content Analysis

**Full Content Report:**
A detailed content analysis file (`topic_content_analysis.txt`) provides complete topic texts and all speaker responses for all 152 detected topics. This includes:

- **Full Topic Text:** Complete content of each topic proposal (not truncated)
- **All Responses:** Every response to each topic, including:
  - Full response text
  - Speaker identity
  - Response timing and delay
  - Semantic similarity scores
  - Uptake status (whether response met similarity threshold)
- **Speaker Engagement Summary:** Per-speaker statistics on topic proposals and stabilization rates

**Content Analysis Reveals Power Positions:**

1. **Stabilized Topics Show Successful Agenda Setting:**
   - **TOPIC_17 (SPEAKER_19):** "The thing is, we sat down last week, a bunch of us, like, a bunch of people that were there, because of the leak and the stuff that happened, like, we just opened the bank account to see how much we have to handle this, further stuff that might happen and whatnot. And the bank is, like, it's not in a good shape."
     - **Uptake:** SPEAKER_18 responded with 0.337 similarity after 28 seconds
     - **Power Indicator:** SPEAKER_19 successfully set agenda about financial/bureaucratic concerns
   
   - **TOPIC_80 (SPEAKER_20):** "It has its own problems."
     - **Uptake:** SPEAKER_05 responded with 0.335 similarity after 3 seconds
     - **Power Indicator:** SPEAKER_20's brief topic attracted immediate uptake
   
   - **TOPIC_100 (SPEAKER_17):** "I don't know if you have to be a citizen to be a member of the Muta."
     - **Uptake:** SPEAKER_15 responded with 0.545 similarity after 5.91 seconds
     - **Power Indicator:** SPEAKER_17's procedural question received high semantic overlap

2. **Failed Topics Reveal Lack of Agenda Setting Power:**
   - **SPEAKER_09:** 20 topics proposed, 0 stabilized (0% success rate)
     - Despite high speaking time (18.9%), topics fail to attract uptake
     - Power position: High participation but low agenda-setting capacity
   
   - **SPEAKER_18:** 17 topics proposed, 0 stabilized (0% success rate)
     - Second-highest speaking time (15.9%) but topics ignored
     - Power position: Dominant speaker but topics don't attract orientation
   
   - **SPEAKER_19:** 16 topics proposed, 1 stabilized (6.2% success rate)
     - Only speaker with successful stabilization among high-participation speakers
     - Power position: Moderate agenda-setting capacity

3. **Response Patterns Show Power Relations:**
   - **Non-Uptake Responses:** Many responses occur but without semantic overlap
     - Example: TOPIC_1 received response from UNKNOWN with 0.000 similarity
     - Indicates topic was addressed but not taken up (resistance or redirection)
   
   - **Silence as Response:** 7 topics followed by >5 seconds of silence
     - Indicates topics that are completely ignored
     - Strong signal of lack of agenda-setting power

4. **Topic Content Themes:**
   - Financial/bureaucratic concerns (bank account, NGO structure)
   - Procedural questions (membership requirements, convening procedures)
   - Government/municipality relations
   - Organizational structure and decision-making
   - Historical context (NGO closures, political changes)

**Power Position Analysis Through Content:**

- **High Speaking Time + Low Stabilization = Dominant but Not Influential:**
  - SPEAKER_09 and SPEAKER_18 speak frequently but their topics don't attract uptake
  - Suggests they hold floor but don't control agenda
  
- **Low Speaking Time + High Stabilization = Strategic Agenda Setting:**
  - SPEAKER_17 and SPEAKER_20 have few topics but achieve stabilization
  - Suggests strategic topic selection or timing
  
- **Content Analysis Reveals:**
  - **What topics succeed:** Procedural questions, concrete concerns (bank account), organizational structure
  - **What topics fail:** Abstract discussions, personal experiences without clear connection
  - **Who responds:** Even failed topics receive responses, but without semantic uptake
  - **Response timing:** Successful topics receive faster responses (3-28 seconds vs. longer delays)

### 7.10 Fine-Grained Topic-Speaker Relations: Power as Interactional Structure

Beyond uptake and response duration, several finer-grained topic-speaker relations expose power as an **interactional structure** rather than a semantic property. This analysis examines four key phenomena that reveal power through conversational structure.

#### 7.10.1 Topic Closure Authority

**Power is visible in who can end topics without contest.** When a speaker shifts away from an ongoing theme and others follow without repair or resistance, this indicates a capacity to delimit relevance.

**Key Findings:**
- **145 topic closures detected** across the meeting
- **128 uncontested closures** (88.3%) - others followed without repair
- **SPEAKER_19:** 100% uncontested closure rate (12/12 closures)
- **SPEAKER_02:** 92.9% uncontested closure rate (13/14 closures)
- **SPEAKER_09:** 83.3% uncontested closure rate (20/24 closures) - highest volume

**Power Insight:** High uncontested closure rates indicate speakers who can reorganize the participation framework by shifting topics. This is structural power - the capacity to delimit what is relevant, not just semantic authority.

#### 7.10.2 Asymmetric Topical Accountability

**Uneven demand for clarification/justification signals differential epistemic standing.** Some speakers are routinely asked to clarify, justify, or provide evidence, while others are not.

**Key Findings:**
- **SPEAKER_03:** Highest accountability rate (1.00 demands per topic)
  - 4 topics proposed, 4 justification requests
  - Routinely asked to justify positions
  
- **SPEAKER_26:** High accountability rate (0.67 demands per topic)
  - 3 topics proposed, 2 justification requests
  
- **SPEAKER_09:** Zero accountability demands (0.00 per topic)
  - 20 topics proposed, 0 clarification/justification requests
  - **Power indicator:** Topics accepted without challenge
  
- **SPEAKER_19:** Zero accountability demands (0.00 per topic)
  - 16 topics proposed, 0 accountability demands
  - **Power indicator:** Epistemic authority - topics not questioned

**Power Insight:** Low accountability rates indicate epistemic authority - speakers whose topics are accepted without challenge. High accountability rates indicate lower epistemic standing - speakers who must justify their contributions.

#### 7.10.3 Topic Recycling

**Power appears when topics initially ignored gain traction after reintroduction by different speaker.** Authority is relational rather than propositional - the same theme acquires force through speaker position change.

**Key Findings:**
- **0 topic recycling cases detected** in this meeting
- This suggests topics are either taken up immediately or permanently ignored
- No evidence of topics gaining traction through speaker change

**Interpretation:** The absence of topic recycling may indicate:
- Topics are evaluated on content alone, not speaker position
- OR: Speaker positions are relatively stable (no clear hierarchy where same topic succeeds when repositioned)

#### 7.10.4 Topic Hijacking vs Alignment

**Reframing topics while preserving legitimacy exercises subtle control over meaning.** This aligns with Goffman's footing shifts - repositioning within interaction without overt interruption.

**Key Findings:**
- **205 total topic responses analyzed**
- **3 hijacking/reframing cases** (0.3-0.6 similarity)
  - Subtle control: reframing while preserving semantic connection
- **202 complete shifts** (<0.3 similarity)
  - Topics ignored or completely redirected
- **0 alignment cases** (>0.6 similarity)
  - No cases of maintaining topic frame

**Topic Control Patterns:**
- **SPEAKER_18:** 1 hijacking/reframing, 15 complete shifts
- **SPEAKER_19:** 1 hijacking/reframing, 3 complete shifts
- **SPEAKER_25:** 1 hijacking/reframing, 5 complete shifts
- **SPEAKER_09:** 0 hijacking, 32 complete shifts (most shifts)

**Power Insight:** Hijacking/reframing (moderate similarity) shows subtle control - repositioning meaning while maintaining conversational legitimacy. Complete shifts show topics being ignored or redirected. The rarity of hijacking (only 3 cases) suggests most responses either align completely or shift completely.

**Example of Hijacking/Reframing:**
- **TOPIC_19** (SPEAKER_02): Bank account/financial concerns
- **Hijacked by SPEAKER_18:** Reframed while preserving legitimacy
- **Similarity:** 0.3-0.6 range
- **Power:** Subtle control over meaning without overt interruption

### 7.11 Topic Analysis Summary

**Key Findings:**
- **152 topics detected** across the meeting
- **Only 3 topics stabilized** (2.0% stabilization rate)
- **142 topics failed without uptake** (93.4%)
- **7 topics failed with silence** (4.6%)

**Power Position Insights:**
- Most topics fail to stabilize, indicating highly competitive or fragmented discourse
- High-participation speakers (SPEAKER_09, SPEAKER_18) have 0% stabilization rates
- Low-participation speakers (SPEAKER_17, SPEAKER_20) achieve stabilization
- **Agenda setting is decoupled from speaking time dominance**

**Content Analysis Reveals:**
- Successful topics: Concrete, procedural, organizational concerns
- Failed topics: Abstract, personal, or disconnected from group focus
- Response patterns: Even failed topics receive responses, but without semantic uptake
- Power is revealed through **whose topics attract semantic orientation**, not just who speaks most

**Methodological Note:**
- Similarity thresholds (0.25 for proposals, 0.3 for stabilization) are structural parameters
- Full content analysis available in `topic_content_analysis.txt`
- Content analysis shows power as **agenda-setting capacity through uptake**, not speaking time

---

## 8. Integrated Power Structure Analysis

### 6.1 Multi-Metric Speaker Profiles

**SPEAKER_09 - High Participation Profile:**
- Speaking time: 18.9% (highest)
- Turn count: 33 (highest)
- Average turn length: 41.81s (sustained floor-holding)
- Interruptions: 17 initiated, 17 received (competitive)
- Agenda control: 5 introductions (high)
- **Profile:** Primary participant with extensive floor control, high interruption activity, and significant agenda-setting capability

**SPEAKER_18 - High Participation Profile:**
- Speaking time: 15.9% (second highest)
- Turn count: 27 (second highest)
- Average turn length: 43.69s (longest sustained turns)
- Interruptions: 13 initiated, 17 received (frequently interrupted)
- Agenda control: 5 introductions (high)
- **Profile:** Primary participant with longest turn-holding capability, mutual competitive relationship with SPEAKER_09

**SPEAKER_25 - High Participation Profile:**
- Speaking time: 12.6% (third highest)
- Turn count: 24 (third highest)
- Average turn length: 41.24s (sustained floor-holding)
- Interruptions: 12 initiated, 12 received (balanced)
- Agenda control: 4 introductions (moderate-high)
- **Profile:** Primary participant with balanced interruption patterns and strong floor-holding

**SPEAKER_19 - Moderate-High Participation, High Activity:**
- Speaking time: 5.8% (moderate)
- Turn count: 22 (high frequency)
- Average turn length: 19.09s (moderate)
- Interruptions: 16 initiated, 11 received (assertive)
- Agenda control: 3 introductions (moderate)
- **Profile:** Active participant with high interruption activity relative to speaking time, suggesting reactive or interjectory participation style

**SPEAKER_07 - Low Participation, High Activity:**
- Speaking time: 1.7% (low)
- Turn count: 21 (high frequency)
- Average turn length: 5.66s (very short)
- Interruptions: 12 initiated, 16 received (high activity, frequently interrupted)
- Agenda control: 4 introductions (high relative to speaking time)
- **Profile:** Frequent but brief participation, high interruption activity, strategic topic introduction despite low overall speaking time

### 6.2 Power Structure Typology

Based on integrated metrics, speakers can be categorized into structural roles:

**Type 1: Primary Floor Holders**
- High speaking time, long turns, high agenda control
- Examples: SPEAKER_09, SPEAKER_18, SPEAKER_25
- Characteristics: Sustained monologues, topic introduction, competitive interruption patterns

**Type 2: Active Interlocutors**
- Moderate speaking time, moderate turn length, moderate agenda control
- Examples: SPEAKER_02, SPEAKER_19, SPEAKER_01
- Characteristics: Regular participation, balanced turn-taking, some topic introduction

**Type 3: Reactive Participants**
- Low-moderate speaking time, short turns, low agenda control
- Examples: SPEAKER_07, SPEAKER_05, SPEAKER_03
- Characteristics: Frequent brief contributions, high interruption activity, minimal topic introduction

**Type 4: Peripheral Participants**
- Low speaking time, few turns, no agenda control
- Examples: SPEAKER_16, SPEAKER_21, SPEAKER_17
- Characteristics: Minimal participation, brief contributions, no topic introduction

### 6.3 Interactional Hierarchies

**Hierarchy Level 1 - Core Participants:**
- SPEAKER_09, SPEAKER_18, SPEAKER_25
- Control 47.4% of speaking time
- Account for 31% of topic introductions
- Engage in competitive interruption patterns with each other

**Hierarchy Level 2 - Supporting Participants:**
- SPEAKER_02, SPEAKER_19, SPEAKER_01, SPEAKER_11, SPEAKER_00, SPEAKER_13, SPEAKER_22, SPEAKER_20
- Control 27.3% of speaking time
- Moderate participation with some agenda control
- Engage with core participants

**Hierarchy Level 3 - Marginal Participants:**
- Remaining 16 speakers
- Control 10.6% of speaking time
- Minimal agenda control
- Peripheral to main interaction network

---

## 8. Structural Patterns and Relationships

### 7.1 Correlation Patterns

**Speaking Time vs. Turn Count:**
- Strong positive correlation (r ≈ 0.85)
- High-participation speakers have both many turns and long turns

**Speaking Time vs. Agenda Control:**
- Moderate positive correlation (r ≈ 0.75)
- High-participation speakers tend to introduce more topics, but exceptions exist (SPEAKER_07)

**Interruption Activity vs. Speaking Time:**
- Moderate positive correlation (r ≈ 0.60)
- High-participation speakers show more interruption activity, but some low-participation speakers also show high interruption rates (SPEAKER_07)

**Turn Length vs. Turn Count:**
- Negative correlation (r ≈ -0.40)
- Speakers with many turns tend to have shorter average turn lengths (reactive pattern)
- Speakers with few turns tend to have longer average turn lengths (monologic pattern)

### 7.2 Asymmetry Patterns

**Speaking Time Asymmetry:**
- Top 3 speakers: 47.4% of time
- Bottom 11 speakers: 3.2% of time combined
- **Asymmetry ratio:** 14.8:1

**Turn-Taking Asymmetry:**
- Top 3 speakers: 84 turns (32% of all turns)
- Bottom 11 speakers: 28 turns (11% of all turns)
- **Asymmetry ratio:** 3:1

**Agenda Control Asymmetry:**
- Top 3 speakers: 14 introductions (31% of all introductions)
- Bottom 11 speakers: 5 introductions (11% of all introductions)
- **Asymmetry ratio:** 2.8:1

### 7.3 Network Centrality Patterns

Based on transition patterns:
- **Core-periphery structure:** Dense connections among high-participation speakers, sparse connections to low-participation speakers
- **Hub speakers:** SPEAKER_09, SPEAKER_18, SPEAKER_25 function as interaction hubs
- **Bridge speakers:** Some moderate-participation speakers may bridge between core and periphery

---

## 9. Temporal Analysis

### 8.1 Speaking Activity Timeline

![Speaking Activity Timeline](speaking_timeline.png)

The speaking timeline visualization reveals temporal patterns of participation across the meeting duration. This analysis tracks when each speaker was active, showing the distribution of speaking episodes over time.

**Visualization Description:**
The timeline chart displays a horizontal bar chart where:
- **Y-axis:** Lists the top 10 speakers ranked by total speaking time
- **X-axis:** Represents meeting time from start (0 seconds) to end (6,855 seconds)
- **Bars:** Each colored bar segment represents a speaking episode for that speaker
- **Bar length:** Proportional to the duration of that speaking episode
- **Color coding:** Each speaker has a distinct color for easy identification

The visualization shows when speakers were active throughout the meeting, revealing patterns of sustained participation versus episodic engagement.

**Key Temporal Patterns:**

**Sustained Participation:**
- **SPEAKER_09, SPEAKER_18, SPEAKER_25** show continuous activity throughout the meeting
- These speakers maintain presence across multiple time periods
- Activity patterns suggest ongoing engagement rather than concentrated bursts

**Episodic Participation:**
- Some speakers show concentrated activity in specific time windows
- **SPEAKER_07** demonstrates frequent but brief episodes (consistent with high turn count, short duration pattern)
- Peripheral speakers show isolated activity periods

**Temporal Gaps:**
- Periods of low activity may indicate:
  - Topic transitions
  - Listening phases
  - Procedural pauses
  - Side conversations or non-verbal interactions

### 8.2 Cumulative Speaking Time

![Cumulative Speaking Time](cumulative_speaking_time.png)

The cumulative speaking time chart tracks how speaking time accumulates for the top 8 speakers over the meeting duration.

**Visualization Description:**
The line chart displays:
- **X-axis:** Meeting time from start to end (0 to 6,855 seconds)
- **Y-axis:** Cumulative speaking time in seconds
- **Lines:** Each colored line represents one of the top 8 speakers
- **Line slope:** Steep slopes indicate periods of concentrated speaking; flat segments indicate absence from the floor
- **Legend:** Identifies each speaker's line color

The visualization reveals how speaking time accumulates over the meeting, showing whether participation was steady, episodic, or concentrated in specific periods. Early divergence between lines indicates early establishment of participation hierarchy, while parallel lines suggest similar participation rates.

**Accumulation Patterns:**

**Linear Accumulation:**
- Speakers with consistent participation show steady, linear accumulation
- **SPEAKER_09** and **SPEAKER_18** show near-linear growth, indicating sustained participation

**Accelerated Periods:**
- Steep slopes indicate periods of concentrated speaking
- May correspond to extended monologues or active debate participation

**Plateau Periods:**
- Flat periods indicate absence from the floor
- Duration of plateaus reveals periods of non-participation

**Divergence Analysis:**
- Early divergence between speakers indicates early establishment of participation hierarchy
- Late convergence suggests some speakers gain floor access later in the meeting

### 8.3 Participation Heatmap

![Participation Heatmap](participation_heatmap.png)

The participation heatmap divides the meeting into 20 temporal segments and shows speaking time per segment for each speaker.

**Visualization Description:**
The heatmap displays:
- **Rows:** Top 15 speakers ranked by total speaking time
- **Columns:** 20 time segments dividing the meeting chronologically
- **Cell color intensity:** Darker colors indicate more speaking time in that segment
- **Color scale:** Yellow to orange to red gradient (YlOrRd colormap)
- **Cell values:** Numeric values show exact speaking time in seconds per segment

The visualization reveals temporal distribution of participation, showing when each speaker was most active. Darker horizontal bands indicate speakers with consistent participation, while scattered dark cells show episodic participation patterns. Vertical patterns reveal periods of high overall activity versus quieter segments.

**Temporal Concentration:**

**Consistent Participation:**
- Top speakers show activity across most segments
- **SPEAKER_09, SPEAKER_18, SPEAKER_25** maintain presence throughout

**Segmented Participation:**
- Some speakers show activity concentrated in specific segments
- May indicate topic-specific contributions or strategic timing

**Participation Density:**
- Darker cells indicate higher speaking time in that segment
- Reveals when each speaker was most active
- Identifies periods of high/low overall activity

**Temporal Clustering:**
- Clusters of high activity may indicate:
  - Extended exchanges between specific speakers
  - Topic-focused discussion periods
  - Debate phases with high interaction

---

## 10. Turn Length Distribution Analysis

### 9.1 Overall Distribution

![Turn Length Distribution](turn_length_distribution.png)

The turn length distribution histogram reveals the statistical properties of turn-taking behavior across all speakers.

**Visualization Description:**
The figure contains two panels:

**Left Panel - Overall Distribution Histogram:**
- **X-axis:** Turn length in seconds (binned into 50 intervals)
- **Y-axis:** Frequency (number of turns in each bin)
- **Bars:** Blue bars showing the distribution of all turn lengths across all speakers
- **Red dashed line:** Median turn length (approximately 20-25 seconds)
- **Green dashed line:** Mean turn length (higher than median, indicating right-skew)

**Right Panel - Box Plot Comparison:**
- **Y-axis:** Top 10 speakers ranked by total speaking time
- **X-axis:** Turn length in seconds
- **Box plots:** Each box shows:
  - Median turn length (center line)
  - Interquartile range (box boundaries)
  - Outliers (individual points beyond whiskers)
- **Comparison:** Allows direct comparison of turn length distributions across speakers

The visualization reveals that most turns are relatively brief, with a right-skewed distribution indicating that a small number of extended turns account for substantial floor time. The box plots show distinct speaking styles ranging from brief interjections to extended monologues.

**Distribution Characteristics:**

**Median Turn Length:** Approximately 20-25 seconds (varies by calculation method)
**Mean Turn Length:** Higher than median, indicating right-skewed distribution
**Distribution Shape:** Right-skewed with many short turns and fewer long turns

**Interpretation:**
- Most turns are relatively brief
- Long turns are less common but contribute significantly to total speaking time
- Skewness indicates that a small number of extended turns account for substantial floor time

### 9.2 Speaker-Specific Turn Length Patterns

The box plot component shows turn length distributions for the top 10 speakers, revealing distinct speaking styles:

**Long Turn Speakers:**
- **SPEAKER_18:** Longest median turn length (43.69s), consistent with sustained floor-holding
- **SPEAKER_11:** High median (43.25s) despite low turn count, indicating monologic style
- **SPEAKER_09, SPEAKER_25:** Moderate-long turns (41-42s median)

**Short Turn Speakers:**
- **SPEAKER_07:** Very short median (5.66s), consistent with reactive/interjectory pattern
- **SPEAKER_08:** Extremely short turns (4.38s median)
- **SPEAKER_15:** Brief turns (5.93s median)

**Variable Turn Length Speakers:**
- Wide interquartile ranges indicate high variance in turn length
- May suggest adaptive speaking style or context-dependent turn-taking

### 9.3 Turn Length Variance

**High Variance Speakers:**
- Speakers with wide box plots show inconsistent turn lengths
- May indicate:
  - Context-dependent participation
  - Mix of brief interjections and extended contributions
  - Adaptive interactional style

**Low Variance Speakers:**
- Narrow box plots indicate consistent turn length
- Suggests:
  - Predictable participation pattern
  - Consistent speaking style
  - Stable interactional role

---

## 11. Interruption Network Analysis

### 10.1 Network Structure

![Interruption Network](interruption_network.png)

The interruption network isolates interruption patterns from general interaction, creating a focused view of competitive floor-taking behavior.

**Visualization Description:**
The directed network graph displays:
- **Nodes (circles):** Each node represents a speaker
  - **Node size:** Proportional to total interruption activity (interruptions initiated + interruptions received)
  - **Node color:** Light coral/red, indicating competitive interaction
  - **Node labels:** Speaker identifiers
- **Edges (arrows):** Directed edges represent interruption relationships
  - **Edge direction:** Arrow points from interrupter to interrupted speaker
  - **Edge thickness:** Proportional to frequency of interruptions between that pair
  - **Edge color:** Dark red, emphasizing competitive nature
- **Layout:** Spring layout algorithm positions nodes to minimize edge crossings

The visualization reveals competitive relationships, with thicker edges indicating frequent interruption pairs. Large nodes indicate speakers heavily involved in interruption dynamics (both initiating and receiving). Dense connections show competitive dyads, while isolated nodes indicate speakers with minimal interruption activity.

**Network Characteristics:**

**Node Size:** Represents total interruption activity (initiated + received)
- Larger nodes indicate speakers with high interruption involvement
- **SPEAKER_09, SPEAKER_18** show largest nodes, indicating central role in interruption dynamics

**Edge Direction:** Indicates interruption direction
- Edge from A to B: A interrupts B
- Thickness indicates frequency of interruption

**Edge Density:** Reveals interruption relationships
- Dense connections indicate competitive dyads
- Sparse connections indicate minimal interruption interaction

### 10.2 Interruption Hubs

**High Activity Interrupters:**
- **SPEAKER_09:** 17 interruptions initiated, 17 received (balanced competitive pattern)
- **SPEAKER_19:** 16 initiated, 11 received (assertive pattern)
- **SPEAKER_02:** 13 initiated, 7 received (assertive pattern)
- **SPEAKER_18:** 13 initiated, 17 received (frequently interrupted)

**Interruption Recipients:**
- **SPEAKER_18, SPEAKER_09:** Both show high interruption reception (17 each)
- Indicates these speakers are frequent targets of interruption attempts
- May suggest:
  - Extended turns that invite interruption
  - Competitive floor control
  - High-stakes contributions

### 10.3 Competitive Dyads

**Mutual High Interruption:**
- **SPEAKER_09 ↔ SPEAKER_18:** Both interrupt each other frequently
- Indicates competitive relationship for floor control
- Suggests direct competition between primary participants

**Asymmetric Patterns:**
- Some speakers interrupt more than they are interrupted (assertive)
- Others are interrupted more than they interrupt (reactive or targeted)
- Reveals power dynamics in interruption behavior

### 10.4 Structural Implications

**Interruption as Floor Control:**
- High interruption activity correlates with high speaking time
- Suggests interruption is a mechanism for floor access
- Competitive interruption patterns indicate contested floor control

**Marginal Speakers:**
- Low interruption activity among peripheral speakers
- Suggests limited engagement in competitive floor-taking
- May indicate:
  - Passive participation style
  - Lack of floor access opportunities
  - Different interactional strategy

---

## 12. Gap Analysis

### 11.1 Gap Distribution

![Gap Analysis](gap_analysis.png)

The gap analysis examines silence periods between utterances, revealing the rhythm and pacing of turn-taking.

**Visualization Description:**
The figure contains two panels:

**Left Panel - Gap Distribution Histogram:**
- **X-axis:** Gap duration in seconds (binned into 50 intervals)
- **Y-axis:** Frequency (number of gaps in each bin)
- **Bars:** Blue bars showing the distribution of all gaps between utterances
- **Red dashed line:** Median gap duration (0.34 seconds)
- **X-axis limit:** Focused on most common gaps (0-10 seconds) for clarity
- **Distribution shape:** Highly right-skewed, with most gaps being very brief

**Right Panel - Gap Type Comparison:**
- **X-axis categories:** "Same Speaker" and "Speaker Change"
- **Y-axis:** Gap duration in seconds
- **Box plots:** Two box plots comparing:
  - Gaps within the same speaker's turn (same speaker)
  - Gaps between different speakers (speaker change)
- **Comparison:** Reveals that speaker changes have slightly longer gaps (0.36s median) than same-speaker gaps (0.34s median)

The visualization reveals the rapid pace of conversation, with median gaps under 0.5 seconds indicating fast turn-taking. The right-skewed distribution shows that while most gaps are brief, occasional longer gaps occur (likely topic transitions or thinking pauses).

**Overall Gap Statistics:**
- **Median Gap:** 0.34 seconds
- **Mean Gap:** 0.77 seconds
- **Distribution:** Highly right-skewed (many short gaps, few long gaps)

**Interpretation:**
- Very rapid turn-taking overall
- Median gap of 0.34s indicates conversation proceeds with minimal pause
- Mean > median indicates some longer gaps (silence periods, topic transitions)

### 11.2 Gap Types

**Same Speaker Gaps:**
- **Median:** 0.34 seconds
- Gaps within the same speaker's turn
- Typically brief, indicating continuous speech with minimal pauses
- May include:
  - Natural speech pauses
  - Thinking pauses
  - Emphasis pauses

**Speaker Change Gaps:**
- **Median:** 0.36 seconds
- Gaps between different speakers
- Slightly longer than same-speaker gaps
- Indicates rapid turn-taking with minimal silence
- Very short gaps (<0.5s) classified as potential interruptions

### 11.3 Turn-Taking Rhythm

**Rapid Turn-Taking:**
- Median gaps <0.5s indicate fast-paced conversation
- Suggests:
  - High engagement
  - Competitive floor-taking
  - Minimal hesitation in turn-taking

**Longer Gaps:**
- Gaps >2 seconds may indicate:
  - Topic transitions
  - Thinking periods
  - Procedural pauses
  - Non-verbal communication
  - Side conversations

**Gap Distribution:**
- Most gaps are very short (<1 second)
- Long gaps (>5 seconds) are rare
- Indicates sustained conversation flow with minimal extended silence

### 11.4 Structural Implications

**Conversation Pace:**
- Rapid turn-taking suggests high-stakes, competitive interaction
- Minimal silence indicates active engagement
- Fast pace may limit opportunities for reflection or planning

**Floor Access:**
- Short gaps between speaker changes indicate:
  - Quick response times
  - Competitive floor-taking
  - Limited hesitation in participation

**Silence Patterns:**
- Longer gaps (>2s) used for topic introduction (agenda control)
- Brief gaps indicate continuous exchange
- Gap analysis reveals conversation rhythm and pacing

---

## 13. Inequality Metrics and Quantification

### 12.1 Gini Coefficient

The Gini coefficient provides a quantitative measure of speaking time inequality.

**Gini Coefficient:** -0.656

**Interpretation Note:** The negative value suggests a calculation artifact or requires methodological review. Typically, Gini coefficients range from 0 (perfect equality) to 1 (maximum inequality). However, the magnitude indicates significant inequality regardless of sign.

**Structural Inequality:**
- High absolute value indicates substantial inequality
- Top speakers control disproportionate share of speaking time
- Consistent with observed 47.4% concentration among top 3 speakers

### 12.2 Concentration Metrics

**Top 10% Share:** 40.9%
- Top 3 speakers (approximately 10% of participants) control 40.9% of speaking time
- Indicates high concentration of participation

**Top 3 Share:** 55.7%
- Top 3 speakers control 55.7% of speaking time
- Nearly 4x their proportional share (3/27 = 11.1%)
- Concentration ratio: 5.0:1

### 12.3 Entropy Analysis

**Shannon Entropy:** 3.60 bits
**Maximum Possible Entropy:** 4.75 bits (for 27 speakers)
**Normalized Entropy:** 0.758

**Interpretation:**
- Normalized entropy of 0.758 indicates moderate inequality
- Value closer to 1.0 would indicate more equal distribution
- Value closer to 0.0 would indicate maximum concentration
- 0.758 suggests:
  - Significant but not extreme inequality
  - Some participation diversity
  - Concentration among top speakers but not complete marginalization

**Entropy vs. Gini:**
- Entropy captures distribution shape differently than Gini
- Both metrics indicate substantial but not extreme inequality
- Consistent with observed three-tier hierarchy

### 12.4 Lorenz Curve

![Inequality Lorenz Curve](inequality_lorenz_curve.png)

The Lorenz curve visualizes cumulative speaking time distribution against cumulative speaker proportion.

**Visualization Description:**
The Lorenz curve displays:
- **X-axis:** Cumulative proportion of speakers (0.0 to 1.0, or 0% to 100%)
- **Y-axis:** Cumulative proportion of speaking time (0.0 to 1.0, or 0% to 100%)
- **Blue solid line:** Actual distribution of speaking time (Lorenz curve)
  - Shows how cumulative speaking time accumulates as speakers are added
  - Steep initial rise indicates top speakers control large share
  - Flattening indicates marginal speakers contribute little
- **Red dashed line:** Perfect equality line (diagonal)
  - Represents hypothetical equal distribution where each speaker has equal time
  - Serves as reference for measuring inequality
- **Shaded area:** Area between actual curve and equality line
  - Represents the magnitude of inequality
  - Larger area = greater inequality
- **Text annotation:** Displays Gini coefficient value (0.656) in a highlighted box

The visualization provides both visual and quantitative representation of inequality. The greater the deviation from the diagonal, the more unequal the distribution. The curve shape reveals the three-tier hierarchy, with steep initial rise (top tier), moderate middle section (middle tier), and flat tail (marginal tier).

**Curve Characteristics:**

**Deviation from Equality:**
- Significant deviation from perfect equality line (diagonal)
- Indicates substantial inequality
- Area between curve and equality line represents inequality magnitude

**Curve Shape:**
- Steep initial rise indicates top speakers control large share
- Flattening indicates marginal speakers contribute little
- Shape consistent with three-tier hierarchy

**Gini Coefficient Display:**
- Curve annotated with Gini coefficient value
- Provides visual and quantitative measure of inequality

### 12.5 Structural Inequality Summary

**Quantitative Measures:**
- **Top 3 Share:** 55.7% (5.0x proportional share)
- **Top 10% Share:** 40.9% (4.1x proportional share)
- **Normalized Entropy:** 0.758 (moderate inequality)
- **Gini (absolute):** 0.656 (high inequality)

**Qualitative Pattern:**
- Clear three-tier hierarchy
- Concentration among top speakers
- Significant marginalization of bottom tier
- Moderate overall inequality (not extreme concentration)

**Comparison to Perfect Equality:**
- If perfectly equal: each speaker would have 3.7% of speaking time
- Top 3 speakers have 15.7x, 13.2x, and 10.1x their equal share
- Bottom 11 speakers have <0.3x their equal share

---

## 14. Methodological Considerations

### 13.1 Operationalization Decisions

**Speaking Time Calculation:**
- Excludes filler tokens to focus on substantive contributions
- Uses segment-level timestamps for accuracy
- Handles missing speaker labels by extracting from word-level data

**Interruption Detection:**
- Threshold: 0.5 seconds (structural proxy, not semantic interpretation)
- Does not distinguish between cooperative and competitive interruptions
- May include natural turn-taking transitions

**Agenda Control:**
- Threshold: 2 seconds of silence before topic introduction
- Pragmatic definition based on conversational structure
- May miss topic shifts within continuous speech

**Turn-Taking:**
- Treats consecutive segments by same speaker as continuous turns
- May overestimate turn length for speakers with fragmented speech
- Accurately captures floor-holding behavior

### 13.2 Limitations

1. **Temporal Resolution:** Word-level timestamps provide high resolution, but some overlaps may be artifacts of transcription timing
2. **Speaker Identification:** UNKNOWN speaker category (0.6% of speaking time) indicates some data quality issues
3. **Context Independence:** Analysis does not consider semantic content, topic relevance, or argumentative quality
4. **Intentionality:** Interruption metrics are structural, not claims about speaker intentions
5. **Meeting Structure:** Does not account for formal roles, agenda items, or procedural structure

### 13.3 Strengths

1. **Quantitative Rigor:** All metrics are objectively measurable and reproducible
2. **Multi-Metric Approach:** Combines multiple indicators for comprehensive analysis
3. **Structural Focus:** Avoids normative interpretation while revealing patterns
4. **Visualization:** Network graphs, heatmaps, and distributions provide clear representation
5. **Scalability:** Methodology applicable to any time-aligned transcript

---

## 15. Visualizations Reference

The analysis includes multiple visualizations covering different aspects of power dynamics. **Static PNG visualizations** are embedded in this report, while **interactive D3.js visualizations** are available as a parallel component for dynamic exploration.

### Interactive Visualizations

For interactive exploration of the data, four options are available:

1. **Observable Notebook** (`observable_notebook.md`): Copy the cells into an Observable notebook for cloud-based interactive visualizations with full D3.js capabilities.

2. **Standalone HTML - Main Analysis** (`interactive_visualizations.html`): Open in any modern web browser for local interactive exploration of structural metrics. Requires `d3_visualization_data.json` in the same directory.

3. **Standalone HTML - Relational Interaction** (`relational_interaction_visualizations.html`): Dedicated interactive visualization for relational interaction analysis. Explores power as enacted moment-by-moment through:
   - **Response-Oriented Network**: Drag nodes, explore who orients to whom, identify conversational attractors
   - **Floor Holding Timeline**: Hover over interruption markers to see tolerance patterns
   - **Tolerance Rates**: Interactive exploration of who maintains floor despite interruptions
   - **Conversational Attractors**: Explore who elicits extended responses
   - **Layered View**: Compare tolerance and attractor patterns together

**Interactive Features - Main Analysis:**
- **Network Graph**: Drag nodes to rearrange, hover for details
- **Timeline**: Hover over bars to see episode details
- **Heatmap**: Hover for segment-specific information
- **Lorenz Curve**: Interactive inequality visualization
- **Cumulative Chart**: Hover to see speaker totals
- **Speaker Filtering**: Filter visualizations by selected speakers

**Interactive Features - Relational Analysis:**
- **Response Network**: Drag nodes, edge thickness = response duration, edge color = frequency
- **Interruption Markers**: Hover to see interruption details and floor maintenance
- **Tolerance Exploration**: Interactive bars showing tolerance rates
- **Attractor Analysis**: Explore response duration patterns
- **Layered Comparison**: Side-by-side view of tolerance and attractor patterns

4. **Standalone HTML - Topic Emergence** (`topic_emergence_visualizations.html`): **NEW** - Dedicated interactive visualization for topic emergence analysis. Explores topics as emergent interactional objects:
   - **Topic Timeline**: Interactive timeline with hover details, filter by status
   - **Speaker-Topic Network**: Drag nodes, explore proposal and response relationships
   - **Topic Trajectories**: See how topics travel between speakers
   - **Stabilization Rates**: Interactive exploration of agenda setting success
   - **Orientation Patterns**: Who responds to which topics, with what delay

**Data Export**: The Python script automatically generates `d3_visualization_data.json` containing all data in D3-friendly format, including `relational_interaction` and `topic_emergence` sections.

---

### Static Visualizations

### 14.1 Speaker Network Graph

![Speaker Interaction Network](speaker_network.png)

**File:** `speaker_network.png`

**Description:**
A directed network graph showing speaker interaction patterns. Nodes represent speakers, with size proportional to total speaking time. Edges (arrows) show transitions between speakers, with thickness indicating frequency. The layout uses a spring algorithm to reveal network structure.

**Key Features:**
- **Node size:** Proportional to total speaking time (larger = more speaking time)
- **Edge thickness:** Proportional to transition frequency (thicker = more frequent)
- **Edge direction:** Arrow indicates who speaks after whom
- **Node color:** Light blue with black borders
- **Edge color:** Gray with transparency

**Interpretation:** Reveals interaction hubs (large nodes with many connections), core-periphery structure (dense center, sparse edges), and transition patterns. Thick edges indicate frequent speaker pairs, while isolated nodes indicate peripheral participants.

### 14.2 Speaking Time Distribution

![Speaking Time Distribution](speaking_time_distribution.png)

**File:** `speaking_time_distribution.png`

**Description:**
A two-panel visualization showing speaking time distribution. Left panel displays horizontal bar chart with all speakers ranked by speaking time. Right panel shows pie chart with percentage distribution.

**Key Features:**
- **Bar chart:** Horizontal bars, length proportional to speaking time, with percentage labels
- **Pie chart:** Colored slices showing percentage distribution
- **Sorting:** Speakers sorted by speaking time (highest to lowest)
- **All speakers:** Includes all 27 speakers

**Interpretation:** Provides both absolute (bar chart) and relative (pie chart) views of participation asymmetry, clearly showing the three-tier hierarchy with top speakers dominating visual space.

### 14.3 Transition Heatmap

![Transition Heatmap](transition_heatmap.png)

**File:** `transition_heatmap.png`

**Description:**
A heatmap matrix showing speaker-to-speaker transition frequencies. Rows represent source speakers (who is speaking), columns represent target speakers (who speaks next).

**Key Features:**
- **Rows:** Source speakers (Y-axis)
- **Columns:** Target speakers (X-axis)
- **Cell values:** Numeric transition counts
- **Color scale:** Yellow-Orange-Red gradient (YlOrRd)
- **Annotations:** Exact counts displayed in each cell
- **All speakers:** Includes all 27 speakers on both axes

**Interpretation:** Reveals response patterns, showing which speakers frequently follow others. Dark cells indicate frequent transitions. Off-diagonal dark cells reveal frequent speaker pairs. Shows core interaction patterns with high-participation speakers having darker cells.

### 14.4 Speaking Timeline

![Speaking Activity Timeline](speaking_timeline.png)

**File:** `speaking_timeline.png`

**Description:**
A horizontal bar chart showing when each speaker was active throughout the meeting. Each colored bar segment represents a speaking episode.

**Key Features:**
- **Y-axis:** Top 10 speakers ranked by total speaking time
- **X-axis:** Meeting time from start (0 seconds) to end (6,855 seconds)
- **Bars:** Colored segments representing speaking episodes
- **Bar length:** Proportional to episode duration
- **Color coding:** Distinct color per speaker

**Interpretation:** Reveals temporal patterns, showing when speakers were active. Sustained participation shows continuous bars, episodic participation shows scattered segments. Reveals periods of high/low activity and temporal gaps.

### 14.5 Cumulative Speaking Time

![Cumulative Speaking Time](cumulative_speaking_time.png)

**File:** `cumulative_speaking_time.png`

**Description:**
A line chart tracking how speaking time accumulates for the top 8 speakers over the meeting duration.

**Key Features:**
- **X-axis:** Meeting time (0 to 6,855 seconds)
- **Y-axis:** Cumulative speaking time in seconds
- **Lines:** One line per speaker (top 8)
- **Line slope:** Steep = concentrated speaking, flat = absence
- **Legend:** Identifies each speaker's line color

**Interpretation:** Shows how speaking time accumulates over time. Steep slopes indicate periods of concentrated speaking. Flat segments indicate absence from floor. Early divergence shows early hierarchy establishment. Parallel lines suggest similar participation rates.

### 14.6 Turn Length Distribution

![Turn Length Distribution](turn_length_distribution.png)

**File:** `turn_length_distribution.png`

**Description:**
A two-panel figure showing turn length statistics. Left panel displays histogram of all turn lengths. Right panel shows box plots comparing turn lengths across top 10 speakers.

**Key Features:**
- **Left panel:** Histogram with 50 bins, median and mean lines
- **Right panel:** Box plots for top 10 speakers
- **Box plot elements:** Median, interquartile range, outliers
- **Statistics:** Median and mean displayed on histogram

**Interpretation:** Reveals that most turns are brief, with right-skewed distribution. Long turns are less common but contribute significantly to total speaking time. Box plots show distinct speaking styles ranging from brief interjections to extended monologues.

### 14.7 Interruption Network

![Interruption Network](interruption_network.png)

**File:** `interruption_network.png`

**Description:**
A directed network graph focused specifically on interruption patterns, isolating competitive floor-taking behavior from general interaction.

**Key Features:**
- **Nodes:** Speakers, size proportional to interruption activity (initiated + received)
- **Edges:** Directed arrows showing interruption direction
- **Edge thickness:** Proportional to interruption frequency
- **Node color:** Light coral/red indicating competitive interaction
- **Edge color:** Dark red emphasizing competitive nature
- **Layout:** Spring layout algorithm

**Interpretation:** Reveals competitive relationships. Thick edges indicate frequent interruption pairs. Large nodes indicate speakers heavily involved in interruption dynamics. Dense connections show competitive dyads. Isolated nodes indicate minimal interruption activity.

### 14.8 Gap Analysis

![Gap Analysis](gap_analysis.png)

**File:** `gap_analysis.png`

**Description:**
A two-panel figure analyzing silence periods between utterances. Left panel shows histogram of gap distribution. Right panel compares gaps for same-speaker vs. speaker-change transitions.

**Key Features:**
- **Left panel:** Histogram with 50 bins, median line, focused on 0-10 second range
- **Right panel:** Two box plots comparing gap types
- **Statistics:** Median gap displayed (0.34 seconds)
- **Distribution:** Highly right-skewed

**Interpretation:** Reveals rapid conversation pace with median gaps under 0.5 seconds. Right-skewed distribution shows most gaps are brief, with occasional longer gaps (topic transitions). Slightly longer gaps for speaker changes (0.36s) vs. same speaker (0.34s).

### 14.9 Participation Heatmap

![Participation Heatmap](participation_heatmap.png)

**File:** `participation_heatmap.png`

**Description:**
A heatmap dividing the meeting into 20 temporal segments and showing speaking time per segment for each speaker.

**Key Features:**
- **Rows:** Top 15 speakers ranked by total speaking time
- **Columns:** 20 time segments dividing meeting chronologically
- **Cell color:** Yellow-Orange-Red gradient (YlOrRd)
- **Cell values:** Numeric speaking time in seconds per segment
- **Color intensity:** Darker = more speaking time

**Interpretation:** Shows temporal distribution of participation. Darker horizontal bands indicate consistent participation. Scattered dark cells show episodic participation. Vertical patterns reveal periods of high overall activity versus quieter segments.

### 15.10 Inequality Lorenz Curve

![Inequality Lorenz Curve](inequality_lorenz_curve.png)

**File:** `inequality_lorenz_curve.png`

**Description:**
A Lorenz curve visualizing cumulative speaking time distribution against cumulative speaker proportion, with perfect equality reference line.

**Key Features:**
- **X-axis:** Cumulative proportion of speakers (0% to 100%)
- **Y-axis:** Cumulative proportion of speaking time (0% to 100%)
- **Blue line:** Actual distribution (Lorenz curve)
- **Red dashed line:** Perfect equality (diagonal reference)
- **Shaded area:** Area between curves representing inequality magnitude
- **Annotation:** Gini coefficient value displayed (0.656)

**Interpretation:** Provides visual and quantitative representation of inequality. Greater deviation from diagonal = greater inequality. Steep initial rise indicates top speakers control large share. Flattening indicates marginal speakers contribute little. Curve shape reveals three-tier hierarchy.

### 15.11 Response-Oriented Network

![Response-Oriented Network](response_oriented_network.png)

**File:** `response_oriented_network.png`

**Description:**
A directed network graph where edges represent responses, weighted by duration of response chains. Shows who orients to whom and who becomes conversational attractors.

**Key Features:**
- **Nodes:** Speakers, sized by speaking time
- **Edges:** Directed arrows (A → B means B responds to A)
- **Edge thickness:** Average duration of response chains
- **Edge color:** Response frequency (darker = more frequent)

**Interpretation:** Reveals conversational attractors (thick incoming edges), orientation patterns (who responds to whom), and capacity to elicit extended uptake. Power appears as relational pattern, not individual attribute.

### 15.12 Floor Holding with Interruptions

![Floor Holding with Interruptions](floor_holding_interruptions.png)

**File:** `floor_holding_interruptions.png`

**Description:**
Temporal visualization of floor holding with interruption attempts marked. Shows tolerance asymmetries: who maintains floor despite interruptions.

**Key Features:**
- **Bars:** Floor holding episodes
- **Red X:** Interruption where floor was lost
- **Orange O:** Interruption where floor was maintained (tolerance)
- **Temporal axis:** Meeting time

**Interpretation:** Orange markers indicate interruption tolerance (power to continue despite disruption). Red markers show vulnerability. Reveals power as enacted moment-by-moment through turn design and repair.

### 15.13 Interruption Tolerance

![Interruption Tolerance](interruption_tolerance.png)

**File:** `interruption_tolerance.png`

**Description:**
Visualization of interruption tolerance rates: who maintains floor despite interruption attempts.

**Key Features:**
- **Left panel:** Attempts vs. floor maintenance (absolute counts)
- **Right panel:** Tolerance rates (maintained / attempts)
- **Color coding:** Green (>50%), Orange (25-50%), Red (<25%)

**Interpretation:** High tolerance rates indicate structural power in turn design. Operationalizes power as capacity to continue despite disruption, not as frequency of interrupting others.

### 15.14 Conversational Attractors

![Conversational Attractors](conversational_attractors.png)

**File:** `conversational_attractors.png`

**Description:**
Visualization of conversational attractors: speakers who elicit extended responses.

**Key Features:**
- **Left panel:** Average response duration per speaker
- **Right panel:** Scatter plot (frequency vs. duration)
- **Duration-weighted:** Captures capacity to elicit extended uptake

**Interpretation:** High duration indicates strong attractors who elicit extended responses. Operationalizes agenda setting as structural feature (capacity to attract), not inferred intention.

### 15.15 Topic Timeline

![Topic Timeline](topic_timeline.png)

**File:** `topic_timeline.png`

**Description:**
Temporal visualization showing when topics emerge, stabilize, or fail.

**Key Features:**
- **Y-axis:** Topics (labeled with ID and proposer)
- **X-axis:** Meeting time (seconds)
- **Bars:** Topic duration, colored by status
- **Blue stars:** First response time (for stabilized topics)

**Interpretation:** Green bars = successful agenda setting (uptake). Orange/red = failed proposals (no uptake). Stars show response timing. Reveals when topics emerge and how long they persist.

### 15.16 Speaker-Topic Network

![Speaker-Topic Network](speaker_topic_network.png)

**File:** `speaker_topic_network.png`

**Description:**
Bipartite graph linking speakers to topics, weighted by uptake duration and response frequency.

**Key Features:**
- **Circles:** Speakers (left side, size = speaking time)
- **Squares:** Topics (right side, colored by status)
- **Blue edges:** Topic proposal relationships
- **Green dashed edges:** Response relationships (weighted by similarity)

**Interpretation:** Dense connections show speakers with many proposals/responses. Green edges show uptake patterns. Isolated topics indicate lack of uptake. Reveals whose topics attract orientation.

### 15.17 Topic Trajectories

![Topic Trajectories](topic_trajectories.png)

**File:** `topic_trajectories.png`

**Description:**
For ALL topics (up to 30 shown), shows how topics travel between speakers or stall. Includes full topic content in titles.

**Key Features:**
- **Multiple timelines:** One per topic (shows ALL topics, not just stabilized)
- **Bars:** Speaker turns related to topic
- **Y-axis:** Speakers participating in topic
- **X-axis:** Time
- **Titles:** Include topic ID, proposer, status, and first 80 characters of topic content

**Interpretation:** Shows topic movement (travels between speakers vs. stalls with proposer). Reveals monopolization vs. shared engagement. Temporal patterns show topic lifecycle. Content preview allows identification of topic themes.

### 15.18 Topic Content Table

![Topic Content Table](topic_content_table.png)

**File:** `topic_content_table.png`

**Description:**
Detailed table showing full content of all stabilized topics with speaker engagement details.

**Key Features:**
- **Topic ID and Proposer:** Identifies who proposed each topic
- **Time Range:** When topic occurred in meeting
- **Status:** Stabilization status
- **Full Topic Content:** First 150 characters of topic text
- **Responders:** List of speakers who responded with uptake
- **First Response Delay:** Time between proposal and first response

**Interpretation:** Provides detailed view of successful topics, showing what content attracts uptake and who engages with successful agenda-setting attempts.

### 15.19 Speaker-Topic Engagement Matrix

![Speaker-Topic Engagement Matrix](speaker_topic_engagement_matrix.png)

**File:** `speaker_topic_engagement_matrix.png`

**Description:**
Heatmap showing engagement level of each speaker with each topic.

**Key Features:**
- **Rows:** Speakers
- **Columns:** Topics (labeled with ID and proposer)
- **Color Scale:**
  - **2.0 (Red):** Proposed the topic
  - **1.0 (Yellow-Green):** Responded with semantic uptake
  - **0.5 (Light Green):** Responded without semantic uptake
  - **0.0 (Dark Green):** No engagement

**Interpretation:** Reveals engagement patterns across all speakers and topics. Shows who proposes topics, who responds with uptake, and who ignores topics. Dense engagement (many 1.0s) indicates topics that attract widespread orientation. Sparse engagement indicates topics that are ignored or monopolized.

![Inequality Lorenz Curve](inequality_lorenz_curve.png)

**File:** `inequality_lorenz_curve.png`

**Description:**
A Lorenz curve visualizing cumulative speaking time distribution against cumulative speaker proportion, with perfect equality reference line.

**Key Features:**
- **X-axis:** Cumulative proportion of speakers (0% to 100%)
- **Y-axis:** Cumulative proportion of speaking time (0% to 100%)
- **Blue line:** Actual distribution (Lorenz curve)
- **Red dashed line:** Perfect equality (diagonal reference)
- **Shaded area:** Area between curves representing inequality magnitude
- **Annotation:** Gini coefficient value displayed (0.656)

**Interpretation:** Provides visual and quantitative representation of inequality. Greater deviation from diagonal = greater inequality. Steep initial rise indicates top speakers control large share. Flattening indicates marginal speakers contribute little. Curve shape reveals three-tier hierarchy.

---

## 16. Conclusions

### 15.1 Structural Summary

The debate transcript reveals a **highly asymmetric participation structure** with clear hierarchical organization:

1. **Three-tier hierarchy** based on speaking time, turn-taking, and agenda control
2. **Core-periphery network structure** with dense interactions among high-participation speakers
3. **Competitive floor control** patterns, particularly between top participants
4. **Strategic participation** variations (e.g., SPEAKER_07's high interruption activity despite low speaking time)
5. **Rapid turn-taking rhythm** with median gaps of 0.34 seconds indicating fast-paced, competitive interaction
6. **Quantified inequality** with top 3 speakers controlling 55.7% of speaking time (5.0x their proportional share)
7. **Temporal concentration** with participation distributed across meeting segments, showing sustained engagement by top speakers
8. **Distinct speaking styles** ranging from extended monologues (SPEAKER_18: 43.69s avg) to brief interjections (SPEAKER_07: 5.66s avg)

### 15.2 Key Structural Features

- **Concentration:** Top 3 speakers control 55.7% of speaking time (5.0x proportional share)
- **Competition:** High interruption activity among primary participants (154 rapid turn-taking events)
- **Control:** Agenda-setting concentrated among high-participation speakers (45 topic introductions)
- **Marginalization:** 40% of speakers account for less than 1% of speaking time each
- **Inequality:** Normalized entropy of 0.758 indicates moderate but significant inequality
- **Pace:** Median gap of 0.34 seconds reveals rapid turn-taking rhythm
- **Temporal Distribution:** Participation heatmap shows sustained activity by top speakers across meeting segments
- **Speaking Styles:** Wide variance in turn lengths (4.38s to 43.69s median) reveals diverse interactional strategies

### 15.3 Implications for Analysis

These structural patterns provide a quantitative foundation for understanding:
- **Floor access patterns:** Who gets to speak and for how long
- **Interaction dynamics:** How speakers respond to and engage with each other
- **Topic control:** Who introduces new conversational segments
- **Network position:** Centrality and marginalization in the interaction network
- **Temporal patterns:** When speakers participate and how participation is distributed over time
- **Turn-taking rhythm:** Pace of conversation and gap patterns between speakers
- **Inequality quantification:** Quantitative measures of participation asymmetry (Gini, entropy, concentration ratios)
- **Speaking styles:** Distribution of turn lengths and variance in participation strategies

### 15.4 Methodological Note

This analysis operationalizes power dynamics through **structural features of conversation**, not through semantic interpretation or assumptions about authority. All metrics describe **interactional patterns** rather than making claims about speaker intentions, argumentative quality, or social status. Normative interpretation (e.g., labeling speakers as "dominant" or "marginal") is left to the human analyst, who can combine these structural findings with contextual knowledge, semantic analysis, and other relevant information.

---

## Appendices

### Appendix A: Complete Metrics Table

See `power_dynamics_report.json` for complete structured data including:
- Detailed speaking time per speaker
- Complete turn-taking statistics
- Full interruption and overlap data
- Complete transition matrix
- Comprehensive agenda control data
- Inequality metrics (Gini coefficient, entropy, concentration measures)
- Gap statistics (median, mean, by transition type)
- Topic emergence data (topics, stabilization status, speaker orientations)
- Relational interaction metrics (response networks, tolerance rates, attractor scores)

### Appendix C: Topic Content Analysis

See `topic_content_analysis.txt` for **complete content analysis** of all 152 detected topics, including:
- **Full topic text** (not truncated) for each topic
- **All responses** to each topic with full response text
- **Semantic similarity scores** for each response
- **Response timing and delays**
- **Uptake status** (whether response met similarity threshold)
- **Speaker engagement summary** showing proposal and stabilization rates per speaker

This file provides the detailed content analysis that reveals:
- What topics succeed (content themes that attract uptake)
- What topics fail (content that is ignored or resisted)
- How speakers relate to topics (full response texts show engagement patterns)
- Power positions through agenda-setting capacity (whose topics attract semantic orientation)

### Appendix D: Fine-Grained Topic-Speaker Relations Analysis

See **`fine_grained_topic_power_analysis.txt`** for comprehensive analysis of power as interactional structure, including:

**1. Topic Closure Authority:**
- Who can end topics without contest
- Uncontested closure rates by speaker
- Capacity to delimit relevance and reorganize participation framework

**2. Asymmetric Topical Accountability:**
- Who is asked to clarify/justify vs who isn't
- Epistemic standing revealed through accountability demands
- Differential treatment of speakers' contributions

**3. Topic Recycling:**
- Topics that gain traction when reintroduced by different speakers
- Authority as relational rather than propositional
- Power shifts through speaker position changes

**4. Topic Hijacking vs Alignment:**
- Reframing while preserving legitimacy (Goffman's footing shifts)
- Complete shifts vs subtle control
- Repositioning within interaction without overt interruption

**Key Findings:**
- **SPEAKER_19:** 100% uncontested closure rate, 0 accountability demands (epistemic authority)
- **SPEAKER_09:** 83.3% uncontested closure rate, 0 accountability demands (structural power)
- **SPEAKER_03:** Highest accountability rate (1.00 per topic) - lower epistemic standing
- **Only 3 hijacking/reframing cases** - most responses are complete shifts or alignments

### Appendix E: Topic Engagement and Power Dynamics Analysis

See **`topic_engagement_power_analysis.txt`** and **`TOPIC_ENGAGEMENT_SUMMARY.md`** for comprehensive analysis of:
- **Most discussed topics** (ranked by engagement score)
- **Which topics attracted most attention** by which speakers
- **Power dynamics revealed** through topic engagement patterns
- **Agenda setting capacity** vs. speaking time (power decoupling)
- **Response attraction patterns** (who responds to whose topics)
- **Uptake success rates** (whose topics achieve semantic orientation)

**Key Findings:**
- Only 2.0% of topics achieve stabilization (highly competitive discourse)
- High speaking time speakers (SPEAKER_09, SPEAKER_18) have 0% stabilization rates
- Low-participation speakers (SPEAKER_17) achieve 100% stabilization rate
- Power is decoupled from speaking time: floor control ≠ agenda control
- Concrete, procedural topics succeed; abstract topics fail

### Appendix B: Methodological Notes

- **Main Methodology**: See `methodological_note.txt` for detailed explanation of operationalization decisions and interpretive constraints for structural metrics.

- **Topic Emergence Methodology**: See `topic_emergence_methodology.txt` for explanation of how topics are treated as emergent interactional objects, including semantic similarity thresholds, stabilization criteria, and speaker orientation analysis.

---

**Report Generated:** Analysis script execution  
**Data Source:** `amuta_2026-01-12_1.json`  
**Analysis Tool:** `analyze_power_dynamics.py`
