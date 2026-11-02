# Video script: Rebuild Your RAG with LangChain (about 9 minutes; section times are approximate)

Notebook open with saved outputs. **[SCREEN]** lines say what to show. Everything else is read aloud.

---

## 1. Intro (0:00–0:30)

**[SCREEN]** Notebook title cell and the TODO table.

> Hi, I'm Dharmin Patel, and this is my mini project for IT 7075C: rebuilding my RAG system with LangChain.
> In the RAG module I built an incident-response bot by hand, over five playbook documents, tested with eight
> gold questions: six the documents answer and two they don't. Here I rebuilt it with LangChain on the same
> documents and questions, and compared the two. LangChain scored one question worse, and I'll show why at the end.

---

## 2. Parts 1–5: the five stages (0:30–3:30)

### TODO 1: Load and split (0:30–1:05)

**[SCREEN]** Part 1 code cell, then its output: `ssrf.txt -> 13 chunks`, `cybersecurity_kb.md -> 10 chunks`, `TOTAL: 23 chunks`.

> Parts 1 to 5 are the five TODOs, which I practised on the course documents first. TODO 1 loads and splits.
> `TextLoader` reads each file into a `Document`, and `RecursiveCharacterTextSplitter` cuts it into overlapping
> chunks. This replaces my `split_into_chunks()` loop. I also no longer keep a separate `sources` list: the
> loader puts the file path in the metadata, and the splitter copies it onto every chunk. 23 chunks in total.

### TODO 2: Vector store (1:05–1:35)

**[SCREEN]** Part 2 cell. Point at `collection_metadata={"hnsw:space": "cosine"}`. Output: `Stored 23 chunks`.

> TODO 2 builds the vector store. `HuggingFaceEmbeddings` wraps the same model as before, `all-MiniLM-L6-v2`,
> and `Chroma.from_documents` embeds and stores every chunk in one call. That replaces my `embed()` function
> and `collection.add()`. The line to notice is this one: cosine space. Chroma's default is L2, and if I left
> this out nothing would crash, but every threshold would quietly mean something different.

### TODO 3: Retriever (1:35–2:20)

**[SCREEN]** Part 3 cell, then the kept/dropped output for the SSRF question and the France question.

> TODO 3 is the retriever, which replaces my `retrieve()` function. And this is the first real gotcha: the
> threshold works in the opposite direction. My RAG module kept hits whose distance was at most 0.75.
> LangChain keeps hits whose relevance score is at least a threshold, where higher means more similar. For
> cosine, LangChain computes relevance as one minus distance, so my max distance of 0.75 becomes a score
> threshold of 0.25. The cell asserts that relevance really equals one minus distance, so the conversion is
> checked, not assumed.
>
> Here's what that looks like. For "Is SSRF limited to HTTP?", four chunks are kept; the top one has relevance
> 0.79. For "What is the capital of France?", the best chunk has relevance 0.07, distance 0.93, so everything
> is dropped and the retriever returns nothing. That empty list is how my bot knows to refuse.

### TODO 4: Prompt template (2:20–2:50)

**[SCREEN]** Part 4 cell and the printed prompt showing `# Context`, `[1] (source: demo.md)` and `Human: A question?`.

> TODO 4 is the prompt template. It has the same instructions as my old `SYSTEM` string: answer only from the
> context, cite the source file, start with `[RAG]` if the answer is in the context, and if it isn't, say you
> don't know instead of answering from memory. The difference is that it's a `ChatPromptTemplate` with two
> placeholders, `{context}` and `{question}`, filled in here with test values.

### TODO 5: The chain (2:50–3:30)

**[SCREEN]** Part 5 cell, then the output: the SSRF answer starting with `[RAG]` and the Log4Shell answer starting with `[LLM] I don't know`.

> TODO 5 wires everything into one chain, and it reads left to right. The question goes into a dictionary:
> the `context` key sends it through the retriever and `format_docs`, and the `question` key passes it straight
> through. That fills the prompt, the prompt goes to the model, and `StrOutputParser` pulls out the text. This
> replaces `ask()` and `generate()`. The model is `gpt-4o-mini` if an API key is set, with an offline
> stand-in as a fallback; this run is offline. The SSRF question is answered from context; Log4Shell isn't
> covered, so it says it doesn't know.

**[SCREEN]** Part 6 output: `found 5/6, refused 2/2`.

> Scored on the course questions, the practice pipeline found 5 of 6 and refused both unanswerable ones.

---

## 3. Part 7: parallel vs branch (3:30–4:15)

**[SCREEN]** Part 7 cell. Point at `RunnableParallel(docs=retriever, question=...)` and then `RunnableBranch`. Output: `{'answer': '[REFUSED] ...', 'sources': []}`.

> Part 7 is about parallel versus branch. The dictionary at the start of my chain is already a
> `RunnableParallel`: retrieval and the question pass-through both get the same input and run independently.
> A branch is different: only one path runs, chosen by a condition. My guarded chain fetches the documents,
> then branches. If nothing came back, it returns a fixed refusal and never calls the model. That matters for
> security: the refusal no longer depends on the model obeying its instructions, so a prompt injection can't
> talk it into answering. It also returns the source files with every answer.

---

## 4. Parts 8–9: my bot on my documents (4:15–5:45)

**[SCREEN]** Part 8 output: the hash table with `same: True` on all six files.

> From Part 8 on, it's my own knowledge base. To make the comparison fair, the first cell hashes all five
> documents and the gold set against the RAG module's originals, and all six say `same: True`.

**[SCREEN]** Part 9: `25 chunks stored`, then scroll through the transcript. Stop on Q2, then Q7.

> Part 9 runs the bot with the same baseline settings as the RAG module: chunk size 600, overlap 100, k of 4,
> and a score threshold of 0.25. Notice it made 25 chunks; my hand-built splitter made 22 from the same text.
> Keep that in mind, it's the whole story later.
>
> In the transcript, Q2, "How quickly do we acknowledge a SEV1 incident?", comes back from the severity-levels
> document: "Acknowledge within 15 minutes, at any hour." Q7, banana bread, is refused, with no model call.

**[SCREEN]** Per-question table under Part 9.

> This table shows the nearest chunk for each question. Baseline result: found 5 out of 6, refused 1 out of
> 2. Two questions are wrong: Q3, which should have been found, and Q8, the DDoS question, which should have
> been refused.

---

## 5. Parts 10–11: the comparison (5:45–7:15)

**[SCREEN]** Part 10 cell: the `SWEEPS` dictionary, then `Saved results_langchain.csv (25 configurations)`.

> Part 10 changes one setting at a time: chunk size, k, and the threshold, using the RAG module's distances
> converted. Plus a fourth sweep that swaps the splitter. 25 configurations in total.

**[SCREEN]** Part 11: the like-for-like row.

> Part 11 lines each row up with the matching RAG module row. Like for like, at the baseline: the hand-built
> version found 6 and refused 1. LangChain found 5 and refused 1. Same documents, same embedding model, same
> settings, so where does the gap come from?

**[SCREEN]** Part 10 results: the two `splitter` rows, `recursive 25 chunks 5/1` and `character 21 chunks 6/1`.

> The splitter row answers it. If I swap in `CharacterTextSplitter` with no separator, which cuts fixed
> 600-character windows like my old code, LangChain goes back to 6 and 1, and every question's nearest
> distance matches the RAG module to three decimal places. So the framework isn't worse at retrieval. The
> entire difference is where the chunks were cut.

**[SCREEN]** The comparison figure, three panels.

> On the chart, grey is the RAG module. At k of 1, LangChain actually does better, 4 versus 3, because its
> section-aligned chunks moved Q1 and Q6 to rank 1. But it needs k of 8 to find all six, where the RAG module
> needed 3. And on the threshold it's stuck at 5 however loose I go, because a looser threshold can't bring
> back a chunk that k already cut off. So the recursive splitter helped some questions and hurt one.

---

## 6. Part 12: why Q3 was wrong (7:15–8:15)

**[SCREEN]** Part 12 output for Q3: ranks 1–4, then rank 8 with the evidence.

> That one question is Q3: "A user typed their password into a phishing page. How far back should we review
> their sign-in logs?" The answer is 14 days. All four retrieved chunks came from the right file, the phishing
> playbook, but none of them had the answer. The chunk with the evidence came eighth, with a relevance of
> 0.275.

**[SCREEN]** Part 12 side-by-side cell: the recursive cut, then the character cut.

> This cell shows why. The recursive splitter broke at the blank line before the numbered list. So the heading
> "If credentials were entered" and the sentence "Treat any user who typed a password into the phishing page"
> stayed at the end of the previous chunk, and the evidence chunk starts at "1. Reset the user's password".
> The overlap didn't save it: the recursive splitter only overlaps whole pieces, and that sentence is about
> 120 characters, longer than the 100-character overlap. The chunk kept the answer but lost the words of the
> question. The fixed-window splitter happened to keep them together, and scored 0.483.
>
> Larger chunks, a bigger overlap, splitting on Markdown headings, or k of 8 all fix it. Q8, the DDoS question, is wrong in both
> versions: the phishing playbook header looks generically like any "steps in our playbook" question, and a
> vector distance can't insist on the word "DDoS".

---

## 7. Close (8:15–8:45)

**[SCREEN]** The Summary cell, or the report PDF, Section 6.

> To wrap up: LangChain made the pipeline shorter and every stage swappable. But it hid how chunks were cut
> and how scores were computed, and for a security team that's an audit problem: if the bot gives an analyst
> the wrong containment step, you need to know which chunk it used and at what score. Next time I'd use
> LangChain, but choose the splitter on purpose and log relevance scores next to every answer. Thanks for watching.
