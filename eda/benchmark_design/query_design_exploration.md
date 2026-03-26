# Query Design Data Exploration Report

**Dataset:** `dev_sample.csv` — 23311 records

**Purpose:** Ground truth data profiling to support design of 30 Gold Standard benchmark queries.

---

## Analysis 1: Entity Landscape Profiling

Total records scanned: 23311

### Equipment Mentions (Top 50)

| Rank | Term | Count | % Records | Density |
|------|------|-------|-----------|---------|
| 1 | vessel | 2604 | 11.2% | HIGH |
| 2 | equipment | 2320 | 10.0% | HIGH |
| 3 | crane | 2297 | 9.9% | HIGH |
| 4 | pipe | 2145 | 9.2% | HIGH |
| 5 | truck | 1724 | 7.4% | HIGH |
| 6 | lifting | 1662 | 7.1% | HIGH |
| 7 | lift | 1621 | 7.0% | HIGH |
| 8 | forklift | 1321 | 5.7% | HIGH |
| 9 | vehicle | 1279 | 5.5% | HIGH |
| 10 | valve | 1245 | 5.3% | HIGH |
| 11 | hose | 1167 | 5.0% | HIGH |
| 12 | tool | 1055 | 4.5% | MEDIUM |
| 13 | machine | 1054 | 4.5% | MEDIUM |
| 14 | cable | 1021 | 4.4% | MEDIUM |
| 15 | wire | 1018 | 4.4% | MEDIUM |
| 16 | door | 1006 | 4.3% | MEDIUM |
| 17 | platform | 971 | 4.2% | MEDIUM |
| 18 | rigging | 956 | 4.1% | MEDIUM |
| 19 | pallet | 906 | 3.9% | MEDIUM |
| 20 | cutting | 679 | 2.9% | MEDIUM |
| 21 | car | 650 | 2.8% | MEDIUM |
| 22 | trailer | 647 | 2.8% | MEDIUM |
| 23 | boom | 640 | 2.7% | MEDIUM |
| 24 | board | 631 | 2.7% | MEDIUM |
| 25 | gloves | 627 | 2.7% | MEDIUM |
| 26 | pump | 606 | 2.6% | MEDIUM |
| 27 | container | 602 | 2.6% | MEDIUM |
| 28 | tank | 596 | 2.6% | MEDIUM |
| 29 | panel | 580 | 2.5% | MEDIUM |
| 30 | scaffold | 554 | 2.4% | MEDIUM |
| 31 | hook | 554 | 2.4% | MEDIUM |
| 32 | scaffolding | 548 | 2.4% | MEDIUM |
| 33 | sling | 547 | 2.3% | MEDIUM |
| 34 | reel | 520 | 2.2% | MEDIUM |
| 35 | saw | 505 | 2.2% | MEDIUM |
| 36 | fitting | 504 | 2.2% | MEDIUM |
| 37 | basket | 502 | 2.2% | MEDIUM |
| 38 | gate | 487 | 2.1% | MEDIUM |
| 39 | winch | 483 | 2.1% | MEDIUM |
| 40 | rope | 466 | 2.0% | MEDIUM |
| 41 | chain | 434 | 1.9% | MEDIUM |
| 42 | compressor | 432 | 1.9% | MEDIUM |
| 43 | roller | 432 | 1.9% | MEDIUM |
| 44 | PPE | 426 | 1.8% | MEDIUM |
| 45 | meter | 413 | 1.8% | MEDIUM |
| 46 | spool | 413 | 1.8% | MEDIUM |
| 47 | welder | 411 | 1.8% | MEDIUM |
| 48 | flange | 405 | 1.7% | MEDIUM |
| 49 | manifold | 404 | 1.7% | MEDIUM |
| 50 | clamp | 403 | 1.7% | MEDIUM |

### Injury/Body Part Mentions (Top 40)

| Rank | Term | Count | % Records | Density |
|------|------|-------|-----------|---------|
| 1 | back | 3651 | 15.7% | HIGH |
| 2 | injury | 2527 | 10.8% | HIGH |
| 3 | hand | 2305 | 9.9% | HIGH |
| 4 | cut | 1485 | 6.4% | HIGH |
| 5 | pain | 1284 | 5.5% | HIGH |
| 6 | finger | 1263 | 5.4% | HIGH |
| 7 | head | 1028 | 4.4% | MEDIUM |
| 8 | foot | 893 | 3.8% | MEDIUM |
| 9 | eye | 661 | 2.8% | MEDIUM |
| 10 | leg | 618 | 2.7% | MEDIUM |
| 11 | arm | 576 | 2.5% | MEDIUM |
| 12 | face | 474 | 2.0% | MEDIUM |
| 13 | wound | 414 | 1.8% | MEDIUM |
| 14 | ankle | 390 | 1.7% | MEDIUM |
| 15 | fracture | 381 | 1.6% | MEDIUM |
| 16 | shoulder | 366 | 1.6% | MEDIUM |
| 17 | knee | 362 | 1.6% | MEDIUM |
| 18 | laceration | 298 | 1.3% | MEDIUM |
| 19 | swelling | 239 | 1.0% | MEDIUM |
| 20 | contusion | 226 | 1.0% | LOW |
| 21 | burn | 209 | 0.9% | LOW |
| 22 | wrist | 200 | 0.9% | LOW |
| 23 | neck | 193 | 0.8% | LOW |
| 24 | elbow | 182 | 0.8% | LOW |
| 25 | abrasion | 160 | 0.7% | LOW |
| 26 | bleeding | 151 | 0.6% | LOW |
| 27 | scratch | 146 | 0.6% | LOW |
| 28 | bruise | 141 | 0.6% | LOW |
| 29 | strain | 124 | 0.5% | LOW |
| 30 | chest | 121 | 0.5% | LOW |
| 31 | exposure | 108 | 0.5% | LOW |
| 32 | toe | 99 | 0.4% | LOW |
| 33 | sprain | 98 | 0.4% | LOW |
| 34 | shin | 86 | 0.4% | LOW |
| 35 | puncture | 72 | 0.3% | LOW |
| 36 | crush | 37 | 0.2% | LOW |
| 37 | hip | 36 | 0.2% | LOW |
| 38 | rib | 36 | 0.2% | LOW |
| 39 | dislocation | 36 | 0.2% | LOW |
| 40 | concussion | 16 | 0.1% | LOW |

### Causal/Action Terms (Top 30)

| Rank | Term | Count | % Records | Density |
|------|------|-------|-----------|---------|
| 1 | fell | 3063 | 13.1% | HIGH |
| 2 | hit | 2208 | 9.5% | HIGH |
| 3 | injured | 1725 | 7.4% | HIGH |
| 4 | damaged | 1646 | 7.1% | HIGH |
| 5 | cut | 1485 | 6.4% | HIGH |
| 6 | slipped | 1273 | 5.5% | HIGH |
| 7 | dropped | 1271 | 5.5% | HIGH |
| 8 | released | 1079 | 4.6% | MEDIUM |
| 9 | contacted | 1039 | 4.5% | MEDIUM |
| 10 | caught | 891 | 3.8% | MEDIUM |
| 11 | struck | 812 | 3.5% | MEDIUM |
| 12 | failed | 710 | 3.0% | MEDIUM |
| 13 | broke | 629 | 2.7% | MEDIUM |
| 14 | tripped | 348 | 1.5% | MEDIUM |
| 15 | pinched | 276 | 1.2% | MEDIUM |
| 16 | spilled | 261 | 1.1% | MEDIUM |
| 17 | trapped | 216 | 0.9% | LOW |
| 18 | leaked | 208 | 0.9% | LOW |
| 19 | dislodged | 197 | 0.8% | LOW |
| 20 | collapsed | 154 | 0.7% | LOW |
| 21 | impacted | 130 | 0.6% | LOW |
| 22 | crushed | 92 | 0.4% | LOW |
| 23 | ejected | 85 | 0.4% | LOW |
| 24 | burned | 79 | 0.3% | LOW |
| 25 | fractured | 46 | 0.2% | LOW |
| 26 | overloaded | 38 | 0.2% | LOW |
| 27 | corroded | 33 | 0.1% | LOW |
| 28 | exploded | 19 | 0.1% | LOW |
| 29 | malfunctioned | 12 | 0.1% | LOW |

---

## Analysis 2: CASE_CATEGORIZATION Taxonomy

Total unique CASE_CATEGORIZATION values: 117

### All Values (sorted by count)

| Rank | CASE_CATEGORIZATION | Count | % |
|------|---------------------|-------|---|
| 1 | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) | 1453 | 6.2% |
| 2 | Mechanical - Equipment condition | 1214 | 5.2% |
| 3 | Basic Organizational - Hazard Identification & Risk Assessment | 1192 | 5.1% |
| 4 | Mechanical - Stored energy (dropped objects) | 1158 | 5.0% |
| 5 | Work environment - Falls, slips and trips on same level (without potential to fall to lower level) | 1034 | 4.4% |
| 6 | Substances  - Hazardous liquids (exposure to / spill / loss of containment /pollution) | 885 | 3.8% |
| 7 | Basic Organizational - Standard Operating Procedures, Procedures & Work instructions | 878 | 3.8% |
| 8 | Basic Organizational - Planning and coordination of works | 777 | 3.3% |
| 9 | Mechanical - Stored energy (pressure, tension) | 687 | 2.9% |
| 10 | Ergonomics - Manual handling | 642 | 2.8% |
| 11 | Basic Organisational - Equipment Suitability | 547 | 2.3% |
| 12 | Work environment - Fall to lower level / fall to water / loose materials (e.g. silos with granulate) | 502 | 2.2% |
| 13 | Work environment - Motor Vehicle Road Accident | 448 | 1.9% |
| 14 | Work environment - Traffic Management / Routes / Pedestrian path | 417 | 1.8% |
| 15 | Fire & Explosion - Flammable solids, liquids and gases | 408 | 1.8% |
| 16 | Basic Organizational - Inadequate Supervision | 395 | 1.7% |
| 17 | Work environment - Workplace layout / congestion | 363 | 1.6% |
| 18 | Equipment condition | 359 | 1.5% |
| 19 | Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) | 345 | 1.5% |
| 20 | Hazard Identification & Risk Assessment | 333 | 1.4% |
| 21 | Basic Organizational - Unfamiliar personnel | 321 | 1.4% |
| 22 | Work environment - Motor Vehicle Worksite Accident | 314 | 1.3% |
| 23 | Electrical - Electrical current / electrocution / ESD / electromagnetic Fields | 311 | 1.3% |
| 24 | Stored energy (dropped objects) | 300 | 1.3% |
| 25 | Hazardous liquids (exposure to / spill / loss of containment /pollution) | 294 | 1.3% |
| 26 | Basic Organizational - Use of personal protective equipment | 275 | 1.2% |
| 27 | Work environment - Access/Egress | 248 | 1.1% |
| 28 | Basic Organizational - Tool suitability | 233 | 1.0% |
| 29 | Stored energy (pressure, tension) | 229 | 1.0% |
| 30 | Mechanical - Unprotected/unguarded moving machine parts (struck by/caught by ) | 229 | 1.0% |
| 31 | Motor Vehicle Road Accident | 193 | 0.8% |
| 32 | Falls, slips and trips on same level (without potential to fall to lower level) | 190 | 0.8% |
| 33 | Work environment - Climate (Heat/Cold/Humidity) | 189 | 0.8% |
| 34 | Mechanical - Dangerous surfaces (sharp/ sharp edged/ high roughness grade) | 187 | 0.8% |
| 35 | Mechanical - Tool condition | 187 | 0.8% |
| 36 | Ergonomics - Posture (constraint or restricted environment) | 183 | 0.8% |
| 37 | Planning and coordination of works | 180 | 0.8% |
| 38 | Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...) | 166 | 0.7% |
| 39 | Manual handling | 163 | 0.7% |
| 40 | Standard Operating Procedures, Procedures & Work instructions | 158 | 0.7% |
| 41 | Equipment Suitability | 154 | 0.7% |
| 42 | Biological - Animals, Bacteria, Viruses and Funguses | 142 | 0.6% |
| 43 | Substances  - Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution) | 128 | 0.5% |
| 44 | Fire & Explosion - Uncontrolled chemical or physical reaction | 124 | 0.5% |
| 45 | Motor Vehicle Worksite Accident | 120 | 0.5% |
| 46 | Physical - Hot/cold surfaces or media | 90 | 0.4% |
| 47 | Use of personal protective equipment | 88 | 0.4% |
| 48 | Ergonomics - Difficult/Hindered operability of tools and equipment | 83 | 0.4% |
| 49 | Tool suitability | 76 | 0.3% |
| 50 | Basic Organizational - SIMOPS (coordination with 3rd Parties) | 76 | 0.3% |
| 51 | Fall to lower level / fall to water / loose materials (e.g. silos with granulate) | 72 | 0.3% |
| 52 | Workplace layout / congestion | 70 | 0.3% |
| 53 | Environment- Over-consumption of energy, natural resources (water, ...) | 68 | 0.3% |
| 54 | Pinch point | 67 | 0.3% |
| 55 | Environment- Unsorted waste, no traceability of the waste;? | 67 | 0.3% |
| 56 | Basic Organizational - Management of Change | 66 | 0.3% |
| 57 | Unfamiliar personnel | 61 | 0.3% |
| 58 | Electrical | 60 | 0.3% |
| 59 | Work environment - Confined Spaces (space/sizing issues only) | 60 | 0.3% |
| 60 | Substances  - Hazardous solids (exposure to / spill / loss of containment /pollution) | 60 | 0.3% |
| 61 | Flammable solids, liquids and gases | 56 | 0.2% |
| 62 | Dangerous surfaces (sharp/ sharp edged/ high roughness grade) | 55 | 0.2% |
| 63 | Difficult/Hindered operability of tools and equipment | 54 | 0.2% |
| 64 | Lifting ops error | 54 | 0.2% |
| 65 | Ergonomics - Repetitive/one sided physical demand | 53 | 0.2% |
| 66 | Traffic Management / Routes / Pedestrian path | 47 | 0.2% |
| 67 | Access/Egress | 46 | 0.2% |
| 68 | Tool condition | 46 | 0.2% |
| 69 | Climate (Heat/Cold/Humidity) | 46 | 0.2% |
| 70 | Posture (constraint or restricted environment) | 43 | 0.2% |
| 71 | Work environment - Illumination / sight / visibility | 41 | 0.2% |
| 72 | Unprotected/unguarded moving machine parts (struck by/caught by) | 39 | 0.2% |
| 73 | Fire & Explosion - Accumulation / Presence of explosive atmosphere | 37 | 0.2% |
| 74 | Inadequate Supervision | 35 | 0.2% |
| 75 | Psycho social - Stress | 35 | 0.2% |
| 76 | Fire & Explosion - Explosives / potential explosives | 35 | 0.2% |
| 77 | Animals, Bacteria, Viruses and Funguses | 32 | 0.1% |
| 78 | Uncontrolled chemical or physical reaction | 28 | 0.1% |
| 79 | Work environment - Hyperbaric work environment | 21 | 0.1% |
| 80 | Environment- Complaints from neighbours (noise, smell, light, dust...) | 21 | 0.1% |
| 81 | Hot/cold surfaces or media | 20 | 0.1% |
| 82 | SIMOPS (coordination with 3rd Parties) | 19 | 0.1% |
| 83 | Repetitive/one sided physical demand | 18 | 0.1% |
| 84 | Physical - Vibrations (hand arm / whole body) | 16 | 0.1% |
| 85 | Weather Condition | 15 | 0.1% |
| 86 | Psycho social - Work time/ Shift pattern | 15 | 0.1% |
| 87 | Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution) | 13 | 0.1% |
| 88 | Management of Change | 13 | 0.1% |
| 89 | Psycho social - Alcohol and drugs abuse | 13 | 0.1% |
| 90 | Hyperbaric work environment | 12 | 0.1% |
| 91 | Ergonomics - Information perceptiveness (amount / mode) & Information reception (extend / range) | 12 | 0.1% |
| 92 | Physical - Radiation (ionising / non ionising) | 11 | 0.0% |
| 93 | Hazardous solids (exposure to / spill / loss of containment /pollution) | 9 | 0.0% |
| 94 | Confined Spaces (space/sizing issues only) | 8 | 0.0% |
| 95 | Psycho social - Workload (Overload/Underload) | 8 | 0.0% |
| 96 | Illumination / sight / visibility | 7 | 0.0% |
| 97 | Accumulation / Presence of explosive atmosphere | 6 | 0.0% |
| 98 | Inappropriate behavior / Horseplay / Aggression / violence (Fights, Riots, etc.) | 6 | 0.0% |
| 99 | Ergonomics - Computer workplaces / Screens | 6 | 0.0% |
| 100 | Physical - Noise | 5 | 0.0% |
| 101 | Computer workplaces / Screens | 4 | 0.0% |
| 102 | Stress | 4 | 0.0% |
| 103 | 1. Internal NCR (issued by TechnipFMC or Partners) | 4 | 0.0% |
| 104 | Radiation (ionising / non ionising) | 3 | 0.0% |
| 105 | Vibrations (hand arm / whole body) | 3 | 0.0% |
| 106 | Information perceptiveness (amount / mode) & Information reception (extend / range) | 3 | 0.0% |
| 107 | Work time/ Shift pattern | 3 | 0.0% |
| 108 | Unsorted waste, no traceability of the waste | 3 | 0.0% |
| 109 | Complaints from neighbors (noise, smell, light, dust, etc.) | 2 | 0.0% |
| 110 | Workload (Overload/Underload) | 2 | 0.0% |
| 111 | Animal Strike | 2 | 0.0% |
| 112 | Basic Organizational | 1 | 0.0% |
| 113 | Protection | 1 | 0.0% |
| 114 | Noise | 1 | 0.0% |
| 115 | Explosives / potential explosives | 1 | 0.0% |
| 116 | 3. 3rd Party NCR (received or managed by TechnipFMC or Partners) | 1 | 0.0% |
| 117 | Over-consumption of energy, natural resources (water, etc.) | 1 | 0.0% |

### Clustered Groupings

**Mechanical** (total: 8772)
  - Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 1453
  - Mechanical - Equipment condition: 1214
  - Mechanical - Stored energy (dropped objects): 1158
  - Mechanical - Stored energy (pressure, tension): 687
  - Basic Organisational - Equipment Suitability: 547
  - Work environment - Motor Vehicle Road Accident: 448
  - Equipment condition: 359
  - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 345
  - Work environment - Motor Vehicle Worksite Accident: 314
  - Basic Organizational - Use of personal protective equipment: 275
  - Basic Organizational - Tool suitability: 233
  - Stored energy (pressure, tension): 229
  - Mechanical - Unprotected/unguarded moving machine parts (struck by/caught by ): 229
  - Motor Vehicle Road Accident: 193
  - Mechanical - Dangerous surfaces (sharp/ sharp edged/ high roughness grade): 187
  - Mechanical - Tool condition: 187
  - Equipment Suitability: 154
  - Motor Vehicle Worksite Accident: 120
  - Use of personal protective equipment: 88
  - Ergonomics - Difficult/Hindered operability of tools and equipment: 83
  - Tool suitability: 76
  - Difficult/Hindered operability of tools and equipment: 54
  - Lifting ops error: 54
  - Tool condition: 46
  - Unprotected/unguarded moving machine parts (struck by/caught by): 39

**Procedural & Organizational** (total: 4111)
  - Basic Organizational - Hazard Identification & Risk Assessment: 1192
  - Basic Organizational - Standard Operating Procedures, Procedures & Work instructions: 878
  - Basic Organizational - Planning and coordination of works: 777
  - Basic Organizational - Inadequate Supervision: 395
  - Basic Organizational - Unfamiliar personnel: 321
  - Planning and coordination of works: 180
  - Standard Operating Procedures, Procedures & Work instructions: 158
  - Basic Organizational - SIMOPS (coordination with 3rd Parties): 76
  - Basic Organizational - Management of Change: 66
  - Inadequate Supervision: 35
  - SIMOPS (coordination with 3rd Parties): 19
  - Management of Change: 13
  - Basic Organizational: 1

**Falls & Slips** (total: 1798)
  - Work environment - Falls, slips and trips on same level (without potential to fall to lower level): 1034
  - Work environment - Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 502
  - Falls, slips and trips on same level (without potential to fall to lower level): 190
  - Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 72

**Environmental** (total: 1612)
  - Work environment - Traffic Management / Routes / Pedestrian path: 417
  - Work environment - Workplace layout / congestion: 363
  - Work environment - Access/Egress: 248
  - Work environment - Climate (Heat/Cold/Humidity): 189
  - Environment- Over-consumption of energy, natural resources (water, ...): 68
  - Environment- Unsorted waste, no traceability of the waste;?: 67
  - Work environment - Confined Spaces (space/sizing issues only): 60
  - Climate (Heat/Cold/Humidity): 46
  - Posture (constraint or restricted environment): 43
  - Work environment - Illumination / sight / visibility: 41
  - Work environment - Hyperbaric work environment: 21
  - Environment- Complaints from neighbours (noise, smell, light, dust...): 21
  - Weather Condition: 15
  - Hyperbaric work environment: 12
  - Over-consumption of energy, natural resources (water, etc.): 1

**Chemical & Hazmat** (total: 1555)
  - Substances  - Hazardous liquids (exposure to / spill / loss of containment /pollution): 885
  - Hazardous liquids (exposure to / spill / loss of containment /pollution): 294
  - Substances  - Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution): 128
  - Fire & Explosion - Uncontrolled chemical or physical reaction: 124
  - Substances  - Hazardous solids (exposure to / spill / loss of containment /pollution): 60
  - Uncontrolled chemical or physical reaction: 28
  - Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution): 13
  - Physical - Radiation (ionising / non ionising): 11
  - Hazardous solids (exposure to / spill / loss of containment /pollution): 9
  - Radiation (ionising / non ionising): 3

**Human Factors** (total: 954)
  - Ergonomics - Manual handling: 642
  - Ergonomics - Posture (constraint or restricted environment): 183
  - Ergonomics - Repetitive/one sided physical demand: 53
  - Psycho social - Stress: 35
  - Psycho social - Alcohol and drugs abuse: 13
  - Ergonomics - Information perceptiveness (amount / mode) & Information reception (extend / range): 12
  - Inappropriate behavior / Horseplay / Aggression / violence (Fights, Riots, etc.): 6
  - Ergonomics - Computer workplaces / Screens: 6
  - Stress: 4

**Other** (total: 793)
  - Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...): 166
  - Biological - Animals, Bacteria, Viruses and Funguses: 142
  - Physical - Hot/cold surfaces or media: 90
  - Pinch point: 67
  - Unfamiliar personnel: 61
  - Dangerous surfaces (sharp/ sharp edged/ high roughness grade): 55
  - Traffic Management / Routes / Pedestrian path: 47
  - Animals, Bacteria, Viruses and Funguses: 32
  - Hot/cold surfaces or media: 20
  - Repetitive/one sided physical demand: 18
  - Physical - Vibrations (hand arm / whole body): 16
  - Psycho social - Work time/ Shift pattern: 15
  - Confined Spaces (space/sizing issues only): 8
  - Psycho social - Workload (Overload/Underload): 8
  - Illumination / sight / visibility: 7
  - Accumulation / Presence of explosive atmosphere: 6
  - Physical - Noise: 5
  - Computer workplaces / Screens: 4
  - 1. Internal NCR (issued by TechnipFMC or Partners): 4
  - Vibrations (hand arm / whole body): 3
  - Information perceptiveness (amount / mode) & Information reception (extend / range): 3
  - Work time/ Shift pattern: 3
  - Unsorted waste, no traceability of the waste: 3
  - Complaints from neighbors (noise, smell, light, dust, etc.): 2
  - Workload (Overload/Underload): 2
  - Animal Strike: 2
  - Protection: 1
  - Noise: 1
  - Explosives / potential explosives: 1
  - 3. 3rd Party NCR (received or managed by TechnipFMC or Partners): 1

**Fire & Explosion** (total: 536)
  - Fire & Explosion - Flammable solids, liquids and gases: 408
  - Flammable solids, liquids and gases: 56
  - Fire & Explosion - Accumulation / Presence of explosive atmosphere: 37
  - Fire & Explosion - Explosives / potential explosives: 35

**Electrical** (total: 371)
  - Electrical - Electrical current / electrocution / ESD / electromagnetic Fields: 311
  - Electrical: 60

**Risk Assessment & Hazard ID** (total: 333)
  - Hazard Identification & Risk Assessment: 333

**PPE & Safety Controls** (total: 300)
  - Stored energy (dropped objects): 300

**Manual Handling** (total: 163)
  - Manual handling: 163

**Housekeeping & Layout** (total: 116)
  - Workplace layout / congestion: 70
  - Access/Egress: 46

### Top 15 CASE_CATEGORIZATION × IMPACT_TYPE

| CASE_CATEGORIZATION | Damage | Environment | Financial Impact | Fire/Explosion | Injury | Occupational Illness | Reputation | Unknown |
|---|---|---|---|---|---|---|---|---|
| Mechanical - Uncontrolled moving objects/ parts (struck by o | 186 | 37 | 336 | 0 | 824 | 14 | 52 | 4 |
| Mechanical - Equipment condition | 178 | 190 | 339 | 13 | 432 | 6 | 56 | 0 |
| Basic Organizational - Hazard Identification & Risk Assessme | 163 | 56 | 225 | 10 | 696 | 7 | 33 | 2 |
| Mechanical - Stored energy (dropped objects) | 113 | 29 | 179 | 0 | 781 | 10 | 46 | 0 |
| Work environment - Falls, slips and trips on same level (wit | 13 | 6 | 6 | 3 | 990 | 7 | 8 | 1 |
| Substances  - Hazardous liquids (exposure to / spill / loss  | 13 | 680 | 40 | 3 | 109 | 16 | 23 | 1 |
| Basic Organizational - Standard Operating Procedures, Proced | 170 | 34 | 183 | 6 | 409 | 11 | 61 | 4 |
| Basic Organizational - Planning and coordination of works | 132 | 43 | 194 | 12 | 329 | 5 | 57 | 5 |
| Mechanical - Stored energy (pressure, tension) | 68 | 55 | 137 | 0 | 394 | 3 | 29 | 1 |
| Ergonomics - Manual handling | 14 | 2 | 26 | 0 | 585 | 12 | 3 | 0 |
| Basic Organisational - Equipment Suitability | 68 | 59 | 129 | 3 | 252 | 6 | 29 | 1 |
| Work environment - Fall to lower level / fall to water / loo | 62 | 5 | 32 | 1 | 388 | 4 | 8 | 2 |
| Work environment - Motor Vehicle Road Accident | 4 | 6 | 241 | 0 | 169 | 3 | 22 | 3 |
| Work environment - Traffic Management / Routes / Pedestrian  | 95 | 3 | 101 | 2 | 200 | 0 | 13 | 3 |
| Fire & Explosion - Flammable solids, liquids and gases | 31 | 28 | 113 | 58 | 163 | 3 | 10 | 2 |

### Top 15 CASE_CATEGORIZATION × SEVERITY

| CASE_CATEGORIZATION | 1-Negligible | 2-Minor | 3-Moderate | 4-Major | 5-Catastrophic | Unknown |
|---|---|---|---|---|---|---|
| Mechanical - Uncontrolled moving objects/ parts (struck by o | 357 | 209 | 323 | 0 | 27 | 537 |
| Mechanical - Equipment condition | 262 | 247 | 133 | 0 | 15 | 557 |
| Basic Organizational - Hazard Identification & Risk Assessme | 328 | 134 | 195 | 0 | 13 | 522 |
| Mechanical - Stored energy (dropped objects) | 341 | 114 | 267 | 0 | 63 | 373 |
| Work environment - Falls, slips and trips on same level (wit | 421 | 5 | 192 | 0 | 1 | 415 |
| Substances  - Hazardous liquids (exposure to / spill / loss  | 77 | 37 | 25 | 1 | 0 | 745 |
| Basic Organizational - Standard Operating Procedures, Proced | 215 | 135 | 141 | 0 | 16 | 371 |
| Basic Organizational - Planning and coordination of works | 184 | 103 | 108 | 3 | 22 | 357 |
| Mechanical - Stored energy (pressure, tension) | 159 | 96 | 179 | 0 | 19 | 234 |
| Ergonomics - Manual handling | 236 | 16 | 114 | 0 | 0 | 276 |
| Basic Organisational - Equipment Suitability | 120 | 98 | 71 | 0 | 8 | 250 |
| Work environment - Fall to lower level / fall to water / loo | 112 | 28 | 158 | 0 | 16 | 188 |
| Work environment - Motor Vehicle Road Accident | 130 | 165 | 55 | 0 | 17 | 81 |
| Work environment - Traffic Management / Routes / Pedestrian  | 104 | 65 | 73 | 0 | 7 | 168 |
| Fire & Explosion - Flammable solids, liquids and gases | 138 | 61 | 51 | 3 | 3 | 152 |

---

## Analysis 3: Causal Language in Narratives

Records with at least one causal phrase: 6036 (25.9%)

### Causal Phrase Frequencies

| Phrase | Count | % Records |
|--------|-------|-----------|
| due to | 3258 | 14.0% |
| led to | 927 | 4.0% |
| as a result | 865 | 3.7% |
| resulted in | 845 | 3.6% |
| because | 653 | 2.8% |
| caused by | 266 | 1.1% |
| root cause | 202 | 0.9% |
| failure of | 89 | 0.4% |
| contributing factor | 61 | 0.3% |
| consequence of | 26 | 0.1% |
| linked to | 24 | 0.1% |
| attributed to | 23 | 0.1% |
| originating from | 12 | 0.1% |
| triggered by | 2 | 0.0% |
| stemming from | 1 | 0.0% |

### Causal Phrase Distribution per Narrative

| Phrases per narrative | Count | % |
|----------------------|-------|---|
| 0 | 17275 | 74.1% |
| 1 | 5013 | 21.5% |
| 2 | 846 | 3.6% |
| 3+ | 177 | 0.8% |

### Example Sentences for Top 5 Causal Phrases

#### "due to" (3258 occurrences)

1. Pallet/crate was returned to workshop for inspection for potential damages  Update 17/3: No damage to equipment due to proper packing and securing with pallet/crate
2. During demobilization operations and flushing of the deck it was noted that there were several areas of the deck that had become damaged/ undercut due to procedures not being followed by the welding c
3. This area of operation on the STU North Pad had a small ‘footprint’ due to the fixed roller paths adjacent to Carousel H and the recently fitted steps on Under Roller 8
4. This is rigged this way due to the extra weight from the adapter and motor on the front
5. Highly suspected due to bad weather/strong wind over the weekend
6. There was no hold back rigging fitted therefore when the rigging was approximately half way up the tower the rigging was swinging due to ships movement
7. The manlift safety system activated and shut the manlift down due to the increase transition angle from the concrete slab to the ground outside the door
8. Due to the set up in the room and lack of TV to share a display, I moved myself to the edge of a small table to allow others to access the monitors
9. At 00:44, due to uncontrolled movement of the UCON basket, a command was given to the crane operator to move the basket back over the side
10. During approximate tests of the PSV Cormoram to board the Deep Star, the PSV presented positioning loss due to an abnormal stop of the electric engine of the bow-thruster of vante

#### "led to" (927 occurrences)

1. The supervisor and HSE rep were called to the scene
2. 09 June 1330 hours – Pre-test visual inspection was done but failed to identify the wrong test cap
3. The substance generated dust when being emptied which led to mild respiratory and eye-irritation that passed rapidly for two of the three participants
4. Driver was making a test run for a path that will need to be traveled tomorrow morning with a long load
5. Deck supervisor called to deck, along with crane technician for inspection
6. Following confirmation that the line was not scheduled to be cut, the Deep Orient returned to Stybarrow field to perform visual inspection of the cut ends at H3 and H4 XT
7. Based on the drops calculation (attached) this could have led to a Major HSE Event
8. The crane technician was immediately called to investigate and advise
9. The sheave assembly had some damage to the maintenance locking pin clevis where the two locking pin clevises had been pulled together
10. This led to back pain and IP had to stop working

#### "as a result" (865 occurrences)

1. Nothing dropped from the tower as a result of the incident
2. As a result, the seal stab fell to the shop floor on the opposite side of the operator from about 70 cm height
3. as a result of this the TSP ran into the back of the vehicle in front of him
4. As a reaction the coordinator turned his head and as a result the hook brushed his chin causing a small abrasion
5. As a result, the IP's right index finger was caught between the steel hose connection, just above the flange, and the connection point on the pump
6. As a result, IP lost the balance and twisted the right ankle
7. They did not require first aid as a result of the incident
8. As a result, she sustained minor scratches on her left hand finger
9. Weight of the ratchet strap is 346grms  When the straps are fitted, they are fully tensioned but when wind catches the tarps the straps move and as a result work loose  Further investigation is requir
10. Note: No material damage or injury occurred as a result of this event

#### "resulted in" (845 occurrences)

1. This resulted in a small burn and did not require any first aid
2. As the TFMC employee continued down the road, he noticed she had prematurely entered into the main road and turned into traffic, cutting me off and reluctantly resulted in the impact
3. This resulted in a finger injury and bruising to the ring finger of his right hand
4. This resulted in the valve dropping on to the employee's foot
5. The part was slightly tilted towards the handle of the cart, which resulted in the cart falling over
6. This resulted in the crane 110% alarm being activated
7. Police responded to the accident and completed D&A screening of the drivers and resulted in negative results
8. The mouse came in contact with the cluster which resulted in the fall of a plate of the cluster
9. This resulted in a load on the 500Te winch peaking at 84Te
10. This resulted in the Umbilical lead end (UCON) pulling backwards and lifting off the trolley approximately 1 metre

#### "because" (653 occurrences)

1. The forklift operator was going into BAY A workshop to collect the equipment, and the fork impacted the door rail as the operator approached the entrance, but he continued working without realizing it
2. During a return with the help of the car returning site clean the container of the basculating bean has been removed and has fallen into the basculating site is daily requested for this type of demand
3. INCIDENT DATE IS THE REPORTED DATE BECAUSE THE DAMAGE WAS NOT NOTICED UNTIL EMPLOYEE WENT TO USE IT
4. Around 1500hrs during reel ROU6 movement on route to TLP jetty (nearby Gate B) found oil dripping while moving, due to pressure gauge fitting defected because of wear and tear issue
5. Because of fear of this found on the ground, he contacted and felt a pain in the middle of the back
6. An incredibly unfortunate situation, a bit chaotic at the start because no one knew where the shut-off valve was
7. after 5 pulls , cp released from from TH and accelerated because of trapped pressure
8. The carousel driver checked his settings and another attempt was made using the carouse,l at this point an all stop was called because 2 roller paths had tipped
9. Because of the high winds around the plant and all stop was made and personnel were sent home as the work areas were unsafe to work on
10. On Wednesday 9th August 2023, at approximately 6:38 pm, while TechnipFMC employee was drying his hand on the drying machine at male toilet, he observed smoking coming out from the dryer machine and su

---

## Analysis 4: Metadata Field Coverage & Cross-tabulation

### Field Coverage

| Field | Source | Non-null | % Coverage | Unique Values | Top 5 |
|-------|--------|----------|------------|---------------|-------|
| INCIDENT_TYPE | ENTITY_FACTS | 16522 | 70.9% | 2 | Accident(9400); Near Miss(7122) |
| IMPACT_TYPE | ENTITY_FACTS | 23094 | 99.1% | 9 | Injury(9805); Injury/Illness(3379); Financial Impact(3157); Environment(2211); Damage - Financial im |
| SEVERITY_DESC | ENTITY_FACTS | 23094 | 99.1% | 39 | Injury - 1. First Aid Care(3362); Injury - 2. Medical Treatment Injury / Restricted Work Case / Loss |
| LIKELIHOOD_RANGE | ENTITY_FACTS | 23187 | 99.5% | 21 | 2 - Unlikely(7326); 3 - Possible(5614); 1 - Very Unlikely(3310); 2- Unlikely - 1% to 10%(1003); 3 -  |
| EVENT_DATETIME | ENTITY_FACTS | 5813 | 24.9% | 61 | 00:00.0(2219); 30:00.0(1492); 45:00.0(202); 15:00.0(166); 20:00.0(135) |
| WORKPLACE | ENTITY_FACTS | 23311 | 100.0% | 717 | Sabetta Site, Sabetta, Russia, Asia Pacific(1009); Flexi France, Le Trait, France, Europe(706); Grem |
| CLIENT | ENTITY_FACTS | 22826 | 97.9% | 875 | TECHNIPFMC PLC(2749); TECHNIPFMC(1896); JSC YAMAL LNG(1493); FLEXI FRANCE(1058); N/A - No Vendor(820 |
| WORK_PROCESS | ENTITY_FACTS | 20567 | 88.2% | 223 | Construction(2532); Construction - Installation(2178); Yards(1166); Vessel / Yards(830); Support Ser |
| RISK_COLOR | META_FACTS | 5813 | 24.9% | 3 | Green(4863); Yellow(898); Red(52) |
| CASE_CATEGORIZATION | META_FACTS | 21414 | 91.9% | 117 | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped obje |
| GENERAL_BUSINESS_UNIT | META_FACTS | 5813 | 24.9% | 3 | Subsea(2940); REMS(1727); Surface(1146) |
| SPECIFIC_BUSINESS_UNIT | META_FACTS | 5807 | 24.9% | 16 | Projects(1547); Services(1007); Surface Americas(854); Flexibles(579); Surface Products(364) |
| LIFE_SAVING_RULES | META_FACTS | 5679 | 24.4% | 10 | Not Applicable(2726); Line of Fire - Keep yourself and others out of the line of fire(1568); Driving |
| LOSS_POTENTIAL | META_FACTS | 22855 | 98.0% | 5 | 1.0(9623); 2.0(8181); 3.0(4051); 4.0(645); 5.0(355) |

### WORKPLACE Parsing

#### Top 20 Countries

| Rank | Country | Count | % |
|------|---------|-------|---|
| 1 | USA | 5242 | 22.5% |
| 2 | UK | 4310 | 18.5% |
| 3 | Brazil | 1947 | 8.4% |
| 4 | France | 1476 | 6.3% |
| 5 | Norway | 1232 | 5.3% |
| 6 | Russia | 1113 | 4.8% |
| 7 | India | 843 | 3.6% |
| 8 | Malaysia | 683 | 2.9% |
| 9 | China | 587 | 2.5% |
| 10 | Canada | 377 | 1.6% |
| 11 | zObsolete - Greece | 370 | 1.6% |
| 12 | Singapore | 365 | 1.6% |
| 13 | Angola | 312 | 1.3% |
| 14 | Australia | 294 | 1.3% |
| 15 | zObsolete - Albania | 293 | 1.3% |
| 16 | Indonesia | 276 | 1.2% |
| 17 | Bahrain | 255 | 1.1% |
| 18 | UAE | 217 | 0.9% |
| 19 | Argentina | 204 | 0.9% |
| 20 | Azerbaijan | 176 | 0.8% |

#### Top 20 Cities

| Rank | City | Count | % |
|------|------|-------|---|
| 1 | Aberdeen | 2893 | 12.4% |
| 2 | Houston | 1663 | 7.1% |
| 3 | Le Trait | 1107 | 4.7% |
| 4 | Unknown | 1060 | 4.5% |
| 5 | Rio de Janeiro | 1014 | 4.3% |
| 6 | Sabetta | 1013 | 4.3% |
| 7 | Minot | 620 | 2.7% |
| 8 | Dunfermline | 594 | 2.5% |
| 9 | Odessa | 463 | 2.0% |
| 10 | Stephenville | 458 | 2.0% |
| 11 | Acu | 449 | 1.9% |
| 12 | Newcastle | 422 | 1.8% |
| 13 | Agotnes | 396 | 1.7% |
| 14 | zObsolete - Athens | 370 | 1.6% |
| 15 | Lake Charles | 369 | 1.6% |
| 16 | Channelview | 367 | 1.6% |
| 17 | Singapore | 366 | 1.6% |
| 18 | Theodore | 298 | 1.3% |
| 19 | Johor Bahru | 296 | 1.3% |
| 20 | zObsolete - Tirana | 293 | 1.3% |

#### Top 10 Regions

| Rank | Region | Count | % |
|------|--------|-------|---|
| 1 | Europe | 8560 | 36.7% |
| 2 | North America | 5744 | 24.6% |
| 3 | Asia Pacific | 3463 | 14.9% |
| 4 | South America | 2400 | 10.3% |
| 5 | Africa | 846 | 3.6% |
| 6 | India | 843 | 3.6% |
| 7 | Middle East | 705 | 3.0% |
| 8 | TechnipFMC | 198 | 0.8% |
| 9 | Unknown | 113 | 0.5% |

### INCIDENT_TYPE × IMPACT_TYPE

| INCIDENT_TYPE | Damage | Damage - Financial impact | Environment | Financial Impact | Fire/Explosion | Injury | Injury/Illness | Occupational Illness | Reputation | Unknown | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Accident | 904 | 1021 | 981 | 817 | 67 | 3371 | 1923 | 115 | 147 | 54 | 9400 |
| Near Miss | 833 | 742 | 546 | 552 | 116 | 2650 | 1456 | 36 | 121 | 70 | 7122 |
| Unknown | 15 | 0 | 684 | 1788 | 0 | 3784 | 0 | 99 | 326 | 93 | 6789 |

### Top 10 Countries × IMPACT_TYPE

| Country | Damage | Damage - Financial impact | Environment | Financial Impact | Fire/Explosion | Injury | Injury/Illness | Occupational Illness | Reputation | Unknown | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| USA | 293 | 613 | 418 | 967 | 6 | 1747 | 760 | 55 | 225 | 158 | 5242 |
| UK | 357 | 341 | 696 | 676 | 22 | 1307 | 732 | 70 | 108 | 1 | 4310 |
| Brazil | 106 | 122 | 285 | 186 | 16 | 721 | 481 | 7 | 22 | 1 | 1947 |
| France | 40 | 29 | 242 | 30 | 12 | 739 | 355 | 12 | 11 | 6 | 1476 |
| Norway | 30 | 150 | 67 | 156 | 1 | 373 | 386 | 18 | 47 | 4 | 1232 |
| Russia | 232 | 0 | 34 | 46 | 36 | 760 | 2 | 1 | 0 | 2 | 1113 |
| India | 10 | 25 | 28 | 51 | 4 | 635 | 73 | 8 | 7 | 2 | 843 |
| Malaysia | 147 | 89 | 44 | 98 | 9 | 204 | 81 | 5 | 5 | 1 | 683 |
| China | 44 | 0 | 6 | 47 | 27 | 449 | 2 | 4 | 3 | 5 | 587 |
| Canada | 8 | 10 | 33 | 116 | 1 | 145 | 20 | 7 | 36 | 1 | 377 |

### SEVERITY (binned) × INCIDENT_TYPE

| Severity | Accident | Near Miss | Unknown | Total |
|---|---|---|---|---|
| 1-Negligible | 3122 | 1986 | 2131 | 7239 |
| 2-Minor | 1846 | 1271 | 1148 | 4265 |
| 3-Moderate | 1264 | 1435 | 1150 | 3849 |
| 4-Major | 56 | 94 | 4 | 154 |
| 5-Catastrophic | 110 | 160 | 61 | 331 |
| Unknown | 3002 | 2176 | 2295 | 7473 |

---

## Analysis 5: Queryable Combinations Matrix

### Step 2: Equipment × Injury/Body Part Co-occurrence Matrix

| Equipment | back | injury | hand | cut | pain | finger | head | foot | eye | leg |
|---|---|---|---|---|---|---|---|---|---|---|
| vessel | 780 | 339 | 255 | 184 | 209 | 96 | 181 | 83 | 108 | 81 |
| equipment | 431 | 316 | 177 | 140 | 67 | 67 | 106 | 83 | 59 | 52 |
| crane | 475 | 254 | 165 | 113 | 48 | 78 | 142 | 63 | 69 | 84 |
| pipe | 391 | 345 | 264 | 258 | 81 | 131 | 98 | 98 | 51 | 79 |
| truck | 384 | 143 | 103 | 53 | 34 | 24 | 43 | 56 | 9 | 27 |
| lifting | 357 | 198 | 156 | 101 | 90 | 82 | 83 | 53 | 86 | 52 |
| lift | 399 | 198 | 117 | 88 | 65 | 44 | 81 | 65 | 63 | 67 |
| forklift | 249 | 110 | 54 | 16 | 21 | 24 | 38 | 49 | 7 | 12 |
| vehicle | 289 | 115 | 102 | 24 | 38 | 10 | 50 | 28 | 8 | 16 |
| valve | 231 | 124 | 114 | 60 | 33 | 49 | 67 | 29 | 24 | 28 |
| hose | 215 | 126 | 71 | 82 | 35 | 26 | 44 | 29 | 48 | 21 |
| tool | 179 | 133 | 127 | 102 | 42 | 72 | 69 | 30 | 42 | 16 |
| machine | 151 | 163 | 153 | 131 | 44 | 102 | 41 | 55 | 24 | 19 |
| cable | 152 | 151 | 97 | 123 | 36 | 49 | 43 | 42 | 19 | 21 |
| wire | 250 | 100 | 139 | 116 | 31 | 62 | 66 | 30 | 45 | 26 |

### Step 3: Equipment × Top 10 Countries

| Equipment | USA | UK | Brazil | France | Norway | Russia | India | Malaysia | China | Canada |
|---|---|---|---|---|---|---|---|---|---|---|
| vessel | 123 | 1883 | 114 | 12 | 45 | 7 | 11 | 20 | 12 | 12 |
| equipment | 402 | 617 | 285 | 41 | 214 | 97 | 18 | 33 | 41 | 51 |
| crane | 354 | 832 | 114 | 17 | 130 | 101 | 73 | 63 | 49 | 14 |
| pipe | 486 | 457 | 51 | 9 | 113 | 83 | 143 | 64 | 81 | 19 |
| truck | 675 | 118 | 34 | 38 | 85 | 59 | 28 | 39 | 24 | 99 |
| lifting | 214 | 404 | 74 | 81 | 123 | 76 | 54 | 49 | 56 | 17 |
| lift | 426 | 443 | 31 | 35 | 108 | 50 | 16 | 37 | 43 | 20 |
| forklift | 548 | 148 | 21 | 9 | 192 | 5 | 5 | 34 | 10 | 35 |
| vehicle | 388 | 159 | 51 | 42 | 17 | 53 | 29 | 28 | 7 | 72 |
| valve | 455 | 268 | 44 | 25 | 54 | 29 | 27 | 18 | 25 | 57 |
| hose | 216 | 390 | 38 | 11 | 90 | 26 | 18 | 22 | 45 | 33 |
| tool | 266 | 274 | 92 | 18 | 122 | 34 | 13 | 15 | 11 | 8 |
| machine | 135 | 176 | 146 | 80 | 48 | 14 | 47 | 85 | 29 | 5 |
| cable | 100 | 191 | 104 | 52 | 28 | 84 | 67 | 54 | 53 | 2 |
| wire | 103 | 410 | 55 | 100 | 41 | 17 | 18 | 54 | 27 | 7 |

### Step 4: Deep Dive on Viable Query Candidates (≥20 co-occurrences)

| Status | Equipment | Injury/Body Part | Co-occurrences | With Causal Language | Top CASE_CATEGORIZATION | Severity Distribution |
|--------|-----------|------------------|----------------|---------------------|------------------------|----------------------|
| **STRONG** | vessel | back | 780 | 399 (51%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(203); 2-Minor(124); 3-Moderate(140); 4-Major(11 |
| **STRONG** | crane | back | 475 | 198 (42%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(101); 2-Minor(92); 3-Moderate(100); 4-Major(5); |
| **STRONG** | equipment | back | 431 | 225 (52%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(100); 2-Minor(90); 3-Moderate(84); 4-Major(5);  |
| **STRONG** | lift | back | 399 | 171 (43%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(88); 2-Minor(74); 3-Moderate(93); 4-Major(8); 5 |
| **STRONG** | pipe | back | 391 | 177 (45%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(89); 2-Minor(59); 3-Moderate(87); 4-Major(2); 5 |
| **STRONG** | truck | back | 384 | 124 (32%) | Mechanical - Equipment condition(36); Unknown(29); Basic Organizational - Planni | 1-Negligible(100); 2-Minor(108); 3-Moderate(54); 4-Major(3); |
| **STRONG** | lifting | back | 357 | 143 (40%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(67); 2-Minor(61); 3-Moderate(87); 4-Major(6); 5 |
| **STRONG** | pipe | injury | 345 | 160 (46%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(92); 2-Minor(44); 3-Moderate(71); 4-Major(3); 5 |
| **STRONG** | vessel | injury | 339 | 166 (49%) | Mechanical - Stored energy (dropped objects)(23); Mechanical - Stored energy (pr | 1-Negligible(111); 2-Minor(57); 3-Moderate(93); 4-Major(6);  |
| **STRONG** | equipment | injury | 316 | 136 (43%) | Basic Organizational - Planning and coordination of works(25); Mechanical - Stor | 1-Negligible(76); 2-Minor(61); 3-Moderate(72); 4-Major(5); 5 |
| **STRONG** | vehicle | back | 289 | 111 (38%) | Work environment - Motor Vehicle Road Accident(47); Work environment - Traffic M | 1-Negligible(76); 2-Minor(66); 3-Moderate(47); 5-Catastrophi |
| **STRONG** | pipe | hand | 264 | 99 (38%) | Basic Organizational - Hazard Identification & Risk Assessment(27); Ergonomics - | 1-Negligible(84); 2-Minor(29); 3-Moderate(51); 4-Major(1); 5 |
| **STRONG** | pipe | cut | 258 | 119 (46%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(62); 2-Minor(41); 3-Moderate(49); 5-Catastrophi |
| **STRONG** | vessel | hand | 255 | 122 (48%) | Mechanical - Equipment condition(16); Mechanical - Stored energy (dropped object | 1-Negligible(80); 2-Minor(32); 3-Moderate(62); 4-Major(4); 5 |
| **STRONG** | crane | injury | 254 | 104 (41%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(63); 2-Minor(40); 3-Moderate(67); 4-Major(5); 5 |
| **STRONG** | wire | back | 250 | 117 (47%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(75); 2-Minor(45); 3-Moderate(40); 4-Major(6); 5 |
| **STRONG** | forklift | back | 249 | 77 (31%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(63); 2-Minor(70); 3-Moderate(42); 4-Major(1); 5 |
| **STRONG** | valve | back | 231 | 90 (39%) | Substances  - Hazardous liquids (exposure to / spill / loss of containment /poll | 1-Negligible(61); 2-Minor(30); 3-Moderate(44); 4-Major(1); 5 |
| **STRONG** | hose | back | 215 | 84 (39%) | Mechanical - Stored energy (pressure, tension)(26); Substances  - Hazardous liqu | 1-Negligible(55); 2-Minor(30); 3-Moderate(36); 5-Catastrophi |
| **STRONG** | vessel | pain | 209 | 90 (43%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(70); 2-Minor(25); 3-Moderate(52); 4-Major(1); U |
| **STRONG** | lifting | injury | 198 | 87 (44%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(43); 2-Minor(32); 3-Moderate(50); 4-Major(4); 5 |
| **STRONG** | lift | injury | 198 | 85 (43%) | Basic Organizational - Planning and coordination of works(23); Mechanical - Unco | 1-Negligible(43); 2-Minor(33); 3-Moderate(62); 4-Major(3); 5 |
| **STRONG** | vessel | cut | 184 | 89 (48%) | Mechanical - Equipment condition(18); Mechanical - Stored energy (pressure, tens | 1-Negligible(57); 2-Minor(24); 3-Moderate(35); 5-Catastrophi |
| **STRONG** | vessel | head | 181 | 100 (55%) | Mechanical - Stored energy (dropped objects)(23); Mechanical - Uncontrolled movi | 1-Negligible(57); 2-Minor(34); 3-Moderate(26); 4-Major(3); 5 |
| **STRONG** | tool | back | 179 | 61 (34%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(43); 2-Minor(41); 3-Moderate(42); 4-Major(2); 5 |
| **STRONG** | equipment | hand | 177 | 58 (33%) | Basic Organizational - Hazard Identification & Risk Assessment(17); Mechanical - | 1-Negligible(49); 2-Minor(38); 3-Moderate(45); 4-Major(3); 5 |
| **STRONG** | crane | hand | 165 | 67 (41%) | Ergonomics - Manual handling(16); Mechanical - Uncontrolled moving objects/ part | 1-Negligible(34); 2-Minor(21); 3-Moderate(53); 4-Major(3); 5 |
| **STRONG** | machine | injury | 163 | 68 (42%) | Basic Organizational - Unfamiliar personnel(16); Electrical - Electrical current | 1-Negligible(40); 2-Minor(41); 3-Moderate(38); 4-Major(3); 5 |
| **STRONG** | lifting | hand | 156 | 44 (28%) | Ergonomics - Manual handling(21); Mechanical - Uncontrolled moving objects/ part | 1-Negligible(43); 2-Minor(14); 3-Moderate(46); 4-Major(5); U |
| **STRONG** | machine | hand | 153 | 44 (29%) | Unknown(17); Basic Organizational - Unfamiliar personnel(15); Basic Organization | 1-Negligible(42); 2-Minor(29); 3-Moderate(26); 4-Major(1); 5 |
| **STRONG** | cable | back | 152 | 61 (40%) | Electrical - Electrical current / electrocution / ESD / electromagnetic Fields(2 | 1-Negligible(32); 2-Minor(24); 3-Moderate(45); 4-Major(1); 5 |
| **STRONG** | machine | back | 151 | 57 (38%) | Basic Organizational - Unfamiliar personnel(19); Basic Organizational - Hazard I | 1-Negligible(39); 2-Minor(17); 3-Moderate(31); 4-Major(3); 5 |
| **STRONG** | cable | injury | 151 | 61 (40%) | Electrical - Electrical current / electrocution / ESD / electromagnetic Fields(2 | 1-Negligible(51); 2-Minor(22); 3-Moderate(31); 4-Major(3); 5 |
| **STRONG** | truck | injury | 143 | 49 (34%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(23); 2-Minor(49); 3-Moderate(20); 5-Catastrophi |
| **STRONG** | crane | head | 142 | 56 (39%) | Basic Organizational - Standard Operating Procedures, Procedures & Work instruct | 1-Negligible(37); 2-Minor(34); 3-Moderate(31); 4-Major(3); 5 |
| **STRONG** | equipment | cut | 140 | 73 (52%) | Basic Organizational - Planning and coordination of works(13); Mechanical - Unco | 1-Negligible(34); 2-Minor(29); 3-Moderate(31); 5-Catastrophi |
| **STRONG** | wire | hand | 139 | 44 (32%) | Unknown(16); Basic Organizational - Hazard Identification & Risk Assessment(10); | 1-Negligible(60); 2-Minor(12); 3-Moderate(27); 4-Major(2); 5 |
| **STRONG** | tool | injury | 133 | 49 (37%) | Basic Organizational - Planning and coordination of works(13); Basic Organizatio | 1-Negligible(37); 2-Minor(18); 3-Moderate(41); Unknown(37) |
| **STRONG** | pipe | finger | 131 | 38 (29%) | Basic Organizational - Hazard Identification & Risk Assessment(13); Ergonomics - | 1-Negligible(46); 2-Minor(8); 3-Moderate(30); Unknown(47) |
| **STRONG** | machine | cut | 131 | 42 (32%) | Basic Organizational - Hazard Identification & Risk Assessment(17); Unknown(13); | 1-Negligible(35); 2-Minor(24); 3-Moderate(29); 5-Catastrophi |
| **STRONG** | tool | hand | 127 | 42 (33%) | Basic Organizational - Hazard Identification & Risk Assessment(15); Mechanical - | 1-Negligible(48); 2-Minor(22); 3-Moderate(24); 4-Major(2); 5 |
| **STRONG** | hose | injury | 126 | 73 (58%) | Basic Organizational - Planning and coordination of works(13); Fire & Explosion  | 1-Negligible(38); 2-Minor(26); 3-Moderate(32); Unknown(30) |
| **STRONG** | valve | injury | 124 | 54 (44%) | Mechanical - Stored energy (dropped objects)(11); Mechanical - Uncontrolled movi | 1-Negligible(39); 2-Minor(15); 3-Moderate(33); 4-Major(1); 5 |
| **STRONG** | cable | cut | 123 | 40 (33%) | Basic Organizational - Inadequate Supervision(17); Electrical - Electrical curre | 1-Negligible(34); 2-Minor(12); 3-Moderate(26); 4-Major(1); 5 |
| **STRONG** | lift | hand | 117 | 48 (41%) | Basic Organizational - Hazard Identification & Risk Assessment(16); Mechanical - | 1-Negligible(28); 2-Minor(17); 3-Moderate(30); 4-Major(1); U |
| **STRONG** | wire | cut | 116 | 39 (34%) | Basic Organisational - Equipment Suitability(13); Unknown(10); Mechanical - Stor | 1-Negligible(38); 2-Minor(22); 3-Moderate(10); 5-Catastrophi |
| **STRONG** | vehicle | injury | 115 | 55 (48%) | Work environment - Motor Vehicle Road Accident(16); Work environment - Motor Veh | 1-Negligible(24); 2-Minor(30); 3-Moderate(24); 5-Catastrophi |
| **STRONG** | valve | hand | 114 | 43 (38%) | Basic Organizational - Unfamiliar personnel(12); Unknown(8); Mechanical - Stored | 1-Negligible(41); 2-Minor(22); 3-Moderate(21); 4-Major(1); 5 |
| **STRONG** | crane | cut | 113 | 46 (41%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(26); 2-Minor(13); 3-Moderate(25); 5-Catastrophi |
| **STRONG** | forklift | injury | 110 | 24 (22%) | Basic Organizational - Planning and coordination of works(10); Work environment  | 1-Negligible(30); 2-Minor(34); 3-Moderate(17); 4-Major(2); U |
| **STRONG** | vessel | eye | 108 | 38 (35%) | Use of personal protective equipment(10); Basic Organizational - Use of personal | 1-Negligible(36); 2-Minor(13); 3-Moderate(20); 5-Catastrophi |
| **STRONG** | equipment | head | 106 | 54 (51%) | Mechanical - Stored energy (dropped objects)(8); Mechanical - Equipment conditio | 1-Negligible(31); 2-Minor(20); 3-Moderate(22); 4-Major(1); 5 |
| **STRONG** | truck | hand | 103 | 37 (36%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(26); 2-Minor(19); 3-Moderate(24); Unknown(34) |
| **STRONG** | vehicle | hand | 102 | 37 (36%) | Work environment - Traffic Management / Routes / Pedestrian path(14); Work envir | 1-Negligible(30); 2-Minor(16); 3-Moderate(17); 5-Catastrophi |
| **STRONG** | tool | cut | 102 | 36 (35%) | Mechanical - Stored energy (pressure, tension)(8); Unknown(6); Mechanical - Unco | 1-Negligible(37); 2-Minor(17); 3-Moderate(17); 5-Catastrophi |
| **STRONG** | machine | finger | 102 | 24 (24%) | Basic Organizational - Use of personal protective equipment(10); Mechanical - Un | 1-Negligible(33); 2-Minor(14); 3-Moderate(20); Unknown(35) |
| **STRONG** | lifting | cut | 101 | 48 (48%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(22); 2-Minor(18); 3-Moderate(17); 5-Catastrophi |
| **STRONG** | wire | injury | 100 | 39 (39%) | Mechanical - Stored energy (dropped objects)(11); Ergonomics - Manual handling(8 | 1-Negligible(37); 2-Minor(16); 3-Moderate(22); 4-Major(2); 5 |
| **STRONG** | pipe | head | 98 | 40 (41%) | Mechanical - Stored energy (dropped objects)(11); Mechanical - Equipment conditi | 1-Negligible(20); 2-Minor(23); 3-Moderate(20); 4-Major(1); 5 |
| **STRONG** | pipe | foot | 98 | 49 (50%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(18); 2-Minor(15); 3-Moderate(32); 5-Catastrophi |
| **STRONG** | cable | hand | 97 | 24 (25%) | Ergonomics - Manual handling(11); Basic Organizational - Use of personal protect | 1-Negligible(36); 2-Minor(4); 3-Moderate(23); 4-Major(2); 5- |
| **STRONG** | vessel | finger | 96 | 41 (43%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(33); 2-Minor(10); 3-Moderate(31); 4-Major(1); 5 |
| **STRONG** | lifting | pain | 90 | 22 (24%) | Ergonomics - Manual handling(26); Unknown(14); Manual handling(9) | 1-Negligible(31); 2-Minor(12); 3-Moderate(20); Unknown(27) |
| **STRONG** | lift | cut | 88 | 47 (53%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(19); 2-Minor(15); 3-Moderate(19); Unknown(35) |
| **STRONG** | lifting | eye | 86 | 31 (36%) | Mechanical - Stored energy (pressure, tension)(13); Basic Organizational - Plann | 1-Negligible(16); 2-Minor(18); 3-Moderate(19); 4-Major(3); U |
| **STRONG** | crane | leg | 84 | 37 (44%) | Basic Organizational - Hazard Identification & Risk Assessment(18); Mechanical - | 1-Negligible(16); 2-Minor(18); 3-Moderate(25); 4-Major(1); 5 |
| **STRONG** | vessel | foot | 83 | 37 (45%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(20); 2-Minor(9); 3-Moderate(24); 5-Catastrophic |
| **STRONG** | equipment | foot | 83 | 39 (47%) | Mechanical - Stored energy (dropped objects)(9); Electrical - Electrical current | 1-Negligible(17); 2-Minor(21); 3-Moderate(23); 5-Catastrophi |
| **STRONG** | lifting | head | 83 | 43 (52%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(18); 2-Minor(24); 3-Moderate(16); 4-Major(4); 5 |
| **STRONG** | lifting | finger | 82 | 19 (23%) | Ergonomics - Manual handling(17); Mechanical - Uncontrolled moving objects/ part | 1-Negligible(20); 2-Minor(6); 3-Moderate(27); 4-Major(1); Un |
| **STRONG** | hose | cut | 82 | 26 (32%) | Mechanical - Stored energy (pressure, tension)(14); Mechanical - Equipment condi | 1-Negligible(27); 2-Minor(5); 3-Moderate(19); Unknown(31) |
| **STRONG** | vessel | leg | 81 | 42 (52%) | Basic Organizational - Standard Operating Procedures, Procedures & Work instruct | 1-Negligible(24); 2-Minor(12); 3-Moderate(19); 5-Catastrophi |
| **STRONG** | pipe | pain | 81 | 35 (43%) | Ergonomics - Manual handling(11); Work environment - Falls, slips and trips on s | 1-Negligible(23); 2-Minor(8); 3-Moderate(19); Unknown(31) |
| **STRONG** | lift | head | 81 | 33 (41%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(20); 2-Minor(18); 3-Moderate(21); 4-Major(2); 5 |
| **STRONG** | pipe | leg | 79 | 33 (42%) | Basic Organizational - Hazard Identification & Risk Assessment(14); Work environ | 1-Negligible(19); 2-Minor(8); 3-Moderate(20); 5-Catastrophic |
| **STRONG** | crane | finger | 78 | 22 (28%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(16); 2-Minor(12); 3-Moderate(16); 4-Major(1); 5 |
| **STRONG** | tool | finger | 72 | 13 (18%) | Basic Organizational - Hazard Identification & Risk Assessment(11); Unknown(6);  | 1-Negligible(30); 2-Minor(10); 3-Moderate(17); Unknown(15) |
| **STRONG** | hose | hand | 71 | 32 (45%) | Basic Organizational - Unfamiliar personnel(15); Unknown(7); Mechanical - Stored | 1-Negligible(24); 2-Minor(12); 3-Moderate(12); Unknown(23) |
| **STRONG** | crane | eye | 69 | 21 (30%) | Mechanical - Stored energy (pressure, tension)(7); Mechanical - Uncontrolled mov | 1-Negligible(24); 2-Minor(15); 3-Moderate(16); Unknown(14) |
| **STRONG** | tool | head | 69 | 25 (36%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(28); 2-Minor(16); 3-Moderate(17); 4-Major(1); U |
| **STRONG** | equipment | pain | 67 | 25 (37%) | Basic Organizational - Planning and coordination of works(7); Ergonomics - Manua | 1-Negligible(16); 2-Minor(13); 3-Moderate(16); 4-Major(1); U |
| **STRONG** | equipment | finger | 67 | 21 (31%) | Basic Organizational - Hazard Identification & Risk Assessment(10); Mechanical - | 1-Negligible(21); 2-Minor(7); 3-Moderate(22); Unknown(17) |
| **STRONG** | lift | leg | 67 | 32 (48%) | Basic Organizational - Hazard Identification & Risk Assessment(12); Mechanical - | 1-Negligible(10); 2-Minor(17); 3-Moderate(23); 4-Major(1); 5 |
| **STRONG** | valve | head | 67 | 26 (39%) | Mechanical - Equipment condition(12); Stored energy (pressure, tension)(7); Mech | 1-Negligible(21); 2-Minor(10); 3-Moderate(11); 4-Major(1); 5 |
| **STRONG** | wire | head | 66 | 30 (45%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(13); 2-Minor(16); 3-Moderate(15); 4-Major(3); 5 |
| **STRONG** | lift | pain | 65 | 23 (35%) | Ergonomics - Manual handling(15); Manual handling(10); Unknown(8) | 1-Negligible(23); 2-Minor(6); 3-Moderate(21); Unknown(15) |
| **STRONG** | lift | foot | 65 | 19 (29%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(13); 2-Minor(12); 3-Moderate(21); 4-Major(1); 5 |
| **STRONG** | crane | foot | 63 | 16 (25%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(21); 2-Minor(8); 3-Moderate(19); 5-Catastrophic |
| **STRONG** | lift | eye | 63 | 20 (32%) | Basic Organizational - Planning and coordination of works(9); Basic Organisation | 1-Negligible(15); 2-Minor(13); 3-Moderate(16); 4-Major(2); 5 |
| **STRONG** | wire | finger | 62 | 11 (18%) | Ergonomics - Manual handling(7); Basic Organisational - Equipment Suitability(7) | 1-Negligible(31); 2-Minor(8); 3-Moderate(11); Unknown(12) |
| **STRONG** | valve | cut | 60 | 19 (32%) | Mechanical - Stored energy (pressure, tension)(10); Basic Organizational - Use o | 1-Negligible(22); 2-Minor(5); 3-Moderate(14); Unknown(19) |
| **STRONG** | equipment | eye | 59 | 22 (37%) | Mechanical - Stored energy (pressure, tension)(10); Basic Organizational - Plann | 1-Negligible(18); 2-Minor(11); 3-Moderate(12); 5-Catastrophi |
| **STRONG** | truck | foot | 56 | 18 (32%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(19); 2-Minor(13); 3-Moderate(11); 5-Catastrophi |
| **STRONG** | machine | foot | 55 | 12 (22%) | Basic Organizational - Unfamiliar personnel(8); Mechanical - Unprotected/unguard | 1-Negligible(11); 2-Minor(8); 3-Moderate(16); 4-Major(1); Un |
| **STRONG** | forklift | hand | 54 | 15 (28%) | Basic Organizational - Planning and coordination of works(7); Basic Organization | 1-Negligible(22); 2-Minor(9); 3-Moderate(8); 5-Catastrophic( |
| **STRONG** | truck | cut | 53 | 27 (51%) | Basic Organizational - Planning and coordination of works(9); Work environment - | 1-Negligible(8); 2-Minor(13); 3-Moderate(8); 5-Catastrophic( |
| **STRONG** | lifting | foot | 53 | 18 (34%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(15); 2-Minor(9); 3-Moderate(16); 5-Catastrophic |
| **STRONG** | equipment | leg | 52 | 29 (56%) | Mechanical - Stored energy (dropped objects)(13); Mechanical - Uncontrolled movi | 1-Negligible(16); 2-Minor(8); 3-Moderate(14); 4-Major(1); 5- |
| **STRONG** | lifting | leg | 52 | 26 (50%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(7); 2-Minor(10); 3-Moderate(19); 5-Catastrophic |
| **STRONG** | pipe | eye | 51 | 25 (49%) | Mechanical - Stored energy (pressure, tension)(8); Basic Organizational - Use of | 1-Negligible(14); 2-Minor(6); 3-Moderate(15); 5-Catastrophic |
| **STRONG** | vehicle | head | 50 | 18 (36%) | Work environment - Traffic Management / Routes / Pedestrian path(9); Motor Vehic | 1-Negligible(10); 2-Minor(19); 3-Moderate(4); 5-Catastrophic |
| VIABLE | forklift | foot | 49 | 15 (31%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(8); 2-Minor(14); 3-Moderate(9); 4-Major(1); 5-C |
| VIABLE | valve | finger | 49 | 12 (24%) | Basic Organizational - Use of personal protective equipment(6); Basic Organisati | 1-Negligible(22); 2-Minor(4); 3-Moderate(9); Unknown(14) |
| VIABLE | cable | finger | 49 | 11 (22%) | Ergonomics - Manual handling(8); Basic Organizational - Use of personal protecti | 1-Negligible(20); 2-Minor(3); 3-Moderate(7); Unknown(19) |
| VIABLE | crane | pain | 48 | 16 (33%) | Ergonomics - Manual handling(10); Work environment - Falls, slips and trips on s | 1-Negligible(14); 2-Minor(6); 3-Moderate(10); Unknown(18) |
| VIABLE | hose | eye | 48 | 18 (38%) | Mechanical - Stored energy (pressure, tension)(13); Mechanical - Equipment condi | 1-Negligible(21); 2-Minor(9); 3-Moderate(5); Unknown(13) |
| VIABLE | wire | eye | 45 | 20 (44%) | Mechanical - Stored energy (dropped objects)(9); Mechanical - Stored energy (pre | 1-Negligible(19); 2-Minor(2); 3-Moderate(7); 4-Major(2); 5-C |
| VIABLE | lift | finger | 44 | 15 (34%) | Ergonomics - Manual handling(8); Mechanical - Unprotected/unguarded moving machi | 1-Negligible(13); 2-Minor(7); 3-Moderate(10); Unknown(14) |
| VIABLE | hose | head | 44 | 18 (41%) | Unknown(6); Substances  - Hazardous liquids (exposure to / spill / loss of conta | 1-Negligible(11); 2-Minor(9); 3-Moderate(9); Unknown(15) |
| VIABLE | machine | pain | 44 | 15 (34%) | Unknown(10); Basic Organizational - Unfamiliar personnel(5); Work environment -  | 1-Negligible(18); 2-Minor(6); 3-Moderate(12); Unknown(8) |
| VIABLE | truck | head | 43 | 7 (16%) | Mechanical - Equipment condition(9); Basic Organizational - Hazard Identificatio | 1-Negligible(9); 2-Minor(19); 3-Moderate(7); Unknown(8) |
| VIABLE | cable | head | 43 | 16 (37%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(11); 2-Minor(7); 3-Moderate(7); 5-Catastrophic( |
| VIABLE | tool | pain | 42 | 16 (38%) | Ergonomics - Manual handling(6); Manual handling(5); Unknown(4) | 1-Negligible(12); 2-Minor(9); 3-Moderate(12); Unknown(9) |
| VIABLE | tool | eye | 42 | 8 (19%) | Mechanical - Stored energy (pressure, tension)(11); Basic Organizational - Hazar | 1-Negligible(14); 2-Minor(9); 3-Moderate(7); 5-Catastrophic( |
| VIABLE | cable | foot | 42 | 18 (43%) | Electrical - Electrical current / electrocution / ESD / electromagnetic Fields(9 | 1-Negligible(11); 2-Minor(4); 3-Moderate(13); 5-Catastrophic |
| VIABLE | machine | head | 41 | 11 (27%) | Unknown(6); Basic Organizational - Planning and coordination of works(5); Fire & | 1-Negligible(13); 2-Minor(10); 3-Moderate(6); 4-Major(1); 5- |
| VIABLE | forklift | head | 38 | 13 (34%) | Unknown(4); Uncontrolled moving objects/ parts (struck by other than machine par | 1-Negligible(7); 2-Minor(15); 3-Moderate(6); Unknown(10) |
| VIABLE | vehicle | pain | 38 | 13 (34%) | Unknown(8); Work environment - Traffic Management / Routes / Pedestrian path(6); | 1-Negligible(16); 2-Minor(5); 3-Moderate(6); 5-Catastrophic( |
| VIABLE | cable | pain | 36 | 9 (25%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(9); 2-Minor(1); 3-Moderate(7); 5-Catastrophic(1 |
| VIABLE | hose | pain | 35 | 11 (31%) | Unknown(6); Ergonomics - Manual handling(5); Falls, slips and trips on same leve | 1-Negligible(12); 2-Minor(7); 3-Moderate(8); Unknown(8) |
| VIABLE | truck | pain | 34 | 12 (35%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(9); 2-Minor(7); 3-Moderate(10); Unknown(8) |
| VIABLE | valve | pain | 33 | 6 (18%) | Ergonomics - Posture (constraint or restricted environment)(5); Ergonomics - Man | 1-Negligible(11); 2-Minor(6); 3-Moderate(9); Unknown(7) |
| VIABLE | wire | pain | 31 | 11 (35%) | Unknown(4); Ergonomics - Manual handling(4); Manual handling(2) | 1-Negligible(13); 2-Minor(5); 3-Moderate(8); 4-Major(1); Unk |
| VIABLE | tool | foot | 30 | 10 (33%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(9); 2-Minor(8); 3-Moderate(8); Unknown(5) |
| VIABLE | wire | foot | 30 | 15 (50%) | Electrical - Electrical current / electrocution / ESD / electromagnetic Fields(9 | 1-Negligible(12); 2-Minor(4); 3-Moderate(4); 5-Catastrophic( |
| VIABLE | valve | foot | 29 | 10 (34%) | Work environment - Falls, slips and trips on same level (without potential to fa | 1-Negligible(9); 2-Minor(2); 3-Moderate(11); 5-Catastrophic( |
| VIABLE | hose | foot | 29 | 6 (21%) | Basic Organizational - Hazard Identification & Risk Assessment(8); Basic Organiz | 1-Negligible(3); 2-Minor(6); 3-Moderate(8); Unknown(12) |
| VIABLE | vehicle | foot | 28 | 10 (36%) | Work environment - Traffic Management / Routes / Pedestrian path(11); Basic Orga | 1-Negligible(6); 2-Minor(7); 3-Moderate(9); Unknown(6) |
| VIABLE | valve | leg | 28 | 14 (50%) | Unknown(6); Basic Organizational - Hazard Identification & Risk Assessment(4); B | 1-Negligible(5); 2-Minor(3); 3-Moderate(9); 4-Major(1); Unkn |
| VIABLE | truck | leg | 27 | 11 (41%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(5); 2-Minor(4); 3-Moderate(11); 5-Catastrophic( |
| VIABLE | hose | finger | 26 | 9 (35%) | Basic Organisational - Equipment Suitability(4); Unknown(3); Mechanical - Unprot | 1-Negligible(7); 2-Minor(8); 3-Moderate(5); Unknown(6) |
| VIABLE | wire | leg | 26 | 13 (50%) | Mechanical - Equipment condition(7); Basic Organizational - Inadequate Supervisi | 1-Negligible(9); 2-Minor(3); 3-Moderate(5); Unknown(9) |
| VIABLE | truck | finger | 24 | 10 (42%) | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine pa | 1-Negligible(7); 3-Moderate(6); Unknown(11) |
| VIABLE | forklift | finger | 24 | 8 (33%) | Basic Organizational - Use of personal protective equipment(4); Basic Organizati | 1-Negligible(7); 2-Minor(2); 3-Moderate(8); Unknown(7) |
| VIABLE | vehicle | cut | 24 | 13 (54%) | Basic Organizational - Unfamiliar personnel(5); Basic Organizational - Hazard Id | 1-Negligible(7); 2-Minor(1); 3-Moderate(3); 5-Catastrophic(1 |
| VIABLE | valve | eye | 24 | 12 (50%) | Mechanical - Stored energy (pressure, tension)(6); Basic Organizational - Unfami | 1-Negligible(5); 2-Minor(4); 3-Moderate(9); Unknown(6) |
| VIABLE | machine | eye | 24 | 4 (17%) | Mechanical - Stored energy (pressure, tension)(6); Basic Organizational - Use of | 1-Negligible(5); 2-Minor(7); 3-Moderate(4); Unknown(8) |
| VIABLE | forklift | pain | 21 | 4 (19%) | Unknown(4); Manual handling(3); Basic Organizational - Hazard Identification & R | 1-Negligible(10); 2-Minor(1); 3-Moderate(5); Unknown(5) |
| VIABLE | hose | leg | 21 | 8 (38%) | Unknown(3); Substances  - Hazardous liquids (exposure to / spill / loss of conta | 1-Negligible(10); 2-Minor(2); 3-Moderate(4); 4-Major(2); Unk |
| VIABLE | cable | leg | 21 | 9 (43%) | Basic Organizational - Hazard Identification & Risk Assessment(4); Work environm | 1-Negligible(7); 3-Moderate(6); 5-Catastrophic(1); Unknown(7 |

---

## Analysis 6: Surface Form Variation Audit

### Equipment Surface Form Variants

| Base Term | Variant | Count |
|-----------|---------|-------|
| vessel | vessel | 2604 |
| equipment | equipment | 2320 |
| crane | crane | 2297 |
| crane | CRANE | 2297 |
| crane | overhead crane | 185 |
| crane | mobile crane | 67 |
| crane | gantry crane | 63 |
| crane | crawler crane | 53 |
| crane | tower crane | 19 |
| crane | pedestal crane | 2 |
| pipe | pipe | 2145 |
| pipe | PIPE | 2145 |
| pipe | pipeline | 261 |
| pipe | piping | 225 |
| pipe | pipework | 74 |
| truck | truck | 1724 |
| truck | TRUCK | 1724 |
| truck | trucks | 106 |
| truck | lorry | 63 |
| truck | HGV | 6 |
| lifting | lifting | 1662 |
| lift | lift | 1621 |
| forklift | forklift | 1321 |
| forklift | FORKLIFT | 1321 |
| forklift | FLT | 104 |
| forklift | fork lift | 74 |
| forklift | \d+[Tt]\s*forklift | 44 |
| forklift | \d+\s*[Tt]on\s*forklift | 18 |
| forklift | fork-lift | 5 |
| vehicle | vehicle | 1279 |
| vehicle | VEHICLE | 1279 |
| vehicle | vehicles | 243 |
| vehicle | company vehicle | 212 |
| vehicle | motor vehicle | 39 |
| valve | valve | 1245 |
| valve | VALVE | 1245 |
| valve | ball valve | 55 |
| valve | gate valve | 50 |
| valve | check valve | 45 |
| valve | relief valve | 37 |
| valve | safety valve | 20 |
| valve | control valve | 18 |
| valve | choke valve | 4 |
| hose | hose | 1167 |
| hose | HOSE | 1167 |
| hose | hoses | 411 |
| hose | hydraulic hose | 151 |
| tool | tool | 1055 |
| tool | TOOL | 1055 |
| tool | tools | 228 |
| tool | hand tool | 11 |
| tool | power tool | 2 |
| machine | machine | 1054 |
| cable | cable | 1021 |
| cable | CABLE | 1021 |
| cable | cables | 240 |
| cable | wire rope | 119 |
| cable | steel cable | 16 |
| wire | wire | 1018 |
| door | door | 1006 |
| platform | platform | 971 |
| rigging | rigging | 956 |
| pallet | pallet | 906 |
| cutting | cutting | 679 |

### Injury Surface Form Variants

| Base Term | Variant | Count |
|-----------|---------|-------|
| back | back | 3651 |
| injury | injury | 2527 |
| hand | hand | 2305 |
| cut | cut | 1485 |
| pain | pain | 1284 |
| pain | sore | 107 |
| pain | painful | 38 |
| pain | soreness | 31 |
| pain | ache | 21 |
| pain | aching | 3 |
| finger | finger | 1263 |
| head | head | 1028 |
| foot | foot | 893 |
| eye | eye | 661 |
| leg | leg | 618 |

### Fragmentation Scores

Higher = more surface form variation = better ER stress-test candidate

| Entity | Type | Distinct Forms | Total Mentions | Fragmentation Score |
|--------|------|---------------|----------------|---------------------|
| pain | Injury | 6 | 1484 | 0.0040 |
| valve | Equipment | 9 | 2719 | 0.0033 |
| forklift | Equipment | 7 | 2887 | 0.0024 |
| tool | Equipment | 5 | 2351 | 0.0021 |
| cable | Equipment | 5 | 2417 | 0.0021 |
| vehicle | Equipment | 5 | 3052 | 0.0016 |
| leg | Injury | 1 | 618 | 0.0016 |
| crane | Equipment | 8 | 4983 | 0.0016 |
| eye | Injury | 1 | 661 | 0.0015 |
| cutting | Equipment | 1 | 679 | 0.0015 |
| hose | Equipment | 4 | 2896 | 0.0014 |
| truck | Equipment | 5 | 3623 | 0.0014 |
| foot | Injury | 1 | 893 | 0.0011 |
| pallet | Equipment | 1 | 906 | 0.0011 |
| rigging | Equipment | 1 | 956 | 0.0010 |
| pipe | Equipment | 5 | 4850 | 0.0010 |
| platform | Equipment | 1 | 971 | 0.0010 |
| door | Equipment | 1 | 1006 | 0.0010 |
| wire | Equipment | 1 | 1018 | 0.0010 |
| head | Injury | 1 | 1028 | 0.0010 |
| machine | Equipment | 1 | 1054 | 0.0009 |
| finger | Injury | 1 | 1263 | 0.0008 |
| cut | Injury | 1 | 1485 | 0.0007 |
| lift | Equipment | 1 | 1621 | 0.0006 |
| lifting | Equipment | 1 | 1662 | 0.0006 |
| hand | Injury | 1 | 2305 | 0.0004 |
| equipment | Equipment | 1 | 2320 | 0.0004 |
| injury | Injury | 1 | 2527 | 0.0004 |
| vessel | Equipment | 1 | 2604 | 0.0004 |
| back | Injury | 1 | 3651 | 0.0003 |

---

## Summary & Query Design Implications

### 1. Top 10 Strong Query Candidate Entity Combinations

These have the highest co-occurrence counts and serve as two-hop query anchors.

| Rank | Equipment | Injury/Body Part | Co-occurrences | Causal Coverage |
|------|-----------|------------------|----------------|-----------------|
| 1 | vessel | back | 780 | 399 (51%) |
| 2 | crane | back | 475 | 198 (42%) |
| 3 | equipment | back | 431 | 225 (52%) |
| 4 | lift | back | 399 | 171 (43%) |
| 5 | pipe | back | 391 | 177 (45%) |
| 6 | truck | back | 384 | 124 (32%) |
| 7 | lifting | back | 357 | 143 (40%) |
| 8 | pipe | injury | 345 | 160 (46%) |
| 9 | vessel | injury | 339 | 166 (49%) |
| 10 | equipment | injury | 316 | 136 (43%) |

### 2. Top 5 Entity Resolution Stress-Test Candidates

Highest fragmentation scores — most surface form variation.

| Rank | Entity | Type | Forms | Total Mentions | Frag Score |
|------|--------|------|-------|----------------|------------|
| 1 | pain | Injury | 6 | 1484 | 0.0040 |
| 2 | valve | Equipment | 9 | 2719 | 0.0033 |
| 3 | forklift | Equipment | 7 | 2887 | 0.0024 |
| 4 | tool | Equipment | 5 | 2351 | 0.0021 |
| 5 | cable | Equipment | 5 | 2417 | 0.0021 |

### 3. Causal Query Feasibility Assessment

- **25.7%** of records contain explicit causal language
- Total records with causal phrases: 5998 / 23311

**CASE_CATEGORIZATION clusters with richest causal language (top 15 by causal %):**

| CASE_CATEGORIZATION | Causal Records | Total | Causal % |
|---------------------|----------------|-------|----------|
| Fire & Explosion - Accumulation / Presence of explosive atmosphere | 20 | 37 | 54.1% |
| Fire & Explosion - Explosives / potential explosives | 18 | 35 | 51.4% |
| Electrical | 28 | 60 | 46.7% |
| Physical - Hot/cold surfaces or media | 36 | 90 | 40.0% |
| Fire & Explosion - Flammable solids, liquids and gases | 152 | 408 | 37.3% |
| Electrical - Electrical current / electrocution / ESD / electromagneti | 113 | 311 | 36.3% |
| Work environment - Climate (Heat/Cold/Humidity) | 65 | 189 | 34.4% |
| Difficult/Hindered operability of tools and equipment | 18 | 54 | 33.3% |
| Mechanical - Unprotected/unguarded moving machine parts (struck by/cau | 76 | 229 | 33.2% |
| Basic Organizational - Unfamiliar personnel | 106 | 321 | 33.0% |
| Substances  - Hazardous gases, vapours, aerosols (exposure to / spill  | 42 | 128 | 32.8% |
| Stored energy (pressure, tension) | 75 | 229 | 32.8% |
| Mechanical - Stored energy (dropped objects) | 376 | 1158 | 32.5% |
| Basic Organizational - Standard Operating Procedures, Procedures & Wor | 284 | 878 | 32.3% |
| Fire & Explosion - Uncontrolled chemical or physical reaction | 40 | 124 | 32.3% |

### 4. Metadata Gaps

Fields with coverage issues that limit query reliability:

- **INCIDENT_TYPE**: 70.9% coverage (6789 missing)
- **EVENT_DATETIME**: 24.9% coverage (17498 missing)
- **RISK_COLOR**: 24.9% coverage (17498 missing)
- **GENERAL_BUSINESS_UNIT**: 24.9% coverage (17498 missing)

### 5. Recommended Query Design Space

A shortlist of entity/relation/metadata combinations for the 30 benchmark queries:

#### Single-hop queries (10): Entity resolution + direct lookup
- Use high-fragmentation entities for ER stress tests
- Use high-frequency equipment terms for direct entity lookup
- Use WORKPLACE parsing for location queries
- Use INCIDENT_TYPE / IMPACT_TYPE for type classification queries

#### Two-hop queries (10): Entity-to-entity traversal
- Equipment → Injury/Body Part (use strong candidates from matrix)
- Equipment → Location (country-level)
- CASE_CATEGORIZATION → Equipment → Location
- Injury → Severity → CASE_CATEGORIZATION

#### Three-hop causal queries (7): Multi-entity causal chains
- Equipment failure → Causal mechanism → Injury → Severity
- Focus on CC clusters with high causal language density
- Use 'due to', 'caused by', 'resulted in' as relation signals

#### Similarity queries (3): Pattern matching across incidents
- Similar incidents by equipment + location + severity
- Similar incidents by CASE_CATEGORIZATION + injury type
- Similar causal chains across different locations

#### Specific Suggested Combinations

| # | Query Type | Entity/Relation Combination | Expected Data Support |
|---|------------|---------------------------|----------------------|
| 1 | 1-hop ER | forklift surface forms → canonical entity | High fragmentation |
| 2 | 1-hop ER | crane surface forms → canonical entity | Multiple compound forms |
| 3 | 1-hop ER | pipe/pipeline/piping → canonical entity | High fragmentation |
| 4 | 1-hop lookup | All incidents at [top country] | High count |
| 5 | 1-hop lookup | All incidents involving [top equipment] | High count |
| 6 | 1-hop lookup | Incidents by CASE_CATEGORIZATION cluster | Well-distributed |
| 7 | 1-hop lookup | Incidents by severity level | 5-bin distribution |
| 8 | 1-hop ER | burn/burned/burnt/scald → canonical injury | Common injury type |
| 9 | 1-hop lookup | Incidents by IMPACT_TYPE | Good coverage |
| 10 | 1-hop ER | laceration/cut/gash → canonical injury | High overlap |
| 11 | 2-hop | vessel → involved → back | 780 co-occurrences |
| 12 | 2-hop | crane → involved → back | 475 co-occurrences |
| 13 | 2-hop | equipment → involved → back | 431 co-occurrences |
| 14 | 2-hop | lift → involved → back | 399 co-occurrences |
| 15 | 2-hop | pipe → involved → back | 391 co-occurrences |
| 16 | 2-hop | truck → involved → back | 384 co-occurrences |
| 17 | 2-hop | lifting → involved → back | 357 co-occurrences |
| 18 | 2-hop | pipe → involved → injury | 345 co-occurrences |
| 19 | 2-hop | vessel → involved → injury | 339 co-occurrences |
| 20 | 2-hop | equipment → involved → injury | 316 co-occurrences |
| 21 | 3-hop causal | Equipment failure → caused_by → [mechanism] → resulted_in → injury | Causal language in 26% records |
| 22 | 3-hop causal | [Equipment] → occurred_at → [Location] → involved → [Injury] | Cross-entity chain |
| 23 | 3-hop causal | [CC category] → caused_by → [Equipment] → resulted_in → [Severity] | CC-anchored chain |
| 24 | 3-hop causal | falls/slips → caused_by → [surface condition] → affected → [body part] | Rich CC cluster |
| 25 | 3-hop causal | mechanical failure → caused_by → [equipment] → resulted_in → [damage type] | Mechanical cluster |
| 26 | 3-hop causal | dropped object → caused_by → [lifting equipment] → affected → [body part] | Dropped object cluster |
| 27 | 3-hop causal | vehicle incident → occurred_at → [location] → resulted_in → [injury type] | Transportation cluster |
| 28 | similarity | Similar incidents: same equipment + same CC + different location | Pattern matching |
| 29 | similarity | Similar incidents: same injury + same severity + different equipment | Injury-anchored |
| 30 | similarity | Similar causal chains across regions | Cross-region patterns |
