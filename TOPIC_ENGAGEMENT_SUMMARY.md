# Topic Engagement Analysis: Topics Discussed and Power Dynamics

## Executive Summary

This report analyzes **152 topics** detected in the debate transcript, identifying which topics attracted the most attention, which speakers engaged with which topics, and how topic engagement patterns reveal power dynamics.

**Key Finding:** Power is **decoupled from speaking time**. Speakers with high speaking time (SPEAKER_09, SPEAKER_18) have low topic engagement success, while some speakers with lower speaking time achieve successful agenda setting.

---

## Section 1: Most Discussed Topics (Top 20)

Topics ranked by **Engagement Score**, which combines:
- Number of responses (uptake weighted heavily)
- Response duration
- Semantic similarity
- Number of unique responders

### Top 5 Most Discussed Topics:

**1. TOPIC_107 (SPEAKER_09)** - Engagement Score: 27.37
- **Content:** "project operates underneath the . If you need to formalize that in order to be able to point and say, like, OK, this is the project underneath us, and this is how we need to do this in order to receive insurance..."
- **Status:** Failed (no uptake) despite 3 responses
- **Responders:** SPEAKER_07, UNKNOWN, SPEAKER_01
- **Total Response Duration:** 207.59s
- **Power Insight:** SPEAKER_09's topic attracted responses but failed to achieve semantic uptake, indicating resistance or redirection

**2. TOPIC_79 (SPEAKER_17)** - Engagement Score: 26.89 ⭐ STABILIZED
- **Content:** "It has its own problems."
- **Status:** Stabilized (successful agenda setting)
- **Responders:** SPEAKER_19 (2 responses), SPEAKER_05, SPEAKER_18, SPEAKER_01
- **Total Response Duration:** 65.59s
- **Power Insight:** Brief topic by SPEAKER_17 achieved stabilization, showing strategic agenda setting despite low overall speaking time

**3. TOPIC_108 (SPEAKER_07)** - Engagement Score: 25.09
- **Content:** "OK, so getting insurance is cool."
- **Status:** Failed (no uptake)
- **Responders:** UNKNOWN, SPEAKER_01
- **Total Response Duration:** 203.88s
- **Power Insight:** Long response duration but no semantic uptake indicates topic was addressed but not taken up

**4. TOPIC_19 (SPEAKER_02)** - Engagement Score: 22.87 ⭐ STABILIZED
- **Content:** "The thing is, we sat down last week, a bunch of us, like, a bunch of people that were there, because of the leak and the stuff that happened, like, we just opened the bank account to see how much we have to handle this, further stuff that might happen and whatnot. And the bank is, like, it's not in a good shape."
- **Status:** Stabilized
- **Responders:** SPEAKER_23, SPEAKER_18
- **Power Insight:** Concrete financial/bureaucratic concern attracted uptake, showing successful agenda setting

**5. TOPIC_99 (SPEAKER_19)** - Engagement Score: 21.88 ⭐ STABILIZED
- **Content:** "I don't know if you have to be a citizen to be a member of the Muta."
- **Status:** Stabilized
- **Responders:** SPEAKER_15, SPEAKER_25, SPEAKER_12
- **Power Insight:** Procedural question received high engagement, showing procedural topics attract attention

---

## Section 2: Topics by Status

### Stabilized Topics (Successful Agenda Setting): 3

Only **3 out of 152 topics (2.0%)** achieved stabilization, indicating highly competitive discourse where most topics fail to attract semantic uptake.

**Successful Topics:**
1. **TOPIC_79** (SPEAKER_17): "It has its own problems" - 5 responses, 1 uptake
2. **TOPIC_19** (SPEAKER_02): Bank account/financial concerns - 2 responses, 1 uptake
3. **TOPIC_99** (SPEAKER_19): Membership/citizenship question - 3 responses, 1 uptake

**Common Characteristics:**
- Concrete, actionable topics (financial, procedural)
- Brief, focused content
- Attracted multiple responders
- Achieved semantic similarity ≥0.3

### Failed Topics (No Uptake): 142

**Top Failed Topics by Engagement:**
- **TOPIC_107** (SPEAKER_09): Project formalization/insurance - 3 responses, 0 uptake
- **TOPIC_108** (SPEAKER_07): Insurance discussion - 2 responses, 0 uptake
- **TOPIC_20** (SPEAKER_07): Call visibility - 2 responses, 0 uptake

**Pattern:** Many failed topics receive responses but without semantic overlap, indicating topics are addressed but not taken up (resistance or redirection).

### Failed Topics (Silence): 7

Topics completely ignored (no responses within 30 seconds):
- TOPIC_21 (SPEAKER_02)
- TOPIC_96 (SPEAKER_12)
- TOPIC_127 (SPEAKER_03)
- TOPIC_140 (SPEAKER_03)
- TOPIC_3 (SPEAKER_04)
- TOPIC_28 (SPEAKER_09)
- TOPIC_103 (SPEAKER_18)

---

## Section 3: Speaker Engagement Patterns

### Most Active Responders (Who Engages with Topics Most)

**Top Responders:**
1. **SPEAKER_01:** Most active responder across topics
2. **SPEAKER_18:** High response activity
3. **SPEAKER_25:** Frequent responder
4. **SPEAKER_19:** Active engagement
5. **SPEAKER_07:** Moderate responder

**Power Insight:** Response activity shows who orients to topics, regardless of who proposes them.

### Topic Proposers Ranked by Average Engagement Score

**Top Proposers (by engagement their topics attract):**
1. **SPEAKER_17:** 1 topic, avg engagement 26.89 (STABILIZED)
2. **SPEAKER_02:** 16 topics, avg engagement ~15.5 (1 stabilized)
3. **SPEAKER_19:** 16 topics, avg engagement ~12.3 (1 stabilized)
4. **SPEAKER_07:** 10 topics, avg engagement ~11.2 (0 stabilized)
5. **SPEAKER_09:** 20 topics, avg engagement ~8.5 (0 stabilized)

**Power Insight:** SPEAKER_17 achieves highest engagement with single topic, while SPEAKER_09 (highest speaking time) has low average engagement despite proposing most topics.

---

## Section 4: Power Dynamics Revealed Through Topic Engagement

### 4.1 Agenda Setting Capacity

**Whose Topics Attract Attention:**

**High Engagement Topics (Top 10):**
1. TOPIC_107 (SPEAKER_09): 27.37 engagement, 3 responses, 0 uptake
2. TOPIC_79 (SPEAKER_17): 26.89 engagement, 5 responses, 1 uptake ⭐
3. TOPIC_108 (SPEAKER_07): 25.09 engagement, 2 responses, 0 uptake
4. TOPIC_19 (SPEAKER_02): 22.87 engagement, 2 responses, 1 uptake ⭐
5. TOPIC_99 (SPEAKER_19): 21.88 engagement, 3 responses, 1 uptake ⭐

**Power Pattern:** Only 3 of top 10 topics achieved stabilization. High engagement doesn't guarantee uptake.

### 4.2 Response Attraction

**Speakers whose topics receive most responses:**

1. **SPEAKER_09:** 20 topics, ~45 total responses (avg: 2.25 per topic)
2. **SPEAKER_18:** 17 topics, ~38 total responses (avg: 2.24 per topic)
3. **SPEAKER_19:** 16 topics, ~35 total responses (avg: 2.19 per topic)
4. **SPEAKER_02:** 16 topics, ~32 total responses (avg: 2.0 per topic)
5. **SPEAKER_07:** 10 topics, ~25 total responses (avg: 2.5 per topic)

**Power Insight:** SPEAKER_07 has highest response rate per topic despite proposing fewer topics.

### 4.3 Uptake Success

**Whose Topics Achieve Semantic Uptake:**

1. **SPEAKER_19:** 1 stabilized topic out of 16 (6.2% success rate)
2. **SPEAKER_02:** 1 stabilized topic out of 16 (6.2% success rate)
3. **SPEAKER_17:** 1 stabilized topic out of 1 (100% success rate)

**Power Insight:** SPEAKER_17 achieves perfect stabilization rate (1/1), while high-participation speakers (SPEAKER_09, SPEAKER_18) have 0% stabilization rates.

### 4.4 Speaking Time vs. Topic Engagement (Power Decoupling)

**High Speaking Time Speakers:**

| Speaker | Speaking Time | Topics Proposed | Stabilized | Stabilization Rate | Avg Engagement |
|---------|---------------|----------------|------------|-------------------|----------------|
| SPEAKER_09 | 1296.5s (18.9%) | 20 | 0 | 0.0% | 8.5 |
| SPEAKER_18 | 1089.2s (15.9%) | 17 | 0 | 0.0% | 7.2 |
| SPEAKER_25 | 865.2s (12.6%) | 12 | 0 | 0.0% | 6.8 |
| SPEAKER_02 | 411.9s (6.0%) | 16 | 1 | 6.2% | 15.5 |
| SPEAKER_19 | 395.0s (5.8%) | 16 | 1 | 6.2% | 12.3 |

**Power Dynamics Revealed:**

1. **Dominant but Not Influential:**
   - SPEAKER_09: Highest speaking time (18.9%) but 0% stabilization rate
   - SPEAKER_18: Second highest speaking time (15.9%) but 0% stabilization rate
   - **Pattern:** High floor control but low agenda-setting capacity

2. **Strategic Agenda Setting:**
   - SPEAKER_17: Low speaking time but 100% stabilization rate (1/1 topic)
   - SPEAKER_02: Moderate speaking time, 6.2% stabilization rate
   - **Pattern:** Strategic topic selection or timing achieves uptake

3. **Power Decoupling:**
   - Speaking time ≠ Agenda-setting capacity
   - Topics that attract responses ≠ Topics that achieve uptake
   - High participation ≠ High influence

### 4.5 Topic Themes That Attract Attention

**Successful Topics (Stabilized):**
1. **Financial/Bureaucratic:** Bank account concerns (TOPIC_19)
2. **Procedural:** Membership requirements (TOPIC_99)
3. **Organizational:** Problems/concerns (TOPIC_79)

**High Engagement Failed Topics:**
- Insurance/project formalization (TOPIC_107, TOPIC_108)
- Call visibility (TOPIC_20)
- Response protocols (TOPIC_67)

**Pattern:** Concrete, actionable topics attract attention. Abstract or disconnected topics fail.

---

## Key Power Dynamics Conclusions

1. **Agenda Setting is Rare:** Only 2.0% of topics achieve stabilization, indicating highly competitive discourse.

2. **Power Decoupling:** High speaking time speakers (SPEAKER_09, SPEAKER_18) have 0% stabilization rates, showing floor control ≠ agenda control.

3. **Strategic Success:** Low-participation speakers (SPEAKER_17) achieve stabilization through strategic topic selection.

4. **Response ≠ Uptake:** Many topics receive responses but fail to achieve semantic uptake, indicating resistance or redirection.

5. **Content Matters:** Concrete, procedural, organizational topics succeed. Abstract or disconnected topics fail.

6. **Engagement Patterns:** SPEAKER_01, SPEAKER_18, SPEAKER_25 are most active responders, showing who orients to topics regardless of proposer.

---

## Full Analysis Available

For complete details, see:
- **`topic_engagement_power_analysis.txt`** - Full 800+ line analysis with all topics
- **`topic_content_analysis.txt`** - Complete content of all 152 topics with full response texts
- **`power_structures_report.md`** - Comprehensive power dynamics report
