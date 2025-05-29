# RAG for CATAN game rules

## Project Description



### Name & URL

| Name          | URL |
|---------------|-----|
| Huggingface (or streamlit)   | [Huggingface Space](https://huggingface.co/spaces/kuhs/ai-application-oxford-pets) |
| Embedding Model Page    | [Huggingface Model Page](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2) |
| Code          | [GitHub Repository](https://github.com/Jasminh/ai-application-rag) |

## Data Sources

| Data Source | Description |
|-------------|-------------|
| [Compendium](https://compendium.ch/) | Swiss Drug Registry  |
| Other data | We also included data of the NHS |

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
| RecursiveCharacterTextsplitter      | 1000 characters, 100 overlap         |
| I also tried this method | x, y           |
| I also tried this one       | x, y           |

## Choice of LLM

| Name | Link |
|-------|---------------|
| 1     | platformhttps://ai.google.dev/gemini-api/docs/models/gemini?hl=de#gemini-2.0-flash-lite     |

(Add rows if you combine multiple models or compared their performance.)

## Test Method

Detail how you selected or generated the test data and how you evaluated the performance of the model.

## Results

| Model/Method                                                         | Accuracy | Precision | Recall |
|----------------------------------------------------------------------|----------|-----------|--------|
|Retrieved chunks with config xyz |  -    | -         | -      |
| Generated answer with config xyz  | -      | -         | -      |

## References