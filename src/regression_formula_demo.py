from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
rows = []
with open(ROOT / 'data/raw/ethiopia_enterprise_outage_indicators.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['indicator_code'] == 'IC.ELC.OUTG':
            rows.append((int(r['year']), float(r['value'])))

# Kujenga-style ordinary least squares by hand:
# m = sum((x - xbar)(y - ybar)) / sum((x - xbar)^2)
# k = ybar - m*xbar
xs = [x for x, y in rows]
ys = [y for x, y in rows]
xbar = sum(xs) / len(xs)
ybar = sum(ys) / len(ys)
m = sum((x - xbar) * (y - ybar) for x, y in rows) / sum((x - xbar) ** 2 for x in xs)
k = ybar - m * xbar
print(f'slope_m_outages_per_month_per_year = {m:.3f}')
print(f'intercept_k = {k:.3f}')
print('Important: n=3, so this is a descriptive trend line, not a forecast model.')
