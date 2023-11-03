"""Module for schemas"""
from enum import Enum
from pydantic import BaseModel


# Schema for GET /cost/{error_type}
class CostResponse(BaseModel):
    """
    Class for CostResponse type
    """
    cost: int


# Schema for GET /loss/{baseline}
class LossResponse(BaseModel):
    """
    Class for LossResponse type
    """
    losses: int


# Schemas for POST /predict/{baseline}
class PredictRequest(BaseModel):
    """
    Class for PredictRequest type
    """
    text: str


class PredictResponse(BaseModel):
    """
    Class for PredictResponse type
    """
    prediction: str


class ErrorType(str, Enum):
    """
    Class for only two ErrorType for input
    """
    FALSE_POSITIVE = "false-positive"
    FALSE_NEGATIVE = "false-negative"


class BaselineType(str, Enum):
    """
    Class for three BaselineType in input
    """
    CONSTANT_CLEAN = "constant-clean"
    CONSTANT_FRAUD = "constant-fraud"
    FIRST_HYPOTHESIS = "first-hypothesis"
