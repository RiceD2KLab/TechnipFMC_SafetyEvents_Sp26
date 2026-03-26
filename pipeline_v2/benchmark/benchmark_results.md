# L1 Benchmark Query Results

**Generated:** 2026-03-25
**Graph:** 100,407 nodes, 233,856 edges
**Records:** 19,820 metadata rows, 19,851 incident nodes
**Layer:** L1 + L2 (34,499 causal edges)

## 1. Summary Table

| ID | Query | Type | Status | Result |
|------|-------|------|:------:|--------|
| AG-01 | Root causes of dropped object incidents | Aggregation | ✅ | 1026 incidents, 43 root_cause_category values, top: Stored energy (dropped objects) |
| AG-02 | Countries with most high-severity incidents | Aggregation | ✅ | 167 incidents, 22 location values, top: USA |
| AG-03 | Most common equipment by incident count | Aggregation | ✅ | 19851 incidents, 13446 equipment values, top: forklift |
| AG-04 | Incident type x business unit crosstab | Aggregation | ✅ | Crosstab: 4 business_unit values x 3 incident_type values |
| AG-05 | Monthly trend of fall/slip incidents | Aggregation | ✅ | 1695 incidents across 110 months |
| AG-06 | Severity distribution by impact type | Aggregation | ✅ | Crosstab: 10 impact_type values x 6 severity_bin values |
| CJ-01 | Corrosion -> equipment failure -> fire (L2) | Conjunctive | ✅ | 34,499 causal edges; 800 for fire/explosion |
| CJ-02 | Crane + back + offshore + high severity | Conjunctive | ✅ | 0 incidents |
| CJ-03 | Maintenance fail + pipe + environmental + Middle East | Conjunctive | ✅ | 0 incidents |
| CJ-04 | Equipment: accident + near-miss same location/year | Conjunctive | ✅ | 539 dual-risk equipment/location/year combos |
| CJ-05 | Procedural -> dropped -> head/hand injury (L2) | Conjunctive | ✅ | 324 incidents; 12 procedural causal edges |
| CJ-06 | Falls/slips + vehicle + construction | Conjunctive | ✅ | 16 incidents |
| CJ-07 | Primary effects of corrosion (L2) | Conjunctive | ✅ | 137 corrosion causal edges across 104 incidents |
| GL-01 | Safety risk clusters (Louvain) | Global | ✅ | 11125 communities detected |
| GL-02 | Equipment recurring across regions | Global | ✅ | 144 equipment types span 5+ regions |
| GL-03 | Temporal trend of incident types | Global | ✅ | Crosstab: 10 year values x 3 incident_type values |
| GL-04 | Hub centrality analysis | Global | ✅ | Hub analysis: degree + PageRank top 20 |
| IOGP-01 | Moving vehicle/mobile equipment incidents | Aggregation | ✅ | 2008 incidents, 122 injury_type values, top: injuries |
| IOGP-02 | Dropped object incidents by severity | Aggregation | ✅ | Crosstab: 6 severity_bin values x 10 year values |
| IOGP-03 | Stored energy / snap-back incidents | Single-hop | ✅ | 114 incidents |
| IOGP-04 | Pressurized system incidents with containment loss | Multi-hop | ✅ | 192 incidents |
| IOGP-05 | Electrical incidents with LOTO failures (L2) | Conjunctive | ✅ | 142 incidents; 9 FAILED_CONTROL edges |
| IOGP-06 | Working at height incidents with fall protection gaps | Multi-hop | ✅ | 246 incidents, 76 body_part values, top: left hand |
| IOGP-07 | Mechanical lifting incidents with rigging failures | Multi-hop | ✅ | 2001 incidents, 152 injury_type values, top: injuries |
| IOGP-08 | Machinery/tools incidents with hand/finger injuries | Multi-hop | ✅ | 200 incidents |
| MH-01 | Equipment in containment->injury at offshore | Multi-hop | ✅ | 1 incidents, 2 equipment types |
| MH-02 | Injuries from equipment failures during maintenance | Multi-hop | ✅ | 29 incidents, 19 pairs |
| MH-03 | Clients with vessel + back injury | Multi-hop | ✅ | 47 incidents, 93 organization values, top: OCM |
| MH-04 | Top injury types per top-5 equipment | Multi-hop | ✅ | Injury breakdown for top 5 equipment |
| MH-05 | Hand + pipe + Asia Pacific | Multi-hop | ✅ | 6 incidents |
| MH-06 | Severity: trucks vs cranes | Multi-hop | ✅ | Truck vs crane severity comparison |
| MH-07 | Scaffold near-misses by location | Multi-hop | ✅ | 121 incidents, 33 location values, top: Sabetta |
| MH-08 | Hydraulic valve -> injury outcome | Multi-hop | ⚠️ | 1 incidents, 0 injury_type values |
| SC-01 | Spot-check: forklift mirror caught manifold (#623703) | Single-hop | ⚠️ | 1 items: ['forklift'] |
| SC-02 | Spot-check: electrical substation feeder fire (#570187) | Single-hop | ✅ | 3 items: ['Connector link', 'feeder box', 'feeder breaker'] |
| SC-03 | Spot-check: forklift hit PGB in yard (#602346) | Single-hop | ✅ | 2 items: ['PGB', 'forklift'] |
| SC-04 | Spot-check: press + back pain (#14338) | Single-hop | ✅ | 1 items: ['press'] |
| SC-04b | Spot-check: press + back pain body part (#14338) | Single-hop | ✅ | 1 items: ['lower back'] |
| SC-05 | Spot-check: ROV marker buoys dropped (#500389) | Single-hop | ✅ | 4 items: ['chain', 'football float', 'marker buoys', 'odom weight'] |
| SC-06 | Spot-check: fall + head cuts on barrier (#8712) | Single-hop | ✅ | 1 items: ['CEU 25 barrier'] |
| SC-06b | Spot-check: fall head cuts body parts (#8712) | Single-hop | ✅ | 3 items: ['face', 'forehead', 'head'] |
| SC-07 | Spot-check: wire sling + crane lip cut (#511771) | Single-hop | ✅ | 2 items: ['crane hook', 'wire rope sling'] |
| SC-07b | Spot-check: wire sling lip cut body part (#511771) | Single-hop | ✅ | 1 items: ['lower lip'] |
| SC-08 | Spot-check: forklift + truck collision (#324) | Single-hop | ✅ | 1 items: ['20T Forklift'] |
| SC-09 | Spot-check: crane exit + head cut (#18312) | Single-hop | ✅ | 2 items: ['crane', 'plastic sun visor'] |
| SC-09b | Spot-check: crane exit head cut body part (#18312) | Single-hop | ✅ | 1 items: ['head'] |
| SH-01 | Forklift incidents in 2022 | Single-hop | ✅ | 71 incidents |
| SH-02 | Equipment for incident #29857 | Single-hop | ⚠️ | 3 items: ['ROV', 'lanyard', 'pry bar'] |
| SH-03 | Body parts in crane incidents | Single-hop | ✅ | 1444 incidents, 192 body_part values, top: finger |
| SH-04 | Locations for valve incidents | Single-hop | ✅ | 387 incidents, 36 location values, top: USA |
| SH-05 | Injuries at offshore installations | Single-hop | ✅ | 1120 incidents, 124 injury_type values, top: cut |
| SH-06 | Incidents reported by Shell Offshore | Single-hop | ✅ | 60 incidents |

**Overall:** 49 ✅ passing / 3 ⚠️ failing out of 52 queries

## 2. Per-Query Details

### AG-01: Root causes of dropped object incidents
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

### AG-02: Countries with most high-severity incidents
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

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
  Australia: 3
  Canada: 3
  Malaysia: 3
```

### AG-03: Most common equipment by incident count
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
  machine: 93
  safety glasses: 93
  pump: 82
  truck: 81
  winch: 81
```

### AG-04: Incident type x business unit crosstab
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

### AG-05: Monthly trend of fall/slip incidents
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

### AG-06: Severity distribution by impact type
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

### CJ-01: Corrosion -> equipment failure -> fire (L2)
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

### CJ-02: Crane + back + offshore + high severity
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-03: Maintenance fail + pipe + environmental + Middle East
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 0
```

### CJ-04: Equipment: accident + near-miss same location/year
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

### CJ-05: Procedural -> dropped -> head/hand injury (L2)
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

### CJ-06: Falls/slips + vehicle + construction
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 16
Sample: ['INCIDENT::11732', 'INCIDENT::24216', 'INCIDENT::520161', 'INCIDENT::527205', 'INCIDENT::543663']
```

### CJ-07: Primary effects of corrosion (L2)
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

### GL-01: Safety risk clusters (Louvain)
**Type:** Global | **Status:** ✅ | **Time:** 8.4s

```
Total communities: 11125
Top 10 by size:

  Community 1 (size=10602):
    INCIDENT: 3177 (e.g. ['INCIDENT 696340 - Equipment Damage - 077290C003 - DUVA P1 - Deep Explorer - 03/11/2020 - Damage to 2" downline hose during recovery', 'ACCIDENT 579989 - Occupational Illness - G1201 – 05.04.2018 - 067821C001 – Crew member with heat related illness', 'INCIDENT 659815 - Environmental Incident- Warm Lay-up - Deep Energy - 18.11.2019 - Oil leak from FRC davit accumulator pressure gauge minimus test point adaptor.'])
    EQUIPMENT: 3017 (e.g. ['tank side valve', 'high bay hook', 'drier'])
    LOCATION: 1991 (e.g. ['Block 255', 'paint-shop area', 'Sliema'])
    ORGANIZATION: 1643 (e.g. ['Cabaca FM', 'Norsea base', 'Vessel Olympic'])
    BODY_PART: 259 (e.g. ['just above the knee', 'arc eye', 'wedding finger'])
    EVENT: 250 (e.g. ['discharge of one of the shells of the unit', 'empty to the basins is refused', 'gate valves dropped on the work desk and landed on the ground'])
    INJURY_TYPE: 105 (e.g. ['DSE assessment', 'head knock', '10mm contusion'])
    CONDITION: 61 (e.g. ['car behind me was not focused and too close to me', 'Pig isotope is still in the pipeline and is fully intact', 'welded onto a ‘No-Weld’ Zone'])
    INJURY: 40 (e.g. ['IP began to experience minor chest pain', 'small surface burns in the region of the stone', 'IP jarring his right shoulder'])
    ACTION: 35 (e.g. ['grinding on C-channel', 'crane operator approached the traffic police to get accident report', 'crane operator handle conteiners with the crane'])
    MATERIAL: 10 (e.g. ['empty food container and empty IBC', 'damaged rollers with the approximate weight of 34 grams each', 'leaked hydraulic fluid'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Stored energy (pressure, tension)', 'Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects)', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)'])
    PERSON: 7 (e.g. ['people in the radius of the fall of the pipes', 'third party employee in the cell', 'Rigging Supervisor being in charge of reel rotation'])

  Community 2 (size=9993):
    INCIDENT: 3952 (e.g. ['ACCIDENT 509322 - FAC - LCCP - 2016 - 09 - 06 (Insect Bite)', 'INCIDENT 648221 - Non-TFMC Owned - Spitzer HFD – BP Atlantis Phase 3 – Property Damage – Dropped Valve Crate – Low', 'ACCIDENT 596951 - Recordable injury - Stephenville - 7-10-18 - Left pinky finger laceration'])
    EQUIPMENT: 2374 (e.g. ['chickson', 'Panini press', 'fork attachments'])
    LOCATION: 1622 (e.g. ['5100 production aisle', 'pumps isle', 'secure screen'])
    ORGANIZATION: 1060 (e.g. ['Hunt', 'Stephenville fire department', 'APC'])
    BODY_PART: 337 (e.g. ['bottom corner', 'thumb_x000D_', 'valve stem'])
    EVENT: 299 (e.g. ['Genesis Facilities, QHSE and Legal team have had a meeting', 'tilting of the valve', 'block tipping'])
    INJURY_TYPE: 142 (e.g. ['insect/bug bite', 'dislocated arm', 'laceration'])
    CONDITION: 80 (e.g. ['frayed wire on bridge crane', 'pressure trapped', 'gloves were on hand, but not worn'])
    ACTION: 59 (e.g. ['could not move over any further', 'grab the side hard barricade', 'pulling on the hose'])
    INJURY: 41 (e.g. ['nauseas', 'small laceration located in the transition between the frontal lobe and top of skull', 'unable to stand on his own'])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['Computer workplaces / Screens', 'Animal Strike', 'Unprotected/unguarded moving machine parts (struck by/caught by)'])
    MATERIAL: 10 (e.g. ['strawberries that exceeded the ground', 'exposed rebar', 'material damage to the vehicle on the front'])
    PERSON: 5 (e.g. ['Collaborators (two) third parties coming from home to work, walking along the side of a small bridge', 'HSE manager on site and the facilities tech', 'Goods Inwards Inspector'])

  Community 3 (size=5416):
    INCIDENT: 1877 (e.g. ['ACCIDENT 640005 - Acidente de Trajeto na Flexibras', 'ACCIDENT 634768 - Duplicate case (Request to remove)', 'INCIDENT 695298 - LH PLáCIDO - Abalroamento do LH Plácido em embarca??o  AHTS'])
    EQUIPMENT: 1227 (e.g. ['16 Ton HYSPTER 360', '7 fun??es manipulator', 'MVT-01'])
    LOCATION: 1001 (e.g. ['safe path', 'Site', 'crossroads of the roadway'])
    ORGANIZATION: 706 (e.g. ['Konecranes Company', 'CSS', 'Hospital Geral Dr. Beda - Campos/RJ'])
    BODY_PART: 235 (e.g. ['mid-left', 'falanges', 'right facial region'])
    EVENT: 158 (e.g. ['slip during descent', 'control of the principle of fire', 'breakage of the wooden protection box'])
    INJURY_TYPE: 110 (e.g. ['surface cutting', 'mild activities', 'endem'])
    INJURY: 33 (e.g. ['Injury on left hypocondrium', 'closed fracture of the right ancle', 'turmoil on the right foot'])
    CONDITION: 33 (e.g. ['weight (approx. 12kg) pressing against the edge of the tub', 'loose soil at the edge', 'all the shrimp work requiring lifting is no longer permitted'])
    ACTION: 17 (e.g. ['daily medical follow-up', 'building management decided to stop the works', 'pressing the right finger between the bubble and the side of the shelter'])
    ROOT_CAUSE_CATEGORY: 13 (e.g. ['Unprotected/unguarded moving machine parts (struck by/caught by )', 'Information perceptiveness (amount / mode) & Information reception (extend / range)', 'Dangerous surfaces (sharp/ sharp edged/ high roughness grade)'])
    MATERIAL: 4 (e.g. ['PVC connections, weighing a maximum of 0.65kg', 'concrete pieces', 'concrete portion of the roof'])
    PERSON: 2 (e.g. ['people in the environment', 'operator in the face'])

  Community 4 (size=4178):
    INCIDENT: 1313 (e.g. ['ACCIDENT 524383 - Recordable non-Technip owned-  PDVSA APS PAGMI - Guiria Venezuela - 01/30/2017 - IP stepped on a bundle of rebar and lost his balance but did not fall to ground - sprain right ankle', 'INCIDENT 739099 - First Aid 083 - MIDOR - Egypt - 5.18.2021 - PTJ grinder with Aneurysm and consequent cardiac arrest - TCF Area C', 'ACCIDENT 564761 - FAC - Yamal LNG Project - Sabetta - 20.06.2017 - Leg contusion'])
    LOCATION: 743 (e.g. ['4th tier', '3-rd level medical post of s. Sabetta', 'Diamantgracht'])
    EQUIPMENT: 639 (e.g. ['Personal Protective Equipment', 'angle grinder', 'KAMAZ truck bed'])
    ORGANIZATION: 574 (e.g. ['FMSi Eurasia', 'The gritting service company', 'ENPPI'])
    INJURY_TYPE: 241 (e.g. ['drowsy', 'without dislocation', 'IP damaged ligaments'])
    BODY_PART: 237 (e.g. ['IPs right hand', 'footstep', 'left shoulder_x000D_'])
    EVENT: 187 (e.g. ['accidentally hit himself in the chest with a plank', 'twisted his left foot', "admitted to the vessel's infirmary"])
    INJURY: 100 (e.g. ['closed fracture of proximal phalanx of the second finger of the left hand', 'burn to his nose and inside his mouth', 'laceration of the right shin'])
    CONDITION: 65 (e.g. ['no fracture has been occurred', 'particle in his right eye', 'genetic predisposition of the IP toward this genetic illness'])
    ACTION: 61 (e.g. ['stumbled over a step of the stairs', 'did not report anything', 'tripped over a junction box support'])
    MATERIAL: 10 (e.g. ['3 palettes containing in all 14 leaf crowns', 'sharp steel piece of the cargo', 'small foreign body (most likely dust or a similar small particle)'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Traffic Management / Routes / Pedestrian path', 'Explosives / potential explosives', 'Fall to lower level / fall to water / loose materials (e.g. silos with granulate)'])
    PERSON: 3 (e.g. ["IP's face", 'REGA slinger', 'SNEMA wireman walking backwards'])

  Community 5 (size=3839):
    INCIDENT: 1477 (e.g. ['INCIDENT 691358 - SB-NM-RG150-14/09/20- Douleur au dos suite à un trébuchement', 'NEAR MISS 628067 - IE - Panier 6 - 08/03/19 - Déversement accidentel de glycol lors du remplissage du flexible', 'NEAR MISS 569724 - Near Miss - Astrazeneca - 22/12/17 - Fuite au réseau eau chaude au 7.70'])
    EQUIPMENT: 756 (e.g. ['Compactor', 'SmartBoard', 'outer belt'])
    LOCATION: 520 (e.g. ['stairs', 'Marseille', 'B100D boiler'])
    ORGANIZATION: 418 (e.g. ['monters', 'PETROINEOS', 'The B team'])
    BODY_PART: 176 (e.g. ['heart coat', 'tête', 'vision'])
    EVENT: 175 (e.g. ['smell of glycol', 'hand pinched between the come-a-long chain and mud mat', 'fell on the shoulder'])
    INJURY_TYPE: 117 (e.g. ['middle finger fracture', 'HSE strain', 'unleveled'])
    INJURY: 77 (e.g. ['laceration to his left palm and thumb', 'pain in the lower back', 'limited movement in left thumb'])
    ACTION: 57 (e.g. ['removal of floor boards', 'reporting to the vessel medic', 'de-tension of jacks which included hand tightening/ loosening the bolts onto the flange'])
    CONDITION: 47 (e.g. ['unsorted waste, no traceability of the waste', 'knee displacement (twist in his knee)', 'conditioned at the supplier with mouth'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['Psycho social - Workload (Overload/Underload)', 'Environment- Over-consumption of energy, natural resources (water, ...)', 'Climate (Heat/Cold/Humidity)'])
    PERSON: 5 (e.g. ['First Responder', 'SA protected by its helmet', 'employee'])
    MATERIAL: 5 (e.g. ['waterized MUD', 'the edge of the lid', 'particle of weld bark'])

  Community 6 (size=3146):
    INCIDENT: 898 (e.g. ['ACCIDENT 562217 - Restricted Work Case (RWC)_ XXXX - Non Project Specific_12/5/2017_Dahej_', 'ACCIDENT 515512 - First aid Case_064536C001 - Onshore Terminal for VA&S1 Development Project_amalapuram_11/1/2016_During the material handling fell down and minor cut injury on lip', 'ACCIDENT 29527 - Minor cut during the handling of material in warehouse'])
    EQUIPMENT: 614 (e.g. ['manual wrench tool', 'Portable electrode oven', 'press machine'])
    LOCATION: 563 (e.g. ['TS- 3', 'HGU plot area', 'Training hall'])
    ORGANIZATION: 330 (e.g. ['RISING FACILITY MANAGEMENT', 'VN Nursing home', 'Tankage subcontractor'])
    EVENT: 287 (e.g. ['fall partly into the hole', 'former falling to the floor', 'minor oil spill'])
    BODY_PART: 125 (e.g. ['fingertip', 'external side', 'ear and neck'])
    CONDITION: 112 (e.g. ['warm reach rod', 'tight scratch', 'impact of temporary support'])
    INJURY_TYPE: 75 (e.g. ['nobody was harmed', 'near miss incident', 'pinch'])
    ACTION: 63 (e.g. ['locks release', 'pulled the tape', 'removing percolator from the coffee machine'])
    INJURY: 59 (e.g. ['10cm cut on his leg', 'minor laceration on the ring finger of the right hand', 'contusion of lower back tissues'])
    MATERIAL: 12 (e.g. ['residual Oceanic 443', 'absorbents', 'hydraulic fluid on the ground'])
    PERSON: 5 (e.g. ['Person: Samsaliev Sakish of REGA JV', 'Injured Person (IP)', 'employee working on scaffold'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Use of personal protective equipment', 'Manual handling', 'Accumulation / Presence of explosive atmosphere'])

  Community 7 (size=3069):
    INCIDENT: 1035 (e.g. ['INCIDENT 677603 - 6L stab hoppet ut av receptackle med trykk p?', 'ACCIDENT 641500 - DO building 16 pallet with SLT dropped from 2nd shelf', 'ACCIDENT 1168 - First Aid Treatment (FAT) - OSB - Burn mark on arm just after welding'])
    EQUIPMENT: 770 (e.g. ['flat rack', 'Stem Adapter', 'H-frame 6'])
    LOCATION: 492 (e.g. ['dock hall', 'red/white barrier', 'grinding/welding room'])
    ORGANIZATION: 425 (e.g. ['Quinta Incência', 'Police Security Service', 'CCB'])
    BODY_PART: 111 (e.g. ['halvbukken', 'huden', 'turning wheel'])
    EVENT: 95 (e.g. ['Medical service provider opened the wound', "worker's hand slipped from the spanner", 'incident was classified as a Hazard Observation'])
    INJURY_TYPE: 45 (e.g. ['loss of sight', 'incident-injury', 'Nobody was injured'])
    CONDITION: 37 (e.g. ['stress level peaked', 'no people were present', 'amount and variation of work on this project'])
    INJURY: 28 (e.g. ['no trauma caused on hand or fingers', 'contamination of Dave’s hands', 'No permanent injury to personnel'])
    ACTION: 21 (e.g. ['required 4-5 stitches', 'use of finger instead of measuring stick', 'Action: He was then told to switch off and lock the tableau in cabinet'])
    MATERIAL: 4 (e.g. ['aluminum', 'steel chip', 'no material damage was inflicted'])
    PERSON: 3 (e.g. ['person opening the door fast from another side without seeing me', 'emergency team on yard', 'deck rigging crew'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Radiation (ionising / non ionising)', 'Difficult/Hindered operability of tools and equipment', '1. Internal NCR (issued by TechnipFMC or Partners)'])

  Community 8 (size=2845):
    LOCATION: 668 (e.g. ['KP 215', 'KP 201', 'Roskovec'])
    INCIDENT: 659 (e.g. ['ACCIDENT 560554 - NON Technip Owned - SCA-FAC 08 - 2529 TAP - Albania/ACS03 - 13/11/2017 -  Worker stung by bee', 'ACCIDENT 618600 - NON Technip Owned - RNT-FAC 12 - 2529 TAP - Albania/ACS03 - 11/12/2018- Worker received a bruise on the leg while performing pipe jacking activity.', 'NEAR MISS 559023 - NON-Technip Owned - BNJ-NM 17 - 2529 TAP Project - Greece/KP 239 -31/10/2017 - Worker walked on pipe'])
    ORGANIZATION: 577 (e.g. ['UG  GRE', 'MOTOR OIL (HELLAS) CORINTH REFINERIES S.A.', 'HIPO'])
    EQUIPMENT: 495 (e.g. ['Dynamic Risk Assessment', 'Flash arrest valves', 'dead man’s handle'])
    EVENT: 174 (e.g. ['blasting activities on a nearby working area', 'some portion of welding cable got burnt', 'A proper JSA was not conducted'])
    CONDITION: 76 (e.g. ['left trench slope inclination off limits (60o instead of 53o max)', 'no one from TechnipFMC accompanying', 'Side-boom transmission problem'])
    BODY_PART: 52 (e.g. ['lower lip', 'right eyebrow area', 'burned fingertips'])
    INJURY_TYPE: 46 (e.g. ['serious injury', 'minor neck strain', 'pelvis fracture'])
    INJURY: 44 (e.g. ['minor burn on employees face', 'small cut on the middle finger', 'hot water on the members right forearm'])
    ACTION: 40 (e.g. ['worker had conducted a cut and placed the knife into his right pocket. He did not fully retract the blade', 'fitter did not notice', 'working off of third step'])
    MATERIAL: 8 (e.g. ['fine sand', 'grease from overhead conveyor chain', 'burn cream from first aid room'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Unfamiliar personnel', 'Illumination / sight / visibility', 'Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)'])
    PERSON: 2 (e.g. ['Nikita Chirko', 'the crew consisted of 1 supervisor, 2 excavator operators, 2 side boom operators'])

  Community 9 (size=1971):
    INCIDENT: 624 (e.g. ['INCIDENT 694829 - PD - APSB - A9 - 16/10/2020 - Wire pulling winch damaged', 'NEAR MISS 14274 - Near Miss Electrical Tripped at QC Hub', 'ACCIDENT 537655 - PD - OUI JV Rapid - Pengerang, Johor - 3 May 2017 - Whilst performing offloading of a cable drum form a delivery truck, the drum fell from the forks to the ground, damaging the cable drum'])
    EQUIPMENT: 444 (e.g. ['auto lock system', 'bending tool equipment', 'CPU'])
    LOCATION: 426 (e.g. ['Port Klang', 'manufacturing canteen', 'grating surface'])
    ORGANIZATION: 285 (e.g. ['URSA management team', 'LIU HUA TR21', 'Mudajaya 1900 workers village'])
    EVENT: 64 (e.g. ['the employee’s right index finger made contact with the wire wheel', 'oil overflow from IBC tank', 'Incident has been report to maintenance'])
    BODY_PART: 55 (e.g. ['head area', 'glove protected finger', 'middle phanlax bone'])
    INJURY_TYPE: 30 (e.g. ['MRI scan', 'minor puncture cut', 'claning activity'])
    CONDITION: 18 (e.g. ['not flowing into the domestic drain', 'possible weld failure', 'minor dented on Long Boring Bar body'])
    ACTION: 10 (e.g. ['bandage was applied on the injured knee to support to injury', 'un-torqueing the torsion A-frame bolts using the pneumatic torqueing tool', 'scaffold jack base used as a hammer'])
    INJURY: 10 (e.g. ['bitten on the leg', 'bent the thumbnail back', 'suffering pain in his right knee'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Weather Condition', 'Electrical current / electrocution / ESD / electromagnetic Fields', 'Psycho social - Alcohol and drugs abuse'])
    MATERIAL: 1 (e.g. ['wooden packing block'])
    PERSON: 1 (e.g. ['stray dog'])

  Community 10 (size=1921):
    INCIDENT: 643 (e.g. ['ACCIDENT 529733 - NWR/RWC-TU Inc-17.03.09- Back pain', 'INCIDENT 651288 - ENV - TUL - IBC punctured with tip of fork on forklift truck resulting in release of glycol/water mix - 10.9.19', 'ACCIDENT 529808 - NWR/MTI-TU Inc.-17.03.08- IP complaining of back pain'])
    EQUIPMENT: 532 (e.g. ['Brastec underollers', 'EKG', 'tilt'])
    LOCATION: 288 (e.g. ['insulation booth', 'clamp area', 'old stores area'])
    ORGANIZATION: 241 (e.g. ['Lord Hire', 'Maintenance and Wood Electric', 'Fin Power'])
    EVENT: 79 (e.g. ['slipping off falling down between the guards and the cat pads', 'prescribed heartburn medicine and released him for a full return to work', 'Restricted duty for 24hrs'])
    INJURY_TYPE: 43 (e.g. ['slightly lacerated', 'nick', 'nip injury'])
    BODY_PART: 38 (e.g. ['right hand knuckle', 'rear of the cab', 'elbow area'])
    CONDITION: 32 (e.g. ['smooth surface on the concrete', 'human failure and a lapse of concentration, poor ergonomics and risk awareness', 'unsuspected gust of strong wind'])
    ACTION: 15 (e.g. ['operator accidentally bumped the down lever', 'Extinguished by C02 fire extinguisher', "Operator was looking up and didn't notice the chain hook caught the fixture table"])
    INJURY: 9 (e.g. ['spraying one of our nearby Technip Apps tech on the side of his face', 'sheath damage', 'no personal were affected'])
    PERSON: 1 (e.g. ['gangway watchman was in place'])
```

### GL-02: Equipment recurring across regions
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

### GL-03: Temporal trend of incident types
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

### GL-04: Hub centrality analysis
**Type:** Global | **Status:** ✅ | **Time:** 7.4s

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

### IOGP-02: Dropped object incidents by severity
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

### IOGP-03: Stored energy / snap-back incidents
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 114
Sample: ['INCIDENT::10888', 'INCIDENT::12332', 'INCIDENT::12630', 'INCIDENT::12715', 'INCIDENT::13227']
```

### IOGP-04: Pressurized system incidents with containment loss
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 192
Sample: ['INCIDENT::10674', 'INCIDENT::10923', 'INCIDENT::10992', 'INCIDENT::11942', 'INCIDENT::12909']
```

### IOGP-05: Electrical incidents with LOTO failures (L2)
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

### IOGP-06: Working at height incidents with fall protection gaps
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 246
Distinct BODY_PART values: 76
Top 10:
  left hand: 15
  shoulder: 10
  left foot: 10
  left leg: 8
  arm: 4
  eye: 4
  ankle: 4
  Knee: 3
  lower leg: 3
  wrist: 3
```

### IOGP-07: Mechanical lifting incidents with rigging failures
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2001
Distinct INJURY_TYPE values: 152
Top 10:
  injuries: 51
  injury: 15
  laceration: 15
  cut: 14
  personal injury: 12
  fracture: 12
  abrasion: 12
  contusion: 9
  personnel injury: 6
  pain: 6
```

### IOGP-08: Machinery/tools incidents with hand/finger injuries
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 200
Sample: ['INCIDENT::10299', 'INCIDENT::10348', 'INCIDENT::10636', 'INCIDENT::10759', 'INCIDENT::10789']
```

### MH-01: Equipment in containment->injury at offshore
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

### MH-02: Injuries from equipment failures during maintenance
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 29
EQUIPMENT->INJURY_TYPE pairs (top 10):
  whip check -> personal injury: 2
  actuator box -> static electric shock: 1
  gusset plate -> static electric shock: 1
  engine room water pump -> minor burn: 1
  induction heater -> minor burn: 1
  PLS deck tensioner control cabin -> personal injury: 1
  needle gun -> finger contusion: 1
  needle gun -> nails: 1
  paint scraper -> finger contusion: 1
  paint scraper -> nails: 1
```

### MH-03: Clients with vessel + back injury
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 47
Distinct ORGANIZATION values: 93
Top 10:
  OCM: 9
  TECHNIPFMC: 8
  HSEA: 5
  HSE: 5
  IP: 4
  TECHNIP MARINE OPERATION SERVICES: 4
  WOODSIDE ENERGY LTD.: 4
  ISOS: 4
  PETROBRAS: 3
  ENQUEST BRITAIN LTD.: 3
```

### MH-04: Top injury types per top-5 equipment
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

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
    personal injuries: 3

  ROV (290 incidents):
    personal injury: 3
    ferimentos pessoais: 2
    injury: 1
    incident categorisation: 1
    FA case: 1

  pallet (186 incidents):
    injuries: 5
    injury: 3
    laceration: 3
    cut: 2
    smashed finger: 1

  PPE (145 incidents):
    cut: 5
    wounds: 3
    bruise: 3
    fracture: 3
    Chemical burn: 2
```

### MH-05: Hand + pipe + Asia Pacific
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 6
Sample: ['INCIDENT::10789', 'INCIDENT::522669', 'INCIDENT::526879', 'INCIDENT::547023', 'INCIDENT::571988']
```

### MH-06: Severity: trucks vs cranes
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

### MH-07: Scaffold near-misses by location
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 121
Distinct LOCATION values: 33
Top 10:
  Sabetta: 12
  Aberdeen: 9
  Dubai: 9
  Baku: 5
  Amalapuram: 4
  Qidong: 4
  Panipat: 3
  Abu Dhabi: 3
  Anvers: 2
  Rio de Janeiro: 2
```

### MH-08: Hydraulic valve -> injury outcome
**Type:** Multi-hop | **Status:** ⚠️ | **Time:** 0.2s

```
Matching incidents: 1
Distinct INJURY_TYPE values: 0
Top 10:
```

### SC-01: Spot-check: forklift mirror caught manifold (#623703)
**Type:** Single-hop | **Status:** ⚠️ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::623703: ['forklift']
Ground truth: ['forklift', 'manifold', 'mirror']
Missing: ['manifold', 'mirror']
Extra (unexpected): none
```

### SC-02: Spot-check: electrical substation feeder fire (#570187)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::570187: ['Connector link', 'feeder box', 'feeder breaker']
Ground truth: ['connector link', 'feeder box', 'feeder breaker']
Missing: none
Extra (unexpected): none
```

### SC-03: Spot-check: forklift hit PGB in yard (#602346)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::602346: ['PGB', 'forklift']
Ground truth: ['forklift', 'pgb']
Missing: none
Extra (unexpected): none
```

### SC-04: Spot-check: press + back pain (#14338)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::14338: ['press']
Ground truth: ['press']
Missing: none
Extra (unexpected): none
```

### SC-04b: Spot-check: press + back pain body part (#14338)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::14338: ['lower back']
Ground truth: ['lower back']
Missing: none
Extra (unexpected): none
```

### SC-05: Spot-check: ROV marker buoys dropped (#500389)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::500389: ['chain', 'football float', 'marker buoys', 'odom weight']
Ground truth: ['chain', 'football float', 'marker buoys', 'odom weight', 'tms']
Missing: ['tms']
Extra (unexpected): none
```

### SC-06: Spot-check: fall + head cuts on barrier (#8712)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::8712: ['CEU 25 barrier']
Ground truth: ['ceu 25 barrier']
Missing: none
Extra (unexpected): none
```

### SC-06b: Spot-check: fall head cuts body parts (#8712)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::8712: ['face', 'forehead', 'head']
Ground truth: ['face', 'forehead', 'head']
Missing: none
Extra (unexpected): none
```

### SC-07: Spot-check: wire sling + crane lip cut (#511771)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::511771: ['crane hook', 'wire rope sling']
Ground truth: ['crane hook', 'wire rope sling']
Missing: none
Extra (unexpected): none
```

### SC-07b: Spot-check: wire sling lip cut body part (#511771)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::511771: ['lower lip']
Ground truth: ['lower lip']
Missing: none
Extra (unexpected): none
```

### SC-08: Spot-check: forklift + truck collision (#324)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::324: ['20T Forklift']
Ground truth: ['20t forklift']
Missing: none
Extra (unexpected): none
```

### SC-09: Spot-check: crane exit + head cut (#18312)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::18312: ['crane', 'plastic sun visor']
Ground truth: ['crane', 'plastic sun visor']
Missing: none
Extra (unexpected): none
```

### SC-09b: Spot-check: crane exit head cut body part (#18312)
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::18312: ['head']
Ground truth: ['head']
Missing: none
Extra (unexpected): none
```

### SH-01: Forklift incidents in 2022
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 71
Sample: ['INCIDENT::10170', 'INCIDENT::10252', 'INCIDENT::10333', 'INCIDENT::1061', 'INCIDENT::1069']
```

### SH-02: Equipment for incident #29857
**Type:** Single-hop | **Status:** ⚠️ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::29857: ['ROV', 'lanyard', 'pry bar']
Ground truth: ['lanyard', 'pry bar', 'rov', 'tms']
Missing: ['tms']
Extra (unexpected): none
```

### SH-03: Body parts in crane incidents
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
  thumb: 9
  arm: 9
  eye: 8
  forearm: 7
```

### SH-04: Locations for valve incidents
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

### SH-05: Injuries at offshore installations
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
  fracture: 4
  bruising: 4
  injury: 4
```

### SH-06: Incidents reported by Shell Offshore
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 60
Sample: ['INCIDENT::100', 'INCIDENT::1039', 'INCIDENT::11906', 'INCIDENT::12463', 'INCIDENT::12507']
```

## 3. Failing Queries

- **MH-08** (Hydraulic valve -> injury outcome): 1 incidents, 0 injury_type values
- **SC-01** (Spot-check: forklift mirror caught manifold (#623703)): 1 items: ['forklift']
- **SH-02** (Equipment for incident #29857): 3 items: ['ROV', 'lanyard', 'pry bar']

## 4. Regression Diff (vs previous run)

No regressions — all results stable.

---
*Generated by pipeline_v2/benchmark/run_benchmark.py*