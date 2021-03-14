import os
from typing import Dict, List, Any, Counter
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine  # type: ignore
from sqlalchemy.orm.session import Session as SQLAlchemySession  # type: ignore
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from .db_tables import (  # type: ignore
    Base,
    NewReleases,
    Artists,
    NewReleasesArtistsBridge,
    AvailableMarkets,
)


class DbHandler:
    def __init__(self) -> None:
        self.engine = self.__get_engine()
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

    def __get_engine(self) -> SQLAlchemyEngine:
        conn_string = (
            "postgresql+asyncpg://"
            f"{os.environ['DB_USERNAME']}:"
            f"{os.environ['DB_PASSWORD']}@"
            f"{os.environ['DB_SERVER']}:"
            f"5432/"
            f"{os.environ['DB_DATABASE']}"
        )
        return create_async_engine(conn_string)

    async def reset_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    def __get_table_keys(self, table) -> List[str]:
        keys = table.__table__.columns.keys()
        keys.remove("last_updated")
        return keys

    def __get_record_instance(self, data: Dict[str, Any], table):
        row = {key: data[key] for key in self.__get_table_keys(table)}
        return table(**row)

    async def __upsert_row(self, data: dict, table, session: SQLAlchemySession) -> None:
        row = self.__get_record_instance(data, table)
        await session.merge(row)

    async def handle_new_releases(
        self, new_releases: List[Dict[str, Any]], counter: Counter
    ) -> None:
        async with self.async_session() as session:
            async with session.begin():
                for album in new_releases:
                    album_id = album["id"]
                    counter.update(albums=1)
                    await self.__upsert_row(album, NewReleases, session)
                    for artist in album["artists"]:
                        await self.__upsert_row(artist, Artists, session)
                        artist["album_id"] = album_id
                        artist["artist_id"] = artist["id"]
                        counter.update(artists=1)
                        await self.__upsert_row(
                            artist, NewReleasesArtistsBridge, session
                        )
                    markets = {
                        k: (True if k in album["available_markets"] else False)
                        for k in self.__get_table_keys(AvailableMarkets)
                    }
                    markets["album_id"] = album_id
                    await self.__upsert_row(markets, AvailableMarkets, session)
            await session.commit()
