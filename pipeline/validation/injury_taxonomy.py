"""Allow-list for INJURY_TYPE extractions.

Hand-curated from the v5 corpus. Covers the ~120 surface forms that actually
appear as legitimate injury descriptions. Anything not in this set (or its
substring matches) is dropped by validation.

Keys are LOWERCASED, stripped. The matcher uses exact-then-substring like
the BODY_PART_REGIONS matcher in pipeline.ontology.taxonomies.
"""
from __future__ import annotations

# Canonical injury terms → broad category (for future rollup use).
# The category values are advisory; the validator only checks membership.
INJURY_TAXONOMY: dict[str, str] = {
    # ── wounds / lacerations ────────────────────────────────────────────
    "cut": "wound",
    "cuts": "wound",
    "laceration": "wound",
    "lacerations": "wound",
    "abrasion": "wound",
    "abrasions": "wound",
    "scrape": "wound",
    "scratch": "wound",
    "scratches": "wound",
    "graze": "wound",
    "puncture": "wound",
    "puncture wound": "wound",
    "stab": "wound",
    "incision": "wound",
    "gash": "wound",
    "nick": "wound",
    "wound": "wound",
    "open wound": "wound",
    "bleeding": "wound",
    "hematoma": "wound",

    # ── contusions / bruising ───────────────────────────────────────────
    "bruise": "contusion",
    "bruises": "contusion",
    "bruising": "contusion",
    "contusion": "contusion",
    "contusions": "contusion",
    "blunt trauma": "contusion",
    "blunt force": "contusion",
    "bump": "contusion",
    "swelling": "contusion",
    "edema": "contusion",
    "hematoma bruise": "contusion",

    # ── fractures / breaks ──────────────────────────────────────────────
    "fracture": "fracture",
    "fractures": "fracture",
    "broken bone": "fracture",
    "break": "fracture",
    "crack": "fracture",
    "cracked bone": "fracture",
    "hairline fracture": "fracture",
    "stress fracture": "fracture",
    "compound fracture": "fracture",
    "displaced fracture": "fracture",

    # ── sprains / strains / musculoskeletal ─────────────────────────────
    "sprain": "sprain_strain",
    "sprains": "sprain_strain",
    "strain": "sprain_strain",
    "strains": "sprain_strain",
    "twist": "sprain_strain",
    "twisted": "sprain_strain",
    "pulled muscle": "sprain_strain",
    "torn muscle": "sprain_strain",
    "torn ligament": "sprain_strain",
    "torn tendon": "sprain_strain",
    "tear": "sprain_strain",
    "rupture": "sprain_strain",
    "dislocation": "sprain_strain",
    "dislocated": "sprain_strain",
    "hyperextension": "sprain_strain",
    "soft tissue injury": "sprain_strain",
    "musculoskeletal injury": "sprain_strain",
    "msd": "sprain_strain",
    "back strain": "sprain_strain",
    "neck strain": "sprain_strain",

    # ── burns ───────────────────────────────────────────────────────────
    "burn": "burn",
    "burns": "burn",
    "thermal burn": "burn",
    "chemical burn": "burn",
    "electrical burn": "burn",
    "friction burn": "burn",
    "scald": "burn",
    "blister": "burn",
    "flash burn": "burn",
    "arc flash": "burn",
    "first degree burn": "burn",
    "second degree burn": "burn",
    "third degree burn": "burn",

    # ── crush / impact ──────────────────────────────────────────────────
    "crush injury": "crush",
    "crush": "crush",
    "crushing": "crush",
    "crushed": "crush",
    "pinch": "crush",
    "pinched": "crush",
    "pinch point injury": "crush",
    "impact injury": "crush",
    "struck by": "crush",
    "struck": "crush",
    "compression injury": "crush",

    # ── eye-specific ────────────────────────────────────────────────────
    "foreign body in eye": "eye",
    "foreign object in eye": "eye",
    "eye irritation": "eye",
    "corneal abrasion": "eye",
    "eye injury": "eye",
    "flash burn eye": "eye",

    # ── exposure / inhalation / chemical ───────────────────────────────
    "chemical exposure": "exposure",
    "inhalation": "exposure",
    "chemical inhalation": "exposure",
    "fume exposure": "exposure",
    "gas exposure": "exposure",
    "asphyxiation": "exposure",
    "suffocation": "exposure",
    "poisoning": "exposure",
    "toxic exposure": "exposure",
    "smoke inhalation": "exposure",
    "dust inhalation": "exposure",

    # ── electrical ──────────────────────────────────────────────────────
    "electric shock": "electrical",
    "electrical shock": "electrical",
    "electrocution": "electrical",
    "shock": "electrical",

    # ── slip / fall / impact ────────────────────────────────────────────
    "fall": "fall",
    "fell": "fall",
    "slip": "fall",
    "slipped": "fall",
    "trip": "fall",
    "tripped": "fall",

    # ── heat / cold / environmental ─────────────────────────────────────
    "heat exhaustion": "environmental",
    "heat stroke": "environmental",
    "heat stress": "environmental",
    "hypothermia": "environmental",
    "frostbite": "environmental",
    "dehydration": "environmental",
    "sunburn": "environmental",

    # ── bites / stings ──────────────────────────────────────────────────
    "bite": "bite_sting",
    "sting": "bite_sting",
    "insect bite": "bite_sting",
    "snake bite": "bite_sting",

    # ── amputation / severe ─────────────────────────────────────────────
    "amputation": "amputation",
    "amputated": "amputation",
    "severed": "amputation",
    "loss of limb": "amputation",
    "loss of finger": "amputation",
    "avulsion": "amputation",
    "degloving": "amputation",

    # ── head / internal ─────────────────────────────────────────────────
    "concussion": "head",
    "head injury": "head",
    "traumatic brain injury": "head",
    "tbi": "head",
    "loss of consciousness": "head",
    "unconscious": "head",
    "internal injury": "internal",
    "internal bleeding": "internal",
    "internal hemorrhage": "internal",

    # ── pain / general discomfort (legitimate injury descriptions) ──────
    "pain": "pain",
    "back pain": "pain",
    "neck pain": "pain",
    "joint pain": "pain",
    "muscle pain": "pain",
    "soreness": "pain",
    "discomfort": "pain",
    "ache": "pain",
    "stiffness": "pain",
    "numbness": "pain",
    "tingling": "pain",

    # ── skin / dermatitis ───────────────────────────────────────────────
    "dermatitis": "skin",
    "rash": "skin",
    "irritation": "skin",
    "skin irritation": "skin",
    "allergic reaction": "skin",
    "allergy": "skin",
    "inflammation": "skin",
    "infection": "skin",
    "blister": "burn",
    "blisters": "burn",
    "redness": "skin",
    "inflamed": "skin",
    "swell": "contusion",
    "swollen": "contusion",

    # ── symptoms / neurological / general ──────────────────────────────
    "headache": "head",
    "headaches": "head",
    "severe headache": "head",
    "severe headaches": "head",
    "migraine": "head",
    "nausea": "head",
    "nauseous": "head",
    "vomiting": "head",
    "dizziness": "head",
    "dizzy": "head",
    "confusion": "head",
    "confused": "head",
    "disoriented": "head",
    "whiplash": "sprain_strain",
    "paralyzed": "internal",
    "paralysis": "internal",
    "weakness": "pain",
    "fatigue": "pain",
    "cramp": "pain",
    "cramps": "pain",
    "body cramps": "pain",
    "muscle cramp": "pain",
    "foreign body": "eye",   # almost always "foreign body in eye" in this corpus
    "foreign object": "eye",
    "symptoms": "medical",
    "symptom": "medical",
    "contusive lesion": "contusion",
    "wounds": "wound",       # plural
    "fractures": "fracture", # plural already there but ensure
    "bruised": "contusion",
    "scrapped up": "wound",  # colloquial for scraped

    # ── general medical outcomes ────────────────────────────────────────
    "first aid": "medical",
    "first aid case": "medical",
    "medical treatment": "medical",
    "medical treatment case": "medical",
    "mtc": "medical",
    "lost time injury": "medical",
    "lti": "medical",
    "restricted work case": "medical",
    "rwc": "medical",
    "injury": "medical",
    "injuries": "medical",
    "harm": "medical",
    "illness": "medical",
    "occupational illness": "medical",
    "fatality": "medical",
    "death": "medical",
    "near miss": "medical",

    # ── needlestick / exposure ─────────────────────────────────────────
    "needlestick": "exposure",
    "needle stick": "exposure",
    "sharps injury": "wound",

    # ── verb forms / past participles (from v6 dropped-term audit) ──────
    "injured": "medical",
    "sprained": "sprain_strain",
    "strained": "sprain_strain",
    "lacerated": "wound",
    "fractured": "fracture",
    "fracturing": "fracture",
    "broken": "fracture",
    "broke": "fracture",
    "broke bones": "fracture",
    "scratched": "wound",
    "bruised": "contusion",
    "burned": "burn",
    "amputated": "amputation",
    "dislocated": "sprain_strain",

    # ── additional legitimate medical terms from v6 audit ──────────────
    "fac": "medical",           # First Aid Case abbreviation
    "trauma": "medical",
    "traumatic injury": "medical",
    "splinter": "wound",
    "tenderness": "pain",
    "burning sensation": "burn",
    "twinge": "pain",
    "deformity": "medical",
    "displacement": "sprain_strain",
    "drowsy": "head",
    "drowsiness": "head",
    "ligament injury": "sprain_strain",
    "ligaments": "sprain_strain",
    "tendon injury": "sprain_strain",
    "tendon": "sprain_strain",
    "tendonitis": "sprain_strain",
    "repetitive strain": "sprain_strain",
    "rsi": "sprain_strain",
    "minor injury": "medical",
    "severe injury": "medical",
    "serious injury": "medical",
}


def is_valid_injury_type(span: str) -> bool:
    """Return True if the span matches any term in INJURY_TAXONOMY.

    Matching strategy:
      1. Normalize: lowercase, strip, replace '/' and '-' with spaces,
         collapse whitespace
      2. Exact match on the normalized form
      3. Substring match for multi-word taxonomy keys
      4. Token-set membership for single-word taxonomy keys
    """
    if not isinstance(span, str):
        return False
    s = span.strip().lower()
    if not s:
        return False
    # Normalize hyphens and slashes to spaces so "eye-irritation" matches
    # "eye irritation" and "cut/laceration" matches "cut"
    import re as _re
    s = _re.sub(r"[/\-]", " ", s)
    s = _re.sub(r"\s+", " ", s).strip()
    if s in INJURY_TAXONOMY:
        return True
    tokens = set(s.split())
    for key in sorted(INJURY_TAXONOMY.keys(), key=len, reverse=True):
        if " " in key:
            if key in s:
                return True
        else:
            if key in tokens:
                return True
    return False
