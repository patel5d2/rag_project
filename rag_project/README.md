# RAG for an Incident Response Playbook

A small retrieval-augmented generation (RAG) system, built from scratch for IT7075 Applied AI for
Cybersecurity, that answers questions about a fictional organization's incident response
playbook. Five documents I wrote myself (`my_kb/`) are split into overlapping chunks. Each chunk is
embedded locally with `all-MiniLM-L6-v2` and stored in ChromaDB. For each question the system
retrieves the closest chunks, drops any match that is too weak, and answers only from what it retrieved,
or says it does not know. Eight gold questions (`goldset.json`) measure two things: how many answers
it finds and how many unanswerable questions it correctly refuses. The experiments vary chunk size,
the number of chunks retrieved (k), and the distance threshold.

| File | What it is |
|------|------------|
| `rag_notebook.ipynb` | The whole project, run top to bottom with outputs saved. Parts 1–5 are the course practice pipeline; Part 6 onward is my RAG. |
| `my_kb/` | My five knowledge-base documents; `SOURCES.md` says where each came from. |
| `goldset.json` | Eight questions: 6 the documents answer, 2 they do not. |
| `results.csv` / `figure.png` | Experiment results and chart. |
| `course_kb/`, `baseline_goldset.json` | Course documents and questions used by the Part 1–5 practice cells. |

**Run it:** `pip install -r requirements.txt`, then open the notebook and run all cells. It runs
offline on CPU with no API key needed. If `OPENAI_API_KEY` is set (in `.env` or the environment, never in the
notebook), the generate step uses `gpt-4o-mini` instead of the offline answer.
