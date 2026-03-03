# L1 Benchmark Query Results

**Generated:** 2026-03-03
**Graph:** 99,166 nodes, 237,094 edges
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
| GL-01 | Safety risk clusters (Louvain) | Global | ✅ | 9518 communities detected | CLEAN | — |
| GL-02 | Equipment recurring across regions | Global | ✅ | 144 equipment types span 5+ regions | ER_NEEDED | — |
| GL-03 | Temporal trend of incident types | Global | ✅ | Crosstab: 10 year values x 3 incident_type values | CLEAN | — |
| GL-04 | Hub centrality analysis | Global | ✅ | Hub analysis: degree + PageRank top 20 | CLEAN | — |
| MH-01 | Equipment in containment->injury at offshore | Multi-hop | ⚠️ | 1 incidents, 2 equipment types | CLEAN | — |
| MH-02 | Injuries from equipment failures during maintenance | Multi-hop | ✅ | 29 incidents, 19 pairs | CLEAN | VALIDATED |
| MH-03 | Clients with vessel + back injury | Multi-hop | ❌ | 0 incidents, 0 organization values | ER_NEEDED | — |
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

**Overall:** 35 ✅ FULL / 7 ⚠️ PARTIAL / 1 ❌ FAIL out of 43 queries

**Diagnosis breakdown:**
- CLEAN: 26
- ER_NEEDED: 10
- EXTRACTION_GAP: 4
- DATA_SPARSE: 3

**Ground truth validation:**
- VALIDATED: 6
- CLOSE: 1
- DRIFT: 2
- —: 34

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
  Malaysia: 3
  Australia: 3
  Angola: 3
  Canada: 3
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
  reel: 98
  manlift: 98
  gloves: 96
  sling: 94
  safety glasses: 93
  machine: 93
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

### GL-01: Safety risk clusters (Louvain)
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 8.9s

```
Total communities: 9518
Top 10 by size:

  Community 1 (size=10011):
    EQUIPMENT: 2795 (e.g. ['TR H beam frame', 'sterile dressing', 'ice compression pack'])
    INCIDENT: 2717 (e.g. ['INCIDENT 724263 - Near Miss - 075260C004 Edvard Greig - 30 July 2021 - ROV Contact with West Bollsta (Rig) anchor Line', 'INCIDENT 650951 - Near Miss - Bokor Project - Deep Orient - Platform step ladder blown overboard during squall', 'INCIDENT 680732 - Near Miss - Conocophillips - TOR ll iEPCI Project 078836C004 - North Sea Atlantic - 4th Junes 2020 - Mini electric shock during welding on NSA deck'])
    LOCATION: 1853 (e.g. ['port quayside', '12 O’ Clock point', 'AFT end'])
    ORGANIZATION: 1536 (e.g. ['Topside medical support', 'Repsol oil', 'TFMC onboard management'])
    EVENT: 385 (e.g. ['spill of around 1-2 litres of diesel', 'clashed with pallet material of other contractor', 'unplanned disconnection of buoyancy module subsea'])
    BODY_PART: 220 (e.g. ['pesco?o', 'static pad eye', 'patesca'])
    CONDITION: 214 (e.g. ['20grams and dropped a distance of 15metres', 'forecasted increase in weather', 'significant bulge in abdomen that was painful to the touch'])
    INJURY_TYPE: 96 (e.g. ['LTI injury', 'swollen hand', 'Attached'])
    ACTION: 95 (e.g. ['chain (15m long) slipped from the personnel hand', 'decision to recover the Dredger', 'IP grabbed the tool by the head where the blade is located and accidentally pushed down the trigger'])
    INJURY: 42 (e.g. ['approx. 8-liter spill of hydraulic oil (Mobil DTE 10 Excel 46)', 'scaffold damage', 'minor abrasion and some local bleeding on his nose'])
    MATERIAL: 38 (e.g. ['piece of metal', '1 x 5.4Te ROV eye hook with the associated 1 x 4.75Te shackle and 1 x 8m 1" rope', 'metal debris'])
    PERSON: 14 (e.g. ['tree cart operator', 'The Company responsible for setting-up the tent', 'Dive Supervisor'])
    ROOT_CAUSE_CATEGORY: 6 (e.g. ['Stored energy (dropped objects)', 'Hyperbaric work environment', 'Biological - Animals, Bacteria, Viruses and Funguses'])

  Community 2 (size=9842):
    INCIDENT: 3725 (e.g. ['ACCIDENT 615015 - Vehicle Break-In', 'ACCIDENT 508642 - PD - LCCP - 2016 - 08 -16 (Warehouse Shelf Damaged by Forklift)', 'NEAR MISS 621707 - Dropped 4"10K valve.'])
    EQUIPMENT: 2181 (e.g. ['rig hands', 'roll-off trash container', '329 track hoe'])
    LOCATION: 1520 (e.g. ['Stephenville Milco facility', 'Corpus Christi Facility', 'wellhead assy facility'])
    ORGANIZATION: 926 (e.g. ['PBCI', 'Bank of America', 'NGT1 Rig  TSP'])
    EVENT: 526 (e.g. ['fan unplugged', 'pressure was released towards the employee', 'bay door came to a stop on top of the test cell door'])
    BODY_PART: 323 (e.g. ['drivers side front grill guard', 'Part of my boot', 'eye_x000D_'])
    CONDITION: 237 (e.g. ['rotten wood was missed', 'bay door tension', 'VX gasket being lifted out of the sealing profile'])
    INJURY_TYPE: 132 (e.g. ['Dislocated shoulder', 'severe wood rotting', 'insect/bug bite'])
    ACTION: 120 (e.g. ['driver did not fix the skid', 'lifted and started to back-up', 'Hand digging requirement specified on the excavation work permit'])
    INJURY: 86 (e.g. ['fissure in two toes', "contamination of Dave's cheeks, right ear lobe and a small spot on his lower neck", 'small dent'])
    MATERIAL: 29 (e.g. ['spilling approximately 8-10 gallons of hydraulic fluid', 'debris (dust)', 'dropped object weighed around 3.5 pounds (1.5 kilograms)'])
    PERSON: 23 (e.g. ['person taking care of the bars supporting the stain', 'Driver from AL-Mahadar co.', 'YAMAL employee taking a photo'])
    ROOT_CAUSE_CATEGORY: 14 (e.g. ['Over-consumption of energy, natural resources (water, etc.)', 'Computer workplaces / Screens', 'Basic Organizational'])

  Community 3 (size=5164):
    INCIDENT: 1634 (e.g. ['NEAR MISS 14694 - Vazamento Contido de fluido hidráulico no Guindaste de Provis?o (BE) / Contained Leakage of hydraulic fluid at Provision Crane (STB)', 'NEAR MISS 113 - NM - Portocel - Queda de dormente na verticaliza??o da Suction Pile (23.01) - Mero1', 'ACCIDENT 623621 - Near Miss - Dropped the pipe in the incoming rack'])
    EQUIPMENT: 1125 (e.g. ['empty collector of fluorescent lamps', 'pal-finger crane', 'CHK 1'])
    LOCATION: 918 (e.g. ['WCM', 'test area channels', 'VLS HPU container'])
    ORGANIZATION: 644 (e.g. ['Building Maintenance team', 'Tecnogera', 'health team'])
    EVENT: 246 (e.g. ['tool fell involuntarily', 'fall of one of the cavaletes and part of the end of the sample of the flexible tube', 'enganchou no suporte da patola 3 do guindaste (empresa terceira)'])
    BODY_PART: 215 (e.g. ['antebra', 'metatarso', 'coluna'])
    CONDITION: 103 (e.g. ['contact with the living parts of the yement eye', 'small amount of oil waste at the end of the pist', 'electrical short'])
    INJURY_TYPE: 98 (e.g. ['roulette discharge', 'restricted work', 'pinching'])
    INJURY: 65 (e.g. ['foot', 'concus cutting in the distal falange of the finger (5° Quirodactile) from the right', 'slight scoria in the left foot'])
    ACTION: 61 (e.g. ['use of extintor PQS', 'cleaning of the area was done with a mop', 'all food from refrigerator and bain-marie was disposed of'])
    MATERIAL: 26 (e.g. ['combustible materials (paper and plastic) arranged inside the greenhouse', '10 liters of the product had been given in the soil', 'paint damage'])
    PERSON: 22 (e.g. ['collaborator of the employed Vivante', 'two third parties coming from home to work', 'Pedro Lima (Brigadista)'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Information perceptiveness (amount / mode) & Information reception (extend / range)', 'Electrical', 'Lifting ops error'])

  Community 4 (size=4104):
    INCIDENT: 1504 (e.g. ['INCIDENT 642236 - FAC - TOYOINK Oissel - TP normandy - 27/06/19 - slipping and falling', 'ACCIDENT 13418 - SB-A6-02/03/2023-Douleur au dos', "NEAR MISS 20307 - NM- FTF/Atelier PTE - 08/04/2024 - Détection d'H2S lors d'une dissection"])
    EQUIPMENT: 770 (e.g. ['devidoir palm', 'etafoam plate', 'sheath'])
    LOCATION: 542 (e.g. ['Eco Sapucaí', 'nursery', 'A-19'])
    ORGANIZATION: 414 (e.g. ['clean site agents', 'flexifrance_x000D_', 'teamate'])
    EVENT: 258 (e.g. ['unusual feeling in his back', 'lost the balance back', 'operator crashed on a wooden cage'])
    BODY_PART: 182 (e.g. ['wing', 'auriculaire droit', 'mouth'])
    CONDITION: 134 (e.g. ['exposure to the wind', 'unexpected pressure inside the bottle', 'absence of 2 barriers at the location of the incident'])
    INJURY_TYPE: 119 (e.g. ['mechanical crackings', 'tendinitis', 'muscle breakdown'])
    ACTION: 82 (e.g. ['no action taken', 'Op moves hard', 'cleaning the TNO machine by air breath'])
    INJURY: 64 (e.g. ['breaking the skin on the arm', 'injury possibly resulting in stitches', 'swelling of the right arm'])
    MATERIAL: 15 (e.g. ['RX5227', 'TSI 115 assembly grease', "radiator's water"])
    ROOT_CAUSE_CATEGORY: 10 (e.g. ['Tool condition', 'Vibrations (hand arm / whole body)', 'Repetitive/one sided physical demand'])
    PERSON: 10 (e.g. ["operator's hands", 'decoration workers on the 13F', 'driver of the micro-bus of the company Fiel Turismo'])

  Community 5 (size=3890):
    INCIDENT: 1153 (e.g. ['INCIDENT 737176 - FAC - ARCTIC LNG-2 - Gydan Site - 28 November 2021 - Foreign body in the right eye', 'ACCIDENT 558597 - RT - Yamal LNG Project - Sabetta - 10.10.2017 - pick-up truck damage', 'ACCIDENT 540876 - RWC - Yamal LNG Project - Sabetta - 05.06.2017 - Fracture of a toe'])
    LOCATION: 649 (e.g. ['north piperack area', '211-PAU-001', 'SGS-508 area'])
    EQUIPMENT: 587 (e.g. ['shelf/rack', 'T1200 690 power van', 'Master-Train 2'])
    ORGANIZATION: 521 (e.g. ['SPMT operators', 'LLC "Integral', 'SOGAZ tier 3 clinic'])
    EVENT: 241 (e.g. ['4 first aiders attending', 'grit from portable blasting equipment was sprayed to his right thumb', 'column fell down'])
    BODY_PART: 216 (e.g. ['injured limb', 'elbow joint', 'left knee ligaments'])
    INJURY_TYPE: 212 (e.g. ['spraining of ligaments', 'partial break', 'bruise on the back'])
    CONDITION: 105 (e.g. ['smoke as a result of an air curtain malfunction in the corridor of the warehouse', 'complacent on the positioning of his feet while climbing over the hand rail', 'duct tape holding the hoses together'])
    INJURY: 93 (e.g. ['right ankle causing discomfort', 'contusion of the left half of ribcage', 'left foot fracture'])
    ACTION: 75 (e.g. ['hand of the rigger slipped', 'wiping his safety glasses', '5 stitches'])
    PERSON: 23 (e.g. ['one of the firewatchers', 'electrician of REGA JV Company', 'foreman K.V. Antonov'])
    MATERIAL: 10 (e.g. ['Gloves worn at time of incident', 'dirt/oil', 'cigarette butts'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Falls, slips and trips on same level (without potential to fall to lower level)', 'Fall to lower level / fall to water / loose materials (e.g. silos with granulate)', 'Uncontrolled chemical or physical reaction'])

  Community 6 (size=3562):
    INCIDENT: 1190 (e.g. ['INCIDENT 731476 - Fainted on grass verge', 'INCIDENT 653355 - Kone crane', 'ACCIDENT 19694 - Index Finger Pinched Between Cap-nut and Wooden Pallet'])
    EQUIPMENT: 752 (e.g. ['tech screw', 'mud guard', 'machine metal plate partition'])
    LOCATION: 568 (e.g. ['Kit Cell', 'control area', 'maintenance and facilities sector'])
    ORGANIZATION: 391 (e.g. ['AWB', 'Const. Piping  Eng.', 'coaster'])
    EVENT: 254 (e.g. ['Employee inadvertently dropped the weld torch', 'contact with the Fender on the quayside', 'Maintenance were contacted'])
    CONDITION: 124 (e.g. ['latch fell is not operable', 'not normal at this stage of assembly', 'loosened excessively during adjustment'])
    BODY_PART: 106 (e.g. ['R/H middle finger', 'left shoulder_x000D_', 'unihead part'])
    ACTION: 53 (e.g. ['machine had to be checked by maintenance', 'access any potential drop in the meeting room', 'adjust the tool length'])
    INJURY: 50 (e.g. ['more significant injury', 'squeezed the fingers on his left hand', 'punctures his jeans and skin with the exposed weld wire tip'])
    INJURY_TYPE: 49 (e.g. ['no open wound', 'electrical fire', 'physical injury'])
    PERSON: 12 (e.g. ['Long sweep assembler', 'external driver', 'grinder operator in the chest'])
    MATERIAL: 11 (e.g. ['counterweight weighed about 841 kg', 'Two plastic rain cover', 'minor damage to the roller cage'])
    ROOT_CAUSE_CATEGORY: 2 (e.g. ['Unprotected/unguarded moving machine parts (struck by/caught by )', 'Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects)'])

  Community 7 (size=3477):
    INCIDENT: 1049 (e.g. ['NEAR MISS 588613 - Overide jack XT Building 14', 'ACCIDENT 589521 - LTI - Agotnes - 030509C001 - STATOIL - Back pain after lifting RCU (30kg) - 31/05/2018', 'ACCIDENT 585709 - Forklift struck gate'])
    EQUIPMENT: 829 (e.g. ['CO2 fire extinguishers', 'grating on the washing machine', 'washout tool'])
    LOCATION: 506 (e.g. ['stop block', 'seafront', 'Lysaker'])
    ORGANIZATION: 430 (e.g. ['Bring truck', 'Warehouse manager', 'Snorre EDP'])
    EVENT: 232 (e.g. ['hub was projected on the first aggregate tester', 'operat?r rygget pallel?fteren ut', 'Equipment and area inspected for damage/return to service'])
    CONDITION: 143 (e.g. ['low deck head height with the addition of steel brackets to support cable trays', 'pallets on the floor', 'surface defects in the casting'])
    BODY_PART: 110 (e.g. ['handen', 'thumb and forefinger', 'beina'])
    INJURY_TYPE: 53 (e.g. ['Small scratches and bruises', 'burn like wound', 'FA case'])
    ACTION: 49 (e.g. ['manipulation of the upper clamp', 'addressed regarding glove choice', 'LOTO policy violation'])
    INJURY: 44 (e.g. ['cut his left hand', 'damaged three teeth', 'minor damage to the plastic protective house'])
    MATERIAL: 18 (e.g. ['no material damage was caused', 'steel box section', 'rag with Fast Degreeser / CRC'])
    PERSON: 12 (e.g. ['Marine operations assistant', 'sentry guard/ fire watch manning the tier 2 barriers', 'crew member'])
    ROOT_CAUSE_CATEGORY: 2 (e.g. ['Stored energy (pressure, tension)', '1. Internal NCR (issued by TechnipFMC or Partners)'])

  Community 8 (size=3381):
    INCIDENT: 905 (e.g. ['ACCIDENT 541593 - FAC - Dutra Industrial Plants - Superficial Skin Cut (Catering)', "INCIDENT 721840 - FAT - BANC 2 EPCM -2021-06-27-the Metal Sheet injured IP's left wrist", 'NEAR MISS 506752 - Near Miss_4536C001 - Onshore Terminal for VA&S1 Development Project_Amalapuram_8/26/2016_rebar  struck the nearby Tree'])
    EQUIPMENT: 670 (e.g. ['structural frame', 'idler unit', '400-watt sodium vapor luminaire'])
    LOCATION: 531 (e.g. ['open storage yard', 'Pipe rack area', 'TS-01 Area'])
    EVENT: 324 (e.g. ['contact with underground HDPE pipe', 'IP landed on the ground with direct hit on left side of his head', 'air leakage'])
    ORGANIZATION: 322 (e.g. ['ICABS TRANSPORT PRIVATE LIMITED', 'Song Junwei', 'BPCL'])
    CONDITION: 170 (e.g. ['wrench is noticeably worn', 'no nitrile gloves were available in her size', 'normal cotton dotted hand gloves'])
    INJURY: 131 (e.g. ['left nail bed into his left thumb', 'left-hand thumb pinched between the bronze chisel and the armor layer', 'cut injury'])
    BODY_PART: 115 (e.g. ['Knee cap', 'concrete edge', 'nail cuticle'])
    ACTION: 100 (e.g. ['IP bent to retrieve his hard hat', 'Truck driver entering warehouse', 'removal of the tool used as an alavanca'])
    INJURY_TYPE: 78 (e.g. ['No injury incident', 'small bleeding cuts and sprain', 'mushroom heads'])
    MATERIAL: 16 (e.g. ['burnt plastic hoses', 'corroded spacer', 'metal wire'])
    PERSON: 14 (e.g. ['Pipe Handler Supv', 'EC700 Excavator driver', 'lorry driver'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Use of personal protective equipment', 'Access/Egress', 'Manual handling'])

  Community 9 (size=2966):
    LOCATION: 678 (e.g. ['KP 310', 'workshop area', 'KP 141'])
    INCIDENT: 659 (e.g. ['NEAR MISS 633596 - NON-Technip Owned - BNJ-NM 42 - 2529 TAP Project - Greece/KP 374- 20/04/2019 - Arm of the side boom fell down on the pipe', 'ACCIDENT 530060 - Non Technip owned - Recordable- PDVSA APS PAGMI site - 3rd party subcontractor - Guiria Venezuela - 03/10/2017 - foreign body left eye', 'ACCIDENT 510213 - NON-Technip Owned - SCA-RWDC (RTA) 01 - Patos/Albania - 24/09/2016 - A private vehicle collided with a Spiecapag minibus'])
    ORGANIZATION: 577 (e.g. ['IPMT', 'CTR’s PMT', 'Egnatia Road Maintenance personnel'])
    EQUIPMENT: 511 (e.g. ['2 flat webbing slings', 'ACS02 Filter Separators', 'belt'])
    EVENT: 166 (e.g. ['vessel moving positions', 'A piece of wooden scaffolding toeboard fell on the first level on Module 06', 'medically assessed and treated'])
    CONDITION: 123 (e.g. ['liquid left in the line', 'Permit Rigger / Welder signed onto', 'no barrier was installed to establish and exclusion zone'])
    ACTION: 60 (e.g. ['operator transited without a banks man on a tight lane', 'EO did not stop to readjust the mirror that was moved out of position earlier that day by tree branches', 'flushing of the eyes'])
    INJURY: 56 (e.g. ['minor cut wound on his left forehead', 'injury to the left wrist', 'injury to the right eyebrow area'])
    BODY_PART: 52 (e.g. ['front head', 'L1 vertebra', 'tree trunk'])
    INJURY_TYPE: 46 (e.g. ['normal body type', 'second fracture', 'serious near miss'])
    PERSON: 20 (e.g. ['worker in the line of fire', 'painter working above him', "stevedore's hands"])
    MATERIAL: 14 (e.g. ['sulfur powder', 'scrap wood from a pallet with protruding nails', 'steel elements'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Unfamiliar personnel', 'Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)', 'Inadequate Supervision'])

  Community 10 (size=2319):
    INCIDENT: 631 (e.g. ["NEAR MISS 504188 - Near miss - Samarang - A9 - 08/08/2016 - Compressor Motor Disengage From It's Position and fall", 'ACCIDENT 551559 - PD - APSB - A9 - 7.9.2017 - Griper position 1 at loader unit broken', 'NEAR MISS 516995 - Near Miss-Layang-WSP18-22/11/2016-Bandit Spool Slipped During Liifting'])
    EQUIPMENT: 480 (e.g. ['Load Sensing', 'JIDET cutting machine', 'broken monitor'])
    LOCATION: 436 (e.g. ['lot 6900 802 1A', 'Level 9', 'reel storage B'])
    ORGANIZATION: 300 (e.g. ['Regency General Hospital', 'casting crew', 'BOMBA'])
    EVENT: 193 (e.g. ['hook block fell on the ground', 'tripped and lost balance', 'spray oil leakage from the side of the guindaste'])
    CONDITION: 99 (e.g. ['flooded with water', 'bad weather(high wave and strong wind)', 'loose from bobbin'])
    BODY_PART: 55 (e.g. ['front offside', 'Distal Third Left Tibia & Fibula Fracture', 'front right side corner'])
    ACTION: 44 (e.g. ['spillage area was barricaded and contained using adsorbent pad and spillage boom', 'disengaged the fifth wheel pin', 'ice packs applied'])
    INJURY_TYPE: 34 (e.g. ['scalds', 'glancing blow', 'soft tissue swelling'])
    INJURY: 24 (e.g. ['left hip', 'small dent on the backside of the truck', 'Injury: No injury'])
    MATERIAL: 14 (e.g. ['damage to ROV manoeuvring panel', 'excavated soil placed at the edge of the trench', 'broken glass'])
    PERSON: 8 (e.g. ['operator on the south side', 'jumbo operator', 'QC inspector'])
    ROOT_CAUSE_CATEGORY: 1 (e.g. ['Equipment condition'])
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
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 7.3s

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
  LOCATION::USA -- PR 0.001606
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
  actuator box -> static electric shock: 1
  gusset plate -> static electric shock: 1
  air hose -> personal injury: 1
  fitting -> personal injury: 1
  hose -> personal injury: 1
  PLS deck tensioner control cabin -> personal injury: 1
  engine room water pump -> minor burn: 1
  induction heater -> minor burn: 1
  needle gun -> finger contusion: 1
```

### MH-03: Clients with vessel + back injury
**Type:** Multi-hop | **Coverage:** ❌ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 0
Distinct ORGANIZATION values: 0
Top 10:
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
    injury: 1
    incident categorisation: 1
    FA case: 1

  pallet (186 incidents):
    injuries: 5
    laceration: 3
    injury: 3
    cut: 2
    personal injuries: 1

  PPE (145 incidents):
    cut: 5
    fracture: 3
    bruise: 3
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
  Aberdeen: 9
  Dubai: 9
  Baku: 5
  Qidong: 4
  Amalapuram: 4
  Panipat: 3
  Abu Dhabi: 3
  Pengerang: 2
  Stavanger: 2
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
  shoulder: 10
  head: 10
  arm: 9
  thumb: 9
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
  injury: 4
  bruising: 4
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
| Multi-hop (8) | 8 | 5/8 pass | 7/8 pass | 7/8 pass |
| Global (4) | 4 | 4/4 pass | 4/4 pass | 4/4 pass |
| Conjunctive (6) | 6 | 4/6 pass | 4/6 pass | 4/6 pass |

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
- **GL-01**: Safety risk clusters (Louvain)
- **GL-02**: Equipment recurring across regions
- **GL-03**: Temporal trend of incident types
- **GL-04**: Hub centrality analysis
- **MH-02**: Injuries from equipment failures during maintenance
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

No regressions detected — all results stable.

---
*Generated by pipeline_v2/benchmark/run_benchmark.py*