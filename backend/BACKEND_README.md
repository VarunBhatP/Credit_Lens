# CreditLens Backend — Handoff README

## What Has Been Built (Day 1 & Day 2 Complete)

### ML Models (Kaggle Notebooks)
Two XGBoost models trained and saved as `.pkl` files:

| File | Purpose | Dataset Used | AUC |
|------|---------|--------------|-----|
| `credit_score_model.pkl` | Predicts default probability → maps to 300-900 credit score | Home Credit Default Risk (Kaggle) | 0.757 |
| `feature_columns.pkl` | 32 column names credit model expects | — | — |
| `loan_eligibility_model.pkl` | Predicts if user can repay a specific loan | Lending Club (Kaggle) | 0.733 |
| `loan_feature_columns.pkl` | 38 column names loan model expects | — | — |

All 4 files are in `backend/ml_models/`.

### FastAPI Endpoints (backend/main.py)
Server runs on `http://127.0.0.1:8000`. Test all endpoints at `http://127.0.0.1:8000/docs`.

#### POST `/auth/register`
Creates a borrower or lender account.
```json
Input:
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "password": "securepassword",
  "role": "borrower"
}
Output: { "message": "User registered successfully", "user_id": 1 }
```

#### POST `/auth/login`
Authenticates a user and returns a JWT token.
```json
Input:
{
  "email": "jane@example.com",
  "password": "securepassword"
}
Output: { "access_token": "...", "token_type": "bearer" }
```

#### GET `/me`
Retrieves details of the currently authenticated user. (Requires authentication token)

#### GET `/borrower`
Retrieves borrower dashboard details. (Requires borrower authorization token)

#### GET `/lender`
Retrieves lender dashboard details. (Requires lender authorization token)

#### POST `/score`
Takes user financial profile → saves to database and returns credit score (300-900). (Requires borrower authorization token)
```json
Input:
{
  "amt_income_total": 180000,
  "amt_credit": 450000,
  "amt_annuity": 22500,
  "days_birth": -12000,
  "days_employed": -2000,
  "ext_source_2": 0.65,
  "ext_source_3": 0.55
}
Output: { "credit_score": 617.1, "status": "ok" }
```

#### POST `/explain`
Same input as `/score` → returns which features are helping/hurting the score.
```json
Output:
{
  "helping": [{"feature": "AMT_ANNUITY", "impact": -0.69}],
  "hurting": [{"feature": "EXT_SOURCE_2", "impact": 0.75}]
}
```
Note: negative impact = helping (pushing away from default), positive = hurting.

#### POST `/eligibility`
Takes credit score + loan details → returns if eligible and recommended amount.
```json
Input:
{
  "credit_score": 617,
  "loan_amnt": 50000,
  "term": 36,
  "annual_inc": 180000,
  "dti": 15.5
}
Output:
{
  "default_probability": 0.097,
  "eligible": true,
  "recommended_amount": 50000
}
```
Logic: eligible if default_probability < 0.3. If not eligible, recommended = 70% of requested.

#### POST `/roadmap`
Maps weak SHAP features to action plans.
```json
Input:
{
  "hurting": [{"feature": "EXT_SOURCE_2", "impact": 0.75}]
}
Output:
{
  "3_months": ["Pay utility bills on time."],
  "6_months": ["Maintain regular digital transactions."],
  "12_months": ["Build consistent repayment behaviour."]
}
```

#### POST `/lender/select/{lender_id}`
Allows a borrower to select a lender. (Requires borrower authorization token)

#### GET `/lender/applicants`
Returns applicants who selected this lender, with optional risk tier filtering. (Requires lender authorization token)
```json
Query parameters: risk (Green/Yellow/Red)
Output: [
  {
    "id": 1,
    "name": "Jane Doe",
    "email": "jane@example.com",
    "score": 617.1,
    "risk_tier": "Yellow"
  }
]
```

### Synthetic UPI Generator (backend/synthetic_upi.py)
Generates fake but realistic UPI transaction CSV for demo purposes.
```bash
python synthetic_upi.py
# outputs sample_upi.csv with 200 rows
```
Columns: UPI ID, Date, Description, Type (Credit/Debit), Amount, Balance.

---

## Project Structure
```
creditlens/
├── backend/
│   ├── auth/                ← JWT auth, hashing & oauth2 dependency injection
│   ├── ml_models/           ← Saved XGBoost models & feature columns
│   ├── models/              ← SQLAlchemy DB models (user, score, lender selection)
│   ├── routers/             ← Auth and Lender API routes
│   ├── schemas/             ← Pydantic validation schemas
│   ├── database.py          ← SQLAlchemy setup & db session generator
│   ├── main.py              ← FastAPI app (All endpoints, db tables initialization)
│   ├── roadmap.py           ← Credit Improvement Roadmap Engine logic
│   ├── synthetic_upi.py     ← UPI CSV generator
│   └── requirements.txt
├── frontend/                ← React app (Day 3)
└── notebooks/               ← Kaggle notebooks reference
```

---

## How to Run

```bash
# From CreditLens root
cd backend

# Activate venv (Windows)
venv\Scripts\activate

# Start server
uvicorn main:app --reload
```

---

## Day 2 Tasks (Backend Completion) - COMPLETED

All tasks for Day 2 have been successfully implemented:

### 1. Credit Improvement Roadmap Engine — `backend/roadmap.py` [COMPLETED]
Rule-based engine (no LLM). Maps weak SHAP features to action plans.
- Input: list of hurting features from `/explain`
- Output: actions for 3 month, 6 month, 12 month timelines
- Example: `DAYS_EMPLOYED` hurting → "Stay at current job for 6+ months"
- Example: `EXT_SOURCE_2` hurting → "Clear any outstanding utility bills"

### 2. PostgreSQL DB Schema [COMPLETED]
Create these tables:
- `users` — id, name, email, password_hash, role (borrower/lender)
- `scores` — id, user_id, score, timestamp
- `lender_selections` — borrower_id, lender_id, selected_at

### 3. JWT Auth Endpoints [COMPLETED]
- `POST /register` — create borrower or lender account
- `POST /login` — returns JWT token
- Role-based: borrowers see their own data, lenders see only applicants who chose them

### 4. Lender Dashboard Endpoints [COMPLETED]
- `GET /lender/applicants` — returns applicants who selected this lender
- Filter by risk tier: Green (score > 700), Yellow (500-700), Red (< 500)

---

## Day 3 Tasks (Frontend)

Work in `frontend/` folder. React app with two views:

### Borrower Portal (7-step journey)
1. Onboarding (name, income, employment)
2. Document Upload (UPI CSV)
3. Score Reveal (animated number from 300-900)
4. Score Breakdown (SHAP helping/hurting list in plain English)
5. Improvement Roadmap (3/6/12 month plan)
6. Loan Simulator (enter amount + tenure → eligibility result)
7. Monthly Health Monitor (score over time graph)

### Lender Dashboard
- Login as lender
- See applicants who selected them
- Filter by Green/Yellow/Red risk tier
- Click applicant to see their score breakdown

### Demo Script (User A vs User B contrast)
- User A: salaried, CIBIL 750 → gets loan everywhere
- User B: Swiggy delivery partner, Jan Dhan account, consistent UPI activity → CIBIL says no history, CreditLens scores at 694, recommends ₹40,000 at 16% interest tier

---

## Prompt to Use with Claude for Day 2

```
We are building CreditLens — a credit scoring platform for thin-file borrowers in India.
Day 1 is complete: two XGBoost models trained (credit score + loan eligibility),
SHAP explainability working, FastAPI with /score, /eligibility, /explain endpoints done.
Now starting Day 2. Help me build:
1. Credit Improvement Roadmap engine in backend/roadmap.py (rule-based, no LLM)
2. PostgreSQL DB schema (users, scores, lender_selections tables)
3. JWT auth with borrower/lender roles (/register, /login endpoints)
4. Lender dashboard endpoints with risk tier filters
Mentor me — don't give full code, guide me step by step and correct me when I go wrong.
```

## Prompt to Use with Claude for Day 3

```
We are building CreditLens — a credit scoring platform for thin-file borrowers in India.
Day 1 and Day 2 are complete: ML models, FastAPI backend with all endpoints, JWT auth,
PostgreSQL schema, roadmap engine, and lender dashboard endpoints are all done.
Now starting Day 3. Help me build:
1. React borrower portal with 7-step user journey
2. Lender dashboard UI with risk tier filters
3. Score reveal animation (emotional hook for judges)
4. Demo prep with User A vs User B contrast script
Guide me step by step, correct mistakes, and keep the demo story tight.
```

---

## Key Concepts to Know

| Term | Meaning |
|------|---------|
| Thin-file borrower | Has bank account but no loan/credit history |
| CIBIL | India's credit bureau — ignores thin-file users |
| SHAP | Explains which features pushed the ML score up or down |
| scale_pos_weight | XGBoost parameter to handle imbalanced datasets |
| feature_columns.pkl | Saved column order — must match exactly at prediction time |
| OCEN | Open Credit Enablement Network — our lender marketplace mirrors this |
| Account Aggregator | RBI framework for consented financial data sharing — our production path |
