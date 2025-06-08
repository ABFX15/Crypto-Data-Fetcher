from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship 
from datetime import datetime, timezone

# Base class for our models
Base = declarative_base()

class CryptoPrice(Base):
    __tablename__ = 'crypto_prices'
    
    id = Column(Integer, primary_key=True)
    crypto_id = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    price_usd = Column(Float, nullable=False)
    market_cap_usd = Column(Float)
    volume_24h_usd = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<CryptoPrice(crypto_id={self.crypto_id}, date={self.date}, price_usd={self.price_usd})>"
    

class CryptoMetaData(Base):
    __tablename__ = 'crypto_metadata'
    
    id = Column(Integer, primary_key=True)
    crypto_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    description = Column(String)
    market_cap_rank = Column(Integer)
    liquidity_score = Column(Float)
    public_interest_score = Column(Float)
    developer_score = Column(Float)
    community_score = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<CryptoMetaData(crypto_id={self.crypto_id}, name={self.name}, symbol={self.symbol})>"
    

class TrendingCrypto(Base):
    __tablename__ = 'trending_crypto'
    
    id = Column(Integer, primary_key=True)
    crypto_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    market_cap_rank = Column(Integer)
    score = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self):
        return f"<TrendingCrypto(crypto_id={self.crypto_id}, name={self.name}, symbol={self.symbol})>"