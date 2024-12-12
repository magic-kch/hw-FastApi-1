import datetime
from typing import Literal

from pydantic import BaseModel


class IdResponseBase(BaseModel):
    id: int


class StatusResponse(BaseModel):
    status: Literal["deleted"]


class GetAdsResponse(BaseModel):
    id: int
    title: str
    description: str
    price: int
    author: int
    created_at: datetime.datetime


class CreateAdsRequest(BaseModel):
    title: str
    description: str
    price: int
    author: int


class CreateAdsResponse(IdResponseBase):
    pass


class UpdateAdsRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None


class UpdateAdsResponse(IdResponseBase):
    pass


class DeleteAdsResponse(StatusResponse):
    pass
