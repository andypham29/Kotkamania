import sqlite3
import os
from sqlalchemy.orm import Session

from server.admin.db.models import NhlPlayerStatLogORM, Session as DBSession


class InternalLogDao:

    def __init__(self, uri=None):
        # Note: uri parameter is kept for backward compatibility but not used
        # The centralized database setup is used instead
        pass

    def _get_session(self) -> Session:
        """Get a new database session"""
        return DBSession()

    def initNhlPlayerStatLogTable(self):
        """Initialize NHL player stat log table"""
        from server.admin.db.models import Base, engine
        Base.metadata.create_all(engine)

    def getNhlPlayerStatLogByDate(self, date):
        session = DBSession()
        try:
            row = session.query(NhlPlayerStatLogORM).filter_by(date=date).first()
            if not row:
                return None
            return NhlPlayerStatLog(row.date, row.description, row.timeExecuted)
        finally:
            session.close()

    def saveNhlPlayerStatLog(self, log):
        session = DBSession()
        try:
            new_log = NhlPlayerStatLogORM(
                date=log.date,
                description=log.description,
                timeExecuted=log.timeExecuted
            )
            session.add(new_log)
            session.commit()
        finally:
            session.close()

    def updateNhlPlayerStatLog(self, log):
        session = DBSession()
        try:
            existing = session.query(NhlPlayerStatLogORM).filter_by(date=log.date).first()
            if existing:
                existing.timeExecuted = log.timeExecuted
                session.commit()
        finally:
            session.close()


class NhlPlayerStatLog:

    def __init__(self, date, description, timeExecuted):
        self.date = date
        self.description = description
        self.timeExecuted = timeExecuted
