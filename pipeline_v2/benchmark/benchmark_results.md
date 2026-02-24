# L1 Benchmark Query Results

**Generated:** 2026-02-23
**Graph:** 61,545 nodes, 202,141 edges
**Records:** 19,820 metadata rows, 19,820 incident nodes
**Layer:** L1 only (pre-ER, pre-Layer 2 causal enrichment)

## 1. Summary Table

| ID | Query | Type | Coverage | Result | Diagnosis |
|------|-------|------|:--------:|--------|-----------|
| AG-01 | Root causes of dropped object incidents | Aggregation | ✅ | 1026 incidents, 68 root_cause_category values, top: Mechanical - Stored energy (dropped objects) | CLEAN |
| AG-02 | Countries with most high-severity incidents | Aggregation | ✅ | 167 incidents, 22 location values, top: USA | CLEAN |
| AG-03 | Most common equipment by incident count | Aggregation | ✅ | 19820 incidents, 15158 equipment values, top: forklift | ER_NEEDED |
| AG-04 | Incident type x business unit crosstab | Aggregation | ⚠️ | Crosstab: 4 business_unit values x 3 incident_type values | DATA_SPARSE |
| AG-05 | Monthly trend of fall/slip incidents | Aggregation | ✅ | 1695 incidents across 110 months | CLEAN |
| AG-06 | Severity distribution by impact type | Aggregation | ✅ | Crosstab: 10 impact_type values x 6 severity_bin values | CLEAN |
| CJ-01 | Corrosion -> equipment failure -> fire (L2) | Conjunctive | ❌ | 0 causal edges; approximate: 0 incidents | L2_REQUIRED |
| CJ-02 | Crane + back + offshore + high severity | Conjunctive | ⚠️ | 0 incidents | DATA_SPARSE |
| CJ-03 | Maintenance fail + pipe + environmental + Middle East | Conjunctive | ⚠️ | 0 incidents | DATA_SPARSE |
| CJ-04 | Equipment: accident + near-miss same location/year | Conjunctive | ✅ | 548 dual-risk equipment/location/year combos | CLEAN |
| CJ-05 | Procedural -> dropped -> head/hand injury (L2) | Conjunctive | ⚠️ | 4 incidents | L2_REQUIRED |
| CJ-06 | Falls/slips + vehicle + construction | Conjunctive | ✅ | 15 incidents | CLEAN |
| GL-01 | Safety risk clusters (Louvain) | Global | ✅ | 40 communities detected | CLEAN |
| GL-02 | Equipment recurring across regions | Global | ✅ | 123 equipment types span 5+ regions | ER_NEEDED |
| GL-03 | Temporal trend of incident types | Global | ✅ | Crosstab: 10 year values x 3 incident_type values | CLEAN |
| GL-04 | Hub centrality analysis | Global | ✅ | Hub analysis: degree + PageRank top 20 | CLEAN |
| MH-01 | Equipment in containment->injury at offshore | Multi-hop | ⚠️ | 1 incidents, 2 equipment types | CLEAN |
| MH-02 | Injuries from equipment failures during maintenance | Multi-hop | ✅ | 29 incidents, 19 pairs | CLEAN |
| MH-03 | Clients with vessel + back injury | Multi-hop | ❌ | 0 incidents, 0 organization values | ER_NEEDED |
| MH-04 | Top injury types per top-5 equipment | Multi-hop | ✅ | Injury breakdown for top 5 equipment | ER_NEEDED |
| MH-05 | Hand + pipe + Asia Pacific | Multi-hop | ✅ | 6 incidents | CLEAN |
| MH-06 | Severity: trucks vs cranes | Multi-hop | ✅ | Truck vs crane severity comparison | ER_NEEDED |
| MH-07 | Scaffold near-misses by location | Multi-hop | ✅ | 115 incidents, 36 location values, top: zObsolete - Trinidad | ER_NEEDED |
| MH-08 | Hydraulic valve -> injury outcome | Multi-hop | ⚠️ | 3 incidents, 0 injury_type values | ER_NEEDED |
| SH-01 | Forklift incidents in 2022 | Single-hop | ✅ | 73 incidents | ER_NEEDED |
| SH-02 | Equipment for incident #29857 | Single-hop | ⚠️ | 3 items: ['ROV', 'lanyard', 'pry bar'] | EXTRACTION_GAP |
| SH-03 | Body parts in crane incidents | Single-hop | ✅ | 1444 incidents, 247 body_part values, top: left hand | ER_NEEDED |
| SH-04 | Locations for valve incidents | Single-hop | ✅ | 386 incidents, 37 location values, top: USA | ER_NEEDED |
| SH-05 | Injuries at offshore installations | Single-hop | ✅ | 1120 incidents, 153 injury_type values, top: personal injury | CLEAN |
| SH-06 | Incidents reported by Shell Offshore | Single-hop | ✅ | 60 incidents | ER_NEEDED |

**Overall:** 21 ✅ FULL / 7 ⚠️ PARTIAL / 2 ❌ FAIL out of 30 queries

**Diagnosis breakdown:**
- CLEAN: 13
- ER_NEEDED: 11
- DATA_SPARSE: 3
- L2_REQUIRED: 2
- EXTRACTION_GAP: 1

## 2. Per-Query Details

### AG-01: Root causes of dropped object incidents
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 1026
Distinct ROOT_CAUSE_CATEGORY values: 68
Top 10:
  Mechanical - Stored energy (dropped objects): 265
  Stored energy (dropped objects): 102
  Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 94
  Basic Organizational - Hazard Identification & Risk Assessment: 51
  Mechanical - Equipment condition: 44
  Work environment - Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 36
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 35
  Basic Organizational - Planning and coordination of works: 30
  Ergonomics - Manual handling: 24
  Basic Organisational - Equipment Suitability: 22
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
  Canada: 3
  Australia: 3
  Malaysia: 3
  Angola: 3
```

### AG-03: Most common equipment by incident count
**Type:** Aggregation | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 19820
Distinct EQUIPMENT values: 15158
Top 20:
  forklift: 734
  crane: 620
  ROV: 279
  pallet: 170
  excavator: 140
  PPE: 139
  equipment: 125
  overhead crane: 104
  machine: 93
  safety glasses: 91
  reel: 89
  forks: 84
  gloves: 83
  grinder: 78
  fire extinguisher: 78
  truck: 77
  winch: 77
  pump: 76
  trailer: 74
  XT: 68
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
**Type:** Conjunctive | **Coverage:** ❌ | **Diagnosis:** L2_REQUIRED | **Time:** 0.0s

```
Causal edges in graph: 0 (EXPECTED: 0)
⚠️ True causal chain query CANNOT be answered at L1

Approximate fallback (narrative 'corrosion' intersection fire/explosion RCC):
  Corrosion narratives: 37
  Fire/explosion RCC values: ['Flammable solids, liquids and gases', 'Fire & Explosion - Uncontrolled chemical or physical reaction', 'Fire & Explosion - Accumulation / Presence of explosive atmosphere', 'Fire & Explosion - Flammable solids, liquids and gases', 'Fire & Explosion - Explosives / potential explosives']
  Fire/explosion incidents: 460
  Intersection: 0
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
Dual-risk (accident + near-miss at same location/year): 548 combos
Top 10:
  crane @ Aberdeen (2017): 10 accidents, 19 near-misses
  ROV @ Aberdeen (2018): 22 accidents, 7 near-misses
  forklift @ Houston (2018): 15 accidents, 10 near-misses
  crane @ Aberdeen (2024): 10 accidents, 12 near-misses
  crane @ Aberdeen (2016): 16 accidents, 6 near-misses
  ROV @ Aberdeen (2017): 14 accidents, 7 near-misses
  forklift @ Houston (2023): 4 accidents, 13 near-misses
  crane @ Aberdeen (2018): 12 accidents, 5 near-misses
  excavator @ zObsolete - Athens (2018): 11 accidents, 6 near-misses
  crane @ Aberdeen (2022): 10 accidents, 6 near-misses
```

### CJ-05: Procedural -> dropped -> head/hand injury (L2)
**Type:** Conjunctive | **Coverage:** ⚠️ | **Diagnosis:** L2_REQUIRED | **Time:** 0.1s

```
Matching incidents: 4
Sample: ['INCIDENT::510452', 'INCIDENT::588198', 'INCIDENT::593157', 'INCIDENT::672903']
```

### CJ-06: Falls/slips + vehicle + construction
**Type:** Conjunctive | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.1s

```
Matching incidents: 15
Sample: ['INCIDENT::11732', 'INCIDENT::24216', 'INCIDENT::520161', 'INCIDENT::543663', 'INCIDENT::549789']
```

### GL-01: Safety risk clusters (Louvain)
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 4.8s

```
Total communities: 40
Top 10 by size:

  Community 1 (size=10724):
    EQUIPMENT: 3415 (e.g. ['HOM', 'U Mats', 'Thruster no 3'])
    INCIDENT: 2939 (e.g. ['NEAR MISS 26964 - Operator bumped hard hat against FLT fork pocket on tent frame', 'NEAR MISS 23874 - Olympic Delta - Halten East - 3000685C001 - 25/09/2024 - Wrongly Operated Valve', 'ACCIDENT 14278 - Sore left eye following soda sorb changing task'])
    LOCATION: 2117 (e.g. ['SW Thrash Zone', 'nearby hospital', 'mid level'])
    ORGANIZATION: 1753 (e.g. ['Fork Lift', 'The Far Superior', 'ST Marine Shipyard'])
    BODY_PART: 303 (e.g. ['rib cage area', 'outer ear', 'right-hand ring fingers'])
    INJURY_TYPE: 180 (e.g. ['Hyper extension', 'risk of injury', '1 cm laceration injury'])
    ROOT_CAUSE_CATEGORY: 17 (e.g. ['Mechanical - Stored energy (pressure, tension)', 'Substances  - Hazardous solids (exposure to / spill / loss of containment /pollution)', 'Access/Egress'])

  Community 2 (size=10041):
    INCIDENT: 3918 (e.g. ['ACCIDENT 8820 - 614145 - Strained back', 'NEAR MISS 24763 - Near Miss- Theodore Spoolbase- Quayside- 15 Oct 2024- fender loadout', 'ACCIDENT 13313 - Back Strain while moving hydraulic hoses'])
    EQUIPMENT: 2547 (e.g. ['torque wrench', 'frac pod system', 'D4 controller'])
    LOCATION: 1730 (e.g. ['way office', 'rt 6', 'guard shack'])
    ORGANIZATION: 1154 (e.g. ['SHELL OFFSHORE, INC', 'Fastenal', 'HPT'])
    BODY_PART: 450 (e.g. ['grip feet', 'Front flap', 'back of their head'])
    INJURY_TYPE: 215 (e.g. ['minor shallow laceration', 'recordable injury', 'small cut / laceration'])
    ROOT_CAUSE_CATEGORY: 27 (e.g. ['Flammable solids, liquids and gases', 'Unfamiliar personnel', 'Basic Organizational'])

  Community 3 (size=5248):
    INCIDENT: 1717 (e.g. ['INCIDENT 662815 - NM - Macae Base Cabiunas - Metal part rolled and dropped down from truck', 'ACCIDENT 8350 - Foco de incêndio na Extrusora - Tie In Shed', 'INCIDENT 711015 - Acidente no TOP CDA  - Pequeno vazamento de óleo do bra?o 5 fun??es do ROV.'])
    EQUIPMENT: 1275 (e.g. ['portable air conditioning', 'end cap', 'industrial lighthouse'])
    LOCATION: 1065 (e.g. ['monkey island_x000D_', 'Van point area', 'passadise'])
    ORGANIZATION: 731 (e.g. ['brigade', 'TECNOLOG', 'Deep Star CPE'])
    BODY_PART: 287 (e.g. ['bobin', 'frontal rege', 'falanges'])
    INJURY_TYPE: 162 (e.g. ['There was no injury', 'blunt cut', 'restricted work'])
    ROOT_CAUSE_CATEGORY: 11 (e.g. ['Inadequate Supervision', 'Protection', 'Equipment condition'])

  Community 4 (size=3748):
    INCIDENT: 1488 (e.g. ['ACCIDENT 631043 - FAC NWR - EMIA - NEWSIDE - 04/04/19 - Breakage of a shower door', 'ACCIDENT 12316 - SB_SP24_03/01/2023_Malaise', "NEAR MISS 618279 - IE W3 10/12/2018 -  Présence hydrocarbure au sol et dans bouche d'égout le long du batiment W3"])
    EQUIPMENT: 828 (e.g. ['lifting station', 'ROU11', 'Elingues'])
    LOCATION: 595 (e.g. ['armed reception zone', 'Carlsbad CHS location', 'SP8'])
    ORGANIZATION: 458 (e.g. ['GREENWISHES', 'production operators', 'roulev operators'])
    BODY_PART: 227 (e.g. ['throat level', 'bulkehead', 'bichenille'])
    INJURY_TYPE: 141 (e.g. ['mandrine extraction phase', 'impacted on fall', 'without injury'])
    ROOT_CAUSE_CATEGORY: 11 (e.g. ['Ergonomics - Posture (constraint or restricted environment)', 'Ergonomics - Difficult/Hindered operability of tools and equipment', 'Ergonomics - Repetitive/one sided physical demand'])

  Community 5 (size=3659):
    INCIDENT: 1129 (e.g. ['ACCIDENT 534078 - LTI - 034693C009 - Yamal LNG Project - Sabetta - 12.04.2017 - IP burned while attempting to extinguish fire in heating shelter', 'ACCIDENT 565217 - FAC - Yamal LNG Project - Sabetta - 1.10.2017 -  Ankle sprain', 'ACCIDENT 615422 - FAC - Yamal LNG Project - Sabetta - 10.11.2018 -  injury of the eyelid'])
    LOCATION: 736 (e.g. ['LNG Plant territory', '214 - SBA - 002', '034-SSH-001M'])
    EQUIPMENT: 640 (e.g. ['fan heater', 'supportive bandage', 'oil pressure tubes'])
    ORGANIZATION: 619 (e.g. ['3 level medical facility', 'doctor', 'slingers'])
    BODY_PART: 281 (e.g. ['right hand', 'left shoulder joint', 'parietal region'])
    INJURY_TYPE: 249 (e.g. ['penetrating wound', 'Closed compression fracture', 'left ankle fracture'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Fire & Explosion - Explosives / potential explosives', 'Work environment - Traffic Management / Routes / Pedestrian path', 'Work environment - Falls, slips and trips on same level (without potential to fall to lower level)'])

  Community 6 (size=3159):
    INCIDENT: 1034 (e.g. ['ACCIDENT 585754 - Lifting bolt broke during handling/securing of speedloc segment', 'ACCIDENT 11766 - Forklift mast hit gate in open position, WS hall 4', 'INCIDENT 661372 - MTC 06 - Bapco Modernization Program - Bahrain - 04.11.2019 - While  manually  shifting compressor IP finger caught in-between'])
    EQUIPMENT: 860 (e.g. ['Unbraco-pipe', 'General PPE', 'press sleeve'])
    LOCATION: 566 (e.g. ['workbench', 'Building 15', 'Agotnes'])
    ORGANIZATION: 465 (e.g. ['HSR', 'RELYON NUTEC NORWAY AS', 'Haugesund Legevakt'])
    BODY_PART: 145 (e.g. ['rib', 'bottom of the door', 'l?fte'])
    INJURY_TYPE: 80 (e.g. ['Nobody was injured', 'A1', 'minor injuries'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['1. Internal NCR (issued by TechnipFMC or Partners)', 'Confined Spaces (space/sizing issues only)', 'Explosives / potential explosives'])

  Community 7 (size=2723):
    LOCATION: 771 (e.g. ['PY5', 'KP 480', 'Ballsh'])
    INCIDENT: 658 (e.g. ['NEAR MISS 564199 - NON Technip Owned - RNT-NM 05 - 2529 TAP - Albania/ACS03 - 16/12/2017 - Potential fall from height', 'INCIDENT 707362 - FAT -TPIT Rome H.O. - Feb 22nd 2021 - Employee stumbled on last step of the office stairs, twisting his left ankle', 'INCIDENT 670080 - NON Technip Owned - RNT-NM 39 - 2529 TAP - Albania/ACS03 - 05/02/2020- Electrical activity without isolation and PTW'])
    ORGANIZATION: 624 (e.g. ['Social Field Monitor', 'TAP IPMT team', 'QA/QC Department'])
    EQUIPMENT: 537 (e.g. ['boom winch', 'retro sideboom', 'Side-boom hook/boom'])
    BODY_PART: 74 (e.g. ['right top front', 'muscles', 'right index finger_x000D_'])
    INJURY_TYPE: 52 (e.g. ['second fracture', 'extensive bruise', 'pain_x000D_'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)', 'Basic Organizational - Unfamiliar personnel', 'Basic Organizational - Inadequate Supervision'])

  Community 8 (size=2524):
    INCIDENT: 805 (e.g. ['INCIDENT 658762 - NM_ Temporary Blasting Shed (under construction) Got Collapsed_HURL_Barauni_077625C005 - 978 (NON TechnipFMC Incident)', 'ACCIDENT 533836 - First Aid Case_033390X001 - Dahej Manufacturing Facility Capex_Dahej_4/8/2017_ During the handling of cylinder,IP got pain on his thigh.', 'NEAR MISS 630324 - NM_073876C001_Spirit level fell  from 6 Mtr. Height Over an Employee Passing Nearby'])
    EQUIPMENT: 580 (e.g. ['winch rope drum', 'Two wheelers', 'Twin Sliding glass doors'])
    LOCATION: 543 (e.g. ['LT panel', '12 mtr EL', 'storage rack shelf'])
    ORGANIZATION: 344 (e.g. ['fitter crew', 'Security Department', 'Scaffolding crew'])
    BODY_PART: 131 (e.g. ['left front corner', 'remaining body', 'shin part'])
    INJURY_TYPE: 118 (e.g. ['minor skin tear', 'No injury took place', 'mild abrasion'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Fire & Explosion - Accumulation / Presence of explosive atmosphere', 'Work environment - Access/Egress', 'Ergonomics - Information perceptiveness (amount / mode) & Information reception (extend / range)'])

  Community 9 (size=2083):
    INCIDENT: 643 (e.g. ['NEAR MISS 26790 - Relaxation machine fell from trolley during transporting via forklift', 'ACCIDENT 537654 - MTI - OUI JV Rapid - Pengerang, Johor - 10 May 2017 - As the IP began apply pressure to bend the rebar , the rebar broke and his lower hand struck the rebar causing the injury .', 'INCIDENT 671274 - NM- APSB - Tooling Workshop - 23/02/2020 - Plastic rain cover dropped at tooling workshop'])
    LOCATION: 500 (e.g. ['jumper pipe area', 'take up', 'SUB 301'])
    EQUIPMENT: 479 (e.g. ['winch cover', 'GRE pipe', 'speaker'])
    ORGANIZATION: 327 (e.g. ['far East crane Company', 'Regency General Hospital', 'konecrane'])
    BODY_PART: 80 (e.g. ['Right hand thumb', 'left hand side of his face', 'phalanges bone'])
    INJURY_TYPE: 51 (e.g. ['Right hand abrasion', 'blistering', 'light wound'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Weather Condition', 'Electrical - Electrical current / electrocution / ESD / electromagnetic Fields', 'Mechanical - Equipment condition'])

  Community 10 (size=1791):
    INCIDENT: 561 (e.g. ['INCIDENT 690071 - LTI-TP owned- TORTUE FFSO-077333C010-02/09/2020 -Left leg hit by toppled Plate Girder', 'INCIDENT 680829 - NM -ALNG 2-Qingdao QMW-5thJun2020-New worker walked on top main PG without fall protection', 'ACCIDENT 505692 - FAC,Yamal LNG MWP1, China Qingdao COOEC, 15th Aug 2016, Finger squeezed'])
    LOCATION: 451 (e.g. ['Truss Project', 'Unit 300', 'Deck ‘G’'])
    EQUIPMENT: 383 (e.g. ['A-deck', 'support', 'electrical cable'])
    ORGANIZATION: 318 (e.g. ['Wison', 'PJOE M&E workshop', 'woundplast'])
    BODY_PART: 36 (e.g. ['left eyebrow', 'left rear wheels', 'Right index  finger'])
    INJURY_TYPE: 36 (e.g. ['trip and fall', 'knock trace', 'foreign body sensation'])
    ROOT_CAUSE_CATEGORY: 6 (e.g. ['Work environment - Fall to lower level / fall to water / loose materials (e.g. silos with granulate)', 'Basic Organizational - Tool suitability', 'Environment- Complaints from neighbours (noise, smell, light, dust...)'])
```

### GL-02: Equipment recurring across regions
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.2s

```
Equipment appearing in 5+ regions: 123
  fire extinguisher: 8 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  Scaffold: 8 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'Republic of. Please update lookup table.', 'South America']
  forklift: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  compressor: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  PPE: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
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
  equipment: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
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
**Type:** Global | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 5.2s

```
Top 20 non-incident nodes by degree:
  LOCATION::Europe -- degree 7436
  LOCATION::North America -- degree 4681
  LOCATION::USA -- degree 4322
  LOCATION::UK -- degree 3746
  LOCATION::Asia Pacific -- degree 3107
  LOCATION::Aberdeen -- degree 2523
  ORGANIZATION::TECHNIPFMC PLC -- degree 2518
  LOCATION::South America -- degree 2144
  ORGANIZATION::TECHNIPFMC -- degree 1821
  LOCATION::Brazil -- degree 1727
  LOCATION::France -- degree 1448
  LOCATION::Houston -- degree 1354
  ORGANIZATION::JSC YAMAL LNG -- degree 1302
  ROOT_CAUSE_CATEGORY::Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) -- degree 1126
  LOCATION::Le Trait -- degree 1113
  LOCATION::Norway -- degree 1064
  LOCATION::Flexi France -- degree 1035
  ORGANIZATION::FLEXI FRANCE -- degree 1004
  ROOT_CAUSE_CATEGORY::Work environment - Falls, slips and trips on same level (without potential to fall to lower level) -- degree 991
  ROOT_CAUSE_CATEGORY::Basic Organizational - Hazard Identification & Risk Assessment -- degree 973

Top 20 non-incident nodes by PageRank:
  LOCATION::Europe -- PR 0.005104
  LOCATION::North America -- PR 0.003520
  LOCATION::USA -- PR 0.002565
  LOCATION::Asia Pacific -- PR 0.002109
  LOCATION::UK -- PR 0.001904
  LOCATION::South America -- PR 0.001613
  LOCATION::Brazil -- PR 0.001041
  LOCATION::France -- PR 0.000943
  LOCATION::Aberdeen -- PR 0.000855
  LOCATION::Norway -- PR 0.000632
  ORGANIZATION::TECHNIPFMC PLC -- PR 0.000581
  LOCATION::Houston -- PR 0.000551
  LOCATION::India -- PR 0.000544
  LOCATION::Africa -- PR 0.000539
  LOCATION::Le Trait -- PR 0.000515
  LOCATION::Russia -- PR 0.000468
  LOCATION::Middle East -- PR 0.000437
  LOCATION::India -- PR 0.000421
  ORGANIZATION::TECHNIPFMC -- PR 0.000405
  LOCATION::Rio de Janeiro -- PR 0.000403
```

### MH-01: Equipment in containment->injury at offshore
**Type:** Multi-hop | **Coverage:** ⚠️ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Containment RCC values matched: ['Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution)', 'Hazardous liquids (exposure to / spill / loss of containment /pollution)', 'Hazardous solids (exposure to / spill / loss of containment /pollution)', 'Substances  - Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution)', 'Substances  - Hazardous liquids (exposure to / spill / loss of containment /pollution)', 'Substances  - Hazardous solids (exposure to / spill / loss of containment /pollution)']
Containment incidents: 1202
-> Offshore containment: 50
-> With injuries: 1
Equipment in those incidents:
  150te crane: 1
  main hoist winch drum: 1
```

### MH-02: Injuries from equipment failures during maintenance
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** CLEAN | **Time:** 0.0s

```
Matching incidents: 29
EQUIPMENT->INJURY_TYPE pairs (top 10):
  whip check -> personal injury: 2
  air hose -> personal injury: 1
  fitting -> personal injury: 1
  hose -> personal injury: 1
  actuator boxes -> mild static-like electric shock: 1
  actuator box -> mild static-like electric shock: 1
  engine room water pump -> burns: 1
  induction heater -> burns: 1
  PLS deck tensioner control cabin -> personal injury: 1
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

  forklift (734 incidents):
    injuries: 19
    pain: 5
    injury: 4
    minor damage: 3
    personnel injury: 3

  crane (620 incidents):
    injuries: 17
    personal injury: 4
    abrasion: 4
    fracture: 3
    contusion: 2

  ROV (279 incidents):
    ferimentos pessoais: 2
    bruise: 1
    spraining: 1
    bites: 1
    injury: 1

  pallet (170 incidents):
    injuries: 5
    laceration: 2
    injury: 2
    no injury reported: 1
    personnel injury: 1

  excavator (140 incidents):
    injuries: 6
    no injuries: 2
    No injuries occurred: 2
    wound: 1
    back injury: 1
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

  truck (424 incidents):
    Severity 1: 53
    Severity 2: 57
    Severity 3: 17
    Severity 4: 4
    Mean severity: 1.79

  crane (1444 incidents):
    Severity 1: 131
    Severity 2: 169
    Severity 3: 89
    Severity 4: 24
    Severity 5: 3
    Mean severity: 2.04
```

### MH-07: Scaffold near-misses by location
**Type:** Multi-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.1s

```
Matching incidents: 115
Distinct LOCATION values: 36
Top 10:
  zObsolete - Trinidad: 15
  Sabetta: 12
  zObsolete - Batam: 11
  Aberdeen: 9
  zObsolete - Tirana: 8
  Dubai: 7
  Amalapuram: 4
  Baku: 4
  Panipat: 3
  Abu Dhabi: 3
```

### MH-08: Hydraulic valve -> injury outcome
**Type:** Multi-hop | **Coverage:** ⚠️ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 3
Distinct INJURY_TYPE values: 0
Top 10:
```

### SH-01: Forklift incidents in 2022
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.3s

```
Matching incidents: 73
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
Distinct BODY_PART values: 247
Top 10:
  left hand: 17
  right hand: 14
  left foot: 11
  head: 10
  middle finger: 10
  finger: 8
  leg: 7
  lower back: 7
  right foot: 6
  back: 6
```

### SH-04: Locations for valve incidents
**Type:** Single-hop | **Coverage:** ✅ | **Diagnosis:** ER_NEEDED | **Time:** 0.0s

```
Matching incidents: 386
Distinct LOCATION values: 37
Top 10:
  USA: 171
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
Distinct INJURY_TYPE values: 153
Top 10:
  personal injury: 12
  superficial cut: 6
  laceration: 6
  cut: 5
  abrasion: 5
  pain: 4
  small cut: 4
  wound: 4
  soft tissue injury: 3
  slight bruising: 3
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
| Single-hop (6) | 6 | 5/6 pass | 6/6 pass | 6/6 pass |
| Aggregation (6) | 6 | 5/6 pass | 5/6 pass | 5/6 pass |
| Multi-hop (8) | 8 | 5/8 pass | 8/8 pass | 8/8 pass |
| Global (4) | 4 | 4/4 pass | 4/4 pass | 4/4 pass |
| Conjunctive (6) | 6 | 2/6 pass | 2/6 pass | 4/6 pass |

## 4. Key Findings

### What works well at L1

- **AG-01**: Root causes of dropped object incidents
- **AG-02**: Countries with most high-severity incidents
- **AG-03**: Most common equipment by incident count
- **AG-05**: Monthly trend of fall/slip incidents
- **AG-06**: Severity distribution by impact type
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

- **CJ-01** (Corrosion -> equipment failure -> fire (L2)): requires CAUSED_BY/CONTRIBUTED_TO edges
- **CJ-05** (Procedural -> dropped -> head/hand injury (L2)): requires CAUSED_BY/CONTRIBUTED_TO edges

### Data sparsity issues

- **AG-04** (Incident type x business unit crosstab): metadata coverage too low for reliable results
- **CJ-02** (Crane + back + offshore + high severity): metadata coverage too low for reliable results
- **CJ-03** (Maintenance fail + pipe + environmental + Middle East): metadata coverage too low for reliable results

---
*Generated by pipeline_v2/benchmark/run_benchmark.py*