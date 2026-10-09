# Air Quality Lakehouse with GenAI

Portfolio project plan for Mamun. Target role: Data and AI Practice Leader.
Working repo name: `databricks-lakehouse-genai`

## Why this project

Hiring managers for practice leader roles want to see three things: you can design a modern data platform, you can put GenAI on top of it responsibly, and you can explain it like a client handover. This project shows all three in one repo, and it closes the gaps called out in your roadmap: Databricks, PySpark, GenAI, dbt, Terraform and GitHub Actions.

It also tells a story recruiters understand quickly: "I took a public dataset and built the kind of platform I would sell and deliver to a client."

## Dataset

**Pick: Air Quality System (AQS) pre-generated data files.**

- Free public CSV downloads of daily and hourly readings for ozone, PM2.5, NO2 and other pollutants, plus site and monitor reference files.
- Many years of history, millions of rows per year, so the volume is real enough to justify a lakehouse.
- Clear business questions: which counties exceed the standards, how air quality changed over time, where monitoring coverage is thin.
- Keeps the project fully separate from your client work.

**Documents for the GenAI layer:** the public AQS data dictionary, the air quality standards fact sheets and the AQI technical guide (all public PDFs). These let the assistant answer both "what does this field mean" and "what does the standard say" questions.

**Rule:** use only public data and public documents. Nothing from any client or employer work goes in the repo.

**Backup option:** a city open data portal with a public license, if the air quality files ever become unavailable. Same architecture works.

## Architecture

```
Public AQS CSVs + public PDFs
        |
        v
Unity Catalog volume (raw files)
        |
        v
BRONZE  Auto Loader / Lakeflow pipeline, raw Delta tables, ingest metadata
        |
        v
SILVER  PySpark: typed, deduplicated, joined to sites and monitors, data quality expectations
        |
        v
GOLD    dbt models: star schema (fact_daily_reading, dim_site, dim_pollutant, dim_date),
        county exceedance marts, trend marts
        |
        +--> Databricks SQL dashboard (exec summary)
        |
        +--> GenAI layer
              - Vector index over chunked PDFs and the data dictionary
              - RAG assistant that answers with citations
              - SQL agent that queries gold tables through a governed function,
                with guardrails, logging and an evaluation set
```

**Platform and tooling**

| Area | Choice | What it proves |
|---|---|---|
| Workspace | Databricks Free Edition | Lakehouse skills without a cloud bill |
| Governance | Unity Catalog: catalog `aq`, schemas `bronze`, `silver`, `gold`, `ai` | Enterprise style data governance |
| Ingestion | Auto Loader inside a Lakeflow Declarative Pipeline | Modern incremental ingestion |
| Transform | PySpark for silver, dbt (dbt-databricks) for gold | PySpark at working level and analytics engineering |
| Quality | Pipeline expectations plus dbt tests | Trustworthy data, not just pipelines |
| GenAI | Vector Search, a hosted foundation model, MLflow tracing and evaluation | RAG and agents done responsibly |
| Infrastructure | Terraform (Databricks provider) for catalog, schemas, volumes and grants | Infrastructure as code |
| Deploy | Databricks Asset Bundles run from GitHub Actions | CI/CD the way current teams work |

Free Edition has usage limits. If a GenAI feature is not available there, fall back to a local vector store (Chroma or FAISS) and an external LLM API, and note the swap in the README. That trade off is itself a good interview talking point.

## Repo layout

```
databricks-lakehouse-genai/
  README.md
  docs/
    architecture.png
    decisions/            short architecture decision records
    runbook.md
  infra/terraform/        catalog, schemas, volumes, grants
  bundles/databricks.yml  jobs and pipelines as an Asset Bundle
  src/
    ingestion/            bronze pipeline
    silver/               PySpark transforms and expectations
    genai/                chunking, index build, RAG app, SQL agent, eval set
  dbt/                    gold models, tests, docs
  tests/                  unit tests for PySpark functions
  .github/workflows/      lint, test, validate, deploy
```

## Milestones (mapped to your 48 week plan)

| Weeks | Dates | Milestone | Done when |
|---|---|---|---|
| 4 | Nov 2 to Nov 8 | Dataset and design locked | This plan is in the repo; 3 to 5 years of AQS daily files chosen; first decision record written |
| 5 | Nov 9 to Nov 15 | Bronze layer | Files land in a volume; pipeline loads raw Delta tables with ingest date and source file columns |
| 6 | Nov 16 to Nov 22 | Silver layer | Typed, deduplicated tables joined to sites and monitors; expectations drop or flag bad rows; row counts reconciled |
| 7 to 8 | Nov 23 to Dec 6 | Exam weeks | Light touch only; the bronze and silver work doubles as Data Engineer Associate practice |
| 9 | Dec 7 to Dec 13 | Infra and CI/CD | Terraform creates the catalog objects; GitHub Actions runs tests and deploys the bundle on merge to main |
| 10 | Dec 14 to Dec 20 | Gold layer and README | dbt star schema and marts with tests; dashboard with 4 to 6 tiles; README written as a client handover |
| 11 to 12 | Dec 21 to Jan 3 | Buffer | Fix anything left over; tag release v1.0 |
| 13 | Jan 4 to Jan 10 | Vector index | PDFs chunked and indexed with source and page metadata |
| 14 | Jan 11 to Jan 17 | RAG assistant | Answers with citations; 25 question eval set with a scored baseline |
| 15 | Jan 18 to Jan 24 | SQL agent | Agent answers numeric questions from gold tables through a read only function; prompts and answers logged; refuses out of scope requests |
| 16 | Jan 25 to Jan 31 | Demo and launch | 5 minute demo video, release v2.0, LinkedIn post |
| 21 | Mar 1 to Mar 7 | Article | "Oracle Analytics to lakehouse: lessons from both sides," using this repo as the example |
| 25 to 26 | Mar 29 to Apr 11 | Interview assets | Project turned into one interview story and a practice leader case (team, cost, risk for an enterprise migration) |

**Rough weekly time:** 6 to 8 hours in build weeks, 2 hours in exam and holiday weeks.

## README outline

Write the README for a hiring manager who gives it two minutes.

1. **Title and one line summary.** What it is and who it is for.
2. **The business problem.** Two or three sentences in business language: which communities are exposed to unhealthy air, and where monitoring has gaps.
3. **Demo.** Video link and three screenshots (dashboard, RAG answer with citations, agent answer).
4. **Architecture.** The diagram and one paragraph per layer.
5. **Key results.** Rows processed, pipeline run time, data quality pass rate, RAG eval score, estimated monthly cost at enterprise scale.
6. **Governance and responsible AI.** Unity Catalog grants, lineage, PII stance (none in this data), guardrails, logging, evaluation.
7. **How to run it.** Prerequisites, Terraform, bundle deploy, dbt run, in under ten steps.
8. **Design decisions.** Links to the decision records, including the trade offs you made.
9. **What I would do for a real client.** Scaling, security hardening (your SAML, RLS and DR background shows here), team shape and cost model. This section is what makes it a practice leader project instead of an engineer project.
10. **About me.** Two lines and a link to LinkedIn.

## Results to capture for your resume

Write these down as you go so the numbers are ready for interviews:

- Rows and years of data processed, and end to end run time
- Data quality pass rate and the number of issues the checks caught
- RAG evaluation score before and after tuning
- Cost per run on serverless, and a projected monthly cost for an enterprise sized version
- Time from git push to deployed pipeline
