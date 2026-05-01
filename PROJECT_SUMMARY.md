# Project Summary

GridSense investigates electricity outage risk in Addis Ababa using community-reported data and a two-stage forecasting approach.

## Project shift

The project moved from report-level risk scoring to **time-location outage forecasting**.

New main question:
Can community-reported data, time features, location, planning status, and weather conditions be used to estimate electricity outage risk in Addis Ababa?

## Two-stage model design

1. **Model 1: Outage forecasting**
- Target: `outage_reported`
- Input: time window, day of week, sub-city, weather, rainy indicator, planning status
- Output: outage risk probability

2. **Model 2: Conditional impact**
- Scope: rows where outage occurs
- Targets: `high_severity_outage` and `avg_duration_hours`
- Output: likely disruption intensity if outage happens

## Why this is useful locally

This design supports planning decisions for students, households, and small businesses by estimating when/where risk is higher and how disruptive outages may be.

## Limits

The data is community-reported and not official utility telemetry. Results should be treated as local decision-support evidence, not operational outage control.

