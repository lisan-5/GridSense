from pathlib import Path
import csv, json

ROOT = Path(__file__).resolve().parents[1]

def read_csv(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

context = read_csv(ROOT / 'data/raw/addis_ababa_reliability_context.csv')
wb = read_csv(ROOT / 'data/raw/ethiopia_enterprise_outage_indicators.csv')

metrics = {r['metric']: float(r['value']) for r in context}
results = {
    'average_mv_interruption_duration_hours': round(metrics['medium_voltage_interruption_duration'] / metrics['medium_voltage_line_interruptions'], 2),
    'estimated_unresolved_issues_count': int(metrics['outage_related_problems_identified'] * (1 - metrics['outage_related_problems_resolved'] / 100)),
}

outage_months = [r for r in wb if r['indicator_code'] == 'IC.ELC.OUTG']
outage_months = sorted(outage_months, key=lambda r: int(r['year']))
results['enterprise_outage_monthly_increase_2006_to_2015'] = round(float(outage_months[-1]['value']) - float(outage_months[0]['value']), 2)
results['enterprise_outage_monthly_pct_increase_2006_to_2015'] = round((float(outage_months[-1]['value']) - float(outage_months[0]['value'])) / float(outage_months[0]['value']) * 100, 1)

# Optional: incorporate real collected community reports when available.
collected_path = ROOT / 'data/collected/community_outage_reports.csv'
if collected_path.exists():
    reports = read_csv(collected_path)
    reports = [r for r in reports if r.get('duration_hours', '').strip()]

    if reports:
        durations = [float(r['duration_hours']) for r in reports]
        results['community_reports_count'] = len(reports)
        results['community_mean_duration_hours'] = round(sum(durations) / len(durations), 2)
        results['community_max_duration_hours'] = round(max(durations), 2)

        rainy = [float(r['duration_hours']) for r in reports if r.get('weather_condition') in {'light_rain', 'heavy_rain', 'storm'}]
        clear = [float(r['duration_hours']) for r in reports if r.get('weather_condition') == 'clear']
        results['community_rainy_n'] = len(rainy)
        results['community_clear_n'] = len(clear)
        if rainy:
            results['community_rainy_mean_duration_hours'] = round(sum(rainy) / len(rainy), 2)
        if clear:
            results['community_clear_mean_duration_hours'] = round(sum(clear) / len(clear), 2)

        # Welch t-test is only run when each group has at least 2 rows.
        if len(rainy) >= 2 and len(clear) >= 2:
            def variance(xs):
                m = sum(xs) / len(xs)
                return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)

            mr = sum(rainy) / len(rainy)
            mc = sum(clear) / len(clear)
            vr = variance(rainy)
            vc = variance(clear)
            se = ((vr / len(rainy)) + (vc / len(clear))) ** 0.5
            t_stat = (mr - mc) / se if se > 0 else 0.0
            results['community_rainy_vs_clear_t_stat'] = round(t_stat, 3)
            results['community_rainy_vs_clear_test_note'] = (
                'Welch t-stat reported; for p-value use notebook/scipy once sample sizes are larger.'
            )

print(json.dumps(results, indent=2))
