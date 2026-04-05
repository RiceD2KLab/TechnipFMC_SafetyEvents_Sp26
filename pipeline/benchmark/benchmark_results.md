# L1 Benchmark Query Results

**Generated:** 2026-03-25
**Graph:** 100,407 nodes, 233,942 edges
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
  Canada: 3
  Angola: 3
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
  manlift: 98
  reel: 98
  gloves: 96
  sling: 94
  machine: 93
  safety glasses: 93
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
**Type:** Global | **Status:** ✅ | **Time:** 8.4s

```
Total communities: 11125
Top 10 by size:

  Community 1 (size=10602):
    INCIDENT: 3177 (e.g. ['ACCIDENT 566838 - FAT - Finger injury from pinch point', 'ACCIDENT 545541 - HSE Incident-Environmental-068878C001-Deep Energy.19.07.2017-Burst hose on ROV system subsea.', 'ACCIDENT 21854 - FAC - Failed regulator whilst pressurising pump for gas hose hydrostatic testing'])
    EQUIPMENT: 3017 (e.g. ['U bolt and bracket arrangement', 'Chicago female fitting', 'UTM OSS 844/4'])
    LOCATION: 1991 (e.g. ['Ninian/ Orlando Field', 'Remontowa yard', 'MJ Field'])
    ORGANIZATION: 1643 (e.g. ['vessel Medic', 'Marine Department', 'vessel HSEA'])
    BODY_PART: 259 (e.g. ['Upper Respiratory Tract', 'AC Joint', 'left knee_x000D_'])
    EVENT: 250 (e.g. ['umbilical slipped from the friction clamp', 'pipe moved and rotate toward, hitting a manometer and a valve', 'yellow buoy passed below the wire and has been compressed between the roller and the wire'])
    INJURY_TYPE: 105 (e.g. ['2 cm abrasion', 'Non-Specific', 'non-permit operation'])
    CONDITION: 61 (e.g. ['car behind me was not focused and too close to me', 'new employee with regards to WAH requirements within TechnipFMC', 'Operator was not in the line of fire'])
    INJURY: 40 (e.g. ['slight: a first aid case, limited to no injury', 'Injury: upper torso', 'IP jarring his right shoulder'])
    ACTION: 35 (e.g. ['strenuous or repetitive movements', 'manual handling of lightning arrestor copper tape (50m length coil)', 'release of tension on the ratchet strap'])
    MATERIAL: 10 (e.g. ['empty food container and empty IBC', 'hot iron chip', 'damaged rollers'])
    PERSON: 7 (e.g. ['operator responsible for driving the wire was near', 'Leader and first aider', 'third party employee in the cell'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Equipment Suitability', 'Electrical', 'Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects)'])

  Community 2 (size=9993):
    INCIDENT: 3952 (e.g. ['INCIDENT 694162 - Flowback Tank sliding off of truck', 'ACCIDENT 619001 - Proper Damage Incident - SHELL Vito - Houston Gremp Campus- Indoor XT Storage - Chipped Paint on ROV Handle', 'ACCIDENT 9268 - Incident notification- First Aid-Theodore Spoolbase- Caesar Tonga- 21 July 2022- Slip trip- shoulder pain'])
    EQUIPMENT: 2374 (e.g. ['internet cable', 'main panel', 'communication cable'])
    LOCATION: 1622 (e.g. ['GLENROCK WY', 'second hole', 'Thistlethwaite Pad'])
    ORGANIZATION: 1060 (e.g. ['desanders', 'mancamp', 'The rental company'])
    BODY_PART: 337 (e.g. ['crossbody', 'driver side quarter panel', '2nd and 3rd knuckle'])
    EVENT: 299 (e.g. ['block tipping', 'hydraulic oil to be released', 'minor front end damage'])
    INJURY_TYPE: 142 (e.g. ['first aid abrasion', 'uncontrolled  pressure release', 'No injuries occurred'])
    CONDITION: 80 (e.g. ['swirling wind around the worksite', 'sleepiness', 'double knot on the rope came untied'])
    ACTION: 59 (e.g. ['disposed of', 'operator handle steel wire with his two hands along the machine', 'immediately used LO/TO'])
    INJURY: 41 (e.g. ['sharp pain on the right side of his back in the rib cage area', 'minor puncture wound to his right wrist', 'middle finger'])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['Hazard Identification & Risk Assessment', 'Planning and coordination of works', 'Animal Strike'])
    MATERIAL: 10 (e.g. ['piece of tie wire', 'thick gear oil (AtomOil Gear EP)', 'residual Oceanic HW 443 (Glycol/Antifreeze) fluid'])
    PERSON: 5 (e.g. ['Collaborators (two) third parties coming from home to work, walking along the side of a small bridge', 'Driver', 'Goods Inwards Inspector'])

  Community 3 (size=5416):
    INCIDENT: 1877 (e.g. ['ACCIDENT 616143 - Near Miss - Break a cutback machine head blade', 'NEAR MISS 24316 - Tombamento gradativo do cabideiro de i?amento.', 'NEAR MISS 10838 - Incidente - Desprendimento da Lingada do Guindaste (OS 006000651658 – JANELA SKVT: Recolhimento de linhas / 7-MRL-109H-RJS / P-33).'])
    EQUIPMENT: 1227 (e.g. ['main deck winch wire', 'stove', 'UEH'])
    LOCATION: 1001 (e.g. ['3/4 tube', 'Berbig?o', 'silicone container area'])
    ORGANIZATION: 706 (e.g. ['PSV Biguá', "West D'Or Hospital", 'CLP'])
    BODY_PART: 235 (e.g. ['prego', 'boca', 'm?o direita'])
    EVENT: 158 (e.g. ['bee stung', "projecting its parts around the table in the inside part of the machine's defect", 'directed to the medical ambulatory'])
    INJURY_TYPE: 110 (e.g. ['Nobody got hurt', 'shallow cut', 'strained ligament'])
    CONDITION: 33 (e.g. ['failure of the sling', 'slippery condition of the floor', 'stuck to the cat of the mouth'])
    INJURY: 33 (e.g. ['slightly cut the hand', 'cutting of minimum right finger', 'superficial injury in his index finger skin of left hand'])
    ACTION: 17 (e.g. ['slipping on the edge of the work platform step', 'not using gloves as required', 'immediate barriered off'])
    ROOT_CAUSE_CATEGORY: 13 (e.g. ['Information perceptiveness (amount / mode) & Information reception (extend / range)', 'Protection', 'Equipment condition'])
    MATERIAL: 4 (e.g. ['nylon parts (3 on main deck, one on the barge)', 'PVC connections, weighing a maximum of 0.65kg', 'concrete portion of the roof'])
    PERSON: 2 (e.g. ['people in the environment', 'operator in the face'])

  Community 4 (size=4178):
    INCIDENT: 1313 (e.g. ['ACCIDENT 565502 - FAC - Yamal LNG Project - Sabetta - 24.11.2017 - Forearm bruise', 'ACCIDENT 542788 - MTC - Yamal LNG Project - Sabetta - 16.06.2017 - Worker tripped and fell on a stairs', 'ACCIDENT 559137 - FAC - 034693C009 - Yamal LNG Project - Sabetta - 06.11.2017 - Contusion of the left shoulder joint'])
    LOCATION: 743 (e.g. ['EWP-51W Jetty', 'Belgium', 'Hanze'])
    EQUIPMENT: 639 (e.g. ['cable drum', 'Tadano ATF crane', 'PAB-100 Pipe Rack'])
    ORGANIZATION: 574 (e.g. ['Cuypers', 'Toyota', 'HSE Representatives'])
    INJURY_TYPE: 241 (e.g. ['Multiple facial graze-wound', 'bruised wound', 'bruised lumbosacral region'])
    BODY_PART: 237 (e.g. ['2nd phalanx', 'low bed', 'lower third'])
    EVENT: 187 (e.g. ['shards flying object penetrated the coverall of IP', 'PDQ tripped and twisted his ankle', 'industrial electric extension cord short circuit'])
    INJURY: 100 (e.g. ['frostbite of the fourth finger of the right hand', 'left ankle joint contusion', 'abdomen pain'])
    CONDITION: 65 (e.g. ['doormat elevation', 'hard barricade, which was not properly fixed', 'movements preserved'])
    ACTION: 61 (e.g. ['IP dropped flashlight', 'removal of safety pins', 'manual pulling of the pipe'])
    MATERIAL: 10 (e.g. ['sharp steel piece of the cargo', 'debris', 'small foreign body (most likely dust or a similar small particle)'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Falls, slips and trips on same level (without potential to fall to lower level)', 'Traffic Management / Routes / Pedestrian path', 'Explosives / potential explosives'])
    PERSON: 3 (e.g. ['REGA slinger', "IP's face", 'SNEMA wireman walking backwards'])

  Community 5 (size=3839):
    INCIDENT: 1477 (e.g. ['INCIDENT 660761 - PA-25/11/2019-Risque de colision avec véhicule exterieur', "ACCIDENT 553310 - IE - Le Trait - 13/09/2017 - Dépassement du seuil pour les MES sur le rejet d'eaux pluviales - Suspended material threshold exceeded on rain water release", 'INCIDENT 647950 - SD-Quai OSLT-15/08/2019- Tri non effectué'])
    EQUIPMENT: 756 (e.g. ['side roller', 'measuring device', 'SP10 valve'])
    LOCATION: 520 (e.g. ['consumable area', 'armed reception zone', 'Tie-In'])
    ORGANIZATION: 418 (e.g. ['tool service', 'PEUPLERAIE', 'companion'])
    BODY_PART: 176 (e.g. ['back', 'bichenille', 'pied droit'])
    EVENT: 175 (e.g. ['knife cut through the tip', 'IP falling backwards', 'electric arc'])
    INJURY_TYPE: 117 (e.g. ['type clous', 'knee pain', 'araladitis'])
    INJURY: 77 (e.g. ['laceration to his left palm and thumb', 'feeling pain behind his right knee', 'injury suffered'])
    ACTION: 57 (e.g. ['immediate stop of work', "hammer which was placed on a worker's belt got loose", 'shoveling sand from one side of a containment berm to another'])
    CONDITION: 47 (e.g. ['Emergency stop button for "Jumbo patrol man (on the floor)" out of order', 'no visible signs of injury', 'abnormal game on the removable platelage'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['Climate (Heat/Cold/Humidity)', 'Environment- Over-consumption of energy, natural resources (water, ...)', 'Psycho social - Workload (Overload/Underload)'])
    PERSON: 5 (e.g. ['informed to the HSE department and labor medicine', 'First Responder', 'SA protected by its helmet'])
    MATERIAL: 5 (e.g. ['the edge of the lid', 'red-colored water recovered in the network', 'waterized MUD'])

  Community 6 (size=3146):
    INCIDENT: 898 (e.g. ['INCIDENT 692614 - FAC_29092020_Right Hand Middle Finger got scratched with Cement Mixer', 'ACCIDENT 513469 - First Aid Case_064536C001 - Onshore Terminal for VA&S1 Development Project_Amalapuram_8/23/2016_Minor cut injury on knee by beam.', 'ACCIDENT 13419 - Cut injury index finger'])
    EQUIPMENT: 614 (e.g. ['level two cut rate gloves', 'insulation Cleat', 'impact resistant Gloves_x000D_'])
    LOCATION: 563 (e.g. ['ISBL', 'Plie no-10075', 'threshold'])
    ORGANIZATION: 330 (e.g. ['MAGMA GLOBAL LIMITED', 'maintenance workmen', 'AJAX FIORI'])
    EVENT: 287 (e.g. ['impact on the left hand', 'slipped from workmen’s hand', 'crane movement'])
    BODY_PART: 125 (e.g. ['IP leg', 'right side rear tire', 'buttocks'])
    CONDITION: 112 (e.g. ['handle retaining screw was loose', 'Isolation for the hydraulic was not closed', 'safety rail came into contact with his lower back'])
    INJURY_TYPE: 75 (e.g. ['internal injuries', 'multiple scratches and bruises', 'shear force'])
    ACTION: 63 (e.g. ['overhead grinding', 'removing his gloves', 'All stop has been called'])
    INJURY: 59 (e.g. ['scraping the shin of the employee', 'small cut to the index finger of his right hand', 'straining/pulling of hamstring'])
    MATERIAL: 12 (e.g. ['residual Oceanic 443', 'protruding strand of steel wire', 'discarded nail (with no head)'])
    PERSON: 5 (e.g. ['employee not stopping to check on employee', 'employee working on scaffold', 'Injured Person (IP)'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Accumulation / Presence of explosive atmosphere', 'Manual handling', 'Use of personal protective equipment'])

  Community 7 (size=3069):
    INCIDENT: 1035 (e.g. ['NEAR MISS 26041 - Sn?m?king p? platting uten for testomr?det.', 'ACCIDENT 18642 - Forklift struck bottom of the door', 'ACCIDENT 14066 - Cut finger with metal shaving'])
    EQUIPMENT: 770 (e.g. ['HTCU', 'pallet strap', 'hand trolly'])
    LOCATION: 492 (e.g. ['understairs area', 'building 90/1', 'Armaturbytte'])
    ORGANIZATION: 425 (e.g. ['Troll Phase', 'Aasta Hansteen Spar', 'doctor'])
    BODY_PART: 111 (e.g. ['wardrobe', 'hendene', 'distal joint'])
    EVENT: 95 (e.g. ["droplets of Tellus 22 hydraulic oil and possibly a small metal chip or swarf splashing into the operator's eye", 'cut tube gave 6.32 cps when cut', 'lifting straps caught the removable-top assembly'])
    INJURY_TYPE: 45 (e.g. ['slightly bruised', 'incident-injury', 'shock/pinch'])
    CONDITION: 37 (e.g. ['too heavy on one side', 'lack of control through the PTW system', 'operator was wearing all PPE for that particular activity'])
    INJURY: 28 (e.g. ['crushed fingertip', 'small blunt cut on the forehead', 'cut to above his left eye'])
    ACTION: 21 (e.g. ['Operator cleaned wound and put plaster/bandage to finger', 'failure to disconnect all the cables', 'repair to outer sheath to be carried out'])
    MATERIAL: 4 (e.g. ['steel chip', 'property and equipment were not damaged', 'no material damage was inflicted'])
    PERSON: 3 (e.g. ['deck rigging crew', 'person opening the door fast from another side without seeing me', 'emergency team on yard'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Radiation (ionising / non ionising)', 'Difficult/Hindered operability of tools and equipment', '1. Internal NCR (issued by TechnipFMC or Partners)'])

  Community 8 (size=2845):
    LOCATION: 668 (e.g. ['KP 141', 'Floq', 'Happy River'])
    INCIDENT: 659 (e.g. ['INCIDENT 726187 - FAC006-076971C - NEW NAPHTHA COMPLEX EPC - Greece-09.08.2021 – Scratch on the left leg with iron bar coming out from the demolished paving during manual excavation', 'ACCIDENT 546295 - NON-Technip Owned - BNJ-RWDC 07 - 2529 TAP - Greece/KP 374 - 24/07/2017 - Excavator struck a welder on the back with the bucket', 'NEAR MISS 605437 - NON Technip Owned - SCA-NM 65 - 2529 TAP - Albania/KP212 - 21/08/2018 - Wire rope for pulling the pipe snapped'])
    ORGANIZATION: 577 (e.g. ['Sparrows', 'HSS department', 'ARB Contractor'])
    EQUIPMENT: 495 (e.g. ['male snap station', 'telescopic forklift', 'retro sideboom'])
    EVENT: 174 (e.g. ['hole that penetrated the plate', 'burning of 50 sq.mm return lid of welding cable', 'tripped on a set of stairs'])
    CONDITION: 76 (e.g. ['uncompacted material which had been previously excavated and backfilled', 'Concerns had been raised previously regarding the supervisors safety performance', 'no face shield was worn'])
    BODY_PART: 52 (e.g. ['back of the neck', '4th_x000D_ finger', 'overhead line'])
    INJURY_TYPE: 46 (e.g. ['scratches/abrasion injuries', 'two stiches', 'minor finger laceration'])
    INJURY: 44 (e.g. ['laceration on the distal phalanx of right middle finger', 'blade cut IP’s left ring finger slightly through his gloves', 'hot water on the members right forearm'])
    ACTION: 40 (e.g. ['Ignoring the procedure', 'the welder did not handle properly the Stanley knife', 'IP flushed his eye out'])
    MATERIAL: 8 (e.g. ['fine sand', 'fuel materials that were inside the equipment', 'barbed wire made of elastic and cutting material'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Unfamiliar personnel', 'Inadequate Supervision', 'Illumination / sight / visibility'])
    PERSON: 2 (e.g. ['Nikita Chirko', 'the crew consisted of 1 supervisor, 2 excavator operators, 2 side boom operators'])

  Community 9 (size=1971):
    INCIDENT: 624 (e.g. ['NEAR MISS 27907 - Equipment drops from pallet.', 'NEAR MISS 30014 - Contractor Crane Hydraulic hose burst', 'NEAR MISS 562216 - Dolly Pile Ruptured'])
    EQUIPMENT: 444 (e.g. ['The exercises bike', 'pallet of "I" beams', 'end fitter'])
    LOCATION: 426 (e.g. ['Armouring 9 cage 2', 'Labuan', 'trench parameter'])
    ORGANIZATION: 285 (e.g. ['office staff', 'Regency General Hospital', 'insulation contractor'])
    EVENT: 64 (e.g. ['hydraulic oil spillage', 'bracket may fall at the staircase awning', 'weld was started'])
    BODY_PART: 55 (e.g. ['thumb nail', 'scaphoid bone', 'bottom body'])
    INJURY_TYPE: 30 (e.g. ['pinch laceration', 'LPG  leakage', 'D&A'])
    CONDITION: 18 (e.g. ['pressure gauge fitting defected because of wear and tear issue', 'improvised connection between a tube and mango inside the channel', 'earth core pulled out of the plug'])
    INJURY: 10 (e.g. ['personnel was in shock & experiencing hearing issues', 'sprained left ankle leg', 'pinched the tip of his thumb'])
    ACTION: 10 (e.g. ['Team Leader want to switch-on high-baylight', 'area secured', 'un-torqueing the torsion A-frame bolts using the pneumatic torqueing tool'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Psycho social - Alcohol and drugs abuse', 'Electrical current / electrocution / ESD / electromagnetic Fields', 'Weather Condition'])
    MATERIAL: 1 (e.g. ['wooden packing block'])
    PERSON: 1 (e.g. ['stray dog'])

  Community 10 (size=1921):
    INCIDENT: 643 (e.g. ["ACCIDENT 545027 - FAC - TU Ltd - 13/07/17 - IP's finger tip pinched between crane hook and spring return latch", 'ACCIDENT 18883 - IP slipped and fell on ice', "ACCIDENT 572905 - Occ Health - TU Ltd. - Hadrian House - 5.1.18 - Employee's asthma was made worse by cleaning chemicals"])
    EQUIPMENT: 532 (e.g. ['Brastec underollers', 'Visor', 'rotating equipment'])
    LOCATION: 288 (e.g. ['KGD6-5RS (4)', 'Drumstand 1', 'concentra'])
    ORGANIZATION: 241 (e.g. ['UT inspectIon', 'surgeons', 'Thermoplastic Umbilical Factory'])
    EVENT: 79 (e.g. ['milk bottles smashed', '0.74 gallons of hydraulic oil spilled', 'gate slamming down'])
    INJURY_TYPE: 43 (e.g. ['unspecific strain', 'graze and swelling', 'strained abdominal muscle'])
    BODY_PART: 38 (e.g. ['index and fore finger', 'shoulder height', 'one of his fingers'])
    CONDITION: 32 (e.g. ['human failure and a lapse of concentration, poor ergonomics and risk awareness', 'short of breath', 'existing back problems'])
    ACTION: 15 (e.g. ['releasing the lock at the top of the steps then the pins at the sides', 'manual pushing of the tipping skip', 'TOFS carried out by OCM'])
    INJURY: 9 (e.g. ['foreign object in eye', 'spraying one of our nearby Technip Apps tech on the side of his face', 'finger trapped between the door and the frame'])
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
**Type:** Global | **Status:** ✅ | **Time:** 0.5s

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
  LOCATION::Europe -- PR 0.012404
  LOCATION::North America -- PR 0.008548
  LOCATION::USA -- PR 0.007244
  LOCATION::UK -- PR 0.005515
  LOCATION::Asia Pacific -- PR 0.005191
  LOCATION::South America -- PR 0.003919
  LOCATION::Brazil -- PR 0.002947
  LOCATION::France -- PR 0.002630
  ORGANIZATION::TECHNIPFMC -- PR 0.002580
  LOCATION::Aberdeen -- PR 0.002106
  LOCATION::Norway -- PR 0.001819
  LOCATION::India -- PR 0.001494
  LOCATION::Africa -- PR 0.001369
  LOCATION::Russia -- PR 0.001351
  LOCATION::Houston -- PR 0.001335
  INJURY_TYPE::fire -- PR 0.001308
  LOCATION::Le Trait -- PR 0.001245
  LOCATION::India -- PR 0.001062
  LOCATION::Middle East -- PR 0.001054
  LOCATION::Malaysia -- PR 0.001002
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
  fracture: 7
  No one was injured: 7
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
  ankle: 4
  arm: 4
  eye: 4
  Knee: 3
  lower leg: 3
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
  abrasion: 12
  fracture: 12
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
  PLS deck tensioner control cabin -> personal injury: 1
  needle gun -> finger contusion: 1
  needle gun -> nails: 1
  paint scraper -> finger contusion: 1
  paint scraper -> nails: 1
  pedestal grinder -> finger contusion: 1
  pedestal grinder -> nails: 1
  scraper -> finger contusion: 1
  scraper -> nails: 1
```

### MH-03: Which clients have experienced vessel-related incidents resulting in back injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 47
Distinct ORGANIZATION values: 93
Top 10:
  OCM: 9
  TECHNIPFMC: 8
  HSE: 5
  HSEA: 5
  TECHNIP MARINE OPERATION SERVICES: 4
  IP: 4
  ISOS: 4
  WOODSIDE ENERGY LTD.: 4
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
    pain: 5
    abrasion: 5
    personal injuries: 4

  crane (622 incidents):
    injuries: 18
    fracture: 5
    abrasion: 4
    personal injury: 4
    personal injuries: 3

  ROV (290 incidents):
    personal injury: 3
    ferimentos pessoais: 2
    personnel injury: 1
    bruise: 1
    spraining: 1

  pallet (186 incidents):
    injuries: 5
    laceration: 3
    injury: 3
    cut: 2
    any type of injury: 1

  PPE (145 incidents):
    cut: 5
    wounds: 3
    fracture: 3
    bruise: 3
    contusion: 2
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
  Pontal do Parana: 2
  Litvinov: 2
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
  head: 10
  shoulder: 10
  thumb: 9
  arm: 9
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
  Argentina: 11
  Brazil: 11
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
  fracture: 4
  injury: 4
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