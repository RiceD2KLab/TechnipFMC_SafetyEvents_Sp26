# Benchmark Query Results

**Generated:** 2026-05-04
**Graph:** 111,115 nodes, 267,682 edges
**Records:** 19,820 metadata rows, 19,849 incident nodes
**Layer:** L1 + L2 (34,499 causal edges)

## 1. Summary Table

| ID | Query | Type | Status | Result |
|------|-------|------|:------:|--------|
| AG-01 | What are the most common root causes of dropped object incidents? | Aggregation | ✅ | 1026 incidents, 43 root_cause_category values, top: Stored energy (dropped objects) |
| AG-02 | Which countries have the highest rate of high-severity incidents? | Aggregation | ✅ | 167 incidents, 22 location values, top: USA |
| AG-03 | What equipment types are involved in the most incidents overall? | Aggregation | ✅ | 19849 incidents, 22286 equipment values, top: crane |
| AG-04 | How do incidents break down by type (accident vs. near miss) across business units? | Aggregation | ✅ | Crosstab: 4 business_unit values x 3 incident_type values |
| AG-05 | What is the monthly trend of fall/slip incidents over the past 3 years? | Aggregation | ✅ | 1695 incidents across 110 months |
| AG-06 | What proportion of incidents in each impact type category result in high-severity outcomes? | Aggregation | ✅ | Crosstab: 10 impact_type values x 6 severity_bin values |
| AG-07 | What are the most common body parts affected across all incidents? | Aggregation | ✅ | 19849 incidents, 1753 body_part values, top: finger |
| AG-08 | What are the most common injury types across all incidents? | Aggregation | ✅ | 19849 incidents, 1179 injury_type values, top: cut |
| AG-09 | Which organizations report the most incidents? | Aggregation | ✅ | 19849 incidents, 8830 organization values, top: TECHNIPFMC |
| AG-10 | What is the annual trend of manual handling incidents? | Aggregation | ✅ | 760 incidents across 108 months |
| AG-11 | What root cause categories are most common in high-severity incidents? | Aggregation | ✅ | 167 incidents, 22 root_cause_category values, top: Stored energy (dropped objects) |
| AG-12 | How do incidents break down by impact type over the years? | Aggregation | ✅ | Crosstab: 10 year values x 10 impact_type values |
| AG-13 | What is the trend of fire/explosion incidents over time? | Aggregation | ✅ | 121 incidents across 16 months |
| AG-14 | Which cities have the highest incident counts? | Aggregation | ✅ | 19849 incidents, 230 location values, top: Aberdeen |
| AG-15 | How do incidents distribute across work process categories? | Aggregation | ✅ | 19849 incidents, 65 root_cause_category values, top: Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) |
| AG-16 | What is the year-over-year trend of eye injuries? | Aggregation | ✅ | 500 incidents across 105 months |
| AG-17 | What are the most common injury types at construction sites? | Aggregation | ✅ | 5357 incidents, 556 injury_type values, top: contusion |
| AG-18 | Which clients report the most high-severity incidents? | Aggregation | ✅ | 167 incidents, 234 organization values, top: TECHNIPFMC |
| AG-19 | What is the year-over-year trend of fracture injuries? | Aggregation | ✅ | 352 incidents across 89 months |
| AG-20 | What equipment is most common in incidents at Aberdeen? | Aggregation | ✅ | 2499 incidents, 6828 equipment values, top: ROV |
| AG-21 | How do incidents break down by work process and risk color? | Aggregation | ✅ | Crosstab: 224 work_process values x 4 risk_color values |
| AG-22 | How do the top countries compare on accident vs near-miss ratios? | Aggregation | ✅ | Crosstab: 233 loc_country values x 3 incident_type values |
| AG-23 | How do root cause categories distribute across business units? | Aggregation | ✅ | Crosstab: 4 business_unit values x 118 case_categorization values |
| AG-24 | How does severity distribution vary by year? | Aggregation | ✅ | Crosstab: 10 year values x 6 severity_bin values |
| AG-25 | What is the year-over-year trend of contusion/bruise injuries? | Aggregation | ✅ | 510 incidents across 99 months |
| AG-26 | How do incident counts compare across the top 10 operating centers? | Aggregation | ✅ | Crosstab: 276 operating_center values x 3 incident_type values |
| CJ-01 | Which incidents match the pattern of corrosion-induced equipment failure leading to fire? | Conjunctive | ✅ | 34,499 causal edges; 800 for fire/explosion |
| CJ-02 | Find all high-severity incidents where a crane was involved AND a back injury was sustained AND the location was offshore. | Conjunctive | ✅ | 0 incidents |
| CJ-03 | Identify incidents where maintenance procedures failed, involving pipe equipment, resulting in environmental impact at locations in the Middle East. | Conjunctive | ✅ | 0 incidents |
| CJ-04 | Which equipment types have caused both injuries AND near-misses at the same location within the same year? | Conjunctive | ✅ | 1453 dual-risk equipment/location/year combos |
| CJ-05 | Find the causal chain pattern: procedural non-compliance -> dropped object -> head/hand injury. How many incidents match? | Conjunctive | ✅ | 451 incidents; 15 procedural causal edges |
| CJ-06 | Which incidents involve the co-occurrence of slip/fall events AND vehicle/transportation equipment at construction sites? | Conjunctive | ✅ | 29 incidents |
| CJ-07 | What are the primary effects of corrosion on equipment and incidents in the dataset? | Conjunctive | ✅ | 137 corrosion causal edges across 104 incidents |
| CJ-08 | Find crane incidents in the UK resulting in fractures. | Conjunctive | ✅ | 1 incidents |
| CJ-09 | Find forklift incidents at construction sites with severity >= 3. | Conjunctive | ✅ | 16 incidents |
| CJ-10 | Find vehicle road accident incidents resulting in injuries in the USA. | Conjunctive | ✅ | 26 incidents |
| CJ-11 | Find incidents involving PPE with eye injuries during manufacturing. | Conjunctive | ✅ | 31 incidents |
| CJ-12 | Find incidents involving chemical exposure resulting in environmental impact. | Conjunctive | ✅ | 69 incidents |
| CJ-13 | Find near-miss incidents involving scaffolding at height. | Conjunctive | ✅ | 148 incidents |
| CJ-14 | Find crane incidents in Houston during 2018. | Conjunctive | ✅ | 21 incidents |
| CJ-15 | Find stored-energy incidents with head injuries. | Conjunctive | ✅ | 37 incidents |
| CJ-16 | Find marine incidents involving ROVs with equipment failures. | Conjunctive | ✅ | 8 incidents |
| CJ-17 | Find vehicle road accidents at construction sites with injuries. | Conjunctive | ✅ | 33 incidents |
| CJ-18 | Find manual handling incidents with sprain/strain injuries. | Conjunctive | ✅ | 36 incidents |
| CJ-19 | Find stored-energy dropped-object incidents with lacerations. | Conjunctive | ✅ | 16 incidents |
| CJ-20 | Find near-miss incidents involving forklifts in 2023. | Conjunctive | ✅ | 63 incidents |
| CJ-21 | What safety controls successfully mitigated harm across all incidents? | Conjunctive | ✅ | 849 MITIGATED_BY edges, 675 distinct controls |
| CJ-22 | What barriers and controls failed most frequently across all incidents? | Conjunctive | ✅ | 828 FAILED_CONTROL edges, 737 distinct barriers |
| CJ-23 | What temporal sequences (event A preceded event B) are most common? | Conjunctive | ✅ | 508 PRECEDED_BY edges, 507 distinct sequences |
| CJ-24 | What are the top causal factors leading to dropped-object incidents? | Conjunctive | ✅ | 5,311 causal edges for 3,145 dropped-object incidents |
| CJ-25 | What are the top causal factors in vehicle-related incidents? | Conjunctive | ✅ | 1,663 causal edges for 1,205 vehicle incidents |
| CJ-26 | What causal chains lead to fracture injuries? | Conjunctive | ✅ | 746 causal edges for 352 fracture incidents |
| CJ-27 | Find crane incidents in Norway resulting in injuries. | Conjunctive | ✅ | 68 incidents |
| CJ-28 | Find incidents with both equipment failure and manual handling root causes. | Conjunctive | ✅ | 0 incidents |
| CJ-29 | Find high-severity incidents at construction sites involving scaffolding. | Conjunctive | ✅ | 7 incidents |
| CJ-30 | Find incidents involving hoses with environmental impact at offshore locations. | Conjunctive | ✅ | 25 incidents |
| CJ-31 | Find severity 5 incidents involving cranes with injury impact. | Conjunctive | ✅ | 3 incidents |
| CJ-32 | What causal chains lead from equipment failures to injuries (L2 traversal)? | Conjunctive | ✅ | 160 endpoints, 160 distinct INJURY_TYPE |
| CJ-33 | What events are caused by corrosion conditions (L2 traversal)? | Conjunctive | ✅ | 17 endpoints, 17 distinct EVENT |
| CJ-34 | What injuries result from failed controls (L2 traversal)? | Conjunctive | ✅ | 23 endpoints, 23 distinct INJURY_TYPE |
| GL-01 | What are the most significant safety risk clusters across TechnipFMC global operations? | Global | ✅ | 11149 communities detected |
| GL-02 | Are there systemic patterns where the same type of equipment failure recurs across different geographic regions? | Global | ✅ | 266 equipment types span 5+ regions |
| GL-03 | How has the overall safety incident profile changed over the dataset time range? Are certain incident types increasing or decreasing? | Global | ✅ | Crosstab: 10 year values x 3 incident_type values |
| GL-04 | What entities serve as the most connected hubs in the knowledge graph, and what does their centrality reveal about systemic risk? | Global | ✅ | Hub analysis: degree + PageRank top 20 |
| GL-05 | What are the most common equipment-body part co-occurrences across all incidents? | Global | ✅ | 26250 equipment–body part pairs |
| GL-06 | How do safety profiles compare across the top 5 clients by incident volume? | Global | ✅ | Safety profiles for top 5 clients |
| GL-07 | Are there seasonal (monthly) patterns in incident frequency? | Global | ✅ | Peaks: none; Troughs: none |
| GL-08 | What are the top root causes by geographic region? | Global | ✅ | RCC breakdown for 7 regions |
| GL-09 | How many incidents mention burns in narrative but have no burn injury type extracted? | Global | ✅ | 51 / 177 (29%) missing INJURY_TYPE |
| GL-10 | How many incidents mention fractures in narrative but have no fracture injury type extracted? | Global | ✅ | 90 / 442 (20%) missing INJURY_TYPE |
| GL-11 | How many incidents mention cranes in narrative but have no crane equipment extracted? | Global | ✅ | 4 / 1,877 (0%) missing EQUIPMENT |
| GL-12 | How many incidents mention forklifts in narrative but have no forklift equipment extracted? | Global | ✅ | 5 / 1,075 (0%) missing EQUIPMENT |
| GL-13 | How many high-severity incidents (>=4) have no injury type extracted? | Global | ✅ | 140 / 167 (84%) high-severity missing INJURY_TYPE |
| GL-14 | How many injury-impact incidents have no body part extracted? | Global | ✅ | 5,533 / 11,736 (47%) injury incidents missing BODY_PART |
| GL-15 | How many incidents have very short narratives (<100 chars) with no entities extracted? | Global | ✅ | 301 short-narrative incidents with 0 entity extraction (5 test records) |
| GL-16 | How many incidents contain non-English narratives with reduced entity extraction? | Global | ✅ | 5,435 non-English incidents, 147 with zero entity extraction |
| GL-17 | Find the 10 incidents most similar to incident #29857 (dropped pry bar) using hybrid embedding similarity. | Global | ✅ | Top 10 similar to #29857, 100% equipment overlap |
| GL-18 | Find the 10 incidents most similar to incident #569346 (ladder fall with broken teeth) using hybrid embedding similarity. | Global | ✅ | Top 10 similar to #569346, 60% equipment overlap |
| GL-19 | Do the top-10 text-similar incidents for a forklift accident share the same equipment type? (structural hit rate) | Global | ✅ | 100% hit rate for forklift|flt retrieval |
| GL-20 | Do the top-10 text-similar incidents for a crane near-miss share the same equipment type? (structural hit rate) | Global | ✅ | 30% hit rate for crane retrieval |
| GL-21 | How well do text embeddings and structural similarity agree on the top-10 most similar incidents? (method correlation) | Global | ✅ | Text vs Node2Vec mean overlap: 4.0% |
| GL-22 | Find incidents semantically similar to 'worker fell from scaffold due to missing guardrail' using text embeddings. | Global | ✅ | Top match: #531820 (sim=0.709) |
| GL-23 | Find incidents semantically similar to 'crane load dropped because sling failed under tension' using text embeddings. | Global | ✅ | Top match: #430 (sim=0.676) |
| GL-24 | Which equipment types appear most often in the top-10 similar incidents for high-severity events? (embedding-based pattern) | Global | ✅ | Top equipment in high-sev neighborhoods: [('crane', 59), ('rigging', 41), ('another forklift', 38)] |
| IOGP-01 | What injuries result from incidents involving moving vehicles and mobile equipment? | Aggregation | ✅ | 2857 incidents, 198 injury_type values, top: pain |
| IOGP-02 | How do dropped object incidents break down by severity over time? | Aggregation | ✅ | Crosstab: 6 severity_bin values x 10 year values |
| IOGP-03 | How many incidents involve stored energy or snap-back hazards? | Single-hop | ✅ | 114 incidents |
| IOGP-04 | How many pressurized system incidents resulted in containment loss? | Multi-hop | ✅ | 675 incidents |
| IOGP-05 | Which electrical incidents had lockout/tagout failures? | Conjunctive | ✅ | 142 incidents; 9 FAILED_CONTROL edges |
| IOGP-06 | What body parts are affected in working-at-height incidents with fall protection gaps? | Multi-hop | ✅ | 560 incidents, 145 body_part values, top: hand |
| IOGP-07 | What injuries result from mechanical lifting incidents with rigging failures? | Multi-hop | ✅ | 2872 incidents, 224 injury_type values, top: personal injury |
| IOGP-08 | How many machinery and tool incidents resulted in hand or finger injuries? | Multi-hop | ✅ | 278 incidents |
| IOGP-09 | What are the top injury types from moving vehicle and mobile equipment incidents? | Aggregation | ✅ | 2857 incidents, 198 injury_type values, top: pain |
| IOGP-10 | How many vehicle incidents resulted in high-severity outcomes? | Multi-hop | ✅ | 33 incidents |
| IOGP-11 | What body parts are most affected in vehicle/mobile equipment incidents? | Aggregation | ✅ | 842 incidents, 82 body_part values, top: driver side |
| IOGP-12 | Which countries have the most mechanical lifting/hoisting incidents? | Aggregation | ✅ | 2872 incidents, 49 location values, top: UK |
| IOGP-13 | What are the top root causes of mechanical lifting incidents? | Aggregation | ✅ | 2872 incidents, 52 root_cause_category values, top: Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects) |
| IOGP-14 | How many working-at-height incidents involved harnesses or lanyards? | Single-hop | ✅ | 196 incidents |
| IOGP-15 | What injury types result from fall-to-lower-level incidents? | Aggregation | ✅ | 1695 incidents, 330 injury_type values, top: pain |
| IOGP-16 | How do dropped object incidents break down by body part affected? | Aggregation | ✅ | 1160 incidents, 147 body_part values, top: hand |
| IOGP-17 | How many tensioned line or snap-back incidents occurred? | Single-hop | ✅ | 109 incidents |
| IOGP-18 | What equipment is involved in stored energy (pressure/tension) incidents? | Aggregation | ✅ | 725 incidents, 1950 equipment values, top: hose |
| IOGP-19 | How many pressurized system incidents mention zero energy verification? | Multi-hop | ✅ | 23 incidents |
| IOGP-20 | What injuries result from compressed gas or pressure vessel incidents? | Multi-hop | ✅ | 559 incidents, 100 injury_type values, top: contusion |
| IOGP-21 | How many machinery/tool incidents involved entrapment or caught-between hazards? | Single-hop | ✅ | 775 incidents |
| IOGP-22 | What body parts are most affected in grinder and power tool incidents? | Multi-hop | ✅ | 471 incidents, 157 body_part values, top: left hand |
| IOGP-23 | How many electrical incidents mention arc flash or electrocution? | Single-hop | ✅ | 88 incidents |
| IOGP-24 | What equipment is involved in electrical incidents with LOTO failures? | Multi-hop | ✅ | 19 incidents, 84 equipment values, top: LOTO |
| IOGP-25 | How many incidents involve projectiles or flying debris? | Single-hop | ✅ | 29 incidents |
| IOGP-26 | What are the top root causes of explosion or fire incidents? | Aggregation | ✅ | 322 incidents, 677 equipment values, top: fire extinguisher |
| IOGP-27 | How many incidents mention extreme weather or natural events? | Single-hop | ✅ | 903 incidents |
| IOGP-28 | What are the year-over-year trends for vehicle incidents? | Aggregation | ✅ | 842 incidents across 89 months |
| MH-01 | Find all equipment types involved in containment loss events leading to injuries at offshore locations. | Multi-hop | ✅ | 3 incidents, 20 equipment types |
| MH-02 | What injury types are associated with equipment failures during maintenance operations? | Multi-hop | ✅ | 29 incidents, 92 pairs |
| MH-03 | Which clients have experienced vessel-related incidents resulting in back injuries? | Multi-hop | ✅ | 62 incidents, 111 organization values, top: PETROBRAS |
| MH-04 | What are the most common injury types for each of the top 5 equipment categories? | Multi-hop | ✅ | Injury breakdown for top 5 equipment |
| MH-05 | Find incidents where hand injuries occurred during work involving pipes at locations in Asia Pacific. | Multi-hop | ✅ | 21 incidents |
| MH-06 | What is the severity distribution of incidents involving trucks compared to those involving cranes? | Multi-hop | ✅ | Truck vs crane severity comparison |
| MH-07 | Which locations have the highest concentration of near-miss incidents involving scaffolding? | Multi-hop | ✅ | 302 incidents, 46 location values, top: Sabetta |
| MH-08 | Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents. | Multi-hop | ✅ | 1 incidents, 2 injury_type+injury+event values, top: oil spray |
| MH-09 | What eye injuries result from grinder incidents? | Multi-hop | ✅ | 20 incidents |
| MH-10 | What injuries occur in ladder incidents at construction sites? | Multi-hop | ✅ | 145 incidents, 44 injury_type values, top: fracture |
| MH-11 | What equipment is involved in finger or thumb injuries? | Multi-hop | ✅ | 1455 incidents, 2475 equipment values, top: PPE |
| MH-12 | Which countries have the most crane-related incidents? | Multi-hop | ✅ | 1891 incidents, 47 location values, top: UK |
| MH-13 | What incidents involve forklifts with foot or leg injuries? | Multi-hop | ✅ | 29 incidents |
| MH-14 | What equipment is involved in fracture injuries? | Multi-hop | ✅ | 352 incidents, 748 equipment values, top: x-raying |
| MH-15 | Which body parts are affected in hammer-related incidents? | Multi-hop | ✅ | 221 incidents, 111 body_part values, top: finger |
| MH-16 | What burn injuries are associated with welding operations? | Multi-hop | ✅ | 23 incidents |
| MH-17 | What incidents involve ROVs in Norway? | Multi-hop | ✅ | 32 incidents |
| MH-18 | What crane incidents occurred in Brazil? | Multi-hop | ✅ | 95 incidents |
| MH-19 | What forklift incidents occurred in the UK? | Multi-hop | ✅ | 145 incidents |
| MH-20 | What scaffold incidents occurred in India? | Multi-hop | ✅ | 74 incidents |
| MH-21 | What injury types result from high-severity crane incidents? | Multi-hop | ✅ | 32 incidents, 4 injury_type values, top: potential shoulder injury |
| MH-22 | What equipment is involved in incidents at Aberdeen? | Multi-hop | ✅ | 2499 incidents, 6828 equipment values, top: ROV |
| MH-23 | What sling incidents involved hand or finger injuries? | Multi-hop | ✅ | 37 incidents |
| MH-24 | What are the injury types from construction incidents resulting in fractures? | Multi-hop | ✅ | 218 incidents |
| MH-25 | What finger or thumb injuries involve fractures? | Multi-hop | ✅ | 114 incidents |
| MH-26 | What back injuries are associated with manual handling root causes? | Multi-hop | ✅ | 96 incidents |
| MH-27 | What crane incidents occurred during 2019? | Multi-hop | ✅ | 208 incidents |
| MH-28 | What forklift incidents occurred during 2023? | Multi-hop | ✅ | 119 incidents |
| MH-29 | What scaffold incidents occurred during 2020? | Multi-hop | ✅ | 78 incidents |
| MH-30 | What ROV incidents occurred during 2017? | Multi-hop | ✅ | 126 incidents |
| MH-31 | What injuries result from fall/slip RCC incidents with fractures? | Multi-hop | ✅ | 110 incidents |
| MH-32 | What equipment is involved in incidents at Houston? | Multi-hop | ✅ | 1358 incidents, 1827 equipment values, top: another forklift |
| MH-33 | What body parts are affected in incidents reported by YAMAL LNG? | Multi-hop | ✅ | 1302 incidents, 304 body_part values, top: right hand |
| MH-34 | What injuries result from incidents at Rio de Janeiro? | Multi-hop | ✅ | 897 incidents, 82 injury_type values, top: cut |
| MH-35 | What incidents involve grinders with hand or finger injuries? | Multi-hop | ✅ | 63 incidents |
| MH-36 | What equipment is involved in incidents reported by PETROBRAS? | Multi-hop | ✅ | 676 incidents, 1420 equipment values, top: ROV |
| MH-37 | What are the top injury types in incidents at Le Trait? | Multi-hop | ✅ | 1135 incidents, 79 injury_type values, top: pain |
| MH-38 | What equipment is involved in near-miss incidents at offshore locations? | Multi-hop | ✅ | 141 incidents, 478 equipment values, top: rigging |
| MH-39 | What are the root causes of incidents in Russia? | Multi-hop | ✅ | 962 incidents, 43 root_cause_category values, top: Falls, slips and trips on same level (without potential to fall to lower level) |
| MH-40 | What body parts are affected in excavator-related incidents? | Multi-hop | ✅ | 209 incidents, 52 body_part values, top: left leg |
| MH-41 | What injury types result from incidents involving pallets? | Multi-hop | ✅ | 579 incidents, 80 injury_type values, top: pain |
| MH-42 | What injuries result from incidents involving pipes at offshore locations? | Multi-hop | ✅ | 19 incidents, 7 injury_type values, top: pain |
| MH-43 | What equipment is involved in red-risk incidents? | Multi-hop | ✅ | 52 incidents, 174 equipment values, top: flange |
| MH-44 | What are the root causes of incidents at Sabetta (Yamal LNG site)? | Multi-hop | ✅ | 880 incidents, 41 root_cause_category values, top: Falls, slips and trips on same level (without potential to fall to lower level) |
| MH-45 | What injury types are connected to crane equipment via graph traversal? | Multi-hop | ✅ | 141 endpoints, 141 distinct INJURY_TYPE |
| MH-46 | What equipment is connected to fracture injuries via graph traversal? | Multi-hop | ✅ | 748 endpoints, 748 distinct EQUIPMENT |
| MH-47 | What body parts are connected to forklift equipment via graph traversal? | Multi-hop | ✅ | 109 endpoints, 109 distinct BODY_PART |
| MH-48 | What root causes are connected to hand injuries via graph traversal? | Multi-hop | ✅ | 50 endpoints, 50 distinct ROOT_CAUSE_CATEGORY |
| MH-49 | What locations have crane equipment via 2-hop graph traversal? | Multi-hop | ✅ | 2039 endpoints, 1987 distinct LOCATION |
| SC-01 | In incident #623703, what equipment was involved? | Single-hop | ✅ | 3 items: ['another forklift', 'manifold', 'mirror'] |
| SC-02 | In incident #570187, what equipment was involved? | Single-hop | ✅ | 4 items: ['Connector link', 'EPMCC panel', 'electric heater feeder breaker', 'within feeder box'] |
| SC-03 | In incident #602346, what equipment was involved? | Single-hop | ✅ | 2 items: ['PGB', 'another forklift'] |
| SC-04 | In incident #14338, what equipment was involved? | Single-hop | ✅ | 3 items: ['large mold', 'mold', 'press'] |
| SC-04b | In incident #14338, which body parts were affected? | Single-hop | ✅ | 1 items: ['lower back'] |
| SC-05 | In incident #500389, what equipment was involved? | Single-hop | ✅ | 8 items: ['ROV', 'TMS’s', 'football float', 'marker buoys', 'odom weight', 'odom weight with chain', 'polyrope', 'vessel'] |
| SC-06 | In incident #8712, what equipment was involved? | Single-hop | ✅ | 1 items: ['barrier'] |
| SC-06b | In incident #8712, which body parts were affected? | Single-hop | ✅ | 3 items: ['face', 'forehead', 'head'] |
| SC-07 | In incident #511771, what equipment was involved? | Single-hop | ✅ | 3 items: ['The Main Crane Hook', 'helmet', 'wire rope sling'] |
| SC-07b | In incident #511771, which body parts were affected? | Single-hop | ✅ | 1 items: ['lower lip'] |
| SC-08 | In incident #324, what equipment was involved? | Single-hop | ✅ | 2 items: ['20T Forklift', 'another forklift'] |
| SC-09 | In incident #18312, what equipment was involved? | Single-hop | ✅ | 1 items: ['crane'] |
| SC-09b | In incident #18312, which body parts were affected? | Single-hop | ✅ | 2 items: ['head', 'top of his head'] |
| SC-10 | In incident #644762, what equipment was involved? | Single-hop | ✅ | 10 items: ['19 reels', 'Helicopter', 'PPE', 'ancillary pipelay equipment', 'crane', 'deck winch', 'his steel toe cap boots', 'main lift shackle', 'rigging', 'tri-plate'] |
| SC-11 | In incident #505133, what equipment was involved? | Single-hop | ✅ | 13 items: ['Billy Pugh', 'Deck F', 'G1200', 'G1200 AB', 'Helicopter', 'Surfer Landing Platform', 'Surfer S 226', 'engine', 'ladder', 'platform', 'rope', 'splint', 'stretcher'] |
| SC-12 | In incident #645871, what body parts were affected? | Single-hop | ✅ | 3 items: ['arm', 'back', 'eye'] |
| SC-13 | In incident #609327, what injury types resulted? | Single-hop | ✅ | 2 items: ['fracture', 'trauma'] |
| SC-14 | In incident #569346, what equipment was involved? | Single-hop | ✅ | 6 items: ['Load. Moment Indicator', 'Superior CPX-94', 'boom block wire rope', 'cable', 'ladder', 'sideboom'] |
| SC-15 | In incident #569346, what body parts were affected? | Single-hop | ✅ | 5 items: ['chin', 'jaw', 'knee', 'lip', 'lower lip'] |
| SC-16 | In incident #569346, what injury types resulted? | Single-hop | ✅ | 1 items: ['laceration'] |
| SC-17 | In incident #685931, what equipment was involved? | Single-hop | ✅ | 12 items: ['A steel Rack', 'The waste rack lid', 'bulker bags', 'ice compression pack', 'impact protection gloves', 'lid', 'locking bar', 'new bulker bag', 'safety helmet', 'securing arm', 'splint and bandage', 'steel lid'] |
| SC-18 | In incident #632796, what equipment was involved? | Single-hop | ✅ | 8 items: ['AQA Wellhead platform', 'Deck Workshop', 'HDA2006 224tn Hydraulic Jack', 'crew boat', 'hose', 'hydraulic jack', 'telephone', 'water guard'] |
| SC-19 | In incident #632796, what body parts were affected? | Single-hop | ✅ | 3 items: ['back', 'lower back area', 'lower side'] |
| SC-20 | In incident #611828, what equipment was involved? | Single-hop | ✅ | 10 items: ['EN388', 'PPE', 'block', 'glasses', 'rigging', 'safety helmet', 'sheeve', 'sideboom', 'slinger', 'the moving block part'] |
| SC-21 | In incident #563945, what equipment was involved? | Single-hop | ✅ | 10 items: ['Ice pack', 'PWT', 'davit', 'emergency lowering arm', 'harness', 'main deck', 'platform', 'vessel hospital', 'vessel lifeboats', 'welding workshop'] |
| SC-22 | In incident #564230, what injury types resulted? | Single-hop | ✅ | 6 items: ['bruising on the brain', 'contusion', 'headache', 'nausea', 'neck pain', 'whiplash'] |
| SC-23 | In incident #696119, what injury types resulted? | Single-hop | ✅ | 3 items: ['Cerebral Hematoma', 'Right eye wound', 'hematoma'] |
| SC-24 | In incident #560111, what injury types resulted? | Single-hop | ✅ | 5 items: ['Eyes injury', 'Left-eye cornea injury', 'Multiple facial graze-wound', 'Open right-eye cornea injury', 'Periorbital hematoma'] |
| SC-25 | In incident #702644, what injury types resulted? | Single-hop | ✅ | 4 items: ['bruising', 'fracture', 'superficial skin abrasion', 'swelling'] |
| SC-26 | In incident #16468, what locations were recorded? | Single-hop | ✅ | 18 items: ['1st level platforms', 'Aberdeen', 'Bridge', 'DEEP ORIENT', 'De -watering spread', 'Deep Orient', 'Duty Mess', 'Europe', 'Karish North', 'Larnaca base', 'Limassol', 'Limassol base', 'Mediterranean hospital', 'North Quay', 'UK', 'mess room', 'quayside', 'work site'] |
| SC-27 | In incident #546948, what locations were recorded? | Single-hop | ✅ | 15 items: ['Doha', 'Doha Service Base', 'Middle East', 'PQ1-Q accommodation', 'PS1-A', 'PS1-C', 'PS1-G', 'PS1-G control room', 'PS1-Q', 'PS1G', 'PS1Q', 'Qatar', 'accommodation', 'control room', 'medical facilities'] |
| SC-28 | In incident #555852, what organizations were recorded? | Single-hop | ✅ | 16 items: ['Communications and project', 'ERTL', 'KVA', 'Operasjonsleder Haugesund Police', 'Police Security Service (PST)', 'Project management', 'QHSE Management', 'Regional Police', 'STATOIL ASA', 'Stakeholders', 'TECHNIPFMC', 'TPFMC Control', 'TechnipFMC ERTL', 'TechnipFMC Management', 'TechnipFMC Norway', 'local police'] |
| SC-29 | In incident #594002, what equipment was involved? | Single-hop | ✅ | 3 items: ['Punch tool', 'Stamping Punch Tool', 'V-Jaw tong'] |
| SC-30 | In incident #706581, what injury types resulted? | Single-hop | ✅ | 4 items: ['cut wound', 'femoral fracture', 'pulmonary contusion', 'rib fracture'] |
| SC-31 | In incident #563298, what equipment was involved? | Single-hop | ✅ | 9 items: ['PPE', 'Steri strips', 'Truck', 'bandage', 'light 4x4 truck', 'rigging', 'skid', 'truck platform', 'x-raying'] |
| SC-32 | In incident #507347, what body parts were affected? | Single-hop | ✅ | 3 items: ['knee', 'leg', 'right knee'] |
| SC-33 | In incident #507347, what equipment was involved? | Single-hop | ✅ | 14 items: ['Full Leg Vacuum splint', 'Hi level flood lighting', 'ROV', 'ROV XLX 85 & TMS', 'ROV XLX94', 'ROV hanger', 'TMS’s', 'Yokohama type fenders', 'bollard', 'crutches', 'medical ambulance', 'pallet', 'rigging', 'vessel'] |
| SC-34 | In incident #19018, what equipment was involved? | Single-hop | ✅ | 14 items: ['CCTV', 'HUB', 'MCV', 'MCV-U', 'ROV', 'Spare SA blind stab', 'Umbilical 9F UEH SDU-3', 'VCM', 'camera', 'crane', 'slinger', 'u-VCM', 'umbilical', 'wet Christmas tree'] |
| SC-35 | In incident #664483, what injury types resulted? | Single-hop | ✅ | 3 items: ['dislocated', 'dislocation and fracture', 'fracture'] |
| SH-01 | What incidents involved forklifts in 2022? | Single-hop | ✅ | 85 incidents |
| SH-02 | What equipment was involved in incident #29857? | Single-hop | ✅ | 4 items: ['Pry Bar', 'ROV', 'TMS’s', 'lanyard'] |
| SH-03 | What body parts were affected in crane-related incidents? | Single-hop | ✅ | 1891 incidents, 255 body_part values, top: finger |
| SH-04 | Which locations reported valve-related incidents? | Single-hop | ✅ | 1149 incidents, 45 location values, top: USA |
| SH-05 | What types of injuries resulted from incidents at offshore installations? | Single-hop | ✅ | 1120 incidents, 175 injury_type values, top: personal injury |
| SH-06 | What incidents were reported by client SHELL OFFSHORE INC.? | Single-hop | ✅ | 60 incidents |
| SH-07 | What incidents involved ladders? | Single-hop | ✅ | 306 incidents |
| SH-08 | What incidents involved grinders? | Single-hop | ✅ | 233 incidents |
| SH-09 | What incidents involved hoses? | Single-hop | ✅ | 1122 incidents |
| SH-10 | What incidents involved pumps? | Single-hop | ✅ | 418 incidents |
| SH-11 | What incidents involved ROVs? | Single-hop | ✅ | 849 incidents |
| SH-12 | What incidents involved excavators? | Single-hop | ✅ | 209 incidents |
| SH-13 | What incidents involved PPE (helmets/gloves/safety glasses)? | Single-hop | ✅ | 1148 incidents |
| SH-14 | What incidents involved slings? | Single-hop | ✅ | 555 incidents |
| SH-15 | What incidents involved compressors? | Single-hop | ✅ | 379 incidents |
| SH-16 | What incidents involved winches? | Single-hop | ✅ | 415 incidents |
| SH-17 | What body parts were affected in hose-related incidents? | Single-hop | ✅ | 1122 incidents, 166 body_part values, top: face |
| SH-18 | What injury types resulted from pump-related incidents? | Single-hop | ✅ | 418 incidents, 42 injury_type values, top: cut |
| SH-19 | Which organizations reported excavator-related incidents? | Single-hop | ✅ | 209 incidents, 308 organization values, top: TRANS ADRIATIC PIPELINE AG |
| SH-20 | What incidents involved welding equipment? | Single-hop | ✅ | 339 incidents |
| SH-21 | What incidents involved pallets? | Single-hop | ✅ | 579 incidents |
| SH-22 | What incidents involved fire extinguishers? | Single-hop | ✅ | 243 incidents |
| SH-23 | What incidents involved reels? | Single-hop | ✅ | 435 incidents |
| SH-24 | What incidents involved umbilicals? | Single-hop | ✅ | 177 incidents |
| SH-25 | What incidents affected the left hand? | Single-hop | ✅ | 503 incidents |
| SH-26 | What incidents affected the thumb? | Single-hop | ✅ | 273 incidents |
| SH-27 | What incidents resulted in contusions or bruises? | Single-hop | ✅ | 510 incidents |
| SH-28 | What incidents resulted in sprains or strains? | Single-hop | ✅ | 212 incidents |
| SH-29 | How many incidents involve confined spaces? | Single-hop | ✅ | 75 incidents |
| SH-30 | How many incidents involve hot work? | Single-hop | ✅ | 152 incidents |
| SH-31 | How many incidents mention chemical exposure? | Single-hop | ✅ | 177 incidents |
| SH-32 | How many incidents involve electrical hazards? | Single-hop | ✅ | 891 incidents |
| SH-33 | How many incidents mention gas leaks? | Single-hop | ✅ | 42 incidents |
| SH-34 | How many incidents describe man overboard situations? | Single-hop | ✅ | 114 incidents |
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
| SH-45 | What incidents involved helicopters? | Single-hop | ✅ | 51 incidents |
| SH-46 | What incidents were reported by PETROBRAS? | Single-hop | ✅ | 676 incidents |
| SH-47 | What incidents were reported by EQUINOR? | Single-hop | ✅ | 402 incidents |
| SH-48 | What incidents occurred at Sabetta? | Single-hop | ✅ | 880 incidents |
| SH-49 | What incidents occurred at Le Trait? | Single-hop | ✅ | 1135 incidents |
| SH-50 | What incidents resulted in abrasions or scratches? | Single-hop | ✅ | 329 incidents |
| SH-51 | What incidents occurred in 2024? | Single-hop | ✅ | 1461 incidents |
| SH-52 | What incidents have severity level 5 (most severe)? | Single-hop | ✅ | 23 incidents |
| SH-53 | What incidents are classified as occupational illness? | Single-hop | ✅ | 160 incidents |
| SH-54 | What incidents have red risk classification? | Single-hop | ✅ | 52 incidents |
| SH-55 | What incidents involved robots or drones? | Single-hop | ✅ | 13 incidents |
| SH-56 | What incidents occurred before 2016? | Single-hop | ✅ | 0 incidents |
| SH-57 | What incidents occurred in Antarctica? | Single-hop | ✅ | 0 incidents |
| SH-58 | What incidents involved tanks? | Single-hop | ✅ | 261 incidents |

**Overall:** 258 ✅ passing / 0 ⚠️ non-passing out of 258 queries

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
  Malaysia: 3
  Canada: 3
  Australia: 3
  Angola: 3
```

### AG-03: What equipment types are involved in the most incidents overall?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19849
Distinct EQUIPMENT values: 22286
Top 20:
  crane: 1069
  another forklift: 937
  ROV: 847
  rigging: 678
  hose: 678
  valve: 624
  deck: 486
  pallet: 405
  barrier: 404
  PPE: 399
  slinger: 363
  vessel: 343
  main deck: 339
  pipe: 323
  flange: 301
  air compressor: 298
  Truck: 286
  scaffolder: 279
  reel: 270
  Scaffolding: 267
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
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.3s

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
Matching incidents: 19849
Distinct BODY_PART values: 1753
Top 20:
  finger: 648
  left hand: 435
  right hand: 407
  hand: 393
  head: 268
  eye: 262
  back: 249
  foot: 216
  knee: 176
  face: 168
  ankle: 163
  right foot: 161
  leg: 160
  left foot: 154
  arm: 140
  shoulder: 137
  thumb: 132
  right eye: 122
  lower back: 110
  left leg: 108
```

### AG-08: What are the most common injury types across all incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19849
Distinct INJURY_TYPE values: 1179
Top 20:
  cut: 501
  pain: 489
  laceration: 265
  contusion: 188
  fracture: 172
  discomfort: 160
  bruise: 157
  personal injury: 152
  scratch: 141
  abrasion: 119
  swelling: 104
  burn: 89
  irritation: 83
  foreign body: 74
  closed fracture: 68
  sprain: 68
  bruising: 62
  personnel injury: 58
  injured: 53
  back pain: 52
```

### AG-09: Which organizations report the most incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 19849
Distinct ORGANIZATION values: 8830
Top 20:
  TECHNIPFMC: 4707
  JSC YAMAL LNG: 1302
  FLEXI FRANCE: 1017
  N/A - No Vendor: 820
  HSE: 577
  TRANS ADRIATIC PIPELINE AG: 571
  PETROBRAS: 520
  Shell: 478
  TECHNIPFMC UMBILICALS LTD: 428
  SASOL NORTH AMERICA, INC.: 332
  TECHNIP MARINE OPERATION SERVICES: 306
  ARCTIC LNG 2: 293
  HSEA: 268
  OCM: 266
  WOODSIDE ENERGY LTD.: 258
  BP: 229
  THE BAHRAIN PETROLEUM COMPANY BSC: 224
  EQUINOR ENERGY AS: 221
  FMC TECHNOLOGIES SURFACE INTEGRATED SERVICES, INC.: 220
  EXXONMOBIL: 209
```

### AG-10: What is the annual trend of manual handling incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

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
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 6
  Planning and coordination of works: 6
  Flammable solids, liquids and gases: 5
  Standard Operating Procedures, Procedures & Work instructions: 4
  Motor Vehicle Worksite Accident: 3
```

### AG-12: How do incidents break down by impact type over the years?
**Type:** Aggregation | **Status:** ✅ | **Time:** 3.3s

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
Matching incidents: 19849
Distinct LOCATION values: 230
Top 20:
  Aberdeen: 2493
  Houston: 1349
  Le Trait: 1110
  Rio de Janeiro: 892
  Sabetta: 872
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
Matching incidents: 19849
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
  Flammable solids, liquids and gases: 322
  Unfamiliar personnel: 322
```

### AG-16: What is the year-over-year trend of eye injuries?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Total incidents: 500
Months with data: 105
Yearly breakdown:
  2016: 50
  2017: 69
  2018: 70
  2019: 70
  2020: 47
  2021: 74
  2022: 22
  2023: 35
  2024: 34
  2025: 29
```

### AG-17: What are the most common injury types at construction sites?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 5357
Distinct INJURY_TYPE values: 556
Top 10:
  contusion: 153
  laceration: 112
  pain: 98
  cut: 92
  bruise: 84
  personal injury: 79
  fracture: 78
  discomfort: 68
  closed fracture: 63
  scratch: 54
```

### AG-18: Which clients report the most high-severity incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 167
Distinct ORGANIZATION values: 234
Top 10:
  TECHNIPFMC: 58
  N/A - No Vendor: 14
  PETROBRAS: 10
  HSE: 8
  EQUINOR ENERGY AS: 8
  WOODSIDE ENERGY LTD.: 5
  SIF: 4
  FMC KONGSBERG SUBSEA AS: 4
  HSEA: 4
  CHEVRON USA INC: 3
```

### AG-19: What is the year-over-year trend of fracture injuries?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Total incidents: 352
Months with data: 89
Yearly breakdown:
  2016: 38
  2017: 108
  2018: 70
  2019: 27
  2020: 18
  2021: 46
  2022: 8
  2023: 16
  2024: 11
  2025: 10
```

### AG-20: What equipment is most common in incidents at Aberdeen?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2499
Distinct EQUIPMENT values: 6828
Top 10:
  ROV: 532
  crane: 360
  rigging: 349
  deck: 323
  vessel: 241
  main deck: 223
  hose: 208
  barrier: 161
  valve: 112
  PPE: 94
```

### AG-21: How do incidents break down by work process and risk color?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.2s

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
**Type:** Aggregation | **Status:** ✅ | **Time:** 3.2s

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
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

```
Total incidents: 510
Months with data: 99
Yearly breakdown:
  2016: 65
  2017: 145
  2018: 122
  2019: 39
  2020: 31
  2021: 51
  2022: 20
  2023: 17
  2024: 11
  2025: 9
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
**Type:** Conjunctive | **Status:** ✅ | **Time:** 6.1s

```
Equipment nodes scanned: 3000
Dual-risk (accident + near-miss at same location/year): 1453 combos
Top 10:
  ROV @ Aberdeen (2017): 48 accidents, 33 near-misses
  ROV @ Aberdeen (2024): 47 accidents, 16 near-misses
  air compressor @ Sabetta (2018): 43 accidents, 20 near-misses
  ROV @ Aberdeen (2018): 45 accidents, 15 near-misses
  air compressor @ Sabetta (2017): 31 accidents, 29 near-misses
  crane @ Aberdeen (2017): 26 accidents, 33 near-misses
  ROV @ Aberdeen (2023): 40 accidents, 16 near-misses
  ROV @ Aberdeen (2016): 43 accidents, 11 near-misses
  rigging @ Aberdeen (2017): 25 accidents, 26 near-misses
  ROV @ Aberdeen (2022): 37 accidents, 10 near-misses
```

### CJ-05: Find the causal chain pattern: procedural non-compliance -> dropped object -> head/hand injury. How many incidents match?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Dropped-object incidents: 4,072
  With head/hand injury: 451
  With L2 causal edges: 298
  Total causal edges: 854

Procedural causal edges: 15
  Samples:
    [540653] pinched his right hand IV finger with the container door --CAUSAL--> immediately after the incident, he informed his supervisor and reported to the REGA JV clinic
    [575162] crane drive was instructed to come up with the hook --CAUSAL--> finger came loose
    [590559] inadequate designated drop off/pick up location for the Pit-stop --CAUSAL--> multiple maneuvers for bus to turn
    [629667] deviation from procedure when an individual entered the table prior to the incident to adjust a winch block --CAUSAL--> slipping of the Chinese finger on the tail end of the test piece
    [644074] misunderstood in communication --CAUSAL--> raising the mastil tensing chains
    [687682] I/P felt dizzy --CAUSAL--> Shift Supervisor advised to call 111 for advice
    [703112] inadequate lighting over the bed to assess patients --CAUSAL--> the bed had to be moved
    [546828] second finger --CAUSAL--> HSE Supervisor brought him to the First Aid point for the control and treatment
    [513348] welding wire head dropped into pipe spool --CAUSAL--> welder entered pipe spool without Confined Space Work to Permit
    [513348] welder entered pipe spool without Confined Space Work to Permit --FAILED_CONTROL--> Confined Space Work to Permit
    [556525] pinching IP’s left thumb --CAUSAL--> notifying supervisor
    [556525] notifying supervisor --CAUSAL--> sent to REGA clinic
    [534066] assistant supervisor removed the stone with his right hand --CAUSAL--> tailgate fully close
    [571609] Op believed that it was just a nip --CAUSAL--> Op contacted the Shift Supervisor on Tuesday evening
    [571609] increase in the pain in his finger --CAUSAL--> Op contacted the Shift Supervisor on Tuesday evening

Top causal factors for dropped → head/hand:
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 12
  fall with his leg between two steel structure: 3
  dropped metal plate (20 cm x 9 cm x 4mm, 250 g weight): 3
  left hand: 3
  small fire: 3
  Rt middle finger pain: 3
  slip: 3
  banging head on shelf lip: 3
  fall from chair: 3
  laceration: 3
```

### CJ-06: Which incidents involve the co-occurrence of slip/fall events AND vehicle/transportation equipment at construction sites?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 29
Sample: ['INCIDENT::11732', 'INCIDENT::16450', 'INCIDENT::24216', 'INCIDENT::516771', 'INCIDENT::520161']
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
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 1
Sample: ['INCIDENT::644762']
```

### CJ-09: Find forklift incidents at construction sites with severity >= 3.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 16
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
Matching incidents: 31
Sample: ['INCIDENT::11564', 'INCIDENT::15728', 'INCIDENT::17664', 'INCIDENT::17726', 'INCIDENT::17999']
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
Matching incidents: 148
Sample: ['INCIDENT::11913', 'INCIDENT::13554', 'INCIDENT::13702', 'INCIDENT::14321', 'INCIDENT::17879']
```

### CJ-14: Find crane incidents in Houston during 2018.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 3.4s

```
Matching incidents: 21
Sample: ['INCIDENT::569963', 'INCIDENT::570340', 'INCIDENT::572265', 'INCIDENT::574246', 'INCIDENT::574985']
```

### CJ-15: Find stored-energy incidents with head injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 37
Sample: ['INCIDENT::10105', 'INCIDENT::10882', 'INCIDENT::10960', 'INCIDENT::10961', 'INCIDENT::11124']
```

### CJ-16: Find marine incidents involving ROVs with equipment failures.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 8
Sample: ['INCIDENT::10944', 'INCIDENT::1314', 'INCIDENT::514184', 'INCIDENT::518912', 'INCIDENT::531362']
```

### CJ-17: Find vehicle road accidents at construction sites with injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 33
Sample: ['INCIDENT::13085', 'INCIDENT::15417', 'INCIDENT::16688', 'INCIDENT::18028', 'INCIDENT::23454']
```

### CJ-18: Find manual handling incidents with sprain/strain injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 36
Sample: ['INCIDENT::1408', 'INCIDENT::15186', 'INCIDENT::19918', 'INCIDENT::21307', 'INCIDENT::25077']
```

### CJ-19: Find stored-energy dropped-object incidents with lacerations.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 16
Sample: ['INCIDENT::11124', 'INCIDENT::13221', 'INCIDENT::20597', 'INCIDENT::504859', 'INCIDENT::520167']
```

### CJ-20: Find near-miss incidents involving forklifts in 2023.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 3.2s

```
Matching incidents: 63
Sample: ['INCIDENT::12422', 'INCIDENT::12535', 'INCIDENT::12642', 'INCIDENT::12794', 'INCIDENT::12820']
```

### CJ-21: What safety controls successfully mitigated harm across all incidents?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Total MITIGATED_BY edges: 849
Unique incidents: 721

Top successful controls/mitigations (675 distinct):
  injury: 20
  injuries: 19
  Ordinary safety glasses: 10
  PPE: 10
  fire: 8
  spill: 8
  fire extinguisher: 7
  SOPEP equipment: 6
  medic: 6
  hand gloves: 6
  Spill kit: 6
  first aid: 5
  harm to personnel: 5
  no injuries: 5
  Kit SOPEP: 4
  extinguisher: 4
  barricaded area: 4
  First Aider: 4
  eye wash station: 3
  Absorbency pads: 3

Top harms mitigated:
  fire: 21
  injury: 6
  spill: 5
  minor fire: 5
  hose failure: 5
  Hydraulic Oil leak: 4
  laceration: 4
  oil leak: 4
  oil spill: 4
  irritation to her skin on her face and eyes: 4

Sample edges (harm → control that worked):
  [1093] small cut to form on his head → first aid
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

Top failed barriers (737 distinct):
  fire: 14
  injuries: 10
  injury: 5
  hand gloves: 5
  hard hat: 4
  IP fell 4m from a ladder: 4
  helmet: 3
  Ordinary safety glasses: 3
  fire extinguisher: 3
  SOPEP equipment: 3
  barriers: 3
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
  Ordinary safety glasses: 4
  Hydraulic Oil leak: 3
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
  vessel movement: 6
  helmet dropped approximately 6m from the platform down to the quayside: 6
  Information tag missing from the trolley: 5
  bow shackle falling off at the bottom of the Cycle: 5
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
  impact: 4
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
Fracture incidents (via INJURY_TYPE): 352
With CAUSAL edges: 268
Total CAUSAL edges: 746

Top causal factors leading to fractures:
  Manual Handling: 6
  bruised and painful tibia: 5
  fracture: 5
  slipped: 5
  slipped and fell down: 4
  lost his balance: 4
  Falls, slips and trips on same level (without potential to fall to lower level): 4
  PTJ scaffolder fall down: 4
  swelling in his wrist: 3
  slipping and falling: 3
```

### CJ-27: Find crane incidents in Norway resulting in injuries.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 68
Sample: ['INCIDENT::10929', 'INCIDENT::11439', 'INCIDENT::12016', 'INCIDENT::12595', 'INCIDENT::12655']
```

### CJ-28: Find incidents with both equipment failure and manual handling root causes.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 0
```

### CJ-29: Find high-severity incidents at construction sites involving scaffolding.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 7
Sample: ['INCIDENT::129', 'INCIDENT::16468', 'INCIDENT::24559', 'INCIDENT::24560', 'INCIDENT::24562']
```

### CJ-30: Find incidents involving hoses with environmental impact at offshore locations.
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 25
Sample: ['INCIDENT::12463', 'INCIDENT::12909', 'INCIDENT::14002', 'INCIDENT::14527', 'INCIDENT::14607']
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
Start: 24103 EQUIPMENT nodes matching '.*'
  --CAUSAL--> EVENT: 1320 nodes
  --CAUSAL--> INJURY_TYPE: 160 nodes
  Final: 160 INJURY_TYPE nodes, 160 distinct values

Top 10:
  2nd degree burn/blisters: 1
  puncture in the tire on the drivers side rear of the loader: 1
  technician nearly struck in the head: 1
  injury: 1
  a couple of Project personnel got wet: 1
  hurt right wrist: 1
  minor damaged to the dock concrete barrier: 1
  no damage to any property's and injuries to personal: 1
  no injuries to any personnel: 1
  No harn to people: 1
```

### CJ-33: What events are caused by corrosion conditions (L2 traversal)?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Start: 28 CONDITION nodes matching 'corros'
  --CAUSAL--> EVENT: 17 nodes
  Final: 17 EVENT nodes, 17 distinct values

Top 10:
  upper hinge broke loose: 1
  small leak coming from a hydraulic hose located on the TTS crane boom: 1
  dropped object: 1
  outer strands broke: 1
  corrosion pinhole: 1
  birdcage in the Winch Level wind assembly: 1
  hydraulic oil return tube was stolen: 1
  securing rivets failed: 1
  hydraulic fluid sitting on top of the quench water: 1
  bollard sheared: 1
```

### CJ-34: What injuries result from failed controls (L2 traversal)?
**Type:** Conjunctive | **Status:** ✅ | **Time:** 0.0s

```
Start: 8921 CONDITION nodes matching '.*'
  --FAILED_CONTROL--> EVENT: 119 nodes
  --CAUSAL--> INJURY_TYPE: 23 nodes
  Final: 23 INJURY_TYPE nodes, 23 distinct values

Top 10:
  pinched left thumb: 1
  wounds or damage to the structure: 1
  landed on scaffolding platform then bounced up and touched the nearby workers' lower leg: 1
  scraped right hand: 1
  fractured pelvis: 1
  Closed fracture of the lateral malleolus on the right: 1
  cut wound of the left hand: 1
  technician getting a lot of oil on their hair, face, and clothes: 1
  wounds: 1
  Potential for harm from contact as the item rebounded to deck: 1
```

### GL-01: What are the most significant safety risk clusters across TechnipFMC global operations?
**Type:** Global | **Status:** ✅ | **Time:** 10.0s

```
Total communities: 11149
Top 10 by size:

  Community 1 (size=13708):
    EQUIPMENT: 6156 (e.g. ['SCM Running tool', '2 x wooden chocks', 'lithium fire blanket'])
    INCIDENT: 2766 (e.g. ['INCIDENT 727768 - Deep Arctic Environmental Incident Report - Lost (25kg uplift) lift bag on the surface during recovery of the large workbasket to deck. Enquest Mallard Power Cable Project 081431C001 - 05/09/2021', 'INCIDENT 712320 - Equipment Damage - 200072C001 - Enquest Norther Producer - North Sea - Deep Discoverer - 11.April.2021 - Damage to winch pipework termination', 'INCIDENT 710192 - Damage  - 000298A001 - Transit to Rotterdam – Deep Blue – 23 Mar 2021 - Damage to Vessel hull during berthing'])
    LOCATION: 2256 (e.g. ['Block 32 offshore Angola', 'Halten East', 'convés do navio'])
    ORGANIZATION: 1717 (e.g. ['Ithaca Energy (UK)Ltd', 'Offshore HSE advisor', 'pipelay crew'])
    BODY_PART: 289 (e.g. ['inside of the eyelid', 'skin area', 'left hand weak link'])
    EVENT: 221 (e.g. ['fingers getting caught between the mushroom vent and the frame', 'falling on the barge (27mt)', 'HPU activation'])
    INJURY_TYPE: 188 (e.g. ['slight ache', 'Conjunctival redness', 'inch laceration'])
    CONDITION: 65 (e.g. ['failing to secure the fitting', 'non-tie-off or non-usage of tool box', 'no work-at height had been identified'])
    ACTION: 30 (e.g. ['suspended activities', 'repair', 'welder raising face shield without signaling'])
    MATERIAL: 11 (e.g. ['welding rod (24" in length and weighing about 2oz)', 'leaked acetylene gas', 'small piece of material'])
    ROOT_CAUSE_CATEGORY: 6 (e.g. ['Stored energy (dropped objects)', 'Weather Condition', 'Psycho social - Alcohol and drugs abuse'])
    PERSON: 3 (e.g. ['operator driving the under roller', 'Bosun and ABs', 'Rigging Supervisor being in charge of reel rotation'])

  Community 2 (size=10291):
    INCIDENT: 3817 (e.g. ['ACCIDENT 599001 - Test Pressure Incident--Large Test Cell--7/23/18', 'ACCIDENT 572924 - Non TFMC owned - MTI - APC Constellation - Spitzer (subcontractor) - 12 Feb, 2018 - Knee laceration', 'ACCIDENT 21583 - 002 - S05 - SIT - Property Damage - A tubing hanger was dropped from the horizontal stands while in process of removing the VAM plug.'])
    EQUIPMENT: 3021 (e.g. ['red 35k capacity forklift', 'hammer wrench', '4-Port pod'])
    LOCATION: 1548 (e.g. ['Gremp Campus', 'row of barricades', 'wooded area'])
    ORGANIZATION: 978 (e.g. ['CSE W-INDUSTRIES, LLC', 'ULM', 'Oncor Electrical utility service'])
    EVENT: 324 (e.g. ['wasp on the desk', 'uncontrolled movement of the crane boom', 'driver lost control turning sideways'])
    BODY_PART: 255 (e.g. ['safety toe portion', 'IPs arm', "palm of the employee's hand"])
    INJURY_TYPE: 188 (e.g. ['mild left ankle sprain', 'stiffness and pain', 'Diagnosis: closed Ulnar styloid fracture'])
    CONDITION: 67 (e.g. ['false floor', 'Lube-A-Boom Grease becoming tacky', 'ESD not functioning'])
    ACTION: 63 (e.g. ['adjusting riser', 'diapers had been laid down to soak up the fluid', 'hammering pegs into the ground'])
    MATERIAL: 12 (e.g. ['thick gear oil (AtomOil Gear EP)', 'combination of regular lithium-purpose grease and Lube-A-Boom Grease', 'residual Oceanic HW 443 (Glycol/Antifreeze) fluid'])
    ROOT_CAUSE_CATEGORY: 11 (e.g. ['Over-consumption of energy, natural resources (water, etc.)', 'Planning and coordination of works', 'Standard Operating Procedures, Procedures & Work instructions'])
    PERSON: 7 (e.g. ['HSE manager on site and the facilities tech', 'employee', 'SUV that was waiting to enter and go N. on 1604'])

  Community 3 (size=6487):
    INCIDENT: 1962 (e.g. ['NEAR MISS 524433 - Incidente Ambiental - P76 Project - Brasil Pontal do Paraná - 16/01/2017 - Oleo hidráulico de um guindaste_x000D_', 'NEAR MISS 7864 - 703672 - Tampa da caixa d’água se desprendeu e caiu', 'INCIDENT 705247 - Quase-Acidente - A?u Spoolbase: Vazamento de óleo na tomada de for?a que movimenta a bomba de caminh?o abastecedor.'])
    EQUIPMENT: 1863 (e.g. ['Starboard Adjuster', 'banco', 'lingada ajustável'])
    LOCATION: 1264 (e.g. ['A?uSpoolbase', 'Cais DOME', 'marinho'])
    ORGANIZATION: 789 (e.g. ['OCEANIC HW', 'Ecopolo', 'Public Hospital of Macaé'])
    EVENT: 230 (e.g. ['hanger leaving its position', 'deslizamento longitudinal da sobra', 'striking of I-beam and handrails'])
    BODY_PART: 175 (e.g. ['perna esquerda', 'corpo', 'no ombro'])
    INJURY_TYPE: 106 (e.g. ['pain or discomfort', 'minor injury', 'slight shoulder injury'])
    CONDITION: 45 (e.g. ['unexpected gust of wind', 'difficulties with this model of glasses', 'broken monitor was not in the healthy state'])
    ACTION: 29 (e.g. ['pressing the right finger between the bubble and the side of the shelter', 'slipping on the edge of the work platform step', "IP inspected the surface but didn't see any objects"])
    ROOT_CAUSE_CATEGORY: 13 (e.g. ['Hot/cold surfaces or media', 'Information perceptiveness (amount / mode) & Information reception (extend / range)', '3. 3rd Party NCR (received or managed by TechnipFMC or Partners)'])
    MATERIAL: 6 (e.g. ['cutting rubber', 'waterized MUD', 'waste of the same ended up falling in the ch.o'])
    PERSON: 5 (e.g. ['people in the environment', 'operator in the face', 'Leader and first aider'])

  Community 4 (size=4247):
    INCIDENT: 1485 (e.g. ["NEAR MISS 18637 - NM - 15/12/2023 - Glissement du collier d'armage en cours de montage", "NEAR MISS 623395 - SD-Riblonneuse-29/01/2019-Chute d'outil au sol", 'NEAR MISS 24257 - NM-15/10/2024- Entre BSP15 et SP10 - Légère torsion de cheville en marchant sur un rebord de chappe'])
    EQUIPMENT: 948 (e.g. ['trimble', 'monocuve', 'airbags of the vehicle'])
    LOCATION: 719 (e.g. ['spiral reception 4', 'pedestrian passage', 'OUTILAGE'])
    ORGANIZATION: 461 (e.g. ['the Adria', 'Ponticelli SONILS', 'MET'])
    EVENT: 232 (e.g. ['second motorcycle entering the lane', 'hydrolysis reaction generating hydrogen / oxygen production', 'helmet fell off his head while falling'])
    INJURY_TYPE: 151 (e.g. ['pain behind the neck', 'strong arm pain', 'left leg injury'])
    BODY_PART: 130 (e.g. ["Operator's arm", 'feet', 'bichenille arm'])
    CONDITION: 53 (e.g. ['no physical consequences', 'static electricity', 'weight of the assembly (Raccord/Vanne/Tuyaux) in false door'])
    ACTION: 52 (e.g. ['medic treatment', 'work performed the previous day', 'manipulating a forest'])
    ROOT_CAUSE_CATEGORY: 9 (e.g. ['Psycho social - Stress', 'Psycho social - Workload (Overload/Underload)', 'Repetitive/one sided physical demand'])
    PERSON: 4 (e.g. ['decoration workers on the 13F', 'First Responder', 'person opening the door fast from another side without seeing me'])
    MATERIAL: 3 (e.g. ['particle of weld bark', 'spilled lubricant', 'amount of water (1-3 m3)'])

  Community 5 (size=3920):
    INCIDENT: 1056 (e.g. ['INCIDENT 740023 - LTI-Arctic LNG 2-NMP-26 December 2021-Employee lost balance and fall from hydraulic pallet mover', 'ACCIDENT 592091 - FAC - Yamal LNG Project - Sabetta - 12.06.2018 - left ankle sprain', 'NEAR MISS 579815 - NM - Yamal LNG Project - 034693C009 - Sabetta - 27.03.2018 -  tearing of textile slings'])
    EQUIPMENT: 885 (e.g. ['man lift “HYUNDAY”', 'insulation strapping tool', 'concrete slabs'])
    LOCATION: 796 (e.g. ['main office', 'dornite', 'BPTH #17 CVB'])
    ORGANIZATION: 483 (e.g. ['OMC management', 'Teplovent LLC', 'Tadano'])
    INJURY_TYPE: 243 (e.g. ['Periorbital hematoma', 'metacarpal bone injury', 'pain at the latter metapes of the hand'])
    BODY_PART: 205 (e.g. ['left ankle-joint ligaments', 'left forearm', 'II metacarpal'])
    EVENT: 147 (e.g. ['self-ignition of the charger which is switched on in the electric network', 'slipped and fell down on his left hand', 'Event("fall on the ground")'])
    ACTION: 51 (e.g. ['the other one activated the fire alarm system', 'stepping on one stone on the ground', 'turning around and moving out of the working area'])
    CONDITION: 45 (e.g. ['sharp edge of the purlin', 'observed the swallowed the feeling', 'fuel did not pass through the fuel injector of the heat generator, as it was clogged with industrial dust in diesel fuel'])
    ROOT_CAUSE_CATEGORY: 4 (e.g. ['Manual handling', 'Explosives / potential explosives', 'Falls, slips and trips on same level (without potential to fall to lower level)'])
    MATERIAL: 3 (e.g. ['hot porrige', '3 palettes containing in all 14 leaf crowns', 'dropped metal plate (20 cm x 9 cm x 4mm, 250 g weight)'])
    PERSON: 2 (e.g. ["IP's face", 'REGA slinger'])

  Community 6 (size=3518):
    EQUIPMENT: 872 (e.g. ['Duster', 'cotton net/gauze', 'four-axle loaded dump truck'])
    LOCATION: 847 (e.g. ['nearby channel', 'river side', 'KP 26+800'])
    INCIDENT: 672 (e.g. ['ACCIDENT 597661 - NON-Technip Owned - BNJ-FAC 36 - 2529 TAP Project - Greece/KP 399- 12/07/2018 - minor laceration on forearm with grinder', 'NEAR MISS 564199 - NON Technip Owned - RNT-NM 05 - 2529 TAP - Albania/ACS03 - 16/12/2017 - Potential fall from height', 'ACCIDENT 524274 - NON-Technip Owned - SCA-DA (RTA) 07 - 2529 TAP - Greece/MMY Alexandropoulos - 14/12/2016 - Mobile canteen exhaust stack damaged by truck'])
    ORGANIZATION: 627 (e.g. ['archaeology department', 'DRA', 'HSS department'])
    EVENT: 199 (e.g. ['IP struggling with the heat and sweating profusely', 'pipe spool slipped from trailer bed', 'grinder kicked back'])
    INJURY_TYPE: 113 (e.g. ['lingering acute pain', 'Injury: I-II degree frostbite', 'second fracture'])
    CONDITION: 67 (e.g. ['sudden change in CG (Eccentric load)', 'Side-boom transmission problem', 'hot water located inside'])
    BODY_PART: 56 (e.g. ['right-side', 'right above the ankle', 'L1 vertebra'])
    ACTION: 55 (e.g. ['spontaneous move to remove the bee', 'lost the grip of the tool', 'the welder did not handle properly the Stanley knife'])
    ROOT_CAUSE_CATEGORY: 5 (e.g. ['Psycho social - Inappropriate behaviour / horseplay / Aggression / violence (Fights/Riots etc. ...)', 'Illumination / sight / visibility', 'Inadequate Supervision'])
    MATERIAL: 3 (e.g. ['hot iron chip', 'empty food container and empty IBC', 'poly plank previously fitted slipped around the bundle'])
    PERSON: 2 (e.g. ['Person', 'the crew consisted of 1 supervisor, 2 excavator operators, 2 side boom operators'])

  Community 7 (size=3483):
    EQUIPMENT: 1045 (e.g. ['haskel pump', 'oxy acetylene hose', 'perforated plate'])
    INCIDENT: 994 (e.g. ['NEAR MISS 505691 - Scaffolder lost balance, fell and stopped his fall', 'ACCIDENT 509696 - LTI-MTC-MWP10B-SMOE-Batam-Indonesia-16 Sept 16-Over pressurization of Actuator resulting in a sudden burst. 1 LTI - 2 MTC injuries recorded', 'NEAR MISS 522901 - Near Miss, Yamal LNG MWP1, China Qingdao COOEC,17th Jan 2017,Insulation material was caught on fire while cutting kick plate on module 213-PAU-001'])
    LOCATION: 614 (e.g. ['B234/235', 'Matak Island', '4A bay Block Assembly Workshop'])
    ORGANIZATION: 523 (e.g. ['Ziquan', 'TechnipFMC China', 'Mechanical & Electrical Workshop'])
    EVENT: 119 (e.g. ["man lift didn't stop in time", 'squeezed the fingers on his left hand between the other part of the door and the container', 'crushes his work pants on the leaf'])
    INJURY_TYPE: 66 (e.g. ['scratch', 'pop in the right knee', 'little cut'])
    CONDITION: 40 (e.g. ['slippery surface of form work ply wood', 'sauce that no improved the problem', 'corrosion where the pad adheres to the bolted base plate'])
    BODY_PART: 39 (e.g. ['both hands and face', 'left side back area', 'lower eyelid'])
    ACTION: 30 (e.g. ['blaster stopped his activities', 'tetanus injection', 'dismantling the scaffold without permission'])
    ROOT_CAUSE_CATEGORY: 6 (e.g. ['Use of personal protective equipment', 'Flammable solids, liquids and gases', 'Workplace layout / congestion'])
    PERSON: 5 (e.g. ['SIEMENS EHS Manager', 'Person: Samsaliev Sakish of REGA JV', 'HSE Scaffold'])
    MATERIAL: 2 (e.g. ['iron filings in the groove of the grinding face shield', 'rusty iron wire'])

  Community 8 (size=3328):
    INCIDENT: 1037 (e.g. ['INCIDENT 697616 - NM - APSB - Maintenance Office - 13/11/2020 - Ceiling dropped', 'NEAR MISS 18117 - Hanger Slipped from Moveable V-Roller Stand', 'ACCIDENT 21154 - Left Index Finger Caught Between Tool and Flange'])
    EQUIPMENT: 936 (e.g. ['fire engine', 'pinion shaft', 'MIG 13'])
    LOCATION: 652 (e.g. ['warehouse charging station', 'sloppy face', 'Switchboard No.1'])
    ORGANIZATION: 423 (e.g. ['GENESIS OIL & GAS CONSULTANTS MALAYSIA SDN. BHD.', 'Operation (Maintenance) Dept', 'Trident Offshore'])
    EVENT: 102 (e.g. ['I-beam slipped off a forklift', '0.5L of hydraulic oil released', 'tilted and broke due to the heavy impact of the collision'])
    BODY_PART: 73 (e.g. ['right hand/thumb', 'left side of the front wheel', 'tibia/tibula'])
    INJURY_TYPE: 61 (e.g. ['possible trauma', 'nail puncture wound', 'pinched and injured'])
    CONDITION: 20 (e.g. ['not flowing into the domestic drain', 'motorized power jack was out of service', 'minor dent sustained by under-roller guard'])
    ACTION: 17 (e.g. ['handbrake application', 'maneuvering the truck closer to the wall', 'crew and contractor stop the job'])
    MATERIAL: 4 (e.g. ['hydraulic fluid on the ground', 'absorbents', 'water and fluid mix'])
    ROOT_CAUSE_CATEGORY: 2 (e.g. ['Equipment condition', 'Electrical current / electrocution / ESD / electromagnetic Fields'])
    PERSON: 1 (e.g. ['IP standing behind the cradle'])

  Community 9 (size=3110):
    EQUIPMENT: 992 (e.g. ['3.2T crane', 'El rack', 'XT reel'])
    INCIDENT: 903 (e.g. ['ACCIDENT 22031 - First aid-cut in face when hit traffic sign', 'NEAR MISS 25209 - In connection with the lifting operation of the XT from the truck to the boat, the crane operator started the lifting operation without receiving a signal from the flagman on the ground. This led to a collision between the lifting cap and the XT.', 'NEAR MISS 13205 - forklift slipped on an oily floor'])
    LOCATION: 459 (e.g. ['moonpool hatch', 'mafi flatbed', 'building 14C WH'])
    ORGANIZATION: 406 (e.g. ['PIG', 'CCB portvakt', 'Martin Linge'])
    EVENT: 107 (e.g. ['structure launched up out of its seat', 'cut tube gave 6.32 cps when cut', 'areas where the object hit'])
    INJURY_TYPE: 83 (e.g. ['personnel-injury', 'unconscious', 'discomfort in his eye'])
    BODY_PART: 69 (e.g. ['last finger', 'thigh', 'starboard leg'])
    CONDITION: 58 (e.g. ['refueling at the time of the incident', 'lifting area delimitation and clearance of the hazardous zone', 'absorbed water'])
    ACTION: 19 (e.g. ['IP flushed his eye out', 'Shawcor index operator stopped the job', 'reversing in the parking area near the compressor'])
    MATERIAL: 7 (e.g. ['barbed wire made of elastic and cutting material', 'use of standard cleaning product', 'tree trunk'])
    PERSON: 4 (e.g. ['IP on his hard hat', 'Nikita Chirko', 'emergency team on yard'])
    ROOT_CAUSE_CATEGORY: 3 (e.g. ['Radiation (ionising / non ionising)', 'Lifting ops error', '1. Internal NCR (issued by TechnipFMC or Partners)'])

  Community 10 (size=2553):
    EQUIPMENT: 775 (e.g. ['Poclain', '1.6 mm thick cutting disc', 'painting bed'])
    INCIDENT: 768 (e.g. ['NEAR MISS 571144 - Near Miss_XXXX_2/5/2018_Intermediate Tube Sheet slipped from its bracket', 'NEAR MISS 27716 - Near Miss - Striking against ROV grab bar', 'NEAR MISS 632742 - NM_HURL-Sindri_077625_Shuttering plates slipped from the trailer bed'])
    LOCATION: 442 (e.g. ['W area', 'south side of CCR', '90-C-02'])
    ORGANIZATION: 292 (e.g. ['GETs', 'Neo', 'M/s Sai Engineering team'])
    EVENT: 87 (e.g. ['harness got stuck on a structural bracing situated below 6 meter', 'tilted', 'wooden bar slipping during leveraging'])
    BODY_PART: 83 (e.g. ['thumb finger', 'fore finger', 'lower ankle joint'])
    INJURY_TYPE: 70 (e.g. ['minor prick injury', 'external injuries', 'bone crack'])
    CONDITION: 23 (e.g. ['unsafe condition of grating', 'inherent weakness in his right ankle', 'lashing belt stuck in-between'])
    ACTION: 10 (e.g. ['fitter tried to fixed (install) this unsafe grating position', 'trip on the door frame lip of the drill shack', 'awkward position using his left shoulder to hold and balance the panel'])
    ROOT_CAUSE_CATEGORY: 1 (e.g. ['Accumulation / Presence of explosive atmosphere'])
    MATERIAL: 1 (e.g. ['protruding strand of steel wire'])
    PERSON: 1 (e.g. ['person handling tremie pipe'])
```

### GL-02: Are there systemic patterns where the same type of equipment failure recurs across different geographic regions?
**Type:** Global | **Status:** ✅ | **Time:** 0.5s

```
Equipment appearing in 5+ regions: 266
  ROV: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  column: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  another forklift: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  x-raying: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  vehicle: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  pallet: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  air compressor: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  crane: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  valve: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  rigging: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  flange: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  hose: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  vessel: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  PPE: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  barrier: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  Truck: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  trailer: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  pipe: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  deck: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
  manlift: 7 regions -> ['Africa', 'Asia Pacific', 'Europe', 'India', 'Middle East', 'North America', 'South America']
```

### GL-03: How has the overall safety incident profile changed over the dataset time range? Are certain incident types increasing or decreasing?
**Type:** Global | **Status:** ✅ | **Time:** 3.4s

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
  ORGANIZATION::TECHNIPFMC -- degree 4709
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
  LOCATION::Le Trait -- degree 1115
  ROOT_CAUSE_CATEGORY::Hazardous liquids (exposure to / spill / loss of containment /pollution) -- degree 1092
  EQUIPMENT::crane -- degree 1070

Top 20 non-incident nodes by PageRank:
  LOCATION::Europe -- PR 0.010182
  LOCATION::North America -- PR 0.007471
  LOCATION::USA -- PR 0.006346
  LOCATION::Asia Pacific -- PR 0.004410
  LOCATION::UK -- PR 0.004197
  LOCATION::South America -- PR 0.003347
  LOCATION::Brazil -- PR 0.002520
  LOCATION::France -- PR 0.002345
  ORGANIZATION::TECHNIPFMC -- PR 0.002270
  LOCATION::Norway -- PR 0.001617
  LOCATION::Aberdeen -- PR 0.001537
  LOCATION::India -- PR 0.001309
  EVENT::fire -- PR 0.001278
  LOCATION::Houston -- PR 0.001183
  LOCATION::Africa -- PR 0.001144
  LOCATION::Le Trait -- PR 0.001125
  LOCATION::Russia -- PR 0.001115
  LOCATION::India -- PR 0.000950
  LOCATION::Middle East -- PR 0.000913
  LOCATION::Malaysia -- PR 0.000894
```

### GL-05: What are the most common equipment-body part co-occurrences across all incidents?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Total distinct (equipment, body_part) pairs: 26250
Top 20:
  Ordinary safety glasses + eye: 68 incidents
  PPE + eye: 54 incidents
  Ordinary safety glasses + face: 35 incidents
  Ordinary safety glasses + left eye: 34 incidents
  hand gloves + finger: 33 incidents
  PPE + finger: 32 incidents
  Ordinary safety glasses + right eye: 31 incidents
  PPE + left hand: 30 incidents
  PPE + right eye: 29 incidents
  PPE + face: 26 incidents
  hard hat + head: 25 incidents
  pipe + finger: 24 incidents
  rigging + finger: 23 incidents
  PPE + left eye: 22 incidents
  PPE + right hand: 21 incidents
  hand gloves + hand: 20 incidents
  PPE + hand: 19 incidents
  hand gloves + left hand: 18 incidents
  crane + finger: 18 incidents
  flange + finger: 17 incidents
```

### GL-06: How do safety profiles compare across the top 5 clients by incident volume?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Top 5 clients by incident count:

  TECHNIPFMC (4707 incidents):
    Types: {'Near Miss': 1477, 'Accident': 1739}
    Severity dist: {1: 598, 2: 642, 3: 288, 4: 48, 5: 10}
    Mean severity: 1.88

  JSC YAMAL LNG (1302 incidents):
    Types: {'Near Miss': 418, 'Accident': 884}
    Severity dist: {}
    Mean severity: 0.00

  FLEXI FRANCE (1017 incidents):
    Types: {'Accident': 338, 'Near Miss': 404}
    Severity dist: {1: 290, 2: 54, 3: 27, 4: 3}
    Mean severity: 1.31

  N/A - No Vendor (820 incidents):
    Types: {'Accident': 458, 'Near Miss': 362}
    Severity dist: {1: 314, 2: 367, 3: 125, 4: 12, 5: 2}
    Mean severity: 1.81

  HSE (577 incidents):
    Types: {'Accident': 269, 'Near Miss': 157}
    Severity dist: {1: 143, 2: 67, 3: 27, 4: 7, 5: 1}
    Mean severity: 1.60
```

### GL-07: Are there seasonal (monthly) patterns in incident frequency?
**Type:** Global | **Status:** ✅ | **Time:** 3.6s

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
Regions with RCC data: 7

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
```

### GL-09: How many incidents mention burns in narrative but have no burn injury type extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'burn': 177
  With INJURY_TYPE extracted: 126
  WITHOUT INJURY_TYPE extracted (gap): 51
  Gap rate: 28.8%

Sample gap incidents:
  #14461: "Around 15:00 local time (8 am HOU time) today, during start-up activities with the WOCS container, our WOCS operator Mag..."
  #19666: "One of the welder after welding trial sample tube, he allowed to cool down to some extent and then kept on welding machi..."
  #20681: "Derived to voltage variations in the site 2 (stock area offices) a UPS was overheated which caused the current adapter t..."
  #21872: "The operator cuts the production end ribs to the lapidary, he carries his protective sheet, the bright projections burn ..."
  #26370: "Tarpaulin, which was protecting some structures (Sealine Protection Frames) of the project, started to burn (see photo),..."
```

### GL-10: How many incidents mention fractures in narrative but have no fracture injury type extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.3s

```
Narrative mentions 'fracture': 442
  With INJURY_TYPE extracted: 352
  WITHOUT INJURY_TYPE extracted (gap): 90
  Gap rate: 20.4%

Sample gap incidents:
  #10689: "Employee (ID# 30800964) was taking his lunch break, and carrying his lunch.  Employee walked behind a pedestal fan that ..."
  #10759: "Employee (ID#  , contract employee) was stapling a plastic covering to a wooden pallet with a hammer tacker.  The plasti..."
  #1594: "Crews were in the process of manually rolling pipe in the ready rack to eliminate open gaps in the pipe advancement area..."
  #16201: "After the fracture operations when the Shell PAD 20 pools were completed, it is observed that the turks and bulbs had fa..."
  #16202: "After the fracture operations when the Shell PAD 20 pools were completed, it is observed that the turks and bulbs had fa..."
```

### GL-11: How many incidents mention cranes in narrative but have no crane equipment extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'crane': 1,877
  With EQUIPMENT extracted: 1,873
  WITHOUT EQUIPMENT extracted (gap): 4
  Gap rate: 0.2%

Sample gap incidents:
  #12582: "Hall G Crane  Halvportalkran ble kj?rt inn i Traverskran, det skjedde med lav fart kranen ble stoppet med én gang. Ingen..."
  #13022: "B14  crane  Da 10 tonns kran var i bruk, ble krankroken kj?rt ned samtidig som l?ypekatten ble kj?rt til h?yre og kranen..."
  #524433: "Durante opera??o do guindaste T160458 (ZOOMLION - 260 ton) na desmontagem do Guindaste da MAMMOET, ocorreu o rompimento ..."
  #632767: "Environmental Conditions  The incident occurred at approx. 11:30 on the 17th April 2019. The vessel was moored at Orkang..."
```

### GL-12: How many incidents mention forklifts in narrative but have no forklift equipment extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.4s

```
Narrative mentions 'forklift': 1,075
  With EQUIPMENT extracted: 1,070
  WITHOUT EQUIPMENT extracted (gap): 5
  Gap rate: 0.5%

Sample gap incidents:
  #14592: "Yard CCB Agotnes DO - Skid fell of forklift forks during transport. Splog mistet skid ved rubbhall mellom flakparkering ..."
  #516354: "Port: Durante basculamento do suporte para descarte de fios da desarmagem em uma ca?amba de resíduos localizada na emiss..."
  #568625: "Technician was on his way out to the WIP lane to bring in an upper tree frame using Big Red Forklift, when he  made a wi..."
  #582302: "EMPLOYEE HIT DOOR JAM WITH TOP OF FORKLIFT..."
  #692361: "At 1.45 am on 28/9/2020, an under roller power damaged by forklift tires during reversing after delivered raw material t..."
```

### GL-13: How many high-severity incidents (>=4) have no injury type extracted?
**Type:** Global | **Status:** ✅ | **Time:** 2.8s

```
Incidents with severity >= 4: 167
  With INJURY_TYPE extracted: 27
  WITHOUT INJURY_TYPE (gap): 140
  Gap rate: 83.8%

Severity breakdown of gap incidents:
  Severity 4: 120
  Severity 5: 20

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
  With BODY_PART extracted: 6,203
  WITHOUT BODY_PART (gap): 5,533
  Gap rate: 47.1%
```

### GL-15: How many incidents have very short narratives (<100 chars) with no entities extracted?
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Incidents with narrative < 100 chars: 978
  With entity extraction: 677
  Without any entity extraction: 301
  Likely test/placeholder records: 5
  Genuine short narratives (no entities): 296

Sample short-narrative gaps:
  #24420: "COMPANY VEHICLE LD5571 STRUCK A DEER"
  #159: "Employee slipped on ice when stepping briefly onto the lawn before entering the building."
  #16649: "COMPANY TRUCK LD3882 WAS DISCOVERED TO HAVE 3 SLASHED TIRES IN MANCAMP PARKING LOT"
  #27422: "Kranservice. Old open case. No explanation. Closing."
  #22971: "Drop of Huron container"
```

### GL-16: How many incidents contain non-English narratives with reduced entity extraction?
**Type:** Global | **Status:** ✅ | **Time:** 0.2s

```
Overall mean entity extraction per incident: 3.76

Portuguese: 410 incidents, mean entities=5.60 (vs 3.76 overall), 15 with zero extraction
French: 4,634 incidents, mean entities=5.88 (vs 3.76 overall), 119 with zero extraction
Spanish: 384 incidents, mean entities=5.68 (vs 3.76 overall), 13 with zero extraction
Russian: 7 incidents, mean entities=4.86 (vs 3.76 overall), 0 with zero extraction

Total non-English incidents: 5,435
Total with zero extraction: 147
```

### GL-17: Find the 10 incidents most similar to incident #29857 (dropped pry bar) using hybrid embedding similarity.
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Seed incident: #29857

Top 10 most similar incidents (text embedding cosine):
  #24829 (sim=0.645) type=Near Miss sev=2.0 eq=['ROV', 'Pry Bar', 'Flange spreaders']
  #503254 (sim=0.583) type=Accident sev=? eq=['ROV', 'lanyard', 'rigging']
  #24785 (sim=0.574) type=Near Miss sev=2.0 eq=['ROV', 'Flange spreaders', 'lanyard']
  #20278 (sim=0.565) type=Accident sev=1.0 eq=['ROV UHD 58', 'Judy Platform', 'ROV hydraulic shackle']
  #25648 (sim=0.561) type=Near Miss sev=2.0 eq=['ROV', 'cage', 'tether']
  #14126 (sim=0.552) type=Near Miss sev=1.0 eq=['ROV system', 'ROV’s', 'ROV']
  #683770 (sim=0.552) type=? sev=? eq=['ROV']
  #548733 (sim=0.540) type=Accident sev=? eq=['ROV Mil 208', 'TMS’s', 'latch beam']
  #693551 (sim=0.540) type=? sev=? eq=['ROV', 'ROV 1', 'FMC Smart pack']
  #639111 (sim=0.538) type=Accident sev=? eq=['ROV', 'TMS’s', 'water pump']

Seed equipment: ['Pry Bar', 'ROV', 'TMS’s', 'lanyard']
Equipment overlap (hit rate): 10/10 (100%)
```

### GL-18: Find the 10 incidents most similar to incident #569346 (ladder fall with broken teeth) using hybrid embedding similarity.
**Type:** Global | **Status:** ✅ | **Time:** 0.1s

```
Seed incident: #569346

Top 10 most similar incidents (text embedding cosine):
  #573223 (sim=0.791) type=Near Miss sev=? eq=['mobile pipe section', 'sideboom', 'mobile section']
  #633596 (sim=0.790) type=Near Miss sev=? eq=['EPE PL95 SN 0042', 'boom', 'pipe']
  #591511 (sim=0.759) type=Accident sev=? eq=['excavator', 'clamper', 'pipe']
  #585953 (sim=0.752) type=Near Miss sev=? eq=['CAT 594 Sideboom', 'mobile section', 'sideboom']
  #522123 (sim=0.737) type=Near Miss sev=? eq=['pipeline mobile section', 'overhead 20 KV mid-voltage cable', 'sideboom']
  #545428 (sim=0.736) type=Near Miss sev=? eq=['four-pipe section', 'four side-booms', 'the machine']
  #605490 (sim=0.736) type=Near Miss sev=? eq=['pipe string', 'section of the pipe', 'sideboom']
  #539318 (sim=0.733) type=Near Miss sev=? eq=['sideboom', 'excavator']
  #602722 (sim=0.723) type=Near Miss sev=? eq=['heavy bending machine', 'winch drum', 'JSA']
  #514069 (sim=0.718) type=Accident sev=? eq=['sideboom', 'Plant number 44.1404', 'counterweight']

Seed equipment: ['Load. Moment Indicator', 'Superior CPX-94', 'boom block wire rope', 'cable', 'ladder', 'sideboom']
Equipment overlap (hit rate): 6/10 (60%)
```

### GL-19: Do the top-10 text-similar incidents for a forklift accident share the same equipment type? (structural hit rate)
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Seed: #324 (equipment=forklift|flt)

  ✓ #663852 (sim=0.701) eq=['5 ton forklift', 'barrier']
  ✓ #18838 (sim=0.683) eq=['loading frame on truck', 'loading frame', 'another forklift']
  ✓ #8142 (sim=0.656) eq=['another forklift', 'WAREHOUSE FLOOR']
  ✓ #721112 (sim=0.655) eq=['cargo box', 'another forklift', 'boom']
  ✓ #676741 (sim=0.654) eq=['another forklift', 'Truck', 'front right wheel']
  ✓ #517760 (sim=0.652) eq=['another forklift', 'Truck']
  ✓ #18589 (sim=0.650) eq=['pallet', 'another forklift']
  ✓ #631498 (sim=0.648) eq=['hotwork equipment', 'Truck', 'welding machine']
  ✓ #530325 (sim=0.645) eq=['another forklift']
  ✓ #8289 (sim=0.644) eq=['another forklift', 'pallet']

Hit rate: 10/10 (100%)
```

### GL-20: Do the top-10 text-similar incidents for a crane near-miss share the same equipment type? (structural hit rate)
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Seed: #611920 (equipment=crane)

  ✗ #690238 (sim=0.759) eq=['doubler', 'doubler plate', 'main deck']
  ✗ #578594 (sim=0.743) eq=['16 inch pipeline', 'starboard freeboard deck', 'adflow helmet']
  ✗ #564142 (sim=0.734) eq=['Theodore Spool Base', 'another forklift', 'low boy trailer']
  ✗ #741158 (sim=0.733) eq=['Vessel position', 'light', 'rubber end cap']
  ✗ #582898 (sim=0.731) eq=['Rigid Deck Tensioner (RDT)', 'elevated walkway', 'RDT']
  ✓ #518187 (sim=0.729) eq=['tower crane', 'main aligner vertical roller', 'deck']
  ✓ #500105 (sim=0.729) eq=['main aligner top rollers', 'tower crane', 'brace']
  ✓ #593614 (sim=0.725) eq=['boom crane', 'boom truck', 'Grapples']
  ✗ #566838 (sim=0.724) eq=['extension cord', 'ballast tank 1204', 'ventilation fan']
  ✗ #679278 (sim=0.723) eq=['reel', 'transportation trolley', 'deck']

Hit rate: 3/10 (30%)
```

### GL-21: How well do text embeddings and structural similarity agree on the top-10 most similar incidents? (method correlation)
**Type:** Global | **Status:** ✅ | **Time:** 0.6s

```
Compared text vs node2vec top-10 for 20 seed incidents
Mean overlap (Jaccard@10): 4.00%

Per-seed overlap:
  #10: 0%
  #100: 0%
  #10005: 0%
  #10016: 0%
  #10019: 10%
  #10021: 10%
  #1003: 10%
  #10044: 0%
  #1005: 0%
  #10064: 0%
```

### GL-22: Find incidents semantically similar to 'worker fell from scaffold due to missing guardrail' using text embeddings.
**Type:** Global | **Status:** ✅ | **Time:** 238.0s

```
Query: "worker fell from scaffold due to missing guardrail"

Top 10 semantically similar incidents:
  #531820 (sim=0.709) Near Miss/sev=? eq=['guardrail', 'Scaffolding'] inj=['risk of fall']
  #709549 (sim=0.656) ?/sev=? eq=['Deck ‘C’', 'Deck ‘A’', 'Guard rails and toeboard'] inj=[]
  #24560 (sim=0.647) Accident/sev=3.0 eq=['Scaffolding', 'scaffold board', 'PPE'] inj=[]
  #24562 (sim=0.647) Accident/sev=3.0 eq=['Scaffolding', 'scaffold board', 'PPE'] inj=[]
  #24563 (sim=0.647) Accident/sev=3.0 eq=['Scaffolding', 'scaffold board', 'PPE'] inj=[]
  #24559 (sim=0.647) Accident/sev=3.0 eq=['Scaffolding', 'scaffold board', 'PPE'] inj=[]
  #709551 (sim=0.638) ?/sev=? eq=['yellow guardrail', 'full scaffold platform'] inj=[]
  #735977 (sim=0.636) ?/sev=? eq=['grinder'] inj=[]
  #518862 (sim=0.636) Near Miss/sev=? eq=['scaffolder', 'ladder steps', 'top handrail'] inj=[]
  #514067 (sim=0.631) Near Miss/sev=? eq=['scaffolder', 'pipe rack 41', 'main deck'] inj=['First Aid Case']
```

### GL-23: Find incidents semantically similar to 'crane load dropped because sling failed under tension' using text embeddings.
**Type:** Global | **Status:** ✅ | **Time:** 0.0s

```
Query: "crane load dropped because sling failed under tension"

Top 10 semantically similar incidents:
  #430 (sim=0.676) Accident/sev=2.0 eq=['CS86', 'slinger', 'crane'] inj=[]
  #552629 (sim=0.666) Near Miss/sev=? eq=['air compressor', 'Eye & eye round slings', 'main lift'] inj=[]
  #697226 (sim=0.663) ?/sev=? eq=['four leg chain sling', 'The Main Crane Hook', 'metallic elongated “O” round sling'] inj=[]
  #703298 (sim=0.663) ?/sev=? eq=['four leg chain sling', 'The Main Crane Hook', 'metallic elongated “O” round sling'] inj=[]
  #725136 (sim=0.662) ?/sev=? eq=['crane', 'transporting slings', 'tested hoisting devices'] inj=[]
  #504414 (sim=0.656) Near Miss/sev=? eq=['The Main Crane Hook'] inj=[]
  #607608 (sim=0.646) Near Miss/sev=? eq=['04 Nos. of “I” Beams', 'OH Gantry Crane', 'trailer'] inj=[]
  #579815 (sim=0.636) Near Miss/sev=? eq=['LIEBHERR LTM 1090-4.1', 'one of the slings', 'slinger'] inj=[]
  #737511 (sim=0.635) ?/sev=? eq=['boom truck', 'slinger', 'truck platform'] inj=[]
  #30460 (sim=0.630) Accident/sev=2.0 eq=['Involved Mobile Crane', 'guide arm', 'slinger'] inj=[]
```

### GL-24: Which equipment types appear most often in the top-10 similar incidents for high-severity events? (embedding-based pattern)
**Type:** Global | **Status:** ✅ | **Time:** 1.0s

```
High-severity incidents sampled: 50
Total high-severity with embeddings: 167

Most common equipment in similar-incident neighborhoods:
  crane: 59
  rigging: 41
  another forklift: 38
  valve: 37
  slinger: 32
  Truck: 28
  deck: 26
  barrier: 25
  hose: 23
  ROV: 19
```

### IOGP-01: What injuries result from incidents involving moving vehicles and mobile equipment?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2857
Distinct INJURY_TYPE values: 198
Top 10:
  pain: 39
  cut: 19
  fracture: 19
  contusion: 18
  personal injury: 16
  laceration: 16
  bruise: 15
  discomfort: 11
  abrasion: 10
  scratch: 10
```

### IOGP-02: How do dropped object incidents break down by severity over time?
**Type:** Aggregation | **Status:** ✅ | **Time:** 3.3s

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
Matching incidents: 675
Sample: ['INCIDENT::10229', 'INCIDENT::10355', 'INCIDENT::10507', 'INCIDENT::10661', 'INCIDENT::10674']
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
  Facilities: 1
  signs ("Under Commissioning" & "High Voltage Do Not Touch"): 1
  All Stop procedure: 1
  check valve 70-NRV-1012: 1
  gasket (which was due to be torqued the following day) failed at the end blind of the 48 inch spool: 1
  no visible damage was found on the Trolley Festoon or any other items: 1

Sample edges (hazard --FAILED_CONTROL--> barrier):
  [16262] deforming the door’s floor latch and breaking the padlock hasp of the LOTO system --> LOTO system | "breaking the padlock hasp of the LOTO system"
  [719499] construction team finish the termination work than put the stick ”cannot close” on the break --> breaker closed without permission | "construction team finish the termination work than put the s"
  [676087] pipes positioned on the line horizontal --> restricted area where personnel are not allowed to enter unless a LOTO is performed | "The area where the pipe fell, was a restricted area where pe"
  [23607] casing damage --> Facilities | "Maintenance barriered the supply off"
  [636840] unlocked panel door (535-EVK-001) --> signs ("Under Commissioning" & "High Voltage Do Not Touch") | "the signs, although sufficient in number and clear in awaren"
  [681052] contact between pipe and manlift --> All Stop procedure | "The spotter called an All Stop as the pipe, but was not hear"
  [565034] wrong direction of installation of the check valve/non-return valve 070-NRV-1012 --> check valve 70-NRV-1012 | "The check valve 70-NRV-1012 wrong direction of installation "
  [654203] LOTO applied by Spiecapag on the valve was not effective, chain and padlock on the hand wheel only and the tag was deteriorated --> gasket (which was due to be torqued the following day) failed at the end blind of the 48 inch spool | "LOTO applied by Spiecapag on the valve was not effective, ch"
  [666246] Trolley Festoon came off from the Trolley Conductor Track --> no visible damage was found on the Trolley Festoon or any other items | "Inspections were carried out by the Workshop Foreman and no "

Top failed controls across all incidents:
  fire: 14
  injuries: 10
  injury: 5
  hand gloves: 5
  hard hat: 4
  IP fell 4m from a ladder: 4
  helmet: 3
  Ordinary safety glasses: 3
  fire extinguisher: 3
  SOPEP equipment: 3
```

### IOGP-06: What body parts are affected in working-at-height incidents with fall protection gaps?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 560
Distinct BODY_PART values: 145
Top 10:
  hand: 19
  left hand: 16
  right hand: 12
  shoulder: 10
  right leg: 9
  left foot: 9
  knee: 7
  right foot: 7
  foot: 7
  leg: 6
```

### IOGP-07: What injuries result from mechanical lifting incidents with rigging failures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2872
Distinct INJURY_TYPE values: 224
Top 10:
  personal injury: 43
  pain: 40
  cut: 33
  fracture: 33
  laceration: 30
  abrasion: 22
  discomfort: 18
  LTI: 17
  contusion: 15
  scratch: 15
```

### IOGP-08: How many machinery and tool incidents resulted in hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 278
Sample: ['INCIDENT::10299', 'INCIDENT::10348', 'INCIDENT::10502', 'INCIDENT::10636', 'INCIDENT::10759']
```

### IOGP-09: What are the top injury types from moving vehicle and mobile equipment incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2857
Distinct INJURY_TYPE values: 198
Top 10:
  pain: 39
  cut: 19
  fracture: 19
  contusion: 18
  personal injury: 16
  laceration: 16
  bruise: 15
  discomfort: 11
  abrasion: 10
  scratch: 10
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
Distinct BODY_PART values: 82
Top 10:
  driver side: 24
  passenger side: 13
  side: 8
  back: 7
  left side: 7
  leg: 4
  head: 4
  front side: 3
  hand: 3
  rear right side: 3
```

### IOGP-12: Which countries have the most mechanical lifting/hoisting incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2872
Distinct LOCATION values: 49
Top 10:
  UK: 1114
  USA: 433
  Brazil: 156
  Norway: 144
  Russia: 105
  Malaysia: 92
  India: 85
  China: 62
  Angola: 46
  France: 38
```

### IOGP-13: What are the top root causes of mechanical lifting incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2872
Distinct ROOT_CAUSE_CATEGORY values: 52
Top 10:
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 409
  Stored energy (dropped objects): 313
  Equipment condition: 256
  Hazard Identification & Risk Assessment: 206
  Planning and coordination of works: 167
  Standard Operating Procedures, Procedures & Work instructions: 157
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 152
  Stored energy (pressure, tension): 143
  Equipment Suitability: 105
  Manual handling: 82
```

### IOGP-14: How many working-at-height incidents involved harnesses or lanyards?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 196
Sample: ['INCIDENT::10671', 'INCIDENT::10929', 'INCIDENT::1193', 'INCIDENT::12554', 'INCIDENT::12923']
```

### IOGP-15: What injury types result from fall-to-lower-level incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1695
Distinct INJURY_TYPE values: 330
Top 10:
  pain: 88
  contusion: 73
  fracture: 45
  closed fracture: 42
  bruise: 40
  sprain: 38
  headache: 27
  swelling: 27
  cut: 26
  laceration: 23
```

### IOGP-16: How do dropped object incidents break down by body part affected?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1160
Distinct BODY_PART values: 147
Top 10:
  hand: 28
  head: 22
  foot: 15
  shoulder: 8
  finger: 8
  left hand: 7
  leg: 6
  left foot: 5
  right foot: 5
  left leg: 4
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
Distinct EQUIPMENT values: 1950
Top 10:
  hose: 80
  valve: 57
  ROV: 54
  crane: 52
  HPU: 43
  rigging: 32
  deck: 32
  barrier: 26
  manifold: 24
  slinger: 22
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
Matching incidents: 559
Distinct INJURY_TYPE values: 100
Top 10:
  contusion: 20
  personal injury: 10
  closed fracture: 9
  laceration: 8
  pain: 7
  Chemical burn: 5
  cut: 4
  bruise: 4
  sprain: 4
  LTI: 4
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
Matching incidents: 471
Distinct BODY_PART values: 157
Top 10:
  left hand: 42
  finger: 26
  right hand: 24
  eye: 14
  hand: 12
  left eye: 12
  thumb: 11
  left leg: 9
  left index finger: 9
  face: 7
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
Distinct EQUIPMENT values: 84
Top 10:
  LOTO: 4
  cable: 2
  feeder: 2
  security post: 1
  overhead crane: 1
  Front G2i: 1
  main power switch: 1
  2 multi core instrument cable: 1
  power cable: 1
  facility electrical panel: 1
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
Distinct EQUIPMENT values: 677
Top 10:
  fire extinguisher: 79
  hose: 25
  air compressor: 14
  welding machine: 12
  torch: 11
  generator: 10
  Scaffolding: 10
  valve: 10
  deck: 9
  scaffolder: 9
```

### IOGP-27: How many incidents mention extreme weather or natural events?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 903
Sample: ['INCIDENT::10173', 'INCIDENT::10178', 'INCIDENT::10232', 'INCIDENT::10239', 'INCIDENT::10240']
```

### IOGP-28: What are the year-over-year trends for vehicle incidents?
**Type:** Aggregation | **Status:** ✅ | **Time:** 0.1s

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
-> With injuries: 3
Equipment in those incidents:
  SDS: 2
  150T crane: 1
  J-401: 1
  main deck: 1
  main hoist winch drum: 1
  boom rest: 1
  piping: 1
  iron pipework: 1
  dewatering skid: 1
  line: 1
```

### MH-02: What injury types are associated with equipment failures during maintenance operations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 29
EQUIPMENT->INJURY_TYPE pairs (top 10):
  hose -> personal injury: 2
  vessel -> personal injury: 2
  Scaffolding -> personal injury: 1
  middle centraliser -> personal injury: 1
  floor level -> personal injury: 1
  needle gun -> finger contusion: 1
  needle gun -> nail injury: 1
  paint scraper -> finger contusion: 1
  paint scraper -> nail injury: 1
  pedestal grinder -> finger contusion: 1
```

### MH-03: Which clients have experienced vessel-related incidents resulting in back injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 62
Distinct ORGANIZATION values: 111
Top 10:
  PETROBRAS: 6
  OCM: 6
  TECHNIPFMC: 6
  WOODSIDE ENERGY LTD.: 6
  Deep orient: 6
  ISOS: 5
  HSE: 5
  TECHNIP MARINE OPERATION SERVICES: 4
  N/A - No Vendor: 4
  Shell: 4
```

### MH-04: What are the most common injury types for each of the top 5 equipment categories?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.2s

```
Top 5 equipment (by incident count):

  crane (1069 incidents):
    personal injury: 18
    fracture: 12
    abrasion: 9
    LTI: 8
    contusion: 7

  another forklift (937 incidents):
    pain: 9
    contusion: 5
    abrasion: 5
    personnel injury: 4
    discomfort: 3

  ROV (847 incidents):
    personal injury: 12
    cut: 9
    pain: 6
    LTI: 4
    swelling: 4

  rigging (678 incidents):
    laceration: 14
    personal injury: 14
    pain: 9
    fracture: 9
    abrasion: 7

  hose (678 incidents):
    personal injury: 13
    cut: 9
    pain: 8
    laceration: 5
    sprain: 4
```

### MH-05: Find incidents where hand injuries occurred during work involving pipes at locations in Asia Pacific.
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 21
Sample: ['INCIDENT::10789', 'INCIDENT::504890', 'INCIDENT::506290', 'INCIDENT::508684', 'INCIDENT::509794']
```

### MH-06: What is the severity distribution of incidents involving trucks compared to those involving cranes?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Severity distribution comparison:

  truck (812 incidents):
    Severity 1: 85
    Severity 2: 102
    Severity 3: 33
    Severity 4: 5
    Severity 5: 1
    Mean severity: 1.83

  crane (1891 incidents):
    Severity 1: 183
    Severity 2: 219
    Severity 3: 114
    Severity 4: 29
    Severity 5: 3
    Mean severity: 2.00
```

### MH-07: Which locations have the highest concentration of near-miss incidents involving scaffolding?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 302
Distinct LOCATION values: 46
Top 10:
  Sabetta: 41
  Aberdeen: 31
  Qidong: 16
  Baku: 13
  Dubai: 13
  Litvinov: 9
  Pontal do Parana: 8
  Newcastle: 6
  Lake Charles: 5
  Penglai: 5
```

### MH-08: Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents.
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.2s

```
Matching incidents: 1
Distinct INJURY_TYPE+INJURY+EVENT values: 2
Top 10:
  oil spray: 1
  leak: 1
```

### MH-09: What eye injuries result from grinder incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 20
Sample: ['INCIDENT::11564', 'INCIDENT::18679', 'INCIDENT::19308', 'INCIDENT::23430', 'INCIDENT::27724']
```

### MH-10: What injuries occur in ladder incidents at construction sites?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 145
Distinct INJURY_TYPE values: 44
Top 10:
  fracture: 7
  bruise: 6
  laceration: 6
  personal injury: 5
  sprain: 5
  pain: 5
  contusion: 4
  discomfort: 4
  abrasion: 3
  swelling: 3
```

### MH-11: What equipment is involved in finger or thumb injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1455
Distinct EQUIPMENT values: 2475
Top 10:
  PPE: 69
  hand gloves: 56
  pipe: 49
  hammer: 47
  rigging: 43
  flange: 39
  crane: 38
  pallet: 32
  valve: 30
  door: 27
```

### MH-12: Which countries have the most crane-related incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1891
Distinct LOCATION values: 47
Top 10:
  UK: 708
  USA: 284
  Norway: 100
  Brazil: 95
  Russia: 80
  India: 69
  Malaysia: 61
  China: 45
  Angola: 32
  Singapore: 29
```

### MH-13: What incidents involve forklifts with foot or leg injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 29
Sample: ['INCIDENT::11886', 'INCIDENT::15610', 'INCIDENT::18921', 'INCIDENT::19826', 'INCIDENT::22001']
```

### MH-14: What equipment is involved in fracture injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 352
Distinct EQUIPMENT values: 748
Top 10:
  x-raying: 43
  crane: 19
  PPE: 19
  air compressor: 16
  pipe: 16
  ladder: 15
  medical ambulance: 15
  slinger: 12
  rigging: 12
  excavator: 11
```

### MH-15: Which body parts are affected in hammer-related incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 221
Distinct BODY_PART values: 111
Top 10:
  finger: 29
  left hand: 24
  right hand: 22
  hand: 14
  thumb: 11
  left index finger: 8
  left thumb: 5
  back: 5
  knee: 5
  right index finger: 5
```

### MH-16: What burn injuries are associated with welding operations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 23
Sample: ['INCIDENT::11142', 'INCIDENT::12111', 'INCIDENT::19154', 'INCIDENT::19275', 'INCIDENT::28012']
```

### MH-17: What incidents involve ROVs in Norway?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 32
Sample: ['INCIDENT::10016', 'INCIDENT::10021', 'INCIDENT::11670', 'INCIDENT::15585', 'INCIDENT::17892']
```

### MH-18: What crane incidents occurred in Brazil?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 95
Sample: ['INCIDENT::10169', 'INCIDENT::11261', 'INCIDENT::11560', 'INCIDENT::13338', 'INCIDENT::14031']
```

### MH-19: What forklift incidents occurred in the UK?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 145
Sample: ['INCIDENT::10170', 'INCIDENT::10333', 'INCIDENT::11665', 'INCIDENT::11848', 'INCIDENT::11875']
```

### MH-20: What scaffold incidents occurred in India?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 74
Sample: ['INCIDENT::501681', 'INCIDENT::501811', 'INCIDENT::502829', 'INCIDENT::503175', 'INCIDENT::503649']
```

### MH-21: What injury types result from high-severity crane incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 32
Distinct INJURY_TYPE values: 4
Top 10:
  potential shoulder injury: 1
  personal injury: 1
  pinch point injury: 1
  amputation: 1
```

### MH-22: What equipment is involved in incidents at Aberdeen?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 2499
Distinct EQUIPMENT values: 6828
Top 10:
  ROV: 532
  crane: 360
  rigging: 349
  deck: 323
  vessel: 241
  main deck: 223
  hose: 208
  barrier: 161
  valve: 112
  PPE: 94
```

### MH-23: What sling incidents involved hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 37
Sample: ['INCIDENT::16611', 'INCIDENT::18519', 'INCIDENT::18552', 'INCIDENT::20555', 'INCIDENT::21894']
```

### MH-24: What are the injury types from construction incidents resulting in fractures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 218
Sample: ['INCIDENT::13286', 'INCIDENT::14265', 'INCIDENT::14990', 'INCIDENT::16634', 'INCIDENT::19923']
```

### MH-25: What finger or thumb injuries involve fractures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 114
Sample: ['INCIDENT::11707', 'INCIDENT::12373', 'INCIDENT::13832', 'INCIDENT::14068', 'INCIDENT::14265']
```

### MH-26: What back injuries are associated with manual handling root causes?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 96
Sample: ['INCIDENT::10371', 'INCIDENT::10797', 'INCIDENT::11066', 'INCIDENT::12298', 'INCIDENT::14291']
```

### MH-27: What crane incidents occurred during 2019?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 3.1s

```
Matching incidents: 208
Sample: ['INCIDENT::22601', 'INCIDENT::620267', 'INCIDENT::621312', 'INCIDENT::621368', 'INCIDENT::621392']
```

### MH-28: What forklift incidents occurred during 2023?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 3.1s

```
Matching incidents: 119
Sample: ['INCIDENT::12422', 'INCIDENT::12484', 'INCIDENT::12495', 'INCIDENT::12535', 'INCIDENT::12642']
```

### MH-29: What scaffold incidents occurred during 2020?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 3.2s

```
Matching incidents: 78
Sample: ['INCIDENT::665507', 'INCIDENT::666570', 'INCIDENT::666736', 'INCIDENT::666891', 'INCIDENT::667301']
```

### MH-30: What ROV incidents occurred during 2017?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 3.1s

```
Matching incidents: 126
Sample: ['INCIDENT::521157', 'INCIDENT::522333', 'INCIDENT::523047', 'INCIDENT::524382', 'INCIDENT::524422']
```

### MH-31: What injuries result from fall/slip RCC incidents with fractures?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 110
Sample: ['INCIDENT::13256', 'INCIDENT::19923', 'INCIDENT::20793', 'INCIDENT::27374', 'INCIDENT::27508']
```

### MH-32: What equipment is involved in incidents at Houston?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1358
Distinct EQUIPMENT values: 1827
Top 10:
  another forklift: 134
  crane: 83
  pallet: 68
  ROV: 59
  hose: 47
  HPU: 40
  valve: 36
  Truck: 30
  slinger: 30
  rigging: 27
```

### MH-33: What body parts are affected in incidents reported by YAMAL LNG?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1302
Distinct BODY_PART values: 304
Top 10:
  right hand: 87
  left hand: 81
  finger: 42
  right foot: 37
  right ankle: 29
  eye: 29
  hand: 28
  left foot: 27
  left ankle: 22
  left leg: 19
```

### MH-34: What injuries result from incidents at Rio de Janeiro?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 897
Distinct INJURY_TYPE values: 82
Top 10:
  cut: 33
  pain: 9
  surface cut: 8
  abrasion: 7
  electric shock: 5
  irritation: 5
  edema: 5
  paralyzed: 4
  injured: 4
  break: 3
```

### MH-35: What incidents involve grinders with hand or finger injuries?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 63
Sample: ['INCIDENT::10299', 'INCIDENT::10636', 'INCIDENT::11972', 'INCIDENT::13662', 'INCIDENT::15690']
```

### MH-36: What equipment is involved in incidents reported by PETROBRAS?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 676
Distinct EQUIPMENT values: 1420
Top 10:
  ROV: 86
  crane: 41
  hose: 32
  main deck: 30
  rigging: 29
  deck: 28
  HPU: 18
  valve: 17
  Work Table: 17
  barrier: 17
```

### MH-37: What are the top injury types in incidents at Le Trait?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1135
Distinct INJURY_TYPE values: 79
Top 10:
  pain: 113
  back pain: 15
  cut: 12
  discomfort: 9
  shock: 8
  scratch: 5
  injured: 5
  fracture: 4
  foreign body: 3
  swelling: 3
```

### MH-38: What equipment is involved in near-miss incidents at offshore locations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.1s

```
Matching incidents: 141
Distinct EQUIPMENT values: 478
Top 10:
  rigging: 26
  ROV: 25
  crane: 21
  main deck: 14
  HPU: 11
  deck: 10
  hose: 10
  barrier: 8
  vessel: 7
  reel: 6
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
Matching incidents: 209
Distinct BODY_PART values: 52
Top 10:
  left leg: 3
  right foot: 3
  left ankle: 2
  hand: 2
  arm: 2
  ankle: 2
  right ankle: 2
  left foot: 2
  head: 2
  leg: 2
```

### MH-41: What injury types result from incidents involving pallets?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 579
Distinct INJURY_TYPE values: 80
Top 10:
  pain: 17
  cut: 15
  laceration: 6
  contusion: 5
  bruise: 5
  scratch: 4
  fracture: 4
  discomfort: 4
  sharp pain: 4
  RWC: 3
```

### MH-42: What injuries result from incidents involving pipes at offshore locations?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 19
Distinct INJURY_TYPE values: 7
Top 10:
  pain: 2
  superficial surface laceration: 1
  personal injury: 1
  muscle bruise: 1
  swollen knee: 1
  skin irritation: 1
  burn: 1
```

### MH-43: What equipment is involved in red-risk incidents?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 52
Distinct EQUIPMENT values: 174
Top 10:
  flange: 5
  barrier: 5
  valve: 4
  tubing hanger: 3
  rig floor: 3
  crane: 3
  another forklift: 3
  BOP: 2
  Hanger: 2
  accumulator: 2
```

### MH-44: What are the root causes of incidents at Sabetta (Yamal LNG site)?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 880
Distinct ROOT_CAUSE_CATEGORY values: 41
Top 10:
  Falls, slips and trips on same level (without potential to fall to lower level): 264
  Manual handling: 77
  Fall to lower level / fall to water / loose materials (e.g. silos with granulate): 54
  Hazard Identification & Risk Assessment: 54
  Traffic Management / Routes / Pedestrian path: 45
  Uncontrolled chemical or physical reaction: 42
  Uncontrolled moving objects/ parts (struck by other than machine parts and dropped objects): 39
  Stored energy (dropped objects): 39
  Inadequate Supervision: 31
  Hazardous liquids (exposure to / spill / loss of containment /pollution): 27
```

### MH-45: What injury types are connected to crane equipment via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 642 EQUIPMENT nodes matching 'crane'
  --INVOLVED--> INCIDENT: 1891 nodes
  --RESULTED_IN--> INJURY_TYPE: 141 nodes
  Final: 141 INJURY_TYPE nodes, 141 distinct values

Top 10:
  first degree burn: 1
  lower back pain: 1
  Multiple open fractures: 1
  twinge: 1
  difficulty in moving the eye or discomfort: 1
  pinch laceration: 1
  main injury: 1
  risk of injury: 1
  Chemical burn: 1
  sharp pain: 1
```

### MH-46: What equipment is connected to fracture injuries via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 289 INJURY_TYPE nodes matching 'fracture'
  --RESULTED_IN--> INCIDENT: 352 nodes
  --INVOLVED--> EQUIPMENT: 748 nodes
  Final: 748 EQUIPMENT nodes, 748 distinct values

Top 10:
  crew bus parking area: 1
  flowline: 1
  man lift “HYUNDAY”: 1
  crew bus stop: 1
  MEWP: 1
  tank: 1
  impact protection gloves: 1
  channel bar: 1
  first aid box: 1
  concrete slabs: 1
```

### MH-47: What body parts are connected to forklift equipment via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 145 EQUIPMENT nodes matching 'forklift'
  --INVOLVED--> INCIDENT: 1110 nodes
  --AFFECTED--> BODY_PART: 109 nodes
  Final: 109 BODY_PART nodes, 109 distinct values

Top 10:
  neck: 1
  left back part: 1
  left-hand ring finger: 1
  fingers of the right hand: 1
  side: 1
  pup joint: 1
  right pinky finger: 1
  left knee: 1
  upper swing arm: 1
  shear point body: 1
```

### MH-48: What root causes are connected to hand injuries via graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 193 BODY_PART nodes matching 'hand'
  --AFFECTED--> INCIDENT: 1411 nodes
  --CATEGORIZED_AS--> ROOT_CAUSE_CATEGORY: 50 nodes
  Final: 50 ROOT_CAUSE_CATEGORY nodes, 50 distinct values

Top 10:
  Stored energy (pressure, tension): 1
  Traffic Management / Routes / Pedestrian path: 1
  Stored energy (dropped objects): 1
  Biological - Animals, Bacteria, Viruses and Funguses: 1
  Psycho social - Workload (Overload/Underload): 1
  Use of personal protective equipment: 1
  Access/Egress: 1
  Tool suitability: 1
  Uncontrolled chemical or physical reaction: 1
  Pinch point: 1
```

### MH-49: What locations have crane equipment via 2-hop graph traversal?
**Type:** Multi-hop | **Status:** ✅ | **Time:** 0.0s

```
Start: 642 EQUIPMENT nodes matching 'crane'
  --INVOLVED--> INCIDENT: 1891 nodes
  --OCCURRED_AT--> LOCATION: 2039 nodes
  Final: 2039 LOCATION nodes, 1987 distinct values

Top 10:
  Singapore: 3
  Malaysia: 2
  France: 2
  Dubai: 2
  Tananger: 2
  Johor Bahru: 2
  Houston: 2
  Aberdeen: 2
  Lysaker: 2
  Orkanger: 2
```

### SC-01: In incident #623703, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::623703: ['another forklift', 'manifold', 'mirror']
Ground truth: ['forklift', 'manifold', 'mirror']
Missing: none
Extra (unexpected): none
```

### SC-02: In incident #570187, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::570187: ['Connector link', 'EPMCC panel', 'electric heater feeder breaker', 'within feeder box']
Ground truth: ['connector link', 'electric heater feeder breaker', 'feeder breaker']
Missing: none
Extra (unexpected): ['epmcc panel', 'within feeder box']
```

### SC-03: In incident #602346, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::602346: ['PGB', 'another forklift']
Ground truth: ['forklift', 'pgb']
Missing: none
Extra (unexpected): none
```

### SC-04: In incident #14338, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::14338: ['large mold', 'mold', 'press']
Ground truth: ['press']
Missing: none
Extra (unexpected): ['large mold', 'mold']
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
EQUIPMENT found for INCIDENT::500389: ['ROV', 'TMS’s', 'football float', 'marker buoys', 'odom weight', 'odom weight with chain', 'polyrope', 'vessel']
Ground truth: ['chain', 'football float', 'marker buoys', 'odom weight', 'tms']
Missing: none
Extra (unexpected): ['polyrope', 'rov', 'vessel']
```

### SC-06: In incident #8712, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::8712: ['barrier']
Ground truth: []
Missing: none
Extra (unexpected): ['barrier']
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
EQUIPMENT found for INCIDENT::511771: ['The Main Crane Hook', 'helmet', 'wire rope sling']
Ground truth: ['crane hook', 'wire rope sling']
Missing: none
Extra (unexpected): ['helmet']
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
EQUIPMENT found for INCIDENT::324: ['20T Forklift', 'another forklift']
Ground truth: ['20t forklift']
Missing: none
Extra (unexpected): ['another forklift']
```

### SC-09: In incident #18312, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::18312: ['crane']
Ground truth: ['crane', 'plastic sun visor']
Missing: ['plastic sun visor']
Extra (unexpected): none
```

### SC-09b: In incident #18312, which body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::18312: ['head', 'top of his head']
Ground truth: ['head']
Missing: none
Extra (unexpected): none
```

### SC-10: In incident #644762, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::644762: ['19 reels', 'Helicopter', 'PPE', 'ancillary pipelay equipment', 'crane', 'deck winch', 'his steel toe cap boots', 'main lift shackle', 'rigging', 'tri-plate']
Ground truth: ['crane', 'deck winch', 'main lift shackle', 'ppe', 'reel', 'tri-plate']
Missing: none
Extra (unexpected): ['ancillary pipelay equipment', 'helicopter', 'his steel toe cap boots', 'rigging']
```

### SC-11: In incident #505133, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::505133: ['Billy Pugh', 'Deck F', 'G1200', 'G1200 AB', 'Helicopter', 'Surfer Landing Platform', 'Surfer S 226', 'engine', 'ladder', 'platform', 'rope', 'splint', 'stretcher']
Ground truth: ['billy pugh', 'helicopter', 'ladder', 'splint', 'stretcher', 'surfer']
Missing: none
Extra (unexpected): ['deck f', 'engine', 'g1200', 'g1200 ab', 'platform', 'rope']
```

### SC-12: In incident #645871, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::645871: ['arm', 'back', 'eye']
Ground truth: ['arm', 'eye']
Missing: none
Extra (unexpected): ['back']
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
EQUIPMENT found for INCIDENT::569346: ['Load. Moment Indicator', 'Superior CPX-94', 'boom block wire rope', 'cable', 'ladder', 'sideboom']
Ground truth: ['hydraulic converted cat 594', 'ladder', 'load. moment indicator', 'sideboom', 'superior cpx-94']
Missing: ['hydraulic converted cat 594']
Extra (unexpected): ['boom block wire rope', 'cable']
```

### SC-15: In incident #569346, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::569346: ['chin', 'jaw', 'knee', 'lip', 'lower lip']
Ground truth: ['chin', 'jaw', 'lip']
Missing: none
Extra (unexpected): ['knee']
```

### SC-16: In incident #569346, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::569346: ['laceration']
Ground truth: ['laceration', 'three broken teeth']
Missing: ['three broken teeth']
Extra (unexpected): none
```

### SC-17: In incident #685931, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::685931: ['A steel Rack', 'The waste rack lid', 'bulker bags', 'ice compression pack', 'impact protection gloves', 'lid', 'locking bar', 'new bulker bag', 'safety helmet', 'securing arm', 'splint and bandage', 'steel lid']
Ground truth: ['bulker bags', 'ice compression pack', 'locking bar', 'splint and bandage', 'steel lid', 'steel rack', 'waste rack lid']
Missing: none
Extra (unexpected): ['impact protection gloves', 'new bulker bag', 'safety helmet', 'securing arm']
```

### SC-18: In incident #632796, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::632796: ['AQA Wellhead platform', 'Deck Workshop', 'HDA2006 224tn Hydraulic Jack', 'crew boat', 'hose', 'hydraulic jack', 'telephone', 'water guard']
Ground truth: ['cabin telephone', 'hydraulic hose', 'hydraulic jack', 'water guard']
Missing: none
Extra (unexpected): ['aqa wellhead platform', 'crew boat', 'deck workshop']
```

### SC-19: In incident #632796, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::632796: ['back', 'lower back area', 'lower side']
Ground truth: ['back', 'lower back']
Missing: none
Extra (unexpected): ['lower side']
```

### SC-20: In incident #611828, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::611828: ['EN388', 'PPE', 'block', 'glasses', 'rigging', 'safety helmet', 'sheeve', 'sideboom', 'slinger', 'the moving block part']
Ground truth: ['block', 'glasses', 'moving block', 'ppe', 'safety helmet', 'sideboom', 'sling']
Missing: none
Extra (unexpected): ['en388', 'rigging', 'sheeve']
```

### SC-21: In incident #563945, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::563945: ['Ice pack', 'PWT', 'davit', 'emergency lowering arm', 'harness', 'main deck', 'platform', 'vessel hospital', 'vessel lifeboats', 'welding workshop']
Ground truth: ['davit', 'ice pack', 'lifeboats']
Missing: none
Extra (unexpected): ['emergency lowering arm', 'harness', 'main deck', 'platform', 'pwt', 'vessel hospital', 'welding workshop']
```

### SC-22: In incident #564230, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::564230: ['bruising on the brain', 'contusion', 'headache', 'nausea', 'neck pain', 'whiplash']
Ground truth: ['contusion', 'dizziness', 'headache', 'nausea']
Missing: ['dizziness']
Extra (unexpected): ['bruising on the brain', 'neck pain', 'whiplash']
```

### SC-23: In incident #696119, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::696119: ['Cerebral Hematoma', 'Right eye wound', 'hematoma']
Ground truth: ['cerebral hematoma', 'crack left pelvis', 'dislocate left shoulder', 'hematoma', 'right eye wound']
Missing: ['crack left pelvis', 'dislocate left shoulder']
Extra (unexpected): none
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
INJURY_TYPE found for INCIDENT::702644: ['bruising', 'fracture', 'superficial skin abrasion', 'swelling']
Ground truth: ['breaks/fractures', 'bruising', 'skin abrasion', 'soft tissue damage']
Missing: ['soft tissue damage']
Extra (unexpected): ['swelling']
```

### SC-26: In incident #16468, what locations were recorded?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
LOCATION found for INCIDENT::16468: ['1st level platforms', 'Aberdeen', 'Bridge', 'DEEP ORIENT', 'De -watering spread', 'Deep Orient', 'Duty Mess', 'Europe', 'Karish North', 'Larnaca base', 'Limassol', 'Limassol base', 'Mediterranean hospital', 'North Quay', 'UK', 'mess room', 'quayside', 'work site']
Ground truth: ['aberdeen', 'deep orient', 'europe', 'uk']
Missing: none
Extra (unexpected): ['1st level platforms', 'bridge', 'de -watering spread', 'duty mess', 'karish north', 'larnaca base', 'limassol', 'limassol base', 'mediterranean hospital', 'mess room', 'north quay', 'quayside', 'work site']
```

### SC-27: In incident #546948, what locations were recorded?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
LOCATION found for INCIDENT::546948: ['Doha', 'Doha Service Base', 'Middle East', 'PQ1-Q accommodation', 'PS1-A', 'PS1-C', 'PS1-G', 'PS1-G control room', 'PS1-Q', 'PS1G', 'PS1Q', 'Qatar', 'accommodation', 'control room', 'medical facilities']
Ground truth: ['doha', 'middle east', 'qatar']
Missing: none
Extra (unexpected): ['accommodation', 'control room', 'medical facilities', 'pq1-q accommodation', 'ps1-a', 'ps1-c', 'ps1-g', 'ps1-g control room', 'ps1-q', 'ps1g', 'ps1q']
```

### SC-28: In incident #555852, what organizations were recorded?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
ORGANIZATION found for INCIDENT::555852: ['Communications and project', 'ERTL', 'KVA', 'Operasjonsleder Haugesund Police', 'Police Security Service (PST)', 'Project management', 'QHSE Management', 'Regional Police', 'STATOIL ASA', 'Stakeholders', 'TECHNIPFMC', 'TPFMC Control', 'TechnipFMC ERTL', 'TechnipFMC Management', 'TechnipFMC Norway', 'local police']
Ground truth: ['ertl', 'kva', 'project management', 'statoil asa', 'technipfmc']
Missing: none
Extra (unexpected): ['communications and project', 'local police', 'operasjonsleder haugesund police', 'police security service (pst)', 'qhse management', 'regional police', 'stakeholders', 'tpfmc control']
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
EQUIPMENT found for INCIDENT::563298: ['PPE', 'Steri strips', 'Truck', 'bandage', 'light 4x4 truck', 'rigging', 'skid', 'truck platform', 'x-raying']
Ground truth: ['light 4x4 truck', 'skid', 'truck platform']
Missing: none
Extra (unexpected): ['bandage', 'ppe', 'rigging', 'steri strips', 'x-raying']
```

### SC-32: In incident #507347, what body parts were affected?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
BODY_PART found for INCIDENT::507347: ['knee', 'leg', 'right knee']
Ground truth: ['knee', 'leg', 'right knee']
Missing: none
Extra (unexpected): none
```

### SC-33: In incident #507347, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::507347: ['Full Leg Vacuum splint', 'Hi level flood lighting', 'ROV', 'ROV XLX 85 & TMS', 'ROV XLX94', 'ROV hanger', 'TMS’s', 'Yokohama type fenders', 'bollard', 'crutches', 'medical ambulance', 'pallet', 'rigging', 'vessel']
Ground truth: ['crutches', 'rov xlx 85', 'yokohama fender']
Missing: ['yokohama fender']
Extra (unexpected): ['bollard', 'full leg vacuum splint', 'hi level flood lighting', 'medical ambulance', 'pallet', 'rigging', 'rov hanger', 'rov xlx94', 'tms’s', 'vessel', 'yokohama type fenders']
```

### SC-34: In incident #19018, what equipment was involved?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::19018: ['CCTV', 'HUB', 'MCV', 'MCV-U', 'ROV', 'Spare SA blind stab', 'Umbilical 9F UEH SDU-3', 'VCM', 'camera', 'crane', 'slinger', 'u-VCM', 'umbilical', 'wet Christmas tree']
Ground truth: ['crane', 'mcv-u', 'mvc', 'rov', 'u-vcm']
Missing: ['mvc']
Extra (unexpected): ['camera', 'cctv', 'hub', 'slinger', 'spare sa blind stab', 'umbilical', 'umbilical 9f ueh sdu-3', 'wet christmas tree']
```

### SC-35: In incident #664483, what injury types resulted?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
INJURY_TYPE found for INCIDENT::664483: ['dislocated', 'dislocation and fracture', 'fracture']
Ground truth: ['dislocated', 'dislocation and fracture', 'fracture']
Missing: none
Extra (unexpected): none
```

### SH-01: What incidents involved forklifts in 2022?
**Type:** Single-hop | **Status:** ✅ | **Time:** 3.1s

```
Matching incidents: 85
Sample: ['INCIDENT::10170', 'INCIDENT::10233', 'INCIDENT::10252', 'INCIDENT::10333', 'INCIDENT::1061']
```

### SH-02: What equipment was involved in incident #29857?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
EQUIPMENT found for INCIDENT::29857: ['Pry Bar', 'ROV', 'TMS’s', 'lanyard']
Ground truth: ['lanyard', 'pry bar', 'rov', 'tms']
Missing: none
Extra (unexpected): none
```

### SH-03: What body parts were affected in crane-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1891
Distinct BODY_PART values: 255
Top 10:
  finger: 37
  head: 25
  left hand: 21
  right hand: 20
  left foot: 17
  leg: 16
  lower back: 12
  hand: 11
  back: 10
  right foot: 9
```

### SH-04: Which locations reported valve-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1149
Distinct LOCATION values: 45
Top 10:
  USA: 414
  UK: 252
  Norway: 53
  Brazil: 44
  Argentina: 37
  Canada: 35
  France: 30
  China: 26
  India: 23
  Malaysia: 20
```

### SH-05: What types of injuries resulted from incidents at offshore installations?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1120
Distinct INJURY_TYPE values: 175
Top 10:
  personal injury: 42
  pain: 33
  cut: 31
  laceration: 17
  swelling: 14
  discomfort: 11
  abrasion: 11
  bruising: 10
  FAC: 10
  burn: 6
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
Matching incidents: 306
Sample: ['INCIDENT::10349', 'INCIDENT::10671', 'INCIDENT::10854', 'INCIDENT::12594', 'INCIDENT::12713']
```

### SH-08: What incidents involved grinders?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 233
Sample: ['INCIDENT::10021', 'INCIDENT::10299', 'INCIDENT::10318', 'INCIDENT::10636', 'INCIDENT::11470']
```

### SH-09: What incidents involved hoses?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1122
Sample: ['INCIDENT::10224', 'INCIDENT::10234', 'INCIDENT::10296', 'INCIDENT::10504', 'INCIDENT::10507']
```

### SH-10: What incidents involved pumps?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 418
Sample: ['INCIDENT::10229', 'INCIDENT::10234', 'INCIDENT::10375', 'INCIDENT::1073', 'INCIDENT::10923']
```

### SH-11: What incidents involved ROVs?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 849
Sample: ['INCIDENT::100', 'INCIDENT::10016', 'INCIDENT::10021', 'INCIDENT::1011', 'INCIDENT::10231']
```

### SH-12: What incidents involved excavators?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 209
Sample: ['INCIDENT::12002', 'INCIDENT::1355', 'INCIDENT::16228', 'INCIDENT::16786', 'INCIDENT::18144']
```

### SH-13: What incidents involved PPE (helmets/gloves/safety glasses)?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1148
Sample: ['INCIDENT::10005', 'INCIDENT::10165', 'INCIDENT::10290', 'INCIDENT::10299', 'INCIDENT::10333']
```

### SH-14: What incidents involved slings?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 555
Sample: ['INCIDENT::10232', 'INCIDENT::10252', 'INCIDENT::10838', 'INCIDENT::10882', 'INCIDENT::11365']
```

### SH-15: What incidents involved compressors?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 379
Sample: ['INCIDENT::10171', 'INCIDENT::10504', 'INCIDENT::11948', 'INCIDENT::12064', 'INCIDENT::12831']
```

### SH-16: What incidents involved winches?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 415
Sample: ['INCIDENT::10428', 'INCIDENT::10507', 'INCIDENT::10541', 'INCIDENT::10786', 'INCIDENT::11261']
```

### SH-17: What body parts were affected in hose-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 1122
Distinct BODY_PART values: 166
Top 10:
  face: 25
  finger: 13
  eye: 13
  left hand: 10
  head: 9
  back: 8
  hand: 7
  right hand: 7
  leg: 7
  right eye: 6
```

### SH-18: What injury types resulted from pump-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 418
Distinct INJURY_TYPE values: 42
Top 10:
  cut: 9
  pain: 8
  personal injury: 8
  burn: 5
  fracture: 3
  laceration: 2
  irritation: 2
  discomfort: 2
  contusion: 2
  deformity: 1
```

### SH-19: Which organizations reported excavator-related incidents?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 209
Distinct ORGANIZATION values: 308
Top 10:
  TRANS ADRIATIC PIPELINE AG: 76
  PETRONAS: 17
  CTR: 15
  THE BAHRAIN PETROLEUM COMPANY BSC: 14
  SASOL NORTH AMERICA, INC.: 12
  JSC YAMAL LNG: 9
  EXXONMOBIL: 8
  SPIECAPAG: 8
  CPY: 8
  TAP: 8
```

### SH-20: What incidents involved welding equipment?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 339
Sample: ['INCIDENT::10172', 'INCIDENT::10206', 'INCIDENT::10598', 'INCIDENT::11142', 'INCIDENT::11528']
```

### SH-21: What incidents involved pallets?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 579
Sample: ['INCIDENT::1037', 'INCIDENT::10535', 'INCIDENT::10759', 'INCIDENT::10882', 'INCIDENT::11027']
```

### SH-22: What incidents involved fire extinguishers?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 243
Sample: ['INCIDENT::10176', 'INCIDENT::10248', 'INCIDENT::10504', 'INCIDENT::1067', 'INCIDENT::1068']
```

### SH-23: What incidents involved reels?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 435
Sample: ['INCIDENT::10165', 'INCIDENT::10173', 'INCIDENT::10197', 'INCIDENT::10296', 'INCIDENT::10980']
```

### SH-24: What incidents involved umbilicals?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 177
Sample: ['INCIDENT::10757', 'INCIDENT::11112', 'INCIDENT::11906', 'INCIDENT::11986', 'INCIDENT::1265']
```

### SH-25: What incidents affected the left hand?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 503
Sample: ['INCIDENT::10598', 'INCIDENT::10636', 'INCIDENT::10680', 'INCIDENT::10943', 'INCIDENT::11027']
```

### SH-26: What incidents affected the thumb?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 273
Sample: ['INCIDENT::10348', 'INCIDENT::10702', 'INCIDENT::10881', 'INCIDENT::10943', 'INCIDENT::110']
```

### SH-27: What incidents resulted in contusions or bruises?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 510
Sample: ['INCIDENT::1057', 'INCIDENT::10689', 'INCIDENT::10789', 'INCIDENT::11583', 'INCIDENT::11727']
```

### SH-28: What incidents resulted in sprains or strains?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 212
Sample: ['INCIDENT::12110', 'INCIDENT::13153', 'INCIDENT::13589', 'INCIDENT::13665', 'INCIDENT::1408']
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
Matching incidents: 114
Sample: ['INCIDENT::10146', 'INCIDENT::103', 'INCIDENT::11655', 'INCIDENT::12923', 'INCIDENT::13299']
```

### SH-35: How many incidents mention fatigue as a factor?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 35
Sample: ['INCIDENT::10671', 'INCIDENT::12483', 'INCIDENT::12687', 'INCIDENT::21772', 'INCIDENT::28625']
```

### SH-36: How many incidents involve H2S or hydrogen sulfide?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

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
Matching incidents: 51
Sample: ['INCIDENT::1288', 'INCIDENT::15422', 'INCIDENT::184', 'INCIDENT::19918', 'INCIDENT::19923']
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
Matching incidents: 402
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
Matching incidents: 1135
Sample: ['INCIDENT::10141', 'INCIDENT::10178', 'INCIDENT::10185', 'INCIDENT::10225', 'INCIDENT::10281']
```

### SH-50: What incidents resulted in abrasions or scratches?
**Type:** Single-hop | **Status:** ✅ | **Time:** 0.0s

```
Matching incidents: 329
Sample: ['INCIDENT::10333', 'INCIDENT::10345', 'INCIDENT::10379', 'INCIDENT::10428', 'INCIDENT::10812']
```

### SH-51: What incidents occurred in 2024?
**Type:** Single-hop | **Status:** ✅ | **Time:** 3.0s

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
Matching incidents: 13
Sample: ['INCIDENT::17567', 'INCIDENT::29152', 'INCIDENT::29469', 'INCIDENT::29471', 'INCIDENT::29472']
```

### SH-56: What incidents occurred before 2016?
**Type:** Single-hop | **Status:** ✅ | **Time:** 3.1s

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
Matching incidents: 261
Sample: ['INCIDENT::10234', 'INCIDENT::10992', 'INCIDENT::11132', 'INCIDENT::11662', 'INCIDENT::12265']
```

## 4. Regression Diff (vs previous run)

No regressions — all results stable.

---
*Generated by pipeline/benchmark/run_benchmark.py*
