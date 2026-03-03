# L1 Benchmark Query Results

**Generated:** 2026-03-03
**Graph:** 99,168 nodes, 237,095 edges
**Records:** 19,820 metadata rows, 19,844 incident nodes
**Layer:** L1 only (pre-ER, pre-Layer 2 causal enrichment)

## 1. Summary Table

| ID | Query | Type | Coverage | Result | Diagnosis | Validation |
|------|-------|------|:--------:|--------|-----------|:----------:|
| AG-01 | Root causes of dropped object incidents | Aggregation | ✅ | 1026 incidents, 43 root_cause_category values, top: Stored energy (dropped objects) | CLEAN | VALIDATED |
| AG-02 | Countries with most high-severity incidents | Aggregation | ✅ | 167 incidents, 22 location values, top: USA | CLEAN | VALIDATED |
| AG-03 | Most common equipment by incident count | Aggregation | ✅ | 19844 incidents, 13446 equipment values, top: forklift | ER_NEEDED | — |
| AG-04 | Incident type x business unit crosstab | Aggregation | ⚠️ | Crosstab: 4 business_unit values x 3 incident_type values | DATA_SPARSE | — |
| AG-05 | Monthly trend of fall/slip incidents | Aggregation | ✅ | 1695 incidents across 110 months | CLEAN | VALIDATED |
| AG-06 | Severity distribution by impact type | Aggregation | ✅ | Crosstab: 10 impact_type values x 6 severity_bin values | CLEAN | — |
| CJ-01 | Corrosion -> equipment failure -> fire (L2) | Conjunctive | ✅ | 37,925 causal edges; 792 for fire/explosion | CLEAN | — |
| CJ-02 | Crane + back + offshore + high severity | Conjunctive | ⚠️ | 0 incidents | DATA_SPARSE | — |
| CJ-03 | Maintenance fail + pipe + environmental + Middle East | Conjunctive | ⚠️ | 0 incidents | DATA_SPARSE | — |
| CJ-04 | Equipment: accident + near-miss same location/year | Conjunctive | ✅ | 539 dual-risk equipment/location/year combos | CLEAN | — |
| CJ-05 | Procedural -> dropped -> head/hand injury (L2) | Conjunctive | ✅ | 324 incidents; 8 procedural causal edges | CLEAN | — |
| CJ-06 | Falls/slips + vehicle + construction | Conjunctive | ✅ | 16 incidents | CLEAN | DRIFT |
| CJ-07 | Primary effects of corrosion (L2) | Conjunctive | ✅ | 98 corrosion causal edges across 69 incidents | CLEAN | — |
| GL-01 | Safety risk clusters (Louvain) | Global | ✅ | 9510 communities detected | CLEAN | — |
| GL-02 | Equipment recurring across regions | Global | ✅ | 144 equipment types span 5+ regions | ER_NEEDED | — |
| GL-03 | Temporal trend of incident types | Global | ✅ | Crosstab: 10 year values x 3 incident_type values | CLEAN | — |
| GL-04 | Hub centrality analysis | Global | ✅ | Hub analysis: degree + PageRank top 20 | CLEAN | — |
| MH-01 | Equipment in containment->injury at offshore | Multi-hop | ⚠️ | 1 incidents, 2 equipment types | CLEAN | — |
| MH-02 | Injuries from equipment failures during maintenance | Multi-hop | ✅ | 29 incidents, 19 pairs | CLEAN | VALIDATED |
| MH-03 | Clients with vessel + back injury | Multi-hop | ✅ | 47 incidents, 93 organization values, top: OCM | ER_NEEDED | — |
| MH-04 | Top injury types per top-5 equipment | Multi-hop | ✅ | Injury breakdown for top 5 equipment | ER_NEEDED | — |
| MH-05 | Hand + pipe + Asia Pacific | Multi-hop | ✅ | 6 incidents | CLEAN | — |
| MH-06 | Severity: trucks vs cranes | Multi-hop | ✅ | Truck vs crane severity comparison | ER_NEEDED | — |
| MH-07 | Scaffold near-misses by location | Multi-hop | ✅ | 121 incidents, 33 location values, top: Sabetta | ER_NEEDED | DRIFT |
| MH-08 | Hydraulic valve -> injury outcome | Multi-hop | ⚠️ | 3 incidents, 0 injury_type values | EXTRACTION_GAP | — |
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

**Overall:** 37 ✅ FULL / 7 ⚠️ PARTIAL / 0 ❌ FAIL out of 44 queries

**Diagnosis breakdown:**
- CLEAN: 27
- ER_NEEDED: 10
- EXTRACTION_GAP: 4
- DATA_SPARSE: 3

**Ground truth validation:**
- VALIDATED: 6
- CLOSE: 1
- DRIFT: 2
- —: 35

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
  Angola: 3
  Canada: 3
  Australia: 3
  Malaysia: 3
```

### AG-03: Most common equipment by incident count
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 19844
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
  machine: 93
  safety glasses: 93
  pump: 82
  truck: 81
  winch: 81
```

### AG-04: Incident type x business unit crosstab
**Type:** Aggregation | **Coverage:** ⚠️ | **Diagnosis:** DATA_SPARSE | **Time:** 0.1s

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
L2 causal edges in graph: 37,925
  CAUSAL: 31,398
  PRECEDED_BY: 3,272
  FAILED_CONTROL: 3,255

Fire/explosion incidents: 322
  With causal edges: 237
  Total causal edges: 792
  Tautological (fire→fire) filtered: 134

Top root causes for fire/explosion (non-tautological):
  fire: 37
  fire coming from the pipe work on top of the acetylene quad: 9
  minor fire: 8
  flames near the connection of the torch end: 7
  smoldering: 5
  ignition: 4
  leak: 4
  smell of smoke and noticed soot was on the ground: 4
  one ditch breaker burned: 4
  self-combustion: 4

Corrosion + fire/explosion intersection: 0 records
  Causal edges in these: 0
```

### CJ-02: Crane + back + offshore + high severity
**Type:** Conjunctive | **Coverage:** ⚠️ | **Diagnosis:** DATA_SPARSE | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-03: Maintenance fail + pipe + environmental + Middle East
**Type:** Conjunctive | **Coverage:** ⚠️ | **Diagnosis:** DATA_SPARSE | **Time:** 0.1s

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
  With L2 causal edges: 224
  Total causal edges: 660

Procedural causal edges: 8
  Samples:
    [575162] crane drive was instructed to come up with the hook --CAUSAL--> finger came loose
    [629667] deviation from procedure --CAUSAL--> Riser Test piece fell through the VLS to the VLS Table
    [644074] raising the mastil tensing chains --CAUSAL--> misunderstood in communication
    [546828] finger was hit --CAUSAL--> HSE Supervisor brought him to the First Aid point for the control and treatment
    [546828] HSE Supervisor brought him to the First Aid point for the control and treatment --CAUSAL--> he returned back to work
    [556525] pinching IP’s left thumb --CAUSAL--> immediate notification to supervisor
    [556525] immediate notification to supervisor --CAUSAL--> sent to REGA clinic at the TSF area
    [534066] assistant supervisor removed the stone with his right hand --CAUSAL--> tailgate to fully close

Top causal factors for dropped → head/hand:
  Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 13
  left middle finger: 6
  Downhole Guide Clamp: 5
  hand: 4
  device escaped from the initial position: 4
  fall from the marchepied of the cabin: 4
  left hand: 4
  slipping forward: 4
  placa metálica: 4
  collar: 3
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
Corrosion-source CAUSAL edges: 98
Unique incidents with corrosion causes: 69

Effects by category:
  leak/release: 6 edges (e.g. ['leak', 'leaky position of the pipe is a repaired protective jacket', 'leak'])
  equipment failure: 5 edges (e.g. ['Collapsed fencing', 'one of the breaker Thruster no 1 has been damaged', 'one of the breaker Thruster no 1 has been damaged'])
  structural damage: 4 edges (e.g. ['superficial damage to the quayside', 'vertical structural column (250 mm)', 'damage to one of the hoses'])
  safety system impact: 3 edges (e.g. ['line shut down', 'Captain shut down the tunnel thrusters from the stbd console', 'Chevron employee was nearby and reported the incident to safety'])

  Other effects: 80 edges
    irritation of eyes and throats: 2
    fishing gear: 2
    hydraulic hose: 2
    Dropped object: 2
    abnormal stop of the electric engine of the bow-thruster of vante: 1
```

### GL-01: Safety risk clusters (Louvain)
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 8.7s

```
Total communities: 9510
Top 10 by size:

  Community 1 (size=9921):
    EQUIPMENT: 2768 (e.g. ['A-frame gangway', 'transformador de 440V', 'drum motor pilot'])
    INCIDENT: 2695 (e.g. ['ACCIDENT 22263 - Minor oil leak during ROV survey operation', 'INCIDENT 705681 - Minor Equipment Damage - 078836C004 TOR II WP 16 - Deep Energy - 15/01/2021 - Damaged transponder antenna guard', "NEAR MISS 561667 - Intruder boards vessel whilst at anchor and steals items of ship's equipment before making off."])
    LOCATION: 1848 (e.g. ['aft engine room', 'Aft Moonpool', 'Barge and Wet Store'])
    ORGANIZATION: 1532 (e.g. ['COM', '1NDU', 'The Island vanguard'])
    EVENT: 380 (e.g. ['oil sheen', 'rigging became tangled under the ear of the shackle', 'guindasteiro was immediately activated and dropped with the collaborator, without the fall occurring'])
    BODY_PART: 211 (e.g. ['back of the thigh', '2nd end', 'Upper Chest & Throat region'])
    CONDITION: 207 (e.g. ['small weep from the fitting at the rear of the plug', 'method used to move the grating and cover plate', 'soap only being sprayed'])
    INJURY_TYPE: 94 (e.g. ['non work related', '2% BSA + Blisters', 'potential shoulder injury'])
    ACTION: 91 (e.g. ['lowering the reel on the hydraulic lift cylinders', 'ROV (XLX127) tasked to conduct a search subsea for the tool', 'shore side support'])
    INJURY: 39 (e.g. ['discomfort to diver 1', 'pinch injury that split the skin', 'jumper insulation damaged by the jumper stand'])
    MATERIAL: 36 (e.g. ['piece of metal', 'baked goods', 'approx. 8lts of Shell Tullos 32 released to sea'])
    PERSON: 12 (e.g. ['sub contracted welding team from Ponticelli', 'Local Agent', 'technician confirming the direction of turns'])
    ROOT_CAUSE_CATEGORY: 8 (e.g. ['Difficult/Hindered operability of tools and equipment', 'Stored energy (dropped objects)', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)'])

  Community 2 (size=9384):
    INCIDENT: 3577 (e.g. ['INCIDENT 671254 - Near Miss Dropped Object - Shell Oil - Houston Gremp Campus S07 Low Bay - 21 February 2020 - MTRT Tool Dropped During Lifting Operations', 'ACCIDENT 28490 - 604391 - Accident-Stephenville-08/28/2018', 'NEAR MISS 27244 - Stephenville - Dropped Object - Window Pane Fell'])
    EQUIPMENT: 2055 (e.g. ['tank', 'X-Ray camera', 'pallet collar'])
    LOCATION: 1432 (e.g. ['maintenance shop', 'back entrance', 'wall'])
    ORGANIZATION: 934 (e.g. ['Shop technicians', 'Liberty Oilfield Services', 'OWIRS team'])
    EVENT: 506 (e.g. ['hub has partially dislodged from its guide rail', 'deer suddenly jumped from the ditch into traffic', 'pallet fell on the right side'])
    BODY_PART: 300 (e.g. ['right tail end', 'boot', 'top of manifold hydraulic leg'])
    CONDITION: 241 (e.g. ['pipe had lost its drive push', 'cut through the skin', 'contact with the top of the fork pockets in the skid'])
    INJURY_TYPE: 116 (e.g. ['severe wood rotting', 'heat exhaustion', 'repetitive motion'])
    ACTION: 98 (e.g. ['crane operator stopped the crane', 'gripping a packing nut wrench', 'adjusting the crate'])
    INJURY: 61 (e.g. ['damage to the lower frame on the unit', 'discomfort and blurry eyesight', 'narrowly missing employees head'])
    MATERIAL: 34 (e.g. ['wire attached to the ground clamp', 'chamfer of the joint', 'gas coming from the vent line from the 9.625" and 5.5" annulus'])
    PERSON: 18 (e.g. ['truck driver who had a trailer attached to his truck', 'Adrian', 'Technician 2'])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['SIMOPS (coordination with 3rd Parties)', 'Motor Vehicle Road Accident', 'Tool suitability'])

  Community 3 (size=5499):
    INCIDENT: 1724 (e.g. ['ACCIDENT 517243 - RWC - Flexibras Vitória - Finger crushed during maintenance_x000D_', 'ACCIDENT 13255 - RWC - Dutra industrial plants - Matriz - Left hand cutting during machining activity / Corte de m?o esquerda durante atividade de usinagem', 'INCIDENT 695605 - Batida de tubo contra pilar de concreto (Mour?o)'])
    EQUIPMENT: 1206 (e.g. ['UTM OSS check valve', 'munck vehicle', 'equipe de bordo'])
    LOCATION: 957 (e.g. ['Marechal Avenue Mascarenhas de Moraes', 'Módulo 13', 'Avenida Lacerda Agostinho'])
    ORGANIZATION: 671 (e.g. ['colaboradores', 'iOGP', 'PAVI-S'])
    EVENT: 281 (e.g. ['interrupted the test', 'hydraulic fluid leakage', 'collision with the cables of the 80TON rolling bridge'])
    BODY_PART: 231 (e.g. ['injection eye', 'dedo médio', 'dobradi'])
    CONDITION: 118 (e.g. ['frozen bread left in too long', 'burs-ted fitting on whip spooling device', 'the 85Kw unit doors were open'])
    INJURY_TYPE: 108 (e.g. ['surface trauma', 'small rubber cut', 'scoria??o'])
    ACTION: 73 (e.g. ['collaborator used the capacet', 'rejecting hot water in his bra?o', 'qualified electrician was called out to re-terminate the cable'])
    INJURY: 73 (e.g. ['deep cut in the ring finger of his right hand', 'burning of 1st degree', 'minor cut on his forehead'])
    MATERIAL: 30 (e.g. ['metallic part', '10 liters reached the interlocking floor', '10 liters of the product had been given in the soil'])
    PERSON: 23 (e.g. ['people on the site', 'two third parties coming from home to work', "collaborator's back"])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Dangerous surfaces (sharp/ sharp edged/ high roughness grade)', 'Management of Change', '3. 3rd Party NCR (received or managed by TechnipFMC or Partners)'])

  Community 4 (size=4068):
    INCIDENT: 1482 (e.g. ['INCIDENT 666289 - NM-W3M6-09/01/2020-Mauvaise protection de la visière de protection pour casque MSA', 'INCIDENT 710112 - FAC Non T.EN owned 17/03/21 ANTARES - JONAGE Minor cut, knee', 'INCIDENT 695280 - NM - 20/10/2020 - Magasin MP - Chute spools sur la chaussée'])
    EQUIPMENT: 763 (e.g. ['white monitor', 'articulated arm', 'cowbot chassis'])
    LOCATION: 529 (e.g. ['marchepied', 'manufacturing batiment', 'Substation accès'])
    ORGANIZATION: 408 (e.g. ['BBC Alberta', 'The B team', 'Falck Global Assistance'])
    EVENT: 267 (e.g. ['water infiltration', 'operator loses its support at the risk of turning the knee', 'motor vehicle incident'])
    BODY_PART: 180 (e.g. ['right edge', 'throat level', 'goulots'])
    CONDITION: 133 (e.g. ['anti-drawing plate (but very oil)', 'Ergonomics - Computer workplaces / Screens', 'holiday watch and rainy episodes announced'])
    INJURY_TYPE: 118 (e.g. ['hand shock', 'impacted on fall', 'boulonnerie discharge'])
    ACTION: 87 (e.g. ['no action taken', 'MET1166 procedure (Chapter 6.1.3 and 6.1.4)', 'maintenance and repair in the engine room'])
    INJURY: 66 (e.g. ['Injury (left knee)', 'allergic reaction', 'persistent pain in shoulder/neck area'])
    MATERIAL: 15 (e.g. ['found a rock', 'shrimp', 'RX5227'])
    ROOT_CAUSE_CATEGORY: 10 (e.g. ['Environment- Unsorted waste, no traceability of the waste;?', 'Environment- Over-consumption of energy, natural resources (water, ...)', 'Climate (Heat/Cold/Humidity)'])
    PERSON: 10 (e.g. ['treated by the nurse', "operator's hands", 'communicated the leading deck'])

  Community 5 (size=3844):
    INCIDENT: 1153 (e.g. ['ACCIDENT 508465 - LTI - Yamal LNG Project - Sabetta - 10.09.2016 - Multiple open fractures of 2nd, 3rd, 4th and 5th fingers of left hand', 'ACCIDENT 508888 - MDA - 61402S - Zeebrugge/MISY - 8/12/16 - one car hit another from rear', 'ACCIDENT 611806 - RT - Yamal LNG Project - Sabetta - 16.10.2018 - cars collision'])
    LOCATION: 639 (e.g. ['SIMOPS area', 'piperack 000-SPP-615', 'EDG-700'])
    EQUIPMENT: 574 (e.g. ['in-line 480 volts 100 amps', 'crane_x000D_', 'Chilling'])
    ORGANIZATION: 521 (e.g. ['Republic of Khacassia', 'REGA JV company', 'KamAZ 43118'])
    EVENT: 228 (e.g. ['falling onto the equipment', 'jumping off KAMAZ truck bed (height below 1 m) on uneven surface of road slab', 'stumbling on one of the steps'])
    BODY_PART: 216 (e.g. ['right hand 1st finger', '3rd, 4th and 5th fingers', 'right side of his face'])
    INJURY_TYPE: 209 (e.g. ['dislocation', 'serious injuries', 'frostbite'])
    CONDITION: 103 (e.g. ['fencing', 'Condition', 'Radio communication problem'])
    INJURY: 91 (e.g. ['closed fracture of the right wrist', 'Contusion of III, IV right hand fingers, under-nail hematoma of III, IV right hand fingers', 'contused wound of right hand 1st finger'])
    ACTION: 74 (e.g. ['Primary surgical debridement, suturing, bandaging', 'holding the metal band with his left hand', 'Operator missed the walk'])
    PERSON: 22 (e.g. ['gas torch operator', 'one of the firewatchers', 'Individual'])
    MATERIAL: 9 (e.g. ['pipe (6 inch, 80.5kg, L shape)', 'Gloves worn at time of incident', 'polymeric material'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Fall to lower level / fall to water / loose materials (e.g. silos with granulate)', 'Traffic Management / Routes / Pedestrian path', 'Uncontrolled chemical or physical reaction'])

  Community 6 (size=3501):
    INCIDENT: 1050 (e.g. ['ACCIDENT 10312 - LTI - Ruche - OSB; Sprained ankle when working in stalkracks', 'NEAR MISS 20196 - O-ring ruptured during THRT Gallery Leakage Test', 'NEAR MISS 18159 - Pressure came out of the bleed line'])
    EQUIPMENT: 826 (e.g. ['Gate Valve stem', 'H-frame number 3', 'protective shield'])
    LOCATION: 504 (e.g. ['Deck 9', 'BOP deck', 'wire fence'])
    ORGANIZATION: 433 (e.g. ['TechnipFMC QHSE Management', 'CCB-SPLOG', 'fireguard'])
    EVENT: 236 (e.g. ['landed in the ALDS laydown area approximately 28 metres below', 'scratching with the body of the assembly the truck’s toolbox', 'burnt by the fire'])
    CONDITION: 147 (e.g. ['spool positioned at 1600mm off the ground', 'clamping force being applied', 'missing entire UMV assembly'])
    BODY_PART: 121 (e.g. ['body assy', 'albue', 'nakken'])
    ACTION: 58 (e.g. ['tried to take off the plastic protection', 'manipulation of the upper clamp', 'deck rigging team along with ACE winches techs proceeded to install scupper bungs and deployed spill kits to the area'])
    INJURY_TYPE: 52 (e.g. ['3-4 cut', 'No physical injuries', 'burnt area'])
    INJURY: 43 (e.g. ['one of the small bones in his foot is also broken', 'IP went over on his right ankle', '1 cm graze on the left side of the head'])
    MATERIAL: 18 (e.g. ['wood waste', 'hydraulic oil from the chamber and rig supply', 'leaking around 5 liters of hydraulic oil'])
    PERSON: 11 (e.g. ["TFMC well head operator and Halliburton's ground supervisor", 'sentry guard/ fire watch manning the tier 2 barriers', 'dropped by a LLC "TPS" (Velesstroy subcontractor) worker'])
    ROOT_CAUSE_CATEGORY: 2 (e.g. ['Stored energy (pressure, tension)', '1. Internal NCR (issued by TechnipFMC or Partners)'])

  Community 7 (size=3418):
    INCIDENT: 898 (e.g. ['INCIDENT 646137 - Near miss_073633C001_IGHDS Prime G site_Bongaigaon_13.07.19_Welding Cable burn', 'ACCIDENT 500441 - FAC 134 - Proj. 2450 - Mangalore - 05/07/2016 - Right hand forearm got minor burn injury', 'NEAR MISS 587951 - Near Miss_XXXX -  Project Specific_Dahej_20/05/2018_Duplex Nylone Sling Parted from Eye(Loop)'])
    EQUIPMENT: 666 (e.g. ['lifting vehicle', 'FRL unit', 'level two cut rate gloves'])
    LOCATION: 544 (e.g. ['methanol tank area', 'PRU area', 'Mumbai'])
    EVENT: 345 (e.g. ['grinder kicked back', 'hammer slipping', 'falling from 10 meters elevation'])
    ORGANIZATION: 314 (e.g. ['PHOENIX INFOCITY PRIVATE LIMITED', 'electrical dept', 'PAGM'])
    CONDITION: 182 (e.g. ['contact with the box’s edge', 'Beam was bent', 'damaged kerb stone'])
    INJURY: 138 (e.g. ["Employee's right finger", 'laceration to his index finger', 'wrist pain'])
    ACTION: 110 (e.g. ['lifting up a metal sheet (size 1x0,2m) from the floor', 'First aid administration (TT injection & dressing)', 'IP accidentally put his foot in front of the steam outlet'])
    BODY_PART: 107 (e.g. ['forehead_x000D_', 'anterior aspect', 'right lateral ankle'])
    INJURY_TYPE: 77 (e.g. ['pinching type injury', 'low level burn', 'minor burn'])
    MATERIAL: 17 (e.g. ['A4 cut rated gloves', 'steel Rack full of Drawing and other official paper', 'burnt plastic hoses'])
    PERSON: 14 (e.g. ['SCTR employee of Socar AZK', 'Engineer of M/s.BIL', 'the vehicle driver'])
    ROOT_CAUSE_CATEGORY: 6 (e.g. ['Unprotected/unguarded moving machine parts (struck by/caught by )', 'Use of personal protective equipment', 'Accumulation / Presence of explosive atmosphere'])

  Community 8 (size=2935):
    LOCATION: 673 (e.g. ['scaffold erections', 'asphalt road', 'Camp No. 2 (Floq)'])
    INCIDENT: 655 (e.g. ['ACCIDENT 573603 - NON-Technip Owned - BNJ-FAC 26 - 2529 TAP - Greece/Camp 5 - 23/02/2018 - Minor finger cut with carton box', 'ACCIDENT 586283 - LTI -TPIT Rome H.O. - May 9th 2018 - Employee stumbled on last step of the office stairs, twisting her right ankle', 'ACCIDENT 596570 - NON-Technip Owned - SCA-DA 19 - 2529 TAP Project - Greece/KP 130+600 - 09/07/2018 -  3 cables on a de-energized 20 KV OHPL broken'])
    ORGANIZATION: 570 (e.g. ['Engineering department', 'HS Department', 'Riprap'])
    EQUIPMENT: 502 (e.g. ['excavator', 'light clamp', 'wooden skids sets'])
    EVENT: 169 (e.g. ['collision with caterpillar 594', 'one ditch breaker burned', 'Tie-in Supervisor lost balance and fell from ladder'])
    CONDITION: 122 (e.g. ['electrical line was not energized', 'cabin pressure', 'Employees traverse through this area throughout the day'])
    ACTION: 59 (e.g. ['TFMC panel operator moved to the spot of the noise and checked the occurrence', 'pipefitter removing his leather safety glove', 'the involved personnel consciously proceeded to a WAH Golden Rule/Scaffold Safety rule violation'])
    INJURY: 57 (e.g. ['First degree Burn injury', 'lacerated wound of his chin', 'lacerating their thumb'])
    INJURY_TYPE: 46 (e.g. ['minor finger laceration', 'intrarticular fracture', 'first three fingers'])
    BODY_PART: 46 (e.g. ['broken ribs', 'L1 vertebra', 'back of the neck'])
    PERSON: 18 (e.g. ['rigger was standing in the line of fire', 'fitter Igumnov Sergey Viktorovich', 'worker in the line of fire'])
    MATERIAL: 14 (e.g. ['anti tetanus serum', 'subcontractor used the “old” material', 'dampened rag'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Illumination / sight / visibility', 'Inadequate Supervision', 'Unfamiliar personnel'])

  Community 9 (size=2639):
    INCIDENT: 747 (e.g. ['NEAR MISS 23612 - Gate Valve 2" slip down during welding job', 'INCIDENT 716599 - First Aid - APSB - QC Laboratory - 21/05/2021 -Chemical burn on skin at right arm', 'INCIDENT 730789 - Wall scratch and bumped guard'])
    EQUIPMENT: 529 (e.g. ['backhoe bucket', 'portable tentage', '4 legged rigging chain'])
    LOCATION: 502 (e.g. ['LOT 43', 'North side transformer bay', 'canteen'])
    ORGANIZATION: 329 (e.g. ['first party', 'tooling team', 'ASSOCIATED CARRIAGE AND WAREHOUSING (M) SDN BHD'])
    EVENT: 202 (e.g. ['STOP THE JOB', 'Both pumps were shut down and the line to the eastern caisson was isolated with a cap', 'caught fire'])
    CONDITION: 114 (e.g. ['2 units of kitchen stove was found leaking', 'clog inside the pipe', 'fuse was burning'])
    BODY_PART: 75 (e.g. ['her finger', 'scaphoid bone', 'phalanges bone'])
    ACTION: 49 (e.g. ["operator's quick reaction", 'cleaning up the spillage', 'walk through ESS-305'])
    INJURY_TYPE: 37 (e.g. ['No potential for injuries', 'nail puncture wound', 'MRI scan'])
    INJURY: 27 (e.g. ['severe risk', 'shock to his hand', 'bobbin #290 was damage'])
    MATERIAL: 14 (e.g. ['remainder of resin', 'damage to ROV manoeuvring panel', 'excavated soil placed at the edge of the trench'])
    PERSON: 11 (e.g. ['three number personnel', 'Contractor PCC Engineer', 'two (2) of the three (3) persons'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Electrical', 'Electrical current / electrocution / ESD / electromagnetic Fields', 'Equipment condition'])

  Community 10 (size=2185):
    INCIDENT: 661 (e.g. ['ACCIDENT 584672 - ENV - TUL - 27.04.18 - Mixed Waste consigned from site', "INCIDENT 672855 - Security gate arm made contact with 18-wheeler's pipe stake", 'ACCIDENT 512636 - FAC - TU Ltd - 15.10.16 - Contractor received minor burn to hand from drill chuck whilst changing out drill bit'])
    EQUIPMENT: 577 (e.g. ['Helix reels', 'Motive tensioner', 'crane lifts'])
    LOCATION: 293 (e.g. ['105 print area', 'TPU compressor area', 'route'])
    ORGANIZATION: 243 (e.g. ['AIS contractors', 'SOS', 'Assembly supervisor'])
    EVENT: 149 (e.g. ['sling became detached from the umbilical', 'breaking the sacrificial arm', 'cable-reeler free-wheeled in uncontrolled manner'])
    CONDITION: 91 (e.g. ['incorrectly installed O-rings', 'rotation of the 90-degree fitting', 'displacement of the brickwork'])
    INJURY_TYPE: 45 (e.g. ['jarring', 'top of his finger', 'strained abdominal muscle'])
    ACTION: 43 (e.g. ['adjusting the guide rollers', 'manual handling training', 'fork positions were checked prior to the unloading'])
    BODY_PART: 37 (e.g. ['guard arm', 'front teeth', 'one of his fingers'])
    INJURY: 28 (e.g. ['minor electric shocks', 'Injury: waist height', 'cut to the finger'])
    MATERIAL: 11 (e.g. ['prescription-strength medicine', '200 litres of HW 443 which was stored in an IBC', 'release of AWS 32 hydraulic oil'])
    PERSON: 6 (e.g. ['contractor from Multitask', 'Shepherd offshore personnel', 'Lead technician'])
    ROOT_CAUSE_CATEGORY: 1 (e.g. ['Radiation (ionising / non ionising)'])
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
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 7.8s

```
Top 20 non-incident nodes by degree:
  LOCATION::Europe -- degree 7433
  ORGANIZATION::TECHNIPFMC -- degree 4689
  LOCATION::North America -- degree 4681
  LOCATION::USA -- degree 4322
  LOCATION::UK -- degree 3746
  LOCATION::Asia Pacific -- degree 3106
  LOCATION::Aberdeen -- degree 2522
  LOCATION::South America -- degree 2144
  LOCATION::Brazil -- degree 1727
  ROOT_CAUSE_CATEGORY::Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) -- degree 1493
  LOCATION::France -- degree 1447
  LOCATION::Houston -- degree 1354
  ROOT_CAUSE_CATEGORY::Hazard Identification & Risk Assessment -- degree 1306
  ORGANIZATION::JSC YAMAL LNG -- degree 1302
  ROOT_CAUSE_CATEGORY::Equipment condition -- degree 1265
  ROOT_CAUSE_CATEGORY::Falls, slips and trips on same level (without potential to fall to lower level) -- degree 1182
  ROOT_CAUSE_CATEGORY::Stored energy (dropped objects) -- degree 1180
  LOCATION::Le Trait -- degree 1113
  ROOT_CAUSE_CATEGORY::Hazardous liquids (exposure to / spill / loss of containment /pollution) -- degree 1110
  LOCATION::Norway -- degree 1064

Top 20 non-incident nodes by PageRank:
  LOCATION::Europe -- PR 0.003210
  LOCATION::North America -- PR 0.002204
  LOCATION::USA -- PR 0.001605
  LOCATION::Asia Pacific -- PR 0.001317
  LOCATION::UK -- PR 0.001196
  LOCATION::South America -- PR 0.001009
  ORGANIZATION::TECHNIPFMC -- PR 0.000662
  LOCATION::Brazil -- PR 0.000650
  LOCATION::France -- PR 0.000591
  EVENT::correctly returned to their original reels -- PR 0.000567
  LOCATION::Aberdeen -- PR 0.000534
  LOCATION::Norway -- PR 0.000402
  LOCATION::Houston -- PR 0.000346
  LOCATION::India -- PR 0.000339
  LOCATION::Africa -- PR 0.000338
  LOCATION::Le Trait -- PR 0.000325
  LOCATION::Russia -- PR 0.000296
  LOCATION::Middle East -- PR 0.000272
  INJURY_TYPE::injury -- PR 0.000265
  LOCATION::India -- PR 0.000262
```

### MH-01: Equipment in containment->injury at offshore
**Type:** Multi-hop | **Coverage:** ⚠️ | **Diagnosis:** CLEAN | **Time:** 0.0s

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
  TECHNIP MARINE OPERATION SERVICES: 4
  ISOS: 4
  IP: 4
  WOODSIDE ENERGY LTD.: 4
  ENQUEST BRITAIN LTD.: 3
  PETROBRAS: 3
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
    personal injury: 4
    abrasion: 4
    contusion: 3

  ROV (290 incidents):
    personal injury: 3
    ferimentos pessoais: 2
    personnel injury: 1
    bruise: 1
    bites: 1

  pallet (186 incidents):
    injuries: 5
    laceration: 3
    injury: 3
    cut: 2
    sharp pain: 1

  PPE (145 incidents):
    cut: 5
    bruise: 3
    fracture: 3
    wounds: 3
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
  Qidong: 4
  Amalapuram: 4
  Panipat: 3
  Abu Dhabi: 3
  Stavanger: 2
  Anvers: 2
```

### MH-08: Hydraulic valve -> injury outcome
**Type:** Multi-hop | **Coverage:** ⚠️ | **Diagnosis:** EXTRACTION_GAP | **Time:** 0.0s

```
Matching incidents: 3
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
  head: 10
  shoulder: 10
  thumb: 9
  arm: 9
  eye: 8
  lower back: 7
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
  injury: 4
  bruising: 4
  fracture: 4
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
| Single-hop (19) | 19 | 17/19 pass | 18/19 pass | 18/19 pass |
| Aggregation (6) | 6 | 5/6 pass | 5/6 pass | 5/6 pass |
| Multi-hop (8) | 8 | 6/8 pass | 7/8 pass | 7/8 pass |
| Global (4) | 4 | 4/4 pass | 4/4 pass | 4/4 pass |
| Conjunctive (7) | 7 | 5/7 pass | 5/7 pass | 5/7 pass |

## 4. Key Findings

### What works well at L1

- **AG-01**: Root causes of dropped object incidents
- **AG-02**: Countries with most high-severity incidents
- **AG-03**: Most common equipment by incident count
- **AG-05**: Monthly trend of fall/slip incidents
- **AG-06**: Severity distribution by impact type
- **CJ-01**: Corrosion -> equipment failure -> fire (L2)
- **CJ-04**: Equipment: accident + near-miss same location/year
- **CJ-05**: Procedural -> dropped -> head/hand injury (L2)
- **CJ-06**: Falls/slips + vehicle + construction
- **CJ-07**: Primary effects of corrosion (L2)
- **GL-01**: Safety risk clusters (Louvain)
- **GL-02**: Equipment recurring across regions
- **GL-03**: Temporal trend of incident types
- **GL-04**: Hub centrality analysis
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
- **CJ-02** (Crane + back + offshore + high severity): metadata coverage too low for reliable results
- **CJ-03** (Maintenance fail + pipe + environmental + Middle East): metadata coverage too low for reliable results

## 5. Regression Diff (vs previous run)

- **CJ-07**: NEW
- **MH-03**: coverage ❌ → ✅

---
*Generated by pipeline_v2/benchmark/run_benchmark.py*