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
| CJ-05 | Procedural -> dropped -> head/hand injury (L2) | Conjunctive | ❌ | 0 incidents | L2_REQUIRED | — |
| CJ-06 | Falls/slips + vehicle + construction | Conjunctive | ✅ | 16 incidents | CLEAN | DRIFT |
| GL-01 | Safety risk clusters (Louvain) | Global | ✅ | 9510 communities detected | CLEAN | — |
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
| MH-08 | Hydraulic valve -> injury outcome | Multi-hop | ⚠️ | 3 incidents, 0 injury_type values | ER_NEEDED | — |
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

**Overall:** 34 ✅ FULL / 7 ⚠️ PARTIAL / 2 ❌ FAIL out of 43 queries

**Diagnosis breakdown:**
- CLEAN: 25
- ER_NEEDED: 11
- EXTRACTION_GAP: 3
- DATA_SPARSE: 3
- L2_REQUIRED: 1

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
  France: 6
  India: 6
  Canada: 3
  Angola: 3
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

Top causal factors for fire/explosion:
  fire: 47
  fire coming from the pipe work on top of the acetylene quad: 12
  minor fire: 11
  flames near the connection of the torch end: 8
  smoke: 7
  sparks: 6
  burner: 5
  smoldering: 5
  smell of smoke and noticed soot was on the ground: 5
  fire principle: 4

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
**Type:** Conjunctive | **Coverage:** ❌ | **Diagnosis:** L2_REQUIRED | **Time:** 0.1s

```
Matching incidents: 0
```

### CJ-06: Falls/slips + vehicle + construction
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
Matching incidents: 16
Sample: ['INCIDENT::11732', 'INCIDENT::24216', 'INCIDENT::520161', 'INCIDENT::527205', 'INCIDENT::543663']
```

### GL-01: Safety risk clusters (Louvain)
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 9.2s

```
Total communities: 9510
Top 10 by size:

  Community 1 (size=9921):
    EQUIPMENT: 2768 (e.g. ['chave de boca', 'flushing hose reel', 'chain and pad assembly'])
    INCIDENT: 2695 (e.g. ['ACCIDENT 598779 - Minor Environmental Incident - Deep Energy - 23/07/18 - 071179C001 -Trestakk Project - Minor release of hydraulic oil to seawater', 'INCIDENT 691363 - Minor Environmental Incident - 075688C001 Fenja SURF & SPS EPCI -  Deep Energy – 15 Sept 20 - 0.5L of Dow Corning 200 Silicone Oil discharge whilst cutting EFL', 'INCIDENT 683385 - Minor Environmental - 031428C001 - IMR - North Sea Giant - 01/07/2020 - Release of Hydraulic oil (approx. 7 litres) from Supporter 3 Subsea'])
    LOCATION: 1848 (e.g. ['Neptune P1 field', 'Venus', 'SW Thrash Zone'])
    ORGANIZATION: 1532 (e.g. ['onboard contractors', 'Damen Verlome Yard', 'GSOC'])
    EVENT: 380 (e.g. ['dumbbells falling behind his head', 'Equipment swinging', 'dislodged by the movement of the LVDT'])
    BODY_PART: 211 (e.g. ['knee level', 'corpo giratório', 'foot/ ankle'])
    CONDITION: 207 (e.g. ['spray of fluid with no taste', 'not fit for purpose connectors', 'no employees were in the line of fire'])
    INJURY_TYPE: 94 (e.g. ['Laceration & Graze', 'Non Work Related LTI', 'non work related'])
    ACTION: 91 (e.g. ['ROV team then removed the Cat 3 tool from the connector and placed it on top of the manifold', 'acknowledge the broke-in case', 'Instruction / participation in the familiarisation and drills with crew members on each asset'])
    INJURY: 39 (e.g. ['minor distortion to the sheave cheek plates', 'pinch injury that split the skin', 'muscular strain to the neck'])
    MATERIAL: 36 (e.g. ['cloth/bandana', 'black foreign powdery substance', '8L of Mobil 32 DTE oil was released into the sea'])
    PERSON: 12 (e.g. ['Dive Supervisor', 'The Company responsible for setting-up the tent', 'GMO collaborator was stuck in a guide cable'])
    ROOT_CAUSE_CATEGORY: 8 (e.g. ['Biological - Animals, Bacteria, Viruses and Funguses', 'Lifting ops error', 'Stored energy (dropped objects)'])

  Community 2 (size=9384):
    INCIDENT: 3577 (e.g. ['NEAR MISS 596684 - Potential Swivel/Hand Incident - NO INJURY', 'NEAR MISS 16128 - Non Project Related  - S11 Workshop - Material Handler crushed pallet with forklift', 'INCIDENT 718523 - Non-TFMC owned - Equipment Damage - EM Payara - Spitzer HFD - 02 June 2021 - Connector Rolled Off Pallet - Low'])
    EQUIPMENT: 2055 (e.g. ['XT accumulators', 'MRO rig-down', 'mobile racks'])
    LOCATION: 1432 (e.g. ['damaged vehicle was further into the yard than usual', 'his location', 'Kilgore'])
    ORGANIZATION: 934 (e.g. ['CHAP', 'Oceanic 443', 'ACADIAN CONTRACTORS, INC.'])
    EVENT: 506 (e.g. ['driver lost control of the vehicle', 'sliding into the ditch', 'trolley on wheels moved slightly'])
    BODY_PART: 300 (e.g. ['tub ear', 'front driver bumper', 'one knee'])
    CONDITION: 241 (e.g. ['Height of forklift: 3.963 meters', 'slipped off the 4x4 blocks', 'unsafe lean'])
    INJURY_TYPE: 116 (e.g. ['pain and stiffness', 'slight brazed', 'mid-back strain'])
    ACTION: 98 (e.g. ['gripping a packing nut wrench', 'lay down the fences', 'TFMC Lead technician contacted management and HSE'])
    INJURY: 61 (e.g. ['minor pinch on the IP finger', 'minor mechanical damages', 'damage to the tailgate'])
    MATERIAL: 34 (e.g. ['residual Oceanic HW 443 (Glycol/Antifreeze) fluid', 'chamfer of the joint', 'materials on the opposing rack'])
    PERSON: 18 (e.g. ['truck driver who had a trailer attached to his truck', 'Adrian', 'honey bee expert'])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['Computer workplaces / Screens', 'Pinch point', 'Tool suitability'])

  Community 3 (size=5499):
    INCIDENT: 1724 (e.g. ['NEAR MISS 24488 - Vazamento de óleo contido - Trolley L91 20t', 'ACCIDENT 19897 - FAT (First Aid Treatment) - Colaborador sentiu dor no joelho ao acessar uma Plataforma Elevatória Móvel de Trabalho (PEMT)', 'NEAR MISS 28092 - NM - Tool failure / Desprendimento do tensionador'])
    EQUIPMENT: 1206 (e.g. ['mangote de abastecimento de água', 'engine lock', 'proteo glasses'])
    LOCATION: 957 (e.g. ['Enseada do Suá', 'carpenter area', 'mesa de trabalho'])
    ORGANIZATION: 671 (e.g. ['Departamento de Máquinas', 'Vehicle Operator Ind.', 'solda'])
    EVENT: 281 (e.g. ['Lots of hot work activities and lifting operations', 'fuel from the leak, reached the passing boxes of the electric cables of the generator Caterpillar', 'noise of impact'])
    BODY_PART: 231 (e.g. ['lower left corner of the IP’s hand', 'right facial region', 'inner arm'])
    CONDITION: 118 (e.g. ['Technip has a lock out system in place for the equipment in Hall B', 'dischargement of its fixed supports', 'curve two of the cylindrals of saying??the came to seromper'])
    INJURY_TYPE: 108 (e.g. ['danos', 'falling', 'lesion or edema'])
    ACTION: 73 (e.g. ['containment process using a SOPEP kit', 'qualified electrician was called out to re-terminate the cable', 'security conversation between the STC and the team working in the activity'])
    INJURY: 73 (e.g. ['mild scoria??es', 'ear', 'deep cut in the ring finger of his right hand'])
    MATERIAL: 30 (e.g. ['metal sludge fallto', '3 liters of oil on the permeable floor', 'spilling of battery acid'])
    PERSON: 23 (e.g. ['people on the site', 'treated and evaluated by the Medicine', 'collaborator of the employed Vivante'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Dangerous surfaces (sharp/ sharp edged/ high roughness grade)', 'Protection', '3. 3rd Party NCR (received or managed by TechnipFMC or Partners)'])

  Community 4 (size=4068):
    INCIDENT: 1482 (e.g. ['NEAR MISS 8009 - 729420 - IE (Croix CODIR Jaune) - Voirie entre batiment A / P3 - 20/09/2021 - déversement eau + huile lors du transport vireur draps', 'NEAR MISS 21115 - SB-choc sur avant bras gauche', 'NEAR MISS 25371 - Backpain during assembly of a armouring collar'])
    EQUIPMENT: 763 (e.g. ['PMC500', '12T car', 'nappe 2'])
    LOCATION: 529 (e.g. ['BSP08/2', 'park R', 'profylus output'])
    ORGANIZATION: 408 (e.g. ['night gaining team', 'Falck Global Assistance', 'SPCH HARBONNIERES'])
    EVENT: 267 (e.g. ['mineral wood board fall down', 'slipped at ground level', 'cut my glove'])
    BODY_PART: 180 (e.g. ['phalange of his left annular', 'top of the back', 'morts'])
    CONDITION: 133 (e.g. ["diagnosis of 'Miozit. Chronic lumbalgia'", 'marking almost deleted "glycol"', 'valve which lead to the spilling'])
    INJURY_TYPE: 118 (e.g. ['wing breaks', 'muscle pain', 'points of sutures'])
    ACTION: 87 (e.g. ['use of a sabot', 'intervened immediately on the building without being able to provide direct care', 'no action taken'])
    INJURY: 66 (e.g. ['Injury (small scratch)', 'minor abrasion', 'slight pull in the groin area'])
    MATERIAL: 15 (e.g. ['recycled and detergent washed apron', 'hydraulic oil stored in the 200l bowl', 'Approx. 3 Liters of Demin-Water containing Ammonia on the ground'])
    ROOT_CAUSE_CATEGORY: 10 (e.g. ['Environment- Unsorted waste, no traceability of the waste;?', 'Psycho social - Workload (Overload/Underload)', 'Posture (constraint or restricted environment)'])
    PERSON: 10 (e.g. ['treated by the nurse', 'driver of the micro-bus of the company Fiel Turismo', "operator's hands"])

  Community 5 (size=3844):
    INCIDENT: 1153 (e.g. ['ACCIDENT 524560 - FAC - 034693C009 - Yamal LNG Project - Sabetta - 27.01.2017 - Oedema and redness to the face', 'ACCIDENT 508465 - LTI - Yamal LNG Project - Sabetta - 10.09.2016 - Multiple open fractures of 2nd, 3rd, 4th and 5th fingers of left hand', 'NEAR MISS 538417 - NM - 61402S - Zeebrugge/BISY -27/03/17 - Scaffolding plank burning due to hot work'])
    LOCATION: 639 (e.g. ['A - Z Zeno Accident and Emergency Blankenberge', 'foreman’s cabin', 'Dept 45'])
    EQUIPMENT: 574 (e.g. ['metal profile', 'Train 3 314-SSH-002', 'rebar mat'])
    ORGANIZATION: 521 (e.g. ['LLC "Integral', 'Naruzhniye Inzhenerniye Seti', 'OJSC Nord Logistic'])
    EVENT: 228 (e.g. ['body tipping and dropping to the floor', 'line moving under stern of vessel at speed due to current and vessel propulsion', 'slipped and fell down'])
    BODY_PART: 216 (e.g. ['facial soft tissue', 'thumb nail bone', 'right ankle ligaments'])
    INJURY_TYPE: 209 (e.g. ['broken bones', 'Left shin fracture', 'cut wrist injury'])
    CONDITION: 103 (e.g. ['vessel rolling slightly', 'ban for use a day before', 'no PTW opened for the partial draining of cooling system and repair to CW circuit'])
    INJURY: 91 (e.g. ['contusion of right shoulder and right side of chest', 'painful wrist (without fracture)', 'closed fracture of right radius bone with displacement'])
    ACTION: 74 (e.g. ['removal of safety pins', 'misplaced his footing on the last step', 'bound is made with the use of the "trick" type belt'])
    PERSON: 22 (e.g. ['WH personnel', 'Yamgaz (Hautequest K. and Sindhawi N.)', 'people on the platform of TMR 002'])
    MATERIAL: 9 (e.g. ['metal plate (20 cm x 9 cm x 4mm, 250 g weight)', 'Gloves worn at time of incident', '1.8 Tonnes beams'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Falls, slips and trips on same level (without potential to fall to lower level)', 'Fall to lower level / fall to water / loose materials (e.g. silos with granulate)', 'Explosives / potential explosives'])

  Community 6 (size=3501):
    INCIDENT: 1050 (e.g. ['ACCIDENT 18064 - Small tear in a muscle tendon in the elbow (Concluded on MR)', 'NEAR MISS 15248 - Forklift hit by crane during lifting operation', 'ACCIDENT 590330 - Dropped object when transporting crate from transport truck in yard to GR area inside warehouse.'])
    EQUIPMENT: 826 (e.g. ['HCR Funnel', '2” down hose', 'receive tank'])
    LOCATION: 504 (e.g. ['X-29', 'HXT', 'M210'])
    ORGANIZATION: 433 (e.g. ['Avonova Occupational Health Service', 'PCR-X', 'SR GROUP AS'])
    EVENT: 236 (e.g. ['rift approximately 5 cm long by 1 cm deep', 'roller falling 14 metres', 'ITC being overturned'])
    CONDITION: 147 (e.g. ['stumbling into some planks lying on the ground', 'incorrect dimension entered into the PDS', 'Hard hat had fallen off'])
    BODY_PART: 121 (e.g. ['gorilla arm', 'skulderen', 'pinkie'])
    ACTION: 58 (e.g. ['manipulation of the upper clamp', 'bolted up the top blind flange using only 6 of the required 16 studs/nuts', 'placing his right hand on the bottom of one of the bowls'])
    INJURY_TYPE: 52 (e.g. ['paralysis', 'broken one toe', 'stroke'])
    INJURY: 43 (e.g. ['Injury: environmental damage', 'irritation on their eyelid', 'potential injury'])
    MATERIAL: 18 (e.g. ['Materiel damage (1off HP hose)', 'shrimp piece', 'wood waste'])
    PERSON: 11 (e.g. ['cladding worker', 'Apprentice', 'Engineer'])
    ROOT_CAUSE_CATEGORY: 2 (e.g. ['Stored energy (pressure, tension)', '1. Internal NCR (issued by TechnipFMC or Partners)'])

  Community 7 (size=3418):
    INCIDENT: 898 (e.g. ['INCIDENT 644238 - LTI_MMY_Angle strike on workers hand', 'NEAR MISS 22971 - Drop of Huron milling machine container by approx 30cm during manoeuvre to Petrobras pipe', 'NEAR MISS 628338 - NM_EPCC-06_Autonaga fabrication yard main gate got partially damaged'])
    EQUIPMENT: 666 (e.g. ['fouling lifting lug', 'hydraulic rig machine', 'Lock/Unlock pump'])
    LOCATION: 544 (e.g. ['J11', 'LSTK 1 Main Road', 'quarta camada'])
    EVENT: 345 (e.g. ['pinched their finger between the torque wrench and scaffolding', 'roustabout injured finger', 'cut was cleaned and bandaged'])
    ORGANIZATION: 314 (e.g. ['Hyderabad manufacturing facility', 'TECHNIP ENERGIES INDIA LIMITED NEW DELHI', 'KC-4 hub'])
    CONDITION: 182 (e.g. ['driver not noticing the extended hydraulic ramp', 'sharp edge within the waste', 'no barricade'])
    INJURY: 138 (e.g. ['laceration of left arm', 'left hand fore finger', 'small surface cut'])
    ACTION: 110 (e.g. ['transported to the emergency room for further medical evaluation', 'pried off using a screwdriver', 'tightening of the bolt with help of spanner and hammer'])
    BODY_PART: 107 (e.g. ['calf area', 'his wrist', 'back side muscles'])
    INJURY_TYPE: 77 (e.g. ['Light swelling', 'low level burn', 'scratch injuries'])
    MATERIAL: 17 (e.g. ['burnt plastic hoses', 'steel Rack full of Drawing and other official paper', 'water and fluid mix'])
    PERSON: 14 (e.g. ['Project Engineer', 'scaffolders hand', 'Manufacturing Engineer'])
    ROOT_CAUSE_CATEGORY: 6 (e.g. ['Access/Egress', 'Manual handling', 'Hot/cold surfaces or media'])

  Community 8 (size=2935):
    LOCATION: 673 (e.g. ['Area P16', 'KP_x000D_ 19+250', 'Main Marshalling Yard'])
    INCIDENT: 655 (e.g. ['INCIDENT 738259 - DA011-076971C - NEW NAPHTHA COMPLEX EPC - Greece-04.11.2021 – Damage of a handwheel of a valve connected to the Water Circuit of Fire Fighting Vessel in U-7500 - hit by manlfit during its transportation on a truck', 'ACCIDENT 572215 - NON-Technip Owned - TAP-FAC 02 - 2529 TAP - Italy/Melendugno- 09/02/2017 - Superficial skin injury', 'ACCIDENT 588666 - NON Technip Owned - RNT-NM 17 - 2529 TAP - Greece/GSC00 - 24/05/2018 - Excavator damaged underground power cable - 2'])
    ORGANIZATION: 570 (e.g. ['Construction and HS Managers', 'SC management and Safety team', 'CTR’s Engineering Department'])
    EQUIPMENT: 502 (e.g. ['Volvo FH 16', 'boom arm', 'side-boom with a winch'])
    EVENT: 169 (e.g. ['falling to the ground level', 'representative of TAP stopped the work', 'temporary suspension'])
    CONDITION: 122 (e.g. ['puddle that was covered with vegetation', 'bent bottom of the ladder', 'narrow and steep road with blind curves condition'])
    ACTION: 59 (e.g. ['side-boom operator didn’t perform required and mandatory daily visual inspection of side-boom prior to commencement of task', 'removing a skid from the bottom of the platform', 'operator released dead man’s handle'])
    INJURY: 57 (e.g. ['superficial laceration on his left eyebrow', 'exposure to the eyes', 'minor cut wound on his left forehead'])
    BODY_PART: 46 (e.g. ['midwheel', 'right knee area', 'ankle_x000D_'])
    INJURY_TYPE: 46 (e.g. ['first degree burn', 'second fracture', 'skin laceration'])
    PERSON: 18 (e.g. ['archaeology department supervisor', 'crane operator Tynybekov Marat Abaevich', 'operator Mr Papathanasiou Nikolaos'])
    MATERIAL: 14 (e.g. ['damaged electrical cables', 'spilled lubricant', 'underground 2.5 mm grounding cables'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Inadequate Supervision', 'Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)', 'Unfamiliar personnel'])

  Community 9 (size=2639):
    INCIDENT: 747 (e.g. ['ACCIDENT 527857 - Environmental incident (Moderate)-Asiaflex Products Sdn Bhd-blasting bay-24.02.2017-Spillage of contained water from blasting sump pit', 'NEAR MISS 12591 - Building side glass door shattered', 'ACCIDENT 501150 - Near Miss - Asiaflex Products - SP17 - 01.07.2016 - Top Door Fell on to SP17 Machine'])
    EQUIPMENT: 529 (e.g. ['reel AR00004', '34mm spanner', 'TR21 cylinder high mast'])
    LOCATION: 502 (e.g. ['Bay A NJ1', 'laydown yard 140', 'HHL Richards Bay'])
    ORGANIZATION: 329 (e.g. ['Contractor personnel', 'ROU12', 'TECHNIP MARINE (M) SDN. BHD.'])
    EVENT: 202 (e.g. ['damage of wire rope', 'moving from jetty to offshore yard', 'entangle on the machine part'])
    CONDITION: 114 (e.g. ['unstrapped/unsecured', 'melted and burned', 'pipe disturbance effect'])
    BODY_PART: 75 (e.g. ['rear rights body', 'right mirror', 'PLT 004 leg'])
    ACTION: 49 (e.g. ['Extinguished by C02 fire extinguisher', 'cleaning up the spillage', 'barricade the area'])
    INJURY_TYPE: 37 (e.g. ['Counterpain', 'sever moderately', 'soft tissue swelling'])
    INJURY: 27 (e.g. ['electric shock', 'right-hand little finger placed in a splint', 'limited finger movement'])
    MATERIAL: 14 (e.g. ['wooden packing block', 'existing fibre optic cable', 'damage to STBD bow deck stopper'])
    PERSON: 11 (e.g. ['two (2) of the three (3) persons', 'CRAT fire watch person (permit coordinator)', 'operator on the south side'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Equipment condition', 'Electrical current / electrocution / ESD / electromagnetic Fields', 'Electrical'])

  Community 10 (size=2185):
    INCIDENT: 661 (e.g. ['INCIDENT 669569 - Genesis - BHP Ruby - Houma - Accident - NON GENESIS OWNED - Employee injury caused by constrained environment', 'ACCIDENT 540753 - PD - TU-Ltd - 06.06.17 - Vehicle barrier damaged after descending onto a forklift truck passing beneath', 'ACCIDENT 9508 - Eye Irritation'])
    EQUIPMENT: 577 (e.g. ['pre - form rollers', 'packed equipment (Fixator)', 'new metal fire suppression pipes'])
    LOCATION: 293 (e.g. ['Texas State Highway 225', 'Security Hut', 'Hadrian House'])
    ORGANIZATION: 243 (e.g. ['AIS', 'Technip Office', 'X ray company'])
    EVENT: 149 (e.g. ['Damage to the coating on the pipe', 'failure of winch rope', 'caught and shattered'])
    CONDITION: 91 (e.g. ['contact with the deflector', 'light drizzle', 'downward force'])
    INJURY_TYPE: 45 (e.g. ['soft tissue damage', 'tendon damage', 'shockload'])
    ACTION: 43 (e.g. ['the method being followed was to unload two drums at a time', 'TechnipFMC Operators utilised to clean the quay', 'releasing the lock at the top of the steps then the pins at the sides'])
    BODY_PART: 37 (e.g. ['top of his thumb', 'Guillotine Bar', 'shoulder level'])
    INJURY: 28 (e.g. ['slightly strained his neck', 'minor laceration to the finger', 'losing his breath'])
    MATERIAL: 11 (e.g. ['residual material (HDPE)', 'release of AWS 32 hydraulic oil', 'metal brackets weighing 67g'])
    PERSON: 6 (e.g. ['foreman Stankovic Milutin', 'Shepherd offshore personnel', 'spotters'])
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
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 7.7s

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
  PLS deck tensioner control cabin -> personal injury: 1
  air hose -> personal injury: 1
  fitting -> personal injury: 1
  hose -> personal injury: 1
  actuator box -> static electric shock: 1
  gusset plate -> static electric shock: 1
  needle gun -> finger contusion: 1
  needle gun -> nails: 1
  paint scraper -> finger contusion: 1
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
    personal injuries: 4

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
    spraining: 1
    cut: 1

  pallet (186 incidents):
    injuries: 5
    laceration: 3
    injury: 3
    cut: 2
    forward momentum: 1

  PPE (145 incidents):
    cut: 5
    fracture: 3
    bruise: 3
    wounds: 3
    Chemical burn: 2
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
  Abu Dhabi: 3
  Panipat: 3
  Stavanger: 2
  Anvers: 2
```

### MH-08: Hydraulic valve -> injury outcome
**Type:** Multi-hop | **Coverage:** ⚠️ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

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
| Multi-hop (8) | 8 | 5/8 pass | 8/8 pass | 8/8 pass |
| Global (4) | 4 | 4/4 pass | 4/4 pass | 4/4 pass |
| Conjunctive (6) | 6 | 3/6 pass | 3/6 pass | 4/6 pass |

## 4. Key Findings

### What works well at L1

- **AG-01**: Root causes of dropped object incidents
- **AG-02**: Countries with most high-severity incidents
- **AG-03**: Most common equipment by incident count
- **AG-05**: Monthly trend of fall/slip incidents
- **AG-06**: Severity distribution by impact type
- **CJ-01**: Corrosion -> equipment failure -> fire (L2)
- **CJ-04**: Equipment: accident + near-miss same location/year
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
- **MH-08** (Hydraulic valve -> injury outcome): surface form fragmentation reduces accuracy
- **SH-01** (Forklift incidents in 2022): surface form fragmentation reduces accuracy
- **SH-03** (Body parts in crane incidents): surface form fragmentation reduces accuracy
- **SH-04** (Locations for valve incidents): surface form fragmentation reduces accuracy
- **SH-06** (Incidents reported by Shell Offshore): surface form fragmentation reduces accuracy

### Queries blocked until Layer 2

- **CJ-05** (Procedural -> dropped -> head/hand injury (L2)): requires CAUSED_BY/CONTRIBUTED_TO edges

### Data sparsity issues

- **AG-04** (Incident type x business unit crosstab): metadata coverage too low for reliable results
- **CJ-02** (Crane + back + offshore + high severity): metadata coverage too low for reliable results
- **CJ-03** (Maintenance fail + pipe + environmental + Middle East): metadata coverage too low for reliable results

## 5. Regression Diff (vs previous run)

- **CJ-01**: coverage ❌ → ✅
- **CJ-01**: diagnosis L2_REQUIRED → CLEAN

---
*Generated by pipeline_v2/benchmark/run_benchmark.py*