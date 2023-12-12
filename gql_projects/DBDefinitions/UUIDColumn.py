import sqlalchemy
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey

def newUuidAsString():
    return f"{uuid.uuid1()}"
# Tyto funkce slouží k definici sloupců pro unikátní identifikátory (UUID) v tabulkách. 
# UUID je použito jako primární klíč pro některé tabulky. Funkce také umožňují určit, zda je sloupec cizího klíče (foreign key) a zda může být nullable.
def UUIDColumn(name=None):
    if name is None:
        return Column(String, primary_key=True, unique=True, default=newUuidAsString)
    else:
        return Column(
            name, String, primary_key=True, unique=True, default=newUuidAsString
        )
    
def UUIDFKey(*, ForeignKey=None, nullable=False):
    if ForeignKey is None:
        return Column(
            String, index=True, nullable=nullable
        )
    else:
        return Column(
            ForeignKey, index=True, nullable=nullable
        )