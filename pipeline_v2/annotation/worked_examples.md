# Worked Examples for Causal Chain Annotation

These examples show how to produce JSONL edges from incident narratives.
Each example includes the narrative, existing entities, and the edges
with reasoning.

---

## Example 1: Simple Single Cause

**Record:** 574147
**Category:** Fire & Explosion - Flammable solids, liquids and gases

### Narrative

> Laminated plastic coated empty wooden box accumulated near GTG open area, got small fire due to High atmospheric temperature. Our one of Engineer observed and immediately extinguished by using sand.

### Edges

```json
{"record_no": 574147, "source": "high atmospheric temperature", "source_type": "Condition", "relation": "CAUSAL", "target": "small fire", "target_type": "Event", "evidence": "got small fire due to High atmospheric temperature"}
```

**Why?** Single explicit cause with "due to". High atmospheric temperature (Condition) caused the fire (Event). Source = cause, target = effect.

---

## Example 2: Multi-Factor (Multiple CAUSAL Edges)

**Record:** 516010
**Category:** Ergonomics - Manual handling

### Narrative

> During manually shifting of portable scaffold (1.5MX1M) by four number of manpower, due to uneven surface and unbalancing it was tilted on ground. No injury/ property damage caused due to the incident.

### Edges

```json
{"record_no": 516010, "source": "unbalancing during manual shift", "source_type": "Condition", "relation": "CAUSAL", "target": "scaffold tilted on ground", "target_type": "Event", "evidence": "due to uneven surface and unbalancing it was tilted on ground"}
{"record_no": 516010, "source": "uneven surface", "source_type": "Condition", "relation": "CAUSAL", "target": "scaffold tilted on ground", "target_type": "Event", "evidence": "due to uneven surface and unbalancing it was tilted on ground"}
```

**Why?** Two factors contributed to the same outcome. Both are CAUSAL — the old distinction between "cause" and "contributing factor" is now unified under CAUSAL. Each gets its own edge pointing to the same target.

---

## Example 3: Causal Chain (Multiple Sequential CAUSAL Edges)

**Record:** 677880
**Category:** Fire & Explosion - Flammable solids, liquids and gases

### Narrative

> Welding gas hose was caught on fire due to the overhead splash that fell on the welding hose. Fire has started due to arc air sparks which has caused the rupture of a welding hose. The Fire was extinguished by the CO2 gas in the hose after the rupture of the hose.

### Edges

```json
{"record_no": 677880, "source": "arc air sparks", "source_type": "Equipment", "relation": "CAUSAL", "target": "fire on welding gas hose", "target_type": "Event", "evidence": "Fire has started due to arc air sparks"}
{"record_no": 677880, "source": "overhead splash falling on welding hose", "source_type": "Event", "relation": "CAUSAL", "target": "welding gas hose caught fire", "target_type": "Event", "evidence": "Welding gas hose was caught on fire due to the overhead splash that fell on the welding hose"}
{"record_no": 677880, "source": "fire from arc air sparks", "source_type": "Event", "relation": "CAUSAL", "target": "rupture of welding hose", "target_type": "Event", "evidence": "Fire has started due to arc air sparks which has caused the rupture of a welding hose"}
{"record_no": 677880, "source": "rupture of welding hose", "source_type": "Event", "relation": "CAUSAL", "target": "fire extinguished by CO2 gas", "target_type": "Event", "evidence": "The Fire was extinguished by the CO2 gas in the hose after the rupture of the hose"}
```

**Why?** Rich causal chain. Each step A→B gets its own CAUSAL edge. The old LED_TO chain format is replaced by multiple CAUSAL edges, each capturing one link in the sequence. Direction is consistent: source = cause, target = effect.

---

## Example 4: No Causal Relationship (Zero Edges)

**Record:** 712201
**Category:** Fire & Explosion - Flammable solids, liquids and gases

### Narrative

> While checking light towers, I noticed a large amount of Diesel had been spilled while filling the fuel tank and had flooded the bottom of the Light plant. The exhaust runs through the bottom of the containment and could potentially cause the diesel to ignite.

### Edges

*(none)*

**Why?** The causal language is hypothetical: "could potentially cause the diesel to ignite." Nothing actually happened — this is an observation of a hazardous condition, not an incident with a causal chain. Producing zero edges is correct.

---

## Example 5: Ambiguous Cause

**Record:** 522905
**Category:** Work environment - Falls, slips and trips

### Narrative

> On 17th January 2017 around 2.30pm, One of the employees working in 4th Floor, While sitting on the chair all of sudden fell down due to chair bottom support got broken. No injury took place.

### Edges

```json
{"record_no": 522905, "source": "chair bottom support broke", "source_type": "Equipment", "relation": "CAUSAL", "target": "employee fell down", "target_type": "Event", "evidence": "fell down due to chair bottom support got broken"}
```

**Why?** Single cause with "due to". The root cause (why the chair broke) is not stated — but we annotate what IS stated. The chair breaking (Equipment) caused the fall (Event). We don't speculate about defective equipment or wear.

---
