# 3. Create basic_metrics_simple.py
$metricsCode = @"
"""
SIMPLE Evaluation - Just basic metrics
"""
import numpy as np

class BasicEvaluatorSimple:
    @staticmethod
    def exact_match(predicted, gold):
        """Simple exact match"""
        return 1.0 if str(predicted).strip().lower() == str(gold).strip().lower() else 0.0
    
    def evaluate_batch(self, predictions, golds):
        """Evaluate batch"""
        scores = [self.exact_match(p, g) for p, g in zip(predictions, golds)]
        
        return {
            'exact_match_mean': float(np.mean(scores)),
            'exact_match_std': float(np.std(scores)),
            'num_examples': len(predictions)
        }
"@

$metricsCode | Out-File -FilePath "phase2/evaluation/basic_metrics_simple.py" -Encoding utf8
Write-Host "✅ Created phase2/evaluation/basic_metrics_simple.py" -ForegroundColor Green