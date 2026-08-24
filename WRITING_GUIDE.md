# Writing guide

Notes to write the report from. Deliberately written as fragments, not sentences — if it reads like prose you can paste, it defeats the purpose.

**How to use it.** Take one part at a time. Write it straight through without looking at the existing draft in `parts/`. Send it back and I'll mark it against the rubric band and tell you what's thin, what's missing, and where the argument doesn't land. Then we swap it into `parts/partN.html` and rebuild.

**What makes it yours.** Not vocabulary — substance. Your ordering, your emphasis, your examples. Wherever a note says *(your call)* there's a genuine choice with no single right answer; make it and say why. Wherever it says *(your example)*, put something from your own experience or reading in. Those are the bits that carry a voice.

**Length.** Rough targets below. Total is guided at 4000; see the word-count section in `AUDIT.md` for where the current draft sits and what to cut.

---

## Part 1 — Current-state analysis & the case for DevOps
**~600 words · Criterion 1 (10 marks)**
Excellent band wants: critique of the model, not recitation · cultural roadblocks named · linked to business strategy · industry examples.

Cover, roughly in this order:

- Who Nimbus is → 15 staff, 7 engineers, Nimbus Notes B2B SaaS, ~400 customer teams, 2 hand-built EC2 boxes from founding
- How a change flows today → ticket → branch lives 2–3 weeks → informal review → manual regression spreadsheet → Sam runs `deploy.sh` from a laptop
- Point at Figure 1 → 17 days lead time · 2.5 days of actual work · ~15% flow efficiency
  - **the move that matters:** queueing dominates → hiring more devs lengthens the queues → constraint is the *process*, not capacity
- Seven wastes — name all seven, one clause each, each tied to a Nimbus symptom:
  partially done work (stale branches) · handoffs (×3, context lost each time) · **waiting (the big one — one person's calendar)** · defects (1 corrective deploy per 4) · task switching (the interrupted engineer is the bottleneck engineer) · relearning (no runbooks, knowledge re-derived mid-outage) · over-processing (identical checklist re-run every release)
- Name the silo precisely → *not* dev-vs-ops, company's too small for either → **knowledge silo, bus factor of one**
- CALMS → define the five briefly, then attack it:
  - it's a description, not a plan — supplies no sequence
  - read naively you start at Automation (tooling is the tangible letter) → you automate a process nobody measured
  - silent on cost and security → which is why FinOps and DevSecOps had to be *appended* rather than derived
  - therefore at Nimbus: Measurement and Sharing first, Automation follows *(your call — argue a different entry point if you can defend it)*
- Table 1 → say where the numbers came from (Git history, deploy notes, incident channel), not just what they are
- Business tie → due diligence asks ship rate and recovery time · 25% failure rate is a churn driver and a renewal discount
- Industry anchor → DORA's multi-year survey; elite performers deploy on demand and restore in under an hour *(your example — swap in one you've actually read about)*

**Don't:** recite CALMS without attacking it. List the wastes without tying each to a symptom. State metrics without saying where they came from.

---

## Part 2 — Version control & collaborative workflow
**~450 words · Criterion 2 (10 marks, shared with Part 3)**

- The choice → trunk-based, branches under 2 days, PR + one approving review, `main` protected (no direct push, no force-push, no merge on red)
- Point at the repo → 4 feature branches merged into a protected trunk, annotated tag
- **Reject GitFlow, and say why for *this* company** → `develop`/`release`/`hotfix` earn their keep when customers choose when to upgrade → Nimbus has one shared production instance → buys no isolation, formalises the long-lived branches already causing the 17-day lead time
- **Reject direct-to-trunk too, on cultural grounds** → bus factor is one → PR is the cheapest knowledge transfer available → review as deliberate redundancy, not distrust
- The real lever is batch size → 12 small merges/week beat 1 big one → smaller = easier to review honestly, faster to diagnose, trivial to revert → lead time and change-failure rate improve *together*
- Conventional Commits → machine-readable history → changelogs and version numbers generated, not negotiated
- Merge commits kept deliberately *(your call)* → a merge groups a feature into one revertible unit; squashing loses the steps that make `git bisect` useful
- Traceability chain, end to end → ticket → branch → commit → PR → tag → image digest → `/api/health` reports the running version
  - so: any environment traces to a commit without asking anyone → this is the audit trail, and it's free

**Don't:** describe Git. Describe *decisions* about Git, each with the alternative you rejected.

---

## Part 3 — CI/CD pipeline & quality strategy
**~700 words · Criteria 2 and 4 (10 + 20 marks)**
Excellent band wants: pipeline *vulnerabilities* critically evaluated · sophisticated mitigation · ROI reasoning for automation.

- Walk Figure 2 → push → lint/unit/build → image tagged with commit SHA → staging auto-deploy → integration + smoke → approval → blue-green production
- **Build once, deploy many** → if each environment compiles its own artefact, staging didn't test what production runs → this is exactly Nimbus's drift problem
- Say what the repo already does today → lint, unit tests, production build, image build from the same commit
- Test pyramid (Table 2) → costed in *time*, because feedback speed is what you're buying
- **The trap** → no unit tests today makes browser tests look like faster coverage → ice-cream cone → slow, fragile, poor failure localisation → a red browser test says checkout broke, a red unit test says which function → flaky suite teaches people to re-run instead of read
- Gates, each with a threshold and a consequence:
  lint/types · tests + **coverage ratchet not a fixed 80%** (a fixed number invites tests written to satisfy the number) · dependency and container scanning · **10-minute pipeline budget** (a slow pipeline gets routed around, and a gate routed around isn't a gate)
- Automation ROI (Table 3) → score candidates by frequency × manual cost vs build effort
  - **include the refusal** → don't automate the production approval gate while change-failure is 25% — the human pause is cheaper than the incidents it prevents
  - staged for later → ML-assisted test selection, telemetry anomaly detection → both data-hungry, applying them with no baseline automates guesswork
- Release → **blue-green**: deploy to idle, smoke test, shift traffic, keep old warm 30 min → rollback is a traffic shift in seconds
  - cost honestly → double compute for the window, a few euro, cheaper than an hour of outage
- **Why not canary** → needs weighted routing, per-cohort metrics, enough traffic for a fast signal → at Nimbus a 1% canary takes days to say anything → and it's only as good as the observability judging it → *a canary without observability is a slower outage* → sequencing, not rejection
- Blue-green doesn't cover the database → **expand-and-contract migrations** → additive first, then the code, then backfill, then drop later → without this every rollback plan is fiction, because code reverts in seconds and a destructive migration never does
- Feature flags → decouple deploy from release → second instant rollback path
- Rollback rehearsed monthly in staging → an untested rollback is a hope

**Don't:** list tools. Every gate needs a threshold and a stated consequence.

---

## Part 4 — Environments, infrastructure & containers
**~750 words · Criterion 3 (20 marks)**
Excellent band wants: critical defence of the software-defined infrastructure paradigm · advanced strategies against drift and environment variance.

- Pets vs cattle → the 2 servers are named, hand-reared, understood by one person → real config exists only in the machine and in Sam's head → neither reviewable nor restorable
- Every manual fix under pressure widens the gap → this is the mechanism behind "it worked in staging" → **being more careful cannot fix it**
- **Imperative vs declarative** → `deploy.sh` is a sequence from an assumed starting state, and isn't idempotent → run it against a drifted host and you get something nobody predicted → declarative converges from any starting point
- **The governance argument (this is the one that scores)** → `terraform plan` in a PR = a reviewable diff of production *before* it changes → peer-reviewed, timestamped, attributable → stronger than a change-approval board because it's precise and automatic
- Structure → modules (network, service, database, observability) + thin per-environment configs differing only in variables → **staging is production with smaller numbers → parity by construction, not by discipline**
- State → remote, locked, encrypted, versioned → it's both the record of what exists and a file full of secrets
- Immutability → never modify in place → new image, new instance, destroy the old → rollback becomes redeployment, DR becomes a rebuild rather than restoring a machine nobody can reproduce
- **Drift defence in four layers (Table 4)** — lead with *why detection alone is insufficient*:
  remove the cause (no interactive SSH; break-glass time-boxed and audited) · detect (scheduled plan, alert on any diff) · correct (pipeline is the only path that may apply) · prevent (pinned digests and provider versions, policy as code at merge)
- Containers → the image is the deployable unit everywhere: laptop, CI, staging, production
  - the repo's Dockerfile → three stages, lockfile-only install, minimal runtime, unprivileged user
  - pays three ways → small and fast to pull · excludes build tooling and source (attack surface) · lockfile + pinned digest = same inputs, same image → **reproducibility is what makes an artefact safe to promote without retesting**
- **Kubernetes — argue NO** *(your call, but the reasoning below is the strong version)*:
  - what it buys → declarative rollouts, self-healing, autoscaling, service discovery
  - what it costs → not one tool but an operational surface: upgrades, networking, ingress, RBAC, storage classes, a control plane to fund
  - **the killer point** → needs one engineer with deep expertise → recreates the bus-factor-of-one problem at a higher altitude with worse failure modes
  - instead → managed container runtime, same image, a fraction of the surface
  - **name the triggers to revisit** → >~10 services · ownership across multiple teams · real need for traffic shaping · a dedicated platform engineer hired → this turns an opinion into a decision record
- Environment topology → Compose locally, ephemeral in CI, staging + production from the same modules, PR previews later

**Don't:** define IaC. Defend it, against the specific thing it replaces here.

---

## Part 5 — Observability, security & reliability
**~800 words · Criterion 5 (20 marks)**
Excellent band wants: self-healing strategies · advanced observability integrated with circuit-breaking and incident response.

- Why MTTR is 4 hours → monitoring answers questions decided in advance; observability lets you ask one nobody anticipated → Nimbus can only interrogate failures it already imagined → every novel incident starts with SSH and grep
- Three signals, concretely:
  - metrics → RED for services, USE for resources, **plus business metrics** (a healthy system that silently stopped taking sign-ups is still an outage)
  - logs → structured JSON, correlation ID, centralised, sampled at volume, retention tiers so cost scales with value
  - traces → OpenTelemetry, propagated from the edge, vendor-neutral so the data stays portable → without them "it's slow" is an opinion, not a location
  - **fourth signal: change events** → deploys, flag flips, infra applies annotated on the dashboards → first question in any incident is *what changed* → answering from memory is how the first hour gets lost
- SLOs on user journeys, not infrastructure → note create/read success + p95 latency, sign-in success
- **99.9%, chosen not inherited** → ~43 min/month → each extra nine ≈ 10× the engineering cost → customers can't perceive 99.9 vs 99.95, the business can perceive the cost
- **Error budget = the mechanism** (walk Figure 4) → healthy: ship freely · <25%: reliability work takes priority · exhausted: freeze until review actions close
  - say what this *does*: converts speed-vs-stability from an argument won by the most senior person into a rule agreed in advance
- Burn-rate alerting → fast burn (2% in 1h) pages, slow burn tickets → CPU thresholds correlate poorly with customer harm → noise trains people to ignore alerts, which turns a detectable incident into a long one
- Security, shifted left → today: credentials in `.env` and Slack history
  - secrets → managed store, runtime injection, rotation · **OIDC federation so CI holds no long-lived cloud keys** · pre-commit scanning → **prevention beats rotation, because Git history is permanent and a committed key is compromised**
  - supply chain → dependency scanning, SBOM per build, signed images, admission rule that only signed images deploy, patch updates auto-merge on green
  - policy as code → rules out of people's heads (no public storage, no open admin access, every resource tagged) → evaluated against the plan at merge
  - **compliance evidence as a by-product** → approvals, logs, signed artefacts, applied plans are already immutable records → questionnaire answered with a query, not a fire drill → ties to the enterprise deals the funding round should unlock
- Resilience designed in, not bolted on:
  timeouts on every outbound call (unbounded calls exhaust thread pools → partial failure becomes total) · backoff **with jitter** (synchronised retries = self-inflicted DoS) · circuit breakers · bulkheads · idempotency keys · graceful degradation (read-only notes beats an error page)
- **Self-healing** → health-check replacement, autoscaling, automatic rollback on burn spike during a release
- When a human is needed → documented rotation across the whole team (not an implicit dependency on one person) · **runbook per alert, an alert without one is a defect** · incident roles so comms and investigation don't compete
- Blameless review within 5 days → actions tracked as real backlog items → **measure the completion rate, because a review that changes nothing is theatre**
- Recovery → RTO 1h / RPO 15m · encrypted backups, PITR, multi-AZ · **restores tested quarterly — a backup never restored is an assumption, not a control**
- **Reject multi-region active-active** → multiplies cost and complexity for a failure mode rarer than what actually breaks Nimbus → revisit when enterprise contracts demand it
- Game days → start small: terminate an instance in staging, find the runbook gaps before an incident does

**Don't:** list the three pillars and stop. The marks are in the error-budget policy and in what happens *automatically* before a human is paged.

---

## Part 6 — Cloud, cost & leading the change
**~750 words · Criterion 6 (20 marks)**
Excellent band wants: frameworks for technical debt · leading cultural change · multi-tiered stakeholder communication.

- Account per environment → bounds blast radius · least-privilege is straightforward · **cost attribution for free, the invoice arrives already split** · org guardrails stop whole classes of error without anyone remembering a rule
- **Name the root cause** → the bill climbs because cost is decided by engineers making architecture choices and reviewed by nobody — the people spending never see the invoice
- FinOps in three stages:
  - **Inform** → mandatory tags enforced by the policy checks from Part 5 → dashboards visible to engineers, not just finance → **headline number is cost per tenant per month**, because rising absolute spend is fine if revenue rises faster; rising unit cost means growth makes you less profitable
  - **Optimise** → right-sizing, autoscaling, commitments for the stable baseline only, spot for CI runners, retention tiers, kill orphaned volumes and idle load balancers, **shut non-production out of hours (~65%)**
  - **Operate** → budgets and anomaly alerts to the owning team, not a monthly finance review → cost delta shown in the PR → **cost becomes a design-time input the way test results already are**
- **Trade-off honestly** → engineering time costs more than infrastructure at this size → 3 weeks of effort to save a few hundred euro a month is a bad trade → prioritise by return → and the real defect is **a missing owner**, not a missing tool
- Leading the change — this is the 20-mark half most people skip:
  - start with pain the team already feels → automating the dreaded release buys credibility → opening with policy enforcement reads as bureaucracy imposed on people who didn't ask
  - **Sam is the most important stakeholder** → can veto this → status currently comes from being indispensable → a plan that quietly removes that will be resisted whatever its merits
  - → frame it as a **promotion**: Sam owns the platform, pipeline and infra code are their product
  - → knowledge transfer structural, not aspirational: pairing, mandatory review, decision records
  - → **measure it: how many engineers can independently deploy and recover production. It starts at one.**
  - multi-tier communication → founders/investors: delivery risk, diligence answer, unit cost · sales: fewer incidents, faster commitments · engineers: fewer interruptions, no weekend releases → same work, three vocabularies → using one vocabulary is how you lose the sponsor
  - technical debt → standing ~20% of each iteration, **not** a remediation sprint that always gets displaced → visible register **with the monthly cost stated** → "we should tidy this up" loses every prioritisation argument, "this costs six engineer-hours a month" wins many
  - decision records preserve the *reasoning* — the part that leaves with a departing employee
  - "you build it, you run it" **with the caveat** → only works with the authority to change what you run and the time to do it; without both it's just extra pager duty *(your call — you could argue against adopting it at 7 people)*
- Roadmap (Table 5) → 0 Measure · 1 Repeatable · 2 Safe · 3 Secure & economical · 4 Self-service
  - **justify the order, not the contents:** measure before changing (unevidenced improvement can't be funded) · repeatable before safe (**automated rollback is meaningless without a reproducible artefact to roll back to**) · security and cost after, because gates on a still-manual process are just obstacles
- Risks → change fatigue (one significant change at a time) · funding round pulling focus · automation theatre (counting pipelines built instead of outcomes improved)
- Measuring success → the four metrics + SLO attainment + error-budget consumption + cost per tenant + bus factor + % time lost to unplanned work → reviewed monthly
- Close → speed and stability aren't opposites → the practices that make delivery fast are the same ones that make it safe, because a small, tested, reversible change is quicker to ship *and* easier to diagnose

**Don't:** make this a tools section. It's the leadership criterion — people, money, sequencing.

---

## A.3 — Artefact explanations (Appendix A)

Three short paragraphs, one each. The placeholder is already in `parts/appendix.html`.

**Dockerfile** — three stages · lockfile-only dependency install · minimal runtime image · unprivileged user · what that buys: pull speed, attack surface, reproducibility · why the same image everywhere fixes the drift problem

**Compose file** — how the container runs, as code: port mapping, restart policy, health check on `/api/health` · why the health check matters: turns "running" into "actually answering", and it's the signal a deploy uses to decide healthy vs roll back

**Terraform snippet** — illustrative, not applied · provider and version pinning · environment as a variable · **mandatory Owner / CostCentre / Environment tags** → connects to the FinOps argument in Part 6 · the host as reviewable versioned code instead of a hand-configured server

---

## Order I'd write them in

1. **Part 4** and **Part 5** first — 40 marks between them, and they're the ones where reasoning depth shows
2. **Part 6** next — another 20, and it needs the most thinking about people rather than tech
3. **Part 3** — 20 marks shared with Part 2
4. **Parts 1 and 2** last — 20 between them, and by then you'll know exactly what the rest of the report needs the opening to set up
