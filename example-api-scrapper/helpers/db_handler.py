import os
from typing import Dict, List, Any, Counter
from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine  # type: ignore
from sqlalchemy.orm.session import Session as SQLAlchemySession  # type: ignore
from sqlalchemy.ext.declarative.api import DeclarativeMeta  # type: ignore
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
        self.session = self.__get_session()
        Base.metadata.create_all(self.engine)

    def __get_engine(self) -> SQLAlchemyEngine:
        conn_string = (
            "postgresql://"
            f"{os.environ['DB_USERNAME']}:"
            f"{os.environ['DB_PASSWORD']}@"
            f"{os.environ['DB_SERVER']}:"
            f"{os.environ['DB_PORT']}/"
            f"{os.environ['DB_DATABASE']}"
        )
        return create_engine(conn_string)

    def __get_session(self) -> SQLAlchemySession:
        Session = sessionmaker(bind=self.engine)
        return Session()

    def __get_table_keys(self, table: DeclarativeMeta) -> List[str]:
        keys = table.__table__.columns.keys()
        keys.remove("last_updated")
        return keys

    def __get_record_instance(self, data: Dict[str, Any], table: DeclarativeMeta):
        row = {key: data[key] for key in self.__get_table_keys(table)}
        return table(**row)

    def __upsert_row(self, data: dict, table: DeclarativeMeta) -> None:
        row = self.__get_record_instance(data, table)
        self.session.merge(row)

    def handle_new_releases(
        self, new_releases: List[Dict[str, Any]], counter: Counter
    ) -> None:
        for album in new_releases:
            album_id = album["id"]
            counter.update(albums=1)
            self.__upsert_row(album, NewReleases)
            for artist in album["artists"]:
                self.__upsert_row(artist, Artists)
                artist["album_id"] = album_id
                artist["artist_id"] = artist["id"]
                counter.update(artists=1)
                self.__upsert_row(artist, NewReleasesArtistsBridge)
            markets = {
                k: (True if k in album["available_markets"] else False)
                for k in self.__get_table_keys(AvailableMarkets)
            }
            markets["album_id"] = album_id
            self.__upsert_row(markets, AvailableMarkets)
        self.session.commit()