from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from datetime import date, timedelta

from database import SessionLocal, engine, Base
from models import HabitLog

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Detector API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add-habit/")
def add_habit(habit_name: str, log_date: date, db: Session = Depends(get_db)):
    entry = HabitLog(habit_name=habit_name, date=log_date)
    db.add(entry)
    db.commit()
    return {"message": "Habit logged successfully"}

@app.get("/streak/")
def get_streak(habit_name: str, db: Session = Depends(get_db)):
    logs = db.query(HabitLog).filter(HabitLog.habit_name == habit_name).all()
    dates = sorted([log.date for log in logs])

    if not dates:
        return {"streak": 0}

    streak = 1
    max_streak = 1

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            streak += 1
        else:
            streak = 1
        max_streak = max(max_streak, streak)

    return {"habit": habit_name, "max_streak": max_streak}
