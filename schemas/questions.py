from pydantic import BaseModel, Field

class QuestionCreate(BaseModel):
    text: str = Field(..., min_length=10) # ... = required


class QuestionResponse(BaseModel):
    id: int
    text: str
