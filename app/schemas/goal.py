from pydantic import BaseModel


class GoalBase(BaseModel):
    pass


class GoalCreate(GoalBase):
    pass


class GoalUpdate(BaseModel):
    pass


class GoalRead(GoalBase):
    id: int

    model_config = {
        "from_attributes": True
    }