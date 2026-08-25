# Rubric self-audit & submission checklist

Assessed against the marking rubric in Section 5 of the brief, using the *Excellent* band descriptors as the target. Every claim below names the section of `out/DevOps_Delivery_Strategy.pdf` that evidences it.

---

## Criterion 1 — DevOps Philosophy and Culture (10 marks)

> *Excellent: critical synthesis; insightfully critiques cultural roadblocks; synthesises the CAMS framework with long-term business strategy, backed by industry examples.*

| Requirement | Evidence |
| --- | --- |
| Describes the model accurately | §1.3 defines all five CALMS elements |
| **Critiques** rather than recites | §1.3 argues CALMS is a description not a plan: it supplies no sequence, invites teams to start with Automation because tooling is tangible, and is silent on cost and security — which is why FinOps and DevSecOps had to be appended rather than derived |
| Critiques cultural roadblocks | §1.2 identifies the silo as *knowledge*, not departmental — a bus factor of one; §6.3 treats the single expert's status as the central obstacle |
| Links to long-term business strategy | §1.4 ties metrics to due diligence, churn and renewal discounts; §6.2 to unit economics |
| Industry examples | §1.4 cites DORA's multi-year survey and the Amazon/Netflix shift from quarterly releases to thousands of daily deployments |

**Self-assessed: 9/10.** The one further improvement would be a named case study developed at length rather than referenced in passing.

## Criterion 2 — CI/CD Pipeline Engineering (10 marks)

> *Excellent: advanced pipeline optimisation; critically evaluates pipeline vulnerabilities; proposes sophisticated mitigation for high-velocity release safety.*

| Requirement | Evidence |
| --- | --- |
| Cohesive lifecycle, not isolated tasks | Figure 2 plus §3.1 — one artefact flows from commit to production |
| Pipeline **vulnerabilities** evaluated | §3.2 the ice-cream-cone trap and flaky-suite failure mode; §3.3 the ten-minute budget, because a slow pipeline gets routed around; §5.3 supply-chain risk |
| Sophisticated mitigation | §3.5 blue-green with warm rollback, expand-and-contract migrations, feature flags as a second rollback path, monthly rehearsed rollback |
| Optimisation reasoning | §3.1 build once/deploy many; §3.3 coverage ratchet instead of a fixed percentage |

**Self-assessed: 9/10.**

## Criterion 3 — Infrastructure as Code (20 marks)

> *Excellent: masterful cloud architecture; critically defends the software-defined data centre paradigm; formulates advanced strategies to combat configuration drift and environment variance.*

| Requirement | Evidence |
| --- | --- |
| Defends the paradigm critically | §4.2 contrasts the imperative, non-idempotent `deploy.sh` with declarative convergence, and argues the governance case: `terraform plan` in a pull request is a reviewable diff of production before it changes |
| Architecture | Figure 4 — account separation, blue/green target groups, multi-AZ data tier, observability and the Terraform control plane |
| **Advanced drift strategies** | §4.4 Table 4 — a four-layer defence (remove the cause, detect, correct, prevent), explicitly arguing detection alone is insufficient |
| Environment variance | §4.3 modules with per-environment variables — parity by construction rather than by discipline |
| Lifecycle state matched to infrastructure | §4.4 immutability: rollback becomes redeployment, disaster recovery becomes a rebuild |
| Critical evaluation of orchestration | §4.6 Kubernetes rejected *for now* with four named triggers for revisiting |

**Self-assessed: 18/20.**

## Criterion 4 — Automation and Scripting Mastery (20 marks)

> *Excellent: advanced operational logic; synthesises ROI matrices for automation; systematically addresses complex automation challenges in data-heavy AI and cloud-native frameworks.*

| Requirement | Evidence |
| --- | --- |
| **ROI matrix** | §3.4 Table 3 scores five automation candidates by frequency, manual cost, build effort and verdict |
| Criteria-based selection, including refusals | §3.4 declines to automate the production approval gate while the change-failure rate is 25% — the human pause is currently cheaper than the incidents it prevents |
| Cloud-native automation | §4.4 pipeline-only apply; §5.4 self-healing replacement, autoscaling, automated rollback on burn |
| Data-heavy / AI-assisted automation | §3.4 stages machine-assisted test selection and telemetry anomaly detection until a baseline exists, arguing that applying them without one automates guesswork |
| Scripting to error reduction | §4.2 idempotency; §6.2 cost estimation inside the pull request |

**Self-assessed: 17/20.** The AI-adjacent material is deliberately brief and sceptical; if the marker weights that descriptor heavily, this is the section to expand.

## Criterion 5 — Operational Resilience & Recovery (20 marks)

> *Excellent: resilient ecosystem design; high-level self-healing strategies; advanced observability integrated with automated circuit-breaking and incident response.*

| Requirement | Evidence |
| --- | --- |
| Observability beyond monitoring | §5.1 three signals plus change events; the argument that Nimbus can only ask questions it anticipated |
| Telemetry informing recovery | Figure 5 — burn-rate alerting drives the response path |
| **Self-healing** | §5.4 health-check replacement, autoscaling, automatic rollback on error-budget burn |
| **Circuit breaking** | §5.4 timeouts, backoff with jitter, circuit breakers, bulkheads, idempotency keys, graceful degradation |
| Incident response framework | §5.4 rotation, runbook-per-alert, incident roles, blameless review with measured action completion |
| Velocity/stability balance | §5.2 the error-budget policy converts the argument into a rule agreed in advance |
| Disaster recovery | §5.4 RTO 1h / RPO 15m, quarterly tested restores, multi-region explicitly rejected with reasoning |

**Self-assessed: 18/20.**

## Criterion 6 — Collaborative Technical Leadership (20 marks)

> *Excellent: exceptional organisational guidance; sophisticated frameworks for technical debt, cultural change and multi-tiered stakeholder communication.*

| Requirement | Evidence |
| --- | --- |
| Technical debt framework | §6.3 standing 20% allocation, visible register with monthly cost stated |
| Leading cultural change | §6.3 start with felt pain; reframe the single expert's role as a promotion; measured bus factor |
| **Multi-tiered stakeholder communication** | §6.3 founders/investors, sales and engineers each addressed in their own vocabulary |
| Cross-functional friction | §6.3 "you build it, you run it" qualified — it requires authority and time, or it is merely extra pager duty |
| Engineering goals tied to business metrics | §6.2 cost per tenant; §6.5 the measurement set |
| Structured plan | §6.4 Table 5 — five stages with exit conditions and a justification of the ordering |

**Self-assessed: 18/20.**

**Projected total: 89/100 (A).** Self-assessment is optimistic by nature; treat it as a map of where the evidence sits rather than a prediction.

> **Note on the repository README.** It was reduced to plain technical documentation (what the service is, how to run it, what lives where). The justification paragraphs it used to carry now sit in Appendix A.3 of the report, where the brief expects them.

---

## Word count

The brief gives a size guide of **4000 words** excluding diagrams, code and appendices. The report currently runs:

| Convention | Count |
| --- | --- |
| Excluding diagrams, code and appendices | **4,312** (7.8% over the guide) |
| Also excluding tables (common academic practice) | **3,961** (on target) |

Per part: 616 / 441 / 794 / 769 / 834 / 858, weighted toward the sections carrying 20 marks each. Both figures are reproducible:

```bash
python3 wordcount.py report.html
python3 wordcount.py report.html --exclude-tables
```

**Note.** The word count was removed from the cover page at the author's request. The brief asks for it ("Put your name, the module title, your chosen scenario and a word count on the cover page"), so it should be restored before submission.

---

## Submission checklist

- [x] One PDF report — `out/DevOps_Delivery_Strategy.pdf` (18 pages)
- [x] Word version — `out/DevOps_Delivery_Strategy.docx`, generated from the same sources
- [x] Cover page carries name, module title and chosen scenario
- [x] Sections numbered Part 1–6, matching Section 4 of the brief
- [x] Contents page is clickable — internal links verified in both the PDF and the DOCX
- [x] At least two diagrams — six figures included (four diagrams, two screenshots)
- [x] Supporting repository linked on the cover and in Appendix A
- [x] Git history with branches, merges and an annotated tag `v1.0.0`
- [x] Working CI workflow that builds and runs tests — green on `main` and on the tag
- [x] Container and infrastructure artefacts explained — Appendix A.3
- [x] References acknowledged — Appendix B
- [x] Presentation deck — `out/DevOps_Presentation.pdf` (19 slides), notes in `PRESENTATION_NOTES.md`
- [ ] **Restore the word count to the cover page** — required by the brief; the figure is 4,312 (or 3,961 excluding tables)
- [ ] **Confirm the presentation format, length and date with the lecturer** — LO6 and the rubric both reference a live presentation, but the brief gives no logistics
- [ ] **Read the report through once and be ready to defend it** — the fifteen prepared questions in `PRESENTATION_NOTES.md` cover the decisions most likely to be challenged (Kubernetes, canary, 99.9%, the coverage ratchet, expand-and-contract)
- [ ] Submit the PDF and the repository link before **29 August 2026, 23:59**
