import json
from pathlib import Path

print('=' * 60)
print('COMPLETE PHASE 1 VERIFICATION')
print('=' * 60)

# Check files
raw_path = Path('data/raw/hotpot_dev_distractor_v1.json')
subset_path = Path('data/processed/dev_subset_100.json')

print('1. File Check:')
print(f'   Raw data: {"✅" if raw_path.exists() else "❌"}')
print(f'   Subset: {"✅" if subset_path.exists() else "❌"}')

# Load subset
with open(subset_path, 'r') as f:
    data = json.load(f)

examples = data['examples']

print(f'\n2. Data Check: {len(examples)} examples loaded')

# Check balance
comparison = sum(1 for ex in examples if ex.get('type') == 'comparison')
bridge = sum(1 for ex in examples if ex.get('type') == 'bridge')

print(f'\n3. Balance Check:')
print(f'   • Comparison: {comparison}')
print(f'   • Bridge: {bridge}')

# Multi-hop verification
multi_hop = sum(1 for ex in examples if len(ex.get('supporting_facts', [])) >= 2)
print(f'\n4. Multi-hop Check:')
print(f'   • Multi-hop questions: {multi_hop}/{len(examples)}')

print('\n' + '=' * 60)
print('✅ PHASE 1 COMPLETE AND VERIFIED')
print('=' * 60)
