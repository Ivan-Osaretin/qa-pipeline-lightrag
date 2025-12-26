"""
PHASE 2 - LIGHTRAG GRAPH CONSTRUCTION
Definitive Version: Fixed constructor and enhanced query logic.
"""
import networkx as nx
from typing import List, Dict, Any, Set
from dataclasses import dataclass
from loguru import logger
import pickle
from pathlib import Path
from .entity_extractor import ExtractedEntity

class LightRAGGraph:
    """LightRAG knowledge graph implementation"""
    
    def __init__(self, graph_name: str = "hotpotqa_knowledge_graph"):
        # Fixed: now accepts graph_name to match scaling script calls
        self.graph = nx.Graph(name=graph_name)
        self.node_counter = 0
        logger.info(f"Initialized LightRAG Graph: {graph_name}")
    
    def add_entity_node(self, entity: ExtractedEntity) -> str:
        node_id = f"entity_{entity.text.lower().replace(' ', '_')}"
        if node_id not in self.graph:
            self.graph.add_node(
                node_id,
                type="entity",
                text=entity.text,
                label=entity.label,
                metadata={"entity_type": entity.label, "chunk_id": entity.chunk_id}
            )
            self.node_counter += 1
        return node_id
    
    def add_chunk_node(self, chunk: Dict) -> str:
        chunk_id = chunk.get("chunk_id", f"chunk_{self.node_counter}")
        self.graph.add_node(
            chunk_id,
            type="chunk",
            text=chunk.get("text", "")[:200],
            full_text=chunk.get("text", ""),
            metadata={"source": "hotpotqa"}
        )
        self.node_counter += 1
        return chunk_id
    
    def add_relationship(self, source_id: str, target_id: str, relation: str = "mentions", weight: float = 1.0):
        if source_id in self.graph and target_id in self.graph:
            self.graph.add_edge(source_id, target_id, relation=relation, weight=weight)
    
    def build_from_entities(self, chunks: List[Dict], entities: Dict[str, List[ExtractedEntity]]) -> nx.Graph:
        chunk_nodes = {c.get("chunk_id"): self.add_chunk_node(c) for c in chunks}
        for chunk_id, entity_list in entities.items():
            if chunk_id in chunk_nodes:
                c_node = chunk_nodes[chunk_id]
                for ent in entity_list:
                    e_node = self.add_entity_node(ent)
                    self.add_relationship(c_node, e_node, "contains", 0.9)
        self._connect_co_occurrences(entities)
        return self.graph

    def _connect_co_occurrences(self, entities: Dict[str, List[ExtractedEntity]]):
        for entity_list in entities.values():
            for i, e1 in enumerate(entity_list):
                for e2 in entity_list[i+1:]:
                    id1 = f"entity_{e1.text.lower().replace(' ', '_')}"
                    id2 = f"entity_{e2.text.lower().replace(' ', '_')}"
                    if id1 in self.graph and id2 in self.graph:
                        self.add_relationship(id1, id2, "co_occurs", 0.7)

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.graph, f)
        logger.info(f"💾 Graph saved to {path}")

    def query(self, query_text: str, max_results: int = 5) -> List[Dict]:
        query_lower = query_text.lower()
        results = []
        for node_id, data in self.graph.nodes(data=True):
            score = 0
            if query_lower in data.get('text', '').lower(): score += 1.0
            if query_lower in str(data.get('label', '')).lower(): score += 0.5
            if score > 0:
                results.append({'node_id': node_id, 'type': data.get('type'), 'text': data.get('text'), 'score': score})
        return sorted(results, key=lambda x: x['score'], reverse=True)[:max_results]
