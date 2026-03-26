# L1 Benchmark Query Results

**Generated:** 2026-03-25
**Graph:** 100,407 nodes, 233,856 edges
**Records:** 19,820 metadata rows, 19,851 incident nodes
**Layer:** L1 + L2 (34,499 causal edges)

## 1. Summary Table

| ID | Query | Type | Status | Result |
|------|-------|------|:------:|--------|
| AG-01 | What are the most common root causes of dropped object incidents? | Aggregation | ✅ | 1026 incidents, 43 root_cause_category values, top: Stored energy (dropped objects) |
| AG-02 | Which countries have the highest rate of high-severity incidents? | Aggregation | ✅ | 167 incidents, 22 location values, top: USA |
| AG-03 | What equipment types are involved in the most incidents overall? | Aggregation | ✅ | 19851 incidents, 13446 equipment values, top: forklift |
| AG-04 | How do incidents break down by type (accident vs. near miss) across business units? | Aggregation | ✅ | Crosstab: 4 business_unit values x 3 incident_type values |
| AG-05 | What is the monthly trend of fall/slip incidents over the past 3 years? | Aggregation | ✅ | 1695 incidents across 110 months |
| AG-06 | What proportion of incidents in each impact type category result in high-severity outcomes? | Aggregation | ✅ | Crosstab: 10 impact_type values x 6 severity_bin values |
| CJ-01 | Which incidents match the pattern of corrosion-induced equipment failure leading to fire? | Conjunctive | ✅ | 34,499 causal edges; 800 for fire/explosion |
| CJ-02 | Find all high-severity incidents where a crane was involved AND a back injury was sustained AND the location was offshore. | Conjunctive | ✅ | 0 incidents |
| CJ-03 | Identify incidents where maintenance procedures failed, involving pipe equipment, resulting in environmental impact at locations in the Middle East. | Conjunctive | ✅ | 0 incidents |
| CJ-04 | Which equipment types have caused both injuries AND near-misses at the same location within the same year? | Conjunctive | ✅ | 539 dual-risk equipment/location/year combos |
| CJ-05 | Find the causal chain pattern: procedural non-compliance -> dropped object -> head/hand injury. How many incidents match? | Conjunctive | ✅ | 324 incidents; 12 procedural causal edges |
| CJ-06 | Which incidents involve the co-occurrence of slip/fall events AND vehicle/transportation equipment at construction sites? | Conjunctive | ✅ | 16 incidents |
| CJ-07 | What are the primary effects of corrosion on equipment and incidents in the dataset? | Conjunctive | ✅ | 137 corrosion causal edges across 104 incidents |
| GL-01 | What are the most significant safety risk clusters across TechnipFMC global operations? | Global | ✅ | 11125 communities detected |
| GL-02 | Are there systemic patterns where the same type of equipment failure recurs across different geographic regions? | Global | ✅ | 144 equipment types span 5+ regions |
| GL-03 | How has the overall safety incident profile changed over the dataset time range? Are certain incident types increasing or decreasing? | Global | ✅ | Crosstab: 10 year values x 3 incident_type values |
| GL-04 | What entities serve as the most connected hubs in the knowledge graph, and what does their centrality reveal about systemic risk? | Global | ✅ | Hub analysis: degree + PageRank top 20 |
| IOGP-01 | What injuries result from incidents involving moving vehicles and mobile equipment? | Aggregation | ✅ | 2008 incidents, 122 injury_type values, top: injuries |
| IOGP-02 | How do dropped object incidents break down by severity over time? | Aggregation | ✅ | Crosstab: 6 severity_bin values x 10 year values |
| IOGP-03 | How many incidents involve stored energy or snap-back hazards? | Single-hop | ✅ | 114 incidents |
| IOGP-04 | How many pressurized system incidents resulted in containment loss? | Multi-hop | ✅ | 192 incidents |
| IOGP-05 | Which electrical incidents had lockout/tagout failures? | Conjunctive | ✅ | 142 incidents; 9 FAILED_CONTROL edges |
| IOGP-06 | What body parts are affected in working-at-height incidents with fall protection gaps? | Multi-hop | ✅ | 246 incidents, 76 body_part values, top: left hand |
| IOGP-07 | What injuries result from mechanical lifting incidents with rigging failures? | Multi-hop | ✅ | 2001 incidents, 152 injury_type values, top: injuries |
| IOGP-08 | How many machinery and tool incidents resulted in hand or finger injuries? | Multi-hop | ✅ | 200 incidents |
| MH-01 | Find all equipment types involved in containment loss events leading to injuries at offshore locations. | Multi-hop | ✅ | 1 incidents, 2 equipment types |
| MH-02 | What injury types are associated with equipment failures during maintenance operations? | Multi-hop | ✅ | 29 incidents, 19 pairs |
| MH-03 | Which clients have experienced vessel-related incidents resulting in back injuries? | Multi-hop | ✅ | 47 incidents, 93 organization values, top: OCM |
| MH-04 | What are the most common injury types for each of the top 5 equipment categories? | Multi-hop | ✅ | Injury breakdown for top 5 equipment |
| MH-05 | Find incidents where hand injuries occurred during work involving pipes at locations in Asia Pacific. | Multi-hop | ✅ | 6 incidents |
| MH-06 | What is the severity distribution of incidents involving trucks compared to those involving cranes? | Multi-hop | ✅ | Truck vs crane severity comparison |
| MH-07 | Which locations have the highest concentration of near-miss incidents involving scaffolding? | Multi-hop | ✅ | 121 incidents, 33 location values, top: Sabetta |
| MH-08 | Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents. | Multi-hop | ⚠️ | 1 incidents, 0 injury_type values |
| SC-01 | In incident #623703, what equipment was involved? | Single-hop | ⚠️ | 1 items: ['forklift'] |
| SC-02 | In incident #570187, what equipment was involved? | Single-hop | ✅ | 3 items: ['Connector link', 'feeder box', 'feeder breaker'] |
| SC-03 | In incident #602346, what equipment was involved? | Single-hop | ✅ | 2 items: ['PGB', 'forklift'] |
| SC-04 | In incident #14338, what equipment was involved? | Single-hop | ✅ | 1 items: ['press'] |
| SC-04b | In incident #14338, which body parts were affected? | Single-hop | ✅ | 1 items: ['lower back'] |
| SC-05 | In incident #500389, what equipment was involved? | Single-hop | ✅ | 4 items: ['chain', 'football float', 'marker buoys', 'odom weight'] |
| SC-06 | In incident #8712, what equipment was involved? | Single-hop | ✅ | 1 items: ['CEU 25 barrier'] |
| SC-06b | In incident #8712, which body parts were affected? | Single-hop | ✅ | 3 items: ['face', 'forehead', 'head'] |
| SC-07 | In incident #511771, what equipment was involved? | Single-hop | ✅ | 2 items: ['crane hook', 'wire rope sling'] |
| SC-07b | In incident #511771, which body parts were affected? | Single-hop | ✅ | 1 items: ['lower lip'] |
| SC-08 | In incident #324, what equipment was involved? | Single-hop | ✅ | 1 items: ['20T Forklift'] |
| SC-09 | In incident #18312, what equipment was involved? | Single-hop | ✅ | 2 items: ['crane', 'plastic sun visor'] |
| SC-09b | In incident #18312, which body parts were affected? | Single-hop | ✅ | 1 items: ['head'] |
| SH-01 | What incidents involved forklifts in 2022? | Single-hop | ✅ | 71 incidents |
| SH-02 | What equipment was involved in incident #29857? | Single-hop | ⚠️ | 3 items: ['ROV', 'lanyard', 'pry bar'] |
| SH-03 | What body parts were affected in crane-related incidents? | Single-hop | ✅ | 1444 incidents, 192 body_part values, top: finger |
| SH-04 | Which locations reported valve-related incidents? | Single-hop | ✅ | 387 incidents, 36 location values, top: USA |
| SH-05 | What types of injuries resulted from incidents at offshore installations? | Single-hop | ✅ | 1120 incidents, 124 injury_type values, top: cut |
| SH-06 | What incidents were reported by client SHELL OFFSHORE INC.? | Single-hop | ✅ | 60 incidents |

**Overall:** 49 ✅ passing / 3 ⚠️ failing out of 52 queries

## 2. Per-Query Details

### AG-01: What are the most common root causes of dropped object incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

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

### AG-02: Which countries have the highest rate of high-severity incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

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
  Australia: 3
  Malaysia: 3
  Angola: 3
  Canada: 3
```

### AG-03: What equipment types are involved in the most incidents overall?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

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
  reel: 98
  manlift: 98
  gloves: 96
  sling: 94
  safety glasses: 93
  machine: 93
  pump: 82
  winch: 81
  truck: 81
```

### AG-04: How do incidents break down by type (accident vs. near miss) across business units?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
business_unit null rate: 14007/19820 (70.7%)

| business_unit | Accident | Near Miss | Unknown | Total |
|---|---|---|---|---|
| Unknown | 5190 | 3368 | 5449 | 14007 |
| Subsea | 1756 | 1184 | 0 | 2940 |
| REMS | 757 | 970 | 0 | 1727 |
| Surface | 850 | 296 | 0 | 1146 |
```

### AG-05: What is the monthly trend of fall/slip incidents over the past 3 years?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

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

### AG-06: What proportion of incidents in each impact type category result in high-severity outcomes?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

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

### CJ-01: Which incidents match the pattern of corrosion-induced equipment failure leading to fire?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

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

### CJ-02: Find all high-severity incidents where a crane was involved AND a back injury was sustained AND the location was offshore.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-03: Identify incidents where maintenance procedures failed, involving pipe equipment, resulting in environmental impact at locations in the Middle East.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 0
```

### CJ-04: Which equipment types have caused both injuries AND near-misses at the same location within the same year?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.4s

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

### CJ-05: Find the causal chain pattern: procedural non-compliance -> dropped object -> head/hand injury. How many incidents match?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

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

### CJ-06: Which incidents involve the co-occurrence of slip/fall events AND vehicle/transportation equipment at construction sites?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 16
Sample: ['INCIDENT::11732', 'INCIDENT::24216', 'INCIDENT::520161', 'INCIDENT::527205', 'INCIDENT::543663']
```

### CJ-07: What are the primary effects of corrosion on equipment and incidents in the dataset?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.5s

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

### GL-01: What are the most significant safety risk clusters across TechnipFMC global operations?
**Type:** Global | **Status:** ✅ | **Time:** 8.2s

```
Total communities: 11125
Top 10 by size:

  Community 1 (size=10602):
    INCIDENT: 3177 (e.g. ['ACCIDENT 510078 - Minor First Aid Non Work Related- 033968C001 MOHO Nord – G1200 – 27 Sep 2016 – Superficial abrasion to crown of head', 'ACCIDENT 1313 - Deep Discoverer - Medical Treatment - Repsol IRM TVIT - 300701C001 - 15.04.2022 - Diver with ear infection', 'ACCIDENT 9014 - Damage – Deep Blue - Mero I - Kenz crane main block hit wire guide / Cabo impactado pelo bloco principal do guindaste Kenz'])
    EQUIPMENT: 3017 (e.g. ['navigation chair', '7-function arm', '16 tonne forklift'])
    LOCATION: 1991 (e.g. ['Kota Kinabalu', 'Vessel position', 'Rouen'])
    ORGANIZATION: 1643 (e.g. ["TA's", 'Sea-Invest Shipping Agency', 'Technip Umbilical'])
    BODY_PART: 259 (e.g. ['lower edge of the coaming', 'costado da embarca', 'outer left foot'])
    EVENT: 250 (e.g. ['entered the water', 'reached the lower work station', 'hub projection'])
    INJURY_TYPE: 105 (e.g. ['small superficial incisive lesion', 'muscular pain', 'danos leves'])
    CONDITION: 61 (e.g. ['access to the deck being barriered off', 'raining', 'Tool not seated properly into the gap of the two plates'])
    INJURY: 40 (e.g. ['punctured his left hand through the glove in the palm region', 'small scratch on the skin surface', 'laceration to the inside of his right hand'])
    ACTION: 35 (e.g. ['grinding on C-channel', 'Mx Paracetamol 500mg 1-2 Tab 4x a day', '2 weeks rest of affected area'])
    MATERIAL: 10 (e.g. ['welding rod (24" in length and weighing about 2oz)', 'hot iron chip', 'leaked hydraulic fluid'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Hyperbaric work environment', 'Equipment Suitability', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)'])
    PERSON: 7 (e.g. ['operator responsible for driving the wire was near', 'third party employee in the cell', 'Rigging Supervisor being in charge of reel rotation'])

  Community 2 (size=9993):
    INCIDENT: 3952 (e.g. ['ACCIDENT 21466 - Environmental Release – OXY Warrior – Olympic Challenger – Haliburton PHORCYS - 19 May 2024 2300hrs - PHORCYS hydraulic Release', 'NEAR MISS 575579 - Trash can caught fire due to a chemical combustion.', 'INCIDENT 675717 - Near Miss - Gremp Campus - S05 - March 6, 2020 - Open hole grating- fall'])
    EQUIPMENT: 2374 (e.g. ['fan', '1502 wing nut', 'mainline 2'])
    LOCATION: 1622 (e.g. ['media/demo area', 'Cutback B', 'main driveway'])
    ORGANIZATION: 1060 (e.g. ['HSE/Medic', 'FMC FLUID CONTROL', 'the I.P.'])
    BODY_PART: 337 (e.g. ['windshield', 'right wrist area', 'right arm/elbow'])
    EVENT: 299 (e.g. ['two sutures being administered', 'collaborator suffered a motorcycle crash', 'right rear tire of the truck contacting a concrete pier'])
    INJURY_TYPE: 142 (e.g. ['fracturing', 'burn and itch', 'injection injury'])
    CONDITION: 80 (e.g. ['distance between the edge of the barge and bulkhead', 'change in the 2 bites', 'metal buckling'])
    ACTION: 59 (e.g. ['disposed of', 'removed this equipment from the work area', 'tensioning and torquing studs'])
    INJURY: 41 (e.g. ['small laceration located in the transition between the frontal lobe and top of skull', 'laceration to his left middle finger', "puncturing of employee's left index finger"])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['Computer workplaces / Screens', 'Over-consumption of energy, natural resources (water, etc.)', 'Unprotected/unguarded moving machine parts (struck by/caught by)'])
    MATERIAL: 10 (e.g. ['fluid in the picture was from a prior operation removing the hoses', 'material damage to the vehicle on the front', 'residual Oceanic HW 443 (Glycol/Antifreeze) fluid'])
    PERSON: 5 (e.g. ['Collaborators (two) third parties coming from home to work, walking along the side of a small bridge', 'Goods Inwards Inspector', 'trained First Aider'])

  Community 3 (size=5416):
    INCIDENT: 1877 (e.g. ['INCIDENT 641877 - NM - Dutra Industrial Plants - Fabrica Matriz - Quebra de conex?o e vazamento de gás', 'ACCIDENT 9049 - Worker sprained ankle leaving interla part of material basket', 'NEAR MISS 7689 - 673726 - NM - Base Macaé Cabiúnas - Batida contra UTF'])
    EQUIPMENT: 1227 (e.g. ['lanch', '8-10kg pip-support', 'directory cup refrigerator'])
    LOCATION: 1001 (e.g. ['valve duts', 'track 3', 'Bay 906'])
    ORGANIZATION: 706 (e.g. ['asart', 'MCV', 'Plataforma de trabalho aéreo – PTA'])
    BODY_PART: 235 (e.g. ['cotovelo', 'corrim?o', 'mounted foot'])
    EVENT: 158 (e.g. ['Counter balance hit and pushed open the machine tool doors with considerable force', 'control of the principle of fire', 'water bottle falling from EVDT (XT-Christmas Tree)'])
    INJURY_TYPE: 110 (e.g. ['paralysis', 'roulette discharge', 'physical or material damage'])
    INJURY: 33 (e.g. ['wounds or damage to the equipment', 'hematoma under the nail', 'slight scory??o'])
    CONDITION: 33 (e.g. ['loose soil at the edge', 'area was clear', 'abnormal stop of the electric engine of the bow-thruster of vante'])
    ACTION: 17 (e.g. ['immediate barriered off', 'slipping on the edge of the work platform step', 'restrictive measures with administrative activities'])
    ROOT_CAUSE_CATEGORY: 13 (e.g. ['Management of Change', 'Unprotected/unguarded moving machine parts (struck by/caught by )', 'Information perceptiveness (amount / mode) & Information reception (extend / range)'])
    MATERIAL: 4 (e.g. ['nylon parts (3 on main deck, one on the barge)', 'concrete portion of the roof', 'concrete pieces'])
    PERSON: 2 (e.g. ['people in the environment', 'operator in the face'])

  Community 4 (size=4178):
    INCIDENT: 1313 (e.g. ['ACCIDENT 600504 - FAC - TU Ltd -  02.08.2018 - IP tripped down a step and twisted his ankle.', 'ACCIDENT 565859 - FAC - Yamal LNG Project - Sabetta - 1.1.2018 - Contusion of the left shoulder joint.', 'INCIDENT 739038 - First Aid 105- MIDOR - Egypt - 9.12.2021- Hard barricades fell inside the cable trench on workers shoulder'])
    LOCATION: 743 (e.g. ['Sabetta village', 'pioneer Offices', 'road slab'])
    EQUIPMENT: 639 (e.g. ['G1200 Helideck', 'electrical travelling crane', 'Air Compressor 70-K-120'])
    ORGANIZATION: 574 (e.g. ['LLC ?Teplovent?', 'Pugnax', 'Velesstroy NDT'])
    INJURY_TYPE: 241 (e.g. ['phalange fissure', 'Right Ankle ligament sprain', 'lateral malleoulus fracture'])
    BODY_PART: 237 (e.g. ['occiput', 'fingers 4 and 5 of his right hand', 'right illium'])
    EVENT: 187 (e.g. ['contact between step ladder and bell trolley frame', 'industrial electric extension cord short circuit', 'hydraulic oil spilled on personnel'])
    INJURY: 100 (e.g. ['cut to the inside of his knee', 'Injury("stomach")', 'Closed fracture of proximal phalanx IV finger of the left hand'])
    CONDITION: 65 (e.g. ['no other obstructions, loose objects or slip hazards in the area', 'sudden change in CG (Eccentric load)', 'swollen'])
    ACTION: 61 (e.g. ['accidentally struck Supervisor with the end of a strip', 'laborer removed protective mask', 'disconnection of air hose without shutting off valve on air line'])
    MATERIAL: 10 (e.g. ['debris', 'hot porrige', 'unsecured wooden edging strip (500g)'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Explosives / potential explosives', 'Traffic Management / Routes / Pedestrian path', 'Falls, slips and trips on same level (without potential to fall to lower level)'])
    PERSON: 3 (e.g. ['SNEMA wireman walking backwards', 'REGA slinger', "IP's face"])

  Community 5 (size=3839):
    INCIDENT: 1477 (e.g. ["NEAR MISS 564444 - NM - Atelier FTF - 22/12/2017 - Rupture d'un flexible hydraulique", 'NEAR MISS 21849 - NM SIF - Packing area - Falling outboard cap', 'NEAR MISS 594244 - IE/26/06/2018/TRI NON EFFECTUE DANS BENNES MIS A DISPOSITION'])
    EQUIPMENT: 756 (e.g. ['Drain pipe', 'monocuve', 'safe'])
    LOCATION: 520 (e.g. ['shower stall', 'domicile', 'workplace'])
    ORGANIZATION: 418 (e.g. ['PLACEO', 'SCI Company', 'Site Manager'])
    BODY_PART: 176 (e.g. ['left index', 'visor', 'goutcher'])
    EVENT: 175 (e.g. ['worker felt a slight shock on his helmet', 'operator helped him descend', "contact of the potency crossing with the victim's hand placed on the crossing"])
    INJURY_TYPE: 117 (e.g. ['cut his hand', '2 fractures', 'HSE strain'])
    INJURY: 77 (e.g. ['trigger thumb', 'Left arm of the worker', 'pain in the lower back'])
    ACTION: 57 (e.g. ['external manipulation the previous day for cites', 'forced to use a ladder', 'bending down'])
    CONDITION: 47 (e.g. ['hole was higher than expected', 'steam and the activities of the ADF subcontractor', 'low pressure only'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['Posture (constraint or restricted environment)', 'Psycho social - Work time/ Shift pattern', 'Climate (Heat/Cold/Humidity)'])
    MATERIAL: 5 (e.g. ['red-colored water recovered in the network', 'the edge of the lid', 'waterized MUD'])
    PERSON: 5 (e.g. ['First Responder', 'operator', 'informed to the HSE department and labor medicine'])

  Community 6 (size=3146):
    INCIDENT: 898 (e.g. ['INCIDENT 740325 - Near miss Report_201744C001 - 1074 - OHCU-FGTU Project_15.12.21_Reverse movement of construction equipment (TMR) close to person', 'NEAR MISS 601446 - Near miss_073633C001_IGHDS Prime G site_Bongaigaon_06.08.18_Lowering of member while installation', 'ACCIDENT 17458 - Left hand finger trapped under ~20kg pipe end fitting'])
    EQUIPMENT: 614 (e.g. ['3rd rig HR-180', 'Appropriate use of PPE (Impact Gloves)', 'Pneumatic valve'])
    LOCATION: 563 (e.g. ['dark room', 'large assembly area', 'reactor area'])
    ORGANIZATION: 330 (e.g. ['third-party transport operator', 'Client Rasgas', 'HPL First aid centre'])
    EVENT: 287 (e.g. ['knife slit thru the finger', 'falling off', 'cargo door falling'])
    BODY_PART: 125 (e.g. ['head/shoulder', 'core', 'left hand thumb'])
    CONDITION: 112 (e.g. ['work area barricaded', 'potential fall to lower level', 'polished floor in accommodation corridors'])
    INJURY_TYPE: 75 (e.g. ['near miss incident', 'bruise', 'reducer type'])
    ACTION: 63 (e.g. ['cutting wood pieces', 'first aid on site', 'removal of gloves for additional dexterity'])
    INJURY: 59 (e.g. ["pinch injury to IP's right ring finger", 'cut to left hand index finger', 'small cut to the index finger of his right hand'])
    MATERIAL: 12 (e.g. ['water and fluid mix', 'hydraulic fluid on the ground', 'absorbents'])
    PERSON: 5 (e.g. ['employee working on scaffold', 'Injured Person (IP)', 'employee not stopping to check on employee'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Manual handling', 'Use of personal protective equipment', 'Accumulation / Presence of explosive atmosphere'])

  Community 7 (size=3069):
    INCIDENT: 1035 (e.g. ['INCIDENT 697636 - Transporting XT. G-26 could have gone bad', 'INCIDENT 645876 - Forklift incident outside B16', 'ACCIDENT 25114 - Property Damage - Fence Struck by Front End Loader - Tenaris Shawcor - Utsira High Tie-Backs Project - 301622C001'])
    EQUIPMENT: 770 (e.g. ['spooling device', 'pallet frame', 'rag'])
    LOCATION: 492 (e.g. ['halls A and B', 'Building 3', 'Horten site'])
    ORGANIZATION: 425 (e.g. ['forklfit', 'Subsea Seven', 'TBH'])
    BODY_PART: 111 (e.g. ['upper mouth', 'reolen', 'gorilla arm'])
    EVENT: 95 (e.g. ['water discharge', 'damage to the outer sheath', 'incident was classified as a Hazard Observation'])
    INJURY_TYPE: 45 (e.g. ['hairline fracture', 'tear', 'burn like wound'])
    CONDITION: 37 (e.g. ['operator was wearing all PPE for that particular activity', 'plastic drip tray appeared slippery in dry conditions', 'exertion of the task'])
    INJURY: 28 (e.g. ['cut to above his left eye', 'sliced open the top of the knuckle and nicked the tendon at the base of the index finger', 'severe injury to IP’s right foot'])
    ACTION: 21 (e.g. ['failure to disconnect all the cables', "IP inspected the surface but didn't see any objects", 'pipework removal being carried out prior to the isolation being requested or confirmed'])
    MATERIAL: 4 (e.g. ['aluminum', 'property and equipment were not damaged', 'no material damage was inflicted'])
    PERSON: 3 (e.g. ['deck rigging crew', 'emergency team on yard', 'person opening the door fast from another side without seeing me'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Radiation (ionising / non ionising)', '1. Internal NCR (issued by TechnipFMC or Partners)', 'Difficult/Hindered operability of tools and equipment'])

  Community 8 (size=2845):
    LOCATION: 668 (e.g. ['KP71', 'Krithia', 'KP 178'])
    INCIDENT: 659 (e.g. ['ACCIDENT 612142 - NON-Technip Owned - BNJ-DA (RTA) 12 - 2529 TAP Project - Greece/Kastoria - 24/10/2018 - iPMT vehicle ending up on the field', 'INCIDENT 655594 - NON-Technip Owned - SPM-RWDC 01 - 2529 TAP - Italy/Italian Landfall -  16/10/2019 - Cut on 2nd finger of right hand', 'ACCIDENT 640411 - NON-Technip Owned - RNT-FAC 15 - 2529 TAP - Albania/ACS03 - 20/06/2019 - Bumped forehead against a corner of a pipe support'])
    ORGANIZATION: 577 (e.g. ['Framework', 'Health manager', 'Bonatti millwright'])
    EQUIPMENT: 495 (e.g. ['Alco tester', 'light 4x4 truck', 'snow clearing equipment'])
    EVENT: 174 (e.g. ['batch payment of AUD$24095.20 being transferred to a fraudulent account', 'power cut', 'pipe spool slipped from trailer bed'])
    CONDITION: 76 (e.g. ['SCM inspection stand MKII adapter insert not fully installed into the stand', 'angle they were standing', 'open to air'])
    BODY_PART: 52 (e.g. ['dorsal base', 'one rib', 'left inner thigh'])
    INJURY_TYPE: 46 (e.g. ['bruise injuries', 'pelvis fracture', 'pain_x000D_'])
    INJURY: 44 (e.g. ['laceration on the distal phalanx of right middle finger', "injury to the worker's finger", 'FST struck in the chest'])
    ACTION: 40 (e.g. ['one of them used the nearest fire extinguisher to fight the fire departure', 'voice command several times by the radio "stop pulled"', 'failure to build a platform outside the shaft'])
    MATERIAL: 8 (e.g. ['burn cream from first aid room', 'fuel materials that were inside the equipment', 'barbed wire made of elastic and cutting material'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)', 'Inadequate Supervision', 'Unfamiliar personnel'])
    PERSON: 2 (e.g. ['Nikita Chirko', 'the crew consisted of 1 supervisor, 2 excavator operators, 2 side boom operators'])

  Community 9 (size=1971):
    INCIDENT: 624 (e.g. ['NEAR MISS 603365 - Near-Miss: Dropped object cause of Zinc roof fell over from roof top.', 'INCIDENT 714744 - Fire Incident - APSB - Open Yard - 04/05/2021 - Fire at Underneath the Carousel', 'INCIDENT 698086 - Damage Incident resulting in DROPS - 078072C003 - Merakes – Skandi Africa - Kevlar band parted during inner clamp tensioning resulting in the clamp being dropped.'])
    EQUIPMENT: 444 (e.g. ['AR00072', 'signal lights', '2 x Running Line Meters'])
    LOCATION: 426 (e.g. ['Jalan Pahang', 'Supervisor Block 3', 'Suction Pile Area'])
    ORGANIZATION: 285 (e.g. ['Institut Jantung Negara', 'tooling team', 'FMC WELLHEAD EQUIPMENT SDN BHD'])
    EVENT: 64 (e.g. ['sludge discharge onto the quayside', 'air pressure hose burst', 'Fenja Trial respool stood down overnight'])
    BODY_PART: 55 (e.g. ['termination head', 'thumb nail', 'Top roof'])
    INJURY_TYPE: 30 (e.g. ['soft tissue injury', 'rubbing', 'overload'])
    CONDITION: 18 (e.g. ['minor dented on Long Boring Bar body', 'the wire wheel was still spinning freely (power was off)', 'out-barrier damaged'])
    ACTION: 10 (e.g. ['smoke detector was removed', 'Team Leader want to switch-on high-baylight', 'scaffold jack base used as a hammer'])
    INJURY: 10 (e.g. ['bent the thumbnail back', 'finger injury (Right hand thumb)', 'mild electric shock'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Weather Condition', 'Electrical current / electrocution / ESD / electromagnetic Fields', 'Psycho social - Alcohol and drugs abuse'])
    MATERIAL: 1 (e.g. ['wooden packing block'])
    PERSON: 1 (e.g. ['stray dog'])

  Community 10 (size=1921):
    INCIDENT: 643 (e.g. ['INCIDENT 689284 - Incident Notification- Near Miss- Shawcor - Shell PowerNap - August 8, 2020 - Box of Poly Bead Material Fell While Being Transferred Over Conveyor Ramp', 'INCIDENT 658615 - NM - TUL - 08.11.2019 - Dropped Tube', 'INCIDENT 704353 - NM - TUL - 20.01.2021 - IP aggravated existing injury to shoulder'])
    EQUIPMENT: 532 (e.g. ['jackable units', 'X-ray screens', 'product encoder'])
    LOCATION: 288 (e.g. ['gravel parking lot', 'River Tyne', 'TPU compressor area'])
    ORGANIZATION: 241 (e.g. ['Liza Project', 'AIS', 'Elis'])
    EVENT: 79 (e.g. ['Employee fell to floor landing on backside', 'grinding', 'fall on to the floor'])
    INJURY_TYPE: 43 (e.g. ['No major cut', 'unspecific strain', 'blood blister'])
    BODY_PART: 38 (e.g. ['left side of her back', 'elbow area', 'fingernail'])
    CONDITION: 32 (e.g. ['no oil leakage to environment', 'oil on the fan cowling', 'smooth surface on the concrete'])
    ACTION: 15 (e.g. ['more force used to cut the sample', 'bending down to measure pipe on the Thermal outbound deck', 'TOFS carried out by OCM'])
    INJURY: 9 (e.g. ['spraying one of our nearby Technip Apps tech on the side of his face', 'first and second-degree burns to his forearms and left armpit area', 'no personal were affected'])
    PERSON: 1 (e.g. ['gangway watchman was in place'])
```

### GL-02: Are there systemic patterns where the same type of equipment failure recurs across different geographic regions?
**Type:** Global | **Status:** ✅ | **Time:** 0.2s

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

### GL-03: How has the overall safety incident profile changed over the dataset time range? Are certain incident types increasing or decreasing?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

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

### GL-04: What entities serve as the most connected hubs in the knowledge graph, and what does their centrality reveal about systemic risk?
**Type:** Global | **Status:** ✅ | **Time:** 6.9s

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

### IOGP-01: What injuries result from incidents involving moving vehicles and mobile equipment?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2008
Distinct INJURY_TYPE values: 122
Top 10:
  injuries: 64
  cut: 16
  injury: 14
  minor damage: 11
  laceration: 10
  contusion: 10
  pain: 9
  abrasion: 8
  No one was injured: 7
  fracture: 7
```

### IOGP-02: How do dropped object incidents break down by severity over time?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.4s

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

### IOGP-03: How many incidents involve stored energy or snap-back hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 114
Sample: ['INCIDENT::10888', 'INCIDENT::12332', 'INCIDENT::12630', 'INCIDENT::12715', 'INCIDENT::13227']
```

### IOGP-04: How many pressurized system incidents resulted in containment loss?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 192
Sample: ['INCIDENT::10674', 'INCIDENT::10923', 'INCIDENT::10992', 'INCIDENT::11942', 'INCIDENT::12909']
```

### IOGP-05: Which electrical incidents had lockout/tagout failures?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.3s

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

### IOGP-06: What body parts are affected in working-at-height incidents with fall protection gaps?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 246
Distinct BODY_PART values: 76
Top 10:
  left hand: 15
  shoulder: 10
  left foot: 10
  left leg: 8
  eye: 4
  arm: 4
  ankle: 4
  lower leg: 3
  Knee: 3
  wrist: 3
```

### IOGP-07: What injuries result from mechanical lifting incidents with rigging failures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

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
  personal injuries: 6
```

### IOGP-08: How many machinery and tool incidents resulted in hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 200
Sample: ['INCIDENT::10299', 'INCIDENT::10348', 'INCIDENT::10636', 'INCIDENT::10759', 'INCIDENT::10789']
```

### MH-01: Find all equipment types involved in containment loss events leading to injuries at offshore locations.
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Containment RCC values matched: ['Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution)', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)']
Containment incidents: 1202
-> Offshore containment: 50
-> With injuries: 1
Equipment in those incidents:
  150T crane: 1
  main hoist winch drum: 1
```

### MH-02: What injury types are associated with equipment failures during maintenance operations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 29
EQUIPMENT->INJURY_TYPE pairs (top 10):
  whip check -> personal injury: 2
  air hose -> personal injury: 1
  fitting -> personal injury: 1
  hose -> personal injury: 1
  PLS deck tensioner control cabin -> personal injury: 1
  needle gun -> finger contusion: 1
  needle gun -> nails: 1
  paint scraper -> finger contusion: 1
  paint scraper -> nails: 1
  pedestal grinder -> finger contusion: 1
```

### MH-03: Which clients have experienced vessel-related incidents resulting in back injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 47
Distinct ORGANIZATION values: 93
Top 10:
  OCM: 9
  TECHNIPFMC: 8
  HSEA: 5
  HSE: 5
  WOODSIDE ENERGY LTD.: 4
  ISOS: 4
  TECHNIP MARINE OPERATION SERVICES: 4
  IP: 4
  PETROBRAS: 3
  ENQUEST BRITAIN LTD.: 3
```

### MH-04: What are the most common injury types for each of the top 5 equipment categories?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Top 5 equipment (by incident count):

  forklift (771 incidents):
    injuries: 20
    injury: 7
    abrasion: 5
    pain: 5
    personal injuries: 4

  crane (622 incidents):
    injuries: 18
    fracture: 5
    abrasion: 4
    personal injury: 4
    injury: 3

  ROV (290 incidents):
    personal injury: 3
    ferimentos pessoais: 2
    personnel injury: 1
    injury: 1
    incident categorisation: 1

  pallet (186 incidents):
    injuries: 5
    laceration: 3
    injury: 3
    cut: 2
    contusion: 1

  PPE (145 incidents):
    cut: 5
    wounds: 3
    fracture: 3
    bruise: 3
    Chemical burn: 2
```

### MH-05: Find incidents where hand injuries occurred during work involving pipes at locations in Asia Pacific.
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 6
Sample: ['INCIDENT::10789', 'INCIDENT::522669', 'INCIDENT::526879', 'INCIDENT::547023', 'INCIDENT::571988']
```

### MH-06: What is the severity distribution of incidents involving trucks compared to those involving cranes?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

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

### MH-07: Which locations have the highest concentration of near-miss incidents involving scaffolding?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

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
  Penglai: 2
  Milan: 2
```

### MH-08: Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents.
**Type:** Multi-hop | **Status:** ⚠️ | **Time:** 0.2s

```
Matching incidents: 1
Distinct INJURY_TYPE values: 0
Top 10:
```

### SC-01: In incident #623703, what equipment was involved?
**Type:** Single-hop | **Status:** ⚠️ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::623703: ['forklift']
Ground truth: ['forklift', 'manifold', 'mirror']
Missing: ['manifold', 'mirror']
Extra (unexpected): none
```

### SC-02: In incident #570187, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::570187: ['Connector link', 'feeder box', 'feeder breaker']
Ground truth: ['connector link', 'feeder box', 'feeder breaker']
Missing: none
Extra (unexpected): none
```

### SC-03: In incident #602346, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::602346: ['PGB', 'forklift']
Ground truth: ['forklift', 'pgb']
Missing: none
Extra (unexpected): none
```

### SC-04: In incident #14338, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::14338: ['press']
Ground truth: ['press']
Missing: none
Extra (unexpected): none
```

### SC-04b: In incident #14338, which body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::14338: ['lower back']
Ground truth: ['lower back']
Missing: none
Extra (unexpected): none
```

### SC-05: In incident #500389, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::500389: ['chain', 'football float', 'marker buoys', 'odom weight']
Ground truth: ['chain', 'football float', 'marker buoys', 'odom weight', 'tms']
Missing: ['tms']
Extra (unexpected): none
```

### SC-06: In incident #8712, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::8712: ['CEU 25 barrier']
Ground truth: ['ceu 25 barrier']
Missing: none
Extra (unexpected): none
```

### SC-06b: In incident #8712, which body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::8712: ['face', 'forehead', 'head']
Ground truth: ['face', 'forehead', 'head']
Missing: none
Extra (unexpected): none
```

### SC-07: In incident #511771, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::511771: ['crane hook', 'wire rope sling']
Ground truth: ['crane hook', 'wire rope sling']
Missing: none
Extra (unexpected): none
```

### SC-07b: In incident #511771, which body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::511771: ['lower lip']
Ground truth: ['lower lip']
Missing: none
Extra (unexpected): none
```

### SC-08: In incident #324, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::324: ['20T Forklift']
Ground truth: ['20t forklift']
Missing: none
Extra (unexpected): none
```

### SC-09: In incident #18312, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::18312: ['crane', 'plastic sun visor']
Ground truth: ['crane', 'plastic sun visor']
Missing: none
Extra (unexpected): none
```

### SC-09b: In incident #18312, which body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::18312: ['head']
Ground truth: ['head']
Missing: none
Extra (unexpected): none
```

### SH-01: What incidents involved forklifts in 2022?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 71
Sample: ['INCIDENT::10170', 'INCIDENT::10252', 'INCIDENT::10333', 'INCIDENT::1061', 'INCIDENT::1069']
```

### SH-02: What equipment was involved in incident #29857?
**Type:** Single-hop | **Status:** ⚠️ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::29857: ['ROV', 'lanyard', 'pry bar']
Ground truth: ['lanyard', 'pry bar', 'rov', 'tms']
Missing: ['tms']
Extra (unexpected): none
```

### SH-03: What body parts were affected in crane-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

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

### SH-04: Which locations reported valve-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 387
Distinct LOCATION values: 36
Top 10:
  USA: 172
  UK: 61
  Norway: 19
  Canada: 16
  France: 13
  Brazil: 11
  Argentina: 11
  China: 10
  India: 9
  Russia: 7
```

### SH-05: What types of injuries resulted from incidents at offshore installations?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

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
  bruising: 4
  injury: 4
  fracture: 4
```

### SH-06: What incidents were reported by client SHELL OFFSHORE INC.?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 60
Sample: ['INCIDENT::100', 'INCIDENT::1039', 'INCIDENT::11906', 'INCIDENT::12463', 'INCIDENT::12507']
```

## 3. Failing Queries

- **MH-08** (Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents.): 1 incidents, 0 injury_type values
- **SC-01** (In incident #623703, what equipment was involved?): 1 items: ['forklift']
- **SH-02** (What equipment was involved in incident #29857?): 3 items: ['ROV', 'lanyard', 'pry bar']

## 4. Regression Diff (vs previous run)

No regressions — all results stable.

---
*Generated by pipeline/benchmark/run_benchmark.py*