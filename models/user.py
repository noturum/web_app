from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column
from passlib.context import CryptContext
from models.base import BaseOrmModel, db_controller

crypt_pass = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(BaseModel):
    username: str
    password: str


class TUser(BaseOrmModel):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()

    def hash_password(self, password):
        self.password = crypt_pass.hash(password)

    def verify_password(self, password):
        return crypt_pass.verify(password, self.password)

    @classmethod
    async def get_by_username(cls, username: str):
        stmt = select(cls).where(cls.username == username)
        res = await db_controller.execute_stmt(stmt)
        return res.one_or_none()
