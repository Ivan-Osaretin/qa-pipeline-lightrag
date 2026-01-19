import pickle
from pathlib import Path
from loguru import logger

class ReasoningEngine:
    def __init__(self, graph_path: str, retriever):
        self.retriever = retriever
        with open(graph_path, 'rb') as f:
            self.graph = pickle.load(f)
        logger.info(f'✅ Graph Loaded: {self.graph.number_of_nodes()} nodes')

    def discover_graph_context(self, question: str) -> str:
        found_context = []
        for node_id, data in self.graph.nodes(data=True):
            if data.get('type') == 'entity':
                entity_name = data.get('text', '').lower()
                if entity_name and entity_name in question.lower():
                    neighbors = list(self.graph.neighbors(node_id))
                    for n_id in neighbors[:3]:
                        n_data = self.graph.nodes[n_id]
                        if 'full_text' in n_data:
                            found_context.append(n_data['full_text'])
        return '\n'.join(list(set(found_context)))[:2000]

    def run_rag_pipeline(self, question: str, llm_client) -> str:
        vector_results = self.retriever.retrieve(question, top_k=3)
        vector_context = '\n'.join([r['text'] for r in vector_results])
        graph_context = self.discover_graph_context(question)
        
        system_msg = 'Answer the multi-hop question using provided context. Be concise.'
        user_msg = f'CONTEXT:\n{vector_context}\n\nRELATED:\n{graph_context}\n\nQ: {question}\nA:'
        return llm_client.generate_answer(system_msg, user_msg)
