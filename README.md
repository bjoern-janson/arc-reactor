# ⚛️ The Arc Reactor Framework (ARC)

## Adaptive Reality-Coupled Correction

The Arc Reactor Framework (ARC) is a research framework investigating whether robust adaptation under deep regime change requires not only learning mechanisms, but a control mechanism that regulates the **permission, location, and magnitude of self-modification**.

ARC studies a fundamental question:

> When reality proves a system wrong, can it repair the broken parts without destroying the parts that were still right?

---

# Overview

Current adaptive systems are primarily optimized around improving updates:

\[
\text{Error} \rightarrow \text{Update}
\]

ARC investigates an additional control layer:

\[
\text{Error}
\rightarrow
\text{Diagnosis}
\rightarrow
\text{Permission}
\rightarrow
\text{Allocation}
\rightarrow
\text{Correction}
\]

The central hypothesis is that as systems become more complex, not all internal assumptions should have equal plasticity.

A system that changes too little becomes rigid.

A system that changes too much destroys accumulated structure.

ARC explores the possibility that intelligence requires a mechanism for deciding:

> **What should be allowed to change?**

---

# Core Architecture

The ARC control pipeline:

\[
\Gamma
\rightarrow
P(L_i|E_t)
\rightarrow
FA_c
\rightarrow
\lambda_A
\rightarrow
\Pi_A
\rightarrow
\Delta S
\rightarrow
RI
\rightarrow
C_{\text{future}}
\]

## Components

### Reality Coupling ($\Gamma$)

Ensures adaptation is grounded in external environmental feedback rather than internal drift.

---

### Failure Attribution ($P(L_i|E_t)$)

Estimates where failure occurred across structural layers.

Possible failure depths include:

- Parameter drift
- Representation shift
- Rule/operator inversion
- World-model failure
- Ontological assumption collapse

---

### Attribution Confidence ($FA_c$)

Measures confidence in the diagnosis.

Low confidence prevents destructive intervention.

---

### Permission Gate ($\lambda_A$)

Controls whether structural modification is permitted.

\[
\lambda_A \in [0,1]
\]

When attribution confidence is insufficient:

\[
FA_c < \tau_c
\Rightarrow
\lambda_A \rightarrow 0
\]

The system enters an **epistemic holding state** rather than blindly rewriting itself.

---

### Plasticity Allocation ($\Pi_A$)

Determines where permitted changes should occur.

The allocation mechanism enforces the blast radius conservation principle:

> Change the lowest sufficient layer.

---

### Recovery Intelligence ($RI$)

Measures whether adaptation restores performance while preserving accumulated structural capability.

---

### Future Adaptive Capacity ($C_{\text{future}}$)

The core invariant:

\[
C_{\text{future}}(t+1) \geq C_{\text{future}}(t)
\]

A successful adaptation should preserve or expand the system's ability to survive future unknown shocks.

---

# The Arc Reactor Principle

A reactor does not survive by avoiding high energy.

It survives by containing and regulating transformation.

Similarly:

> An adaptive system does not survive by avoiding failure. It survives by controlling how failure changes it.

---

# RAHU Benchmark

## Regime-Adaptive Hierarchical Updating

RAHU is the adversarial benchmark environment for testing ARC.

The benchmark introduces controlled regime shifts:

| Shock | Failure Type | Expected Response |
|---|---|---|
| Shock A | Parameter Drift | Update parameters |
| Shock B | Representation Shift | Update representation |
| Shock C | Rule Inversion | Update structural rules |
| Shock D | Attribution Ambiguity | Reduce permeability and hold |

The goal is not merely recovery.

The goal is:

- correct diagnosis
- selective modification
- structural retention
- increased future adaptive capacity

---

# Research Hypothesis

ARC proposes:

> Under sufficiently deep, consequential, and structurally heterogeneous regime shifts, adaptive advantage may shift from faster optimization toward accurate failure attribution and controlled self-modification.

The framework predicts a transition boundary:

\[
AAR^* \approx 1
\]

where the expected cost of unlocalized failure exceeds the cost of maintaining diagnostic control.

---

# Evaluation

ARC is evaluated against:

| Agent | Purpose |
|---|---|
| Flat Optimizer | Continual learning baseline |
| Meta-Learner | Fast adaptation baseline |
| ARC-Lite | Oracle attribution upper bound |
| ARC-Full | Learned attribution controller |
| Oracle Reset | Theoretical recovery ceiling |

Metrics:

- Attribution Accuracy ($AE_w$)
- Structural Retention ($S_{\text{retained}}$)
- Recovery Intelligence ($RI$)
- Future Capacity ($C_{\text{future}}$)
- Attribution efficiency gap

---

# Scientific Falsification

ARC is considered unsuccessful if:

- Attribution provides no measurable advantage.
- Controlled plasticity does not outperform flat optimization when diagnostic costs are justified.
- The predicted $AAR^* \approx 1$ transition boundary does not emerge.
- Learned attribution cannot outperform simpler adaptive strategies.

ARC is not a claim that diagnostic control is always optimal.

It is a hypothesis about **when** diagnostic control becomes necessary.

---

# Current Status

🚧 Research prototype phase

The theoretical framework is specified.

The next phase is empirical validation through:

1. RAHU environment implementation
2. Baseline agent comparison
3. Oracle ARC evaluation
4. Learned ARC development
5. Phase boundary measurement

---

# Repository Structure

Planned:

```text
arc-reactor-framework/
│
├── README.md
├── LICENSE
│
├── docs/
│   ├── theory/
│   ├── specifications/
│   └── experiments/
│
├── src/
│   ├── arc/
│   │   ├── attribution/
│   │   ├── governor/
│   │   ├── permeability/
│   │   └── evaluation/
│
├── rahu/
│   ├── environments/
│   ├── agents/
│   └── benchmarks/
│
└── experiments/
    └── rahu_0/
```
Citation

If this framework becomes useful in research, please cite:

The Arc Reactor Framework (ARC):
Adaptive Reality-Coupled Correction

---

License

Licensed under the GNU Affero General Public License v3.0.

See LICENSE for details.
