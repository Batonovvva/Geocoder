from typing import Optional

from Source.database.models import async_session, Address

try:
    from sqlalchemy import select  # type: ignore
except ModuleNotFoundError:
    class _SelectStub:
        def __init__(self, *args, **kwargs):
            self.args = args

        def where(self, *args, **kwargs):
            return self

    def select(*args, **kwargs):
        return _SelectStub(*args, **kwargs)


async def return_address_if_exist(query: str) -> Optional[Address]:
    async with async_session() as session:
        result = await session.execute(select(Address).where(Address.input_query == query))
        return result.scalar_one_or_none()


async def add_new_address(input_query: str, full_address: str, lat: float, lon: float) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add(Address(input_query=input_query, full_address=full_address, latitude=lat, longitude=lon))
