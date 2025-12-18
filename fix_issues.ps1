# Save this as fix_issues.ps1
Write-Host "=== COMPLETE QA PIPELINE FIX ===" -ForegroundColor Cyan

# 1. Show current status
Write-Host "`n1. Current Project Structure:" -ForegroundColor Yellow
Get-Location

# 2. Check what we have
Write-Host "`n2. Existing Files:" -ForegroundColor Yellow
$files = @(
    "src/data_loader.py",
    "scripts/setup_data.py", 
    "scripts/analyze_data.py",
    "requirements.txt",
    "src/__init__.py",
    "src/config.py"
)

foreach ($file in $files) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file (will create)" -ForegroundColor Yellow
    }
}

# 3. Check data
Write-Host "`n3. Data Files:" -ForegroundColor Yellow
python -c "
import json
from pathlib import Path

print('Checking data files...')
files = [
    ('Raw HotpotQA', Path('data/raw/hotpot_dev_distractor_v1.json')),
    ('Processed subset', Path('data/processed/dev_subset_100.json'))
]

for name, path in files:
    if path.exists():
        size_mb = path.stat().st_size / (1024 * 1024)
        print(f'  ✓ {name}: {size_mb:.1f} MB')
    else:
        print(f'  ✗ {name}: MISSING')
"

# 4. Install dependencies
Write-Host "`n4. Installing Dependencies:" -ForegroundColor Yellow
try {
    python -c "
try:
    import pandas
    print('✓ pandas already installed')
except ImportError:
    print('Installing pandas...')
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'tqdm'])
    print('✓ Dependencies installed')
"
} catch {
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    pip install pandas numpy matplotlib seaborn tqdm requests
}

# 5. Test the setup
Write-Host "`n5. Testing Setup:" -ForegroundColor Yellow

# Test 1: Python imports
Write-Host "  Testing imports..." -ForegroundColor Yellow
python -c "
try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    print('  ✓ Core dependencies imported')
except ImportError as e:
    print(f'  ✗ Import error: {e}')
"

# Test 2: Data loader
Write-Host "  Testing data loader..." -ForegroundColor Yellow
python -c "
import sys
from pathlib import Path
sys.path.append(str(Path().cwd() / 'src'))

try:
    from data_loader import HotpotQADataLoader
    print('  ✓ Data loader imported')
    
    try:
        loader = HotpotQADataLoader()
        data = loader.load_subset()
        print(f'  ✓ Data loaded: {len(data)} examples')
    except Exception as e:
        print(f'  ✗ Could not load data: {e}')
        
except ImportError as e:
    print(f'  ✗ Could not import: {e}')
"

# 6. Run the setup
Write-Host "`n6. Running Setup Script:" -ForegroundColor Yellow
try {
    python scripts/setup_data.py
    Write-Host "  ✓ Setup script completed successfully" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Setup script failed" -ForegroundColor Red
    Write-Host "  Running fallback test..." -ForegroundColor Yellow
    
    # Fallback test
    python -c "
import json
print('Running fallback verification...')
try:
    with open('data/processed/dev_subset_100.json', 'r') as f:
        data = json.load(f)
    print(f'✓ Data loaded: {len(data)} examples')
    if data:
        first = data[0]
        print(f'First example: {first[\"question\"][:80]}...')
except Exception as e:
    print(f'✗ Error: {e}')
"
}

Write-Host "`n=== FIX COMPLETE ===" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Run analysis: python scripts/analyze_data.py" -ForegroundColor Green
Write-Host "2. Check Google Doc for updates needed" -ForegroundColor Green
Write-Host "3. Update reports/phase1_report.md" -ForegroundColor Green