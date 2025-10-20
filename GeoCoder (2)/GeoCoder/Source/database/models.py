from typing import Any, Optional

try:
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
    from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

    engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")
    async_session = async_sessionmaker(engine)


    class Base(AsyncAttrs, DeclarativeBase):
        pass


    class Address(Base):
        __tablename__ = "addresses"

        id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
        input_query: Mapped[str] = mapped_column(unique=True)
        full_address: Mapped[str] = mapped_column()
        latitude: Mapped[float] = mapped_column()
        longitude: Mapped[float] = mapped_column()


    async def init_db() -> None:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

except ModuleNotFoundError:
    async_session = None  # type: ignore


    class Address:
        input_query = None
        full_address = None
        latitude = None
        longitude = None

        def __init__(self, input_query: str = None, full_address: str = None, latitude: float = None, longitude: float = None):
            self.input_query = input_query
            self.full_address = full_address
            self.latitude = latitude
            self.longitude = longitude


    async def init_db() -> None:
        return None
