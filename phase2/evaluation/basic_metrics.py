"""
Basic Evaluation Metrics - Complete Implementation
Metrics from LightRAG paper: Exact Match, Token F1, Contains Score
"""
import numpy as np
from typing import List, Dict, Tuple, Any
from loguru import logger
import re
from sklearn.metrics import f1_score, precision_score, recall_score
import json
from datetime import datetime
from pathlib import Path

class BasicEvaluator:
    """Complete evaluation metrics for QA systems"""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison (case-insensitive, punctuation removed)"""
        text = str(text).lower().strip()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        return text
    
    @staticmethod
    def exact_match(predicted: str, gold: str) -> float:
        """Binary exact match score"""
        pred_norm = BasicEvaluator.normalize_text(predicted)
        gold_norm = BasicEvaluator.normalize_text(gold)
        return 1.0 if pred_norm == gold_norm else 0.0
    
    @staticmethod
    def token_f1(predicted: str, gold: str) -> Dict[str, float]:
        """Token-level F1, Precision, Recall"""
        pred_tokens = set(BasicEvaluator.normalize_text(predicted).split())
        gold_tokens = set(BasicEvaluator.normalize_text(gold).split())
        
        if not pred_tokens or not gold_tokens:
            return {'f1': 0.0, 'precision': 0.0, 'recall': 0.0}
        
        # Calculate token-level metrics
        tp = len(pred_tokens.intersection(gold_tokens))
        fp = len(pred_tokens - gold_tokens)
        fn = len(gold_tokens - pred_tokens)
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        
        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)
        
        return {'f1': f1, 'precision': precision, 'recall': recall}
    
    @staticmethod
    def contains_score(predicted: str, gold: str) -> Dict[str, float]:
        """Check if predicted contains gold answer"""
        pred_norm = BasicEvaluator.normalize_text(predicted)
        gold_norm = BasicEvaluator.normalize_text(gold)
        
        # Exact containment
        exact_contained = 1.0 if gold_norm in pred_norm else 0.0
        
        # Token containment
        gold_words = gold_norm.split()
        if not gold_words:
            return {'exact': 0.0, 'partial': 0.0}
        
        matches = sum(1 for word in gold_words if word in pred_norm)
        partial_score = matches / len(gold_words)
        
        return {'exact': exact_contained, 'partial': partial_score}
    
    @staticmethod
    def evaluate_single(predicted: str, gold: str) -> Dict[str, Any]:
        """Comprehensive single prediction evaluation"""
        em = BasicEvaluator.exact_match(predicted, gold)
        token_metrics = BasicEvaluator.token_f1(predicted, gold)
        contain_metrics = BasicEvaluator.contains_score(predicted, gold)
        
        return {
            'exact_match': em,
            'token_f1': token_metrics['f1'],
            'token_precision': token_metrics['precision'],
            'token_recall': token_metrics['recall'],
            'contains_exact': contain_metrics['exact'],
            'contains_partial': contain_metrics['partial'],
            'predicted': predicted,
            'gold': gold,
            'predicted_normalized': BasicEvaluator.normalize_text(predicted),
            'gold_normalized': BasicEvaluator.normalize_text(gold)
        }
    
    def evaluate_batch(self, predictions: List[str], golds: List[str]) -> Dict[str, Any]:
        """Evaluate batch of predictions"""
        if len(predictions) != len(golds):
            logger.error(f"❌ Mismatch: {len(predictions)} predictions vs {len(golds)} golds")
            return {}
        
        logger.info(f"📊 Evaluating {len(predictions)} predictions...")
        
        results = []
        for i, (pred, gold) in enumerate(zip(predictions, golds)):
            result = self.evaluate_single(pred, gold)
            result['example_id'] = i
            results.append(result)
            
            # Log first few examples
            if i < 3:
                logger.info(f"  Example {i+1}:")
                logger.info(f"    Gold: '{gold[:50]}...'")
                logger.info(f"    Pred: '{pred[:50]}...'")
                logger.info(f"    EM: {result['exact_match']:.3f}, F1: {result['token_f1']:.3f}")
        
        # Calculate aggregate statistics
        em_scores = [r['exact_match'] for r in results]
        f1_scores = [r['token_f1'] for r in results]
        precision_scores = [r['token_precision'] for r in results]
        recall_scores = [r['token_recall'] for r in results]
        contain_exact_scores = [r['contains_exact'] for r in results]
        contain_partial_scores = [r['contains_partial'] for r in results]
        
        aggregate_stats = {
            'exact_match': {
                'mean': float(np.mean(em_scores)),
                'std': float(np.std(em_scores)),
                'median': float(np.median(em_scores)),
                'max': float(np.max(em_scores)),
                'min': float(np.min(em_scores))
            },
            'token_f1': {
                'mean': float(np.mean(f1_scores)),
                'std': float(np.std(f1_scores)),
                'median': float(np.median(f1_scores))
            },
            'token_precision': {
                'mean': float(np.mean(precision_scores)),
                'std': float(np.std(precision_scores))
            },
            'token_recall': {
                'mean': float(np.mean(recall_scores)),
                'std': float(np.std(recall_scores))
            },
            'contains_exact': {
                'mean': float(np.mean(contain_exact_scores)),
                'std': float(np.std(contain_exact_scores))
            },
            'contains_partial': {
                'mean': float(np.mean(contain_partial_scores)),
                'std': float(np.std(contain_partial_scores))
            },
            'num_examples': len(predictions),
            'timestamp': datetime.now().isoformat()
        }
        
        # Find best and worst examples
        if results:
            best_f1_idx = np.argmax(f1_scores)
            worst_f1_idx = np.argmin(f1_scores)
            
            aggregate_stats['best_example'] = {
                'index': int(best_f1_idx),
                'f1': float(f1_scores[best_f1_idx]),
                'predicted': results[best_f1_idx]['predicted'][:100],
                'gold': results[best_f1_idx]['gold'][:100]
            }
            
            aggregate_stats['worst_example'] = {
                'index': int(worst_f1_idx),
                'f1': float(f1_scores[worst_f1_idx]),
                'predicted': results[worst_f1_idx]['predicted'][:100],
                'gold': results[worst_f1_idx]['gold'][:100]
            }
        
        logger.info(f"✅ Evaluation complete:")
        logger.info(f"   Exact Match: {aggregate_stats['exact_match']['mean']:.3f} ± {aggregate_stats['exact_match']['std']:.3f}")
        logger.info(f"   Token F1: {aggregate_stats['token_f1']['mean']:.3f} ± {aggregate_stats['token_f1']['std']:.3f}")
        logger.info(f"   Contains (exact): {aggregate_stats['contains_exact']['mean']:.3f}")
        
        return {
            'aggregate_stats': aggregate_stats,
            'individual_results': results,
            'predictions': predictions,
            'golds': golds
        }
    
    def generate_report(self, evaluation_results: Dict[str, Any], save_path: str = None) -> str:
        """Generate comprehensive evaluation report"""
        if not evaluation_results:
            return "❌ No evaluation results to report"
        
        stats = evaluation_results.get('aggregate_stats', {})
        individual_results = evaluation_results.get('individual_results', [])
        
        report = []
        report.append("=" * 80)
        report.append("LIGHTRAG EVALUATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {stats.get('timestamp', datetime.now().isoformat())}")
        report.append(f"Number of examples: {stats.get('num_examples', 0)}")
        report.append("")
        
        # Summary Statistics
        report.append("📊 SUMMARY STATISTICS")
        report.append("-" * 40)
        report.append(f"Exact Match:      {stats.get('exact_match', {}).get('mean', 0):.3f} ± {stats.get('exact_match', {}).get('std', 0):.3f}")
        report.append(f"Token F1:         {stats.get('token_f1', {}).get('mean', 0):.3f} ± {stats.get('token_f1', {}).get('std', 0):.3f}")
        report.append(f"Token Precision:  {stats.get('token_precision', {}).get('mean', 0):.3f} ± {stats.get('token_precision', {}).get('std', 0):.3f}")
        report.append(f"Token Recall:     {stats.get('token_recall', {}).get('mean', 0):.3f} ± {stats.get('token_recall', {}).get('std', 0):.3f}")
        report.append(f"Contains (exact): {stats.get('contains_exact', {}).get('mean', 0):.3f} ± {stats.get('contains_exact', {}).get('std', 0):.3f}")
        report.append(f"Contains (partial): {stats.get('contains_partial', {}).get('mean', 0):.3f} ± {stats.get('contains_partial', {}).get('std', 0):.3f}")
        report.append("")
        
        # Best/Worst Examples
        if 'best_example' in stats:
            report.append("🏆 BEST PERFORMING EXAMPLE")
            report.append("-" * 40)
            report.append(f"Example {stats['best_example']['index'] + 1}:")
            report.append(f"  F1 Score: {stats['best_example']['f1']:.3f}")
            report.append(f"  Gold: {stats['best_example']['gold']}")
            report.append(f"  Predicted: {stats['best_example']['predicted']}")
            report.append("")
        
        if 'worst_example' in stats:
            report.append("⚠️ WORST PERFORMING EXAMPLE")
            report.append("-" * 40)
            report.append(f"Example {stats['worst_example']['index'] + 1}:")
            report.append(f"  F1 Score: {stats['worst_example']['f1']:.3f}")
            report.append(f"  Gold: {stats['worst_example']['gold']}")
            report.append(f"  Predicted: {stats['worst_example']['predicted']}")
            report.append("")
        
        # Sample Results
        report.append("📋 SAMPLE RESULTS (First 5 examples)")
        report.append("-" * 40)
        
        for i, result in enumerate(individual_results[:5]):
            report.append(f"Example {i + 1}:")
            report.append(f"  Gold: '{result.get('gold', '')[:80]}...'")
            report.append(f"  Pred: '{result.get('predicted', '')[:80]}...'")
            report.append(f"  Scores: EM={result.get('exact_match', 0):.3f}, F1={result.get('token_f1', 0):.3f}, Contains={result.get('contains_exact', 0):.3f}")
            report.append("")
        
        # Score Distribution
        if individual_results:
            em_scores = [r.get('exact_match', 0) for r in individual_results]
            f1_scores = [r.get('token_f1', 0) for r in individual_results]
            
            perfect_em = sum(1 for score in em_scores if score == 1.0)
            good_f1 = sum(1 for score in f1_scores if score >= 0.7)
            poor_f1 = sum(1 for score in f1_scores if score <= 0.3)
            
            report.append("📈 SCORE DISTRIBUTION")
            report.append("-" * 40)
            report.append(f"Perfect Exact Matches: {perfect_em}/{len(individual_results)} ({perfect_em/len(individual_results)*100:.1f}%)")
            report.append(f"Good F1 (≥0.7): {good_f1}/{len(individual_results)} ({good_f1/len(individual_results)*100:.1f}%)")
            report.append(f"Poor F1 (≤0.3): {poor_f1}/{len(individual_results)} ({poor_f1/len(individual_results)*100:.1f}%)")
            report.append("")
        
        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        full_report = "\n".join(report)
        
        # Save report if path provided
        if save_path:
            save_path = Path(save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(full_report)
            
            # Also save detailed results as JSON
            json_path = save_path.with_suffix('.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
            
            logger.info(f"📄 Report saved to {save_path}")
            logger.info(f"📊 Detailed results saved to {json_path}")
        
        return full_report
    
    def save_results(self, evaluation_results: Dict[str, Any], path: Path):
        """Save evaluation results to file"""
        path.mkdir(parents=True, exist_ok=True)
        
        # Save summary
        summary_file = path / "evaluation_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(self.generate_report(evaluation_results))
        
        # Save detailed results
        results_file = path / "detailed_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(evaluation_results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"💾 Evaluation results saved to {path}")