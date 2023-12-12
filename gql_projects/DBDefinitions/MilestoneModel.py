from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey
from .BaseModel import BaseModel
import sqlalchemy


class MilestoneModel(BaseModel):
    """
    Represents a milestone for projects in the system.
    """
    __tablename__ = "projectmilestones"

    id = UUIDColumn()
    name = Column(String, comment="Name of the milestone")
    startdate = Column(DateTime, comment="Start date of the milestone")
    enddate = Column(DateTime, comment="End date of the milestone")

    project_id = Column(ForeignKey("projects.id"), index=True, comment="Foreign key referencing the associated project")

    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the milestone was created")
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the milestone")
    createdby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)
    changedby = UUIDFKey(nullable=True)#Column(ForeignKey("users.id"), index=True, nullable=True)