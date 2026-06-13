from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import io
import joblib
import pandas as pd
import numpy as np
import shap
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_borrower)
):
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
    
    amt_credit = df[df['Type'] == 'Credit']['Amount'].sum()
    amt_annuity = df[df['Type'] == 'Debit']['Amount'].mean() if len(df[df['Type'] == 'Debit']) > 0 else 0
    
    # EXT_SOURCE derivation from UPI data
    total_txns = len(df)
    credit_ratio = len(df[df['Type'] == 'Credit']) / total_txns if total_txns > 0 else 0
    avg_balance = df['Balance'].mean()
    ext_source_2 = float(round(min(credit_ratio * 1.5, 1.0), 2))
    ext_source_3 = float(round(min(avg_balance / 10000, 1.0), 2))

    db_user = db.query(User).filter(User.id == current_user["id"]).first()
    if db_user:
        db_user.amt_credit = int(amt_credit)
        db_user.amt_annuity = int(amt_annuity)
        db_user.ext_source_2 = ext_source_2   # add this
        db_user.ext_source_3 = ext_source_3   # add this
        db.commit()
    
    return {
        "message": "Document processed successfully",
        "amt_credit": amt_credit,
        "amt_annuity": amt_annuity,
        "ext_source_2": ext_source_2,
        "ext_source_3": ext_source_3
    }
@app.post('/score')
def get_credit_score(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_borrower)
):
    db_user = db.query(User).filter(User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    input_data = pd.DataFrame([{
        "AMT_INCOME_TOTAL": db_user.income or 180000,
        "AMT_CREDIT": db_user.amt_credit or 450000,
        "AMT_ANNUITY": db_user.amt_annuity or 22500,
        "DAYS_BIRTH": (db_user.age * -365) if db_user.age else -12000,
        "DAYS_EMPLOYED": (db_user.employment_days * -1) if db_user.employment_days else -2000,
        "EXT_SOURCE_2": db_user.ext_source_2 or 0.3,
        "EXT_SOURCE_3": db_user.ext_source_3 or 0.55
    }])

    for col in credit_columns:
        if col not in input_data.columns:
            input_data[col] = 0

    input_data = input_data[credit_columns]

    score = 900 - (
        credit_model.predict_proba(input_data)[:, 1][0] * 600
    )

    new_score = Score(
        user_id=current_user["id"],
        score=round(float(score))
    )

    db.add(new_score)
    db.commit()

    return {
        "credit_score": round(float(score)),
        "status": "ok"
    }

from roadmap import generate_roadmap, get_feature_message
@app.post('/explain')
def explain_score(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_borrower)
):
    db_user = db.query(User).filter(User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    input_data = pd.DataFrame([{
        "AMT_INCOME_TOTAL": db_user.income or 180000,
        "AMT_CREDIT": db_user.amt_credit or 450000,
        "AMT_ANNUITY": db_user.amt_annuity or 22500,
        "DAYS_BIRTH": (db_user.age * -365) if db_user.age else -12000,
        "DAYS_EMPLOYED": (db_user.employment_days * -1) if db_user.employment_days else -2000,
        "EXT_SOURCE_2": db_user.ext_source_2 or 0.5,
        "EXT_SOURCE_3": db_user.ext_source_3 or 0.5
    }])

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
        {
            "feature": f,
            "message": get_feature_message(f, "good"),
            "impact": float(v)
        }
        for f, v in helping
    ],
    "hurting": [
        {
            "feature": f,
            "message": get_feature_message(f, "bad"),
            "impact": float(v)
        }
        for f, v in hurting
    ]
}


class LoanInput(BaseModel):
    loan_amnt: float
    term: int

@app.post("/eligibility")
def check_eligibility(
    input: LoanInput,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_borrower)
):
    db_user = db.query(User).filter(User.id == current_user["id"]).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    latest_score = db.query(Score).filter(Score.user_id == current_user["id"]).order_by(Score.timestamp.desc()).first()
    score_val = latest_score.score if latest_score else 600.0
    annual_inc = db_user.income or 0.0
    dti = (db_user.amt_annuity / (annual_inc / 12)) if annual_inc > 0 else 0.0
    if annual_inc > 0 and input.loan_amnt > (annual_inc * 0.4):
        return {
        "default_probability": 1.0,
        "eligible": False,
        "recommended_amount": float(annual_inc * 0.3),
        "reason": "Loan amount exceeds 40% of annual income"
    }

    input_data = pd.DataFrame([{
        "credit_score": score_val,
        "loan_amnt": input.loan_amnt,
        "term": input.term,
        "annual_inc": annual_inc,
        "dti": dti
    }])
    
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

@app.get("/borrower/notifications")
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_borrower)
):
    selections = db.query(LenderSelection).filter(
        LenderSelection.borrower_id == current_user["id"]
    ).all()
    results = []
    for s in selections:
        lender = db.query(User).filter(User.id == s.lender_id).first()
        results.append({
            "lender_name": lender.name if lender else "Unknown",
            "status": s.status or "pending"
        })
    return results

@app.get("/lenders")
def get_all_lenders(db: Session = Depends(get_db)):
    lenders = db.query(User).filter(User.role == "lender").all()
    return [{"id": l.id, "name": l.name} for l in lenders]
