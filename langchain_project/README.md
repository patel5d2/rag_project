# RAG Rebuilt with LangChain

The incident-response RAG from the RAG module (`../rag_project/`), rebuilt with LangChain on the same five documents
(`my_kb/`) and the same eight questions (`goldset.json`), then measured the same way and compared with the
hand-built version. `TextLoader` + `RecursiveCharacterTextSplitter` replace the chunking loop, `Chroma` +
`HuggingFaceEmbeddings` (`all-MiniLM-L6-v2`) replace the embed-and-add calls, a score-threshold retriever
replaces `retrieve()`, a `ChatPromptTemplate` replaces the prompt string, and a piped chain with a refusal
branch replaces `ask()`.

| File | What it is |
|------|------------|
| `langchain_notebook.ipynb` | Parts 1–7: practice TODOs on the course documents. Part 8 on: my RAG, experiments, comparison. Outputs saved. |
| `my_kb/`, `goldset.json` | Byte-identical copies of the RAG module's files (the notebook checks the hashes). |
| `results_langchain.csv` | 25 configurations: chunk size, k, score threshold, and splitter, one setting at a time. |
| `figure_comparison.png` | LangChain vs RAG module results on the same sweeps. |
| `report/` | Report source and PDF. |

**Run it:** from this folder, `pip install -r ../rag_project/requirements.txt langchain-core langchain-community
langchain-text-splitters langchain-chroma langchain-huggingface langchain-openai`, then open the notebook
from this folder and run all cells. It runs offline on CPU. If `OPENAI_API_KEY` is set in `.env` (never in the
notebook), the last stage of the chain uses `gpt-4o-mini`.
