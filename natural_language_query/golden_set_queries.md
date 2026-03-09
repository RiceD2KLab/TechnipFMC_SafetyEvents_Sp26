# Golden Set Query Suite (Dashboard NLQ)

This document captures the canonical "golden set" of natural language queries
for validating `natural_language_query` coverage across the major analyst
question types in the TechnipFMC safety context.

## Purpose

- Validate NL -> structured query translation quality against realistic asks.
- Ensure coverage across retrieval, aggregation, multi-hop, global, and
  conjunctive query types.
- Use as the baseline reference for repeatable NLQ regression testing.

## Query Families

- Single-Hop Queries: 6
- Aggregation Queries: 6
- Multi-Hop Queries: 8
- Global Queries: 4
- Conjunctive Queries: 6

Total: 30 queries

---

## Single-Hop Queries (6)

### SH-01
- **Query:** What incidents involved forklifts in 2022?
- **Traversal:** [Equipment: FORKLIFT] <- involved <- [Incident] -> occurred_on -> [Date: 2022]
- **Tests:** ER (7 forklift surface forms) + temporal metadata integration
- **Data Density:** ~1,330 forklift records (5.7%); REPORTED_DATE available for year filtering
- **Expected Answer:** List of incident IDs with forklift involvement in 2022
- **Why This Query:** Forklift has 7 known surface variants (forklift, fork lift, fork-lift, FLT, 20T forklift, etc.); count directly measures ER effectiveness.

### SH-02
- **Query:** What equipment was involved in incident #29857?
- **Traversal:** [Incident: 29857] -> involved -> [Equipment]
- **Tests:** L1 entity extraction for a specific known record
- **Data Density:** Single record (pry bar/ROV example)
- **Expected Answer:** Equipment list: PRY BAR, ROV, TMS, LANYARD
- **Why This Query:** Directly verifiable known-ground-truth spot check.

### SH-03
- **Query:** What body parts were affected in crane-related incidents?
- **Traversal:** [Equipment: CRANE] <- involved <- [Incident] -> affected -> [Body Part]
- **Tests:** L1 co-extraction of Equipment + Body Part; ER on crane (8 variants)
- **Data Density:** crane x back: 475 co-occurrences; crane total: 2,309 records (9.9%)
- **Expected Answer:** Ranked list of body parts for crane incidents
- **Why This Query:** High-frequency + high-fragmentation entity; checks cross-entity linkage.

### SH-04
- **Query:** Which locations reported valve-related incidents?
- **Traversal:** [Equipment: VALVE] <- involved <- [Incident] -> occurred_at -> [Location]
- **Tests:** ER (valve has 9 forms) + location metadata integration
- **Data Density:** ~1,236 valve records (5.3%); WORKPLACE at 100% coverage
- **Expected Answer:** Countries/cities with valve incident counts
- **Why This Query:** High-fragmentation ER stress test with deterministic location dimension.

### SH-05
- **Query:** What types of injuries resulted from incidents at offshore installations?
- **Traversal:** [Location: OFFSHORE] <- occurred_at <- [Incident] -> resulted_in -> [Injury Type]
- **Tests:** META (WORK_PROCESS "Offshore Installation") linked to injury extraction
- **Data Density:** WORK_PROCESS at 88.2% coverage; offshore is a major category
- **Expected Answer:** Injury types ranked by frequency at offshore sites
- **Why This Query:** Core sponsor context; tests metadata-to-NER integration.

### SH-06
- **Query:** What incidents were reported by client SHELL OFFSHORE INC.?
- **Traversal:** [Organization: SHELL OFFSHORE INC.] <- associated_with <- [Incident]
- **Tests:** CLIENT metadata integration + organization ER
- **Data Density:** CLIENT at 97.9% coverage
- **Expected Answer:** List of incident IDs associated with Shell
- **Why This Query:** Organization integration and naming/abbreviation robustness.

---

## Aggregation Queries (6)

### AG-01
- **Query:** What are the most common root causes of dropped object incidents?
- **Traversal:** Filter incidents with action "dropped" -> aggregate [Incident] -> caused_by -> [Root Cause] -> rank by frequency
- **Tests:** L1 action extraction + L2 causal edges + aggregation over CASE_CATEGORIZATION
- **Data Density:** "dropped" is #2 action term; CASE_CATEGORIZATION at 91.9%
- **Expected Answer:** Top-N root causes for dropped-object incidents
- **Why This Query:** Real analyst workflow around recurring dropped-object events.

### AG-02
- **Query:** Which countries have the highest rate of high-severity incidents?
- **Traversal:** [Incident] -> occurred_at -> [Location: COUNTRY] + [Incident] -> has_severity -> [Severity >= 4] -> group by country -> rank
- **Tests:** META integration (WORKPLACE + SEVERITY) + aggregation
- **Data Density:** WORKPLACE 100%, SEVERITY 99.1%
- **Expected Answer:** Countries ranked by severity 4-5 counts/rates
- **Why This Query:** Core safety-management ask combining two metadata dimensions.

### AG-03
- **Query:** What equipment types are involved in the most incidents overall?
- **Traversal:** [Incident] -> involved -> [Equipment] -> group by equipment type -> rank
- **Tests:** L1 completeness + ER merged counts + aggregation
- **Data Density:** vessel 11.2%, crane 9.9%, pipe 9.2%, truck 7.4%, forklift 5.7%, valve 5.3%
- **Expected Answer:** Equipment ranking aligned to known entity landscape
- **Why This Query:** Fundamental aggregate sanity check for extraction + ER.

### AG-04
- **Query:** How do incidents break down by type (accident vs. near miss) across business units?
- **Traversal:** [Incident] -> is_type -> [Incident Type] + [Incident] -> part_of -> [Organization: GBU] -> crosstab
- **Tests:** META integration (INCIDENT_TYPE x GENERAL_BUSINESS_UNIT) + sparse-field handling
- **Data Density:** INCIDENT_TYPE 70.9%; GENERAL_BUSINESS_UNIT 24.9%
- **Expected Answer:** Crosstab or explicit insufficient-data acknowledgment
- **Why This Query:** Deliberate missing-data stress case.

### AG-05
- **Query:** What is the monthly trend of fall/slip incidents over the past 3 years?
- **Traversal:** Filter CASE_CATEGORIZATION to Falls & Slips -> group by month/year -> count
- **Tests:** CASE_CATEGORIZATION + temporal aggregation
- **Data Density:** Falls & Slips 3,619 records; REPORTED_DATE available
- **Expected Answer:** Monthly time series for fall/slip incidents
- **Why This Query:** Core dashboard trend use case.

### AG-06
- **Query:** What proportion of incidents in each impact type category result in high-severity outcomes?
- **Traversal:** [Incident] -> resulted_in -> [Impact Type] + [Incident] -> has_severity -> [Severity] -> group by impact type -> compute distributions
- **Tests:** META (IMPACT_TYPE x SEVERITY) + proportional aggregation
- **Data Density:** IMPACT_TYPE 99.1%; SEVERITY 99.1%
- **Expected Answer:** Severity distribution per impact type
- **Why This Query:** Conditional-risk analysis, not just counts.

---

## Multi-Hop Queries (8)

### MH-01
- **Query:** Find all equipment types involved in containment loss events leading to injuries at offshore locations.
- **Traversal:** [Location: OFFSHORE] <- occurred_at <- [Incident] -> involved -> [Equipment] where [Incident] -> resulted_in -> [Injury] AND [Incident] -> categorized_as -> [CASE: containment loss]
- **Tests:** 3-way join: location + equipment + injury + category
- **Data Density:** Offshore subset x equipment x injury + containment loss category
- **Expected Answer:** Equipment types at offshore sites with containment-loss injuries
- **Why This Query:** Sponsor-critical offshore containment loss scenario.

### MH-02
- **Query:** What injury types are associated with equipment failures during maintenance operations?
- **Traversal:** [Work Process: MAINTENANCE] <- performed_during <- [Incident] -> involved -> [Equipment] + [Incident] -> resulted_in -> [Injury Type] where narrative contains "fail"
- **Tests:** WORK_PROCESS + equipment/injury extraction + narrative signal
- **Data Density:** WORK_PROCESS 88.2%; "failed" is a top action term
- **Expected Answer:** Equipment-injury patterns in maintenance failure contexts
- **Why This Query:** Canonical maintenance -> failure -> injury path.

### MH-03
- **Query:** Which clients have experienced vessel-related incidents resulting in back injuries?
- **Traversal:** [Equipment: VESSEL] <- involved <- [Incident] -> affected -> [Body Part: BACK] + [Incident] -> associated_with -> [Organization: CLIENT]
- **Tests:** Strong co-occurrence pair + organization metadata
- **Data Density:** vessel x back: 780; CLIENT 97.9%
- **Expected Answer:** Clients ranked by vessel+back incident count
- **Why This Query:** Anchored on strongest co-occurrence pair.

### MH-04
- **Query:** What are the most common injury types for each of the top 5 equipment categories?
- **Traversal:** For each top-5 equipment: [Equipment] <- involved <- [Incident] -> resulted_in -> [Injury Type] -> rank per equipment
- **Tests:** Multi-hop traversal pattern repeated across top entities
- **Data Density:** Top 5 equipment have strong representation and injury co-occurrence
- **Expected Answer:** Five ranked injury lists (one per equipment type)
- **Why This Query:** Reveals uneven extraction quality by equipment class.

### MH-05
- **Query:** Find incidents where hand injuries occurred during work involving pipes at locations in Asia Pacific.
- **Traversal:** [Body Part: HAND] <- affected <- [Incident] -> involved -> [Equipment: PIPE] + [Incident] -> occurred_at -> [Location: ASIA PACIFIC]
- **Tests:** Conjunctive constraints across entity + location dimensions
- **Data Density:** hand 9.9%; pipe 9.2%; Asia Pacific in location region
- **Expected Answer:** Incident list matching all constraints
- **Why This Query:** Geography-focused operational relevance.

### MH-06
- **Query:** What is the severity distribution of incidents involving trucks compared to those involving cranes?
- **Traversal:** For each [TRUCK, CRANE]: [Equipment] <- involved <- [Incident] -> has_severity -> [Severity] -> compare distributions
- **Tests:** Comparative multi-hop analysis
- **Data Density:** truck 7.4%; crane 9.9%; SEVERITY 99.1%
- **Expected Answer:** Side-by-side severity distributions
- **Why This Query:** Direct risk comparison workflow.

### MH-07
- **Query:** Which locations have the highest concentration of near-miss incidents involving scaffolding?
- **Traversal:** [Equipment: SCAFFOLD] <- involved <- [Incident] -> is_type -> [Near Miss] + [Incident] -> occurred_at -> [Location] -> rank
- **Tests:** Scaffold extraction + incident type filter + location aggregation
- **Data Density:** INCIDENT_TYPE 70.9%; near miss 29.4%
- **Expected Answer:** Locations ranked by scaffold near-miss count
- **Why This Query:** Leading-indicator style analysis.

### MH-08
- **Query:** Trace the relationship path between a specific piece of equipment (e.g., hydraulic valve) and all recorded injury outcomes across all incidents.
- **Traversal:** [Equipment: HYDRAULIC VALVE] <- involved <- [Incident] -> resulted_in -> [Injury Type]
- **Tests:** Entity specificity vs ER normalization tradeoff
- **Data Density:** valve 5.3% with 9 surface forms; hydraulic-valve subset narrower
- **Expected Answer:** Injury-outcome map for hydraulic valve incidents
- **Why This Query:** Compound-noun ER stress case.

---

## Global Queries (4)

### GL-01
- **Query:** What are the most significant safety risk clusters across TechnipFMC's global operations?
- **Traversal:** Global community detection -> characterize dense incident clusters by dominant entities
- **Tests:** Graph topology analysis (Louvain/label propagation style)
- **Data Density:** Full graph (~20k incidents)
- **Expected Answer:** Top 5-10 clusters with defining characteristics
- **Why This Query:** Core graph-native "pattern discovery" capability test.

### GL-02
- **Query:** Are there systemic patterns where the same type of equipment failure recurs across different geographic regions?
- **Traversal:** [Equipment] <- involved <- [Incident] -> occurred_at -> [Location], compare spread and profile globally
- **Tests:** Cross-region structural pattern detection
- **Data Density:** High-frequency equipment spans multiple countries
- **Expected Answer:** Equipment types recurring across 5+ countries with similar profiles
- **Why This Query:** Global-vs-local intervention planning.

### GL-03
- **Query:** How has the overall safety incident profile changed over the dataset's time range? Are certain incident types increasing or decreasing?
- **Traversal:** Global temporal aggregation over incident type by date
- **Tests:** Longitudinal trend analysis with missing-type handling
- **Data Density:** Multi-year date coverage; INCIDENT_TYPE 70.9%
- **Expected Answer:** Trend lines by incident type (increase/decrease/stable)
- **Why This Query:** Program-level "are we getting safer?" question.

### GL-04
- **Query:** What entities serve as the most connected hubs in the knowledge graph, and what does their centrality reveal about systemic risk?
- **Traversal:** Degree/PageRank centrality across all nodes -> interpret top hubs
- **Tests:** Pure topology metric capability
- **Data Density:** Full graph
- **Expected Answer:** Top hubs + centrality scores + interpretation
- **Why This Query:** Graph health and granularity diagnostic.

---

## Conjunctive Queries (6)

### CJ-01
- **Query:** Which incidents match the pattern of corrosion-induced equipment failure leading to fire?
- **Traversal:** [Root Cause: CORROSION] -> caused -> [Equipment Failure] -> resulted_in -> [Incident Type: FIRE]
- **Tests:** L2 causal chain extraction + conjunctive pattern match
- **Data Density:** Fire/Explosion high causal density; corrosion common in mechanical cluster
- **Expected Answer:** Incident set matching full corrosion -> failure -> fire chain
- **Why This Query:** Canonical L2 conjunctive-causal benchmark.

### CJ-02
- **Query:** Find all high-severity incidents where a crane was involved AND a back injury was sustained AND the location was offshore.
- **Traversal:** [Incident] with crane AND back injury AND offshore AND severity >= 4
- **Tests:** 4-way intersection over entity + metadata constraints
- **Data Density:** crane x back high base volume; offshore + severity narrow set
- **Expected Answer:** Incident list meeting all four constraints
- **Why This Query:** Precision stress test via progressive narrowing.

### CJ-03
- **Query:** Identify incidents where maintenance procedures failed, involving pipe equipment, resulting in environmental impact at locations in the Middle East.
- **Traversal:** narrative contains maintenance+fail AND pipe involvement AND environmental impact AND Middle East location
- **Tests:** Narrative + equipment + impact + geography conjunction
- **Data Density:** pipe strong frequency; environmental impact and region metadata available
- **Expected Answer:** Incidents satisfying full conjunction
- **Why This Query:** Real investigation-style composite filter.

### CJ-04
- **Query:** Which equipment types have caused both injuries AND near-misses at the same location within the same year?
- **Traversal:** Cross-incident pattern: same equipment + same location + same year with both accident and near-miss evidence
- **Tests:** Cross-incident conjunctive pattern matching
- **Data Density:** INCIDENT_TYPE 70.9%; strong equipment-location co-occurrence
- **Expected Answer:** Equipment types meeting dual-risk pattern
- **Why This Query:** Intervention-priority signal discovery.

### CJ-05
- **Query:** Find the causal chain pattern: procedural non-compliance -> dropped object -> head/hand injury. How many incidents match?
- **Traversal:** [Root Cause: PROCEDURAL] -> caused -> [Action: DROPPED] -> resulted_in -> [Injury] -> affected -> [HEAD|HAND]
- **Tests:** Deep L2 chain + action + body-part specificity
- **Data Density:** Procedural cluster 3,531; dropped is top action; hand/head common enough
- **Expected Answer:** Count + incident list for full 4-step chain
- **Why This Query:** High-risk operational chain with concrete intervention value.

### CJ-06
- **Query:** Which incidents involve the co-occurrence of slip/fall events AND vehicle/transportation equipment at construction sites?
- **Traversal:** Falls & Slips category AND truck/vehicle equipment AND construction work process
- **Tests:** Category + equipment + work process conjunction
- **Data Density:** Falls & Slips 3,619; truck 7.4%; construction in WORK_PROCESS
- **Expected Answer:** Incident intersection across all three constraints
- **Why This Query:** Uncommon cross-dimension intersection that may reveal hidden risk pattern.

---

## Notes for Evaluation Use

- `natural_language_query.eval_harness` currently validates against its own built-in
  paraphrase/ground-truth set and does not directly consume this file.
- This file is the canonical query specification for future batch testing scripts
  and prompt/regression tracking.
