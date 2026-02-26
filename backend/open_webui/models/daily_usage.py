from sqlalchemy import Column, String, Integer
from open_webui.db import Base

class DailyUsage(Base):
    __tablename__ = "daily_usage"

    user_id = Column(String, primary_key=True)
    date = Column(String, primary_key=True)
    count = Column(Integer, default=0)
