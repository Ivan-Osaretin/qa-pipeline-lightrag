import numpy as np
import re
from loguru import logger

class RAGEvaluator:
    @staticmethod
    def normalize_text(text):
        return re.sub(r'[^\w\s]', '', text.lower().strip())

    def evaluate_batch(self, predictions, golds, return_details=False):
        em_scores = []
        f1_scores = []
        for p, g in zip(predictions, golds):
            p_norm, g_norm = self.normalize_text(str(p)), self.normalize_text(str(g))
            em_scores.append(1.0 if p_norm == g_norm else 0.0)
            
            p_tokens, g_tokens = set(p_norm.split()), set(g_norm.split())
            if not p_tokens or not g_tokens: 
                f1 = 0.0
            else:
                common = p_tokens.intersection(g_tokens)
                prec, rec = len(common)/len(p_tokens), len(common)/len(g_tokens)
                f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0
            f1_scores.append(f1)
            
        return {
            'exact_match': {'mean': np.mean(em_scores), 'std': np.std(em_scores)},
            'f1_score': {'mean': np.mean(f1_scores), 'std': np.std(f1_scores)},
            'num_examples': len(predictions)
        }

    def generate_report(self, results, model_name="LightRAG"):
        return f"# {model_name} Evaluation\n- EM: {results['exact_match']['mean']:.3f}\n- F1: {results['f1_score']['mean']:.3f}"
