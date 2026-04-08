# PetroSuperPipeline

Schema-guided NLP pipeline for extracting structured knowledge from unstructured incident reports.

---

## Overview

This project builds an end-to-end pipeline that:

* Uses GLiNER for zero-shot entity recognition
* Dynamically generates labels from an Excel data catalogue
* Resolves entity duplicates using embeddings
* Stores results in a Neo4j graph database

---

## Key Innovation: Schema-Guided Extraction

Instead of static labels, this system generates entity categories dynamically from an Excel schema.

* Column names → entity labels
* Column descriptions → semantic context

These are passed into GLiNER, enabling domain-aware extraction.

---

## Architecture

Excel Schema → Label Generator → NER → Entity Resolution → Graph DB

---

## Installation

```bash
git clone https://github.com/yourname/petro-super-pipeline.git
cd petro-super-pipeline
pip install -r requirements.txt
```

---

## Setup

Create `.env`:

```
NEO4J_URI=your_uri
NEO4J_USER=your_user
NEO4J_PASSWORD=your_password
```

---

## Run

```bash
python scripts/run_pipeline.py
```

---

## Test

```bash
pytest tests/
```

---

## Output

* Entities
* Relationships
* Knowledge Graph (Neo4j)

---

## Future Work

* Improved embeddings
* Evaluation metrics

---

