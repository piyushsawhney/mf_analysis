from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()
class MFScheme(Base):
    __tablename__ = 'mf_schemes'

    isin = Column(String, primary_key=True)
    amfi_scheme_code = Column(String, nullable=False)
    scheme_name = Column(String, nullable=False)
    sebi_scheme_code = Column(String, nullable=False)
    plan = Column(String, nullable=False)
    option = Column(String, nullable=False)
    category = Column(String, nullable=False)
    sub_category = Column(String, nullable=False)
    benchmark_code = Column(String, ForeignKey('mf_benchmarks.code'), nullable=True)

    benchmark = relationship("MFBenchmark", back_populates="schemes")
    navs = relationship("MFSchemeNAV", back_populates="scheme", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MFScheme(isin={self.isin}, scheme_name={self.scheme_name})>"

class MFSchemeNAV(Base):
    __tablename__ = 'mf_scheme_navs'

    isin = Column(String, ForeignKey('mf_schemes.isin', ondelete='CASCADE'), primary_key=True)
    date = Column(Date, primary_key=True)
    nav = Column(Numeric(10, 4), nullable=False)

    scheme = relationship("MFScheme", back_populates="navs")

    __table_args__ = (
        Index('idx_mf_nav_isin_date', 'isin', 'date'),
    )

    def __repr__(self):
        return f"<MFSchemeNAV(isin={self.isin}, date={self.date}, nav={self.nav})>"
