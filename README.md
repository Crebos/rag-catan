# RAG for Catan game rules

## Project Description

This project is the final assignment for the AI Applications module at ZHAW School of Management and Law. The goal is to build a Retrieval-Augmented Generation (RAG) system that equips a language model with detailed knowledge of the official Settlers of Catan rules. The core idea is to enhance the model’s ability to answer game-related questions accurately by grounding its responses in the actual rulebook (provided as a PDF).

To achieve this, I'm using the LangChain framework along with FAISS for semantic search over embedded rule chunks. The RAG pipeline connects these pieces to a language model that generates context-aware responses. The end result will be a functional Gradio web app that lets users interact with the model in real time.

### Name & URL

| Name          | URL |
|---------------|-----|
| Huggingface (or streamlit)   | [Huggingface Space]() |
| Embedding Model Page    | [Huggingface Model Page](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| Code          | [GitHub Repository](https://github.com/Crebos/rag-catan) |

## Data Sources

| Data Source | Description |
|-------------|-------------|
| [Catan Website](https://www.catan.com/understand-catan/game-rules/) | Official Settlers of Catan Website with rulebooks  |

## RAG Improvements

| Improvement                     | Description |
|-----------------------------------|-------------|
| `Query Expansion`          | Generate extra queries to expand search |
| `Query Rewriting`              | Rewrite queries to yield better result |
| `Result reranking` | Reranked the top 10 results with another model |

## Chunking

### Data Chunking Method

The data was chunked with the following logic to improve the performance of the RAG model:

| Type of Chunking  | Configuration |
|------------|---------------:|
| RecursiveCharacterTextSplitter      | chunk_size=600, chunk_overlap=100         |
| Manual splitting by layout and paragraph |            |

## Choice of LLM

| Name | Link |
|-------|---------------|
| 1     |     |

(Add rows if you combine multiple models or compared their performance.)

## Test Method

At first tests I simply tested with a simple Query
query = "I have all the necessary resources and it is my turn. Where can I place a city? Anywhere connected to a road, right?"
and manually interpreting the output, since the output already should have self explanatory text, which are understandable. 

## Results

| Model/Method                                                         | Accuracy | Precision | Recall |
|----------------------------------------------------------------------|----------|-----------|--------|
|Retrieved chunks with config xyz |  -    | -         | -      |
| Generated answer with config xyz  | -      | -         | -      |

## References

