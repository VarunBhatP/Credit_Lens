from fastapi import FastAPI
import joblib
import pandas as pd
import numpy as np
import shap
from pydantic import BaseModel
app = FastAPI()

from roadmap import generate_roadmap

from database import engine
from models.user import User
from models.score import Score
from models.lender_selection import LenderSelection
from routers.auth_router import router as auth_router
from routers.lender_router import router as lender_router
from auth.oauth2 import get_current_user, get_current_borrower, get_current_lender
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db

User.metadata.create_all(bind=engine)
Score.metadata.create_all(bind=engine)
LenderSelection.metadata.create_all(bind=engine)

credit_model = joblib.load('ml_models/credit_score_model.pkl')
credit_columns = joblib.load('ml_models/feature_columns.pkl')
loan_model = joblib.load('ml_models/loan_eligibility_model.pkl')
loan_columns = joblib.load('ml_models/loan_feature_columns.pkl')

class UserInput(BaseModel):
    amt_income_total: float
    amt_credit: float
    amt_annuity: float
    days_birth: int
    days_employed: int
    ext_source_2: float
    ext_source_3: float

class LoanInput(BaseModel):
    credit_score: float
    loan_amnt: float
    term: int
    annual_inc: float
    dti: float

class RoadmapInput(BaseModel):
    hurting: list

app.include_router(auth_router)
app.include_router(lender_router)

@app.get("/me")
def me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/borrower")
def borrower_dashboard(
    current_user=Depends(get_current_borrower)
):
    return current_user

@app.get("/lender")
def lender_dashboard(
    current_user=Depends(get_current_lender)
):
    return current_user

@app.post('/score')
def get_credit_score(
    input: UserInput,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_borrower)
):
    input_data = pd.DataFrame([input.dict()])

    for col in credit_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[credit_columns]

    score = 900 - (
        credit_model.predict_proba(input_data)[:, 1][0] * 600
    )

    new_score = Score(
        user_id=current_user["id"],
        score=float(score)
    )

    db.add(new_score)
    db.commit()

    return {
        "credit_score": float(score),
        "status": "ok"
    }


@app.post('/explain')
def explain_score(input: UserInput):
    input_data = pd.DataFrame([input.dict()])

    for col in credit_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[credit_columns]

    explainer = shap.TreeExplainer(credit_model)
    shap_values = explainer.shap_values(input_data)[0]

    shap_series = pd.Series(shap_values, index=credit_columns)

    helping = (
        shap_series.nsmallest(3)
        .reset_index()
        .values.tolist()
    )

    hurting = (
        shap_series.nlargest(3)
        .reset_index()
        .values.tolist()
    )

    return {
        "helping": [
            {"feature": f, "impact": float(v)}
            for f, v in helping
        ],
        "hurting": [
            {"feature": f, "impact": float(v)}
            for f, v in hurting
        ]
    }


@app.post("/eligibility")
def check_eligibility(input: LoanInput):
    input_data = pd.DataFrame([input.dict()])
    for col in loan_columns:
        if col not in input_data.columns:
            input_data[col] = 0
    input_data = input_data[loan_columns]
    prob = float(loan_model.predict_proba(input_data)[:, 1][0])
    eligible = prob < 0.3
    recommended_amount = float(input.loan_amnt) if eligible else float(input.loan_amnt * 0.7)

    return {
        "default_probability": prob,
        "eligible": eligible,
        "recommended_amount": recommended_amount
    }

@app.post("/roadmap")
def get_roadmap(input: RoadmapInput):
    return generate_roadmap(input.hurting)