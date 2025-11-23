# Anomaly Detection in Observability

## Учебные материалы

- [Школьный уровень](school.ru.md)
- [Университетский уровень](univer.ru.md)

## Algorithm Visualization

### Flowchart (ASCII)

```
Anomaly Detection in Observability Flowchart:

┌─────────────┐
│   Start     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Initialize │
│   data      │
└──────┬──────┘
       │
       ▼
┌─────────────┐      Yes
│  Process   ├──────┐
│  condition?│      │
└──────┬──────┘      │
       │ No          │
       ▼             │
┌─────────────┐      │
│  Execute   │      │
│  operation │      │
└──────┬──────┘      │
       │             │
       └─────────────┘
       │
       ▼
┌─────────────┐
│    End      │
└─────────────┘
```

### Step-by-Step Execution

```
Anomaly Detection in Observability Step-by-Step Execution:

Input: [example data]

Step 1: Initialize
State: [initial state]

Step 2: Process
State: [intermediate state]

Step 3: Finalize
State: [final state]

Result: [output]
```

### Interactive Flowchart (Mermaid)

```mermaid
flowchart TD
    Start([Start]) --> Init[Initialize data]
    Init --> Process{Process condition}
    Process -->|True| Execute[Execute operation]
    Execute --> Done{Complete?}
    Done -->|No| Process
    Done -->|Yes| End([End])
    Process -->|False| End
```

> **Note**: Mermaid diagrams are rendered automatically on GitHub. For local viewing, use a Mermaid-compatible Markdown viewer.

- [Python Implementation](/code/semester_11/lecture_78_observability_platform/anomaly_detection/algorithm.py)
- [Java Implementation](/code/semester_11/lecture_78_observability_platform/anomaly_detection/Algorithm.java)
- [Python Tests](/code/semester_11/lecture_78_observability_platform/anomaly_detection/test_algorithm.py)

   Anomaly Detection in Observability

What problem does it solve? (1 sentence)  
   Detects unusual patterns, behaviors, or events in system metrics, logs, and traces that deviate from normal baselines, enabling early detection of issues and incidents.

Intuition (plain-language explanation)  
   Like a smoke detector: Anomaly Detection is like a smoke detector for systems - it watches for unusual patterns (smoke) that indicate problems (fire) - just as smoke detectors alert you to fires early, anomaly detection alerts you to system issues early.

Inputs & Outputs  

  - Input: Time-series metrics, logs, traces, baseline patterns, detection algorithms, thresholds.  
  - Output: Detected anomalies, anomaly scores, alerts, root cause indicators, incident triggers.

Step-by-step description (5–10 lines max)  
Establish baseline: establish baseline of normal behavior.
Collect data: collect metrics, logs, and traces.
Analyze: analyze data for deviations from baseline.
Detect: detect anomalies using algorithms (statistical, ML).
Score: score anomalies by severity and confidence.
Correlate: correlate anomalies across systems.
Alert: alert on significant anomalies.
Investigate: investigate anomalies for root causes.
Learn: learn from anomalies to improve detection.
Tune: tune detection algorithms based on feedback.

Tiny example (hand-simulated)  
   Anomaly Detection: baseline: CPU usage 40-60% → detect: CPU spikes to 95% → score: high severity anomaly → correlate: correlates with database query spike → alert: alert ops team → investigate: find slow query → Anomaly Detection successful.

Time & Space Complexity  

  - Time: O(c + a + d) where c is collection time, a is analysis time, d is detection time (real-time, continuous).  
  - Space: O(d + b) where d is data storage, b is baseline storage (historical patterns).

Strengths  

- Early detection: enables early detection of issues.
- Automation: automates issue detection.
- Coverage: can detect issues across multiple dimensions.

Weaknesses / limitations  

- False positives: may generate false positive alerts.
- Baseline: requires good baseline for accurate detection.
- Tuning: requires tuning to reduce false positives.

Compare with alternatives  
    Alternatives: Threshold-Based Alerts, Manual Monitoring, Rule-Based Detection, ML-Based Detection

30-second explanation (your own words)  
    Detects unusual patterns, behaviors, or events in system metrics, logs, and traces that deviate from normal baselines, enabling early detection of issues and incidents.

*Sources: Adapted from standard university textbooks and Wikipedia summaries.*
