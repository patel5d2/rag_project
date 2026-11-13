# Video script: Alert Triage Agent with LangGraph (about 9 minutes; section times are approximate)

**[SCREEN]** lines say what to show. Everything else is read aloud.

## Before recording

- Open `agent_notebook.ipynb` in VS Code with the `rag_project .venv` kernel. Zoom the editor so the output is readable.
- **Restart the kernel and clear all outputs**, then run each cell live as you reach it (Shift+Enter). The brief asks
  for the notebook "while it runs", not slides of screenshots.
- Keep `my_alerts.json` open in a second tab for section 7.
- Every number below is what the notebook prints. The agent is deterministic, so a live run gives the same output.

---

## 1. Intro (0:00–0:25)

**[SCREEN]** Title cell.

> Hi, I'm Dharmin Patel, and this is my IT 7075C mini project: an alert triage agent built with LangGraph. It reads a
> security alert and decides whether to escalate it to an analyst or close it. Every node is plain Python, with no
> model and no API key, so every number here is exact and comes out the same on every run.

---

## 2. Setup and the course alerts (0:25–0:45)

**[SCREEN]** Run the setup cell, then the course-alerts cell (`8 alerts, 4 real incidents`).

> Setup imports `StateGraph`, `START`, `END` and `MemorySaver`. Then there are eight course alerts, four real and four
> routine, and the lecture rule: escalate if the text contains one of five words, like "malware" or "exploit".
> `lookup_asset` is the tool, an ordinary function that returns a host's owner and criticality.

---

## 3. Parts 1–5: the five TODOs (0:45–2:15)

**[SCREEN]** Run Part 1. Point at `hits` and `decision`.

> TODO 1 is the state, one typed dictionary that travels through the graph. The alert brings its id, text and
> host. I added `hits`, which the triage node writes, and `decision`, which the last node writes.

**[SCREEN]** Run Part 2. Output: `{'hits': ['mimikatz']}`.

> TODO 2 is the triage node. It finds the keywords in the text and returns **only** the field it changed, `hits`, not
> the whole state. LangGraph merges that update into the state.

**[SCREEN]** Run Part 3. Output: `escalate close`.

> TODO 3, the router, is one line. It reads `hits` and returns a *label*. It doesn't run anything. It just names the branch.

**[SCREEN]** Run Part 4. Output shows `'criticality': 'high'`.

> TODO 4 is the escalate node, which calls the lookup tool. The tool sits only on the escalation branch, because an
> analyst needs the owner of an escalated host and nobody needs it for a closed alert.

**[SCREEN]** Run Part 5. Point at `add_edge(START, ...)`, `add_conditional_edges`, `compile()`, then the dotted lines in the Mermaid output.

> TODO 5 wires it up: `START` to triage, then the conditional edge, which attaches the router to triage and maps each
> label to a node. Both branches go to `END`, which stops the run and returns the final state. In the drawing, the
> dotted arrows are the conditional edge, and that's where the agent decides.

---

## 4. Parts 6–7: run it, and trace a missed alert (2:15–3:00)

**[SCREEN]** Run Part 6. Point at P3/P4 `MISSED` and P7/P8 `OVER-ESCALATED`.

> I score three outcomes, never one accuracy. Caught is an incident escalated. Missed is an incident closed, so the
> attacker carries on. Over-escalated is noise sent to a human. The lecture rule catches 2, misses 2 and
> over-escalates 2, so it misses half the incidents. P3, a new admin account on a domain controller at 2:40 a.m., has
> none of the five words. P7 has "exploit" but describes a *blocked* request.

**[SCREEN]** Run Part 7. Output: `{'triage': {'hits': []}}` then `{'close': {'decision': 'close'}}`.

> This is P3 streamed through the graph. Triage wrote an empty `hits` list, the router returned "close", and the
> close node ran. The escalate node and its tool never ran. The decision happened at that one conditional edge.

---

## 5. Part 8: memory by thread id (3:00–3:35)

**[SCREEN]** Run Part 8. Point at `operator.add`, `checkpointer=MemorySaver()`, then the output.

> Part 8 compiles with a `MemorySaver` checkpointer, and each call gets a `thread_id`. One thread is one host's case.
> The `seen` field has an `operator.add` reducer, so each run appends to it. After eight separate calls,
> `case-WS-ENG-04` remembers four alerts, P1, P5, P6 and P8, with 16 checkpoints. A thread I never used is empty. So
> the analyst sees that the "harmless" failed logons came on the same host as a mimikatz alert, which is context no
> single alert carries.

---

## 6. Part 9: my 12 alerts and the hard cases (3:35–4:15)

**[SCREEN]** Run Part 9. Then switch to `my_alerts.json` and show E4, then C1.

> From here it's my own work: twelve alerts based on real types, including EDR, Windows logon events, CloudTrail,
> Suricata and PowerShell logging. Six are escalate and six are close, each with a `why`, plus fields like user, IP,
> parent process and MFA.
> Two hard cases. **E4** has no keywords but is a real incident: root signs in to the payroll AWS account without
> MFA from outside, creates an access key, and makes the payroll bucket public. **C1** contains "malware" but is
> routine: it's the EICAR test file that IT drops every month under change CHG-4471 to prove the antivirus works.

---

## 7. Part 10: the keyword sweep (4:15–4:50)

**[SCREEN]** Run Part 10. Point at the three lines.

> First I only change the word list. The lecture words catch 2, miss 4 and over-escalate 2. Adding technique words
> like "lsass" and "psexec" catches E3 but over-escalates C6, a patch job that uses PsExec, so one alert just
> trades columns. Adding broad words like "powershell" catches nothing new and over-escalates five. E4, E5 and E6 stay
> missed at every list. Widening the rule moves along the trade-off. It never gets off it.

---

## 8. Part 11: my change to the graph (4:50–5:30)

**[SCREEN]** Run both Part 11 cells. Show the three tools, then the new Mermaid drawing.

> What decided my labels was context, not words. So I changed the graph. Now a keyword hit goes to
> `check_suppression`, which checks the change calendar and our scanner list. An alert with no hit goes to
> `check_context`, which looks at process lineage, IP reputation, and privileged logins from outside on critical
> assets. Each new node has its own conditional edge, so there are three decisions instead of one, backed by three
> tools I wrote as stubs.

---

## 9. Parts 12–13: one change at a time (5:30–6:15)

**[SCREEN]** Run Part 12. Point at steps 4, 5, 6. Then run Part 13 to write `results_mine.csv`.

> I turn on one piece at a time. With suppression alone, over-escalation drops from 3 to **0**, and missed doesn't
> move, because suppression only ever closes alerts. Adding the context node catches E4 and E5, so missed drops to
> **1**. It costs one new over-escalation, C5, a privileged engineer signing in from a hotel. Requiring MFA to be
> absent closes C5 again. That's step 6: **5 caught, 1 missed, 0 over-escalated**. Part 13 saves all eight rows to
> `results_mine.csv`.

---

## 10. Parts 14–15: trace a caught alert and a missed one (6:15–7:40)

**[SCREEN]** Run Part 14. Point at row E6 and `wrong at every setting (v1 and v2): ['E6']`.

> In this matrix, five alerts were wrong at every word list on the original graph. After my change only one is
> wrong everywhere: E6.

**[SCREEN]** Run Part 15. Walk down the E4 block line by line, then C1, then E6.

> Here is one alert through the final graph. **E4, caught.** Triage writes empty `hits`, so the first router returns
> "check_context". That node sees the user is root, which is privileged, and the IP isn't corporate. It calls the
> asset tool, payroll is high criticality, and MFA is false, so it writes one signal. The second router sees a
> signal and returns "escalate", and the escalate node adds the asset for the analyst. The original graph closed this
> alert at the first edge.
>
> **C1**: triage finds "malware", the router sends it to suppression, `lookup_change` finds CHG-4471 covering that
> host at that time, and it's closed.
>
> **E6, missed.** It's DNS tunnelling, 1,800 TXT lookups to random subdomains. No keyword, so it goes to context, and
> every check comes back empty. There's no Office parent, the domain is too new to have a reputation, and there's no
> privileged user, so it closes. The attack is in the volume and randomness across many queries, which nothing my
> agent looks at can see. It would need an entropy or domain-age tool. This is the alert I'm choosing to get wrong.

---

## 11. Part 16: graph versus chain (7:40–8:15)

**[SCREEN]** Run Part 16. Point at `True`, `total 38`, `total 20`, then the per-alert paths.

> I wrote the same checks as a LangChain chain. It gives the same twelve decisions, but a chain runs every stage on
> every alert: **38** tool calls against the graph's **20**, because the conditional edge sends each alert only to
> the check it needs. The graph's routing is visible in each path, like `triage -> check_context -> escalate`. A
> chain also has no checkpointer, so there's no case memory by thread id. A chain is still the better choice for a
> straight line, like enriching every alert and writing it to the SIEM.

---

## 12. Part 17, limits and wrap-up (8:15–9:00)

**[SCREEN]** Run Part 17, then scroll to the Summary table.

> I wrote my rules after reading my alerts, so I ran the final graph on the course alerts as well. It did no better
> than the lecture rule, because those alerts lack the fields and tool data my nodes need. And with twelve alerts,
> one alert is a sixth of a column, so this is a fit to my data, not an estimate. Next I'd test a held-out set with
> the rules frozen.
>
> I'd deploy step 6 and knowingly miss E6. As the person staffing the team, I'd rather remove noise with evidence than
> with a narrower word list that goes blind. Thanks for watching.

---

**After recording:** paste the video link into `report/report.md` (replace `VIDEO_LINK`), run
`python report/make_pdf.py` from `langgraph_project/`, and commit.
