from .UUIDColumn import UUIDColumn, UUIDFKey
from sqlalchemy import Column, DateTime, String, ForeignKey, Boolean
from .BaseModel import BaseModel
import sqlalchemy
from sqlalchemy.orm import relationship

class StatementOfWorkModel(BaseModel):
    """
    Represents a SOW in the system. 
    
    """
    __tablename__ = "projects_events"

    id = UUIDColumn()
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp of the last change to the SOW")
    #name = Column(String, comment="Name of the sow")
    valid = Column(Boolean, default=True, comment="if this entity is valid or invalid")
    startdate = Column(DateTime, comment="Start date of the milestone")
    enddate = Column(DateTime, comment="End date of the milestone")

    project_id = Column(ForeignKey("projects.id"), index=True, comment="Foreign key referencing the associated project")

    event_id = UUIDFKey(nullable=True)


    created = Column(DateTime, server_default=sqlalchemy.sql.func.now(), comment="Timestamp when the SOW was created")

    createdby = UUIDFKey(nullable=True)
    changedby = UUIDFKey(nullable=True)
    rbacobject = UUIDFKey(nullable=True, comment="user or group id, determines access")