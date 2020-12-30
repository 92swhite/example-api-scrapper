import os
from sqlalchemy import create_engine


class DbHandler:
    def __init__(self) -> None:
        self.engine = self.__get_engine()

    def __get_engine(self):
        thing = create_engine(
            f"postgresql://\
            {os.environ['DB_USERNAME']}:\
            {os.environ['DB_PASSWORD']}@\
            {os.environ['DB_SERVER']}:\
            {os.environ['DB_PORT']}/\
            {os.environ['DB_DATABASE']}"
        )
        print(type(thing))
