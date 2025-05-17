from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship

from db.base import Base


class MFScheme(Base):
    __tablename__ = 'mf_schemes'

    amfi_code = Column(String, primary_key=True)
    scheme_name = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    option = Column(String, nullable=False)
    type = Column(String, nullable=True)
    asset_class = Column(String, nullable=True)
    sub_category = Column(String, nullable=True)
    sebi_scheme_code = Column(String, nullable=True)
    isin1 = Column(String, nullable=True)
    isin2 = Column(String, nullable=True)
    launch_date = Column(Date, nullable=True)
    metrics = relationship("SchemeMetric", back_populates="scheme")
    drawdowns = relationship("Drawdown", back_populates="scheme")
    benchmark_code = Column(String, ForeignKey('mf_benchmarks.code'), nullable=True)
    benchmark = relationship("MFBenchmark", back_populates="schemes")
    navs = relationship("MFSchemeNAV", back_populates="scheme", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MFScheme(amfi_code={self.amfi_code}, scheme_name={self.scheme_name})>"


class MFSchemeNAV(Base):
    __tablename__ = 'mf_scheme_navs'

    amfi_code = Column(String, ForeignKey('mf_schemes.amfi_code', ondelete='CASCADE'), primary_key=True)
    date = Column(Date, primary_key=True)
    nav = Column(Numeric(10, 4), nullable=False)

    scheme = relationship("MFScheme", back_populates="navs")

    __table_args__ = (
        Index('idx_mf_nav_amfi_code_date', 'amfi_code', 'date'),
    )

    def __repr__(self):
        return f"<MFSchemeNAV(amfi_code={self.amfi_code}, date={self.date}, nav={self.nav})>"
