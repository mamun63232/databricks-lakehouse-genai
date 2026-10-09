# Air Quality Lakehouse with GenAI

A Databricks lakehouse built on public air quality data, with a GenAI assistant that answers questions about the data and the standards behind it. Built as a portfolio project to show how I would design and deliver a modern data and AI platform for a client.

> Status: in progress. See the [project plan](docs/project-plan.md) for scope and milestones.
> Personal project, not affiliated with or endorsed by any data publisher. See the [disclaimer](#disclaimer).

## The business problem

Which communities are exposed to unhealthy air, how has that changed over time, and where is monitoring coverage too thin to know? Organizations have the raw data, but it sits in large flat files that are hard to query and harder to explain. This project turns it into governed, tested tables and puts a question answering layer on top.

## Demo

Coming in milestone 16: a 5 minute video and screenshots of the dashboard, a RAG answer with citations, and an agent answer.

## Architecture

```
Public air quality CSVs + public PDFs
        |
        v
Unity Catalog volume (raw files)
        |
        v
BRONZE  Auto Loader / Lakeflow pipeline, raw Delta tables
        |
        v
SILVER  PySpark: typed, deduplicated, joined, quality checked
        |
        v
GOLD    dbt star schema and marts
        |
        +--> Databricks SQL dashboard
        +--> GenAI: vector index, RAG assistant, governed SQL agent
```

| Layer | Tools |
|---|---|
| Governance | Unity Catalog |
| Ingestion | Auto Loader, Lakeflow Declarative Pipelines |
| Transform | PySpark (silver), dbt (gold) |
| GenAI | Vector Search, foundation model API, MLflow tracing and evaluation |
| Infrastructure | Terraform |
| CI/CD | Databricks Asset Bundles, GitHub Actions |

## Key results

To be filled in as milestones land: rows processed, pipeline run time, data quality pass rate, RAG evaluation score, and estimated monthly cost at enterprise scale.

## Governance and responsible AI

To be written: Unity Catalog grants and lineage, data sensitivity (public data only, no PII), agent guardrails, logging and evaluation.

## How to run it

To be written once the infrastructure and bundle are in place.

## Design decisions

Short decision records live in [docs/decisions](docs/decisions).

## What I would do for a real client

To be written: scaling, security hardening, disaster recovery, team shape and cost model.

## Repo layout

```
docs/                 plan, architecture, decision records, runbook
infra/terraform/      catalog, schemas, volumes, grants
bundles/              Databricks Asset Bundle for jobs and pipelines
src/ingestion/        bronze pipeline
src/silver/           PySpark transforms and expectations
src/genai/            chunking, vector index, RAG app, SQL agent, eval set
dbt/                  gold models and tests
tests/                unit tests
.github/workflows/    lint, test, validate, deploy
```

## Data sources

All data is public: the Air Quality System pre-generated data files, the data dictionary, air quality standards fact sheets and the AQI technical guide. Nothing from any client engagement is used.

Data source: Air Quality System pre-generated data files, https://aqs.epa.gov/aqsweb/airdata/download_files.html. Published for public download and in the public domain.

## Disclaimer

This is a personal portfolio project. It is not affiliated with, sponsored by or endorsed by the publisher of the data or any other organization. The data is used as published, and any analysis or conclusions here are my own.
