# Video outline (5–10 min, live screen, notebook running)

1. **Intro (0:30).** Same incident-response bot as the RAG module, rebuilt with LangChain; same docs, same 8 questions.
2. **Parts 1–5, the five stages (3:00).** Run each cell and say what it replaced:
   - TODO 1 `TextLoader` + `RecursiveCharacterTextSplitter` → my `split_into_chunks()` loop. Metadata now travels with each chunk.
   - TODO 2 `Chroma.from_documents` → `embed()` + `collection.add()`. Point at `hnsw:space: cosine`.
   - TODO 3 retriever → `retrieve()`. **Opposite direction:** relevance ≥ 0.25 is distance ≤ 0.75; show the assert and kept/dropped for the France question.
   - TODO 4 prompt template → `SYSTEM` string; show the printed prompt with `{context}` and `{question}` filled.
   - TODO 5 the pipe chain → `ask()`; read the chain left to right.
3. **Part 7, branch vs parallel (0:45).** Retriever and question run in parallel; the branch refuses with no model call when nothing is retrieved.
4. **Parts 8–9, my bot (1:30).** Hash check shows the files are unchanged. Transcript: Q2 answered with its source, Q7 refused.
5. **Parts 10–11, the comparison (1:30).** Like-for-like row: 6/1 hand-built vs 5/1 LangChain. The splitter row brings it back to 6/1, so the chunks are the whole difference. Walk the chart.
6. **Part 12, Q3 wrong (1:00).** Evidence chunk is rank 8; show the side-by-side cut: the "typed a password into the phishing page" sentence stayed in the previous chunk.
7. **Close (0:30).** Next time: LangChain, but choose the splitter on purpose and log relevance scores next to every answer.
