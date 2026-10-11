# Project 03 — Financial Crime Alert Optimization

## Business question
How does an alert threshold change detection, false-positive review workload, and the hypothetical cost of missed suspicious activity?

## Run it
From the repository root:

```bash
python project-03-financial-crime-analytics/src/threshold_demo.py
```

The script generates synthetic labels and scores, evaluates thresholds from 0.10 to 0.95, and writes `reports/generated/threshold_tradeoffs.csv`. It reports precision, recall, F1, alert volume, missed positives, alert rate, average precision, and a transparent cost sensitivity scenario.

## Cost assumptions
The demo assigns 1 cost unit per reviewed alert and 25 cost units per missed positive. These values are arbitrary illustrative assumptions, not estimates of actual financial or regulatory loss. Change them and rerun the analysis to test how the preferred threshold changes.

## Example run (synthetic scores, seed 19)
Under the illustrative cost assumptions, threshold **0.40** had the lowest total hypothetical cost in this run (941 units), with precision 48.4%, recall 94.8%, 566 alerts, and 15 missed positives. This is not a recommended real-world threshold: the scores are synthetic and the cost assumptions are arbitrary. The point is to demonstrate how an operating decision changes when workload and missed-case costs are considered together.

## Important limitations
- The scores are generated from known synthetic distributions; there is no trained classifier and the metrics are not a claim of real-world model performance.
- In real financial-crime work, labels are delayed and imperfect, classes are highly imbalanced, and threshold decisions require compliance, investigation capacity, and human oversight.
- A score is a prioritization signal, not a determination that a customer or transaction is criminal. Never use this demo for live decisions.
