"""Equipment validation rules.

Two responsibilities:
  1. Reject EQUIPMENT spans that are actually person roles or generic nouns
     (the "Grinder man", "worker", "companion" problem from the v5 audit).
  2. Provide a keyword set used by the validator to decide whether a
     mis-tagged BODY_PART should be reclassified as EQUIPMENT or just dropped.

Both lists are lowercased. Matching is exact or whole-word token membership.
"""
from __future__ import annotations

# ── People / roles that GLiNER sometimes tags as EQUIPMENT or BODY_PART ──
# When one of these appears, drop the extraction entirely — we have a
# dedicated PERSON type in the schema for cases where we want to keep them.
PERSON_ROLES: frozenset[str] = frozenset({
    "worker",
    "workers",
    "operator",
    "operators",
    "employee",
    "employees",
    "associate",
    "associates",
    "technician",
    "technicians",
    "supervisor",
    "foreman",
    "manager",
    "driver",
    "mechanic",
    "welder",
    "electrician",
    "fitter",
    "rigger",
    "deckhand",
    "crew",
    "crewman",
    "crewmember",
    "personnel",
    "staff",
    "contractor",
    "subcontractor",
    "visitor",
    "companion",
    "individual",
    "person",
    "persons",
    "people",
    "ip",                     # "Injured Person" — domain abbreviation, never a body part or equipment
    "ips",
    "ipo",
    "pe",                     # "Person Exposed"
    "grinder man",
    "material handler",
    "tall employee",
    "receiving technician",
    "deck supervisor",
    "the operator",
    "the worker",
    "the technician",
    "site engineer",
    "safety officer",
    "health officer",
})


# ── Generic positional / structural phrases that are neither body nor equipment ──
# These are GLiNER artifacts from mechanical context — "bottom of the door",
# "front portion", "lower left corner". Drop them; they don't belong to any
# entity type.
GENERIC_POSITIONS: frozenset[str] = frozenset({
    "top",
    "bottom",
    "front",
    "back",        # NOTE: "back" as BODY_PART stays via the anatomy allow-list; this set is only for EQUIPMENT/LOCATION validation
    "side",
    "edge",
    "corner",
    "top part",
    "bottom part",
    "front part",
    "back part",
    "front portion",
    "back portion",
    "top portion",
    "bottom portion",
    "front flap",
    "back flap",
    "back side",
    "front side",
    "opposite side",
    "right side",
    "left side",
    "upper side",
    "lower side",
    "inner side",
    "outer side",
    "outerside",
    "inner sleeve",
    "outer sleeve",
    "front corner",
    "back corner",
    "right corner",
    "left corner",
    "upper left corner",
    "upper right corner",
    "lower left corner",
    "lower right corner",
    "front end",
    "back end",
    "top end",
    "bottom end",
    "first end",
    "second end",
    "rear left view",
    "front right view",
    "top of",
    "bottom of",
    "back of",
    "front of",
    "side of",
    "middle of",
    "center of",
    "area",
    "region",
    "zone",
    "portion",
    "section",
    "part",
    "face",     # NOTE: real anatomical "face" stays via BODY_PART allow-list; this only blocks it as EQUIPMENT/LOCATION
    "surface",
    "overhead",
    "underneath",
})


# ── Equipment keyword set (substring matchers) ────────────────────────────
# Used by the validator to decide: when BODY_PART fails the anatomy check,
# does the span LOOK like equipment? If yes → reclassify; if no → drop.
#
# This is intentionally broad — false reclassification is fine because the
# downstream EQUIPMENT type is already messy and ER will clean it up. The
# important thing is to not LOSE the information entirely.
EQUIPMENT_KEYWORDS: frozenset[str] = frozenset({
    # Vehicles
    "car", "truck", "van", "bus", "vehicle", "trailer", "forklift",
    "crane", "excavator", "bulldozer", "loader", "tractor", "rig",
    "motorcycle", "bicycle", "atv", "skidsteer", "backhoe",
    # Vehicle parts
    "door", "window", "wheel", "tire", "bumper", "hood", "grill", "grille",
    "fender", "mirror", "headlight", "taillight", "tailight", "windshield",
    "dashboard", "steering", "brake", "axle", "chassis", "radiator",
    "engine", "transmission", "exhaust",
    # Structural / industrial parts
    "boom", "mast", "cable", "chain", "hook", "sling", "rope", "wire",
    "pipe", "pipeline", "hose", "valve", "flange", "bolt", "nut",
    "washer", "bearing", "shaft", "gear", "pulley", "belt", "pump",
    "motor", "generator", "compressor", "tank", "vessel", "cylinder",
    "drum", "reel", "spool", "winch", "jack", "hoist", "lift",
    "stand", "frame", "rack", "skid", "pallet", "crate", "container",
    "box", "cabinet", "panel", "board", "bracket", "clamp", "fastener",
    # Tools
    "tool", "drill", "grinder", "saw", "hammer", "wrench", "screwdriver",
    "cutter", "torch", "welder", "welding",
    # PPE / safety equipment
    "helmet", "gloves", "boots", "harness", "lanyard", "vest", "goggles",
    "mask", "respirator", "ppe",
    # Facility / structure
    "deck", "platform", "scaffold", "ladder", "stairs", "staircase",
    "walkway", "catwalk", "handrail", "railing", "guardrail",
    "floor", "wall", "ceiling", "roof", "beam", "column", "pillar",
    "post", "plate", "grating", "duct", "vent", "pipe rack",
    # Marine / subsea
    "rov", "umbilical", "riser", "manifold", "jumper", "xt", "wellhead",
    "bop", "tree", "anchor", "mooring", "buoy", "fender", "fairlead",
    # Misc heavy equipment
    "overhead door", "overhead crane", "passenger door", "car door",
    "trailer door", "front door", "rear door",
    "boom tip", "rear wheel", "front wheel", "rear tire", "front tire",
    "module column", "racking guard",
})


def is_person_role(span: str) -> bool:
    """Return True if span is a generic person/role term that shouldn't
    be EQUIPMENT, BODY_PART, or ORGANIZATION."""
    if not isinstance(span, str):
        return False
    s = span.strip().lower()
    if not s:
        return False
    if s in PERSON_ROLES:
        return True
    tokens = set(s.split())
    # Short tokens only — avoid matching "operator" inside "crane operator"
    # (which we want to keep as equipment-adjacent context, not drop)
    if s in tokens and len(tokens) == 1 and s in PERSON_ROLES:
        return True
    return False


def is_generic_position(span: str) -> bool:
    """Return True if span is a generic positional/structural phrase that
    isn't a meaningful entity of any type."""
    if not isinstance(span, str):
        return False
    s = span.strip().lower()
    if not s:
        return False
    return s in GENERIC_POSITIONS


def looks_like_equipment(span: str) -> bool:
    """Heuristic: does this span contain any EQUIPMENT_KEYWORDS?

    Used to decide whether a mis-tagged BODY_PART should be reclassified
    as EQUIPMENT instead of dropped. False positives here are acceptable —
    EQUIPMENT ER will clean them up.
    """
    if not isinstance(span, str):
        return False
    s = span.strip().lower()
    if not s:
        return False
    tokens = set(s.split())
    for kw in EQUIPMENT_KEYWORDS:
        if " " in kw:
            if kw in s:
                return True
        else:
            if kw in tokens:
                return True
    return False


# ── Event keyword set (for EVENT reclassification) ──────────────────────
# Words that describe physical occurrences rather than injuries or
# equipment. Used to rescue BODY_PART / INJURY_TYPE / LOCATION drops that
# are actually events (leak, spill, fall, fire, explosion, ...).
EVENT_KEYWORDS: frozenset[str] = frozenset({
    # Fluid / release
    "leak", "leaks", "leakage", "leaking",
    "spill", "spills", "spillage", "spilled", "spilling",
    "spray", "sprays", "spraying", "sprayed",
    "discharge", "discharges", "discharged", "discharging",
    "release", "releases", "released", "releasing",
    "emission", "emissions", "emit", "emitted",
    "drip", "drips", "dripping",
    "overflow", "overflows", "overflowing",
    "seepage", "seep", "seeping",
    # Falls / slips / kinematic
    "fall", "falls", "falling", "fell",
    "slip", "slips", "slipped", "slipping",
    "trip", "trips", "tripped", "tripping",
    "stumble", "stumbles", "stumbled", "stumbling",
    "drop", "drops", "dropped", "dropping", "dropped object",
    "tipping", "tip-over", "tipover", "overturn", "overturned",
    "rollover", "rolled over",
    # Fire / explosion / thermal
    "fire", "fires",
    "explosion", "explosions", "exploded",
    "ignition", "ignited",
    "blaze",
    "flame", "flames",
    "flashover", "flash fire",
    # Structural failure / damage events
    "collapse", "collapsed", "collapsing",
    "rupture", "ruptures", "ruptured",
    "burst", "bursting",
    "breakage", "break", "breakdown", "broke",
    "crack", "cracked", "cracking",
    "fracture",     # noun event, differentiated from INJURY_TYPE "fracture" which is already allow-listed
    "tear", "tore", "tearing",
    "snap", "snapped",
    "shear", "sheared",
    "buckle", "buckled",
    "deformation", "deformed",
    # Impact / collision
    "impact", "impacts", "impacted",
    "collision", "collisions", "collided",
    "crash", "crashed",
    "hit", "hits",
    "strike", "struck",
    "caught between",
    # System / process failures
    "malfunction", "malfunctioned",
    "failure", "failed",
    "shutdown", "shut down",
    "trip",          # system trip (ambiguous with slip-trip; EVENT bucket is fine either way)
    "stoppage",
    "outage",
    "blackout",
    "power loss",
    # Electrical
    "short circuit", "short-circuit", "short",
    "arc", "arcing", "arc flash",
    "sparking", "sparks",
    # Environmental
    "flood", "flooding", "flooded",
    "submersion", "submerged",
    # Generic occurrence nouns
    "incident",      # meta but fine — will co-exist with INCIDENT hub nodes since they use prefix
    "accident",
    "event",
    "occurrence",
    "mishap",
    "near miss",
    # Damage states (ambiguous but better as EVENT than dropped)
    "damage", "damages", "damaged",
    "damaged equipment",
})


def looks_like_event(span: str) -> bool:
    """Heuristic: does this span describe a physical event/occurrence?

    Used to rescue mis-tagged INJURY_TYPE / BODY_PART entries by
    reclassifying them to EVENT instead of dropping. False positives are
    acceptable — the downstream graph just gets an event node that L2 may
    or may not connect.
    """
    if not isinstance(span, str):
        return False
    s = span.strip().lower()
    if not s:
        return False
    tokens = set(s.split())
    for kw in EVENT_KEYWORDS:
        if " " in kw:
            if kw in s:
                return True
        else:
            if kw in tokens:
                return True
    return False
