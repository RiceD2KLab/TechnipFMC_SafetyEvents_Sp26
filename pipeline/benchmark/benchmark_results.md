# L1 Benchmark Query Results

**Generated:** 2026-03-30
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
| AG-07 | What are the most common body parts affected across all incidents? | Aggregation | ✅ | 19851 incidents, 1980 body_part values, top: left hand |
| AG-08 | What are the most common injury types across all incidents? | Aggregation | ✅ | 19851 incidents, 1324 injury_type values, top: injuries |
| AG-09 | Which organizations report the most incidents? | Aggregation | ✅ | 19851 incidents, 8447 organization values, top: TECHNIPFMC |
| AG-10 | What is the annual trend of manual handling incidents? | Aggregation | ✅ | 760 incidents across 108 months |
| AG-11 | What root cause categories are most common in high-severity incidents? | Aggregation | ✅ | 167 incidents, 22 root_cause_category values, top: Stored energy (dropped objects) |
| AG-12 | How do incidents break down by impact type over the years? | Aggregation | ✅ | Crosstab: 10 year values x 10 impact_type values |
| AG-13 | What is the trend of fire/explosion incidents over time? | Aggregation | ✅ | 121 incidents across 16 months |
| AG-14 | Which cities have the highest incident counts? | Aggregation | ✅ | 19851 incidents, 230 location values, top: Aberdeen |
| AG-15 | How do incidents distribute across work process categories? | Aggregation | ✅ | 19851 incidents, 65 root_cause_category values, top: Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) |
| AG-16 | What is the year-over-year trend of eye injuries? | Aggregation | ✅ | 492 incidents across 103 months |
| AG-17 | What are the most common injury types at construction sites? | Aggregation | ✅ | 5357 incidents, 583 injury_type values, top: injuries |
| AG-18 | Which clients report the most high-severity incidents? | Aggregation | ✅ | 167 incidents, 247 organization values, top: TECHNIPFMC |
| AG-19 | What is the year-over-year trend of fracture injuries? | Aggregation | ✅ | 228 incidents across 78 months |
| AG-20 | What equipment is most common in incidents at Aberdeen? | Aggregation | ✅ | 2501 incidents, 3183 equipment values, top: crane |
| AG-21 | How do incidents break down by work process and risk color? | Aggregation | ✅ | Crosstab: 224 work_process values x 4 risk_color values |
| AG-22 | How do the top countries compare on accident vs near-miss ratios? | Aggregation | ✅ | Crosstab: 233 loc_country values x 3 incident_type values |
| AG-23 | How do root cause categories distribute across business units? | Aggregation | ✅ | Crosstab: 4 business_unit values x 118 case_categorization values |
| AG-24 | How does severity distribution vary by year? | Aggregation | ✅ | Crosstab: 10 year values x 6 severity_bin values |
| AG-25 | What is the year-over-year trend of contusion/bruise injuries? | Aggregation | ✅ | 360 incidents across 86 months |
| AG-26 | How do incident counts compare across the top 10 operating centers? | Aggregation | ✅ | Crosstab: 276 operating_center values x 3 incident_type values |
| CJ-01 | Which incidents match the pattern of corrosion-induced equipment failure leading to fire? | Conjunctive | ✅ | 34,499 causal edges; 800 for fire/explosion |
| CJ-02 | Find all high-severity incidents where a crane was involved AND a back injury was sustained AND the location was offshore. | Conjunctive | ✅ | 0 incidents |
| CJ-03 | Identify incidents where maintenance procedures failed, involving pipe equipment, resulting in environmental impact at locations in the Middle East. | Conjunctive | ✅ | 0 incidents |
| CJ-04 | Which equipment types have caused both injuries AND near-misses at the same location within the same year? | Conjunctive | ✅ | 539 dual-risk equipment/location/year combos |
| CJ-05 | Find the causal chain pattern: procedural non-compliance -> dropped object -> head/hand injury. How many incidents match? | Conjunctive | ✅ | 324 incidents; 12 procedural causal edges |
| CJ-06 | Which incidents involve the co-occurrence of slip/fall events AND vehicle/transportation equipment at construction sites? | Conjunctive | ✅ | 16 incidents |
| CJ-07 | What are the primary effects of corrosion on equipment and incidents in the dataset? | Conjunctive | ✅ | 137 corrosion causal edges across 104 incidents |
| CJ-08 | Find crane incidents in the UK resulting in fractures. | Conjunctive | ✅ | 0 incidents |
| CJ-09 | Find forklift incidents at construction sites with severity >= 3. | Conjunctive | ✅ | 13 incidents |
| CJ-10 | Find vehicle road accident incidents resulting in injuries in the USA. | Conjunctive | ✅ | 26 incidents |
| CJ-11 | Find incidents involving PPE with eye injuries during manufacturing. | Conjunctive | ✅ | 13 incidents |
| CJ-12 | Find incidents involving chemical exposure resulting in environmental impact. | Conjunctive | ✅ | 69 incidents |
| CJ-13 | Find near-miss incidents involving scaffolding at height. | Conjunctive | ✅ | 60 incidents |
| CJ-14 | Find crane incidents in Houston during 2018. | Conjunctive | ✅ | 17 incidents |
| CJ-15 | Find stored-energy incidents with head injuries. | Conjunctive | ✅ | 22 incidents |
| CJ-16 | Find marine incidents involving ROVs with equipment failures. | Conjunctive | ✅ | 7 incidents |
| CJ-17 | Find vehicle road accidents at construction sites with injuries. | Conjunctive | ✅ | 33 incidents |
| CJ-18 | Find manual handling incidents with sprain/strain injuries. | Conjunctive | ✅ | 19 incidents |
| CJ-19 | Find stored-energy dropped-object incidents with lacerations. | Conjunctive | ✅ | 12 incidents |
| CJ-20 | Find near-miss incidents involving forklifts in 2023. | Conjunctive | ✅ | 53 incidents |
| CJ-21 | What safety controls successfully mitigated harm across all incidents? | Conjunctive | ✅ | 849 MITIGATED_BY edges, 676 distinct controls |
| CJ-22 | What barriers and controls failed most frequently across all incidents? | Conjunctive | ✅ | 828 FAILED_CONTROL edges, 738 distinct barriers |
| CJ-23 | What temporal sequences (event A preceded event B) are most common? | Conjunctive | ✅ | 508 PRECEDED_BY edges, 507 distinct sequences |
| CJ-24 | What are the top causal factors leading to dropped-object incidents? | Conjunctive | ✅ | 5,311 causal edges for 3,145 dropped-object incidents |
| CJ-25 | What are the top causal factors in vehicle-related incidents? | Conjunctive | ✅ | 1,663 causal edges for 1,205 vehicle incidents |
| CJ-26 | What causal chains lead to fracture injuries? | Conjunctive | ✅ | 472 causal edges for 228 fracture incidents |
| CJ-27 | Find crane incidents in Norway resulting in injuries. | Conjunctive | ✅ | 57 incidents |
| CJ-28 | Find incidents with both equipment failure and manual handling root causes. | Conjunctive | ✅ | 0 incidents |
| CJ-29 | Find high-severity incidents at construction sites involving scaffolding. | Conjunctive | ✅ | 2 incidents |
| CJ-30 | Find incidents involving hoses with environmental impact at offshore locations. | Conjunctive | ✅ | 4 incidents |
| CJ-31 | Find severity 5 incidents involving cranes with injury impact. | Conjunctive | ✅ | 3 incidents |
| CJ-32 | What causal chains lead from equipment failures to injuries (L2 traversal)? | Conjunctive | ✅ | 105 endpoints, 105 distinct INJURY |
| CJ-33 | What events are caused by corrosion conditions (L2 traversal)? | Conjunctive | ✅ | 18 endpoints, 18 distinct EVENT |
| CJ-34 | What injuries result from failed controls (L2 traversal)? | Conjunctive | ✅ | 11 endpoints, 11 distinct INJURY |
| GL-01 | What are the most significant safety risk clusters across TechnipFMC global operations? | Global | ✅ | 11125 communities detected |
| GL-02 | Are there systemic patterns where the same type of equipment failure recurs across different geographic regions? | Global | ✅ | 144 equipment types span 5+ regions |
| GL-03 | How has the overall safety incident profile changed over the dataset time range? Are certain incident types increasing or decreasing? | Global | ✅ | Crosstab: 10 year values x 3 incident_type values |
| GL-04 | What entities serve as the most connected hubs in the knowledge graph, and what does their centrality reveal about systemic risk? | Global | ✅ | Hub analysis: degree + PageRank top 20 |
| GL-05 | What are the most common equipment-body part co-occurrences across all incidents? | Global | ✅ | 13045 equipment–body part pairs |
| GL-06 | How do safety profiles compare across the top 5 clients by incident volume? | Global | ✅ | Safety profiles for top 5 clients |
| GL-07 | Are there seasonal (monthly) patterns in incident frequency? | Global | ✅ | Peaks: none; Troughs: none |
| GL-08 | What are the top root causes by geographic region? | Global | ✅ | RCC breakdown for 10 regions |
| GL-09 | How many incidents mention burns in narrative but have no burn injury type extracted? | Global | ✅ | 69 / 177 (39%) missing INJURY_TYPE |
| GL-10 | How many incidents mention fractures in narrative but have no fracture injury type extracted? | Global | ✅ | 215 / 442 (49%) missing INJURY_TYPE |
| GL-11 | How many incidents mention cranes in narrative but have no crane equipment extracted? | Global | ✅ | 438 / 1,873 (23%) missing EQUIPMENT |
| GL-12 | How many incidents mention forklifts in narrative but have no forklift equipment extracted? | Global | ✅ | 161 / 1,075 (15%) missing EQUIPMENT |
| GL-13 | How many high-severity incidents (>=4) have no injury type extracted? | Global | ✅ | 133 / 167 (80%) high-severity missing INJURY_TYPE |
| GL-14 | How many injury-impact incidents have no body part extracted? | Global | ✅ | 5,604 / 11,736 (48%) injury incidents missing BODY_PART |
| GL-15 | How many incidents have very short narratives (<100 chars) with no entities extracted? | Global | ✅ | 327 short-narrative incidents with 0 entity extraction (5 test records) |
| GL-16 | How many incidents contain non-English narratives with reduced entity extraction? | Global | ✅ | 5,392 non-English incidents, 630 with zero entity extraction |
| GL-17 | Find the 10 incidents most similar to incident #29857 (dropped pry bar) using hybrid embedding similarity. | Global | ✅ | Top 10 similar to #29857, 60% equipment overlap |
| GL-18 | Find the 10 incidents most similar to incident #569346 (ladder fall with broken teeth) using hybrid embedding similarity. | Global | ✅ | Top 10 similar to #569346, 80% equipment overlap |
| GL-19 | Do the top-10 text-similar incidents for a forklift accident share the same equipment type? (structural hit rate) | Global | ✅ | 90% hit rate for forklift|flt retrieval |
| GL-20 | Do the top-10 text-similar incidents for a crane near-miss share the same equipment type? (structural hit rate) | Global | ✅ | 70% hit rate for crane retrieval |
| GL-21 | How well do text embeddings and structural similarity agree on the top-10 most similar incidents? (method correlation) | Global | ✅ | Text vs Node2Vec mean overlap: 3.0% |
| GL-22 | Find incidents semantically similar to 'worker fell from scaffold due to missing guardrail' using text embeddings. | Global | ✅ | Top match: #531820 (sim=0.709) |
| GL-23 | Find incidents semantically similar to 'crane load dropped because sling failed under tension' using text embeddings. | Global | ✅ | Top match: #430 (sim=0.676) |
| GL-24 | Which equipment types appear most often in the top-10 similar incidents for high-severity events? (embedding-based pattern) | Global | ✅ | Top equipment in high-sev neighborhoods: [('crane', 35), ('forklift', 34), ('equipment', 14)] |
| IOGP-01 | What injuries result from incidents involving moving vehicles and mobile equipment? | Aggregation | ✅ | 2008 incidents, 122 injury_type values, top: injuries |
| IOGP-02 | How do dropped object incidents break down by severity over time? | Aggregation | ✅ | Crosstab: 6 severity_bin values x 10 year values |
| IOGP-03 | How many incidents involve stored energy or snap-back hazards? | Single-hop | ✅ | 114 incidents |
| IOGP-04 | How many pressurized system incidents resulted in containment loss? | Multi-hop | ✅ | 192 incidents |
| IOGP-05 | Which electrical incidents had lockout/tagout failures? | Conjunctive | ✅ | 142 incidents; 9 FAILED_CONTROL edges |
| IOGP-06 | What body parts are affected in working-at-height incidents with fall protection gaps? | Multi-hop | ✅ | 246 incidents, 76 body_part values, top: left hand |
| IOGP-07 | What injuries result from mechanical lifting incidents with rigging failures? | Multi-hop | ✅ | 2001 incidents, 152 injury_type values, top: injuries |
| IOGP-08 | How many machinery and tool incidents resulted in hand or finger injuries? | Multi-hop | ✅ | 200 incidents |
| IOGP-09 | What are the top injury types from moving vehicle and mobile equipment incidents? | Aggregation | ✅ | 2008 incidents, 122 injury_type values, top: injuries |
| IOGP-10 | How many vehicle incidents resulted in high-severity outcomes? | Multi-hop | ✅ | 33 incidents |
| IOGP-11 | What body parts are most affected in vehicle/mobile equipment incidents? | Aggregation | ✅ | 842 incidents, 153 body_part values, top: BUMPER |
| IOGP-12 | Which countries have the most mechanical lifting/hoisting incidents? | Aggregation | ✅ | 2001 incidents, 61 location values, top: UK |
| IOGP-13 | What are the top root causes of mechanical lifting incidents? | Aggregation | ✅ | 2001 incidents, 48 root_cause_category values, top: Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) |
| IOGP-14 | How many working-at-height incidents involved harnesses or lanyards? | Single-hop | ✅ | 74 incidents |
| IOGP-15 | What injury types result from fall-to-lower-level incidents? | Aggregation | ✅ | 1695 incidents, 310 injury_type values, top: contusion |
| IOGP-16 | How do dropped object incidents break down by body part affected? | Aggregation | ✅ | 1160 incidents, 149 body_part values, top: left foot |
| IOGP-17 | How many tensioned line or snap-back incidents occurred? | Single-hop | ✅ | 109 incidents |
| IOGP-18 | What equipment is involved in stored energy (pressure/tension) incidents? | Aggregation | ✅ | 725 incidents, 1024 equipment values, top: crane |
| IOGP-19 | How many pressurized system incidents mention zero energy verification? | Multi-hop | ✅ | 23 incidents |
| IOGP-20 | What injuries result from compressed gas or pressure vessel incidents? | Multi-hop | ✅ | 298 incidents, 59 injury_type values, top: injuries |
| IOGP-21 | How many machinery/tool incidents involved entrapment or caught-between hazards? | Single-hop | ✅ | 775 incidents |
| IOGP-22 | What body parts are most affected in grinder and power tool incidents? | Multi-hop | ✅ | 312 incidents, 96 body_part values, top: left hand |
| IOGP-23 | How many electrical incidents mention arc flash or electrocution? | Single-hop | ✅ | 88 incidents |
| IOGP-24 | What equipment is involved in electrical incidents with LOTO failures? | Multi-hop | ✅ | 19 incidents, 37 equipment values, top: IRP |
| IOGP-25 | How many incidents involve projectiles or flying debris? | Single-hop | ✅ | 29 incidents |
| IOGP-26 | What are the top root causes of explosion or fire incidents? | Aggregation | ✅ | 322 incidents, 352 equipment values, top: fire extinguisher |
| IOGP-27 | How many incidents mention extreme weather or natural events? | Single-hop | ✅ | 903 incidents |
| IOGP-28 | What are the year-over-year trends for vehicle incidents? | Aggregation | ✅ | 842 incidents across 89 months |
| MH-01 | Find all equipment types involved in containment loss events leading to injuries at offshore locations. | Multi-hop | ✅ | 1 incidents, 2 equipment types |
| MH-02 | What injury types are associated with equipment failures during maintenance operations? | Multi-hop | ✅ | 29 incidents, 19 pairs |
| MH-03 | Which clients have experienced vessel-related incidents resulting in back injuries? | Multi-hop | ✅ | 47 incidents, 93 organization values, top: OCM |
| MH-04 | What are the most common injury types for each of the top 5 equipment categories? | Multi-hop | ✅ | Injury breakdown for top 5 equipment |
| MH-05 | Find incidents where hand injuries occurred during work involving pipes at locations in Asia Pacific. | Multi-hop | ✅ | 6 incidents |
| MH-06 | What is the severity distribution of incidents involving trucks compared to those involving cranes? | Multi-hop | ✅ | Truck vs crane severity comparison |
| MH-07 | Which locations have the highest concentration of near-miss incidents involving scaffolding? | Multi-hop | ✅ | 121 incidents, 33 location values, top: Sabetta |
| MH-08 | Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents. | Multi-hop | ⚠️ | 1 incidents, 0 injury_type values |
| MH-09 | What eye injuries result from grinder incidents? | Multi-hop | ✅ | 16 incidents |
| MH-10 | What injuries occur in ladder incidents at construction sites? | Multi-hop | ✅ | 77 incidents, 26 injury_type values, top: injuries |
| MH-11 | What equipment is involved in finger or thumb injuries? | Multi-hop | ✅ | 1352 incidents, 1569 equipment values, top: gloves |
| MH-12 | Which countries have the most crane-related incidents? | Multi-hop | ✅ | 1444 incidents, 59 location values, top: UK |
| MH-13 | What incidents involve forklifts with foot or leg injuries? | Multi-hop | ✅ | 26 incidents |
| MH-14 | What equipment is involved in fracture injuries? | Multi-hop | ✅ | 228 incidents, 296 equipment values, top: PPE |
| MH-15 | Which body parts are affected in hammer-related incidents? | Multi-hop | ✅ | 146 incidents, 67 body_part values, top: left hand |
| MH-16 | What burn injuries are associated with welding operations? | Multi-hop | ✅ | 16 incidents |
| MH-17 | What incidents involve ROVs in Norway? | Multi-hop | ✅ | 26 incidents |
| MH-18 | What crane incidents occurred in Brazil? | Multi-hop | ✅ | 71 incidents |
| MH-19 | What forklift incidents occurred in the UK? | Multi-hop | ✅ | 102 incidents |
| MH-20 | What scaffold incidents occurred in India? | Multi-hop | ✅ | 44 incidents |
| MH-21 | What injury types result from high-severity crane incidents? | Multi-hop | ✅ | 27 incidents, 4 injury_type values, top: injury |
| MH-22 | What equipment is involved in incidents at Aberdeen? | Multi-hop | ✅ | 2501 incidents, 3183 equipment values, top: crane |
| MH-23 | What sling incidents involved hand or finger injuries? | Multi-hop | ✅ | 14 incidents |
| MH-24 | What are the injury types from construction incidents resulting in fractures? | Multi-hop | ✅ | 135 incidents |
| MH-25 | What finger or thumb injuries involve fractures? | Multi-hop | ✅ | 61 incidents |
| MH-26 | What back injuries are associated with manual handling root causes? | Multi-hop | ✅ | 97 incidents |
| MH-27 | What crane incidents occurred during 2019? | Multi-hop | ✅ | 166 incidents |
| MH-28 | What forklift incidents occurred during 2023? | Multi-hop | ✅ | 99 incidents |
| MH-29 | What scaffold incidents occurred during 2020? | Multi-hop | ✅ | 40 incidents |
| MH-30 | What ROV incidents occurred during 2017? | Multi-hop | ✅ | 82 incidents |
| MH-31 | What injuries result from fall/slip RCC incidents with fractures? | Multi-hop | ✅ | 68 incidents |
| MH-32 | What equipment is involved in incidents at Houston? | Multi-hop | ✅ | 1361 incidents, 1244 equipment values, top: forklift |
| MH-33 | What body parts are affected in incidents reported by YAMAL LNG? | Multi-hop | ✅ | 1302 incidents, 302 body_part values, top: left hand |
| MH-34 | What injuries result from incidents at Rio de Janeiro? | Multi-hop | ✅ | 905 incidents, 97 injury_type values, top: cut |
| MH-35 | What incidents involve grinders with hand or finger injuries? | Multi-hop | ✅ | 45 incidents |
| MH-36 | What equipment is involved in incidents reported by PETROBRAS? | Multi-hop | ✅ | 676 incidents, 764 equipment values, top: ROV |
| MH-37 | What are the top injury types in incidents at Le Trait? | Multi-hop | ✅ | 1163 incidents, 116 injury_type values, top: pain |
| MH-38 | What equipment is involved in near-miss incidents at offshore locations? | Multi-hop | ✅ | 141 incidents, 205 equipment values, top: crane |
| MH-39 | What are the root causes of incidents in Russia? | Multi-hop | ✅ | 962 incidents, 43 root_cause_category values, top: Falls, slips and trips on same level (without potential to fall to lower level) |
| MH-40 | What body parts are affected in excavator-related incidents? | Multi-hop | ✅ | 201 incidents, 37 body_part values, top: ankle |
| MH-41 | What injury types result from incidents involving pallets? | Multi-hop | ✅ | 340 incidents, 60 injury_type values, top: injuries |
| MH-42 | What injuries result from incidents involving pipes at offshore locations? | Multi-hop | ⚠️ | 8 incidents, 2 injury_type values, top: danos leves |
| MH-43 | What equipment is involved in red-risk incidents? | Multi-hop | ✅ | 52 incidents, 81 equipment values, top: crane |
| MH-44 | What are the root causes of incidents at Sabetta (Yamal LNG site)? | Multi-hop | ✅ | 880 incidents, 41 root_cause_category values, top: Falls, slips and trips on same level (without potential to fall to lower level) |
| MH-45 | What injury types are connected to crane equipment via graph traversal? | Multi-hop | ✅ | 113 endpoints, 113 distinct INJURY_TYPE |
| MH-46 | What equipment is connected to fracture injuries via graph traversal? | Multi-hop | ✅ | 296 endpoints, 296 distinct EQUIPMENT |
| MH-47 | What body parts are connected to forklift equipment via graph traversal? | Multi-hop | ✅ | 137 endpoints, 137 distinct BODY_PART |
| MH-48 | What root causes are connected to hand injuries via graph traversal? | Multi-hop | ✅ | 46 endpoints, 46 distinct ROOT_CAUSE_CATEGORY |
| MH-49 | What locations have crane equipment via 2-hop graph traversal? | Multi-hop | ✅ | 1495 endpoints, 1466 distinct LOCATION |
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
| SC-10 | In incident #644762, what equipment was involved? | Single-hop | ✅ | 6 items: ['STB chute', 'crane', 'deck winch', 'main lift shackle', 'reel', 'tri-plate'] |
| SC-11 | In incident #505133, what equipment was involved? | Single-hop | ✅ | 6 items: ['Billy Pugh personnel transfer basket', 'G1200 Helideck', 'helicopter', 'ladder', 'splint', 'stretcher'] |
| SC-12 | In incident #645871, what body parts were affected? | Single-hop | ✅ | 2 items: ['arm', 'eye'] |
| SC-13 | In incident #609327, what injury types resulted? | Single-hop | ✅ | 2 items: ['fracture', 'trauma'] |
| SC-14 | In incident #569346, what equipment was involved? | Single-hop | ✅ | 4 items: ['Negative side string', 'Sideboom', 'Superior CPX-94', 'ladder'] |
| SC-15 | In incident #569346, what body parts were affected? | Single-hop | ✅ | 4 items: ['chin', 'jaw', 'lip', 'lower lip'] |
| SC-16 | In incident #569346, what injury types resulted? | Single-hop | ✅ | 2 items: ['laceration', 'three broken teeth'] |
| SC-17 | In incident #685931, what equipment was involved? | Single-hop | ✅ | 7 items: ['bulker bags', 'ice compression pack', 'locking bar', 'safety helmet', 'splint and bandage', 'steel rack', 'waste rack lid'] |
| SC-18 | In incident #632796, what equipment was involved? | Single-hop | ✅ | 4 items: ['HDA2006 224tn Hydraulic Jack', 'hydraulic hose', 'hydraulic jack', 'water guard'] |
| SC-19 | In incident #632796, what body parts were affected? | Single-hop | ✅ | 5 items: ['back', 'left', 'lower back', 'lower back area', 'lower left side of his back'] |
| SC-20 | In incident #611828, what equipment was involved? | Single-hop | ✅ | 7 items: ['Sideboom', 'glasses', 'moving block part', 'safety helmet', 'sideboom_x000D_', 'sling', 'top hook block'] |
| SC-21 | In incident #563945, what equipment was involved? | Single-hop | ✅ | 4 items: ['davit', 'emergency lowering arm', 'ice pack', 'lifeboats'] |
| SC-22 | In incident #564230, what injury types resulted? | Single-hop | ✅ | 7 items: ['bruising on the brain', 'contusion', 'dizziness', 'headache', 'nausea', 'neck pain', 'whiplash'] |
| SC-23 | In incident #696119, what injury types resulted? | Single-hop | ✅ | 5 items: ['Cerebral Hematoma', 'Crack left pelvis', 'Dislocate left shoulder', 'dislocate left shoulder_x000D_', 'hematoma'] |
| SC-24 | In incident #560111, what injury types resulted? | Single-hop | ✅ | 5 items: ['Eyes injury', 'Left-eye cornea injury', 'Multiple facial graze-wound', 'Open right-eye cornea injury', 'Periorbital hematoma'] |
| SC-25 | In incident #702644, what injury types resulted? | Single-hop | ✅ | 4 items: ['breaks/fractures', 'bruising', 'skin abrasion', 'soft tissue damage'] |
| SC-26 | In incident #16468, what locations were recorded? | Single-hop | ✅ | 14 items: ['Aberdeen', 'Deep Orient', 'Duty Mess', 'Europe', 'Larnaca base', 'Limassol', 'Limassol base', 'Mediterranean hospital', 'Mez deck', 'UK', 'deck level', 'hospital', 'main deck', 'quayside'] |
| SC-27 | In incident #546948, what locations were recorded? | Single-hop | ✅ | 13 items: ['4th floor', 'Doha', 'Doha Service Base', 'Middle East', 'PQ1-Q', 'PS1', 'PS1-A', 'PS1-C', 'PS1-G', 'PS1-Q', 'PS1G', 'PS1Q', 'Qatar'] |
| SC-28 | In incident #555852, what organizations were recorded? | Single-hop | ✅ | 16 items: ['Client', 'ERTL', 'KVA', 'Operasjonsleder Haugesund Police', 'Police Security Service', 'Project', 'Project management', 'Regional Police', 'STATOIL ASA', 'Stakeholders', 'TECHNIPFMC', 'TPFMC Control', 'TechnipFMC ERTL', 'TechnipFMC QHSE Management', 'TechnipFMC management', 'local police'] |
| SC-29 | In incident #594002, what equipment was involved? | Single-hop | ✅ | 3 items: ['Punch tool', 'Stamping Punch Tool', 'V-Jaw tong'] |
| SC-30 | In incident #706581, what injury types resulted? | Single-hop | ✅ | 4 items: ['cut wound', 'femoral fracture', 'pulmonary contusion', 'rib fracture'] |
| SC-31 | In incident #563298, what equipment was involved? | Single-hop | ✅ | 3 items: ['light 4x4 truck', 'skid', 'truck platform'] |
| SC-32 | In incident #507347, what body parts were affected? | Single-hop | ✅ | 4 items: ['Dislocated R Knee', 'Dislocated knee cap', 'Knee', 'left leg'] |
| SC-33 | In incident #507347, what equipment was involved? | Single-hop | ✅ | 4 items: ['Full Leg Vacuum splint', 'ROV XLX94', 'Yokohama fenders', 'crutches'] |
| SC-34 | In incident #19018, what equipment was involved? | Single-hop | ✅ | 11 items: ['CCTV', 'DVC', 'MCV-U', 'MVC', 'ROV', 'SDU', 'SDU-3', 'UEH', 'VCM', 'crane', 'u-VCM'] |
| SC-35 | In incident #664483, what injury types resulted? | Single-hop | ✅ | 2 items: ['confirmed fracture', 'dislocation'] |
| SH-01 | What incidents involved forklifts in 2022? | Single-hop | ✅ | 71 incidents |
| SH-02 | What equipment was involved in incident #29857? | Single-hop | ⚠️ | 3 items: ['ROV', 'lanyard', 'pry bar'] |
| SH-03 | What body parts were affected in crane-related incidents? | Single-hop | ✅ | 1444 incidents, 192 body_part values, top: finger |
| SH-04 | Which locations reported valve-related incidents? | Single-hop | ✅ | 387 incidents, 36 location values, top: USA |
| SH-05 | What types of injuries resulted from incidents at offshore installations? | Single-hop | ✅ | 1120 incidents, 124 injury_type values, top: cut |
| SH-06 | What incidents were reported by client SHELL OFFSHORE INC.? | Single-hop | ✅ | 60 incidents |
| SH-07 | What incidents involved ladders? | Single-hop | ✅ | 157 incidents |
| SH-08 | What incidents involved grinders? | Single-hop | ✅ | 175 incidents |
| SH-09 | What incidents involved hoses? | Single-hop | ✅ | 429 incidents |
| SH-10 | What incidents involved pumps? | Single-hop | ✅ | 314 incidents |
| SH-11 | What incidents involved ROVs? | Single-hop | ✅ | 562 incidents |
| SH-12 | What incidents involved excavators? | Single-hop | ✅ | 201 incidents |
| SH-13 | What incidents involved PPE (helmets/gloves/safety glasses)? | Single-hop | ✅ | 684 incidents |
| SH-14 | What incidents involved slings? | Single-hop | ✅ | 265 incidents |
| SH-15 | What incidents involved compressors? | Single-hop | ✅ | 209 incidents |
| SH-16 | What incidents involved winches? | Single-hop | ✅ | 278 incidents |
| SH-17 | What body parts were affected in hose-related incidents? | Single-hop | ✅ | 429 incidents, 93 body_part values, top: eye |
| SH-18 | What injury types resulted from pump-related incidents? | Single-hop | ✅ | 314 incidents, 29 injury_type values, top: laceration |
| SH-19 | Which organizations reported excavator-related incidents? | Single-hop | ✅ | 201 incidents, 284 organization values, top: TRANS ADRIATIC PIPELINE AG |
| SH-20 | What incidents involved welding equipment? | Single-hop | ✅ | 261 incidents |
| SH-21 | What incidents involved pallets? | Single-hop | ✅ | 340 incidents |
| SH-22 | What incidents involved fire extinguishers? | Single-hop | ✅ | 148 incidents |
| SH-23 | What incidents involved reels? | Single-hop | ✅ | 241 incidents |
| SH-24 | What incidents involved umbilicals? | Single-hop | ✅ | 115 incidents |
| SH-25 | What incidents affected the left hand? | Single-hop | ✅ | 1015 incidents |
| SH-26 | What incidents affected the thumb? | Single-hop | ✅ | 253 incidents |
| SH-27 | What incidents resulted in contusions or bruises? | Single-hop | ✅ | 360 incidents |
| SH-28 | What incidents resulted in sprains or strains? | Single-hop | ✅ | 156 incidents |
| SH-29 | How many incidents involve confined spaces? | Single-hop | ✅ | 75 incidents |
| SH-30 | How many incidents involve hot work? | Single-hop | ✅ | 152 incidents |
| SH-31 | How many incidents mention chemical exposure? | Single-hop | ✅ | 177 incidents |
| SH-32 | How many incidents involve electrical hazards? | Single-hop | ✅ | 891 incidents |
| SH-33 | How many incidents mention gas leaks? | Single-hop | ✅ | 42 incidents |
| SH-34 | How many incidents describe man overboard situations? | Single-hop | ✅ | 897 incidents |
| SH-35 | How many incidents mention fatigue as a factor? | Single-hop | ✅ | 35 incidents |
| SH-36 | How many incidents involve H2S or hydrogen sulfide? | Single-hop | ✅ | 32 incidents |
| SH-37 | How many incidents mention fire (not line of fire)? | Single-hop | ✅ | 1500 incidents |
| SH-38 | How many incidents mention pressure hazards? | Single-hop | ✅ | 1260 incidents |
| SH-39 | How many incidents reference permit-to-work procedures? | Single-hop | ✅ | 398 incidents |
| SH-40 | How many incidents mention struck-by hazards? | Single-hop | ✅ | 86 incidents |
| SH-41 | How many incidents describe caught-between or pinch-point hazards? | Single-hop | ✅ | 466 incidents |
| SH-42 | How many incidents mention line-of-fire hazards? | Single-hop | ✅ | 461 incidents |
| SH-43 | How many incidents mention scaffolding falls? | Single-hop | ✅ | 398 incidents |
| SH-44 | How many incidents reference JSA or toolbox talks? | Single-hop | ✅ | 268 incidents |
| SH-45 | What incidents involved helicopters? | Single-hop | ✅ | 8 incidents |
| SH-46 | What incidents were reported by PETROBRAS? | Single-hop | ✅ | 676 incidents |
| SH-47 | What incidents were reported by EQUINOR? | Single-hop | ✅ | 401 incidents |
| SH-48 | What incidents occurred at Sabetta? | Single-hop | ✅ | 880 incidents |
| SH-49 | What incidents occurred at Le Trait? | Single-hop | ✅ | 1163 incidents |
| SH-50 | What incidents resulted in abrasions or scratches? | Single-hop | ✅ | 223 incidents |
| SH-51 | What incidents occurred in 2024? | Single-hop | ✅ | 1461 incidents |
| SH-52 | What incidents have severity level 5 (most severe)? | Single-hop | ✅ | 23 incidents |
| SH-53 | What incidents are classified as occupational illness? | Single-hop | ✅ | 160 incidents |
| SH-54 | What incidents have red risk classification? | Single-hop | ✅ | 52 incidents |
| SH-55 | What incidents involved robots or drones? | Single-hop | ✅ | 8 incidents |
| SH-56 | What incidents occurred before 2016? | Single-hop | ✅ | 0 incidents |
| SH-57 | What incidents occurred in Antarctica? | Single-hop | ✅ | 0 incidents |
| SH-58 | What incidents involved tanks? | Single-hop | ✅ | 67 incidents |

**Overall:** 254 ✅ passing / 4 ⚠️ failing out of 258 queries

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
  reel: 98
  manlift: 98
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

### AG-07: What are the most common body parts affected across all incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19851
Distinct BODY_PART values: 1980
Top 20:
  left hand: 942
  finger: 723
  left foot: 419
  eye: 417
  Knee: 318
  left leg: 317
  ankle: 297
  arm: 258
  shoulder: 255
  thumb: 212
  back: 206
  head: 181
  wrist: 153
  face: 138
  forearm: 122
  lower back: 114
  elbow: 113
  neck: 100
  forehead: 91
  left side: 69
```

### AG-08: What are the most common injury types across all incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19851
Distinct INJURY_TYPE values: 1324
Top 20:
  injuries: 319
  cut: 281
  laceration: 207
  pain: 145
  contusion: 130
  injury: 125
  abrasion: 96
  bruise: 86
  fracture: 86
  minor scratch: 75
  wounds: 75
  minor burn: 68
  personal injury: 64
  sprain: 50
  bruising: 47
  closed fracture: 45
  minor damage: 44
  no injuries: 41
  swelling: 38
  No injury: 37
```

### AG-09: Which organizations report the most incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19851
Distinct ORGANIZATION values: 8447
Top 20:
  TECHNIPFMC: 4688
  JSC YAMAL LNG: 1302
  FLEXI FRANCE: 1017
  IP: 875
  N/A - No Vendor: 820
  HSE: 695
  TRANS ADRIATIC PIPELINE AG: 571
  PETROBRAS: 522
  TECHNIPFMC UMBILICALS LTD: 428
  Shell: 411
  OCM: 332
  SASOL NORTH AMERICA, INC.: 332
  TECHNIP MARINE OPERATION SERVICES: 306
  ARCTIC LNG 2: 293
  Client: 272
  WOODSIDE ENERGY LTD.: 258
  HSEA: 247
  THE BAHRAIN PETROLEUM COMPANY BSC: 224
  EQUINOR ENERGY AS: 221
  BP: 221
```

### AG-10: What is the annual trend of manual handling incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Total incidents: 760
Months with data: 108
Yearly breakdown:
  2016: 92
  2017: 111
  2018: 149
  2019: 108
  2020: 74
  2021: 83
  2022: 37
  2023: 49
  2024: 39
  2025: 18
```

### AG-11: What root cause categories are most common in high-severity incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 167
Distinct ROOT_CAUSE_CATEGORY values: 22
Top 10:
  Stored energy (dropped objects): 32
  Stored energy (pressure, tension): 25
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 18
  Hazard Identification & Risk Assessment: 13
  Equipment condition: 10
  Planning and coordination of works: 6
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 6
  Flammable solids, liquids and gases: 5
  Standard Operating Procedures, Procedures & Work instructions: 4
  Motor Vehicle Worksite Accident: 3
```

### AG-12: How do incidents break down by impact type over the years?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.4s

```
| year | Damage | Damage - Financial impact | Environment | Financial Impact | Fire/Explosion | Injury | Injury/Illness | Occupational Illness | Reputation | Unknown | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2018 | 64 | 13 | 259 | 596 | 0 | 1872 | 27 | 38 | 52 | 74 | 2995 |
| 2017 | 725 | 7 | 206 | 59 | 63 | 1526 | 2 | 42 | 18 | 0 | 2648 |
| 2019 | 6 | 32 | 252 | 621 | 0 | 1545 | 48 | 25 | 30 | 81 | 2640 |
| 2021 | 0 | 85 | 244 | 528 | 0 | 1212 | 179 | 22 | 6 | 35 | 2311 |
| 2020 | 13 | 36 | 274 | 624 | 0 | 1160 | 52 | 12 | 9 | 25 | 2205 |
| 2016 | 460 | 3 | 117 | 0 | 58 | 1017 | 1 | 20 | 6 | 0 | 1682 |
| 2023 | 0 | 453 | 181 | 0 | 0 | 0 | 888 | 0 | 0 | 0 | 1522 |
| 2024 | 0 | 392 | 176 | 0 | 0 | 0 | 893 | 0 | 0 | 0 | 1461 |
| 2022 | 0 | 476 | 151 | 16 | 0 | 25 | 775 | 1 | 0 | 2 | 1446 |
| 2025 | 0 | 266 | 130 | 0 | 0 | 0 | 514 | 0 | 0 | 0 | 910 |
```

### AG-13: What is the trend of fire/explosion incidents over time?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Total incidents: 121
Months with data: 16
Yearly breakdown:
  2016: 58
  2017: 63
```

### AG-14: Which cities have the highest incident counts?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19851
Distinct LOCATION values: 230
Top 20:
  Aberdeen: 2493
  Houston: 1349
  Le Trait: 1110
  Rio de Janeiro: 892
  Sabetta: 880
  Dunfermline: 504
  Odessa: 423
  Stephenville: 412
  Minot: 402
  Newcastle: 368
  Acu: 362
  Agotnes: 342
  Lake Charles: 330
  Singapore: 304
  Channelview: 281
  Johor Bahru: 280
  Qidong: 276
  Macae: 225
  Theodore: 202
  Tananger: 158
```

### AG-15: How do incidents distribute across work process categories?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19851
Distinct ROOT_CAUSE_CATEGORY values: 65
Top 20:
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 1471
  Hazard Identification & Risk Assessment: 1306
  Equipment condition: 1255
  Falls, slips and trips on same level (without potential to fall to lower level): 1181
  Stored energy (dropped objects): 1160
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 1084
  Standard Operating Procedures, Procedures & Work instructions: 817
  Manual handling: 760
  Stored energy (pressure, tension): 725
  Planning and coordination of works: 718
  Equipment Suitability: 537
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 514
  Motor Vehicle Road Accident: 489
  Workplace layout / congestion: 392
  Traffic Management / Routes / Pedestrian path: 363
  Motor Vehicle Worksite Accident: 353
  Use of personal protective equipment: 350
  Inadequate Supervision: 335
  Unfamiliar personnel: 322
  Flammable solids, liquids and gases: 322
```

### AG-16: What is the year-over-year trend of eye injuries?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Total incidents: 492
Months with data: 103
Yearly breakdown:
  2016: 52
  2017: 67
  2018: 68
  2019: 67
  2020: 51
  2021: 70
  2022: 27
  2023: 33
  2024: 32
  2025: 25
```

### AG-17: What are the most common injury types at construction sites?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 5357
Distinct INJURY_TYPE values: 583
Top 10:
  injuries: 139
  contusion: 99
  laceration: 86
  cut: 51
  closed fracture: 43
  bruise: 42
  abrasion: 34
  personal injury: 33
  injury: 28
  fracture: 27
```

### AG-18: Which clients report the most high-severity incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 167
Distinct ORGANIZATION values: 247
Top 10:
  TECHNIPFMC: 54
  N/A - No Vendor: 14
  PETROBRAS: 10
  EQUINOR ENERGY AS: 8
  HSE: 8
  IP: 6
  WOODSIDE ENERGY LTD.: 5
  FMC KONGSBERG SUBSEA AS: 4
  HSEA: 3
  CHEVRON USA INC: 3
```

### AG-19: What is the year-over-year trend of fracture injuries?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Total incidents: 228
Months with data: 78
Yearly breakdown:
  2016: 29
  2017: 65
  2018: 47
  2019: 19
  2020: 10
  2021: 25
  2022: 4
  2023: 13
  2024: 10
  2025: 6
```

### AG-20: What equipment is most common in incidents at Aberdeen?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2501
Distinct EQUIPMENT values: 3183
Top 10:
  crane: 171
  ROV: 164
  rigging: 34
  winch: 31
  PPE: 31
  SOPEP equipment: 28
  reel: 28
  ROV XLX94: 27
  kenz crane: 26
  umbilical: 21
```

### AG-21: How do incidents break down by work process and risk color?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
work_process null rate: 2722/19820 (13.7%)

| work_process | Green | Red | Unknown | Yellow | Total |
|---|---|---|---|---|---|
| Unknown | 2103 | 21 | 299 | 299 | 2722 |
| Construction | 0 | 0 | 2141 | 0 | 2141 |
| Construction - Installation | 0 | 0 | 1883 | 0 | 1883 |
| Yards | 0 | 0 | 935 | 0 | 935 |
| Vessel / Yards | 0 | 0 | 608 | 0 | 608 |
| Support Service | 0 | 0 | 580 | 0 | 580 |
| Marine Operations | 0 | 0 | 448 | 0 | 448 |
| Transport / Handling / Packing | 0 | 0 | 409 | 0 | 409 |
| Construction - Installation-Operations | 340 | 4 | 0 | 55 | 399 |
| Manufacturing | 0 | 0 | 388 | 0 | 388 |
| Other Manufacturing Activities | 0 | 0 | 380 | 0 | 380 |
| Construction - Installation-Construction | 347 | 0 | 0 | 17 | 364 |
| Workshop Activities | 0 | 0 | 354 | 0 | 354 |
| Vessel / Yards-Workshop Activities | 209 | 2 | 0 | 139 | 350 |
| Operations | 0 | 0 | 325 | 0 | 325 |
```

### AG-22: How do the top countries compare on accident vs near-miss ratios?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
loc_country null rate: 5/19820 (0.0%)

| loc_country | Accident | Near Miss | Unknown | Total |
|---|---|---|---|---|
| USA | 2078 | 1065 | 1142 | 4285 |
| UK | 1781 | 966 | 982 | 3729 |
| Brazil | 608 | 727 | 382 | 1717 |
| France | 509 | 507 | 406 | 1422 |
| Norway | 400 | 402 | 248 | 1050 |
| Russia | 695 | 196 | 71 | 962 |
| India | 254 | 230 | 302 | 786 |
| Malaysia | 280 | 260 | 90 | 630 |
| China | 80 | 103 | 350 | 533 |
| Singapore | 71 | 101 | 132 | 304 |
| zObsolete - Greece | 152 | 90 | 53 | 295 |
| Canada | 128 | 56 | 96 | 280 |
| Australia | 140 | 52 | 84 | 276 |
| Indonesia | 72 | 140 | 40 | 252 |
| Bahrain | 0 | 0 | 225 | 225 |
```

### AG-23: How do root cause categories distribute across business units?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
business_unit null rate: 14007/19820 (70.7%)

| business_unit | 1. Internal NCR (issued by TechnipFMC or Partners) | 3. 3rd Party NCR (received or managed by TechnipFMC or Partners) | Access/Egress | Accumulation / Presence of explosive atmosphere | Animal Strike | Animals, Bacteria, Viruses and Funguses | Basic Organisational - Equipment Suitability | Basic Organizational | Basic Organizational - Hazard Identification & Risk Assessment | Basic Organizational - Inadequate Supervision | Basic Organizational - Management of Change | Basic Organizational - Planning and coordination of works | Basic Organizational - SIMOPS (coordination with 3rd Parties) | Basic Organizational - Standard Operating Procedures, Procedures & Work instructions | Basic Organizational - Tool suitability | Basic Organizational - Unfamiliar personnel | Basic Organizational - Use of personal protective equipment | Biological - Animals, Bacteria, Viruses and Funguses | Climate (Heat/Cold/Humidity) | Complaints from neighbors (noise, smell, light, dust, etc.) | Computer workplaces / Screens | Confined Spaces (space/sizing issues only) | Dangerous surfaces (sharp/ sharp edged/ high roughness grade) | Difficult/Hindered operability of tools and equipment | Electrical | Electrical - Electrical current / electrocution / ESD / electromagnetic Fields | Environment- Complaints from neighbours (noise, smell, light, dust...) | Environment- Over-consumption of energy, natural resources (water, ...) | Environment- Unsorted waste, no traceability of the waste;? | Equipment Suitability | Equipment condition | Ergonomics - Computer workplaces / Screens | Ergonomics - Difficult/Hindered operability of tools and equipment | Ergonomics - Information perceptiveness (amount / mode) & Information reception (extend / range) | Ergonomics - Manual handling | Ergonomics - Posture (constraint or restricted environment) | Ergonomics - Repetitive/one sided physical demand | Explosives / potential explosives | Fall to lower level / fall to water / loose materials (e.g. silos with granulate) | Falls, slips and trips on same level (without potential to fall to lower level) | Fire & Explosion - Accumulation / Presence of explosive atmosphere | Fire & Explosion - Explosives / potential explosives | Fire & Explosion - Flammable solids, liquids and gases | Fire & Explosion - Uncontrolled chemical or physical reaction | Flammable solids, liquids and gases | Hazard Identification & Risk Assessment | Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution) | Hazardous liquids (exposure to / spill / loss of containment /pollution) | Hazardous solids (exposure to / spill / loss of containment /pollution) | Hot/cold surfaces or media | Hyperbaric work environment | Illumination / sight / visibility | Inadequate Supervision | Inappropriate behavior / Horseplay / Aggression / violence (Fights, Riots, etc.) | Information perceptiveness (amount / mode) & Information reception (extend / range) | Lifting ops error | Management of Change | Manual handling | Mechanical - Dangerous surfaces (sharp/ sharp edged/ high roughness grade) | Mechanical - Equipment condition | Mechanical - Stored energy (dropped objects) | Mechanical - Stored energy (pressure, tension) | Mechanical - Tool condition | Mechanical - Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) | Mechanical - Unprotected/unguarded moving machine parts (struck by/caught by ) | Motor Vehicle Road Accident | Motor Vehicle Worksite Accident | Noise | Over-consumption of energy, natural resources (water, etc.) | Physical - Hot/cold surfaces or media | Physical - Noise | Physical - Radiation (ionising / non ionising) | Physical - Vibrations (hand arm / whole body) | Pinch point | Planning and coordination of works | Posture (constraint or restricted environment) | Protection | Psycho social - Alcohol and drugs abuse | Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...) | Psycho social - Stress | Psycho social - Work time/ Shift pattern | Psycho social - Workload (Overload/Underload) | Radiation (ionising / non ionising) | Repetitive/one sided physical demand | SIMOPS (coordination with 3rd Parties) | Standard Operating Procedures, Procedures & Work instructions | Stored energy (dropped objects) | Stored energy (pressure, tension) | Stress | Substances  - Hazardous gases, vapours, aerosols (exposure to / spill / loss of containment /pollution) | Substances  - Hazardous liquids (exposure to / spill / loss of containment /pollution) | Substances  - Hazardous solids (exposure to / spill / loss of containment /pollution) | Tool condition | Tool suitability | Traffic Management / Routes / Pedestrian path | Uncontrolled chemical or physical reaction | Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) | Unfamiliar personnel | Unknown | Unprotected/unguarded moving machine parts (struck by/caught by) | Unsorted waste, no traceability of the waste | Use of personal protective equipment | Vibrations (hand arm / whole body) | Weather Condition | Work environment - Access/Egress | Work environment - Climate (Heat/Cold/Humidity) | Work environment - Confined Spaces (space/sizing issues only) | Work environment - Fall to lower level / fall to water / loose materials (e.g. silos with granulate) | Work environment - Falls, slips and trips on same level (without potential to fall to lower level) | Work environment - Hyperbaric work environment | Work environment - Illumination / sight / visibility | Work environment - Motor Vehicle Road Accident | Work environment - Motor Vehicle Worksite Accident | Work environment - Traffic Management / Routes / Pedestrian path | Work environment - Workplace layout / congestion | Work time/ Shift pattern | Workload (Overload/Underload) | Workplace layout / congestion | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Unknown | 4 | 1 | 0 | 0 | 0 | 0 | 383 | 0 | 973 | 300 | 46 | 538 | 71 | 659 | 193 | 261 | 262 | 134 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 209 | 20 | 62 | 61 | 0 | 0 | 6 | 78 | 9 | 597 | 178 | 53 | 0 | 0 | 0 | 24 | 22 | 266 | 92 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 174 | 896 | 860 | 496 | 158 | 1126 | 189 | 0 | 0 | 0 | 0 | 74 | 5 | 10 | 16 | 0 | 0 | 0 | 0 | 5 | 144 | 32 | 15 | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 105 | 743 | 38 | 0 | 0 | 0 | 0 | 0 | 0 | 347 | 0 | 0 | 0 | 0 | 0 | 207 | 162 | 39 | 442 | 991 | 21 | 35 | 296 | 233 | 316 | 322 | 0 | 0 | 0 | 14007 |
| Subsea | 0 | 0 | 28 | 2 | 0 | 24 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 19 | 1 | 1 | 4 | 35 | 42 | 29 | 0 | 0 | 0 | 0 | 89 | 229 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 36 | 114 | 0 | 0 | 0 | 0 | 40 | 186 | 7 | 228 | 7 | 13 | 12 | 4 | 21 | 3 | 2 | 33 | 7 | 76 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 36 | 38 | 0 | 1 | 0 | 0 | 0 | 0 | 34 | 113 | 21 | 1 | 0 | 0 | 0 | 0 | 0 | 3 | 9 | 10 | 85 | 214 | 136 | 1 | 0 | 0 | 0 | 24 | 30 | 23 | 15 | 204 | 31 | 487 | 21 | 2 | 58 | 0 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 1 | 40 | 2940 |
| REMS | 0 | 0 | 17 | 4 | 0 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 12 | 1 | 3 | 2 | 12 | 6 | 28 | 0 | 0 | 0 | 0 | 32 | 94 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 27 | 49 | 0 | 0 | 0 | 0 | 5 | 79 | 4 | 30 | 1 | 4 | 0 | 1 | 6 | 0 | 1 | 19 | 4 | 40 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 22 | 0 | 0 | 0 | 0 | 0 | 0 | 21 | 44 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 5 | 1 | 45 | 54 | 51 | 2 | 0 | 0 | 0 | 15 | 27 | 12 | 11 | 108 | 23 | 725 | 8 | 0 | 18 | 2 | 5 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 23 | 1727 |
| Surface | 0 | 0 | 1 | 0 | 2 | 5 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 15 | 0 | 0 | 2 | 8 | 6 | 3 | 0 | 0 | 0 | 0 | 33 | 36 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 27 | 0 | 0 | 0 | 0 | 11 | 68 | 2 | 36 | 1 | 3 | 0 | 2 | 8 | 3 | 0 | 2 | 2 | 47 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 148 | 60 | 1 | 0 | 0 | 0 | 0 | 0 | 12 | 23 | 11 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 8 | 28 | 32 | 42 | 1 | 0 | 0 | 0 | 7 | 19 | 12 | 2 | 33 | 7 | 328 | 10 | 1 | 12 | 1 | 3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 7 | 1146 |
```

### AG-24: How does severity distribution vary by year?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.4s

```
| year | 1.0 | 2.0 | 3.0 | 4.0 | 5.0 | Unknown | Total |
|---|---|---|---|---|---|---|---|
| 2018 | 8 | 26 | 9 | 0 | 0 | 2952 | 2995 |
| 2017 | 4 | 4 | 1 | 0 | 0 | 2639 | 2648 |
| 2019 | 22 | 34 | 22 | 2 | 2 | 2558 | 2640 |
| 2021 | 116 | 112 | 54 | 10 | 3 | 2016 | 2311 |
| 2020 | 32 | 35 | 21 | 7 | 0 | 2110 | 2205 |
| 2016 | 3 | 1 | 0 | 0 | 0 | 1678 | 1682 |
| 2023 | 639 | 559 | 287 | 33 | 4 | 0 | 1522 |
| 2024 | 606 | 571 | 240 | 38 | 6 | 0 | 1461 |
| 2022 | 629 | 493 | 226 | 38 | 6 | 54 | 1446 |
| 2025 | 390 | 374 | 128 | 16 | 2 | 0 | 910 |
```

### AG-25: What is the year-over-year trend of contusion/bruise injuries?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Total incidents: 360
Months with data: 86
Yearly breakdown:
  2016: 53
  2017: 103
  2018: 76
  2019: 28
  2020: 22
  2021: 43
  2022: 14
  2023: 9
  2024: 9
  2025: 3
```

### AG-26: How do incident counts compare across the top 10 operating centers?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
operating_center null rate: 4/19820 (0.0%)

| operating_center | Accident | Near Miss | Unknown | Total |
|---|---|---|---|---|
| N/A - Non Project Specific | 1976 | 1607 | 0 | 3583 |
| EMIA - TPIT - Italy - Rome | 263 | 257 | 598 | 1118 |
| NAM - FMCSurfSvsUS - USA - Houston | 229 | 137 | 318 | 684 |
| REGION NORTH AMERICA - TPUSA - USA - Hou | 455 | 168 | 1 | 624 |
| NAM - FMCSubseaServ - USA - Houston | 92 | 105 | 315 | 512 |
| NAM - TPUSA - USA - Houston | 130 | 63 | 310 | 503 |
| EMIA - STLNG - France - Paris | 364 | 102 | 0 | 466 |
| EMIA - FFRANCE - France - Le Trait (Flex | 70 | 118 | 251 | 439 |
| REGION YAMAL - STLNG - France - Paris | 326 | 87 | 0 | 413 |
| SUBSEA EUROPE - TUK - UK - Aberdeen (UKB | 116 | 57 | 209 | 382 |
| EMIA - TPINDIALTD - India - New Delhi | 74 | 115 | 176 | 365 |
| REGION A - TPFR - France - Paris | 248 | 98 | 0 | 346 |
| SUBSEA EUROPE - FMCLimitedENG - UK - Dun | 74 | 49 | 223 | 346 |
| SUBSEA EUROPE - TUK - UK - Aberdeen (TMO | 56 | 46 | 229 | 331 |
| REGION B - TPIT - Italy - Rome | 192 | 126 | 2 | 320 |
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

### CJ-08: Find crane incidents in the UK resulting in fractures.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-09: Find forklift incidents at construction sites with severity >= 3.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 13
Sample: ['INCIDENT::15134', 'INCIDENT::15148', 'INCIDENT::15794', 'INCIDENT::16414', 'INCIDENT::17286']
```

### CJ-10: Find vehicle road accident incidents resulting in injuries in the USA.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 26
Sample: ['INCIDENT::13085', 'INCIDENT::21932', 'INCIDENT::23454', 'INCIDENT::27029', 'INCIDENT::28188']
```

### CJ-11: Find incidents involving PPE with eye injuries during manufacturing.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 13
Sample: ['INCIDENT::11564', 'INCIDENT::15728', 'INCIDENT::17999', 'INCIDENT::22980', 'INCIDENT::23563']
```

### CJ-12: Find incidents involving chemical exposure resulting in environmental impact.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 69
Sample: ['INCIDENT::13470', 'INCIDENT::172', 'INCIDENT::17238', 'INCIDENT::18105', 'INCIDENT::20203']
```

### CJ-13: Find near-miss incidents involving scaffolding at height.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 60
Sample: ['INCIDENT::14321', 'INCIDENT::24555', 'INCIDENT::500940', 'INCIDENT::501641', 'INCIDENT::501648']
```

### CJ-14: Find crane incidents in Houston during 2018.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 17
Sample: ['INCIDENT::569963', 'INCIDENT::570340', 'INCIDENT::574246', 'INCIDENT::574985', 'INCIDENT::581728']
```

### CJ-15: Find stored-energy incidents with head injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 22
Sample: ['INCIDENT::10105', 'INCIDENT::10882', 'INCIDENT::11124', 'INCIDENT::13221', 'INCIDENT::14077']
```

### CJ-16: Find marine incidents involving ROVs with equipment failures.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 7
Sample: ['INCIDENT::10944', 'INCIDENT::1314', 'INCIDENT::514184', 'INCIDENT::518912', 'INCIDENT::548364']
```

### CJ-17: Find vehicle road accidents at construction sites with injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 33
Sample: ['INCIDENT::13085', 'INCIDENT::15417', 'INCIDENT::16688', 'INCIDENT::18028', 'INCIDENT::23454']
```

### CJ-18: Find manual handling incidents with sprain/strain injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 19
Sample: ['INCIDENT::13444', 'INCIDENT::15186', 'INCIDENT::29185', 'INCIDENT::507532', 'INCIDENT::509296']
```

### CJ-19: Find stored-energy dropped-object incidents with lacerations.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 12
Sample: ['INCIDENT::20597', 'INCIDENT::504859', 'INCIDENT::520167', 'INCIDENT::553088', 'INCIDENT::562819']
```

### CJ-20: Find near-miss incidents involving forklifts in 2023.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.4s

```
Matching incidents: 53
Sample: ['INCIDENT::12422', 'INCIDENT::12535', 'INCIDENT::12642', 'INCIDENT::12794', 'INCIDENT::12820']
```

### CJ-21: What safety controls successfully mitigated harm across all incidents?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Total MITIGATED_BY edges: 849
Unique incidents: 721

Top successful controls/mitigations (676 distinct):
  injury: 20
  injuries: 19
  safety glasses: 10
  PPE: 10
  fire: 8
  spill: 8
  fire extinguisher: 7
  SOPEP equipment: 6
  Medic: 6
  Spill kit: 6
  First aid: 5
  harm to personnel: 5
  no injuries: 5
  gloves: 5
  SOPEP kit: 4
  extinguisher: 4
  barricaded area: 4
  First Aider: 4
  eye wash station: 3
  Absorbent pads: 3

Top harms mitigated:
  fire: 21
  injury: 6
  spill: 5
  minor fire: 5
  hose failure: 5
  hydraulic oil leak: 4
  laceration: 4
  oil leak: 4
  oil spill: 4
  irritation to her skin on her face and eyes: 4

Sample edges (harm → control that worked):
  [1093] small cut to form on his head → First aid
  [11035] injury → Axiom Medical
  [11746] cotton T Shirt under his long sleeve → melted to his skin
  [12933] bolt dropped → no personnel were in the DROPS area at the time of incident
  [13338] small cut on his finger → nitrile gloves
  [13376] roller cage being in place → harm to personnel
  [1398] drive roller tipped over → personnel outside barrier fencing
  [14083] spanner dropped → level 2 red barriers
```

### CJ-22: What barriers and controls failed most frequently across all incidents?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Total FAILED_CONTROL edges: 828
Unique incidents: 764

Top failed barriers (738 distinct):
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
  Barriers: 3
  Polyurethane foam in valve box caught on fire: 3
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 3
  leak: 3
  generator fill nozzle: 3
  pipe slipping off the wooden skid support: 3
  ROV: 3
  spill containment: 2
  fire blanket: 2
  dropped object: 2

Top hazards with barrier failures:
  Use of personal protective equipment: 6
  fire: 4
  safety glasses: 4
  hydraulic oil leak: 3
  hydraulic hose failure: 3
  transfer hose rupture: 3
  slipped and fell: 3
  minor fire: 3
  CCB portvakt being unfamiliar with the system: 2
  PPE: 2

Sample edges (hazard → failed barrier):
  [10176] fire extinguisher malfunctioned (handle hinge broken) → flame extinguished
  [10424] stack leaned forward → lifting strap
  [11262] BPV → pressure isolation
  [11599] tag lines not fitted → loss of control of the load
  [1203] hydraulic leak from the rear of the Baker Hughes pump skid → ROV XLX 93 visual inspection
  [12088] EDGE safety gloves with performance levels 4342B to EN 388, but it was already wasted → superficial cutting of two fingers of my right
  [12762] leaking hydraulic oil → all oil was contained within the cabinet
  [1288] back of the glove (fabric material) does not protect him from the hot water → burn on the back of the hand
```

### CJ-23: What temporal sequences (event A preceded event B) are most common?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Total PRECEDED_BY edges: 508
Unique incidents: 382

Top temporal sequences (A → B means A preceded B):
  Fire Teams on board to carried out adjacent areas → Muster outside the vessel: 2
  hit the right head light → side collision: 1
  Facilities Supervisor advise to stop work → supervisor spotted: 1
  directed the supervisor of the PIH to carry out the mitigation → HSE team was operated via radio and after evaluation: 1
  PIH team started the mitigation with the support of the maintenance of TPFMC → field engineer went to the site to evaluate and support in the treatments: 1
  fume extractor → overhead crane(MD-1) at Bay D: 1
  I arrive before the preparator → call of the RUAM ( I ) who was in the tool service: 1
  asks to warn an emergency SST → I arrive before the preparator: 1
  Several SST arrive to take care of the victim → asks to warn an emergency SST: 1
  A SST strain asks for an emergency SST → Decision with the SST to call the guard post for a call: 1
  application of anti-biotic ointment and a Band-Aid → thumb cut: 1
  worker returned to work → thumb cut: 1
  work site was checked for further potential dropped objects → incident was not reported at the time: 1
  Unit is not in location → Operator parked the FL1296 Electric pallet to inside warehouse charging station: 1
  helped the Injured Technician → rolled ankle: 1
  reported the issue to client rep and TechnipFMC Service manager → helped the Injured Technician: 1
  investigation began → reported the issue to client rep and TechnipFMC Service manager: 1
  Tech 1 moved the crane from GWA3 to GWA6 → incident occurred: 1
  valve was replaced and tagged for out of service → pressure test operations were halted: 1
  field superintendent, Bill MacKinnon, took the valve back to Minot for inspection → valve was replaced and tagged for out of service: 1

Sample edges (event → prior event):
  [10] side collision preceded by hit the right head light
  [11544] supervisor spotted preceded by Facilities Supervisor advise to stop work
  [11771] HSE team was operated via radio and after evaluation preceded by directed the supervisor of the PIH to carry out the mitigation
  [11771] field engineer went to the site to evaluate and support in the treatments preceded by PIH team started the mitigation with the support of the maintenance of TPFMC
  [12593] overhead crane(MD-1) at Bay D preceded by fume extractor
  [14780] call of the RUAM ( I ) who was in the tool service preceded by I arrive before the preparator
  [14780] I arrive before the preparator preceded by asks to warn an emergency SST
  [14780] asks to warn an emergency SST preceded by Several SST arrive to take care of the victim
```

### CJ-24: What are the top causal factors leading to dropped-object incidents?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Dropped-object incidents (via RCC): 3,145
With CAUSAL edges: 2,031
Total CAUSAL edges: 5,311

Top causal factors for dropped objects:
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 81
  Stored energy (dropped objects): 21
  dropped object: 11
  high winds: 8
  unexpected movement of the gantry crane: 7
  unsecured equipment on pallet: 7
  helmet dropped approximately 6m from the platform down to the quayside: 6
  Information tag missing from the trolley: 5
  bow shackle falling off at the bottom of the Cycle: 5
  vendaval: 5
```

### CJ-25: What are the top causal factors in vehicle-related incidents?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Vehicle/traffic incidents (via RCC): 1,205
With CAUSAL edges: 700
Total CAUSAL edges: 1,663

Top causal factors for vehicle incidents:
  Motor Vehicle Road Accident: 44
  collision: 9
  IMPACT: 4
  medium snowfall: 4
  shock: 4
  forklift mast striking the MQC plate on one of YT manifolds: 4
  slipped and fell: 4
  vessel moved 2 meters: 4
  fall: 3
  overturned on the highway: 3
```

### CJ-26: What causal chains lead to fracture injuries?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Fracture incidents (via INJURY_TYPE): 228
With CAUSAL edges: 176
Total CAUSAL edges: 472

Top causal factors leading to fractures:
  manual handling: 6
  fracture: 5
  slipped: 5
  PTJ scaffolder fall down: 4
  slipping and falling: 3
  lost his balance: 3
  slipped and fell: 3
  angle hit two workers: 3
  upper chain jack hook hit the IP in the nose: 3
  part of the frame landed on the IP’s foot: 3
```

### CJ-27: Find crane incidents in Norway resulting in injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 57
Sample: ['INCIDENT::10929', 'INCIDENT::12016', 'INCIDENT::12595', 'INCIDENT::12655', 'INCIDENT::13512']
```

### CJ-28: Find incidents with both equipment failure and manual handling root causes.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-29: Find high-severity incidents at construction sites involving scaffolding.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 2
Sample: ['INCIDENT::129', 'INCIDENT::16468']
```

### CJ-30: Find incidents involving hoses with environmental impact at offshore locations.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 4
Sample: ['INCIDENT::12909', 'INCIDENT::21202', 'INCIDENT::29647', 'INCIDENT::8407']
```

### CJ-31: Find severity 5 incidents involving cranes with injury impact.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 3
Sample: ['INCIDENT::13746', 'INCIDENT::21939', 'INCIDENT::9106']
```

### CJ-32: What causal chains lead from equipment failures to injuries (L2 traversal)?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Start: 15217 EQUIPMENT nodes matching '.*'
  --CAUSAL--> EVENT: 1254 nodes
  --CAUSAL--> INJURY: 105 nodes
  Final: 105 INJURY nodes, 105 distinct values

Top 10:
  painful wrist (without fracture): 1
  Calf part of right leg: 1
  Minor contusions to his knees and hand: 1
  FST struck in the chest: 1
  cut fingers on left hand: 1
  contacting the employee in the back of his head: 1
  superficial injury on right hand middle finger: 1
  fracture to his left arm radius bone just above the wrist: 1
  dislocation in the right foot: 1
  bleeding from his face: 1
```

### CJ-33: What events are caused by corrosion conditions (L2 traversal)?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Start: 28 CONDITION nodes matching 'corros'
  --CAUSAL--> EVENT: 18 nodes
  Final: 18 EVENT nodes, 18 distinct values

Top 10:
  dropped object: 1
  corrosion pinhole: 1
  hydraulic oil return tube was stolen: 1
  disconnection of mooring lines: 1
  hydraulic fluid sitting on top of the quench water: 1
  small leak coming from a hydraulic hose located on the TTS crane boom: 1
  rupture of the safety steel cable: 1
  ammonia eats through the pipework: 1
  broken strands on the umbilical wraps below the damaged section: 1
  securing rivets failed: 1
```

### CJ-34: What injuries result from failed controls (L2 traversal)?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Start: 8944 CONDITION nodes matching '.*'
  --FAILED_CONTROL--> EVENT: 118 nodes
  --CAUSAL--> INJURY: 11 nodes
  Final: 11 INJURY nodes, 11 distinct values

Top 10:
  minor laceration on his finger: 1
  pinched left thumb: 1
  cut wound of the left hand: 1
  technician getting a lot of oil on their hair, face, and clothes: 1
  Third Party Contractor sprayed by oil: 1
  Closed fracture of the lateral malleolus on the right: 1
  Potential for harm from contact as the item rebounded to deck: 1
  helper got hydraulic oil on clothes, hair and face: 1
  cut in face: 1
  landed on scaffolding platform then bounced up and touched the nearby workers' lower leg: 1
```

### GL-01: What are the most significant safety risk clusters across TechnipFMC global operations?
**Type:** Global | **Status:** ✅ | **Time:** 9.2s

```
Total communities: 11125
Top 10 by size:

  Community 1 (size=10602):
    INCIDENT: 3177 (e.g. ['ACCIDENT 22315 - Environmental - Pipe fitting failure from transfer winch upper drum - Hydraulic oil leak into moonpool of 5 Litres', 'ACCIDENT 556616 - First Aid (Non Work Related) - 074250C001 - Marathon IRM 2017 - Deep Arctic - 18/10/17 - Diver having a suspected seizure in Sat', 'ACCIDENT 601642 - Damage Incident - 07.08.2018 - Deep Orient - Greater Enfield - VLS Gutter handrail contacted the VLS Crane'])
    EQUIPMENT: 3017 (e.g. ['P3 winch', 'tool basket', 'steel toe cap boots_x000D_'])
    LOCATION: 1991 (e.g. ['Survey desk', 'position on deck', 'Clipper Quay'])
    ORGANIZATION: 1643 (e.g. ['scott pallet material movement team', 'OMV (NORGE) AS', 'scanning team'])
    BODY_PART: 259 (e.g. ['left mid-forearm', 'arc eye', 'bottom face of the cavity'])
    EVENT: 250 (e.g. ['significant damage to the outside and inside of the wall', 'Damage to Barriers', 'beam fell from the back of the truck bed to the ground'])
    INJURY_TYPE: 105 (e.g. ['left side lumber back pain', 'MOI', 'lateral deviation'])
    CONDITION: 61 (e.g. ['load was not suspended', 'unauthorized / unapproved route of the release', 'access to the deck being barriered off'])
    INJURY: 40 (e.g. ['IP began to experience minor chest pain', 'contusion of his left elbow and wrist', 'small surface burns in the region of the stone'])
    ACTION: 35 (e.g. ['wearing hard hat instead of bump cap', 'MPFM secured to the pallet by way of pallet banding', 'toe boards should be fitted'])
    MATERIAL: 10 (e.g. ['leaked hydraulic fluid', 'damaged rollers with the approximate weight of 34 grams each', 'piece of wood weighing approximately 1.55 kg'])
    ROOT_CAUSE_CATEGORY: 7 (e.g. ['Electrical', 'Biological - Animals, Bacteria, Viruses and Funguses', 'Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects)'])
    PERSON: 7 (e.g. ['operator responsible for driving the wire was near', 'people in the radius of the load', 'people in the radius of the fall of the pipes'])

  Community 2 (size=9993):
    INCIDENT: 3952 (e.g. ['INCIDENT 729534 - Brakes failed LD3733', 'ACCIDENT 607246 - Recordable hand injury-Davis, CA', 'INCIDENT 643700 - Lost Time Injury - Odessa Supercenter parking lot - 7/8/19 - Sprained ankle, broken medial bone foot'])
    EQUIPMENT: 2374 (e.g. ['generator_x000D_', 'Subsea Drilling equipment', 'Jay Gun'])
    LOCATION: 1622 (e.g. ['new work location', 'EVDO vessel dress out yard', 'shopping centers'])
    ORGANIZATION: 1060 (e.g. ['Ross Shire', 'Spitzer', 'Tech'])
    BODY_PART: 337 (e.g. ['both eyes', 'rear bumper', 'guard rail'])
    EVENT: 299 (e.g. ['hydraulic leak on actuator line for H07', 'HPU damaged', '5S operation carried out in the manufacturing batiment'])
    INJURY_TYPE: 142 (e.g. ['smashed finger', 'tingling in fingers', 'split'])
    CONDITION: 80 (e.g. ['NOTICED UNTIL EMPLOYEE WENT TO USE IT', 'damaged', 'chocks not secured fully with duplex nails'])
    ACTION: 59 (e.g. ['could not move over any further', 'incorrect application of pressure into the lower piston port', 'disposed of'])
    INJURY: 41 (e.g. ['egg on his left upper leg', 'laceration to his left middle finger', 'cut injury over his columella near sub nasal'])
    ROOT_CAUSE_CATEGORY: 12 (e.g. ['Hazard Identification & Risk Assessment', 'Standard Operating Procedures, Procedures & Work instructions', 'Motor Vehicle Road Accident'])
    MATERIAL: 10 (e.g. ['piece of tie wire', 'anti-histamine tablet', 'pressurized water'])
    PERSON: 5 (e.g. ['Goods Inwards Inspector', 'trained First Aider', 'Driver'])

  Community 3 (size=5416):
    INCIDENT: 1877 (e.g. ['INCIDENT 709512 - Near Miss - 033316A001 - Maintenance Period - Amsterdam, Damen Shipyard - Skandi Vitoria - 16 March 2021 - COVID Breach - Vessel contractor entered the bridge without authorization', 'NEAR MISS 13567 - Vazamento de resíduo oleoso - Contêiner ROV SKN', 'NEAR MISS 8173 - 736066 - NM - Macae Base Cabiunas - Queda de tambor de HW durante movimenta??o com Ponte Rolante.'])
    EQUIPMENT: 1227 (e.g. ['air jet', 'fire extender', 'latch of the door lock'])
    LOCATION: 1001 (e.g. ['BR 262', 'Saint Wandrille quayside', 'Jucu'])
    ORGANIZATION: 706 (e.g. ['catering company', 'EVDT', 'Spirodutos company'])
    BODY_PART: 235 (e.g. ['male bathroom', 'body', 'patolas'])
    EVENT: 158 (e.g. ['tube fell between the DRT car and the transfer table', 'drop', "accidental contact between the employee's left knee and the end of the spool (point)"])
    INJURY_TYPE: 110 (e.g. ['flat-foot fall', 'type caravela', 'unable to hold on'])
    INJURY: 33 (e.g. ['slight scory??o', 'minor abrasions on her legs and arms', 'deodos on the foot'])
    CONDITION: 33 (e.g. ['the height from the roof to the floor is approximately 30 meters', 'flooding on the floor', 'loose soil at the edge'])
    ACTION: 17 (e.g. ['Book in/out system not being followed', 'building management decided to stop the works', 'restrictive measures with administrative activities'])
    ROOT_CAUSE_CATEGORY: 13 (e.g. ['Equipment condition', 'Hot/cold surfaces or media', 'Pinch point'])
    MATERIAL: 4 (e.g. ['concrete portion of the roof', 'PVC connections, weighing a maximum of 0.65kg', 'nylon parts (3 on main deck, one on the barge)'])
    PERSON: 2 (e.g. ['operator in the face', 'people in the environment'])

  Community 4 (size=4178):
    INCIDENT: 1313 (e.g. ['INCIDENT 739012 - First Aid 065 - MIDOR - Egypt - 1.16.2021 - PTJ Labor Suffered Ankle Twist', 'ACCIDENT 609681 - FAC - Yamal LNG Project - Sabetta - 25.09.2018 -  pinching of the left hand thumb', 'ACCIDENT 531914 - MDA - 61402S - Zeebrugge/NID - 7/03/17 - Equipment boxe found damaged at BISY Warehouse'])
    LOCATION: 743 (e.g. ['Jetty SPP-322', 'earthworks area', '3rd level medical post'])
    EQUIPMENT: 639 (e.g. ['steel rebars', 'section of cable tray', 'manipulator truck'])
    ORGANIZATION: 574 (e.g. ['_x000D_ Hospital', 'OJSC Yamal LNG', 'OOO SOGAZ-Medservice'])
    INJURY_TYPE: 241 (e.g. ['spraining of ligaments', 'fracture and laceration', 'right ankle dislocation'])
    BODY_PART: 237 (e.g. ['I metacarpal phalanx', 'left knee joint area', 'axillary'])
    EVENT: 187 (e.g. ['slipped and fell down on the left leg', 'disc got caught and shattered', 'unexpected move of the step ladder'])
    INJURY: 100 (e.g. ['bruise of the right elbow joint', 'back and leg ache', 'injuring his left leg'])
    CONDITION: 65 (e.g. ['cut edge of the crown', 'genetic predisposition of the IP toward this genetic illness', 'observed the swallowed the feeling'])
    ACTION: 61 (e.g. ['unintentionally grabbed the cable', 'installation of the wire from the pilot release valves to the manual handle', 'Treatment: Immobilization with cast'])
    MATERIAL: 10 (e.g. ['debris', 'unsecured wooden edging strip (500g)', 'wooden sheet with sharp edge'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Falls, slips and trips on same level (without potential to fall to lower level)', 'Fall to lower level / fall to water / loose materials (e.g. silos with granulate)', 'Explosives / potential explosives'])
    PERSON: 3 (e.g. ["IP's face", 'REGA slinger', 'SNEMA wireman walking backwards'])

  Community 5 (size=3839):
    INCIDENT: 1477 (e.g. ["NEAR MISS 641250 - NM - ARM11 - 24/06/19 - Rupture d'un chapeau d'amarrage d'une ligne d'amarrage", 'ACCIDENT 592983 - Financial Impact - Lyon Offices - 22/05/18 - Car accident - no casualties', 'INCIDENT 712588 - PA/SITE PROPRE /14/04/2021/FISSURE SUR STRUCTURE ROLL PACKER'])
    EQUIPMENT: 756 (e.g. ['frelons', 'glass protection', 'pen'])
    LOCATION: 520 (e.g. ['bobinoir', 'emergency', 'basin 3'])
    ORGANIZATION: 418 (e.g. ['BADT', 'DERICHEBOURG Environment REVIVAL', 'ground operators'])
    BODY_PART: 176 (e.g. ['c.te right', 'return sabot level', 'one of the feet'])
    EVENT: 175 (e.g. ['spilling of fluids onto concrete ground', 'blade tip puncturing the glove', 'RUAP was warned after this signal and the lights were turned off'])
    INJURY_TYPE: 117 (e.g. ['No body injury', 'mild', 'back pain'])
    INJURY: 77 (e.g. ['Injury: pelvic area', 'minor LTI', 'Injury (shoulder blades)'])
    ACTION: 57 (e.g. ['combination of training (press up’s, chin up’s, yoga and use of the punch bag) in conjunction with maintenance and repair in the engine room', 'detachment from the steel cable', 'bending down'])
    CONDITION: 47 (e.g. ['unsorted waste, no traceability of the waste', 'leg was blocked', 'Emergency stop button for "Jumbo patrol man (on the floor)" out of order'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['Environment- Over-consumption of energy, natural resources (water, ...)', 'Environment- Unsorted waste, no traceability of the waste;?', 'Climate (Heat/Cold/Humidity)'])
    PERSON: 5 (e.g. ['SA protected by its helmet', 'employee', 'informed to the HSE department and labor medicine'])
    MATERIAL: 5 (e.g. ['the edge of the lid', 'waterized MUD', 'red-colored water recovered in the network'])

  Community 6 (size=3146):
    INCIDENT: 898 (e.g. ['INCIDENT 654923 - NM_073876C001_EPCC-5_Pipe spool slide on the stairs case landed on ground from 1st Platform.', 'INCIDENT 645583 - Near miss_75352C001_IOCL DHDT site_Haldia_29.07.19_Cladding sheet fall from height', 'INCIDENT 681329 - NM_HURL,Barauni_the tractor with trolley collided with the goal post'])
    EQUIPMENT: 614 (e.g. ['hydraulic rig', 'load transmitting beams', 'portable working platform'])
    LOCATION: 563 (e.g. ['Convection tower-1', 'hazardous waste storage', 'open area'])
    ORGANIZATION: 330 (e.g. ['Sunshine Global Hospital', 'Onboard management/representatives', 'NHT/CCR'])
    EVENT: 287 (e.g. ['Bus movement had halted due to bad weather conditions', 'Showering the area around me', 'right hand index finger pinched between the 2-pin fork and the structure of the stabframe frame'])
    BODY_PART: 125 (e.g. ['right parietal area', 'his leg', 'back of his two fingers'])
    CONDITION: 112 (e.g. ['IP not wearing gloves', 'greasy knife', 'force of the motion'])
    INJURY_TYPE: 75 (e.g. ['nobody was harmed', 'Hard hit', 'cut'])
    ACTION: 63 (e.g. ['removal of gloves for additional dexterity', 'bevel operator pushed the emergency button', 'used an ice pack for swelling'])
    INJURY: 59 (e.g. ['cut to left hand index finger', 'piercing injury to his Right hand (palm)', 'stick on his fingers'])
    MATERIAL: 12 (e.g. ['damage of property', 'scaffold clamps that had recently been removed', 'protruding screw'])
    PERSON: 5 (e.g. ['employee not stopping to check on employee', 'employee working on scaffold', 'Person: Samsaliev Sakish of REGA JV'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Manual handling', 'Accumulation / Presence of explosive atmosphere', 'Use of personal protective equipment'])

  Community 7 (size=3069):
    INCIDENT: 1035 (e.g. ['NEAR MISS 24713 - Technician Injured Due to Inadequate Tool and Equipment Constraints', 'ACCIDENT 29673 - In connection with the movement of subject PN/SNr from building 85 back to Warehouse/Tent 140, the HCR Dummy fell off the transport pallet and onto the asphalt.', 'NEAR MISS 14646 - SPX TWLC2 TORQUE WRENCHE retaining ring give away'])
    EQUIPMENT: 770 (e.g. ['XT frame', 'plastic drip tray', 'Piston accumulators'])
    LOCATION: 492 (e.g. ['Uvdal', 'WS hall 3', 'Hall H'])
    ORGANIZATION: 425 (e.g. ['Island Valiant', 'Nordstream', 'Agility'])
    BODY_PART: 111 (e.g. ['l?kke', 'bottom of the door', 'steering head'])
    EVENT: 95 (e.g. ['hitting the back of his head', 'back welds unexpectedly broke', 'manifold drop approximately 50 mm down on to the supports'])
    INJURY_TYPE: 45 (e.g. ['stabbing wound', '3 cm laceration', 'burn like wound'])
    CONDITION: 37 (e.g. ['side was secured with only six screws, which were too short for the thickness of the wood', 'contact with a small bolt attached to a monorail cable tray', 'incorrect plate thickness'])
    INJURY: 28 (e.g. ['No permanent injury to personnel', 'small blunt cut on the forehead', 'cut in his right hand forefinger'])
    ACTION: 21 (e.g. ['removing a poster on the wall', 'stopped work before dismantling started', 'All stop was called'])
    MATERIAL: 4 (e.g. ['no material damage was inflicted', 'steel chip', 'property and equipment were not damaged'])
    PERSON: 3 (e.g. ['emergency team on yard', 'person opening the door fast from another side without seeing me', 'deck rigging crew'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['1. Internal NCR (issued by TechnipFMC or Partners)', 'Radiation (ionising / non ionising)', 'Difficult/Hindered operability of tools and equipment'])

  Community 8 (size=2845):
    LOCATION: 668 (e.g. ['Aliakmonas 1 River', 'negative side of the river', 'Mvakull village'])
    INCIDENT: 659 (e.g. ['NEAR MISS 557850 - NON Technip Owned - TAP-NM 06 - 2529 TAP - Greece/GSC00 - 27/10/2017 - Hit panel with head', 'ACCIDENT 607283 - NON Technip Owned - RNT-FAC 08 - 2529 TAP - Albania/ACS03 - 31/08/2018-  Finger laceration using grinder', 'ACCIDENT 618602 - NON Technip Owned - RNT-DA 07 - 2529 TAP - Albania/ACS03 - 07/12/2018- Fire coming from generator'])
    ORGANIZATION: 577 (e.g. ['APM Welding Crew', 'Drejtoria e kolaudimit te makinave', 'SCTR civil works'])
    EQUIPMENT: 495 (e.g. ['lifting supports', 'sheet piling rig', 'Site ambulance'])
    EVENT: 174 (e.g. ['fall to the deck', 'they were stopped immediately and returned to the scaffold platform', 'noise was heard when the tube point arrived near Cabine 03'])
    CONDITION: 76 (e.g. ['cylinder, tied on the structure, was without a cap and almost empty', 'Concerns had been raised previously regarding the supervisors safety performance', 'left trench slope inclination off limits (60o instead of 53o max)'])
    BODY_PART: 52 (e.g. ['ankle_x000D_', 'right top front', 'sheeve'])
    INJURY_TYPE: 46 (e.g. ['ripping', 'near miss', 'first degree burn'])
    INJURY: 44 (e.g. ['blade cut IP’s left ring finger slightly through his gloves', 'hot water on the members right forearm', 'some of it getting into his right eye'])
    ACTION: 40 (e.g. ['disconnected the hose assembly at the chocolate and hot water mixer end on a coffee machine', 'removal of project equipment sea fastenings', 'failure to sign in confined space entry log'])
    MATERIAL: 8 (e.g. ['fuel materials that were inside the equipment', 'loose items', 'fine sand'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Inadequate Supervision', 'Illumination / sight / visibility', 'Unfamiliar personnel'])
    PERSON: 2 (e.g. ['Nikita Chirko', 'the crew consisted of 1 supervisor, 2 excavator operators, 2 side boom operators'])

  Community 9 (size=1971):
    INCIDENT: 624 (e.g. ['NEAR MISS 559103 - N/M - APSB - Mounting Bay 6 - Jumbo ROU 6 contacted the yellow barrier', 'NEAR MISS 556032 - Near Miss - OUI JV Rapid - Pengerang, Johor - 13 Oct 2017 - A part of a ceiling at the hot kitchen in Mess Hall 2 collapsed', 'NEAR MISS 17475 - Hydraulic oil leak from sky lift'])
    EQUIPMENT: 444 (e.g. ['torque multiplier jig', 'SBMS SL', 'temporary reel'])
    LOCATION: 426 (e.g. ['vacant desk', 'Kota Tinggi', 'Jascon 34'])
    ORGANIZATION: 285 (e.g. ['Mudajaya 1900', 'ATSB Operation', 'crew and contractor'])
    EVENT: 64 (e.g. ['fall approximately 1 meter', 'chemical spillage around the AUR rail area', 'detached from the pneumatic piston rod & dropped to the ground'])
    BODY_PART: 55 (e.g. ['rear left body', 'glove protected finger', 'left side of his nose'])
    INJURY_TYPE: 30 (e.g. ['Counterpain', 'scalds', 'MRI scan'])
    CONDITION: 18 (e.g. ['improvised connection between a tube and mango inside the channel', 'extension did have a pat test sticker applied but has become faded and is not easily read', 'not flowing into the domestic drain'])
    ACTION: 10 (e.g. ['crew and contractor stop the job', 'scaffold jack base used as a hammer', 'use of air compressor suspended'])
    INJURY: 10 (e.g. ['pinched the tip of his thumb', 'suffering pain in his right knee', 'finger injury (Right hand thumb)'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Psycho social - Alcohol and drugs abuse', 'Weather Condition', 'Electrical current / electrocution / ESD / electromagnetic Fields'])
    MATERIAL: 1 (e.g. ['wooden packing block'])
    PERSON: 1 (e.g. ['stray dog'])

  Community 10 (size=1921):
    INCIDENT: 643 (e.g. ['NEAR MISS 578501 - NM-TU Inc. -18.03.24- Dropped Object (ID Tag fell off reel)', 'ACCIDENT 627417 - LTI - BSR Coating Facility - Struck hand on pipe fracturing hand - 26/02/19 - 073754C001 Shell FRAM', 'INCIDENT 680780 - NM - TUL - 04.06.2020 - Material ejected from extruder'])
    EQUIPMENT: 532 (e.g. ['bottom sweeper arms', 'gear', 'Thermal Inbound rack'])
    LOCATION: 288 (e.g. ['Shepherd main access gate', 'LBCT line', 'Dorado'])
    ORGANIZATION: 241 (e.g. ['Stores', 'TIMAS SUPLINDO, PT', 'SOS'])
    EVENT: 79 (e.g. ['grinding', 'ankle twisted underneath him', 'IP tripped over the release mechanism'])
    INJURY_TYPE: 43 (e.g. ['No major cut', 'Medical treatment incident', 'nick'])
    BODY_PART: 38 (e.g. ['index and pinky finger', 'Axle 11', 'Umbilicals'])
    CONDITION: 32 (e.g. ['earth connection', 'environmental risk', 'entry manhole not provided with drip tray'])
    ACTION: 15 (e.g. ['placed "snakes" around the drain', 'Extinguished by C02 fire extinguisher', 'Norskan riggers moving Yokohamas fluters without TechnipFMC staff assistance'])
    INJURY: 9 (e.g. ['first and second-degree burns to his forearms and left armpit area', 'Employee was not injured', 'sheath damage'])
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
**Type:** Global | **Status:** ✅ | **Time:** 0.7s

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

### GL-05: What are the most common equipment-body part co-occurrences across all incidents?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Total distinct (equipment, body_part) pairs: 13045
Top 20:
  safety glasses + eye: 51 incidents
  PPE + eye: 39 incidents
  gloves + finger: 36 incidents
  gloves + left hand: 30 incidents
  face shield + eye: 17 incidents
  hammer + left hand: 16 incidents
  crane + finger: 16 incidents
  PPE + left hand: 15 incidents
  pallet + finger: 14 incidents
  PPE + finger: 14 incidents
  pallet + left foot: 13 incidents
  hammer + finger: 11 incidents
  swab + eye: 11 incidents
  forklift + left hand: 11 incidents
  compressor + left hand: 11 incidents
  forklift + left foot: 11 incidents
  pallet + left hand: 10 incidents
  safety glasses + face: 10 incidents
  pipe + finger: 10 incidents
  forklift + finger: 10 incidents
```

### GL-06: How do safety profiles compare across the top 5 clients by incident volume?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Top 5 clients by incident count:

  TECHNIPFMC (4688 incidents):
    Types: {'Accident': 1729, 'Near Miss': 1469}
    Severity dist: {1: 598, 2: 637, 3: 286, 4: 44, 5: 10}
    Mean severity: 1.88

  JSC YAMAL LNG (1302 incidents):
    Types: {'Accident': 884, 'Near Miss': 418}
    Severity dist: {}
    Mean severity: 0.00

  FLEXI FRANCE (1017 incidents):
    Types: {'Near Miss': 404, 'Accident': 338}
    Severity dist: {1: 290, 2: 54, 3: 27, 4: 3}
    Mean severity: 1.31

  IP (875 incidents):
    Types: {'Accident': 582, 'Near Miss': 31}
    Severity dist: {1: 92, 2: 81, 3: 45, 4: 5, 5: 1}
    Mean severity: 1.85

  N/A - No Vendor (820 incidents):
    Types: {'Near Miss': 362, 'Accident': 458}
    Severity dist: {1: 314, 2: 367, 3: 125, 4: 12, 5: 2}
    Mean severity: 1.81
```

### GL-07: Are there seasonal (monthly) patterns in incident frequency?
**Type:** Global | **Status:** ✅ | **Time:** 0.6s

```
Monthly incident totals (all years combined):
  Jan: 1653 (+0.1%)
  Feb: 1558 (-5.7%)
  Mar: 1671 (+1.2%)
  Apr: 1437 (-13.0%)
  May: 1526 (-7.6%)
  Jun: 1623 (-1.7%)
  Jul: 1825 (+10.5%)
  Aug: 1799 (+8.9%)
  Sep: 1639 (-0.8%)
  Oct: 1834 (+11.0%)
  Nov: 1571 (-4.9%)
  Dec: 1684 (+2.0%)

Peak months (>15% above avg): none
Trough months (>15% below avg): none
```

### GL-08: What are the top root causes by geographic region?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Regions with RCC data: 10

  Europe (6682 categorised incidents):
    Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 613
    Hazardous liquids (exposure to / spill / loss of containment /pollution): 571
    Equipment condition: 495

  North America (3973 categorised incidents):
    Hazard Identification & Risk Assessment: 372
    Standard Operating Procedures, Procedures & Work instructions: 302
    Motor Vehicle Road Accident: 287

  Asia Pacific (2998 categorised incidents):
    Falls, slips and trips on same level (without potential to fall to lower level): 357
    Hazard Identification & Risk Assessment: 250
    Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 227

  South America (1923 categorised incidents):
    Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 214
    Hazardous liquids (exposure to / spill / loss of containment /pollution): 187
    Equipment condition: 185

  India (745 categorised incidents):
    Manual handling: 106
    Stored energy (dropped objects): 60
    Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 55

  Africa (645 categorised incidents):
    Falls, slips and trips on same level (without potential to fall to lower level): 95
    Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 72
    Equipment condition: 42

  Middle East (604 categorised incidents):
    Inadequate Supervision: 69
    Motor Vehicle Road Accident: 52
    Hazard Identification & Risk Assessment: 51

  Republic of. Please update lookup table. (14 categorised incidents):
    Stored energy (pressure, tension): 4
    Stored energy (dropped objects): 3
    Unprotected/unguarded moving machine parts (struck by/caught by ): 2

  Republic of the - Pointe-Noire. Please update lookup table. (1 categorised incidents):
    Biological - Animals, Bacteria, Viruses and Funguses: 1

  Valves and Trees - Nusajaya Campus 1 Manufacturing - Welding and Location: Malaysia - Nusajaya. Please update lookup table. (1 categorised incidents):
    Workplace layout / congestion: 1
```

### GL-09: How many incidents mention burns in narrative but have no burn injury type extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'burn': 177
  With INJURY_TYPE extracted: 108
  WITHOUT INJURY_TYPE extracted (gap): 69
  Gap rate: 39.0%

Sample gap incidents:
  #12111: "Employee was TIG welding a clamped piece of material on a welding table. While welding he inadvertently dropped the weld..."
  #1288: "Environmental condition: The Deep Blue is in the Mero 1 field   Events leading up to the incident/Incident: Employee in ..."
  #14461: "Around 15:00 local time (8 am HOU time) today, during start-up activities with the WOCS container, our WOCS operator Mag..."
  #14668: "A contractor was injured and received first aid when he was grinding and a hot ember went into his glove causing a minor..."
  #19666: "One of the welder after welding trial sample tube, he allowed to cool down to some extent and then kept on welding machi..."
```

### GL-10: How many incidents mention fractures in narrative but have no fracture injury type extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'fracture': 442
  With INJURY_TYPE extracted: 227
  WITHOUT INJURY_TYPE extracted (gap): 215
  Gap rate: 48.6%

Sample gap incidents:
  #10005: "On 31 Aug 3:20 Pm, IP was tasked to configure the release sleeve on the penetrator. IP was assigned by leader to do this..."
  #10689: "Employee (ID# 30800964) was taking his lunch break, and carrying his lunch.  Employee walked behind a pedestal fan that ..."
  #10759: "Employee (ID#  , contract employee) was stapling a plastic covering to a wooden pallet with a hammer tacker.  The plasti..."
  #13256: "When leaving work, IP biked towards and up the ramp with an electrical bicycle. Heave El-Bikes often use this entrance. ..."
  #14068: "Hall C  A technician caught his thumb between an impact wrench and a steel structure. The bolt had to be screwed back a ..."
```

### GL-11: How many incidents mention cranes in narrative but have no crane equipment extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'crane': 1,873
  With EQUIPMENT extracted: 1,435
  WITHOUT EQUIPMENT extracted (gap): 438
  Gap rate: 23.4%

Sample gap incidents:
  #10173: "Environmental conditions: The Deep Blue is at Theodore spoolbase, weather dry and sunny.  Wind was 8 knots from the west..."
  #10232: "Description/summary of Incident:  The operation ongoing was the deployment of a buoyancy module for 1st end fitting DVC ..."
  #10239: "The North Sea Atlantic (NSA) was operational on DP in the Karish Field on co-ordinates 33°10,6’ N, 034°17,5’ E having co..."
  #10240: "The North Sea Atlantic (NSA) was operational on DP in the Karish Field on co-ordinates 33°10,6’ N, 034°17,5’ E having co..."
  #10349: "Environmental Conditions: The vessel was operational on DP in the Karish Field on co-ordinates 33°13,55’ N, 034°17,38’ E..."
```

### GL-12: How many incidents mention forklifts in narrative but have no forklift equipment extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'forklift': 1,075
  With EQUIPMENT extracted: 914
  WITHOUT EQUIPMENT extracted (gap): 161
  Gap rate: 15.0%

Sample gap incidents:
  #10233: "A third party 7"10k gate valve with a wireline cap was bolted onto a 36" and 14" spool standing up on the shop floor (va..."
  #10760: "At 2:00 pm the forklift operator was attempting to load two hangers on the truck for shipment. The operator loaded the f..."
  #12484: "Forklift operator was unloading a frac valve off of SAIA and was not paying attention, resulting in running into buildin..."
  #12749: "Employee driving the forklift pulled up to the bay door and waited for the sensor to open the door. When the door starte..."
  #13372: "NM 75 - IP entered forklift electrolyte spill area and was slightly affected by fumes..."
```

### GL-13: How many high-severity incidents (>=4) have no injury type extracted?
**Type:** Global | **Status:** ✅ | **Time:** 2.0s

```
Incidents with severity >= 4: 167
  With INJURY_TYPE extracted: 34
  WITHOUT INJURY_TYPE (gap): 133
  Gap rate: 79.6%

Severity breakdown of gap incidents:
  Severity 4: 117
  Severity 5: 16

Sample gap incidents:
  #7557 (sev=4.0): "A technician started the process of opening the Test Cell doors. During the process the door became ..."
  #30149 (sev=4.0): "During the motorcycle commute from home to the Campos bus station, where he would proceed to Macaé t..."
  #15506 (sev=5.0): "Two Pipe Coupons rolled off the trailer as truck was making right turn on to Richey.  JH Walker used..."
  #827 (sev=4.0): "At 16:10hrs there was sudden change in the Environment with heavy winds followed by rain for span of..."
  #17271 (sev=4.0): "On October 4, 2023 at approximately 09:45, TFMC personnel were prepping the WBRT assembly (P150372) ..."
```

### GL-14: How many injury-impact incidents have no body part extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.2s

```
Incidents with impact_type=Injury: 11,736
  With BODY_PART extracted: 6,132
  WITHOUT BODY_PART (gap): 5,604
  Gap rate: 47.8%
```

### GL-15: How many incidents have very short narratives (<100 chars) with no entities extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Incidents with narrative < 100 chars: 972
  With entity extraction: 645
  Without any entity extraction: 327
  Likely test/placeholder records: 5
  Genuine short narratives (no entities): 322

Sample short-narrative gaps:
  #7383: "by climbing the operator to slide and raped his back on the structure"
  #24420: "COMPANY VEHICLE LD5571 STRUCK A DEER"
  #159: "Employee slipped on ice when stepping briefly onto the lawn before entering the building."
  #27422: "Kranservice. Old open case. No explanation. Closing."
  #21332: "Car was in a stop position where other car hit it from the side."
```

### GL-16: How many incidents contain non-English narratives with reduced entity extraction?
**Type:** Global | **Status:** ✅ | **Time:** 0.2s

```
Overall mean entity extraction per incident: 2.14

Portuguese: 410 incidents, mean entities=2.95 (vs 2.14 overall), 50 with zero extraction
French: 4,591 incidents, mean entities=2.65 (vs 2.14 overall), 534 with zero extraction
Spanish: 384 incidents, mean entities=2.92 (vs 2.14 overall), 46 with zero extraction
Russian: 7 incidents, mean entities=2.71 (vs 2.14 overall), 0 with zero extraction

Total non-English incidents: 5,392
Total with zero extraction: 630
```

### GL-17: Find the 10 incidents most similar to incident #29857 (dropped pry bar) using hybrid embedding similarity.
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Seed incident: #29857

Top 10 most similar incidents (text embedding cosine):
  #24829 (sim=0.645) type=Near Miss sev=2.0 eq=['ROV', 'pry bar']
  #503254 (sim=0.583) type=Accident sev=? eq=['ROV', 'ROV cutter']
  #24785 (sim=0.574) type=Near Miss sev=2.0 eq=['ROV', 'Flange Spreader', 'ROV Hook']
  #20278 (sim=0.565) type=Accident sev=1.0 eq=['hydraulic shackle']
  #25648 (sim=0.561) type=Near Miss sev=2.0 eq=['ROV']
  #14126 (sim=0.552) type=Near Miss sev=1.0 eq=[]
  #683770 (sim=0.552) type=? sev=? eq=['ROV']
  #548733 (sim=0.540) type=Accident sev=? eq=['ROV Mil 208', 'latch beam', 'TMS main winch wire']
  #693551 (sim=0.540) type=? sev=? eq=['FMC Smart pack', 'Hydraulic Level Sensor']
  #639111 (sim=0.538) type=Accident sev=? eq=['water pump', '420 Dynaset Pump', 'ROV']

Seed equipment: ['ROV', 'lanyard', 'pry bar']
Equipment overlap (hit rate): 6/10 (60%)
```

### GL-18: Find the 10 incidents most similar to incident #569346 (ladder fall with broken teeth) using hybrid embedding similarity.
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Seed incident: #569346

Top 10 most similar incidents (text embedding cosine):
  #573223 (sim=0.791) type=Near Miss sev=? eq=['Sideboom']
  #633596 (sim=0.790) type=Near Miss sev=? eq=['Sideboom', 'boom', 'boom winch']
  #591511 (sim=0.759) type=Accident sev=? eq=['pipe section', 'excavator', 'belt']
  #585953 (sim=0.752) type=Near Miss sev=? eq=['CAT 594 Sideboom', 'two-joint pipe section', 'Sideboom']
  #522123 (sim=0.737) type=Near Miss sev=? eq=['Sideboom', 'boom']
  #545428 (sim=0.736) type=Near Miss sev=? eq=['Sideboom', 'lowering-in strap']
  #605490 (sim=0.736) type=Near Miss sev=? eq=['Sideboom']
  #539318 (sim=0.733) type=Near Miss sev=? eq=['Sideboom', 'excavator']
  #602722 (sim=0.723) type=Near Miss sev=? eq=['bending machine', 'lifting accessories']
  #514069 (sim=0.718) type=Accident sev=? eq=['Sideboom', 'side-boom 44.1404', 'side-boom No. 44.1404']

Seed equipment: ['Negative side string', 'Sideboom', 'Superior CPX-94', 'ladder']
Equipment overlap (hit rate): 8/10 (80%)
```

### GL-19: Do the top-10 text-similar incidents for a forklift accident share the same equipment type? (structural hit rate)
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Seed: #324 (equipment=forklift|flt)

  ✓ #663852 (sim=0.701) eq=['5 Ton forklift']
  ✗ #18838 (sim=0.683) eq=['truck']
  ✓ #8142 (sim=0.656) eq=['forklift']
  ✓ #721112 (sim=0.655) eq=['forklift boom']
  ✓ #676741 (sim=0.654) eq=['forklift']
  ✓ #517760 (sim=0.652) eq=['forklift', 'forks']
  ✓ #18589 (sim=0.650) eq=['pallet', 'forklift']
  ✓ #631498 (sim=0.648) eq=['forklift', 'hotwork equipment', 'truck']
  ✓ #530325 (sim=0.645) eq=['forklift']
  ✓ #8289 (sim=0.644) eq=['forklift']

Hit rate: 9/10 (90%)
```

### GL-20: Do the top-10 text-similar incidents for a crane near-miss share the same equipment type? (structural hit rate)
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Seed: #26866 (equipment=crane)

  ✓ #9622 (sim=0.744) eq=['crane', 'SOPEP kit']
  ✓ #18886 (sim=0.666) eq=['250T crane']
  ✗ #536624 (sim=0.665) eq=['stationary front-end loader']
  ✗ #667540 (sim=0.651) eq=[]
  ✓ #641469 (sim=0.650) eq=['FRC crane']
  ✓ #735720 (sim=0.647) eq=['15Te NOV crane']
  ✗ #1667 (sim=0.645) eq=['slider', 'SOPEP kit']
  ✓ #546946 (sim=0.640) eq=['vessel crane', '150T crane']
  ✓ #567597 (sim=0.639) eq=['crane']
  ✓ #22425 (sim=0.639) eq=['kenz crane']

Hit rate: 7/10 (70%)
```

### GL-21: How well do text embeddings and structural similarity agree on the top-10 most similar incidents? (method correlation)
**Type:** Global | **Status:** ✅ | **Time:** 0.6s

```
Compared text vs node2vec top-10 for 20 seed incidents
Mean overlap (Jaccard@10): 3.00%

Per-seed overlap:
  #10: 0%
  #100: 0%
  #10005: 0%
  #10016: 0%
  #10019: 0%
  #10021: 0%
  #1003: 10%
  #10044: 0%
  #1005: 0%
  #10064: 0%
```

### GL-22: Find incidents semantically similar to 'worker fell from scaffold due to missing guardrail' using text embeddings.
**Type:** Global | **Status:** ✅ | **Time:** 4.2s

```
Query: "worker fell from scaffold due to missing guardrail"

Top 10 semantically similar incidents:
  #531820 (sim=0.709) Near Miss/sev=? eq=['Module 200-PAR-005', 'several guardrail', 'scaffolding'] inj=['risk of fall']
  #709549 (sim=0.656) ?/sev=? eq=['GUARDRAIL', 'full body safety harness'] inj=[]
  #24560 (sim=0.647) Accident/sev=3.0 eq=['PPE', 'fall protection', 'ambulance'] inj=[]
  #24562 (sim=0.647) Accident/sev=3.0 eq=['PPE', 'fall protection', 'ambulance'] inj=[]
  #24563 (sim=0.647) Accident/sev=3.0 eq=['PPE', 'fall protection', 'ambulance'] inj=[]
  #24559 (sim=0.647) Accident/sev=3.0 eq=['PPE', 'fall protection', 'ambulance'] inj=[]
  #709551 (sim=0.638) ?/sev=? eq=['1-TMP-003 module'] inj=[]
  #735977 (sim=0.636) ?/sev=? eq=['grinder'] inj=[]
  #518862 (sim=0.636) Near Miss/sev=? eq=['safety belt', 'hand rail'] inj=[]
  #514067 (sim=0.631) Near Miss/sev=? eq=['Scaffold', 'helmet'] inj=[]
```

### GL-23: Find incidents semantically similar to 'crane load dropped because sling failed under tension' using text embeddings.
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Query: "crane load dropped because sling failed under tension"

Top 10 semantically similar incidents:
  #430 (sim=0.676) Accident/sev=2.0 eq=['single overhead crane CS86'] inj=[]
  #552629 (sim=0.666) Near Miss/sev=? eq=['train 2', 'compressor', '214-PAU-012'] inj=[]
  #697226 (sim=0.663) ?/sev=? eq=['four leg chain sling', '“O” round sling'] inj=[]
  #703298 (sim=0.663) ?/sev=? eq=['four leg chain sling', '“O” round sling'] inj=[]
  #725136 (sim=0.662) ?/sev=? eq=['transporting slings', 'tested hoisting devices'] inj=['No one was hurt']
  #504414 (sim=0.656) Near Miss/sev=? eq=['crane'] inj=[]
  #607608 (sim=0.646) Near Miss/sev=? eq=['gantry crane', 'trailer'] inj=['No any injury']
  #579815 (sim=0.636) Near Miss/sev=? eq=['LIEBHERR LTM 1090-4.1'] inj=[]
  #737511 (sim=0.635) ?/sev=? eq=['sling', 'truck platform'] inj=[]
  #30460 (sim=0.630) Accident/sev=2.0 eq=['third-party mobile crane'] inj=['kink']
```

### GL-24: Which equipment types appear most often in the top-10 similar incidents for high-severity events? (embedding-based pattern)
**Type:** Global | **Status:** ✅ | **Time:** 1.3s

```
High-severity incidents sampled: 50
Total high-severity with embeddings: 167

Most common equipment in similar-incident neighborhoods:
  crane: 35
  forklift: 34
  equipment: 14
  forks: 9
  truck: 7
  winch: 7
  actuator: 6
  ROV: 6
  sling: 6
  overhead crane: 6
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
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 192
Sample: ['INCIDENT::10674', 'INCIDENT::10923', 'INCIDENT::10992', 'INCIDENT::11942', 'INCIDENT::12909']
```

### IOGP-05: Which electrical incidents had lockout/tagout failures?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.2s

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
  left foot: 10
  shoulder: 10
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
  pain: 6
  personnel injury: 6
```

### IOGP-08: How many machinery and tool incidents resulted in hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 200
Sample: ['INCIDENT::10299', 'INCIDENT::10348', 'INCIDENT::10636', 'INCIDENT::10759', 'INCIDENT::10789']
```

### IOGP-09: What are the top injury types from moving vehicle and mobile equipment incidents?
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

### IOGP-10: How many vehicle incidents resulted in high-severity outcomes?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 33
Sample: ['INCIDENT::10171', 'INCIDENT::1184', 'INCIDENT::13358', 'INCIDENT::13602', 'INCIDENT::13614']
```

### IOGP-11: What body parts are most affected in vehicle/mobile equipment incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 842
Distinct BODY_PART values: 153
Top 10:
  BUMPER: 20
  FRONT BUMPER: 12
  tailgate: 8
  left leg: 8
  passenger side: 8
  rear bumper: 7
  shoulder: 6
  rear quarter panel: 5
  tail light: 5
  driver side: 5
```

### IOGP-12: Which countries have the most mechanical lifting/hoisting incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2001
Distinct LOCATION values: 61
Top 10:
  UK: 724
  USA: 313
  Norway: 103
  Brazil: 100
  Russia: 81
  Malaysia: 79
  India: 70
  China: 47
  Singapore: 32
  France: 27
```

### IOGP-13: What are the top root causes of mechanical lifting incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2001
Distinct ROOT_CAUSE_CATEGORY values: 48
Top 10:
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 293
  Stored energy (dropped objects): 206
  Equipment condition: 188
  Hazard Identification & Risk Assessment: 139
  Planning and coordination of works: 121
  Standard Operating Procedures, Procedures & Work instructions: 118
  Stored energy (pressure, tension): 103
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 93
  Equipment Suitability: 75
  Manual handling: 59
```

### IOGP-14: How many working-at-height incidents involved harnesses or lanyards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 74
Sample: ['INCIDENT::1193', 'INCIDENT::14083', 'INCIDENT::14519', 'INCIDENT::26102', 'INCIDENT::29857']
```

### IOGP-15: What injury types result from fall-to-lower-level incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1695
Distinct INJURY_TYPE values: 310
Top 10:
  contusion: 39
  sprain: 29
  closed fracture: 26
  fracture: 22
  injuries: 18
  bruise: 18
  pain: 18
  laceration: 18
  abrasion: 15
  wounds: 14
```

### IOGP-16: How do dropped object incidents break down by body part affected?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1160
Distinct BODY_PART values: 149
Top 10:
  left foot: 19
  left hand: 15
  shoulder: 15
  head: 11
  left leg: 9
  body: 6
  finger: 6
  arm: 5
  thumb: 4
  forearm: 4
```

### IOGP-17: How many tensioned line or snap-back incidents occurred?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 109
Sample: ['INCIDENT::11392', 'INCIDENT::11394', 'INCIDENT::12332', 'INCIDENT::12666', 'INCIDENT::132']
```

### IOGP-18: What equipment is involved in stored energy (pressure/tension) incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 725
Distinct EQUIPMENT values: 1024
Top 10:
  crane: 36
  ROV: 12
  winch: 11
  pump: 11
  compressor: 10
  actuator: 9
  HPU: 9
  reel: 8
  tubing hanger: 7
  needle valve: 6
```

### IOGP-19: How many pressurized system incidents mention zero energy verification?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 23
Sample: ['INCIDENT::14527', 'INCIDENT::24660', 'INCIDENT::26149', 'INCIDENT::545087', 'INCIDENT::548236']
```

### IOGP-20: What injuries result from compressed gas or pressure vessel incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 298
Distinct INJURY_TYPE values: 59
Top 10:
  injuries: 8
  laceration: 3
  Chemical burn: 3
  abrasion: 2
  pain: 2
  injury: 2
  cut: 2
  personal injury: 2
  blunt injury: 2
  personal injuries: 2
```

### IOGP-21: How many machinery/tool incidents involved entrapment or caught-between hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 775
Sample: ['INCIDENT::10206', 'INCIDENT::10299', 'INCIDENT::10379', 'INCIDENT::10502', 'INCIDENT::10632']
```

### IOGP-22: What body parts are most affected in grinder and power tool incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 312
Distinct BODY_PART values: 96
Top 10:
  left hand: 44
  finger: 32
  thumb: 25
  eye: 21
  left leg: 9
  Knee: 7
  wrist: 6
  forearm: 6
  arm: 5
  face: 4
```

### IOGP-23: How many electrical incidents mention arc flash or electrocution?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 88
Sample: ['INCIDENT::1272', 'INCIDENT::1273', 'INCIDENT::12861', 'INCIDENT::13871', 'INCIDENT::14244']
```

### IOGP-24: What equipment is involved in electrical incidents with LOTO failures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19
Distinct EQUIPMENT values: 37
Top 10:
  IRP: 1
  feeder terminal: 1
  feeder: 1
  pump: 1
  MTR2: 1
  MTR1: 1
  SIS: 1
  Breaker: 1
  circuit breaker: 1
  ROV UHD 58: 1
```

### IOGP-25: How many incidents involve projectiles or flying debris?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 29
Sample: ['INCIDENT::11280', 'INCIDENT::12640', 'INCIDENT::13462', 'INCIDENT::19569', 'INCIDENT::20399']
```

### IOGP-26: What are the top root causes of explosion or fire incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 322
Distinct EQUIPMENT values: 352
Top 10:
  fire extinguisher: 38
  fire blanket: 11
  welding machine: 8
  torch: 7
  welder: 7
  Gas hose: 7
  compressor: 5
  flashback arrestor: 5
  Train 1: 4
  extinguisher: 4
```

### IOGP-27: How many incidents mention extreme weather or natural events?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 903
Sample: ['INCIDENT::10173', 'INCIDENT::10178', 'INCIDENT::10232', 'INCIDENT::10239', 'INCIDENT::10240']
```

### IOGP-28: What are the year-over-year trends for vehicle incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Total incidents: 842
Months with data: 89
Yearly breakdown:
  2018: 113
  2019: 141
  2020: 156
  2021: 135
  2022: 50
  2023: 105
  2024: 90
  2025: 52
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
  actuator box -> static electric shock: 1
  gusset plate -> static electric shock: 1
  engine room water pump -> minor burn: 1
  induction heater -> minor burn: 1
  air hose -> personal injury: 1
  fitting -> personal injury: 1
  hose -> personal injury: 1
  needle gun -> finger contusion: 1
  needle gun -> nails: 1
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
    minor damage: 4

  crane (622 incidents):
    injuries: 18
    fracture: 5
    abrasion: 4
    personal injury: 4
    personal injuries: 3

  ROV (290 incidents):
    personal injury: 3
    ferimentos pessoais: 2
    bites: 1
    cut: 1
    spraining: 1

  pallet (186 incidents):
    injuries: 5
    injury: 3
    laceration: 3
    cut: 2
    fracture: 1

  PPE (145 incidents):
    cut: 5
    bruise: 3
    fracture: 3
    wounds: 3
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
  Amalapuram: 4
  Qidong: 4
  Panipat: 3
  Abu Dhabi: 3
  Pontal do Parana: 2
  Anvers: 2
```

### MH-08: Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents.
**Type:** Multi-hop | **Status:** ⚠️ | **Time:** 0.2s

```
Matching incidents: 1
Distinct INJURY_TYPE values: 0
Top 10:
```

### MH-09: What eye injuries result from grinder incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 16
Sample: ['INCIDENT::11564', 'INCIDENT::18679', 'INCIDENT::19308', 'INCIDENT::23430', 'INCIDENT::27724']
```

### MH-10: What injuries occur in ladder incidents at construction sites?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 77
Distinct INJURY_TYPE values: 26
Top 10:
  injuries: 4
  contusion: 3
  laceration: 3
  bruise: 2
  fracture: 2
  closed fracture: 2
  spraining of ligaments: 1
  Left foot instep bones fracture: 1
  strain: 1
  got injured: 1
```

### MH-11: What equipment is involved in finger or thumb injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1352
Distinct EQUIPMENT values: 1569
Top 10:
  gloves: 50
  hammer: 25
  PPE: 24
  crane: 23
  pallet: 21
  forklift: 19
  grinder: 17
  pipe: 15
  impact gloves: 12
  overhead crane: 10
```

### MH-12: Which countries have the most crane-related incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1444
Distinct LOCATION values: 59
Top 10:
  UK: 501
  USA: 242
  Norway: 80
  Brazil: 65
  Russia: 59
  India: 59
  Malaysia: 53
  China: 38
  Singapore: 27
  UAE: 25
```

### MH-13: What incidents involve forklifts with foot or leg injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 26
Sample: ['INCIDENT::11886', 'INCIDENT::15610', 'INCIDENT::18921', 'INCIDENT::19826', 'INCIDENT::22001']
```

### MH-14: What equipment is involved in fracture injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 228
Distinct EQUIPMENT values: 296
Top 10:
  PPE: 10
  crane: 8
  x-ray: 7
  forklift: 5
  crew bus: 4
  sling: 4
  x ray: 4
  ambulance: 4
  ladder: 4
  truck: 3
```

### MH-15: Which body parts are affected in hammer-related incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 146
Distinct BODY_PART values: 67
Top 10:
  left hand: 28
  finger: 25
  thumb: 10
  Knee: 5
  back: 3
  shoulder: 3
  left leg: 3
  eye: 3
  chest: 2
  nose: 2
```

### MH-16: What burn injuries are associated with welding operations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 16
Sample: ['INCIDENT::11142', 'INCIDENT::19154', 'INCIDENT::19275', 'INCIDENT::28887', 'INCIDENT::506937']
```

### MH-17: What incidents involve ROVs in Norway?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 26
Sample: ['INCIDENT::11670', 'INCIDENT::15585', 'INCIDENT::20327', 'INCIDENT::22841', 'INCIDENT::30042']
```

### MH-18: What crane incidents occurred in Brazil?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 71
Sample: ['INCIDENT::10169', 'INCIDENT::13338', 'INCIDENT::14031', 'INCIDENT::14429', 'INCIDENT::14694']
```

### MH-19: What forklift incidents occurred in the UK?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 102
Sample: ['INCIDENT::10170', 'INCIDENT::10333', 'INCIDENT::11665', 'INCIDENT::11848', 'INCIDENT::11875']
```

### MH-20: What scaffold incidents occurred in India?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 44
Sample: ['INCIDENT::501811', 'INCIDENT::502829', 'INCIDENT::503649', 'INCIDENT::505527', 'INCIDENT::507554']
```

### MH-21: What injury types result from high-severity crane incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 27
Distinct INJURY_TYPE values: 4
Top 10:
  injury: 1
  potential shoulder injury: 1
  involuntary movement: 1
  amputation: 1
```

### MH-22: What equipment is involved in incidents at Aberdeen?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2501
Distinct EQUIPMENT values: 3183
Top 10:
  crane: 171
  ROV: 164
  rigging: 34
  winch: 31
  PPE: 31
  SOPEP equipment: 28
  reel: 28
  ROV XLX94: 27
  kenz crane: 26
  umbilical: 21
```

### MH-23: What sling incidents involved hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 14
Sample: ['INCIDENT::508701', 'INCIDENT::512454', 'INCIDENT::513353', 'INCIDENT::513470', 'INCIDENT::571735']
```

### MH-24: What are the injury types from construction incidents resulting in fractures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 135
Sample: ['INCIDENT::13286', 'INCIDENT::14265', 'INCIDENT::14990', 'INCIDENT::16634', 'INCIDENT::19923']
```

### MH-25: What finger or thumb injuries involve fractures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 61
Sample: ['INCIDENT::12373', 'INCIDENT::13832', 'INCIDENT::14265', 'INCIDENT::14990', 'INCIDENT::16634']
```

### MH-26: What back injuries are associated with manual handling root causes?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 97
Sample: ['INCIDENT::10371', 'INCIDENT::10797', 'INCIDENT::11066', 'INCIDENT::12298', 'INCIDENT::14291']
```

### MH-27: What crane incidents occurred during 2019?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 166
Sample: ['INCIDENT::22601', 'INCIDENT::620267', 'INCIDENT::621368', 'INCIDENT::621392', 'INCIDENT::621599']
```

### MH-28: What forklift incidents occurred during 2023?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 99
Sample: ['INCIDENT::12422', 'INCIDENT::12495', 'INCIDENT::12535', 'INCIDENT::12642', 'INCIDENT::12794']
```

### MH-29: What scaffold incidents occurred during 2020?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 40
Sample: ['INCIDENT::666891', 'INCIDENT::667916', 'INCIDENT::669507', 'INCIDENT::671174', 'INCIDENT::672042']
```

### MH-30: What ROV incidents occurred during 2017?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 82
Sample: ['INCIDENT::521157', 'INCIDENT::522333', 'INCIDENT::524422', 'INCIDENT::526544', 'INCIDENT::526963']
```

### MH-31: What injuries result from fall/slip RCC incidents with fractures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 68
Sample: ['INCIDENT::19923', 'INCIDENT::20793', 'INCIDENT::27374', 'INCIDENT::503927', 'INCIDENT::505042']
```

### MH-32: What equipment is involved in incidents at Houston?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1361
Distinct EQUIPMENT values: 1244
Top 10:
  forklift: 110
  crane: 61
  pallet: 35
  ROV: 24
  overhead crane: 20
  forks: 19
  stand up forklift: 15
  tool: 14
  HPU: 13
  manlift: 12
```

### MH-33: What body parts are affected in incidents reported by YAMAL LNG?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1302
Distinct BODY_PART values: 302
Top 10:
  left hand: 169
  left foot: 64
  eye: 48
  ankle: 47
  left leg: 46
  shoulder: 30
  finger: 28
  arm: 25
  Knee: 23
  left ankle joint: 22
```

### MH-34: What injuries result from incidents at Rio de Janeiro?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 905
Distinct INJURY_TYPE values: 97
Top 10:
  cut: 24
  wounds: 22
  injuries: 19
  cutting: 12
  injury: 11
  surface cut: 7
  abrasion: 5
  minor damage: 5
  wounded: 3
  tropear: 3
```

### MH-35: What incidents involve grinders with hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 45
Sample: ['INCIDENT::10299', 'INCIDENT::10636', 'INCIDENT::13662', 'INCIDENT::15891', 'INCIDENT::16261']
```

### MH-36: What equipment is involved in incidents reported by PETROBRAS?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 676
Distinct EQUIPMENT values: 764
Top 10:
  ROV: 42
  crane: 25
  guindaste: 14
  ROV XLX94: 14
  XLX94: 8
  A&R: 7
  UEH: 5
  550Te crane: 5
  winch: 5
  XLX 93: 5
```

### MH-37: What are the top injury types in incidents at Le Trait?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1163
Distinct INJURY_TYPE values: 116
Top 10:
  pain: 55
  back pain: 12
  shock: 9
  No injury: 6
  cut: 6
  cutting: 5
  cervical pain: 3
  loss of balance: 3
  araladitis: 2
  tendinitis: 2
```

### MH-38: What equipment is involved in near-miss incidents at offshore locations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 141
Distinct EQUIPMENT values: 205
Top 10:
  crane: 13
  ROV: 10
  chain hoist: 5
  rigging: 5
  UEH: 4
  top drive: 3
  SOPEP equipment: 3
  reel: 3
  safety harness: 2
  Tensioner: 2
```

### MH-39: What are the root causes of incidents in Russia?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 962
Distinct ROOT_CAUSE_CATEGORY values: 43
Top 10:
  Falls, slips and trips on same level (without potential to fall to lower level): 272
  Manual handling: 78
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 60
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 60
  Hazard Identification & Risk Assessment: 55
  Traffic Management / Routes / Pedestrian path: 48
  Uncontrolled chemical or physical reaction: 44
  Stored energy (dropped objects): 42
  Inadequate Supervision: 34
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 28
```

### MH-40: What body parts are affected in excavator-related incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 201
Distinct BODY_PART values: 37
Top 10:
  ankle: 6
  left foot: 5
  left hand: 4
  left leg: 4
  Knee: 3
  arm: 3
  head: 2
  right-side window: 1
  rear passenger side: 1
  fourth finger: 1
```

### MH-41: What injury types result from incidents involving pallets?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 340
Distinct INJURY_TYPE values: 60
Top 10:
  injuries: 11
  cut: 8
  injury: 6
  laceration: 4
  contusion: 3
  sharp pain: 3
  minor damage: 2
  fracture: 2
  bruise: 2
  pain: 2
```

### MH-42: What injuries result from incidents involving pipes at offshore locations?
**Type:** Multi-hop | **Status:** ⚠️ | **Time:** 0.0s

```
Matching incidents: 8
Distinct INJURY_TYPE values: 2
Top 10:
  danos leves: 1
  muscle bruise: 1
```

### MH-43: What equipment is involved in red-risk incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 52
Distinct EQUIPMENT values: 81
Top 10:
  crane: 3
  forklift: 2
  Jack up drilling rig: 2
  XT controller: 1
  high-pressure hose: 1
  spill bucket: 1
  WBRT assembly: 1
  aux rotary: 1
  rig: 1
  assembly: 1
```

### MH-44: What are the root causes of incidents at Sabetta (Yamal LNG site)?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 880
Distinct ROOT_CAUSE_CATEGORY values: 41
Top 10:
  Falls, slips and trips on same level (without potential to fall to lower level): 264
  Manual handling: 77
  Hazard Identification & Risk Assessment: 54
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 54
  Traffic Management / Routes / Pedestrian path: 45
  Uncontrolled chemical or physical reaction: 42
  Stored energy (dropped objects): 39
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 39
  Inadequate Supervision: 31
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 27
```

### MH-45: What injury types are connected to crane equipment via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 568 EQUIPMENT nodes matching 'crane'
  --INVOLVED--> INCIDENT: 1444 nodes
  --RESULTED_IN--> INJURY_TYPE: 113 nodes
  Final: 113 INJURY_TYPE nodes, 113 distinct values

Top 10:
  muscular pain: 1
  fracture: 1
  crush injury: 1
  property damage: 1
  LTI injury: 1
  aggravation of previous injury: 1
  abrasion: 1
  Multiple open fractures: 1
  bone deformity: 1
  laceration: 1
```

### MH-46: What equipment is connected to fracture injuries via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 82 INJURY_TYPE nodes matching 'fracture'
  --RESULTED_IN--> INCIDENT: 228 nodes
  --INVOLVED--> EQUIPMENT: 296 nodes
  Final: 296 EQUIPMENT nodes, 296 distinct values

Top 10:
  pumpflex hose: 1
  scaffolding pipe: 1
  scaffolding plank: 1
  light 4x4 truck: 1
  wing lug: 1
  Allen wrench: 1
  pipeline support: 1
  electric cable: 1
  auto crane: 1
  outrigger pads: 1
```

### MH-47: What body parts are connected to forklift equipment via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 154 EQUIPMENT nodes matching 'forklift'
  --INVOLVED--> INCIDENT: 947 nodes
  --AFFECTED--> BODY_PART: 137 nodes
  Final: 137 BODY_PART nodes, 137 distinct values

Top 10:
  drain guard: 1
  tire: 1
  dormente: 1
  BUMPER: 1
  chest: 1
  two toes: 1
  knuckle: 1
  undercarriage: 1
  window: 1
  upper body: 1
```

### MH-48: What root causes are connected to hand injuries via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 117 BODY_PART nodes matching 'hand'
  --AFFECTED--> INCIDENT: 1133 nodes
  --CATEGORIZED_AS--> ROOT_CAUSE_CATEGORY: 46 nodes
  Final: 46 ROOT_CAUSE_CATEGORY nodes, 46 distinct values

Top 10:
  Psycho social - Workload (Overload/Underload): 1
  Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...): 1
  Difficult/Hindered operability of tools and equipment: 1
  Standard Operating Procedures, Procedures & Work instructions: 1
  Stored energy (dropped objects): 1
  Unprotected/unguarded moving machine parts (struck by/caught by ): 1
  Biological - Animals, Bacteria, Viruses and Funguses: 1
  Computer workplaces / Screens: 1
  Planning and coordination of works: 1
  Posture (constraint or restricted environment): 1
```

### MH-49: What locations have crane equipment via 2-hop graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 568 EQUIPMENT nodes matching 'crane'
  --INVOLVED--> INCIDENT: 1444 nodes
  --OCCURRED_AT--> LOCATION: 1495 nodes
  Final: 1495 LOCATION nodes, 1466 distinct values

Top 10:
  Singapore: 3
  Dubai: 2
  Malaysia: 2
  Le Trait: 2
  Lysaker: 2
  Tananger: 2
  Haugesund: 2
  India: 2
  Cyprus: 2
  Israel: 2
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

### SC-10: In incident #644762, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::644762: ['STB chute', 'crane', 'deck winch', 'main lift shackle', 'reel', 'tri-plate']
Ground truth: ['crane', 'deck winch', 'reel']
Missing: none
Extra (unexpected): ['main lift shackle', 'stb chute', 'tri-plate']
```

### SC-11: In incident #505133, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::505133: ['Billy Pugh personnel transfer basket', 'G1200 Helideck', 'helicopter', 'ladder', 'splint', 'stretcher']
Ground truth: ['helicopter', 'ladder', 'stretcher']
Missing: none
Extra (unexpected): ['billy pugh personnel transfer basket', 'g1200 helideck', 'splint']
```

### SC-12: In incident #645871, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::645871: ['arm', 'eye']
Ground truth: ['arm', 'eye']
Missing: none
Extra (unexpected): none
```

### SC-13: In incident #609327, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::609327: ['fracture', 'trauma']
Ground truth: ['fracture', 'trauma']
Missing: none
Extra (unexpected): none
```

### SC-14: In incident #569346, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::569346: ['Negative side string', 'Sideboom', 'Superior CPX-94', 'ladder']
Ground truth: ['ladder', 'sideboom']
Missing: none
Extra (unexpected): ['negative side string', 'superior cpx-94']
```

### SC-15: In incident #569346, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::569346: ['chin', 'jaw', 'lip', 'lower lip']
Ground truth: ['chin', 'jaw', 'lip']
Missing: none
Extra (unexpected): ['lower lip']
```

### SC-16: In incident #569346, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::569346: ['laceration', 'three broken teeth']
Ground truth: ['laceration', 'three broken teeth']
Missing: none
Extra (unexpected): none
```

### SC-17: In incident #685931, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::685931: ['bulker bags', 'ice compression pack', 'locking bar', 'safety helmet', 'splint and bandage', 'steel rack', 'waste rack lid']
Ground truth: ['bulker bags', 'locking bar', 'safety helmet', 'steel rack']
Missing: none
Extra (unexpected): ['ice compression pack', 'splint and bandage', 'waste rack lid']
```

### SC-18: In incident #632796, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::632796: ['HDA2006 224tn Hydraulic Jack', 'hydraulic hose', 'hydraulic jack', 'water guard']
Ground truth: ['hydraulic hose', 'hydraulic jack']
Missing: none
Extra (unexpected): ['hda2006 224tn hydraulic jack', 'water guard']
```

### SC-19: In incident #632796, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::632796: ['back', 'left', 'lower back', 'lower back area', 'lower left side of his back']
Ground truth: ['back', 'lower back']
Missing: none
Extra (unexpected): ['left', 'lower back area', 'lower left side of his back']
```

### SC-20: In incident #611828, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::611828: ['Sideboom', 'glasses', 'moving block part', 'safety helmet', 'sideboom_x000D_', 'sling', 'top hook block']
Ground truth: ['safety helmet', 'sideboom', 'sling']
Missing: none
Extra (unexpected): ['glasses', 'moving block part', 'sideboom_x000d_', 'top hook block']
```

### SC-21: In incident #563945, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::563945: ['davit', 'emergency lowering arm', 'ice pack', 'lifeboats']
Ground truth: ['davit', 'ice pack', 'lifeboats']
Missing: none
Extra (unexpected): ['emergency lowering arm']
```

### SC-22: In incident #564230, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::564230: ['bruising on the brain', 'contusion', 'dizziness', 'headache', 'nausea', 'neck pain', 'whiplash']
Ground truth: ['contusion', 'dizziness', 'headache', 'nausea']
Missing: none
Extra (unexpected): ['bruising on the brain', 'neck pain', 'whiplash']
```

### SC-23: In incident #696119, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::696119: ['Cerebral Hematoma', 'Crack left pelvis', 'Dislocate left shoulder', 'dislocate left shoulder_x000D_', 'hematoma']
Ground truth: ['cerebral hematoma', 'crack left pelvis', 'dislocate left shoulder']
Missing: none
Extra (unexpected): ['dislocate left shoulder_x000d_', 'hematoma']
```

### SC-24: In incident #560111, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::560111: ['Eyes injury', 'Left-eye cornea injury', 'Multiple facial graze-wound', 'Open right-eye cornea injury', 'Periorbital hematoma']
Ground truth: ['eyes injury', 'left-eye cornea injury', 'multiple facial graze-wound', 'open right-eye cornea injury', 'periorbital hematoma']
Missing: none
Extra (unexpected): none
```

### SC-25: In incident #702644, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::702644: ['breaks/fractures', 'bruising', 'skin abrasion', 'soft tissue damage']
Ground truth: ['breaks/fractures', 'bruising', 'skin abrasion', 'soft tissue damage']
Missing: none
Extra (unexpected): none
```

### SC-26: In incident #16468, what locations were recorded?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
LOCATION found for INCIDENT::16468: ['Aberdeen', 'Deep Orient', 'Duty Mess', 'Europe', 'Larnaca base', 'Limassol', 'Limassol base', 'Mediterranean hospital', 'Mez deck', 'UK', 'deck level', 'hospital', 'main deck', 'quayside']
Ground truth: ['aberdeen', 'deep orient', 'europe', 'uk']
Missing: none
Extra (unexpected): ['deck level', 'duty mess', 'hospital', 'larnaca base', 'limassol', 'limassol base', 'main deck', 'mediterranean hospital', 'mez deck', 'quayside']
```

### SC-27: In incident #546948, what locations were recorded?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
LOCATION found for INCIDENT::546948: ['4th floor', 'Doha', 'Doha Service Base', 'Middle East', 'PQ1-Q', 'PS1', 'PS1-A', 'PS1-C', 'PS1-G', 'PS1-Q', 'PS1G', 'PS1Q', 'Qatar']
Ground truth: ['doha', 'middle east', 'qatar']
Missing: none
Extra (unexpected): ['4th floor', 'doha service base', 'pq1-q', 'ps1', 'ps1-a', 'ps1-c', 'ps1-g', 'ps1-q', 'ps1g', 'ps1q']
```

### SC-28: In incident #555852, what organizations were recorded?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
ORGANIZATION found for INCIDENT::555852: ['Client', 'ERTL', 'KVA', 'Operasjonsleder Haugesund Police', 'Police Security Service', 'Project', 'Project management', 'Regional Police', 'STATOIL ASA', 'Stakeholders', 'TECHNIPFMC', 'TPFMC Control', 'TechnipFMC ERTL', 'TechnipFMC QHSE Management', 'TechnipFMC management', 'local police']
Ground truth: ['ertl', 'kva', 'project management', 'statoil asa', 'technipfmc']
Missing: none
Extra (unexpected): ['client', 'local police', 'operasjonsleder haugesund police', 'police security service', 'project', 'regional police', 'stakeholders', 'technipfmc ertl', 'technipfmc management', 'technipfmc qhse management', 'tpfmc control']
```

### SC-29: In incident #594002, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::594002: ['Punch tool', 'Stamping Punch Tool', 'V-Jaw tong']
Ground truth: ['punch tool', 'stamping punch tool', 'v-jaw tong']
Missing: none
Extra (unexpected): none
```

### SC-30: In incident #706581, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::706581: ['cut wound', 'femoral fracture', 'pulmonary contusion', 'rib fracture']
Ground truth: ['cut wound', 'femoral fracture', 'pulmonary contusion', 'rib fracture']
Missing: none
Extra (unexpected): none
```

### SC-31: In incident #563298, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::563298: ['light 4x4 truck', 'skid', 'truck platform']
Ground truth: ['light 4x4 truck', 'skid', 'truck platform']
Missing: none
Extra (unexpected): none
```

### SC-32: In incident #507347, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::507347: ['Dislocated R Knee', 'Dislocated knee cap', 'Knee', 'left leg']
Ground truth: ['knee', 'left leg']
Missing: none
Extra (unexpected): ['dislocated knee cap', 'dislocated r knee']
```

### SC-33: In incident #507347, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::507347: ['Full Leg Vacuum splint', 'ROV XLX94', 'Yokohama fenders', 'crutches']
Ground truth: ['crutches', 'rov xlx94', 'yokohama fenders']
Missing: none
Extra (unexpected): ['full leg vacuum splint']
```

### SC-34: In incident #19018, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::19018: ['CCTV', 'DVC', 'MCV-U', 'MVC', 'ROV', 'SDU', 'SDU-3', 'UEH', 'VCM', 'crane', 'u-VCM']
Ground truth: ['crane', 'mcv-u', 'mvc', 'rov', 'u-vcm']
Missing: none
Extra (unexpected): ['cctv', 'dvc', 'sdu', 'sdu-3', 'ueh', 'vcm']
```

### SC-35: In incident #664483, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::664483: ['confirmed fracture', 'dislocation']
Ground truth: ['confirmed fracture', 'dislocation']
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
  thumb: 9
  arm: 9
  eye: 8
  forearm: 7
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
  fracture: 4
  bruising: 4
  injury: 4
```

### SH-06: What incidents were reported by client SHELL OFFSHORE INC.?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 60
Sample: ['INCIDENT::100', 'INCIDENT::1039', 'INCIDENT::11906', 'INCIDENT::12463', 'INCIDENT::12507']
```

### SH-07: What incidents involved ladders?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 157
Sample: ['INCIDENT::10854', 'INCIDENT::12713', 'INCIDENT::12827', 'INCIDENT::13286', 'INCIDENT::13665']
```

### SH-08: What incidents involved grinders?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 175
Sample: ['INCIDENT::10021', 'INCIDENT::10299', 'INCIDENT::10318', 'INCIDENT::10636', 'INCIDENT::11470']
```

### SH-09: What incidents involved hoses?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 429
Sample: ['INCIDENT::10504', 'INCIDENT::10570', 'INCIDENT::10674', 'INCIDENT::10800', 'INCIDENT::10884']
```

### SH-10: What incidents involved pumps?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 314
Sample: ['INCIDENT::10234', 'INCIDENT::10375', 'INCIDENT::1073', 'INCIDENT::10923', 'INCIDENT::10963']
```

### SH-11: What incidents involved ROVs?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 562
Sample: ['INCIDENT::100', 'INCIDENT::1011', 'INCIDENT::10231', 'INCIDENT::103', 'INCIDENT::10369']
```

### SH-12: What incidents involved excavators?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 201
Sample: ['INCIDENT::12002', 'INCIDENT::1355', 'INCIDENT::16228', 'INCIDENT::16786', 'INCIDENT::18144']
```

### SH-13: What incidents involved PPE (helmets/gloves/safety glasses)?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 684
Sample: ['INCIDENT::10005', 'INCIDENT::10290', 'INCIDENT::10636', 'INCIDENT::10875', 'INCIDENT::11177']
```

### SH-14: What incidents involved slings?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 265
Sample: ['INCIDENT::10252', 'INCIDENT::10838', 'INCIDENT::11365', 'INCIDENT::11702', 'INCIDENT::13421']
```

### SH-15: What incidents involved compressors?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 209
Sample: ['INCIDENT::10171', 'INCIDENT::10504', 'INCIDENT::11948', 'INCIDENT::12064', 'INCIDENT::14536']
```

### SH-16: What incidents involved winches?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 278
Sample: ['INCIDENT::10428', 'INCIDENT::10541', 'INCIDENT::11392', 'INCIDENT::11394', 'INCIDENT::12334']
```

### SH-17: What body parts were affected in hose-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 429
Distinct BODY_PART values: 93
Top 10:
  eye: 12
  finger: 10
  left hand: 10
  face: 9
  ankle: 9
  wrist: 7
  shoulder: 6
  left leg: 6
  Knee: 5
  palm: 5
```

### SH-18: What injury types resulted from pump-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 314
Distinct INJURY_TYPE values: 29
Top 10:
  laceration: 2
  minor burn: 2
  injuries: 2
  contusion: 2
  personal injury: 2
  fracture: 2
  chafing: 2
  No injuries occurred: 1
  bites: 1
  personal injuries: 1
```

### SH-19: Which organizations reported excavator-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 201
Distinct ORGANIZATION values: 284
Top 10:
  TRANS ADRIATIC PIPELINE AG: 70
  PETRONAS: 17
  THE BAHRAIN PETROLEUM COMPANY BSC: 14
  SASOL NORTH AMERICA, INC.: 12
  JSC YAMAL LNG: 9
  SPIECAPAG: 8
  EXXONMOBIL: 8
  CPY: 7
  CTR: 7
  TAP: 7
```

### SH-20: What incidents involved welding equipment?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 261
Sample: ['INCIDENT::10172', 'INCIDENT::10206', 'INCIDENT::10598', 'INCIDENT::11142', 'INCIDENT::11528']
```

### SH-21: What incidents involved pallets?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 340
Sample: ['INCIDENT::10367', 'INCIDENT::10901', 'INCIDENT::11027', 'INCIDENT::11295', 'INCIDENT::11302']
```

### SH-22: What incidents involved fire extinguishers?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 148
Sample: ['INCIDENT::10176', 'INCIDENT::10248', 'INCIDENT::10504', 'INCIDENT::1067', 'INCIDENT::1068']
```

### SH-23: What incidents involved reels?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 241
Sample: ['INCIDENT::10173', 'INCIDENT::10980', 'INCIDENT::11665', 'INCIDENT::1184', 'INCIDENT::12094']
```

### SH-24: What incidents involved umbilicals?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 115
Sample: ['INCIDENT::10980', 'INCIDENT::11112', 'INCIDENT::11906', 'INCIDENT::12909', 'INCIDENT::12933']
```

### SH-25: What incidents affected the left hand?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1015
Sample: ['INCIDENT::10217', 'INCIDENT::10290', 'INCIDENT::10296', 'INCIDENT::10636', 'INCIDENT::10680']
```

### SH-26: What incidents affected the thumb?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 253
Sample: ['INCIDENT::10348', 'INCIDENT::10702', 'INCIDENT::10881', 'INCIDENT::10943', 'INCIDENT::110']
```

### SH-27: What incidents resulted in contusions or bruises?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 360
Sample: ['INCIDENT::1057', 'INCIDENT::10689', 'INCIDENT::10789', 'INCIDENT::11583', 'INCIDENT::1175']
```

### SH-28: What incidents resulted in sprains or strains?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 156
Sample: ['INCIDENT::12821', 'INCIDENT::12864', 'INCIDENT::13153', 'INCIDENT::13444', 'INCIDENT::13589']
```

### SH-29: How many incidents involve confined spaces?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 75
Sample: ['INCIDENT::12051', 'INCIDENT::21646', 'INCIDENT::26533', 'INCIDENT::501664', 'INCIDENT::501773']
```

### SH-30: How many incidents involve hot work?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 152
Sample: ['INCIDENT::10176', 'INCIDENT::12307', 'INCIDENT::12714', 'INCIDENT::12932', 'INCIDENT::13653']
```

### SH-31: How many incidents mention chemical exposure?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 177
Sample: ['INCIDENT::10636', 'INCIDENT::10667', 'INCIDENT::10907', 'INCIDENT::11542', 'INCIDENT::12010']
```

### SH-32: How many incidents involve electrical hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 891
Sample: ['INCIDENT::10019', 'INCIDENT::10064', 'INCIDENT::10174', 'INCIDENT::10248', 'INCIDENT::10504']
```

### SH-33: How many incidents mention gas leaks?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 42
Sample: ['INCIDENT::12333', 'INCIDENT::20401', 'INCIDENT::22645', 'INCIDENT::29190', 'INCIDENT::506046']
```

### SH-34: How many incidents describe man overboard situations?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 897
Sample: ['INCIDENT::10021', 'INCIDENT::10146', 'INCIDENT::103', 'INCIDENT::10355', 'INCIDENT::10503']
```

### SH-35: How many incidents mention fatigue as a factor?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 35
Sample: ['INCIDENT::10671', 'INCIDENT::12483', 'INCIDENT::12687', 'INCIDENT::21772', 'INCIDENT::28625']
```

### SH-36: How many incidents involve H2S or hydrogen sulfide?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 32
Sample: ['INCIDENT::10955', 'INCIDENT::20307', 'INCIDENT::21461', 'INCIDENT::21968', 'INCIDENT::22645']
```

### SH-37: How many incidents mention fire (not line of fire)?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 1500
Sample: ['INCIDENT::1003', 'INCIDENT::10171', 'INCIDENT::10172', 'INCIDENT::10176', 'INCIDENT::10239']
```

### SH-38: How many incidents mention pressure hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1260
Sample: ['INCIDENT::10064', 'INCIDENT::10174', 'INCIDENT::10322', 'INCIDENT::10323', 'INCIDENT::10345']
```

### SH-39: How many incidents reference permit-to-work procedures?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 398
Sample: ['INCIDENT::10619', 'INCIDENT::11235', 'INCIDENT::12465', 'INCIDENT::13403', 'INCIDENT::136']
```

### SH-40: How many incidents mention struck-by hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 86
Sample: ['INCIDENT::10378', 'INCIDENT::13653', 'INCIDENT::13681', 'INCIDENT::14102', 'INCIDENT::14507']
```

### SH-41: How many incidents describe caught-between or pinch-point hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 466
Sample: ['INCIDENT::10206', 'INCIDENT::10299', 'INCIDENT::10379', 'INCIDENT::10502', 'INCIDENT::10789']
```

### SH-42: How many incidents mention line-of-fire hazards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 461
Sample: ['INCIDENT::10172', 'INCIDENT::10239', 'INCIDENT::10240', 'INCIDENT::10245', 'INCIDENT::10272']
```

### SH-43: How many incidents mention scaffolding falls?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 398
Sample: ['INCIDENT::11913', 'INCIDENT::11986', 'INCIDENT::12070', 'INCIDENT::12307', 'INCIDENT::13298']
```

### SH-44: How many incidents reference JSA or toolbox talks?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 268
Sample: ['INCIDENT::10965', 'INCIDENT::12666', 'INCIDENT::1278', 'INCIDENT::13249', 'INCIDENT::13430']
```

### SH-45: What incidents involved helicopters?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 8
Sample: ['INCIDENT::15422', 'INCIDENT::19923', 'INCIDENT::505133', 'INCIDENT::533381', 'INCIDENT::581766']
```

### SH-46: What incidents were reported by PETROBRAS?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 676
Sample: ['INCIDENT::10019', 'INCIDENT::1011', 'INCIDENT::10146', 'INCIDENT::10223', 'INCIDENT::10228']
```

### SH-47: What incidents were reported by EQUINOR?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 401
Sample: ['INCIDENT::10016', 'INCIDENT::10021', 'INCIDENT::10887', 'INCIDENT::1089', 'INCIDENT::10891']
```

### SH-48: What incidents occurred at Sabetta?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 880
Sample: ['INCIDENT::500290', 'INCIDENT::500716', 'INCIDENT::500842', 'INCIDENT::501273', 'INCIDENT::501829']
```

### SH-49: What incidents occurred at Le Trait?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1163
Sample: ['INCIDENT::10141', 'INCIDENT::10178', 'INCIDENT::10185', 'INCIDENT::10225', 'INCIDENT::10281']
```

### SH-50: What incidents resulted in abrasions or scratches?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 223
Sample: ['INCIDENT::10333', 'INCIDENT::10345', 'INCIDENT::12341', 'INCIDENT::12430', 'INCIDENT::12591']
```

### SH-51: What incidents occurred in 2024?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.3s

```
Matching incidents: 1461
Sample: ['INCIDENT::16728', 'INCIDENT::18565', 'INCIDENT::18569', 'INCIDENT::18577', 'INCIDENT::18580']
```

### SH-52: What incidents have severity level 5 (most severe)?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 23
Sample: ['INCIDENT::10167', 'INCIDENT::10955', 'INCIDENT::11262', 'INCIDENT::13746', 'INCIDENT::1446']
```

### SH-53: What incidents are classified as occupational illness?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 160
Sample: ['INCIDENT::501107', 'INCIDENT::501163', 'INCIDENT::501933', 'INCIDENT::502122', 'INCIDENT::502678']
```

### SH-54: What incidents have red risk classification?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 52
Sample: ['INCIDENT::10166', 'INCIDENT::10167', 'INCIDENT::11126', 'INCIDENT::11221', 'INCIDENT::11246']
```

### SH-55: What incidents involved robots or drones?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 8
Sample: ['INCIDENT::17567', 'INCIDENT::29469', 'INCIDENT::29471', 'INCIDENT::29472', 'INCIDENT::571228']
```

### SH-56: What incidents occurred before 2016?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 0
```

### SH-57: What incidents occurred in Antarctica?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 0
```

### SH-58: What incidents involved tanks?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 67
Sample: ['INCIDENT::10820', 'INCIDENT::10821', 'INCIDENT::10992', 'INCIDENT::12756', 'INCIDENT::1450']
```

## 3. Failing Queries

- **MH-08** (Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents.): 1 incidents, 0 injury_type values
- **MH-42** (What injuries result from incidents involving pipes at offshore locations?): 8 incidents, 2 injury_type values, top: danos leves
- **SC-01** (In incident #623703, what equipment was involved?): 1 items: ['forklift']
- **SH-02** (What equipment was involved in incident #29857?): 3 items: ['ROV', 'lanyard', 'pry bar']

## 4. Regression Diff (vs previous run)

No regressions — all results stable.

---
*Generated by pipeline/benchmark/run_benchmark.py*