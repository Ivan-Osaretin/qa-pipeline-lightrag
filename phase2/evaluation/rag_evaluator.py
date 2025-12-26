"""
RAG EVALUATOR - Comprehensive evaluation metrics
"""
import numpy as np
from typing import List, Dict, Any, Tuple
import re
from sklearn.metrics import f1_score
from loguru import logger

class RAGEvaluator:
    """Comprehensive evaluation for RAG systems"""
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize text for comparison"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = ' '.join(text.split())  # Normalize whitespace
        return text
    
    @staticmethod
    def exact_match(predicted: str, gold: str) -> float:
        """Exact match (case-insensitive, punctuation-insensitive)"""
        pred_norm = RAGEvaluator.normalize_text(predicted)
        gold_norm = RAGEvaluator.normalize_text(gold)
        return 1.0 if pred_norm == gold_norm else 0.0
    
    @staticmethod
    def f1_score_qa(predicted: str, gold: str) -> float:
        """F1 score based on token overlap"""
        pred_tokens = set(RAGEvaluator.normalize_text(predicted).split())
        gold_tokens = set(RAGEvaluator.normalize_text(gold).split())
        
        if not pred_tokens or not gold_tokens:
            return 0.0
        
        # Calculates precision and recall
        common = pred_tokens.intersection(gold_tokens)
        precision = len(common) / len(pred_tokens)
        recall = len(common) / len(gold_tokens)
        
        if precision + recall == 0:
            return 0.0
        
        return 2 * (precision * recall) / (precision + recall)
    
    @staticmethod
    def contains_answer(predicted: str, gold: str) -> float:
        """Check if predicted contains gold answer"""
        pred_norm = RAGEvaluator.normalize_text(predicted)
        gold_norm = RAGEvaluator.normalize_text(gold)
        
        # Splits gold into words
        gold_words = gold_norm.split()
        if not gold_words:
            return 0.0
        
        # Checks how many gold words are in predicted
        matches = sum(1 for word in gold_words if word in pred_norm)
        return matches / len(gold_words)
    
    def evaluate_single(self, predicted: str, gold: str) -> Dict[str, float]:
        """Evaluates single prediction"""
        return {
            'exact_match': self.exact_match(predicted, gold),
            'f1_score': self.f1_score_qa(predicted, gold),
            'contains_score': self.contains_answer(predicted, gold)
        }
    
    def evaluate_batch(self, 
                      predictions: List[str], 
                      golds: List[str],
                      return_details: bool = False) -> Dict[str, Any]:
        """Evaluates batch of predictions"""
        if len(predictions) != len(golds):
            logger.error(f"Mismatch: {len(predictions)} predictions vs {len(golds)} golds")
            return {}
        
        em_scores = []
        f1_scores = []
        contains_scores = []
        
        details = [] if return_details else None
        
        logger.info(f"Evaluating {len(predictions)} predictions...")
        
        for i, (pred, gold) in enumerate(zip(predictions, golds)):
            result = self.evaluate_single(pred, gold)
            em_scores.append(result['exact_match'])
            f1_scores.append(result['f1_score'])
            contains_scores.append(result['contains_score'])
            
            if return_details and i < 10:  # Store details for first 10
                details.append({
                    'prediction': pred,
                    'gold': gold,
                    'exact_match': result['exact_match'],
                    'f1_score': result['f1_score'],
                    'contains_score': result['contains_score']
                })
        
        results = {
            'exact_match': {
                'mean': float(np.mean(em_scores)),
                'std': float(np.std(em_scores)),
                'median': float(np.median(em_scores))
            },
            'f1_score': {
                'mean': float(np.mean(f1_scores)),
                'std': float(np.std(f1_scores)),
                'median': float(np.median(f1_scores))
            },
            'contains_score': {
                'mean': float(np.mean(contains_scores)),
                'std': float(np.std(contains_scores)),
                'median': float(np.median(contains_scores))
            },
            'num_examples': len(predictions)
        }
        
        if return_details:
            results['details'] = details
        
        return results
    
    def generate_report(self, 
                       evaluation_results: Dict[str, Any],
                       model_name: str = "LightRAG",
                       save_path: str = None) -> str:
        """Generates professional evaluation report"""
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append(f"RAG EVALUATION REPORT - {model_name}")
        report_lines.append("=" * 80)
        report_lines.append(f"Number of examples: {evaluation_results.get('num_examples', 0)}")
        report_lines.append("")
        
        # Metrics section
        report_lines.append("📊 EVALUATION METRICS")
        report_lines.append("-" * 40)
        
        for metric_name in ['exact_match', 'f1_score', 'contains_score']:
            if metric_name in evaluation_results:
                metric = evaluation_results[metric_name]
                report_lines.append(f"{metric_name.replace('_', ' ').title()}:")
                report_lines.append(f"  Mean:   {metric['mean']:.3f}")
                report_lines.append(f"  Std:    {metric['std']:.3f}")
                report_lines.append(f"  Median: {metric['median']:.3f}")
                report_lines.append("")
        
        # Details section
        if 'details' in evaluation_results and evaluation_results['details']:
            report_lines.append("📋 SAMPLE EVALUATIONS")
            report_lines.append("-" * 40)
            
            for i, detail in enumerate(evaluation_results['details'][:5]):
                report_lines.append(f"Example {i+1}:")
                report_lines.append(f"  Gold: {detail['gold'][:80]}...")
                report_lines.append(f"  Pred: {detail['prediction'][:80]}...")
                report_lines.append(f"  Scores: EM={detail['exact_match']:.3f}, F1={detail['f1_score']:.3f}, Contains={detail['contains_score']:.3f}")
                report_lines.append("")
        
        # Summary
        report_lines.append("📈 SUMMARY")
        report_lines.append("-" * 40)
        
        # Calculates overall score (weighted average)
        weights = {'exact_match': 0.4, 'f1_score': 0.4, 'contains_score': 0.2}
        overall_score = 0
        for metric_name, weight in weights.items():
            if metric_name in evaluation_results:
                overall_score += evaluation_results[metric_name]['mean'] * weight
        
        report_lines.append(f"Overall Score: {overall_score:.3f}")
        report_lines.append("")
        
        # Interpretation ability based on overall score
        if overall_score >= 0.7:
            report_lines.append("✅ EXCELLENT: Model performs very well")
        elif overall_score >= 0.5:
            report_lines.append("⚠️  GOOD: Model performs reasonably well")
        elif overall_score >= 0.3:
            report_lines.append("📉 FAIR: Room for improvement")
        else:
            report_lines.append("❌ POOR: Significant improvement needed")
        
        report_lines.append("=" * 80)
        
        full_report = '\n'.join(report_lines)
        
        # Save if path provided
        if save_path:
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(full_report)
            logger.info(f"Report saved to {save_path}")
        
        return full_report