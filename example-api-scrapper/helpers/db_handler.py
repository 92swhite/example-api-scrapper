import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine
from sqlalchemy.orm.session import Session as SQLAlchemySession
from .db_tables import NewReleases


class DbHandler:
    def __init__(self) -> None:
        self.engine = self.__get_engine()
        self.session = self.__get_session()

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

    def __upsert_new_releases(self, new_releases: dict) -> None:
        self.session.add(NewReleases(**new_releases))
        print(NewReleases(**new_releases))
        print("starting to commit")
        self.session.commit()
        print("committed!")

    def handle_new_releases(self, new_releases: dict) -> None:
        for album in new_releases:
            self.__upsert_new_releases(
                {key: album[key] for key in NewReleases.__table__.columns.keys()}
            )
