# Mini Project: An Alert Triage Agent with LangGraph

**IT 7075C Applied AI for Cybersecurity** · Dharmin Patel

**GitHub project folder:** [github.com/patel5d2/rag_project/tree/main/langgraph_project](https://github.com/patel5d2/rag_project/tree/main/langgraph_project)

**Video walkthrough:** [Watch the video](https://mailuc-my.sharepoint.com/:v:/g/personal/patel5d2_mail_uc_edu/IQA0hbyTSqq_Tp45nMxiaLePASykDwc8RXdbq5otaLYqitU?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=qfc3BJ)

---

## 1. Concept check

**What is the state in a LangGraph agent, and how do nodes use it?**
The state is one typed dictionary (a `TypedDict`) that holds everything the agent knows about the item it is
working on. For my agent that is the alert, the keywords found, any suppression reason, the context signals and
the decision. Each node receives the current state and returns only the fields it changed. LangGraph merges that
update into the state, overwriting by default or appending when a field has a reducer such as `operator.add`.

**What is a node and what is an edge? What does the end marker do?**
A node is one step of work, an ordinary Python function from state to a partial update, such as `triage` or
`check_context`. An edge says which node runs next: a normal edge always goes to the same node, a conditional
edge picks one. `END` is the node that means "stop": when the graph reaches it, the run finishes and `invoke`
returns the final state.

**How does a conditional edge let an agent choose its path? Give a security example.**
A conditional edge attaches a router function to a node. The router reads the state and returns a label, and a
mapping turns that label into the next node, so different inputs take different paths through the same graph.
In my graph, after `triage` the router sends an alert with a keyword hit to `check_suppression` (is this an
approved change or our own scanner?) and an alert without one to `check_context` (privileged login from outside,
Office spawning a script host, known-bad IP). The EICAR test alert C1 takes the first path and is closed.
The root login E4 takes the second and is escalated.

**What is a tool in an agent, and why do agents need them?**
A tool is a function a node calls to fetch information or act outside the state, such as my `lookup_change`
(change calendar), `lookup_asset2` (asset inventory) and `ip_reputation` (threat intel). Agents need tools
because the alert text alone rarely holds the deciding fact. Whether "malware" on WS-IT-01 matters depends on
a change ticket the alert does not mention. Tools bring in that outside context.

**What does a checkpointer with a thread identifier give the agent?**
A checkpointer saves the state after every step, and the thread id is the key it is filed under. Calling the
graph again with the same thread id continues from the saved state instead of starting empty, and
`get_state_history` shows every earlier step. In Part 8 one thread is one host's case: `case-WS-ENG-04`
accumulated `P1 P5 P6 P8` over four separate calls, while a new thread was empty.

## 2. What I built

**The graph.** `START -> triage ->` (keyword hit?) `-> check_suppression ->` (approved change or scanner?)
`-> close | escalate`, and on the no-hit side `-> check_context ->` (any risky context signal?) `-> escalate | close
-> END`. That is three decisions instead of the practice graph's one, plus three tools. The practice graph from
Parts 1–5 (`START -> triage -> escalate | close -> END`, with the asset lookup on the escalate branch) is kept
unchanged as the baseline ("v1").

**My 12 alerts** (`my_alerts.json`), based on real alert types and written in my own words:

| | Escalate | | Close |
|---|---|---|---|
| E1 | EDR: Word -> cmd -> `vssadmin delete shadows` (ransomware prep) | C1 | Defender: EICAR test file "malware" during AV check, CHG-4471 |
| E2 | 240 failed logons then a success on the VPN from one external IP | C2 | IDS "ET EXPLOIT Log4j" from our own vulnerability scanner |
| E3 | EDR: procdump read LSASS memory, dump in `C:\Users\Public` | C3 | Six failed logons, then self-service password reset, same desk |
| E4 | CloudTrail: root login, no MFA, new access key, payroll bucket made public | C4 | IT admin's PowerShell `Get-ADUser` for the quarterly access review |
| E5 | EDR: Outlook -> mshta -> HTTPS to a known-bad IP | C5 | CloudTrail: engineer at a hotel, MFA, read-only calls |
| E6 | IDS: 1,800 DNS TXT queries to random subdomains of a new domain | C6 | PsExec from the patching account during change CHG-4502 |

**The two hard cases.** *E4 is a real incident with none of my keywords* (no word list I tried contains
anything in it). I labelled it escalate because the root user should never sign in for daily work, never without
MFA, and creating an access key and making a payroll bucket world-readable within four minutes is persistence
and data exposure at once. *C1 is a routine alert that contains a keyword* ("malware"). I labelled it close
because EICAR is a harmless test string that IT drops monthly to prove the AV works, under an approved change,
and Defender did exactly what it should. I wrote more hard cases than the minimum: E5 and E6 have no keywords
either, and C2, C3, C4 and C6 each contain a word from at least one of my lists.

## 3. Results: the two errors, one change at a time

From `results_mine.csv` (12 alerts: 6 incidents, 6 routine):

| step | graph | words | change | caught | missed | over-esc. | which are wrong |
|---|---|---|---|---|---|---|---|
| 1 | v1 | K0 | lecture word list | 2 | 4 | 2 | E3 E4 E5 E6 / C1 C2 |
| 2 | v1 | K1 | +5 technique words (lsass, psexec…) | 3 | 3 | 3 | E4 E5 E6 / C1 C2 C6 |
| 3 | v1 | K2 | +5 broad words (powershell, failed…) | 3 | 3 | 5 | E4 E5 E6 / C1 C2 C3 C4 C6 |
| 4 | v2 | K1 | + suppression node | 3 | 3 | 0 | E4 E5 E6 / – |
| 5 | v2 | K1 | + context node | 5 | 1 | 1 | E6 / C5 |
| 6 | v2 | K1 | privileged-external rule needs MFA absent | **5** | **1** | **0** | E6 / – |
| 7 | v2 | K0 | final graph, narrower words | 4 | 2 | 0 | E3 E6 / – |
| 8 | v2 | K2 | final graph, wider words | 5 | 1 | 2 | E6 / C3 C4 |

Widening the word list moves along the trade-off but not off it. K0 -> K1 buys E3 for C6. K1 -> K2 buys
nothing and costs C3 and C4. Changing the graph is what moved both columns at once.

## 4. Analysis

**The two errors: which would I rather the agent made?** As the person who has to staff the team, I would
rather it over-escalated, *up to the point where analysts stop reading*. A miss is invisible: E4 closed means
an attacker holding root on the payroll account with no one looking, and nobody learns about it until the data
appears somewhere. An over-escalation is visible and costs a known amount, a few analyst minutes. But that cost
compounds. At step 3 five of the eight alerts sent to a human are noise, and a team that sees mostly false
alarms starts closing them in bulk, which turns over-escalation back into misses. So my rule is: accept
over-escalation of alerts that are *cheap to dismiss with context*, and never accept a miss on a critical asset
or privileged identity. That is why I added a node that removes noise using evidence (a change ticket, the
scanner list) rather than a narrower word list, which removes noise by going blind.

**My operating point.** I would deploy step 6: v2 with K1, suppression and the context node with the MFA
condition (5 caught, 1 missed, 0 over-escalated). I am choosing to get **E6 wrong**, the DNS tunnelling from a
low-criticality build server. I accept that because nothing my agent checks can see it (Section 4.3) and
because it would be better caught by a volume/entropy detection upstream than by this triage agent. I am also
knowingly accepting two risks that do not show in the table. First, the suppression node will close a real
attack that happens on a host during its change window, so tickets must name hosts and times, and suppressed
alerts should still be logged for review. Second, the MFA condition re-closes C5, which means a privileged
external login *with* MFA, say after MFA fatigue or a stolen session cookie, would also be closed. Step 5 is
the safer choice if the team can absorb one extra escalation per dozen.

**The alerts that stay wrong at every setting.** On the original graph, E4, E5, E6, C1 and C2 were wrong at all
three word lists (Part 14 of the notebook). A keyword rule sees *words in the text*. It cannot see *who* (root,
an IT admin), *where from* (inside or outside the corporate range), *what is expected* (a change ticket, an
approved scanner), *process lineage* (Outlook starting mshta) or *reputation* (an IP we already know is bad).
E4 and E5 describe attacks in neutral vocabulary, and C1 and C2 use alarming vocabulary for harmless activity.
My change (Part 11): the first router now sends a keyword hit to `check_suppression` and a no-hit alert to
`check_context`. Each new node calls tools and is followed by its own conditional edge. This fixed four of the
five: C1, C2 (and C6) are closed by suppression, and E4 and E5 are escalated by context. **E6 is wrong at every
one of the eight settings.** DNS tunnelling is a pattern across many queries (volume, label entropy, a new
domain). None of that is a word in one alert or a field my tools look up, and the domain is too new to be in a
reputation list. Fixing it would need a different signal: a domain-age or entropy tool, or aggregation across
alerts.

**LangGraph compared with LangChain.** I wrote the same three checks as a LangChain chain
(`RunnableLambda | RunnableLambda | …`, Part 16). It made the same 12 decisions, so the chain is not wrong. The
differences are these:

* *The conditional edge.* The chain runs every stage on every alert and hides the decision in one `if` at the
  end. It made **38** tool calls against the graph's **20**, because the graph's `route_first` edge sends each
  alert to only the check it needs. The graph's `path` field shows the branch each alert took, for example
  `E4: triage -> check_context -> escalate` and `C1: triage -> check_suppression -> close`, and
  `get_graph().draw_mermaid()` draws the decision structure. In a chain the routing exists only inside a
  function. In the graph it is a reviewable structure, and that structure is the object of study here.
* *Memory by thread id.* `mem_graph.get_state(thread("case-WS-ENG-04"))` returned `seen=['P1','P5','P6','P8']`
  after four separate invocations, with 16 checkpoints in its history, and `case-NEW-HOST` returned an empty
  list. A chain has no checkpointer: every `invoke` starts from nothing, so "this host had a mimikatz alert
  earlier" would have to be stored and looked up by hand.
* *When a chain is still better:* when every input takes the same steps with no decision in the middle. An
  enrichment pipeline that normalises every alert, adds GeoIP and asset owner and writes it to the SIEM is a
  straight line, and a chain is less code, easier to read and has no state to manage.

**Honest limits.** Twelve alerts means one alert is a sixth of a column, so "5 of 6 caught" could be 3 of 6
or 6 of 6 on the next dozen. A 95% interval for 5/6 runs from roughly 36% to 99%. I also wrote the context
and suppression rules *after* reading my own alerts, so step 6 is a fit to the data, not a test of it. The
evidence is Part 17: on the eight course alerts, which the rules were not designed for, v2 did no better than
the lecture rule (2 caught, 2 missed, 2 over-escalated). Those alerts lack the structured fields and the tool
data my nodes depend on. What the numbers do support is narrower: which alert each change fixes, and what each
change costs. What I would measure next:

1. A held-out set written by someone else, or a public labelled dataset, scored with the rules frozen.
2. At least 100 alerts with a realistic ratio (far more routine than real), so that the over-escalation cost
   is measured at its true scale.
3. Adversarial cases for each new node: an attack inside a change window, an attacker with MFA, and a
   compromised internal host as the source.
4. Analyst minutes per escalation, so the two error columns can be weighed in the same unit.
