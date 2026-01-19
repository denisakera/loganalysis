# Fine-Grained Topic-Speaker Relations: Power as Interactional Structure

## Executive Summary

This analysis examines power as an **interactional structure** rather than semantic property, focusing on four phenomena that reveal power through conversational structure:

1. **Topic Closure Authority** - Who can end topics without contest
2. **Asymmetric Topical Accountability** - Who is asked to clarify/justify vs who isn't
3. **Topic Recycling** - Topics that gain traction when repositioned
4. **Topic Hijacking vs Alignment** - Reframing while preserving legitimacy

---

## 1. Topic Closure Authority

**Power is visible in who can end topics without contest.** When a speaker shifts away from an ongoing theme and others follow without repair, this indicates capacity to delimit relevance.

### Key Findings:

- **145 topic closures detected**
- **128 uncontested closures (88.3%)** - others followed without repair

### Top Speakers by Closure Authority:

| Speaker | Total Closures | Uncontested | Success Rate |
|---------|---------------|-------------|--------------|
| **SPEAKER_19** | 12 | 12 | **100.0%** |
| **SPEAKER_02** | 14 | 13 | **92.9%** |
| **SPEAKER_07** | 12 | 11 | **91.7%** |
| **SPEAKER_09** | 24 | 20 | **83.3%** (highest volume) |
| **SPEAKER_25** | 13 | 9 | 69.2% |
| **SPEAKER_18** | 11 | 7 | 63.6% |

### Power Insight:

**SPEAKER_19** and **SPEAKER_02** have highest closure authority - they can reorganize the participation framework by shifting topics. This is **structural power** - the capacity to delimit what is relevant, not just semantic authority.

**SPEAKER_09** has highest volume of closures (24) with 83.3% success rate, showing consistent capacity to shift topics.

---

## 2. Asymmetric Topical Accountability

**Uneven demand for clarification/justification signals differential epistemic standing.** Some speakers are routinely asked to clarify, justify, or provide evidence, while others are not.

### High Accountability Speakers (Routinely Challenged):

| Speaker | Topics Proposed | Accountability Demands | Rate per Topic |
|---------|----------------|----------------------|----------------|
| **SPEAKER_03** | 4 | 4 | **1.00** |
| **SPEAKER_26** | 3 | 2 | **0.67** |
| **UNKNOWN** | 4 | 2 | **0.50** |
| **SPEAKER_24** | 6 | 2 | **0.33** |
| **SPEAKER_25** | 12 | 3 | **0.25** |

### Low Accountability Speakers (Never Challenged):

| Speaker | Topics Proposed | Accountability Demands | Rate per Topic |
|---------|----------------|----------------------|----------------|
| **SPEAKER_09** | 20 | 0 | **0.00** |
| **SPEAKER_19** | 16 | 0 | **0.00** |
| **SPEAKER_18** | 17 | 2 | **0.12** |
| **SPEAKER_02** | 16 | 3 | **0.19** |

### Power Insight:

**SPEAKER_09** and **SPEAKER_19** have **zero accountability demands** despite proposing many topics. This indicates **epistemic authority** - their topics are accepted without challenge.

**SPEAKER_03** has **highest accountability rate (1.00)** - every topic challenged. This indicates **lower epistemic standing** - must justify contributions.

**Pattern:** High-participation speakers (SPEAKER_09, SPEAKER_19) have low accountability, suggesting their epistemic authority is recognized.

---

## 3. Topic Recycling

**Power appears when topics initially ignored gain traction after reintroduction by different speaker.** Authority is relational rather than propositional.

### Key Finding:

- **0 topic recycling cases detected**

### Interpretation:

The absence of topic recycling suggests:
- Topics are evaluated on content alone, not speaker position
- OR: Speaker positions are relatively stable (no clear hierarchy where same topic succeeds when repositioned)
- Topics are either taken up immediately or permanently ignored

---

## 4. Topic Hijacking vs Alignment

**Reframing topics while preserving legitimacy exercises subtle control over meaning.** Aligns with Goffman's footing shifts - repositioning within interaction.

### Key Findings:

- **205 total topic responses analyzed**
- **3 hijacking/reframing cases** (0.3-0.6 similarity)
  - Subtle control: reframing while preserving semantic connection
- **202 complete shifts** (<0.3 similarity)
  - Topics ignored or completely redirected
- **0 alignment cases** (>0.6 similarity)
  - No cases of maintaining topic frame

### Topic Control Patterns:

| Speaker | Hijacking/Reframing | Complete Shifts | Total Responses |
|---------|-------------------|----------------|-----------------|
| **SPEAKER_18** | 1 | 15 | 16 |
| **SPEAKER_19** | 1 | 3 | 4 |
| **SPEAKER_25** | 1 | 5 | 6 |
| **SPEAKER_09** | 0 | 32 | 32 (most shifts) |
| **SPEAKER_02** | 0 | 17 | 17 |

### Power Insight:

**Hijacking/Reframing (moderate similarity)** shows subtle control - repositioning meaning while maintaining conversational legitimacy. Only 3 cases detected, suggesting most responses either:
- Align completely (maintain topic frame)
- Shift completely (ignore or redirect)

**SPEAKER_09** has most complete shifts (32), showing capacity to redirect topics.

**SPEAKER_18, SPEAKER_19, SPEAKER_25** show subtle control through hijacking/reframing.

---

## Integrated Power Dynamics

### Power Profiles:

**SPEAKER_19:**
- **100% closure authority** (can end topics without contest)
- **0 accountability demands** (epistemic authority)
- **1 hijacking/reframing** (subtle control)
- **Power Type:** Structural + Epistemic authority

**SPEAKER_09:**
- **83.3% closure authority** (24 closures, highest volume)
- **0 accountability demands** (epistemic authority)
- **32 complete shifts** (capacity to redirect)
- **Power Type:** Structural + Epistemic authority + Redirective capacity

**SPEAKER_02:**
- **92.9% closure authority** (high success rate)
- **0.19 accountability rate** (low challenges)
- **17 complete shifts**
- **Power Type:** Structural authority

**SPEAKER_03:**
- **1.00 accountability rate** (highest - routinely challenged)
- **Lower epistemic standing** (must justify contributions)
- **Power Type:** Lower epistemic authority

---

## Key Conclusions

1. **Power is Structural:** Topic closure authority reveals capacity to reorganize participation framework, not just semantic control.

2. **Epistemic Standing is Uneven:** Accountability patterns reveal differential epistemic authority - some speakers' topics accepted without challenge, others routinely questioned.

3. **Subtle Control is Rare:** Only 3 hijacking/reframing cases - most responses are complete shifts or alignments.

4. **High-Participation Speakers Have Multiple Power Forms:** SPEAKER_09 and SPEAKER_19 combine structural power (closure authority) with epistemic authority (low accountability).

5. **Power is Interactional:** Revealed through conversational structure (who can shift topics, who is challenged, who can reframe), not semantic content alone.

---

## Full Analysis Available

See **`fine_grained_topic_power_analysis.txt`** for complete analysis with all examples and detailed patterns.
