# Test Results Analysis Template

Use this template to systematically analyze LLM prompt test results after each experiment.

## 1. Executive Summary

**Current Performance:**
- Daily Summaries: [X]% accuracy ([correct]/[total] correct)
- Weekly Summary: [description of major issues if any]

**Key Insight:** [One sentence explaining the core failure mode]

---

## 2. Error Classification

### Error Inventory

For each error found, document:

| Error ID | Summary Type | Date/Context | Error Type | Severity |
|----------|--------------|--------------|------------|----------|
| E1 | Daily/Weekly | [specific case] | [classification] | Critical/Major/Minor |

### Error Type Categories

- **Math errors**: Incorrect calculations (e.g., "40% marked as consistent")
- **Boundary confusion**: Errors near thresholds (e.g., 16-17% near 20%)
- **Baseline selection**: Wrong average chosen (weekly vs monthly)
- **Pattern misidentification**: Trend direction wrong (said decrease, data shows increase)
- **Self-contradiction**: Contradictory statements within same output
- **Tone violations**: Interpretive language when should be descriptive
- **Factual errors**: Numbers don't match data

---

## 3. Quantitative Analysis

### By Rule Type

| Rule/Requirement | Total Cases | Correct | Accuracy | Error Pattern |
|------------------|-------------|---------|----------|---------------|
| ±20% comparison rule | [n] | [n] | [%] | [description] |
| Baseline priority (weekly first) | [n] | [n] | [%] | [description] |
| Boundary cases (15-20%) | [n] | [n] | [%] | [description] |
| Pattern direction (increase/decrease) | [n] | [n] | [%] | [description] |

### Error Frequency Distribution

```
[Create a simple breakdown like:]
Math errors: 1/15 (7%)
Boundary confusion: 2/15 (13%)
Wrong baseline: 1/15 (7%)
Contradictions: 1/1 (100% of weekly)
```

---

## 4. Root Cause Analysis

For each error type, identify:

### Error Type: [Name]

**What happened:**
```
[Specific example with data]
```

**Why it happened:**
- [Root cause - e.g., "Calculation not performed", "Verification step skipped"]

**Evidence from prompt:**
- [Quote relevant section that failed]
- [Explain why this section didn't work]

**The fix:**
```xml
[Show the specific prompt change needed]
```

**Expected impact:** [percentage improvement estimate]

---

## 5. Prompt Effectiveness Analysis

### What Worked ✓

List sections/approaches that successfully prevented errors:
- ✓ [Section name]: [What it prevented]
- ✓ [Approach]: [Evidence it worked]

### What Didn't Work ✗

List sections/approaches that failed to prevent errors:
- ✗ [Section name]: [What it failed to prevent]
- ✗ [Why it failed]: [Explanation - e.g., "treated as optional", "too vague"]

### Core Issue Identification

**Pattern:** [e.g., "Long instructions create suggestion effect, not requirement effect"]

**Evidence:** [Point to specific failures that show this pattern]

**Solution Direction:** [e.g., "Mandatory outputs with verification"]

---

## 6. Comparison to Baseline/Expected

### Expected Performance (from prompt review)
- Expected accuracy: [X]%
- Expected improvements: [list]

### Actual Performance
- Actual accuracy: [X]%
- Actual improvements: [list]

### Gap Analysis

**Why the gap?**
1. [Reason 1 with evidence]
2. [Reason 2 with evidence]
3. [Reason 3 with evidence]

---

## 7. Specific Fixes (Prioritized)

### Must-Do (Critical - Next Version)

#### Fix #1: [Name]
- **Problem:** [description]
- **Root cause:** [explanation]
- **Solution:** [prompt change]
- **Estimated impact:** +[X]% accuracy
- **Implementation:** [daily/weekly prompt v[X]]

#### Fix #2: [Name]
- **Problem:** [description]
- **Root cause:** [explanation]
- **Solution:** [prompt change]
- **Estimated impact:** +[X]% accuracy
- **Implementation:** [daily/weekly prompt v[X]]

[Continue for each critical fix]

**Expected total improvement:** [current]% → [target]%

### Should-Do (After Testing)

[List secondary improvements with less critical impact]

### Nice-to-Have (Future Optimization)

[List experimental or long-term improvements]

---

## 8. Test Strategy for Next Iteration

### Test Dataset Requirements

**Stratified cases needed:**

1. **[Error Type 1] Cases:** [n] cases
   - [Specific scenarios to cover]
   - [Acceptance criteria]

2. **[Error Type 2] Cases:** [n] cases
   - [Specific scenarios to cover]
   - [Acceptance criteria]

[Continue for each error type]

**Total test cases:** [n]

### Acceptance Criteria

**Daily summaries:**
- ✓ [X]%+ correct [specific rule]
- ✓ [X]%+ correct [specific rule]
- ✓ 0 [specific error type]

**Weekly summaries:**
- ✓ 100% pattern direction accuracy
- ✓ [X]%+ [specific requirement]
- ✓ 0 self-contradictory statements

---

## 9. Implementation Roadmap

### Week 1: Critical Fixes
- [ ] Implement Fix #1
- [ ] Implement Fix #2
- [ ] Implement Fix #3
- [ ] Test on current dataset
- [ ] Target: [X]% accuracy

### Week 2: Validation Testing
- [ ] Create stratified test dataset
- [ ] Run full test suite
- [ ] Calculate accuracy by error type
- [ ] Identify remaining failure modes

### Week 3: Optimization
- [ ] [Secondary improvements]
- [ ] [Experimental approaches]

### Week 4: Production Prep
- [ ] [Production readiness steps]

---

## 10. Key Metrics to Track

**Per Iteration:**
- Overall accuracy (daily)
- Overall accuracy (weekly)
- Errors by type (distribution)
- Boundary case accuracy (15-25% range)
- Baseline selection accuracy (weekly vs monthly)
- Contradiction rate (weekly)
- Tone compliance (no interpretive language)

**Trend Over Time:**
- Track each metric across versions (v1 → v2 → v3, etc.)
- Identify which fixes had biggest impact
- Document regression (if any metric got worse)

---

## 11. Bottom Line

**Summary:** [2-3 sentences explaining what you learned and what's next]

**Confidence in next iteration:** [Low/Medium/High] based on [reasoning]

**Blockers/Risks:** [Any concerns about whether fixes will work]

---

## Template Usage Notes

1. **Complete this analysis after every test run** - don't skip even if results look good
2. **Be specific with examples** - always show the actual error, not just describe it
3. **Quantify everything possible** - percentages, counts, frequencies
4. **Root cause over symptoms** - don't just list errors, explain WHY they happened
5. **Actionable fixes only** - every problem should have a concrete proposed solution
6. **Track metrics over time** - compare each version to previous to see actual improvement
7. **Be honest about gaps** - if expected improvement didn't materialize, explain why

This systematic approach prevents "prompt drift" where you keep adding instructions without measuring their actual impact.
