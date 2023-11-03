"""Modules for API creation, func from fraud detection and schemas"""
from datetime import datetime
from fastapi import FastAPI, Depends
# from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from .model_estimate import Estimation
from .model_predict import Baseline
from .schemas import (CostResponse, LossResponse,
                      PredictResponse, PredictRequest,
                      ErrorType, BaselineType)
from .models import FRAUDORNOT
from .database import engine, SessionLocal

app = FastAPI()
FRAUDORNOT.metadata.create_all(bind=engine)

estimation = Estimation()
baseline_class = Baseline()


def get_db():
    """
    Def for connection with DB
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    """
    API GET first request
    :return: string message
    """
    return {"message": "Hello! This is the fraud detector."}


@app.get("/cost/{error_type}", response_model=CostResponse)
async def get_cost(error_type: ErrorType):
    """
    Def for receiving cost of error type
    :param error_type: 'false-positive' or 'false-negative'
    :return: cost of error type
    """
    cost_error = {
        ErrorType.FALSE_POSITIVE: 10000,
        ErrorType.FALSE_NEGATIVE: 75000,
    }

    if error_type in cost_error:
        return {"cost": cost_error[error_type]}
    # raise HTTPException(status_code=404, detail="Error type not found")


@app.get("/loss/{baseline}", response_model=LossResponse)
async def get_loss(baseline: BaselineType):
    """
    Def for counting loss for each baseline
    :param baseline: 'constant-clean', 'constant-fraud', 'first-hypothesis'
    :return: daily loss for baseline
    """
    losses = estimation.daily_loss(baseline)
    return {"losses": losses}


@app.post("/predict/{baseline}", response_model=PredictResponse)
async def post_predict(
    baseline: BaselineType,
    text: PredictRequest,
    db: Session = Depends(get_db)
):
    """
    Def for detecting fraud in message
    :param baseline: 'constant-clean', 'constant-fraud', 'first-hypothesis'
    :param text: message for detecting
    :param db: db for predictions
    :return: 'clean' or 'fraud' result
    """

    prediction = baseline_class.prediction(baseline, text.text)

    # Store the prediction and input text in the database
    message = FRAUDORNOT(
        message_text=text.text,
        prediction=prediction,
        used_base_line=baseline,
        request_time=datetime.now()
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    return message


@app.get("/get_latest_entry/{baseline}")
async def get_latest_entry(baseline: str, db: Session = Depends(get_db)):
    """
    Def for getting last entry in DB
    :param baseline: 'constant-clean', 'constant-fraud', 'first-hypothesis'
    :param db: db for predictions
    :return: latest_entry
    """
    latest_entry = (
        db.query(FRAUDORNOT)
        .filter(FRAUDORNOT.used_base_line == baseline)
        .order_by(FRAUDORNOT.id.desc())
        .first()
    )

    if latest_entry:
        return {
            "message_text": latest_entry.message_text,
            "prediction": latest_entry.prediction,
            "used_base_line": latest_entry.used_base_line,
            "request_time": latest_entry.request_time
        }

    return {"message": "No entry found for the specified baseline."}


@app.get("/get_number_of_entries")
async def get_number_of_entries(db: Session = Depends(get_db)):
    """
       Def for getting number of entries in db
       :param db:  for predictions
       :return: number of entries
       """
    result = (
        db.query(FRAUDORNOT.used_base_line,
                 # pylint: disable=E1102
                 func.count().label("count_entries"))  # noqa
        .group_by(FRAUDORNOT.used_base_line)
        .all()
    )
    count_entries = {row[0]: row[1] for row in result}

    return count_entries
