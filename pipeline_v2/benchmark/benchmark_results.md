# L1 Benchmark Query Results

**Generated:** 2026-03-21
**Graph:** 100,407 nodes, 233,856 edges
**Records:** 19,820 metadata rows, 19,851 incident nodes
**Layer:** L1 + L2 (34,499 causal edges)

## 1. Summary Table

| ID | Query | Type | Coverage | Result | Diagnosis | Validation |
|------|-------|------|:--------:|--------|-----------|:----------:|
| AG-01 | Root causes of dropped object incidents | Aggregation | ✅ | 1026 incidents, 43 root_cause_category values, top: Stored energy (dropped objects) | CLEAN | VALIDATED |
| AG-02 | Countries with most high-severity incidents | Aggregation | ✅ | 167 incidents, 22 location values, top: USA | CLEAN | VALIDATED |
| AG-03 | Most common equipment by incident count | Aggregation | ✅ | 19851 incidents, 13446 equipment values, top: forklift | ER_NEEDED | — |
| AG-04 | Incident type x business unit crosstab | Aggregation | ✅ | Crosstab: 4 business_unit values x 3 incident_type values | DATA_SPARSE | — |
| AG-05 | Monthly trend of fall/slip incidents | Aggregation | ✅ | 1695 incidents across 110 months | CLEAN | VALIDATED |
| AG-06 | Severity distribution by impact type | Aggregation | ✅ | Crosstab: 10 impact_type values x 6 severity_bin values | CLEAN | — |
| CJ-01 | Corrosion -> equipment failure -> fire (L2) | Conjunctive | ✅ | 34,499 causal edges; 800 for fire/explosion | CLEAN | — |
| CJ-02 | Crane + back + offshore + high severity | Conjunctive | ✅ | 0 incidents | KNOWN_SPARSE | — |
| CJ-03 | Maintenance fail + pipe + environmental + Middle East | Conjunctive | ✅ | 0 incidents | KNOWN_SPARSE | — |
| CJ-04 | Equipment: accident + near-miss same location/year | Conjunctive | ✅ | 539 dual-risk equipment/location/year combos | CLEAN | — |
| CJ-05 | Procedural -> dropped -> head/hand injury (L2) | Conjunctive | ✅ | 324 incidents; 12 procedural causal edges | CLEAN | — |
| CJ-06 | Falls/slips + vehicle + construction | Conjunctive | ✅ | 16 incidents | CLEAN | DRIFT |
| CJ-07 | Primary effects of corrosion (L2) | Conjunctive | ✅ | 137 corrosion causal edges across 104 incidents | CLEAN | — |
| GL-01 | Safety risk clusters (Louvain) | Global | ✅ | 11125 communities detected | CLEAN | — |
| GL-02 | Equipment recurring across regions | Global | ✅ | 144 equipment types span 5+ regions | ER_NEEDED | — |
| GL-03 | Temporal trend of incident types | Global | ✅ | Crosstab: 10 year values x 3 incident_type values | CLEAN | — |
| GL-04 | Hub centrality analysis | Global | ✅ | Hub analysis: degree + PageRank top 20 | CLEAN | — |
| IOGP-01 | Moving vehicle/mobile equipment incidents | Aggregation | ✅ | 2008 incidents, 122 injury_type values, top: injuries | ER_NEEDED | — |
| IOGP-02 | Dropped object incidents by severity | Aggregation | ✅ | Crosstab: 6 severity_bin values x 10 year values | CLEAN | — |
| IOGP-03 | Stored energy / snap-back incidents | Single-hop | ✅ | 114 incidents | CLEAN | — |
| IOGP-04 | Pressurized system incidents with containment loss | Multi-hop | ✅ | 192 incidents | ER_NEEDED | — |
| IOGP-05 | Electrical incidents with LOTO failures (L2) | Conjunctive | ✅ | 142 incidents; 9 FAILED_CONTROL edges | CLEAN | — |
| IOGP-06 | Working at height incidents with fall protection gaps | Multi-hop | ✅ | 246 incidents, 76 body_part values, top: left hand | ER_NEEDED | — |
| IOGP-07 | Mechanical lifting incidents with rigging failures | Multi-hop | ✅ | 2001 incidents, 152 injury_type values, top: injuries | ER_NEEDED | — |
| IOGP-08 | Machinery/tools incidents with hand/finger injuries | Multi-hop | ✅ | 200 incidents | ER_NEEDED | — |
| MH-01 | Equipment in containment->injury at offshore | Multi-hop | ✅ | 1 incidents, 2 equipment types | CLEAN | — |
| MH-02 | Injuries from equipment failures during maintenance | Multi-hop | ✅ | 29 incidents, 19 pairs | CLEAN | VALIDATED |
| MH-03 | Clients with vessel + back injury | Multi-hop | ✅ | 47 incidents, 93 organization values, top: OCM | ER_NEEDED | — |
| MH-04 | Top injury types per top-5 equipment | Multi-hop | ✅ | Injury breakdown for top 5 equipment | ER_NEEDED | — |
| MH-05 | Hand + pipe + Asia Pacific | Multi-hop | ✅ | 6 incidents | CLEAN | — |
| MH-06 | Severity: trucks vs cranes | Multi-hop | ✅ | Truck vs crane severity comparison | ER_NEEDED | — |
| MH-07 | Scaffold near-misses by location | Multi-hop | ✅ | 121 incidents, 33 location values, top: Sabetta | ER_NEEDED | DRIFT |
| MH-08 | Hydraulic valve -> injury outcome | Multi-hop | ⚠️ | 1 incidents, 0 injury_type values | DATA_SPARSE | — |
| SC-01 | Spot-check: forklift mirror caught manifold (#623703) | Single-hop | ⚠️ | 1 items: ['forklift'] | EXTRACTION_GAP | — |
| SC-02 | Spot-check: electrical substation feeder fire (#570187) | Single-hop | ✅ | 3 items: ['Connector link', 'feeder box', 'feeder breaker'] | CLEAN | — |
| SC-03 | Spot-check: forklift hit PGB in yard (#602346) | Single-hop | ✅ | 2 items: ['PGB', 'forklift'] | CLEAN | — |
| SC-04 | Spot-check: press + back pain (#14338) | Single-hop | ✅ | 1 items: ['press'] | CLEAN | — |
| SC-04b | Spot-check: press + back pain body part (#14338) | Single-hop | ✅ | 1 items: ['lower back'] | CLEAN | — |
| SC-05 | Spot-check: ROV marker buoys dropped (#500389) | Single-hop | ✅ | 4 items: ['chain', 'football float', 'marker buoys', 'odom weight'] | EXTRACTION_GAP | — |
| SC-06 | Spot-check: fall + head cuts on barrier (#8712) | Single-hop | ✅ | 1 items: ['CEU 25 barrier'] | CLEAN | — |
| SC-06b | Spot-check: fall head cuts body parts (#8712) | Single-hop | ✅ | 3 items: ['face', 'forehead', 'head'] | CLEAN | — |
| SC-07 | Spot-check: wire sling + crane lip cut (#511771) | Single-hop | ✅ | 2 items: ['crane hook', 'wire rope sling'] | CLEAN | — |
| SC-07b | Spot-check: wire sling lip cut body part (#511771) | Single-hop | ✅ | 1 items: ['lower lip'] | CLEAN | — |
| SC-08 | Spot-check: forklift + truck collision (#324) | Single-hop | ✅ | 1 items: ['20T Forklift'] | CLEAN | — |
| SC-09 | Spot-check: crane exit + head cut (#18312) | Single-hop | ✅ | 2 items: ['crane', 'plastic sun visor'] | CLEAN | — |
| SC-09b | Spot-check: crane exit head cut body part (#18312) | Single-hop | ✅ | 1 items: ['head'] | CLEAN | — |
| SH-01 | Forklift incidents in 2022 | Single-hop | ✅ | 71 incidents | ER_NEEDED | CLOSE |
| SH-02 | Equipment for incident #29857 | Single-hop | ⚠️ | 3 items: ['ROV', 'lanyard', 'pry bar'] | EXTRACTION_GAP | — |
| SH-03 | Body parts in crane incidents | Single-hop | ✅ | 1444 incidents, 192 body_part values, top: finger | ER_NEEDED | — |
| SH-04 | Locations for valve incidents | Single-hop | ✅ | 387 incidents, 36 location values, top: USA | ER_NEEDED | — |
| SH-05 | Injuries at offshore installations | Single-hop | ✅ | 1120 incidents, 124 injury_type values, top: cut | CLEAN | VALIDATED |
| SH-06 | Incidents reported by Shell Offshore | Single-hop | ✅ | 60 incidents | ER_NEEDED | VALIDATED |

**Overall:** 49 ✅ FULL / 3 ⚠️ PARTIAL / 0 ❌ FAIL out of 52 queries

**Diagnosis breakdown:**
- CLEAN: 30
- ER_NEEDED: 15
- EXTRACTION_GAP: 3
- DATA_SPARSE: 2
- KNOWN_SPARSE: 2

**Ground truth validation:**
- VALIDATED: 6
- CLOSE: 1
- DRIFT: 2
- —: 43

## 2. Per-Query Details

### AG-01: Root causes of dropped object incidents
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 1026
Distinct ROOT_CAUSE_CATEGORY values: 43
Top 10:
  Stored energy (dropped objects): 367
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 129
  Hazard Identification & Risk Assessment: 66
  Equipment condition: 59
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 45
  Planning and coordination of works: 43
  Manual handling: 32
  Equipment Suitability: 29
  Stored energy (pressure, tension): 28
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 24
```

### AG-02: Countries with most high-severity incidents
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 167
Distinct LOCATION values: 22
Top 10:
  USA: 44
  UK: 34
  Brazil: 30
  Norway: 21
  India: 6
  France: 6
  Australia: 3
  Angola: 3
  Malaysia: 3
  Canada: 3
```

### AG-03: Most common equipment by incident count
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 19851
Distinct EQUIPMENT values: 13446
Top 20:
  forklift: 771
  crane: 622
  ROV: 290
  pallet: 186
  PPE: 145
  excavator: 141
  equipment: 131
  compressor: 121
  forks: 117
  overhead crane: 110
  fire extinguisher: 100
  manlift: 98
  reel: 98
  gloves: 96
  sling: 94
  safety glasses: 93
  machine: 93
  pump: 82
  winch: 81
  truck: 81
```

### AG-04: Incident type x business unit crosstab
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** DATA_SPARSE | **Time:** 0.1s

```
business_unit null rate: 14007/19820 (70.7%)

| business_unit | Accident | Near Miss | Unknown | Total |
|---|---|---|---|---|
| Unknown | 5190 | 3368 | 5449 | 14007 |
| Subsea | 1756 | 1184 | 0 | 2940 |
| REMS | 757 | 970 | 0 | 1727 |
| Surface | 850 | 296 | 0 | 1146 |
```

### AG-05: Monthly trend of fall/slip incidents
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Total incidents: 1695
Months with data: 110
Yearly breakdown:
  2016: 187
  2017: 321
  2018: 306
  2019: 231
  2020: 154
  2021: 264
  2022: 53
  2023: 64
  2024: 65
  2025: 50
```

### AG-06: Severity distribution by impact type
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
impact_type null rate: 217/19820 (1.1%)

| impact_type | 1.0 | 2.0 | 3.0 | 4.0 | 5.0 | Unknown | Total |
|---|---|---|---|---|---|---|---|
| Injury | 0 | 0 | 0 | 0 | 0 | 8357 | 8357 |
| Injury/Illness | 1281 | 1125 | 812 | 139 | 22 | 0 | 3379 |
| Financial Impact | 0 | 0 | 0 | 0 | 0 | 2444 | 2444 |
| Environment | 477 | 154 | 40 | 0 | 0 | 1319 | 1990 |
| Damage - Financial impact | 691 | 930 | 136 | 5 | 1 | 0 | 1763 |
| Damage | 0 | 0 | 0 | 0 | 0 | 1268 | 1268 |
| Unknown | 0 | 0 | 0 | 0 | 0 | 217 | 217 |
| Occupational Illness | 0 | 0 | 0 | 0 | 0 | 160 | 160 |
| Reputation | 0 | 0 | 0 | 0 | 0 | 121 | 121 |
| Fire/Explosion | 0 | 0 | 0 | 0 | 0 | 121 | 121 |
```

### CJ-01: Corrosion -> equipment failure -> fire (L2)
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
L2 causal edges in graph: 34,499
  CAUSAL: 32,314
  PRECEDED_BY: 508
  FAILED_CONTROL: 828

Fire/explosion incidents: 322
  With causal edges: 238
  Total causal edges: 800
  Tautological (fire→fire) filtered: 192

Top root causes for fire/explosion (non-tautological):
  fire: 15
  smoldering: 7
  fuel truck leaking diesel fuel: 6
  smell of smoke and soot on the ground: 4
  cotton waste pieces inside the gaps: 4
  towels stored in the steel cupboard: 3
  wooden box containing spares caught fire: 3
  explosion in the burning chamber: 3
  small fire: 3
  flash back: 3

Corrosion + fire/explosion intersection: 0 records
  Causal edges in these: 0
```

### CJ-02: Crane + back + offshore + high severity
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** KNOWN_SPARSE | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-03: Maintenance fail + pipe + environmental + Middle East
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** KNOWN_SPARSE | **Time:** 0.1s

```
Matching incidents: 0
```

### CJ-04: Equipment: accident + near-miss same location/year
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.4s

```
Equipment nodes scanned: 3000
Dual-risk (accident + near-miss at same location/year): 539 combos
Top 10:
  crane @ Aberdeen (2017): 10 accidents, 19 near-misses
  ROV @ Aberdeen (2018): 22 accidents, 7 near-misses
  compressor @ Sabetta (2018): 22 accidents, 7 near-misses
  compressor @ Sabetta (2017): 14 accidents, 15 near-misses
  forklift @ Houston (2018): 15 accidents, 10 near-misses
  ROV @ Aberdeen (2017): 16 accidents, 8 near-misses
  Train 1 @ Sabetta (2017): 9 accidents, 14 near-misses
  crane @ Aberdeen (2024): 10 accidents, 12 near-misses
  crane @ Aberdeen (2016): 16 accidents, 6 near-misses
  forklift @ Houston (2023): 4 accidents, 13 near-misses
```

### CJ-05: Procedural -> dropped -> head/hand injury (L2)
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
Dropped-object incidents: 4,072
  With head/hand injury: 324
  With L2 causal edges: 212
  Total causal edges: 607

Procedural causal edges: 12
  Samples:
    [540653] pinched his right hand IV finger with the container door --CAUSAL--> immediately after the incident, he informed his supervisor and reported to the REGA JV clinic
    [575162] crane drive was instructed to come up with the hook --CAUSAL--> finger came loose
    [629667] deviation from procedure when an individual entered the table prior to the incident to adjust a winch block --CAUSAL--> slipping of the Chinese finger on the tail end of the test piece
    [644074] misunderstood in communication --CAUSAL--> raising the mastil tensing chains
    [687682] I/P felt dizzy --CAUSAL--> Shift Supervisor advised to call 111 for advice
    [703112] inadequate lighting over the bed to assess patients --CAUSAL--> the bed had to be moved
    [546828] second finger --CAUSAL--> HSE Supervisor brought him to the First Aid point for the control and treatment
    [556525] pinching IP’s left thumb --CAUSAL--> notifying supervisor
    [556525] notifying supervisor --CAUSAL--> sent to REGA clinic
    [534066] assistant supervisor removed the stone with his right hand --CAUSAL--> tailgate fully close
    [571609] Op believed that it was just a nip --CAUSAL--> Op contacted the Shift Supervisor on Tuesday evening
    [571609] increase in the pain in his finger --CAUSAL--> Op contacted the Shift Supervisor on Tuesday evening

Top causal factors for dropped → head/hand:
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 10
  fall with his leg between two steel structure: 3
  left hand: 3
  Rt middle finger pain: 3
  slip: 3
  banging head on shelf lip: 3
  fall from chair: 3
  laceration: 3
  pinched his right hand IV finger with the container door: 2
  wind gust: 2
```

### CJ-06: Falls/slips + vehicle + construction
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
Matching incidents: 16
Sample: ['INCIDENT::11732', 'INCIDENT::24216', 'INCIDENT::520161', 'INCIDENT::527205', 'INCIDENT::543663']
```

### CJ-07: Primary effects of corrosion (L2)
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.5s

```
Corrosion-source CAUSAL edges: 137
Unique incidents with corrosion causes: 104

Effects by category:
  leak/release: 10 edges (e.g. ['foam extinguisher discharged to cool equipment', 'leak', 'leakage of hydraulic oil'])
  equipment failure: 9 edges (e.g. ['blisters on the soles of his feet and the day after they burst', 'container failure', 'clutched gearing inside of the lever hoist failed'])
  safety system impact: 5 edges (e.g. ['Low Level alarm on compensator thruster group 2', 'Alarm was Low Lube Oil Pressure upper gearbox', 'Tunnel Thruster no 2 (BT3) due to power drop to hydraulic pump and signal command “External Shutdown” from RR controller to Siemens frequency converter drive'])
  structural damage: 4 edges (e.g. ['loose bolt with nuts and washer still in place in its original mounting hole on the top of the outboard main frame trolley clevis', 'damage to one of the hoses', 'corrosion pinhole'])

  Other effects: 109 edges
    loss of hydraulic oil: 3
    fire: 2
    heat build up: 1
    positioning loss: 1
    upper hinge broke loose: 1
```

### GL-01: Safety risk clusters (Louvain)
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 8.4s

```
Total communities: 11125
Top 10 by size:

  Community 1 (size=10602):
    INCIDENT: 3177 (e.g. ['NEAR MISS 606878 - Deep Arctic - Near Miss -Damage to container due to loss of control during backloading operations - Bhar Essalam - 064081C002 - Sat 8th Sept 18.', 'ACCIDENT 604711 - Damage Incident - 29.08.2018 - Deep Orient - Greater Enfield - Hydraulic line pinched on knuckle boom deck crane', 'INCIDENT 675923 - Minor Equipment Damage - 077290C003 - Duva & P1 SPS and SURF EPCI - Deep Energy – 09 April 2020 – Stopper on gangway sheared'])
    EQUIPMENT: 3017 (e.g. ['Horizontal Forward Port thruster', 'whipline hook', 'Grandberg EX7114 Winter Glove'])
    LOCATION: 1991 (e.g. ['air handling room', 'freeboard deck', 'Averoy Norsea Quay 21'])
    ORGANIZATION: 1643 (e.g. ['Subsea7', 'Iqaris', 'Ithaca Vorlich Project'])
    BODY_PART: 259 (e.g. ['extremidade inferior', '5th digit', 'patella'])
    EVENT: 250 (e.g. ['activated itself with contact of water', 'beam fell from the back of the truck bed to the ground', 'blade broke'])
    INJURY_TYPE: 105 (e.g. ['2cm abrasion/cut', 'finger contusion', 'minor capillary bleeding'])
    CONDITION: 61 (e.g. ['unexpected gust of wind', 'inappropriate fastening', 'unauthorized / unapproved route of the release'])
    INJURY: 40 (e.g. ['Injury: upper torso', 'contusion of the 4th finger of the right hand', 'incised wound of the right hand at the thumb area'])
    ACTION: 35 (e.g. ['toe boards should be fitted', 'rigging failed', 'three workers were trying to move a steel beam manually'])
    MATERIAL: 10 (e.g. ['piece of wood weighing approximately 1.55 kg', 'small piece of material', 'empty food container and empty IBC'])
    PERSON: 7 (e.g. ['people in the radius of the fall of the pipes', 'operator responsible for driving the wire was near', 'third party employee in the cell'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Hyperbaric work environment', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)', 'Equipment Suitability'])

  Community 2 (size=9993):
    INCIDENT: 3952 (e.g. ['ACCIDENT 16097 - Contractor bit by unknown animal/insect', 'ACCIDENT 500034 - Coffee burn', 'ACCIDENT 8295 - First Aid Incident - Wellhead - Stephenville'])
    EQUIPMENT: 2374 (e.g. ['loop and drill', 'torque pump', 'heater 1400'])
    LOCATION: 1622 (e.g. ['fast channel', 'frac pad', 'Cell 4'])
    ORGANIZATION: 1060 (e.g. ['overhead door company', 'HEB', 'third party vendor'])
    BODY_PART: 337 (e.g. ['upright', 'cement pillar', '3rd finger of the left hand'])
    EVENT: 299 (e.g. ['puncture to the metal side wall', 'IP was stretched, given over the counter Aleve, and was given a full release to go back to work', 'handle was bent back to its engaged position'])
    INJURY_TYPE: 142 (e.g. ['insect/bug bite', 'puncture', 'personal illness'])
    CONDITION: 80 (e.g. ['electrical current transfer', 'weight shifted during movement', 'discomfort in his right side'])
    ACTION: 59 (e.g. ['rope slipped out of the employee’s hand', 'driver was signaled by two spotters one on either sides of the truck as he drove through the shop', 'Employee was more towards the side'])
    INJURY: 41 (e.g. ["crushing and lacerating of the employee's right ring and little finger", 'landing on right side and elbow', 'light outflow above the left neck'])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['Basic Organizational', 'Over-consumption of energy, natural resources (water, etc.)', 'Motor Vehicle Worksite Accident'])
    MATERIAL: 10 (e.g. ['fluid in the picture was from a prior operation removing the hoses', 'anti-histamine tablet', 'strawberries that exceeded the ground'])
    PERSON: 5 (e.g. ['Driver', 'trained First Aider', 'Collaborators (two) third parties coming from home to work, walking along the side of a small bridge'])

  Community 3 (size=5416):
    INCIDENT: 1877 (e.g. ['NEAR MISS 15539 - [Mero 2] Near Miss - Queda de plet durante movimenta??o na sala de pintura - IMETAME (n?o apropriado)', 'NEAR MISS 22381 - Near Miss - NG, S?o Paulo, Brazil - Uaru - Bypassing Safety Controls during a Lifting', 'ACCIDENT 612184 - FAC - Skandi Búzios -  Cut in left hand / Corte na m?o esquerda'])
    EQUIPMENT: 1227 (e.g. ['cavaletes', 'shipyard crane', 'Manitou strawber'])
    LOCATION: 1001 (e.g. ['Alexandre Buaiz avenue', 'Douala', 'Super Pesa II cabin'])
    ORGANIZATION: 706 (e.g. ['FRT', 'line 572', 'immediate'])
    BODY_PART: 235 (e.g. ['main wing', 'stickman', 'nose'])
    EVENT: 158 (e.g. ['gate fell from a height of 6 meters', 'control of the principle of fire', 'the fact was identified by the watch during the day-to-day safety round'])
    INJURY_TYPE: 110 (e.g. ['paralysis', 'flat-foot fall', 'No injury incident'])
    INJURY: 33 (e.g. ['hospitalized', 'minor abrasions on her legs and arms', 'counter blow on the canela'])
    CONDITION: 33 (e.g. ["sling strap got stuck to GV's bonnet stem", 'nobody was around the working area', 'no people in line of fire'])
    ACTION: 17 (e.g. ['sudden pulling movement of the current', 'misjudged his next step', 'not using gloves as required'])
    ROOT_CAUSE_CATEGORY: 13 (e.g. ['Access/Egress', 'Tool condition', 'Pinch point'])
    MATERIAL: 4 (e.g. ['PVC connections, weighing a maximum of 0.65kg', 'concrete pieces', 'nylon parts (3 on main deck, one on the barge)'])
    PERSON: 2 (e.g. ['operator in the face', 'people in the environment'])

  Community 4 (size=4178):
    INCIDENT: 1313 (e.g. ['INCIDENT 716553 - FAC - Arctic LNG 2 - Gydan Site - 27 April 2021 - Cut to the finger', 'ACCIDENT 565505 - FAC - Yamal LNG Project - Sabetta - 1.12.2017 - Face abrasion', 'ACCIDENT 569432 - FAC - Yamal LNG Project - Sabetta - 26.01.2018 - frostnip of fingers'])
    LOCATION: 743 (e.g. ['BOG Compressor Storage area', 'warehouse space', '314-SPP-012'])
    EQUIPMENT: 639 (e.g. ['proper gloves', 'I/V needle', 'pachometer'])
    ORGANIZATION: 574 (e.g. ['Tadano', '3rd level SOGAZ clinic', 'REGA JV Companies'])
    INJURY_TYPE: 241 (e.g. ['dislocation of radial bone', 'shoulder contusion', 'spider bite'])
    BODY_PART: 237 (e.g. ['sacral region', 'left hand palm side', 'ligament apparatus'])
    EVENT: 187 (e.g. ['slipped and fell striking his forehead against a staircase handrail', 'twisted his right ankle', 'can return to work normally in the same day'])
    INJURY: 100 (e.g. ['penetrating wound of the right eye, contusion and penetrating wound of upper and lower lid and of the right zygomatic region', 'spraining of ligaments of the right ankle joint', 'turned his left foot'])
    CONDITION: 65 (e.g. ['foul chemical smell', 'hole created', 'no other obstructions, loose objects or slip hazards in the area'])
    ACTION: 61 (e.g. ['stumbled over the board', 'stepping on left boot laces', 'advised for light duties for 1 week'])
    MATERIAL: 10 (e.g. ['hot porrige', 'small foreign body (most likely dust or a similar small particle)', 'Antibiotic medication'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Falls, slips and trips on same level (without potential to fall to lower level)', 'Traffic Management / Routes / Pedestrian path', 'Uncontrolled chemical or physical reaction'])
    PERSON: 3 (e.g. ['REGA slinger', "IP's face", 'SNEMA wireman walking backwards'])

  Community 5 (size=3839):
    INCIDENT: 1477 (e.g. ["INCIDENT 673200 - IE - 06/03/2020 - Extérieur W9 / Tente chantiers montage - Lumières allumées en journée alors que pas de matériel/pas d'activité", 'INCIDENT 666249 - FAC / NM - 05/01/2020 /blessure au poignet dégainage au W3', 'ACCIDENT 503402 - FAC - BA62 - 02/08/2016 - Choc à la main'])
    EQUIPMENT: 756 (e.g. ['nappe 2', '1 Meter pedon', 'safe'])
    LOCATION: 520 (e.g. ['Salengro street', 'BFT1', 'local test'])
    ORGANIZATION: 418 (e.g. ['MET', 'MGC', 'roulev operators'])
    BODY_PART: 176 (e.g. ['back level', 'lapersoon foot', 'tle'])
    EVENT: 175 (e.g. ['fall down from bicycle', 'person left the nursery around 10h30', 'hit suddenly the duct that was insulated'])
    INJURY_TYPE: 117 (e.g. ['muscle breakdown', 'deformed march', 'mechanical crackings'])
    INJURY: 77 (e.g. ['back pain persisted', 'unexpected discomfort on the back', 'limited movement to his left wrist'])
    ACTION: 57 (e.g. ['put one side of the bolt cutters handle against a concrete column and held the other handle with both hands', 'handling of chainblock on the floor', 'flushing arm with cold water'])
    CONDITION: 47 (e.g. ['weight of the assembly (Raccord/Vanne/Tuyaux) in false door', 'residual press in the mango', 'low pressure only'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['Posture (constraint or restricted environment)', 'Environment- Unsorted waste, no traceability of the waste;?', 'Psycho social - Workload (Overload/Underload)'])
    PERSON: 5 (e.g. ['SA protected by its helmet', 'operator', 'employee'])
    MATERIAL: 5 (e.g. ['red-colored residual water', 'particle of weld bark', 'red-colored water recovered in the network'])

  Community 6 (size=3146):
    INCIDENT: 898 (e.g. ['INCIDENT 674103 - NM_HURL-Sindri_077625_Sling got sheared off', 'ACCIDENT 562787 - First Aid Case_071338C001 - 918 - HGU Reformer Revamp_Bina_11/30/2017_IP got abrasion injury', 'ACCIDENT 520569 - Technip Chennai - Damage Incident - due to external factor'])
    EQUIPMENT: 614 (e.g. ['04 nos of cotter bolts', 'scaffolding pipe', 'Garden pruning knife'])
    LOCATION: 563 (e.g. ['South side of L1 shop', 'L & T area', 'underneath area'])
    ORGANIZATION: 330 (e.g. ['waste disposal vendor', 'five man team', 'house keeping department'])
    EVENT: 287 (e.g. ['left palm got stuck between machine and interior furnace wall', 'partially tilted', 'former falling to the floor'])
    BODY_PART: 125 (e.g. ['2nd phalange', 'Little finger', 'left-hand forefinger'])
    CONDITION: 112 (e.g. ['inherent weakness in his right ankle', 'clamps angle exceeding 10% with vertical plane', 'nameplates not removed in time after installation'])
    INJURY_TYPE: 75 (e.g. ['impact/pinch point injury', 'bodily injury', 'gust of wind & rain'])
    ACTION: 63 (e.g. ['more force applied to complete the task', 'JSA reflecting work being performed', 'failure to wear gloves when installing the locking bar'])
    INJURY: 59 (e.g. ['minor cut injury on his lower lip', 'hit to the left eyebrow', 'fracture on right lateral ankle'])
    MATERIAL: 12 (e.g. ['hydraulic fluid on the ground', 'damaged buried cable (11KVA HT power cable, size: 185 Sq mm)', 'residual Oceanic 443'])
    PERSON: 5 (e.g. ['employee not stopping to check on employee', 'Injured Person (IP)', 'employee working on scaffold'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Use of personal protective equipment', 'Manual handling', 'Accumulation / Presence of explosive atmosphere'])

  Community 7 (size=3069):
    INCIDENT: 1035 (e.g. ['NEAR MISS 18158 - Car jerked forward and hit the barracks', 'ACCIDENT 9475 - Hall F -  LTI: Operator hit by spanner', 'ACCIDENT 635127 - MTI - 075688C004 - Fenja - Orkanger - Cut to head - 08/05/2019'])
    EQUIPMENT: 770 (e.g. ['cabinet', '"No hands" equipment', 'RLWI stack'])
    LOCATION: 492 (e.g. ['Chicksan', 'wellhead area', 'emergency room'])
    ORGANIZATION: 425 (e.g. ['WST', 'Mardahl Maskin AS', 'UCON-H'])
    BODY_PART: 111 (e.g. ['venstre underarm', 'clothes', 'distal joint'])
    EVENT: 95 (e.g. ['medic advised for me to travel onshore', 'snagged remote control', 'fell on floor'])
    INJURY_TYPE: 45 (e.g. ['3-4 cut', 'Prosedyre', 'slightly bruised'])
    CONDITION: 37 (e.g. ['stronger/brighter light', 'safety pin cutout groove', 'wound weeping through dressings'])
    INJURY: 28 (e.g. ['technician left eye', 'twist in the palm', 'reclassification to MIT'])
    ACTION: 21 (e.g. ['axle pin removal with hammer and punch', 'knocking a pry bar off the bench', 'Operator cleaned wound and put plaster/bandage to finger'])
    MATERIAL: 4 (e.g. ['steel chip', 'no material damage was inflicted', 'property and equipment were not damaged'])
    PERSON: 3 (e.g. ['emergency team on yard', 'deck rigging crew', 'person opening the door fast from another side without seeing me'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Radiation (ionising / non ionising)', '1. Internal NCR (issued by TechnipFMC or Partners)', 'Difficult/Hindered operability of tools and equipment'])

  Community 8 (size=2845):
    LOCATION: 668 (e.g. ['Hoxhaj', 'negative side of the river', 'Spiecapag'])
    INCIDENT: 659 (e.g. ['ACCIDENT 524276 - NON-Technip Owned - SCA-DA 08/A - 2529 TAP - Greece/KP19-W13 - 04/01/2017 - Polyurethane trench breaker catch fire', 'NEAR MISS 608997 - NON Technip Owned - SCA-NM (HiPo) 67 - 2529 TAP - Albania/KP 106+200 - 28/09/2018 - Worker on top of the form work of the retaining wall', 'ACCIDENT 530236 - NON Technip Owned - BNJ-MTC 02 - 2529 TAP - Greece/KP298-Row2 - 06/03/2017 - Pinched finger during Tie-In operations'])
    ORGANIZATION: 577 (e.g. ['OHPL', 'Feres Medical Facility', 'TAP Operations'])
    EQUIPMENT: 495 (e.g. ['weld-on adaptor', 'integrated safety break system', 'FOCA duct reel'])
    EVENT: 174 (e.g. ['tallest part of the structure was bending from the original position', 'Event("Cunningham exited the facility and began yelling at the other employees that had assembled.")', 'worker entering pipe without controls'])
    CONDITION: 76 (e.g. ['operators were complicit in the supervisor’s actions by not intervening', 'TBT was given but did not cover the risks of the activities', 'lack of concentration to her footing and surroundings'])
    BODY_PART: 52 (e.g. ['left top front', 'broken ribs', 'overhead line'])
    INJURY_TYPE: 46 (e.g. ['injury to personnel', 'small cut and bruise', 'near miss'])
    INJURY: 44 (e.g. ['FST struck in the chest', 'welder of crew A reported to be slightly affected by the electrostatic charge', 'stomach cramps and diarrhea'])
    ACTION: 40 (e.g. ['wearing nitrile gloves', 'failure to register in confined space entry log', 'relieved tooling'])
    MATERIAL: 8 (e.g. ['fuel materials that were inside the equipment', 'barbed wire made of elastic and cutting material', 'fine sand'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Illumination / sight / visibility', 'Inadequate Supervision', 'Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)'])
    PERSON: 2 (e.g. ['Nikita Chirko', 'the crew consisted of 1 supervisor, 2 excavator operators, 2 side boom operators'])

  Community 9 (size=1971):
    INCIDENT: 624 (e.g. ['ACCIDENT 542001 - FA - OUI JV Rapid - Pengerang, Johor - 3 June 2017 - The IP received first degree burns to his forearms when flames flared from the bottom of the gas cooker he was using', 'NEAR MISS 23225 - Forklift tires stuck at drain grating', 'ACCIDENT 502711 - FAC - General Office - Kuala Lumpur, Malaysia - 21st July 2016 - Minor cut to hand while wiping off the whiteboard'])
    EQUIPMENT: 444 (e.g. ['cup', 'low pressure oxygen gas hose', 'jumbo'])
    LOCATION: 426 (e.g. ['Bukit Dahlia', 'SQC workshop', 'GWA3'])
    ORGANIZATION: 285 (e.g. ['Offshore Base', 'nearest clinic', 'APSB'])
    EVENT: 64 (e.g. ['trap pressure release through the upper face sealing O-ring on the plug of the choke stem', 'send to CMF to receive first aid treatment', 'sludge hose became free from the filling hatch'])
    BODY_PART: 55 (e.g. ['lower hand', 'Head L', 'performing head'])
    INJURY_TYPE: 30 (e.g. ['facet arthropathy', 'Ligament TRO', 'light wound'])
    CONDITION: 18 (e.g. ['RCD did not trip', 'pressure gauge fitting defected because of wear and tear issue', 'power not available'])
    ACTION: 10 (e.g. ['area secured', 'crew and contractor stop the job', 'misstep to conduit pipe'])
    INJURY: 10 (e.g. ['pinched the tip of his thumb', 'bent the thumbnail back', 'personnel was in shock & experiencing hearing issues'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Weather Condition', 'Psycho social - Alcohol and drugs abuse', 'Electrical current / electrocution / ESD / electromagnetic Fields'])
    PERSON: 1 (e.g. ['stray dog'])
    MATERIAL: 1 (e.g. ['wooden packing block'])

  Community 10 (size=1921):
    INCIDENT: 643 (e.g. ['INCIDENT 723726 - Shell King Embayment- Accident - Shawcor Channelview - Oil Spill - Plant supervisor reported a hydraulic oil spill.', 'ACCIDENT 547695 - FA- TU Inc. (DRAPS) - 17.08.01 - Hand Incident', 'INCIDENT 654315 - PROCESS NC - Sheathing - Sheath Removal method, IP Struck with pry bar Ref 640483'])
    EQUIPMENT: 532 (e.g. ['Braider Number 7', 'Timber packing blocks', 'cardboard skip'])
    LOCATION: 288 (e.g. ['base of the carousel', 'Channelview', 'Thermal A side booth'])
    ORGANIZATION: 241 (e.g. ['COOPER ENERGY (SOLE) PTY. LTD.', 'QHSE Dept.', 'Bredero Shaw / Shawcor'])
    EVENT: 79 (e.g. ['Demobilisation', 'contamination of paved floor', 'Sparks and flame from plug/socket'])
    INJURY_TYPE: 43 (e.g. ['strained abdominal muscle', 'whiplash', 'type K repair'])
    BODY_PART: 38 (e.g. ['right hand knuckle', 'top of his thumb', 'Axle 11'])
    CONDITION: 32 (e.g. ['oil on the fan cowling', 'fitting between the manifold and the valve loosened', 'lack of correct information, instruction and training'])
    ACTION: 15 (e.g. ['bending down to measure pipe on the Thermal outbound deck', 'valve not secured to the stand', "Operator was looking up and didn't notice the chain hook caught the fixture table"])
    INJURY: 9 (e.g. ['Injury("lower back")', 'finger trapped between the door and the frame', 'foreign object in eye'])
    PERSON: 1 (e.g. ['gangway watchman was in place'])
```

### GL-02: Equipment recurring across regions
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.2s

```
Equipment appearing in 5+ regions: 144
  fire extinguisher: 8 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  Scaffold: 8 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  forklift: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  compressor: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  PPE: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  manlift: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  grinder: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  truck: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  crane: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  helmet: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  trailer: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  welding machine: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  gloves: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  scaffolding: 7 regions -> ['Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  machine: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  spool: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  air compressor: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  basket: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  ladder: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  ice pack: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
```

### GL-03: Temporal trend of incident types
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.4s

```
| year | Accident | Near Miss | Unknown | Total |
|---|---|---|---|---|
| 2018 | 1745 | 1250 | 0 | 2995 |
| 2017 | 1697 | 951 | 0 | 2648 |
| 2019 | 748 | 623 | 1269 | 2640 |
| 2021 | 122 | 173 | 2016 | 2311 |
| 2020 | 48 | 47 | 2110 | 2205 |
| 2016 | 1078 | 604 | 0 | 1682 |
| 2023 | 890 | 632 | 0 | 1522 |
| 2024 | 819 | 642 | 0 | 1461 |
| 2022 | 903 | 489 | 54 | 1446 |
| 2025 | 503 | 407 | 0 | 910 |
```

### GL-04: Hub centrality analysis
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 6.9s

```
Top 20 non-incident nodes by degree:
  LOCATION::Europe -- degree 7433
  ORGANIZATION::TECHNIPFMC -- degree 4688
  LOCATION::North America -- degree 4681
  LOCATION::USA -- degree 4322
  LOCATION::UK -- degree 3746
  LOCATION::Asia Pacific -- degree 3106
  LOCATION::Aberdeen -- degree 2522
  LOCATION::South America -- degree 2144
  LOCATION::Brazil -- degree 1727
  ROOT_CAUSE_CATEGORY::Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) -- degree 1581
  LOCATION::France -- degree 1447
  LOCATION::Houston -- degree 1354
  ROOT_CAUSE_CATEGORY::Hazard Identification & Risk Assessment -- degree 1307
  ORGANIZATION::JSC YAMAL LNG -- degree 1302
  ROOT_CAUSE_CATEGORY::Equipment condition -- degree 1260
  ROOT_CAUSE_CATEGORY::Falls, slips and trips on same level (without potential to fall to lower level) -- degree 1204
  ROOT_CAUSE_CATEGORY::Stored energy (dropped objects) -- degree 1183
  LOCATION::Le Trait -- degree 1113
  ROOT_CAUSE_CATEGORY::Hazardous liquids (exposure to / spill / loss of containment /pollution) -- degree 1092
  LOCATION::Norway -- degree 1064

Top 20 non-incident nodes by PageRank:
  LOCATION::Europe -- PR 0.003177
  LOCATION::North America -- PR 0.002177
  LOCATION::USA -- PR 0.001585
  LOCATION::Asia Pacific -- PR 0.001304
  LOCATION::UK -- PR 0.001190
  LOCATION::South America -- PR 0.000996
  ORGANIZATION::TECHNIPFMC -- PR 0.000654
  LOCATION::Brazil -- PR 0.000642
  LOCATION::France -- PR 0.000582
  LOCATION::Aberdeen -- PR 0.000538
  LOCATION::Norway -- PR 0.000396
  LOCATION::Houston -- PR 0.000341
  LOCATION::India -- PR 0.000335
  LOCATION::Africa -- PR 0.000333
  INJURY_TYPE::fire -- PR 0.000329
  LOCATION::Le Trait -- PR 0.000318
  LOCATION::Russia -- PR 0.000292
  LOCATION::Middle East -- PR 0.000268
  LOCATION::India -- PR 0.000259
  LOCATION::Rio de Janeiro -- PR 0.000249
```

### IOGP-01: Moving vehicle/mobile equipment incidents
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 2008
Distinct INJURY_TYPE values: 122
Top 10:
  injuries: 64
  cut: 16
  injury: 14
  minor damage: 11
  contusion: 10
  laceration: 10
  pain: 9
  abrasion: 8
  fracture: 7
  No one was injured: 7
```

### IOGP-02: Dropped object incidents by severity
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.4s

```
severity_bin null rate: 14007/19820 (70.7%)

| severity_bin | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Unknown | 1678 | 2639 | 2952 | 2558 | 2110 | 2016 | 54 | 0 | 0 | 0 | 14007 |
| 1.0 | 3 | 4 | 8 | 22 | 32 | 116 | 629 | 639 | 606 | 390 | 2449 |
| 2.0 | 1 | 4 | 26 | 34 | 35 | 112 | 493 | 559 | 571 | 374 | 2209 |
| 3.0 | 0 | 1 | 9 | 22 | 21 | 54 | 226 | 287 | 240 | 128 | 988 |
| 4.0 | 0 | 0 | 0 | 2 | 7 | 10 | 38 | 33 | 38 | 16 | 144 |
| 5.0 | 0 | 0 | 0 | 2 | 0 | 3 | 6 | 4 | 6 | 2 | 23 |
```

### IOGP-03: Stored energy / snap-back incidents
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
Matching incidents: 114
Sample: ['INCIDENT::10888', 'INCIDENT::12332', 'INCIDENT::12630', 'INCIDENT::12715', 'INCIDENT::13227']
```

### IOGP-04: Pressurized system incidents with containment loss
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 192
Sample: ['INCIDENT::10674', 'INCIDENT::10923', 'INCIDENT::10992', 'INCIDENT::11942', 'INCIDENT::12909']
```

### IOGP-05: Electrical incidents with LOTO failures (L2)
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.3s

```
Total FAILED_CONTROL edges in graph: 828
LOTO/electrical incidents (narrative match): 142
  With FAILED_CONTROL edges: 9
  FAILED_CONTROL edges in LOTO incidents: 9

Top failed controls in LOTO incidents:
  LOTO system: 1
  breaker closed without permission: 1
  restricted area where personnel are not allowed to enter unless a LOTO is performed: 1
  facilities: 1
  signs ("Under Commissioning" & "High Voltage Do Not Touch"): 1
  All Stop procedure: 1
  check valve 70-NRV-1012: 1
  gasket (which was due to be torqued the following day) failed at the end blind of the 48 inch spool: 1
  no visible damage was found on the Trolley Festoon or any other items: 1

Sample edges (hazard --FAILED_CONTROL--> barrier):
  [16262] deforming the door’s floor latch and breaking the padlock hasp of the LOTO system --> LOTO system | "breaking the padlock hasp of the LOTO system"
  [719499] construction team finish the termination work than put the stick ”cannot close” on the break --> breaker closed without permission | "construction team finish the termination work than put the s"
  [676087] pipes positioned on the line horizontal --> restricted area where personnel are not allowed to enter unless a LOTO is performed | "The area where the pipe fell, was a restricted area where pe"
  [23607] casing damage --> facilities | "Maintenance barriered the supply off"
  [636840] unlocked panel door (535-EVK-001) --> signs ("Under Commissioning" & "High Voltage Do Not Touch") | "the signs, although sufficient in number and clear in awaren"
  [681052] contact between pipe and manlift --> All Stop procedure | "The spotter called an All Stop as the pipe, but was not hear"
  [565034] wrong direction of installation of the check valve/non-return valve 070-NRV-1012 --> check valve 70-NRV-1012 | "The check valve 70-NRV-1012 wrong direction of installation "
  [654203] LOTO applied by Spiecapag on the valve was not effective, chain and padlock on the hand wheel only and the tag was deteriorated --> gasket (which was due to be torqued the following day) failed at the end blind of the 48 inch spool | "LOTO applied by Spiecapag on the valve was not effective, ch"
  [666246] Trolley Festoon came off from the Trolley Conductor Track --> no visible damage was found on the Trolley Festoon or any other items | "Inspections were carried out by the Workshop Foreman and no "

Top failed controls across all incidents:
  fire: 14
  injuries: 10
  injury: 5
  hard hat: 4
  gloves: 4
  IP fell 4m from a ladder: 4
  helmet: 3
  safety glasses: 3
  fire extinguisher: 3
  SOPEP equipment: 3
```

### IOGP-06: Working at height incidents with fall protection gaps
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 246
Distinct BODY_PART values: 76
Top 10:
  left hand: 15
  left foot: 10
  shoulder: 10
  left leg: 8
  arm: 4
  ankle: 4
  eye: 4
  wrist: 3
  Knee: 3
  lower leg: 3
```

### IOGP-07: Mechanical lifting incidents with rigging failures
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 2001
Distinct INJURY_TYPE values: 152
Top 10:
  injuries: 51
  laceration: 15
  injury: 15
  cut: 14
  personal injury: 12
  fracture: 12
  abrasion: 12
  contusion: 9
  personnel injury: 6
  pain: 6
```

### IOGP-08: Machinery/tools incidents with hand/finger injuries
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 200
Sample: ['INCIDENT::10299', 'INCIDENT::10348', 'INCIDENT::10636', 'INCIDENT::10759', 'INCIDENT::10789']
```

### MH-01: Equipment in containment->injury at offshore
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Containment RCC values matched: ['Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution)', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)']
Containment incidents: 1202
-> Offshore containment: 50
-> With injuries: 1
Equipment in those incidents:
  150T crane: 1
  main hoist winch drum: 1
```

### MH-02: Injuries from equipment failures during maintenance
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 29
EQUIPMENT->INJURY_TYPE pairs (top 10):
  whip check -> personal injury: 2
  needle gun -> finger contusion: 1
  needle gun -> nails: 1
  paint scraper -> finger contusion: 1
  paint scraper -> nails: 1
  pedestal grinder -> finger contusion: 1
  pedestal grinder -> nails: 1
  scraper -> finger contusion: 1
  scraper -> nails: 1
  grinding stone -> finger contusion: 1
```

### MH-03: Clients with vessel + back injury
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 47
Distinct ORGANIZATION values: 93
Top 10:
  OCM: 9
  TECHNIPFMC: 8
  HSE: 5
  HSEA: 5
  ISOS: 4
  IP: 4
  TECHNIP MARINE OPERATION SERVICES: 4
  WOODSIDE ENERGY LTD.: 4
  PETROBRAS: 3
  ENQUEST BRITAIN LTD.: 3
```

### MH-04: Top injury types per top-5 equipment
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Top 5 equipment (by incident count):

  forklift (771 incidents):
    injuries: 20
    injury: 7
    pain: 5
    abrasion: 5
    minor damage: 4

  crane (622 incidents):
    injuries: 18
    fracture: 5
    abrasion: 4
    personal injury: 4
    contusion: 3

  ROV (290 incidents):
    personal injury: 3
    ferimentos pessoais: 2
    injury: 1
    incident categorisation: 1
    FA case: 1

  pallet (186 incidents):
    injuries: 5
    laceration: 3
    injury: 3
    cut: 2
    tripped and fell backwards: 1

  PPE (145 incidents):
    cut: 5
    wounds: 3
    bruise: 3
    fracture: 3
    contusion: 2
```

### MH-05: Hand + pipe + Asia Pacific
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 6
Sample: ['INCIDENT::10789', 'INCIDENT::522669', 'INCIDENT::526879', 'INCIDENT::547023', 'INCIDENT::571988']
```

### MH-06: Severity: trucks vs cranes
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Severity distribution comparison:

  truck (428 incidents):
    Severity 1: 54
    Severity 2: 57
    Severity 3: 17
    Severity 4: 4
    Mean severity: 1.78

  crane (1444 incidents):
    Severity 1: 131
    Severity 2: 168
    Severity 3: 89
    Severity 4: 24
    Severity 5: 3
    Mean severity: 2.04
```

### MH-07: Scaffold near-misses by location
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 121
Distinct LOCATION values: 33
Top 10:
  Sabetta: 12
  Dubai: 9
  Aberdeen: 9
  Baku: 5
  Amalapuram: 4
  Qidong: 4
  Panipat: 3
  Abu Dhabi: 3
  Litvinov: 2
  Stavanger: 2
```

### MH-08: Hydraulic valve -> injury outcome
**Type:** Multi-hop | **Coverage:** ⚠️ | **Diagnosis:** DATA_SPARSE | **Time:** 0.2s

```
Matching incidents: 1
Distinct INJURY_TYPE values: 0
Top 10:
```

### SC-01: Spot-check: forklift mirror caught manifold (#623703)
**Type:** Single-hop | **Coverage:** ⚠️ | **Diagnosis:** EXTRACTION_GAP | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::623703: ['forklift']
Ground truth: ['forklift', 'manifold', 'mirror']
Missing: ['manifold', 'mirror']
Extra (unexpected): none
```

### SC-02: Spot-check: electrical substation feeder fire (#570187)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::570187: ['Connector link', 'feeder box', 'feeder breaker']
Ground truth: ['connector link', 'feeder box', 'feeder breaker']
Missing: none
Extra (unexpected): none
```

### SC-03: Spot-check: forklift hit PGB in yard (#602346)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::602346: ['PGB', 'forklift']
Ground truth: ['forklift', 'pgb']
Missing: none
Extra (unexpected): none
```

### SC-04: Spot-check: press + back pain (#14338)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::14338: ['press']
Ground truth: ['press']
Missing: none
Extra (unexpected): none
```

### SC-04b: Spot-check: press + back pain body part (#14338)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
BODY_PART found for INCIDENT::14338: ['lower back']
Ground truth: ['lower back']
Missing: none
Extra (unexpected): none
```

### SC-05: Spot-check: ROV marker buoys dropped (#500389)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** EXTRACTION_GAP | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::500389: ['chain', 'football float', 'marker buoys', 'odom weight']
Ground truth: ['chain', 'football float', 'marker buoys', 'odom weight', 'tms']
Missing: ['tms']
Extra (unexpected): none
```

### SC-06: Spot-check: fall + head cuts on barrier (#8712)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::8712: ['CEU 25 barrier']
Ground truth: ['ceu 25 barrier']
Missing: none
Extra (unexpected): none
```

### SC-06b: Spot-check: fall head cuts body parts (#8712)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
BODY_PART found for INCIDENT::8712: ['face', 'forehead', 'head']
Ground truth: ['face', 'forehead', 'head']
Missing: none
Extra (unexpected): none
```

### SC-07: Spot-check: wire sling + crane lip cut (#511771)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::511771: ['crane hook', 'wire rope sling']
Ground truth: ['crane hook', 'wire rope sling']
Missing: none
Extra (unexpected): none
```

### SC-07b: Spot-check: wire sling lip cut body part (#511771)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
BODY_PART found for INCIDENT::511771: ['lower lip']
Ground truth: ['lower lip']
Missing: none
Extra (unexpected): none
```

### SC-08: Spot-check: forklift + truck collision (#324)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::324: ['20T Forklift']
Ground truth: ['20t forklift']
Missing: none
Extra (unexpected): none
```

### SC-09: Spot-check: crane exit + head cut (#18312)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::18312: ['crane', 'plastic sun visor']
Ground truth: ['crane', 'plastic sun visor']
Missing: none
Extra (unexpected): none
```

### SC-09b: Spot-check: crane exit head cut body part (#18312)
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
BODY_PART found for INCIDENT::18312: ['head']
Ground truth: ['head']
Missing: none
Extra (unexpected): none
```

### SH-01: Forklift incidents in 2022
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.3s

```
Matching incidents: 71
Sample: ['INCIDENT::10170', 'INCIDENT::10252', 'INCIDENT::10333', 'INCIDENT::1061', 'INCIDENT::1069']
```

### SH-02: Equipment for incident #29857
**Type:** Single-hop | **Coverage:** ⚠️ | **Diagnosis:** EXTRACTION_GAP | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::29857: ['ROV', 'lanyard', 'pry bar']
Ground truth: ['lanyard', 'pry bar', 'rov', 'tms']
Missing: ['tms']
Extra (unexpected): none
```

### SH-03: Body parts in crane incidents
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 1444
Distinct BODY_PART values: 192
Top 10:
  finger: 35
  left hand: 31
  left foot: 20
  left leg: 15
  shoulder: 10
  head: 10
  thumb: 9
  arm: 9
  eye: 8
  forearm: 7
```

### SH-04: Locations for valve incidents
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 387
Distinct LOCATION values: 36
Top 10:
  USA: 172
  UK: 61
  Norway: 19
  Canada: 16
  France: 13
  Argentina: 11
  Brazil: 11
  China: 10
  India: 9
  Russia: 7
```

### SH-05: Injuries at offshore installations
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 1120
Distinct INJURY_TYPE values: 124
Top 10:
  cut: 16
  laceration: 13
  personal injury: 12
  abrasion: 9
  pain: 8
  wounds: 6
  swelling: 5
  fracture: 4
  bruising: 4
  injury: 4
```

### SH-06: Incidents reported by Shell Offshore
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 60
Sample: ['INCIDENT::100', 'INCIDENT::1039', 'INCIDENT::11906', 'INCIDENT::12463', 'INCIDENT::12507']
```

## 3. Ablation Prediction Table

| Query Type | Count | L1 Baseline | After ER (predicted) | After L2 (predicted) |
|-----------|:-----:|:-----------:|:-------------------:|:-------------------:|
| Single-hop (20) | 20 | 18/20 pass | 19/20 pass | 19/20 pass |
| Aggregation (8) | 8 | 8/8 pass | 8/8 pass | 8/8 pass |
| Multi-hop (12) | 12 | 11/12 pass | 12/12 pass | 12/12 pass |
| Global (4) | 4 | 4/4 pass | 4/4 pass | 4/4 pass |
| Conjunctive (8) | 8 | 8/8 pass | 8/8 pass | 8/8 pass |

## 4. Key Findings

### What works well at L1

- **AG-01**: Root causes of dropped object incidents
- **AG-02**: Countries with most high-severity incidents
- **AG-03**: Most common equipment by incident count
- **AG-04**: Incident type x business unit crosstab
- **AG-05**: Monthly trend of fall/slip incidents
- **AG-06**: Severity distribution by impact type
- **CJ-01**: Corrosion -> equipment failure -> fire (L2)
- **CJ-02**: Crane + back + offshore + high severity
- **CJ-03**: Maintenance fail + pipe + environmental + Middle East
- **CJ-04**: Equipment: accident + near-miss same location/year
- **CJ-05**: Procedural -> dropped -> head/hand injury (L2)
- **CJ-06**: Falls/slips + vehicle + construction
- **CJ-07**: Primary effects of corrosion (L2)
- **GL-01**: Safety risk clusters (Louvain)
- **GL-02**: Equipment recurring across regions
- **GL-03**: Temporal trend of incident types
- **GL-04**: Hub centrality analysis
- **IOGP-01**: Moving vehicle/mobile equipment incidents
- **IOGP-02**: Dropped object incidents by severity
- **IOGP-03**: Stored energy / snap-back incidents
- **IOGP-04**: Pressurized system incidents with containment loss
- **IOGP-05**: Electrical incidents with LOTO failures (L2)
- **IOGP-06**: Working at height incidents with fall protection gaps
- **IOGP-07**: Mechanical lifting incidents with rigging failures
- **IOGP-08**: Machinery/tools incidents with hand/finger injuries
- **MH-01**: Equipment in containment->injury at offshore
- **MH-02**: Injuries from equipment failures during maintenance
- **MH-03**: Clients with vessel + back injury
- **MH-04**: Top injury types per top-5 equipment
- **MH-05**: Hand + pipe + Asia Pacific
- **MH-06**: Severity: trucks vs cranes
- **MH-07**: Scaffold near-misses by location
- **SC-02**: Spot-check: electrical substation feeder fire (#570187)
- **SC-03**: Spot-check: forklift hit PGB in yard (#602346)
- **SC-04**: Spot-check: press + back pain (#14338)
- **SC-04b**: Spot-check: press + back pain body part (#14338)
- **SC-05**: Spot-check: ROV marker buoys dropped (#500389)
- **SC-06**: Spot-check: fall + head cuts on barrier (#8712)
- **SC-06b**: Spot-check: fall head cuts body parts (#8712)
- **SC-07**: Spot-check: wire sling + crane lip cut (#511771)
- **SC-07b**: Spot-check: wire sling lip cut body part (#511771)
- **SC-08**: Spot-check: forklift + truck collision (#324)
- **SC-09**: Spot-check: crane exit + head cut (#18312)
- **SC-09b**: Spot-check: crane exit head cut body part (#18312)
- **SH-01**: Forklift incidents in 2022
- **SH-03**: Body parts in crane incidents
- **SH-04**: Locations for valve incidents
- **SH-05**: Injuries at offshore installations
- **SH-06**: Incidents reported by Shell Offshore

### ER merges that would improve results most

- **AG-03** (Most common equipment by incident count): surface form fragmentation reduces accuracy
- **GL-02** (Equipment recurring across regions): surface form fragmentation reduces accuracy
- **IOGP-01** (Moving vehicle/mobile equipment incidents): surface form fragmentation reduces accuracy
- **IOGP-04** (Pressurized system incidents with containment loss): surface form fragmentation reduces accuracy
- **IOGP-06** (Working at height incidents with fall protection gaps): surface form fragmentation reduces accuracy
- **IOGP-07** (Mechanical lifting incidents with rigging failures): surface form fragmentation reduces accuracy
- **IOGP-08** (Machinery/tools incidents with hand/finger injuries): surface form fragmentation reduces accuracy
- **MH-03** (Clients with vessel + back injury): surface form fragmentation reduces accuracy
- **MH-04** (Top injury types per top-5 equipment): surface form fragmentation reduces accuracy
- **MH-06** (Severity: trucks vs cranes): surface form fragmentation reduces accuracy
- **MH-07** (Scaffold near-misses by location): surface form fragmentation reduces accuracy
- **SH-01** (Forklift incidents in 2022): surface form fragmentation reduces accuracy
- **SH-03** (Body parts in crane incidents): surface form fragmentation reduces accuracy
- **SH-04** (Locations for valve incidents): surface form fragmentation reduces accuracy
- **SH-06** (Incidents reported by Shell Offshore): surface form fragmentation reduces accuracy

### Queries blocked until Layer 2


### Data sparsity issues

- **AG-04** (Incident type x business unit crosstab): metadata coverage too low for reliable results
- **MH-08** (Hydraulic valve -> injury outcome): metadata coverage too low for reliable results

### Extraction gaps (actionable — would improve with better L1)

- **SC-01** (Spot-check: forklift mirror caught manifold (#623703)): 1 items: ['forklift']
- **SC-05** (Spot-check: ROV marker buoys dropped (#500389)): 4 items: ['chain', 'football float', 'marker buoys', 'odom weight']
- **SH-02** (Equipment for incident #29857): 3 items: ['ROV', 'lanyard', 'pry bar']

### Confirmed sparse (correct result — data does not contain these intersections)

- **CJ-02** (Crane + back + offshore + high severity): conjunction too specific for dataset — 0 results confirmed
- **CJ-03** (Maintenance fail + pipe + environmental + Middle East): conjunction too specific for dataset — 0 results confirmed

## 5. Regression Diff (vs previous run)

No regressions detected — all results stable.

---
*Generated by pipeline_v2/benchmark/run_benchmark.py*