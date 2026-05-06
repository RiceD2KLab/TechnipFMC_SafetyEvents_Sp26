def enforce_schema(entity_text):
    if "FORKLIFT" in entity_text:
        return "EQUIPMENT::FORKLIFT"
    return entity_text