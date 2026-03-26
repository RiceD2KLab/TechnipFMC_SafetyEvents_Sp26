// ============================================================
// TechnipFMC Safety Events — Example Cypher Queries
// Graph: ~100K nodes (Entity), ~234K edges (L1 + L2 relations)
// Key labels: Entity (all nodes), secondary labels per entity_type
//   e.g. INCIDENT, EQUIPMENT, LOCATION, ROOT_CAUSE_CATEGORY ...
// Key relation types:
//   L1: OCCURRED_AT, REPORTED_BY, INVOLVED, CATEGORIZED_AS,
//       AFFECTED, RESULTED_IN, LOCATED_IN
//   L2: CAUSAL, PRECEDED_BY, FAILED_CONTROL, MITIGATED_BY
// ============================================================


// ------------------------------------------------------------
// Q1: Equipment involved in high-severity incidents
//     Find equipment nodes linked to incidents rated HIGH or CRITICAL
// ------------------------------------------------------------
MATCH (inc:Entity {entity_type: 'INCIDENT'})-[:INVOLVED]->(eq:Entity {entity_type: 'EQUIPMENT'})
WHERE inc.severity IN ['HIGH', 'CRITICAL']
RETURN eq.value AS equipment, inc.severity AS severity, inc.incident_type AS incident_type,
       inc.entity_id AS incident_id
ORDER BY severity DESC
LIMIT 50;


// ------------------------------------------------------------
// Q2: What caused fires? — CAUSAL chains ending at fire incidents
//     Follow L2 CAUSAL edges (source=cause, target=effect)
// ------------------------------------------------------------
MATCH path = (cause:Entity)-[:CAUSAL*1..3]->(effect:Entity)
WHERE toLower(effect.value) CONTAINS 'fire'
   OR toLower(effect.value) CONTAINS 'ignition'
RETURN cause.value AS root_cause, cause.entity_type AS cause_type,
       effect.value AS fire_event, length(path) AS hops
ORDER BY hops, root_cause
LIMIT 40;


// ------------------------------------------------------------
// Q3: Incidents where a safety barrier failed (FAILED_CONTROL)
//     Identify which controls were bypassed and what incident followed
// ------------------------------------------------------------
MATCH (inc:Entity {entity_type: 'INCIDENT'})-[fc:FAILED_CONTROL]->(ctrl:Entity)
RETURN inc.entity_id AS incident_id,
       inc.incident_type AS incident_type,
       inc.severity AS severity,
       ctrl.value AS failed_control,
       ctrl.entity_type AS control_type,
       fc.evidence AS evidence
ORDER BY inc.severity DESC
LIMIT 50;


// ------------------------------------------------------------
// Q4: Variable-length causal path (1–3 hops) from a condition
//     Explore how conditions propagate into downstream events
// ------------------------------------------------------------
MATCH path = (start:Entity {entity_type: 'CONDITION'})-[:CAUSAL*1..3]->(end:Entity)
WHERE end.entity_type IN ['INCIDENT', 'INJURY', 'EVENT']
RETURN start.value AS condition,
       [n IN nodes(path) | n.value] AS causal_chain,
       end.entity_type AS outcome_type,
       length(path) AS depth
ORDER BY depth DESC
LIMIT 30;


// ------------------------------------------------------------
// Q5: Full-text search on entity values
//     Find any entity whose value mentions "pressure" or "valve"
//     Requires the entity_value_ft fulltext index (created by loader)
// ------------------------------------------------------------
CALL db.index.fulltext.queryNodes('entity_value_ft', 'pressure valve')
YIELD node, score
RETURN node.value AS value, node.entity_type AS entity_type, score
ORDER BY score DESC
LIMIT 20;


// ------------------------------------------------------------
// Q6: Mitigated incidents — what controls worked?
//     MITIGATED_BY: source=event/harm, target=control that worked
// ------------------------------------------------------------
MATCH (harm:Entity)-[mb:MITIGATED_BY]->(ctrl:Entity)
WHERE harm.entity_type IN ['INCIDENT', 'INJURY', 'EVENT']
RETURN harm.value AS event_or_harm,
       harm.entity_type AS harm_type,
       ctrl.value AS mitigating_control,
       ctrl.entity_type AS control_type,
       mb.evidence AS evidence
ORDER BY harm_type, ctrl.value
LIMIT 50;


// ------------------------------------------------------------
// Q7: Top equipment by incident count
//     Rank equipment nodes by how many distinct incidents involve them
// ------------------------------------------------------------
MATCH (inc:Entity {entity_type: 'INCIDENT'})-[:INVOLVED]->(eq:Entity {entity_type: 'EQUIPMENT'})
WITH eq.value AS equipment, count(DISTINCT inc.entity_id) AS incident_count
RETURN equipment, incident_count
ORDER BY incident_count DESC
LIMIT 20;


// ------------------------------------------------------------
// Q8: Corrosion → equipment failure chains
//     Find paths where corrosion-related conditions cause equipment events
// ------------------------------------------------------------
MATCH path = (corr:Entity)-[:CAUSAL*1..2]->(fail:Entity)
WHERE (toLower(corr.value) CONTAINS 'corrosion'
    OR toLower(corr.value) CONTAINS 'corrosive')
  AND fail.entity_type IN ['EQUIPMENT', 'EVENT', 'INCIDENT']
RETURN corr.value AS corrosion_factor,
       fail.value AS failure_node,
       fail.entity_type AS failure_type,
       length(path) AS hops,
       [r IN relationships(path) | type(r)] AS rel_types
ORDER BY hops
LIMIT 30;


// ------------------------------------------------------------
// Q9: All causal factors for a specific incident
//     Replace 'INC-XXXXX' with an actual entity_id from the graph
// ------------------------------------------------------------
MATCH (cause:Entity)-[:CAUSAL*1..4]->(inc:Entity {entity_id: 'INC-XXXXX'})
RETURN cause.value AS causal_factor,
       cause.entity_type AS factor_type,
       shortestPath((cause)-[:CAUSAL*]->(inc)) AS path
ORDER BY factor_type;


// ------------------------------------------------------------
// Q10: LOTO / electrical incidents with FAILED_CONTROL edges
//      Find electrical isolation failures linked to injuries
// ------------------------------------------------------------
MATCH (inc:Entity {entity_type: 'INCIDENT'})-[:FAILED_CONTROL]->(ctrl:Entity)
WHERE toLower(ctrl.value) CONTAINS 'loto'
   OR toLower(ctrl.value) CONTAINS 'lockout'
   OR toLower(ctrl.value) CONTAINS 'isolation'
   OR toLower(ctrl.value) CONTAINS 'electrical'
OPTIONAL MATCH (inc)-[:RESULTED_IN]->(inj:Entity {entity_type: 'INJURY'})
RETURN inc.entity_id AS incident_id,
       inc.incident_type AS incident_type,
       inc.severity AS severity,
       ctrl.value AS failed_control,
       inj.value AS resulting_injury
ORDER BY inc.severity DESC
LIMIT 40;
