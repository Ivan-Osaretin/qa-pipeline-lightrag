from pathlib import Path
print('Checking Deliverables...')
files = ['data/indices/final_predictions_phase3.json', 'reports/PHASE3_FINAL_REPORT.md']
for f in files:
    status = '✅' if Path(f).exists() else '❌'
    print(f'{status} {f}')
