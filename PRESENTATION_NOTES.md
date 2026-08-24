# Presentation notes & defence preparation

Deck: `out/DevOps_Presentation.pdf` (19 slides, 16:9). Suggested running time **15–20 minutes**, leaving time for questions. If you are given only 10 minutes, drop slides 6, 11 and 15 and compress 8 and 14 into a single "quality and safety" beat.

---

## Slide-by-slide talking points

**1 · Title.** Name the scenario and the fictional company in one sentence: "Scenario B — a fifteen-person SaaS start-up called Nimbus that has outgrown the scripts it was built on."

**2 · The organisation.** Set the scene in about 45 seconds. The three facts that matter: two hand-configured servers, deployment is a person rather than a process, and a cloud bill nobody owns. Close on *why now* — the funding round makes delivery risk a commercial problem, not just an engineering one.

**3 · Value stream (Figure 1).** This is the slide the whole argument rests on. Point at the bar: 17 days of lead time, 2.5 days of work. Say the line out loud — **"the constraint is the process, not the number of engineers"** — because it pre-empts the obvious objection that they should just hire more people.

**4 · Baseline metrics.** Emphasise that these were *reconstructed*, not invented, and that Stage 0 of the roadmap is measurement with no other change. If asked how you would gather them for real: Git history for lead time, deployment logs for frequency, incident channel for MTTR and failure rate.

**5 · Diagnosis and the CALMS critique.** Spend your time on the critique, not the definition — the marker already knows what CALMS stands for. The two original points are that CALMS supplies no *sequence*, and that its silence on cost and security is why FinOps and DevSecOps had to be appended later.

**6 · Version control.** Lead with the rejections. GitFlow is wrong here for a specific reason (one shared production instance), and pure trunk without review is wrong for a cultural reason (review is knowledge transfer when the bus factor is one).

**7 · Pipeline (Figure 2).** Trace the flow with a finger: one image built from the commit, promoted unchanged. Say "build once, deploy many" explicitly and connect it to the scenario's environment drift.

**8 · Quality gates.** The coverage ratchet is the point worth defending — a fixed 80% target invites tests written to satisfy a number. Mention the ten-minute pipeline budget as a *quality gate on the gates themselves*.

**9 · Blue-green and why not canary.** Be clear that canary is deferred, not rejected, and give the two reasons: insufficient traffic for a fast statistical signal, and no observability yet to judge it. The memorable line is **"a canary without observability is just a slower outage."**

**10 · Architecture (Figure 3).** The single most important idea: staging and production come from the *same* Terraform modules with different variables, so parity is structural rather than a matter of discipline.

**11 · Drift.** Stress that detection alone is insufficient — that is why there are four layers, starting with removing the cause (no interactive SSH). The reviewable `terraform plan` in a pull request is a governance argument, not just a technical one.

**12 · Kubernetes.** Expect a challenge here, so state the reasoning cleanly: Kubernetes would recreate the bus-factor-of-one problem at a higher altitude. Then immediately give the named triggers for revisiting — that converts an opinion into a decision record.

**13 · Error budget (Figure 4).** The framing that earns marks: the error budget converts speed-versus-stability from an argument usually won by whoever is most senior into a rule agreed in advance.

**14 · Security and recovery.** Two lines carry this slide: prevention beats rotation because Git history is permanent, and a backup that has never been restored is an assumption rather than a control.

**15 · FinOps.** Unit economics first — cost per tenant, not absolute spend. Then the honest trade-off: engineering time costs more than infrastructure at this size. Finish on the real defect being a missing *owner*.

**16 · Leading the change.** This is the slide most candidates skip and it carries 20 marks. Sam is a person with status to protect, and the plan must make the change a promotion. Then the measurable: how many engineers can independently deploy and recover production — starting at one.

**17 · Roadmap.** Justify the *order*, not the contents: measure before changing, repeatable before safe, security and cost after the process is automated rather than before.

**18 · Artefacts.** Offer to run the commands live if the room wants it. The repository is public and the pipeline is green on `main` and on the `v1.0.0` tag.

**19 · Close.** End on the DORA finding that speed and stability are produced by the same practices, and let the before/after numbers do the closing argument.

---

## Likely questions and prepared answers

**1. Why not Kubernetes? Everyone uses it.**
Kubernetes buys declarative rollouts, self-healing and autoscaling, but it is an operational surface rather than a tool — upgrades, networking, ingress, RBAC, storage classes and a control plane to fund. Running it well needs one person with deep expertise, which recreates exactly the bus-factor-of-one problem we are trying to remove, at a higher altitude and with worse failure modes. A managed container runtime delivers most of the benefit from the same image. I have named four triggers for revisiting it, so the decision is time-bound rather than ideological.

**2. Isn't blue-green wasteful compared with rolling deployments?**
It doubles compute only for the release window, which for a stateless web tier is a few euro. That buys a rollback measured in seconds instead of a redeployment measured in hours, which is worth far more than the compute at a 25% change-failure rate. As the failure rate drops, the calculation can be revisited.

**3. How do you know any of this worked?**
Stage 0 exists precisely for that: instrument the four delivery metrics and the cost baseline before changing anything. Then monthly review against Table 1, plus SLO attainment, error-budget consumption, cost per tenant, and the number of engineers who can deploy and recover production.

**4. What if the team resists?**
Expected, and the plan is built around it. Start with the pain they already feel rather than a maturity model, keep the programme to one significant change at a time, and make the single expert the owner of the new platform rather than its casualty. Resistance is usually rational — it is a response to a plan that costs someone status or time.

**5. Why 99.9% and not higher?**
Each additional nine multiplies engineering cost by roughly an order of magnitude. For a small-business productivity tool, customers cannot perceive the difference between 99.9% and 99.95%, but the business can perceive the cost. The target is a commercial decision expressed as an engineering one, and it can be raised when enterprise contracts require it.

**6. Your metrics are invented — isn't that a weakness?**
They are reconstructed from plausible sources named in the report: Git history, deployment notes and incident messages. The specific values matter less than the discipline of establishing a baseline before change; the same method would produce real numbers on day one of Stage 0.

**7. Why keep merge commits when everyone squashes?**
A merge commit groups a feature's commits into a single revertible unit while preserving the intermediate steps that make `git bisect` useful. Squashing optimises for a tidy log; merge commits optimise for diagnosis and rollback, which matter more when change failure is the problem being solved.

**8. Isn't a coverage ratchet just a weaker target?**
It is a different target. A fixed percentage invites tests written to satisfy the number and penalises a small, well-tested change that happens to touch a poorly covered file. A ratchet guarantees the trend is monotonic, which is the property you actually want.

**9. What if the funding round fails and budget disappears?**
The roadmap is ordered so that the cheapest stages deliver the largest risk reduction first. Stages 0 and 1 need engineering time rather than spend, and they already remove the release bottleneck and the single point of failure. Later stages are separable.

**10. Where does AI or automation of the pipeline itself fit?**
The same principle applies as elsewhere: automate what is repetitive and measured. Dependency updates merge automatically when the pipeline is green; test selection and anomaly detection in telemetry are candidates once there is enough data. What I would not automate early is judgement — approval gates stay human until the failure rate justifies removing them.

**11. How is this different from just "doing DevOps"?**
Every decision here is justified against this organisation's constraints rather than best practice in the abstract — which is why the report rejects GitFlow, canary and Kubernetes despite all three being defensible elsewhere.

**12. Why separate cloud accounts rather than tags or naming conventions?**
Blast radius and attribution. A mistake in staging cannot reach production, least-privilege becomes straightforward, and the invoice arrives already divided by environment rather than requiring reconstruction.

**13. What is the single biggest risk to this plan?**
Key-person risk during the transition. Sam is both the bottleneck being removed and the person best placed to remove it, so the plan has to keep them engaged. The mitigation is structural: pairing, mandatory review, decision records, and tracking the bus factor as an explicit metric.

**14. Expand-and-contract migrations sound slow. Why not just take a maintenance window?**
Maintenance windows are what produce release weekends, and they do not solve rollback — once a destructive migration has run, reverting the code does not revert the data. Expand-and-contract costs one extra release per schema change and makes every rollback plan genuine.

**15. Which part of this would you do first if you had one week?**
Instrument the four metrics and put the existing build behind a pipeline that runs tests on every push. That is a week's work, it costs nothing but time, and it produces both the evidence and the first visible reduction in toil.
