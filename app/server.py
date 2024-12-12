import datetime

import crud
import pydantic
from constants import STATUS_DELETED
from dependency import SessionDependency
from fastapi import FastAPI, Query
from lifespan import lifespan
from models import Advertisement
from schema import (
    CreateAdsRequest,
    CreateAdsResponse,
    DeleteAdsResponse,
    GetAdsResponse,
    IdResponseBase,
    StatusResponse,
    UpdateAdsRequest,
    UpdateAdsResponse,
)

app = FastAPI(
    title="Advertisements API",
    terms_of_service="",
    description="Sell or Buy advertisements",
    lifespan=lifespan,
)

"""
Создание: POST /advertisement
Обновление: PATCH /advertisement/{advertisement_id}
Удаление: DELETE /advertisement/{advertisement_id}
Получение по id: GET  /advertisement/{advertisement_id}
Поиск по полям: GET /advertisement?{query_string}
"""


@app.post("/advertisement", response_model=CreateAdsResponse, tags=["advertisements"])
async def create_item(item: CreateAdsRequest, session: SessionDependency):
    ad = Advertisement(
        title=item.title,
        description=item.description,
        price=item.price,
        author=item.author,
    )
    await crud.add_item(session, ad)
    return ad.id_dict


@app.patch("/advertisement/{advertisement_id}", response_model=UpdateAdsResponse, tags=["advertisements"])
async def update_item(advertisement_id: int, item: UpdateAdsRequest, session: SessionDependency):
    json_data = item.dict(exclude_unset=True, by_alias=True)
    ad = await crud.get_item_by_id(session, Advertisement, advertisement_id)
    for key, value in json_data.items():
        setattr(ad, key, value)
    await crud.add_item(session, ad)
    return ad.id_dict


@app.delete("/advertisement/{advertisement_id}", response_model=DeleteAdsResponse, tags=["advertisements"])
async def delete_item(advertisement_id: int, session: SessionDependency):
    ad = await crud.get_item_by_id(session, Advertisement, advertisement_id)
    await crud.add_item(session, ad)
    return STATUS_DELETED


@app.get("/advertisement/{advertisement_id}", response_model=GetAdsResponse, tags=["advertisements"])
async def get_item(advertisement_id: int, session: SessionDependency):
    ad = await crud.get_item_by_id(session, Advertisement, advertisement_id)
    return ad.dict


@app.get("/advertisement", response_model=list[GetAdsResponse], tags=["advertisements"])
async def get_advertisement(session: SessionDependency,
                            title: str = Query(None),
                            description: str = Query(None),
                            price: int = Query(None),
                            author: int = Query(None)):
    search_params = {}
    if title:
        search_params["title"] = title
    if description:
        search_params["description"] = description
    if price:
        search_params["price"] = price
    if author:
        search_params["author"] = author

    ad = await crud.get_items_by_params(session, Advertisement, **search_params)
    return ad.scalars().all()
