# import dataclasses

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int]
    username: Mapped[str]
    first_name: Mapped[str | None]
    preferred_location: Mapped[str | None]

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, username={self.username!r}, "
            f"telegram_id={self.telegram_id!r}, first_name={self.first_name!r},"
            f"preferred_location={self.preferred_location!r})"
        )


# @dataclasses.dataclass
# class Weather:
#     name: str
#     temp: int
#     wind: int
#     description: str
