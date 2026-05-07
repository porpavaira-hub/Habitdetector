from sqlalchemy import Column, Integer, String, Date
from database import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_name = Column(String, index=True)
    date = Column(Date)
