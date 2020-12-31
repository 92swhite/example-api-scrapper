import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine as SQLAlchemyEngine
from sqlalchemy.orm.session import Session as SQLAlchemySession


class DbHandler:
    def __init__(self) -> None:
        self.engine = self.__get_engine()
        self.session = self.__get_session()

    def __get_engine(self) -> SQLAlchemyEngine:
        return create_engine(
            f"postgresql://\
            {os.environ['DB_USERNAME']}:\
            {os.environ['DB_PASSWORD']}@\
            {os.environ['DB_SERVER']}:\
            {os.environ['DB_PORT']}/\
            {os.environ['DB_DATABASE']}"
        )

    def __get_session(self) -> SQLAlchemySession:
        Session = sessionmaker(bind=self.engine)
        return Session()
