# 1. Create lightrag_graph_simple.py
$graphCode = @"
"""
ULTRA-SIMPLE Graph - Just to get something running
"""
import networkx as nx
import pickle
from pathlib import Path

class LightRAGGraphSimple:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_from_chunks(self, chunks):
        """Just add nodes - no entities, no relationships"""
        print(f"Building simple graph from {len(chunks)} chunks")
        
        for i, chunk in enumerate(chunks[:10]):  # Just 10 for testing
            self.graph.add_node(
                f"chunk_{i}",
                text=chunk.get('text', '')[:100],
                type="chunk"
            )
        
        print(f"Built graph with {self.graph.number_of_nodes()} nodes")
        return self.graph
    
    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self.graph, f)
        print(f"Saved graph to {path}")
"@

$graphCode | Out-File -FilePath "phase2/graph_indexing/lightrag_graph_simple.py" -Encoding utf8
Write-Host "✅ Created phase2/graph_indexing/lightrag_graph_simple.py" -ForegroundColor Green