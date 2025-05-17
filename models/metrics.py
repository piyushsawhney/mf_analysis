from sqlalchemy import Column, Integer, ForeignKey, Float, String, Date, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship

from db import Base


# Metrics by time period
class SchemeMetric(Base):
    __tablename__ = 'scheme_metric'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amfi_code = Column(String, ForeignKey('mf_schemes.amfi_code'))
    time_horizon = Column(Integer)
    metric_name = Column(String)
    investment = Column(Float)
    category = Column(Float)
    index = Column(Float)
    scheme = relationship("MFScheme", back_populates="metrics")
    __table_args__ = (
        UniqueConstraint('amfi_code', 'time_horizon', 'metric_name', name='uq_scheme_metric'),
        CheckConstraint("time_horizon IN (3, 5, 10)", name='valid_time_horizon'),
    )


class SchemeDrawdown(Base):
    __tablename__ = 'scheme_drawdowns'
    id = Column(Integer, primary_key=True, autoincrement=True)
    amfi_code = Column(String, ForeignKey('mf_schemes.amfi_code'))
    time_horizon = Column(Integer)
    peak_date = Column(Date)
    valley_date = Column(Date)
    max_duration = Column(String)

    scheme = relationship("MFScheme", back_populates="drawdowns")
    __table_args__ = (
        UniqueConstraint('amfi_code', 'time_horizon', name='uq_scheme_drawdown'),
        CheckConstraint("time_horizon IN (3, 5, 10)", name='valid_time_horizon'),
    )
