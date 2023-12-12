from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey
from .BaseModel import BaseModel
import sqlalchemy
from sqlalchemy.orm import relationship

class ProjectTypeModel(BaseModel):
    """
    Represents a type of project in the system.
    """
    __tablename__ = "projecttypes"

    id = UUIDColumn()
    name = Column(String, comment="Name of the project type")
    name_en = Column(String, comment="English name of the project type")

    category_id = Column(ForeignKey("projectcategories.id"), index=True, nullable=True, comment="Foreign key referencing the project category")
    projects = relationship("ProjectModel", back_populates="projecttype")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the project type was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the project type")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)