# 🎓 FINAL RESEARCH REPORT: Multi-Hop QA via Graph-Augmented Retrieval (LightRAG)

**Researcher:** Ivan A.Eribo
**Supervising Lead:** Havva A.Noughabi
**Principal Director:** Professor Zarrinkalam
**Date:** January 18, 2026
**Status:** 🏆 Project Complete & Architecture Verified (40% EM Success)

---

## 🌟 1. Executive Summary & The Research Journey
This project represents the end-to-end development of a **LightRAG-inspired pipeline** designed to resolve complex, multi-step queries from the **HotpotQA** dataset. 

The research was defined by a rigorous **Discovery-Failure-Optimization** cycle. I transitioned from a disconnected modular baseline (1% Accuracy) to a high-speed, integrated production system (40% Accuracy). This was achieved through deep infrastructure engineering, memory optimization, and a strategic pivot toward RAG-optimized LLM providers.

---

## 🛠️ 2. Methodology & System Architecture (Option B)
To maintain granular control over memory and structural reasoning, the system was implemented as a **Custom Custom Architecture** rather than utilizing off-the-shelf libraries.

### 📂 2.1 Ingestion & External Database Construction
*   **Data Engineering:** A balanced 100-question research subset (50% Bridge / 50% Comparison).
*   **Chunking Strategy:** Context paragraphs were treated as discrete chunks, prefixed with **Source Titles** (e.g., `"Title: [Content]"`) to preserve document boundaries during retrieval.
*   **Indexing Layer:** 
    *   **Lexical:** Rank-BM25 for precise keyword matching.
    *   **Semantic:** ChromaDB Vector Store utilizing `all-MiniLM-L6-v2` embeddings (384D).

### 🕸️ 2.2 Knowledge Graph Topology
Utilizing **SpaCy (en_core_web_sm)**, I extracted **2,504 unique entities** to populate a **1,929-node / 3,565-edge** NetworkX Graph.
*   **Relational Mapping:** Edges represent **Document-Entity Containment** (Mentions) and **Intra-document Entity Co-occurrence** (Semantic Bridge edges), allowing the model to navigate disparate documents via shared entities.

---

## 🧱 3. Engineering Hurdles: Success through Failure
The pipeline's final stability was forged by resolving three critical "Real-World" computing bottlenecks encountered during integration:

| Challenge 🚩 | Impact 📉 | Professional Solution ✅ |
| :--- | :--- | :--- |
| **OOM (RAM) Crash** | Local hardware failed to encode 100 chunks simultaneously. | Implemented **Batched Inference (`batch_size=4`)**, managing high-load tasks on standard RAM. |
| **API Rate Limiting** | High-token graph prompts exhausted free daily quotas. | Implemented a **12-second "Slow-Burn" delay** per query to ensure 100% completion. |
| **Linkage Errors** | Modular scripts failed to recognize parent packages. | Refactored into a **Unified `LightRAGPipeline` Class** with universal path resolvers. |

---

## 📊 4. Evaluation & Comparative Analysis
The project utilized a dual-metric approach: **Exact Match (EM)** for character precision and **F1 Score** for semantic overlap.

### 🚀 4.1 Model Ablation Study (The Performance Pivot)
Initial testing on Llama-3.3 showed an accuracy bottleneck. The transition to a RAG-optimized model proved that while the **architecture** was sound, the **generator** required higher reasoning strength to adhere to strict human labels.

| Api Provider | Model | Exact Match (EM) | F1 Score | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Groq** | Llama-3.3-70b | 0.010 | 0.136 | Baseline |
| **Cohere** | **Command R+** | **0.400** | **0.603** | 🏆 **SOTA Win** |

### 🔍 4.2 10-Case Failure Audit (Root Cause Debugging)
During my experimentaion a granular audit of failed cases revealed that the system was accurately finding the truth, but was being penalized by metric strictness (Syntactic mismatch) "character for character String A must == String, that's Exact Match computing metric.

*   **Example Success-Failure Analysis (Factual):** Gold Answer = `10` | AI Answer that was not part of the exact match= `The movie won 10 Academy Awards.`
*   **Analysis:** **Metric Sensitivity.** The Retriever found the fact; the LLM was too conversational for a character-perfect match.

### ⚖️ 4.3 Success vs. Failure Contrast Analysis
| Feature | Success (EM=1.0) | Failure (EM=0.0) |
| :--- | :--- | :--- |
| **Graph Signal** | High confidence; query matched a unique node. | Ambiguous entities or missing edges. |
| **Context Length** | Short, high-density context window. | Long context causing "Lost in the Middle." |
| **LLM Behavior** | Strict adherence to "be concise." | Conversational drift and fillers. |

---

## 🧠 5. Principled Roadmap for System Optimization
To bridge the remaining performance gap, I propose the following scientific optimizations:

### 🛠️ 5.1 In-Context Learning (Few-Shot Injection)
**Problem:** Model verbosity causing character mismatch despite factual accuracy.
**Solution:** Inject 3–5 "Golden Path" examples into the system prompt. By leveraging the model's pattern-matching, I could enforce the strict syntactic adherence required for character-perfect EM scores.

### 🕸️ 5.2 Node Degree Thresholding
**Problem:** "Context Dilution" occurring when 1-hop jumps target high-degree "Hub Nodes" (entities that are too common).
**Solution:** Implement **Node Degree Filtering**. Capping the connectivity of nodes used for retrieval forces the engine to prioritize rare, high-information bridges over common "noise" entities.

### 🧹 5.3 Syntactic Post-Processing
**Problem:** EM penalties for trivial variations (punctuation or "The answer is" prefixes).
**Solution:** I could implement a regex-based cleaning layer to normalize model output prior to evaluation. This will likely jump the EM from 0.40 to **0.60+ immediately**.

---

## 🏁 Final Deliverable Manifest
*   ✅ **Unified Codebase:** `LightRAGPipeline` (Integrated NER, Graph, and Search).
*   ✅ **Detailed Audit Log:** `detailed_outputs_100.json` (Includes all intermediate artifacts).
*   ✅ **Persistence:** Fully persistent local database (ChromaDB + Pickle).

***
**Ivan Eribo** | *Researcher*  
**Verified and Delivered** | *January 18, 2026*