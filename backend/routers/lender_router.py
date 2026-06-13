from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from auth.oauth2 import (
    get_current_borrower,
    get_current_lender
)

from models.user import User
from models.lender_selection import LenderSelection
from models.score import Score

router = APIRouter(
    prefix="/lender",
    tags=["Lender"]
)


@router.post("/select/{lender_id}")
def select_lender(
    lender_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_borrower)
):
    lender = (
    db.query(User)
    .filter(
        User.id == lender_id,
        User.role == "lender"
    )
    .first()
    )

    if not lender:
        raise HTTPException(
            status_code=404,
            detail="Lender not found"
        )
    
    existing = (
    db.query(LenderSelection)
    .filter(
        LenderSelection.borrower_id == current_user["id"],
        LenderSelection.lender_id == lender_id
    )
    .first()
)

    if existing:
        return {
            "message": "Already selected"
        }
    
    selection = LenderSelection(
        borrower_id=current_user["id"],
        lender_id=lender_id
    )

    db.add(selection)
    db.commit()
    return {
        "message": "Lender selected successfully"
    }


def get_risk_tier(score):
    if score > 700:
        return "Green"
    elif score >= 500:
        return "Yellow"
    else:
        return "Red"
    
@router.get("/applicants")
def get_applicants(
    risk: str = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_lender)
):
    print("CURRENT USER:", current_user)

    selections = (
        db.query(LenderSelection)
        .filter(
            LenderSelection.lender_id == current_user["id"]
        )
        .all()
    )

    print("SELECTIONS:", selections)

    applicants = []

    for selection in selections:

        borrower = (
            db.query(User)
            .filter(
                User.id == selection.borrower_id
            )
            .first()
        )

        if not borrower:
            continue

        print("BORROWER:", borrower.id)

        latest_score = (
            db.query(Score)
            .filter(
                Score.user_id == borrower.id
            )
            .order_by(Score.timestamp.desc())
            .first()
        )

        print("LATEST SCORE:", latest_score)

        # If borrower has no score, skip them
        if latest_score is None:
            continue

        tier = get_risk_tier(latest_score.score)

        # Apply optional risk filter
        if risk is not None and tier != risk:
            continue

        applicants.append(
            {
                "id": borrower.id,
                "name": borrower.name,
                "email": borrower.email,
                "score": float(latest_score.score),
                "risk_tier": tier,
                "income": borrower.income or 0,
                "employment_days": borrower.employment_days or 0,
                "status": selection.status or "pending"
            }
        )

    return applicants

@router.get("/applicant/{applicant_id}")
def get_applicant(
    applicant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_lender)
):
    selection = db.query(LenderSelection).filter(
        LenderSelection.lender_id == current_user["id"],
        LenderSelection.borrower_id == applicant_id
    ).first()
    
    if not selection:
        raise HTTPException(status_code=403, detail="Not authorized to view this applicant")
        
    borrower = db.query(User).filter(User.id == applicant_id).first()
    latest_score = db.query(Score).filter(Score.user_id == applicant_id).order_by(Score.timestamp.desc()).first()
    
    return {
        "id": borrower.id,
        "name": borrower.name,
        "email": borrower.email,
        "score": round(float(latest_score.score), 1),
        "risk_tier": get_risk_tier(latest_score.score) if latest_score else "Yellow",
        "income": f"₹ {borrower.income or 0} / year",
        "employment": f"{borrower.employment_days or 0} days",
        "explainData": {
            "helping": [
                {"feature": "EXT_SOURCE_2", "impact": -0.38},
                {"feature": "AMT_ANNUITY", "impact": -0.29}
            ],
            "hurting": [
                {"feature": "DAYS_EMPLOYED", "impact": 0.44},
                {"feature": "AMT_CREDIT", "impact": 0.21}
            ]
        }
    }

@router.post("/applicant/{applicant_id}/accept")
def accept_applicant(
    applicant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_lender)
):
    selection = db.query(LenderSelection).filter(
        LenderSelection.lender_id == current_user["id"],
        LenderSelection.borrower_id == applicant_id
    ).first()
    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")
    selection.status = "accepted"
    db.commit()
    return {"message": "Applicant accepted"}

@router.post("/applicant/{applicant_id}/reject")
def reject_applicant(
    applicant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_lender)
):
    selection = db.query(LenderSelection).filter(
        LenderSelection.lender_id == current_user["id"],
        LenderSelection.borrower_id == applicant_id
    ).first()
    if not selection:
        raise HTTPException(status_code=404, detail="Selection not found")
    selection.status = "rejected"
    db.commit()
    return {"message": "Applicant rejected"}