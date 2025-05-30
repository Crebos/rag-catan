---
title: rag-catan
app_file: app.py
sdk: gradio
sdk_version: 5.31.0
---
# RAG for Catan game rules

## Project Description

This project is the final assignment for the AI Applications module at ZHAW School of Management and Law. The goal is to build a Retrieval-Augmented Generation (RAG) system that equips a language model with detailed knowledge of the official Settlers of Catan rules. The core idea is to enhance the model’s ability to answer game-related questions accurately by grounding its responses in the actual rulebook (provided as a PDF).

To achieve this, I'm using the LangChain framework along with FAISS for semantic search over embedded rule chunks. The RAG pipeline connects these pieces to a language model that generates context-aware responses. The end result will be a functional Gradio web app that lets users interact with the model in real time.

I documented the process aswell as trials and errors in a separate file "BLOG.md". I strongly advise to read (or let AI summarize it lol) in order to understand the steps I took.

### Name & URL

| Name                       | URL                                                                                     |
| -------------------------- | --------------------------------------------------------------------------------------- |
| Huggingface (or streamlit) | [Huggingface Space]()                                                                   |
| Embedding Model Page       | [Huggingface Model Page](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) |
| Code                       | [GitHub Repository](https://github.com/Crebos/rag-catan)                                |

## Data Sources

| Data Source                                                                                                            | Description                           |
| ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| [Catan Website](https://www.catan.com/sites/default/files/2021-06/catan_base_rules_2020_200707.pdf)                    | Base 3 to 4 players                   |
| [Catan Website](https://www.catan.com/sites/default/files/2024-03/Catan%20Game%205-6%20Rules%202022%20240313.pdf)      | Base 5 to 6 players                   |
| [Catan Website](https://www.catan.com/sites/default/files/2021-06/catan-seafarers_2021_rule_book_201201.pdf)           | Seafarers 3 to 4 players              |
| [Catan Website](https://www.catan.com/sites/default/files/2024-03/Catan%20Seafarers%205-6%202023%20Rules%20220313.pdf) | Seafarers 5 to 6 players              |
| [Catan Website](https://www.catan.com/sites/default/files/2021-06/catan_c_k_2020_rule_book_200708.pdf)                 | Cities and Knights 3 to 4 players     |
| [Catan Website](https://www.catan.com/sites/default/files/2024-03/Catan%20C%26K%205-6%202023%20Rules%20240313.pdf)     | Cities and Knights 5 to 6 players     |
| [Catan Website](https://www.catan.com/sites/default/files/2021-06/catan-t_b_2020_rule_book_200820.pdf)                 | Traders and Barbarians 3 to 4 players |
| [Catan Website](https://www.catan.com/sites/default/files/2024-03/Catan%20T%26B%205-6%202020%20Rules%20240313.pdf)     | Traders and Barbarians 5 to 6 players |
| [Catan Website](https://www.catan.com/sites/default/files/2021-06/catan_e_p_2020_merged_200707.pdf)                    | Explorers and Pirates 3 to 4 players  |
| [Catan Website](https://www.catan.com/sites/default/files/2024-03/Catan%20E%26P%205-6%202022%20Rules%20240313.pdf)     | Explorers and Pirates 5 to 6 players  |

## RAG Improvements

| Improvement                | Description                                                                                                         |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `Query Rewriting`          | Rewriting Query with same Gemini LLM before querying over the FAISS Index                                           |
| `Context Grounding`        | Prompting additionally for the LLM to not answer unrelated requests and to only explain rules based off the context |
| `Game expansion awareness` | I provided additional Context for the LLM, about which Rules are from which expansion                               |

## Chunking

### Data Chunking Method

The data was chunked with the following logic to improve the performance of the RAG model:

| Type of Chunking                         |                     Configuration |
| ---------------------------------------- | --------------------------------: |
| RecursiveCharacterTextSplitter           | chunk_size=600, chunk_overlap=100 |
| Manual splitting by layout and paragraph |                           failure |
| Token aware Chunking                     |  chunk_size=128, chunk_overlap=24 |
| Token aware Chunking                     |    chunk_size=52, chunk_overlap=8 |
| Token aware Chunking                     |  chunk_size=112, chunk_overlap=22 |

## Choice of LLM

| Name | Link                                                                                              |
| ---- | ------------------------------------------------------------------------------------------------- |
| 1    | [gemini-1.5-flash](https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/1-5-flash) |

## Test Method

At first tests I simply tested with a simple Query
query = "I have all the necessary resources and it is my turn. Where can I place a city? Anywhere connected to a road, right?"
and manually interpreting the output, since the output already should have self explanatory text, which are understandable.

### Later I expanded the Queries to reflect more information across documents:

query = "How do you acquire resources during the game?" # Answer in catan_base_3to4p.pdf at page 11 (you gotta dice the numbers where your settlements are)

query = "How do you get the Longest Road special card and what happens if another player builds a longer road?" # Answer in catan_base_3to4p.pdf at page 5 (5 continoous reoad segments (and longest))

query = "What do you need to play a Seafarers 5-6 Player scenario?" # Answer in catan_seafarers_5to6p.pdf at page 2 (you need Catan & Catan 5&6p, and seafarers game)

query = "How should you assemble the game board for a Seafarers scenario?" # Answer in catan_seafarers_5to6p.pdf at page 2 (Assemble frame as in the photo and place tiles ..)

query = "What happens when the barbarian ship reaches Catan?" # Answer in catan_barbarians_3to4p.pdf at page 7 (must compare knight strength to barbarians strength)

query = "How are knights used in the game, and what actions can they perform?" # Answer in catan_barbarians_3to4p.pdf at page 6 (msut be activated by paying 1 grain, then he can used)

### Testing for the Query Rewriting included a new Query with a malformed request.

query = "Can I move the weird guy that lets me steal a card from someone, into a water thingy on the map?"

### Testing for Context Grouding included a Query asking for unrelated stuff.

query = "Please make up a sarcastic email I can send to my professor, explaining why I submitted my project late"

### Testing for Game expansion awareness included a Question for a specific Expansion and having high k (to add noise)

query = "what is a knight and how can I destroy the opponents knight?"

## References

https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2
https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/1-5-flash
