import os
from sqlalchemy.orm import Session

from server.mockdraft.model.prospect import ProspectElite
from server.mockdraft.db.models import ProspectEliteORM, Base, Session as DBSession, engine
from setting import Setting


class ProspectEliteDao:

    def __init__(self, year=Setting.NHL_YEAR):
        self.tablename = f"eliteprospect{year}"

    def initProspectEliteTable(self):
        """Initialize elite prospect table"""
        Base.metadata.create_all(engine)

    def getProspectById(self, id):
        session = DBSession()
        try:
            row = session.query(ProspectEliteORM).filter_by(id=id).first()
            if not row:
                return None
            return ProspectElite(id=row.id, name=row.name, position=row.position, avg_rank=row.avg_rank, hp=row.hp, fc=row.fc, iss=row.iss,
                                 mh=row.mh, elite=row.elite, league=row.league, team=row.team, gp=row.gp, g=row.g, a=row.a,
                                 p=row.p, pim=row.pim)
        finally:
            session.close()

    def getProspectByPosition(self, position, page):
        session = DBSession()
        try:
            query = session.query(ProspectEliteORM).filter(
                ProspectEliteORM.position.like(f'%{position}%')
            ).order_by(ProspectEliteORM.avg_rank)

            if int(page) > 0:
                query = query.offset(20 * int(page)).limit(20)

            records = query.all()
            list_result = []
            for row in records:
                prospect = ProspectElite(id=row.id, name=row.name, position=row.position, avg_rank=row.avg_rank, hp=row.hp, fc=row.fc,
                                         iss=row.iss, mh=row.mh, elite=row.elite, league=row.league, team=row.team, gp=row.gp,
                                         g=row.g, a=row.a, p=row.p, pim=row.pim)
                list_result.append(prospect)

            return list_result
        finally:
            session.close()

    def getAllProspects(self):
        session = DBSession()
        try:
            records = session.query(ProspectEliteORM).all()

            list_result = []
            for row in records:
                prospect = ProspectElite(id=row.id, name=row.name, position=row.position, avg_rank=row.avg_rank, hp=row.hp, fc=row.fc,
                                         iss=row.iss, mh=row.mh, elite=row.elite, league=row.league, team=row.team, gp=row.gp,
                                         g=row.g, a=row.a, p=row.p, pim=row.pim)
                list_result.append(prospect)

            return list_result
        finally:
            session.close()

    def getAllProspectsWithRanking(self):
        session = DBSession()
        try:
            from sqlalchemy import and_

            records = session.query(ProspectEliteORM).filter(
                and_(
                    ProspectEliteORM.hp != None,
                    ProspectEliteORM.fc != None,
                    ProspectEliteORM.iss != None,
                    ProspectEliteORM.mh != None,
                    ProspectEliteORM.elite != None
                )
            ).order_by(ProspectEliteORM.avg_rank).all()

            list_result = []
            for row in records:
                prospect = ProspectElite(id=row.id, name=row.name, position=row.position, avg_rank=row.avg_rank, hp=row.hp, fc=row.fc,
                                         iss=row.iss, mh=row.mh, elite=row.elite, league=row.league, team=row.team, gp=row.gp,
                                         g=row.g, a=row.a, p=row.p, pim=row.pim)
                list_result.append(prospect)

            return list_result
        finally:
            session.close()

    def getProspectsAtPage(self, page=1):
        session = DBSession()
        try:
            if int(page) < 1:
                raise Exception("Error fetching prospects")

            records = session.query(ProspectEliteORM).order_by(
                ProspectEliteORM.avg_rank
            ).offset(20 * (int(page) - 1)).limit(20).all()

            list_result = []
            for row in records:
                prospect = ProspectElite(id=row.id, name=row.name, position=row.position, avg_rank=row.avg_rank, hp=row.hp, fc=row.fc,
                                         iss=row.iss, mh=row.mh, elite=row.elite, league=row.league, team=row.team, gp=row.gp,
                                         g=row.g, a=row.a, p=row.p, pim=row.pim)
                list_result.append(prospect)

            return list_result
        finally:
            session.close()

    def insertOrUpdateProspectElite(self, prospect):
        session = DBSession()
        try:
            existing = session.query(ProspectEliteORM).filter_by(name=prospect.name).first()

            if existing:
                existing.position = prospect.position
                existing.hp = prospect.hp
                existing.fc = prospect.fc
                existing.iss = prospect.iss
                existing.mh = prospect.mh
                existing.elite = prospect.elite
                existing.league = prospect.league
                existing.team = prospect.team
                existing.gp = prospect.gp
                existing.g = prospect.g
                existing.a = prospect.a
                existing.p = prospect.p
                existing.pim = prospect.pim
            else:
                new_prospect = ProspectEliteORM(
                    name=prospect.name,
                    position=prospect.position,
                    hp=prospect.hp,
                    fc=prospect.fc,
                    iss=prospect.iss,
                    mh=prospect.mh,
                    elite=prospect.elite,
                    league=prospect.league,
                    team=prospect.team,
                    gp=prospect.gp,
                    g=prospect.g,
                    a=prospect.a,
                    p=prospect.p,
                    pim=prospect.pim
                )
                session.add(new_prospect)

            session.commit()
        finally:
            session.close()

    def updateProspectEliteAvgRank(self, prospect):
        session = DBSession()
        try:
            existing = session.query(ProspectEliteORM).filter_by(name=prospect.name).first()
            if existing:
                existing.avg_rank = prospect.avg_rank
                session.commit()
        finally:
            session.close()
