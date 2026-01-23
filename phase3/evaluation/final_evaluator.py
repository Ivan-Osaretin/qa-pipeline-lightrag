import json
from loguru import logger
from phase2.evaluation.rag_evaluator import RAGEvaluator

class FinalEvaluator:
    def __init__(self):
        self.evaluator = RAGEvaluator()

    def run_final_audit(self, results_path: str):
        with open(results_path, 'r') as f:
            data = json.load(f)
        preds = [item['predicted_answer'] for item in data]
        golds = [item['gold_answer'] for item in data]
        return self.evaluator.evaluate_batch(preds, golds, return_details=True)
