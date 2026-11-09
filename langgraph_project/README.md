# Alert Triage Agent with LangGraph

A small deterministic LangGraph agent that decides whether a security alert is escalated to an analyst or
closed. Parts 1–8 of the notebook build the practice graph (state, triage node, router, tool node, conditional
edge, checkpointer memory by thread id) and run it on eight course alerts. From Part 9, the agent runs on my 12
labelled alerts (`my_alerts.json`). I widen the keyword list, then change the graph itself: a suppression node
(change calendar, scanner list) and a context node (process lineage, IP reputation, privileged access from
outside), each followed by its own conditional edge. Caught, missed and over-escalated alerts are measured one
change at a time, and the graph is compared with the same logic written as a LangChain chain.

| File | What it is |
|------|------------|
| `agent_notebook.ipynb` | The completed notebook, run top to bottom with outputs saved. |
| `my_alerts.json` | My 12 labelled alerts (6 escalate, 6 close), each with a `why`. |
| `alerts_template.json` | The field layout the alerts follow. |
| `results_mine.csv` | Eight settings, one change at a time: caught, missed, over-escalated, and which alerts. |
| `SOURCES.md` | References used to write realistic alert types. |
| `report/` | Report source (`report.md`), PDF, and the script that renders it. |

**Run it:** `pip install langgraph langchain-core pandas jupyter`, then open the notebook from this folder and
run all cells. No API key, no model, no network: every node is plain Python, so the numbers are exact.

**Result:** the lecture word list catches 2 of 6 incidents and over-escalates 2 routine alerts. The final
graph catches 5 of 6 with no over-escalations on these 12 alerts. E6 (DNS tunnelling) is missed at every
setting.
