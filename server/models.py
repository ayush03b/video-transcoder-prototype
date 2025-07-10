from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from db_setup import Base

from sqlalchemy import Column, Integer, String
from sqlalchemy.sql import func
from models import Base

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    s3_key = Column(String, nullable=False)
    uploaded_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )