# Worked Examples for Causal Chain Annotation

These examples show how to fill out the annotation template.
Each example includes the full narrative, existing entities,
and completed annotation fields with reasoning.

---


## Example 1: Simple Single Cause

**Record:** 574147
**Stratum:** fire_explosion
**Causal Matches:** 1.0
**Causal Density:** 0.0333
**Category:** Fire & Explosion - Flammable solids, liquids and gases

### Narrative

> Laminated plastic coated empty wooden box accumulated near GTG open area, got small fire due to High atmospheric temperature. Our one of Engineer observed and immediately extinguished by using sand.

### Existing Entities

| Type | Value | Relation |
|------|-------|----------|
| LOCATION | Amalapuram | OCCURRED_AT |
| LOCATION | India | OCCURRED_AT |
| LOCATION | India | OCCURRED_AT |
| ORGANIZATION | OIL AND NATURAL GAS CORP.LTD | REPORTED_BY |
| ROOT_CAUSE_CATEGORY | Flammable solids, liquids and gases | CATEGORIZED_AS |
| LOCATION | GTG | OCCURRED_AT |

### Annotation

This record has a single, clear causal indicator. Fill in `caused_by_1` only. Leave all other annotation fields blank.

| Field | Value |
|-------|-------|
| caused_by_1_cause | High atmospheric temperature |
| caused_by_1_evidence | "got small fire due to High atmospheric temperature" |
| caused_by_1_confidence | HIGH |
| *(all other fields)* | *(blank)* |

**Why this annotation?** The narrative contains explicit causal language ("due to") pointing to a single, unambiguous cause. High atmospheric temperature is directly named as what ignited the wooden box. There is no secondary contributing factor mentioned, and no multi-step sequence to capture. One `caused_by_1` entry is sufficient and correct. Confidence is HIGH because "due to" is explicit causal language per the guidelines.

---


## Example 2: Multi-Factor

**Record:** 516010
**Stratum:** high_causal_any
**Causal Matches:** 3.0
**Causal Density:** 0.0938
**Category:** Ergonomics - Manual handling

### Narrative

> During manually shifting of portable scaffold (1.5MX1M) by four number of manpower, due to uneven surface and unbalancing it was tilted on ground._x000D_ No injury/ property damage caused due to the incident.

### Existing Entities

| Type | Value | Relation |
|------|-------|----------|
| LOCATION | Amalapuram | OCCURRED_AT |
| LOCATION | India | OCCURRED_AT |
| LOCATION | India | OCCURRED_AT |
| ORGANIZATION | OIL AND NATURAL GAS CORP.LTD | REPORTED_BY |
| ROOT_CAUSE_CATEGORY | Manual handling | CATEGORIZED_AS |
| EQUIPMENT | portable scaffold | INVOLVED |
| LOCATION | ground | OCCURRED_AT |

### Annotation

This record has multiple causal indicators suggesting both a primary cause and a contributing factor.

| Field | Value |
|-------|-------|
| caused_by_1_cause | unbalancing of scaffold during manual shift |
| caused_by_1_evidence | "due to uneven surface and unbalancing it was tilted on ground" |
| caused_by_1_confidence | HIGH |
| contributed_to_1_factor | uneven surface |
| contributed_to_1_evidence | "due to uneven surface and unbalancing it was tilted on ground" |
| contributed_to_1_confidence | MEDIUM |

**Why this annotation?** The narrative names two factors in a single "due to" clause: "uneven surface" and "unbalancing." Unbalancing is the direct mechanical cause of the scaffold tilting — it describes the failure mode of the task itself. The uneven surface is a pre-existing environmental condition that made the task harder and contributed to the loss of balance, fitting the Swiss cheese model of a contributing factor. Both share the same evidence span because the narrative does not separate them into distinct sentences. The contributing factor gets MEDIUM confidence because the narrative presents both factors jointly rather than distinguishing them explicitly — a reasonable annotator could argue either is primary.

---


## Example 3: Causal Chain

**Record:** 677880
**Stratum:** fire_explosion
**Causal Matches:** 5.0
**Causal Density:** 0.0962
**Category:** Fire & Explosion - Flammable solids, liquids and gases

### Narrative

> Welding gas hose was caught on fire due to the overhead splash that fell on the welding hose._x000D_ Fire has started due to arc air sparks which has caused the rupture of a welding hose._x000D_ The Fire was extinguished by the CO2 gas in the hose after the rupture of the hose.

### Existing Entities

| Type | Value | Relation |
|------|-------|----------|
| LOCATION | Tianjin | OCCURRED_AT |
| LOCATION | China | OCCURRED_AT |
| LOCATION | Asia Pacific | OCCURRED_AT |
| ORGANIZATION | NOVARCTIC SNC | REPORTED_BY |
| ROOT_CAUSE_CATEGORY | Flammable solids, liquids and gases | CATEGORIZED_AS |
| EQUIPMENT | Welding gas hose | INVOLVED |
| EQUIPMENT | welding hose | INVOLVED |

### Annotation

This record has a rich causal sequence with multiple steps. Use the LED_TO fields to capture the chain.

| Field | Value |
|-------|-------|
| caused_by_1_cause | arc air sparks |
| caused_by_1_evidence | "Fire has started due to arc air sparks" |
| caused_by_1_confidence | HIGH |
| contributed_to_1_factor | overhead splash falling on welding hose |
| contributed_to_1_evidence | "Welding gas hose was caught on fire due to the overhead splash that fell on the welding hose" |
| contributed_to_1_confidence | HIGH |
| led_to_1_event | fire starting from arc air sparks |
| led_to_1_outcome | rupture of welding hose |
| led_to_1_evidence | "Fire has started due to arc air sparks which has caused the rupture of a welding hose" |
| led_to_1_confidence | HIGH |
| led_to_2_event | rupture of welding hose |
| led_to_2_outcome | fire extinguished by CO2 gas released from hose |
| led_to_2_evidence | "The Fire was extinguished by the CO2 gas in the hose after the rupture of the hose" |
| led_to_2_confidence | HIGH |

**Why this annotation?** The narrative contains two overlapping causal accounts of the same fire. Sentence 2 identifies arc air sparks as the ignition source ("Fire has started due to arc air sparks") — this is the root cause for `caused_by_1`. Sentence 1 identifies the overhead splash as what caused the hose to catch fire — this is a distinct contributing mechanism (a flammable material contacted an ignition source), so it goes in `contributed_to_1`. The LED_TO chain then captures the sequence that followed: fire starting from sparks led to hose rupture (step 1), and hose rupture released CO2 which extinguished the fire (step 2). Each LED_TO entry is an event→outcome pair with a direct evidence span. The evidence for `led_to_1` quotes the full sentence that connects the event (fire starting) to the outcome (rupture). Confidence is HIGH throughout because every step uses explicit causal language ("due to", "caused", "after").

---


## Example 4: No Causal Relationship

**Record:** 712201
**Stratum:** fire_explosion
**Causal Matches:** 1.0
**Causal Density:** 0.0222
**Category:** Fire & Explosion - Flammable solids, liquids and gases

### Narrative

> While checking light towers, I noticed a large amount of Diesel had been spilled while filling the fuel tank and had flooded the bottom o the Light plant.  The exhaust runs through the bottom of the containment and could potentially cause the diesel to ignite.

### Existing Entities

| Type | Value | Relation |
|------|-------|----------|
| LOCATION | Minot Service Base | OCCURRED_AT |
| LOCATION | Minot | OCCURRED_AT |
| LOCATION | USA | OCCURRED_AT |
| LOCATION | North America | OCCURRED_AT |
| ORGANIZATION | HESS CORPORATION | REPORTED_BY |
| ROOT_CAUSE_CATEGORY | Flammable solids, liquids and gases | CATEGORIZED_AS |
| ORGANIZATION | light plant | REPORTED_BY |

### Annotation

This record was selected due to having causal keyword matches, but on close reading the causal language is hypothetical, not factual. **It is correct to leave all annotation fields blank.**

| Field | Value |
|-------|-------|
| *(all annotation fields)* | *(blank)* |
| annotator_notes | No causal relationship identifiable in narrative — the phrase "could potentially cause the diesel to ignite" is a hypothetical risk observation, not a description of something that actually happened. No ignition event occurred. |

**Why this annotation?** The keyword "cause" triggered this record's selection, but context shows it is speculative: "could potentially cause the diesel to ignite." Nothing ignited. The narrative describes a hazardous condition that was observed (spilled diesel near an exhaust), not an incident with an actual cause-and-effect sequence. The guidelines require that causes be "stated or strongly implied" — a hypothetical future risk does not qualify. Leaving all fields blank is the correct and expected answer here. Do not force an annotation just because causal keywords appear.

---


## Example 5: Ambiguous

**Record:** 522905
**Stratum:** falls_slips
**Causal Matches:** 1.0
**Causal Density:** 0.0286
**Category:** Work environment - Falls, slips and trips on same level (without potential to fall to lower level)

### Narrative

> On 17th January 2017 around 2.30pm, One of the employees working in 4th Floor, While sitting on the chair all of sudden fell down due to chair bottom support got broken. No injury took place.

### Existing Entities

| Type | Value | Relation |
|------|-------|----------|
| LOCATION | Chennai Building 1 | OCCURRED_AT |
| LOCATION | Chennai | OCCURRED_AT |
| LOCATION | India | OCCURRED_AT |
| LOCATION | India | OCCURRED_AT |
| ORGANIZATION | TECHNIPFMC | REPORTED_BY |
| ROOT_CAUSE_CATEGORY | Falls, slips and trips on same level (without potential to fall to lower level) | CATEGORIZED_AS |
| LOCATION | 4th floor | OCCURRED_AT |
| EQUIPMENT | chair | INVOLVED |
| INJURY_TYPE | No injury took place | RESULTED_IN |

### Annotation

This record describes an incident where the immediate cause is stated, but the root cause (why the chair broke) is not explained. Use MEDIUM confidence.

| Field | Value |
|-------|-------|
| caused_by_1_cause | chair bottom support failure |
| caused_by_1_evidence | "fell down due to chair bottom support got broken" |
| caused_by_1_confidence | MEDIUM |
| annotator_notes | Immediate cause of fall is explicit ("due to chair bottom support got broken"), but why the support broke is not stated — defective equipment, overloading, and wear are all plausible. Confidence is MEDIUM rather than HIGH because the causal phrasing is grammatically imprecise ("got broken" implies the breakage happened but does not confirm it as a pre-existing failure vs. happening at that moment). |

**Why this annotation?** The narrative does use "due to," which normally warrants HIGH confidence, but there is genuine ambiguity about the nature of the failure. "Chair bottom support got broken" is an effect description, not a root cause explanation — it tells us what broke, not why it broke. A HIGH confidence annotation would imply the cause is fully understood; here it is only partially understood. MEDIUM is appropriate when the causal chain is implied but incomplete. Note that this is different from Example 4: here something did happen (the chair broke and someone fell), and there is a stated causal link — we just lack the full root cause. Do not leave it blank; annotate what you can and flag the gap in `annotator_notes`.

---
