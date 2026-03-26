# BrainDrive - Credit Scorer 

BrainDrive is a credit scoring system designed for "thin-file" users (those without traditional credit history). It leverages alternative data signals—such as UPI transaction frequency, utility payment streaks, and mobile recharges—to generate explainable credit scores using XGBoost and LLM-powered narratives.

## 🏗 Architecture: Modular Monolith

The project follows a **Modular Monolith** pattern. This ensures that while the application is a single deployable unit, the domain logic is strictly isolated into modules, sharing a unified "Infrastructure Core."

### High-Level Design
- **The Core (`app/core`)**: Shared infrastructure including Database sessions, Supabase Authentication, and Global Configuration.
- **The Modules (`app/modules`)**: Domain-specific logic. Currently, the `scoring` module handles all credit-related operations.
- **The Point of Contact**: The PostgreSQL database (Supabase) serves as the central integration point for all modules.

---

## 🛠 Tech Stack
- **Framework**: FastAPI (Python 3.12+)
- **Database**: PostgreSQL (via Supabase)
- **ORM/Query**: SQLAlchemy 2.0 (with **Raw SQL** for performance)
- **Authentication**: Supabase Auth (JWT-based)
- **Validation**: Pydantic v2
- **ML (Planned)**: XGBoost + SHAP
- **LLM (Planned)**: gemini API

---

## 🚀 Key Features Implemented

### 1. Context-Aware Authentication
We use a custom `authenticate_user` dependency that decodes Supabase JWTs. Instead of passing the `user_id` through every function, we use **Python `ContextVar`** to inject the ID into the request-local context. 
- **Benefit**: Any service can call `get_current_user_id()` and magically receive the authenticated UUID without explicit parameter passing.

### 2. Clean DB Layer (Raw SQL)
While we use SQLAlchemy for schema management, the business logic in `ScoringService` uses **Native SQL Queries**. 
- **Benefit**: Maximum performance, precise control over joins, and full utilization of PostgreSQL features like `RETURNING id`.

### 3. Automatic Schema Management
The application uses the modern FastAPI `lifespan` handler to automatically check and create missing database tables (`profiles`, `applications`, `scores`) upon server startup.

### 4. Modular Scoring Domain
- **`POST /api/v1/scoring/apply`**: Validates alternative data signals and saves the application.
- **`GET /api/v1/scoring/my-scores`**: Retrieves the scoring history strictly for the authenticated user.

---

## 📂 Project Structure
```text
app/
├── core/                # Shared Infrastructure
│   ├── auth.py          # JWT extraction & ContextVar injection
│   ├── config.py        # Pydantic Settings
│   └── db/              # SQLAlchemy Engine & Unified Schema
├── modules/             # Domain-Specific Modules
│   └── scoring/         # Credit Scoring Domain
│       ├── router.py    # Module-specific API Endpoints
│       ├── service.py   # Raw SQL Business Logic
│       └── schemas.py   # Pydantic Request/Response Models
└── main.py              # Application Hub (Lifespan & Routing)
```

---

## 📝 Setup
1. **Environment**: Create a `.env` file with:
   ```env
   DATABASE_URL=postgresql+asyncpg://...
   SUPABASE_URL=...
   SUPABASE_KEY=...
   SUPABASE_JWT_SECRET=...
   ```
2. **Install Dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy asyncpg pyjwt pydantic-settings
   ```
3. **Run**:
   ```bash
   uvicorn app.main:app --reload
   ```
