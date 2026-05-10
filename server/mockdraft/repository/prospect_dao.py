import os
from sqlalchemy.orm import Session

from server.mockdraft.model.prospect import Prospect
from server.mockdraft.db.models import ProspectORM, Base, Session as DBSession, engine


class ProspectDao:

    def __init__(self):
        pass

    def initProspectTable(self):
        """Initialize prospect table"""
        Base.metadata.create_all(engine)

    def createProspect(self, prospect):
        session = DBSession()
        try:
            new_prospect = ProspectORM(
                rank=prospect.rank,
                player_name=prospect.player_name,
                height=prospect.height,
                weight=prospect.weight,
                position=prospect.position,
                team=prospect.team,
                league=prospect.league
            )
            session.add(new_prospect)
            session.commit()
        finally:
            session.close()

    def getProspectById(self, id):
        session = DBSession()
        try:
            row = session.query(ProspectORM).filter_by(id=id).first()
            if not row:
                return None
            return Prospect(row.id, row.rank, row.player_name, row.height, row.weight, row.position, row.team, row.league)
        finally:
            session.close()

    def getAllProspects(self):
        session = DBSession()
        try:
            records = session.query(ProspectORM).all()

            list_result = []
            for row in records:
                prospect = Prospect(row.id, row.rank, row.player_name, row.height, row.weight, row.position, row.team, row.league)
                list_result.append(prospect)

            return list_result
        finally:
            session.close()

    def deleteProspectById(self, id):
        session = DBSession()
        try:
            session.query(ProspectORM).filter_by(id=id).delete()
            session.commit()
        finally:
            session.close()
