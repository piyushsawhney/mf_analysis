from sqlalchemy import Column, String, Date, Numeric, ForeignKey, Index
from sqlalchemy.orm import relationship

from db.base import Base


class MFBenchmark(Base):
    __tablename__ = 'mf_benchmarks'

    code = Column(String, primary_key=True)  # e.g., "NIFTY 50 TRI"
    values = relationship("MFBenchmarkValue", back_populates="benchmark", cascade="all, delete-orphan")
    schemes = relationship("MFScheme", back_populates="benchmark")

    def __repr__(self):
        return f"<MFBenchmark(code={self.code})>"


class MFBenchmarkValue(Base):
    __tablename__ = 'mf_benchmark_values'

    code = Column(String, ForeignKey('mf_benchmarks.code', ondelete='CASCADE'), primary_key=True)
    date = Column(Date, primary_key=True)
    value = Column(Numeric(12, 4), nullable=False)

    benchmark = relationship("MFBenchmark", back_populates="values")

    __table_args__ = (
        Index('idx_mf_benchmark_code_date', 'code', 'date'),
    )

    def __repr__(self):
        return f"<MFBenchmarkValue(code={self.code}, date={self.date}, value={self.value})>"
