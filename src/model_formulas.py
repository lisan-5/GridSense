"""Model formulas for future verified Addis Ababa outage reports.

This file is intentionally formula-focused. The final project avoids training a
production ML model on synthetic data. When enough verified event-level data is
collected, these are the first models to train.
"""

import math

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def logistic_probability(beta0, betas, x):
    """P(outage_next_hour = 1 | x) = sigmoid(beta0 + beta^T x)."""
    return sigmoid(beta0 + sum(b * xi for b, xi in zip(betas, x)))

def squared_error(y_true, y_pred):
    """Linear regression learns parameters that minimize sum((y - y_hat)^2)."""
    return (y_true - y_pred) ** 2

def weighted_severity(duration_score, report_score, impact_score, confidence_score):
    """Transparent decision-support score, not a ground-truth label."""
    return 0.40 * duration_score + 0.25 * report_score + 0.20 * impact_score + 0.15 * confidence_score
