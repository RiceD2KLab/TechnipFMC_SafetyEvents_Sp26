"""Paraphrase test set for NL evaluation.

Each benchmark query gets 6-10 natural language phrasings that a safety
analyst might actually type. Includes formal, casual, typo-laden, and
shorthand variants.
"""

PARAPHRASES = {
    # ── Single-hop queries ───────────────────────────────────────────
    "SH-01": [
        "How many forklift incidents happened in 2022?",
        "Forklift incidents in 2022",
        "Count of forklift-related events in 2022",
        "Show me 2022 forklift accidents",
        "forklifts 2022",
        "How many incidents involved a forklift in the year 2022?",
        "Number of fork lift incidents last year in 2022",
        "2022 incidents where forklifts were involved",
    ],

    "SH-03": [
        "What body parts are most commonly injured in crane incidents?",
        "Body parts affected by crane accidents",
        "Which body parts get hurt in crane-related incidents?",
        "Top injuries from crane operations by body part",
        "crane incidents body part breakdown",
        "What parts of the body are injured when cranes are involved?",
        "Most common body part injuries involving cranes",
    ],

    "SH-04": [
        "Which countries have valve incidents?",
        "Locations for valve-related incidents",
        "Where do valve incidents happen by country?",
        "valve incidents by location",
        "Countries with the most valve failures",
        "Geographic distribution of valve incidents",
    ],

    "SH-05": [
        "What injuries occur at offshore installations?",
        "Injuries at offshore sites",
        "injury types for offshore work",
        "What types of injuries happen in offshore operations?",
        "Show me injury breakdown for offshore incidents",
        "Most common injuries at offshore facilities",
    ],

    "SH-06": [
        "How many incidents were reported by Shell Offshore?",
        "Shell Offshore incident count",
        "incidents from Shell Offshore",
        "Count Shell Offshore reported incidents",
        "How many safety events did Shell Offshore report?",
        "Number of incidents Shell Offshore reported",
    ],

    # ── Aggregation queries ──────────────────────────────────────────
    "AG-01": [
        "What are the root causes of dropped object incidents?",
        "Root causes for dropped objects",
        "Why do dropped object incidents happen?",
        "Top root causes when objects are dropped",
        "dropped object root cause breakdown",
        "What causes objects to be dropped?",
        "Main reasons for dropped object events",
        "root cause categories for dropped object incidents",
    ],

    "AG-02": [
        "Which countries have the most high-severity incidents?",
        "Countries with severe incidents",
        "High severity incidents by country",
        "Where are the most serious incidents happening?",
        "Top countries for severity 4+ incidents",
        "Geographic breakdown of high severity events",
        "Most dangerous countries by incident severity",
    ],

    "AG-03": [
        "What is the most common equipment involved in incidents?",
        "Most common equipment in safety incidents",
        "Top equipment types by incident count",
        "Which equipment is involved in the most incidents?",
        "equipment breakdown across all incidents",
        "Rank equipment by number of incidents",
        "What equipment causes the most safety events?",
    ],

    "AG-05": [
        "Show me the trend of fall and slip incidents over time",
        "Fall/slip incidents by year",
        "Monthly trend of falls and slips",
        "How have fall incidents changed over the years?",
        "Trend of slip and fall events",
        "fall slip incidents over time",
        "Historical trend of fall/slip incidents",
    ],

    "AG-06": [
        "Break down severity by impact type",
        "Severity distribution across impact types",
        "How does severity vary by impact type?",
        "Impact type vs severity crosstab",
        "severity levels for each impact type",
        "Cross-reference impact type and severity",
    ],

    # ── Multi-hop queries ────────────────────────────────────────────
    "MH-02": [
        "What injuries happen from equipment failures during maintenance?",
        "Injuries from maintenance equipment failures",
        "Equipment failure injuries in maintenance activities",
        "What types of injuries result from equipment failing during maintenance work?",
        "maintenance equipment failure injury types",
        "Injury breakdown for maintenance-related equipment failures",
    ],

    "MH-05": [
        "Hand injuries from pipe incidents in Asia Pacific",
        "Pipe-related hand injuries in APAC",
        "hand + pipe + Asia Pacific incidents",
        "How many hand injuries involved pipes in the Asia Pacific region?",
        "Incidents with pipe equipment and hand injury in Asia Pacific",
        "APAC pipe incidents causing hand injuries",
    ],

    "MH-06": [
        "Compare severity of truck vs crane incidents",
        "Trucks vs cranes by severity",
        "Are truck or crane incidents more severe?",
        "Severity comparison between truck and crane events",
        "truck incidents severity compared to crane incidents",
        "Which is more dangerous: trucks or cranes?",
    ],

    # ── Conjunctive queries ──────────────────────────────────────────
    "CJ-06": [
        "Falls or slips involving vehicles in construction",
        "Fall/slip + vehicle + construction incidents",
        "Construction incidents with falls and vehicles",
        "Vehicle-related falls in construction work",
        "How many construction incidents involved both falls/slips and vehicles?",
        "falls slips vehicles construction",
    ],
}
