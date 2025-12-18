"""
Simplified Text Preprocessor for Phase 1
"""
import json
from pathlib import Path

class TextPreprocessor:
    """Basic text preprocessing for Phase 1."""
    
    def __init__(self):
        print("TextPreprocessor initialized")
    
    def prepare_for_graphrag(self, examples):
        """Prepare examples for GraphRAG indexing."""
        print(f"Preparing {len(examples)} examples for GraphRAG...")
        
        processed_data = []
        for example in examples:
            processed_example = {
                'id': example.get('id', ''),
                'question': example.get('question', ''),
                'answer': example.get('answer', ''),
                'type': example.get('type', ''),
                'level': example.get('level', ''),
                'supporting_facts': example.get('supporting_facts', []),
                'context': example.get('context', []),
                'gold_paragraphs': self._extract_gold_paragraphs(example),
                'all_context': self._combine_all_context(example)
            }
            processed_data.append(processed_example)
        
        return processed_data
    
    def _extract_gold_paragraphs(self, example):
        """Extract gold supporting paragraphs."""
        gold_titles = {fact[0] for fact in example.get('supporting_facts', [])}
        gold_paragraphs = []
        
        for title, sentences in example.get('context', []):
            if title in gold_titles:
                gold_paragraphs.append(' '.join(sentences))
        
        return gold_paragraphs
    
    def _combine_all_context(self, example):
        """Combine all context text."""
        all_text = []
        for title, sentences in example.get('context', []):
            all_text.append(' '.join(sentences))
        
        return ' '.join(all_text)
