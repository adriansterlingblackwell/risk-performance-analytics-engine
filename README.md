# Risk & Performance Analytics Engine

## Overview

Risk & Performance Analytics Engine is an institutional-grade quantitative system designed to evaluate portfolio performance, risk exposure, and trading behavior.

The project is built with a modular, production-oriented architecture that separates data ingestion, validation, transformation, analytics, and reporting layers.

The system is designed to evolve from a research-oriented pipeline into a fully production-ready quantitative analytics platform.

---

## Core Capabilities

### Performance Analytics

* Daily Returns
* Cumulative Returns
* Total Return
* (Planned: CAGR, Sharpe Ratio, Sortino Ratio)

### Risk Analytics (Planned)

* Volatility
* Drawdown
* Value at Risk (VaR)
* Conditional VaR (CVaR)

### Data Pipeline

* Market data ingestion (yfinance)
* Data validation and schema enforcement
* Data transformation into analytics-ready format
* Structured output for downstream analysis

---

## Repository Structure

```
risk-performance-analytics-engine/
├── configs/              # Configuration files
├── data/                 # Raw and processed datasets
├── docs/                 # Architecture and design documentation
├── notebooks/            # Research and exploration
├── reports/              # Exported analytics outputs
├── scripts/              # Pipeline entrypoints
├── src/risk_analytics/   # Core application code
├── tests/                # Unit and integration tests
```

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/adriansterlingblackwell/risk-performance-analytics-engine.git
cd risk-performance-analytics-engine
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -e .
```

Development dependencies:

```bash
pip install -e ".[dev]"
```

### 4. Run tests

```bash
pytest
```

### 5. Run the pipeline

```bash
python scripts/run_pipeline.py
```

---

## Pipeline Flow

```
yfinance
  ↓
loaders.py
  ↓
schemas.py
  ↓
validators.py
  ↓
transforms.py
  ↓
processed market data
  ↓
analytics/performance/returns.py
  ↓
reports/exports
```

### Step-by-step

1. **Data ingestion**
   `loaders.py` downloads historical market data from yfinance.

2. **Schema normalization**
   `schemas.py` defines the internal data contract.

3. **Validation**
   `validators.py` ensures data integrity and correctness.

4. **Transformation**
   `transforms.py` prepares analytics-ready datasets.

5. **Analytics**
   `returns.py` computes return metrics.

6. **Export**
   Results are written to `reports/exports/`.

---

## Output Structure

After running the pipeline, the following outputs are generated:

* `data/raw/` → normalized raw market data
* `data/processed/` → analytics-ready dataset
* `reports/exports/` → computed return analytics

---

## Testing

Run all tests with:

```bash
pytest
```

The test suite validates:

* return calculations
* cumulative return consistency
* data integrity checks

---

## Design Principles

* **Separation of Concerns**
  Each module has a single responsibility.

* **Data Contract First**
  All data must conform to a defined schema.

* **Deterministic Pipelines**
  Same input always produces the same output.

* **Modular Architecture**
  New analytics modules can be added without breaking existing logic.

* **Testability**
  Core functions operate on simple structures (e.g., pandas Series).

---

## Current Status

### Implemented

* Data ingestion pipeline
* Schema definition and validation
* Data transformation layer
* Return analytics (daily, cumulative, total)
* Unit testing for performance metrics

### In Progress

* Pipeline stabilization
* Documentation improvements

### Planned

* CAGR
* Sharpe Ratio
* Sortino Ratio
* Volatility and drawdown
* VaR / CVaR
* Multi-asset portfolio support
* API layer (FastAPI)
* Dashboard layer (Streamlit)

---

## Future Vision

The project aims to evolve into a production-grade quantitative analytics system capable of:

* real-time portfolio evaluation
* risk monitoring
* factor exposure analysis
* institutional-level reporting

---

## Summary

This project is designed not just as a collection of metrics, but as a structured analytics engine that reflects real-world quantitative system design principles.
