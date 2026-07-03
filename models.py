from sqlalchemy import Column, Integer, String, Float
from database import Base

class TransportRoute(Base):
    __tablename__ = "transport_routes"

    id = Column(Integer, primary_key=True, index=True)
    origin = Column(String, index=True)
    destination = Column(String, index=True)
    price = Column(Float)
    vehicle_type = Column(String)
