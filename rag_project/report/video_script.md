# Video script: RAG for an Incident Response Playbook

Target: about 8 minutes, around 1,150 spoken words at a normal pace.
**[SCREEN]** lines tell you what to show. Everything else is what you say. Use it as a guide and say
it in your own words. It will sound more natural that way, and the assignment asks for that.

**Before you hit record**
- Open `rag_notebook.ipynb` in VS Code or Jupyter, with the `.venv` kernel selected
  (`rag_project/.venv/bin/python`). Don't use "ai-tools-setup", the notebook's saved default:
  it has no pandas, so it fails on the first cell.
- Close `.env` and anything else that holds a key. Nothing secret should be on screen.
- Run all cells once beforehand so the embedding model is downloaded and cached. That way the
  recorded run does not stall on a download.
- Have `my_kb/04_ransomware_playbook.md` and `figure.png` ready in tabs.

---

## 0:00 – 0:40 · Intro

**[SCREEN]** The notebook at the top. Click **Restart & Run All**, then keep talking while it runs.

> Hi, I'm Dharmin Patel, and this is my mini project for IT 7075, Applied AI for Cybersecurity. I
> built a retrieval-augmented generation system, a RAG, from scratch. No LangChain, just
> sentence-transformers for embeddings and ChromaDB as the vector database.
>
> My system answers questions about an incident response playbook for a fictional organization.
> I wrote five documents for it myself. I've just restarted the notebook and hit Run All, so
> everything you see is running live. I'll walk through it from top to bottom.

---

## 0:40 – 3:00 · Part 1: the pipeline, step by step

**[SCREEN]** Scroll to Part 1. Point at `embed()`.

> First, why RAG at all? A language model only knows its training data. It has never seen my
> playbook, so if I ask it how fast we must acknowledge a SEV1, it will make up a believable
> number. RAG fixes that by finding the right passage in my own documents first and giving it to
> the model with the question.
>
> Step one is embeddings. I use all-MiniLM-L6-v2, which runs locally on the CPU. It turns any text
> into 384 numbers, and texts with similar *meaning* end up close together, even when they share no
> words. I normalize the vectors and use cosine distance, so zero means identical and one means
> unrelated. The same model has to embed both the chunks and the question, or the distances mean
> nothing.

**[SCREEN]** Point at `split_into_chunks()` (TODO 1) and its output.

> TODO 1 is chunking. A whole document can't be one vector, because one vector can't represent ten
> topics. So I cut each document into 600-character pieces with a 100-character overlap. The overlap
> means a sentence that lands on a boundary still appears whole in one of the neighboring chunks.
> On the course documents that gives 11 plus 11, so 22 chunks, which is the expected number.

**[SCREEN]** Part 2, `build_collection()` (TODO 2). Show "Stored 22 chunks".

> TODO 2 stores them in ChromaDB. For each chunk it saves an ID, the text, the embedding, and
> metadata saying which file it came from. That metadata is what lets an answer cite its source.

**[SCREEN]** Part 3, `retrieve()` (TODO 3). Point at `if dist <= max_distance` and the two outputs.

> TODO 3 is retrieval. I embed the question and ask Chroma for the k closest chunks. The important
> line is this one: I throw away any hit farther than the threshold. Chroma *always* returns k
> results, however irrelevant they are. Without this filter the bot would answer anything. You can
> see it here: the SSRF question gets four hits around 0.36 to 0.43, and "What is the capital of
> France?" gets zero.

**[SCREEN]** Part 4, `build_context()` (TODO 4) and the `SYSTEM` prompt.

> TODO 4 is augmentation, which really is just building a string. Each retrieved chunk gets a number
> and its source file, and they go into the system prompt. The prompt says: answer only from this
> context, cite the file, and if the context is empty, say you don't know. If there are no hits I
> return an empty string, and that's what triggers the refusal. Generation then sends the prompt to
> the model. I don't have an API key set, so it runs in offline mode and quotes the retrieved text.
> With a key in `.env` it would use gpt-4o-mini. The key never goes in the notebook.

**[SCREEN]** Part 5, `score()` (TODO 5). Show "found 6/6, refused 2/2".

> TODO 5 is measurement. "Found" counts the answerable questions where a retrieved chunk contains the
> exact evidence phrase. "Refused" counts the unanswerable questions where nothing was retrieved. On
> the course data I get the expected 6 out of 6 found and 2 out of 2 refused.

---

## 3:00 – 4:00 · Part 2: my documents and questions

**[SCREEN]** Part 6, the load-and-check cell. Briefly flash the `my_kb/` folder and `SOURCES.md`.

> Now my own data. I chose incident response because playbooks are full of precise facts you can
> check: who decides, how fast, which tool, how long. And an analyst in the middle of an incident
> really does need to look these up quickly. I wrote five documents: an overview, severity levels,
> a phishing playbook, a ransomware playbook, and evidence handling. That's about 10,000
> characters, structured after NIST 800-61, CISA's ransomware guide, and RFC 3227, all
> paraphrased and cited in SOURCES.md.
>
> I wrote eight questions: six the documents answer and two they don't. This cell checks that every
> evidence phrase really appears word for word in its file, and all six say OK. I phrased the
> questions the way an analyst would ask them. Q5, for example, asks how to prove a disk image is
> an exact copy, and never says "hash".
>
> The two unanswerable ones are different on purpose. Q7, a banana bread recipe, is the easy one.
> Q8 asks for the steps in our DDoS playbook. It sounds exactly like my other questions, but my
> documents never mention DDoS.

---

## 4:00 – 5:15 · Part 3: answering one, refusing another

**[SCREEN]** The transcript cell. Scroll to **Q4**.

> Here's the system running on my data: 22 chunks stored, then the transcript. Look at Q4: "What
> should we do with the backup servers when ransomware is detected?" It retrieved four chunks, and
> the top one, from the ransomware playbook, says "Take the backup servers offline from the
> production network so the attacker cannot encrypt or delete them." That's the right answer, and
> it's tagged with its source file.

**[SCREEN]** Scroll to **Q7**.

> And here's a refusal. Q7, the banana bread question: "grounded? NO, nothing retrieved". The
> closest chunk was at 0.914, well past the threshold, so the context is empty and the system says
> "I don't know, the documents do not cover this." That's exactly the behavior I want.

**[SCREEN] (optional, but it shows the system is really live)** Add a new cell and run:
`ask(my_collection, "Can the response team decide on its own to pay a ransom?")`

> Let me ask one it hasn't seen before. "Can the response team decide on its own to pay a ransom?"
> It pulls the ransom payment section of the ransomware playbook: the policy is not to pay, and
> the decision is never made by the response team alone.

---

## 5:15 – 7:15 · Part 4: experiments and results

**[SCREEN]** The experiments cell, then the `results.csv` table, then the chart (`figure.png`).

> For the experiments I started from the lecture settings, chunk size 600, k 4, threshold 0.75, and
> changed one setting at a time. That's 23 configurations, saved to results.csv, and this is the
> chart. Blue is found out of six, red is refused out of two.
>
> **Chunk size:** at 450 characters and below, found drops to five. Q4 fails, because a chunk about
> *restoring* from backups outranks the one about taking backups *offline*. Both mention backups,
> and the right one gets pushed out of the top four.
>
> **k:** with k equal to 1, only three questions find their evidence. Q6 is interesting: its closest
> chunk starts mid-sentence and has lost the word "kept", so the full phrase is only in the
> overlapping chunk at rank three. From k equal to 3 onward, everything is found.
>
> **The threshold mattered most.** It's the only setting that changed refusals at all. At 0.40 it
> refuses both but finds only two answers. At 1.0 it finds all six but refuses nothing, not even
> banana bread. It has started guessing.

**[SCREEN]** The sorted-distance cell. Point at Q8 (0.494) sitting above Q3 (0.498).

> This cell shows why no threshold gets eight out of eight. It sorts the questions by the distance
> to their nearest chunk. Q8, the DDoS question, is at 0.494, which is *closer* than Q3, a real
> answerable question at 0.498. Any threshold that lets Q3 through also lets Q8 through. Distance
> alone can't separate them.
>
> The settings I'd use are chunk size 600, overlap 100, k 4, and threshold 0.65. That's the tightest
> threshold that still finds all six answers, and it keeps weaker, noisier chunks out of the prompt.

---

## 7:15 – 8:15 · What it got wrong, and limits

**[SCREEN]** The Q8 cell: the three retrieved chunks and `Does 'ddos' appear anywhere in my_kb? False`.

> So the question my system got wrong is Q8. Instead of nothing, it retrieved the header of the
> phishing playbook, then the header of the ransomware playbook. Those headers are generic:
> "Playbook", "Trigger", "this playbook starts when". The question asks for "the steps in our
> playbook for responding to an attack", which matches that shape almost perfectly. The one word
> that matters, DDoS, is a single token among many, and the vector can't insist that it appear.
> Retrieval answers "what text is most like this?", not "does this text contain the answer?".
>
> Threshold tuning can't fix that. Three things could: a real LLM in the generate step that reads the
> chunks and says they don't cover DDoS, hybrid search with keyword matching like BM25, or a
> cross-encoder re-ranker.
>
> One honest caveat: eight questions is a tiny sample, so each question moves a score by a big step.
> I also wrote both the documents and the questions, so real-world retrieval would probably do worse.

---

## 8:15 – 8:30 · Close

**[SCREEN]** Scroll back up quickly to show the notebook finished with all outputs, then show the repo.

> The notebook, my documents, the gold set, results.csv, the chart and the report are all in my
> private GitHub repository. Thanks for watching.
