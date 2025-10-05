# FIWARE Smart City Mini‑Sim — Use Case Specification

> Version: 0.1 • Author: You • Status: Draft (Phase 1 focus)

## 1. Purpose & Scope
This document defines the use cases, actors, and requirements for a personal learning project that simulates a smart‑city environment using FIWARE components. Phase 1 focuses on core context ingestion (sensors → IoT Agent → Orion). Phase 2 adds persistence and basic visualisation. Later phases (alerts, auth, linked data) are out of scope for the initial MVP.

### 1.1 Goals
- Learn and practise FIWARE context management with realistic (non‑random) simulated signals.
- Produce a minimal yet coherent architecture that can be iterated upon.
- Document decisions, assumptions, and trade‑offs for future study.

### 1.2 Out of Scope (for now)
- Production‑grade security and multi‑tenant management.
- High‑availability clustering and horizontal scaling tests.
- Complex semantics/graph modelling (advanced NGSI‑LD relationships).

---

## 2. System Context (High‑Level)
**External Actors** interact with the **Smart City Mini‑Sim** via APIs and dashboards.

```
[Developer / User] → (HTTP/REST) → [Orion Context Broker]
[Simulator] → (HTTP/MQTT) → [IoT Agent] → [Orion]
[Persistence (Cygnus/QuantumLeap)] ← (Subscriptions) ← [Orion] → (Web/UI) → [Grafana/WireCloud]
```

**Core FIWARE components (Phase 1):** Orion Context Broker, IoT Agent, MongoDB (Orion backend).

**Added in Phase 2:** Cygnus or QuantumLeap + PostgreSQL/TimescaleDB and dashboard(s).

---

## 3. Actors
- **Simulator**: Python processes that emit environmental and traffic measurements following time‑based curves and correlations.
- **IoT Agent**: FIWARE enabler that maps device messages to NGSI entities.
- **Orion Context Broker**: Stores and serves current context state; manages subscriptions.
- **Developer/User**: Operates the system, issues queries, inspects entities, and validates behaviour.
- **Persistence Service** (Phase 2): Cygnus/QuantumLeap for historical storage.
- **Dashboard Viewer** (Phase 2): Views charts/maps; can be the same person as Developer/User.

---

## 4. High‑Level Requirements

### 4.1 Functional Requirements (FR)
- **FR‑1**: The system shall accept sensor readings from simulators via the IoT Agent.
- **FR‑2**: The IoT Agent shall upsert NGSI entities/attributes in Orion.
- **FR‑3**: The system shall model at least two domains: *Traffic* and *Environment (Air Quality)*.
- **FR‑4**: The simulator shall generate values using configurable time‑based curves and noise.
- **FR‑5**: The Developer/User shall be able to query Orion for current state via REST.
- **FR‑6 (Phase 2)**: The system shall persist entity updates to a database via subscriptions.
- **FR‑7 (Phase 2)**: The system shall present basic dashboards for trends/maps.

### 4.2 Non‑Functional Requirements (NFR)
- **NFR‑1**: Deployable via Docker Compose on a developer laptop.
- **NFR‑2**: Clear configuration via `.env` and version‑controlled YAML/JSON.
- **NFR‑3**: Reproducible: a fresh clone + documented steps should run in ≤10 minutes.
- **NFR‑4**: Observability: minimal logs and health checks to verify data flow.
- **NFR‑5**: Educational clarity: code and docs prioritise readability over micro‑optimisation.

---

## 5. Use Case Catalogue

| ID | Name | Primary Actor | Trigger | Summary |
|----|------|----------------|---------|---------|
| UC‑01 | Register Device | Developer/User | New simulated device required | Declare a device and its attributes in the IoT Agent so payloads are accepted. |
| UC‑02 | Send Sensor Reading | Simulator | Time tick / schedule | Post a measurement; IoT Agent maps it to NGSI and updates Orion. |
| UC‑03 | Query Current State | Developer/User | Need to inspect data | Retrieve entity/attribute values from Orion via REST. |
| UC‑04 | Configure Curves | Developer/User | Adjust realism | Define the curve/noise parameters for simulated signals. |
| UC‑05 | Subscribe to Changes (P2) | Developer/User | Need history/alerts | Create Orion subscription(s) that notify persistence layer. |
| UC‑06 | Persist History (P2) | Persistence Service | On notification | Store updates in DB for later analysis. |
| UC‑07 | Visualise Data (P2) | Dashboard Viewer | Investigate trends | View time series and maps for environment/traffic. |

---

## 6. Detailed Use Cases (Phase 1 focus)

### UC‑01: Register Device
**Primary Actor:** Developer/User  
**Preconditions:** IoT Agent and Orion are running; network reachable.  
**Main Flow:**
1. Developer posts device configuration to IoT Agent (device ID, entity type, attributes, transport).
2. IoT Agent stores registration, exposing endpoints/keys as needed.
3. Confirmation returned with device details.

**Alternate/Exceptions:**
- A1: Invalid schema → IoT Agent returns error; Developer fixes payload.
- A2: Orion unreachable → Retry/back‑off; log error.

**Success Outcome:** Device accepted; subsequent readings are mapped to the target NGSI entity in Orion.

---

### UC‑02: Send Sensor Reading
**Primary Actor:** Simulator  
**Preconditions:** Device registered; IoT Agent + Orion healthy.  
**Main Flow:**
1. Simulator emits a measurement built from a time‑based function (e.g., sin wave + noise; or dependency on traffic index).
2. Message delivered to IoT Agent (HTTP or MQTT).
3. IoT Agent transforms and upserts the corresponding entity/attribute in Orion.
4. Orion acknowledges update.

**Postconditions:** Orion reflects the latest state of the entity.

**Quality Constraints:** Median end‑to‑end latency ≤ 500 ms on local machine under nominal load.

---

### UC‑03: Query Current State
**Primary Actor:** Developer/User  
**Preconditions:** Entities exist in Orion.  
**Main Flow:**
1. Developer issues a REST GET for entity or attribute (e.g., `/v2/entities?type=AirQualityObserved`).
2. Orion returns current values and metadata (timestamps; optionally location).

**Alternate:** Filter by geo or attribute to narrow results.

**Success Outcome:** Operator can verify ingestion correctness and sanity of curves.

---

### UC‑04: Configure Curves
**Primary Actor:** Developer/User  
**Preconditions:** Simulator supports config file(s).  
**Main Flow:**
1. Developer edits `simulators/config.yml` to set baselines, amplitudes, periods, phases, noise, and dependencies (e.g., `CO2 = f(traffic_mavg)`).
2. Simulator hot‑reloads or restarts and applies new parameters.
3. Subsequent readings follow updated dynamics.

**Non‑Functional:** Documentation explains parameter meanings and sensible ranges.

---

## 7. Data Model (Initial)

### 7.1 Entity Types (NGSI‑v2 for Phase 1)
- **AirQualityObserved**
  - `id` (URN) • `type` • `co2` (Number) • `no2` (Number) • `pm25` (Number) • `location` (geo:point) • `area` (Text) • `dateObserved` (DateTime)
- **TrafficFlowObserved** (or custom `TrafficSensor`)
  - `id` • `type` • `intensity` (Number) • `speed` (Number) • `congestionIndex` (Number 0–1) • `location` • `lane/segmentId` • `dateObserved`

> Note: Keep Phase 1 simple; adopt Smart Data Models naming later if desired.

### 7.2 Identity & Naming
- Entity IDs: `urn:ngsi-ld:<Type>:<AreaOrSegment>:<Seq>` (e.g., `urn:ngsi-ld:AirQualityObserved:Downtown:001`).
- Attributes follow NGSI conventions (`Number`, `Text`, `DateTime`, `geo:point`).

---

## 8. Acceptance Criteria (per Phase)

### Phase 1 (MVP)
- AC‑1: From a clean clone, `docker compose up` starts Orion, MongoDB, IoT Agent without manual hacks.
- AC‑2: Running the simulator for 5 minutes results in ≥ 60 successful updates per entity.
- AC‑3: A manual GET from Orion returns plausible values (e.g., rush‑hour traffic peaks, nightly lows).

### Phase 2 (Persistence & Visuals)
- AC‑P2‑1: Historical updates appear in DB tables or time‑series store.
- AC‑P2‑2: At least one dashboard shows a 24‑hour pattern for traffic/environment.

---

## 9. Prioritisation (MoSCoW)
- **Must**: UC‑01, UC‑02, UC‑03, baseline entity models, runnable Compose stack.
- **Should**: UC‑04 parameterised curves, basic health endpoints, seed data.
- **Could**: Basic subscription hooks for future persistence; minimal map visual.
- **Won’t (now)**: AuthN/AuthZ, multi‑tenant, advanced NGSI‑LD relationships.

---

## 10. Risks & Assumptions
- **Assumptions**: Local Docker resources are sufficient; network ports not conflicting; stable versions of Orion/IoT Agent.
- **Risks**: Over‑modelling simulation complexity; scope creep beyond Phase 1; config drift.
- **Mitigations**: Keep curve presets; tag releases per phase; store configs in VCS.

---

## 11. Open Questions
- Choose IoT Agent: JSON (simplicity) vs MQTT (closer to real IoT). For Phase 1, default to JSON.
- Decide on entity naming scheme and geographic granularity (segments vs zones).
- Pick persistence path for Phase 2: Cygnus→Postgres or QuantumLeap→TimescaleDB.

---

## 12. Traceability
- FR‑1 ↔ UC‑01/02; FR‑2 ↔ UC‑02; FR‑3 ↔ Entity Models; FR‑4 ↔ UC‑04; FR‑5 ↔ UC‑03; FR‑6/7 ↔ UC‑05–07.

---

## 13. Glossary
- **NGSI**: FIWARE API spec for context data.
- **Entity**: A digital representation of a real‑world thing (sensor, segment, zone).
- **Attribute**: A property of an entity (e.g., `co2`, `speed`).
- **Subscription**: Orion rule to notify external systems when context changes.

