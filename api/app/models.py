from sqlmodel import SQLModel, Field


class Greeting(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    lang: str
    message: str
