from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, scoped_session 
from sqlalchemy.ext.declarative import declarative_base 
from models import Base, CryptoPrice, CryptoMetaData, TrendingCrypto
from contextlib import contextmanager 
import os 
from datetime import datetime

DATABASE_URL = "postgresql://adam_crypto:crypto@localhost:5432/crypto_data" 

engine = create_engine(DATABASE_URL)

SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

@contextmanager 
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e 
    finally: 
        session.close() 
        
def init_db():
    Base.metadata.create_all(engine)
    
def store_crypto_price(crypto_id, date, price_usd, market_cap_usd, volume_24h_usd):
    with get_db_session() as session:
        price = CryptoPrice(
            crypto_id=crypto_id,
            date=date,
            price_usd=price_usd,
            market_cap_usd=market_cap_usd,
            volume_24h_usd=volume_24h_usd
        )
        session.add(price)
    
def get_crypto_prices(crypto_id, start_date=None, end_date=None):
    with get_db_session() as session:
        query = session.query(CryptoPrice).filter(CryptoPrice.crypto_id == crypto_id)
        if start_date:
            query = query.filter(CryptoPrice.date >= start_date)
        if end_date:
            query = query.filter(CryptoPrice.date <= end_date)
        return query.all()
    
def update_crypto_price(crypto_id, date, price_usd, market_cap_usd, volume_24h_usd):
    with get_db_session() as session:
        query = session.query(CryptoPrice).filter(CryptoPrice.crypto_id == crypto_id, CryptoPrice.date == date)
        if query.count() > 0:
            query.price_usd = price_usd
            query.market_cap_usd = market_cap_usd
            query.volume_24h_usd = volume_24h_usd
            session.commit()
        else:
            raise ValueError(f"No price data found for crypto_id: {crypto_id} and date: {date}")

def store_crypto_metadata(crypto_id, name, symbol, description, market_cap_rank, liquidity_score, public_interest_score, developer_score, community_score):
    with get_db_session() as session:
        metadata = CryptoMetaData(
            crypto_id=crypto_id,
            name=name,
            symbol=symbol,
            description=description,
            market_cap_rank=market_cap_rank,
            liquidity_score=liquidity_score,
            public_interest_score=public_interest_score,
            developer_score=developer_score,
            community_score=community_score
        )
        session.add(metadata)
        
def get_crypto_metadata(crypto_id=None, name=None, symbol=None):
    with get_db_session() as session:
        query = session.query(CryptoMetaData)
        if crypto_id:
            query = query.filter(CryptoMetaData.crypto_id == crypto_id)
        if name:
            query = query.filter(CryptoMetaData.name == name)
        if symbol:
            query = query.filter(CryptoMetaData.symbol == symbol)
        return query.first()
    
def remove_crypto_metadata(crypto_id, name=None, symbol=None):
    with get_db_session() as session:
        query = session.query(CryptoMetaData)
        if crypto_id:
            query = query.filter(CryptoMetaData.crypto_id == crypto_id)
        if name:
            query = query.filter(CryptoMetaData.name == name)
        if symbol:
            query = query.filter(CryptoMetaData.symbol == symbol)
        query.delete()
        
def update_crypto_metadata(crypto_id, name=None, symbol=None, description=None, market_cap_rank=None, liquidity_score=None, public_interest_score=None, developer_score=None, community_score=None):
    with get_db_session() as session:
        query = session.query(CryptoMetaData).filter(CryptoMetaData.crypto_id == crypto_id)
        if name:
            query.name = name
        if symbol:
            query.symbol = symbol
        if description:
            query.description = description
        if market_cap_rank:
            query.market_cap_rank = market_cap_rank
        if liquidity_score:
            query.liquidity_score = liquidity_score
        if public_interest_score:
            query.public_interest_score = public_interest_score
        if developer_score:
            query.developer_score = developer_score
        if community_score:
            query.community_score = community_score 
        else:
            raise ValueError(f"No metadata found for crypto_id: {crypto_id}")
        session.commit()
    
class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine) 
        
    def init_db(self):
        Base.metadata.create_all(self.engine) 
    
    def store_price_data(self, crypto_id, price_data):
        session = self.Session()
        try:
            price = CryptoPrice(
                crypto_id=crypto_id,
                date=price_data['date'],
                price_usd=price_data['price_usd'],
                market_cap_usd=price_data.get('market_cap_usd'),
                volume_24h_usd=price_data.get('volume_24h_usd')
            )
            session.add(price)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
            
    def store_metadata(self, metadata):
        session = self.Session()
        try:
            crypto_metadata = CryptoMetaData(
                crypto_id=metadata['id'],
                name=metadata['name'],
                symbol=metadata['symbol'],
                description=metadata.get('description'),
                market_cap_rank=metadata.get('market_cap_rank'),
                liquidity_score=metadata.get('liquidity_score'),
                public_interest_score=metadata.get('public_interest_score'),
                developer_score=metadata.get('developer_score'),
                community_score=metadata.get('community_score')
            )
            session.add(crypto_metadata)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def store_trending(self, trending_data):
        session = self.Session()
        try:
            for coin in trending_data:
                trending = TrendingCrypto(
                    crypto_id=coin['id'],
                    name=coin['name'],
                    symbol=coin['symbol'],
                    market_cap_rank=coin.get('market_cap_rank'),
                    score=coin.get('score')
                )
                session.add(trending)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close() 
            
    def get_latest_price(self, crypto_id):
        session = self.Session()
        try:
            return session.query(CryptoPrice)\
                .filter(CryptoPrice.crypto_id == crypto_id)\
                .order_by(CryptoPrice.date.desc())\
                .first()
        finally:
            session.close() 
            
    def get_metadata(self, crypto_id):
        session = self.Session()
        try:
            return session.query(CryptoMetaData)\
                .filter(CryptoMetaData.crypto_id == crypto_id)\
                .first()
        finally:
            session.close()
            
    def get_trending(self, limit=10):
        session = self.Session()
        try:
            return session.query(TrendingCrypto)\
                .order_by(TrendingCrypto.created_at.desc())\
                .limit(limit)\
                .all()
        finally:
            session.close()