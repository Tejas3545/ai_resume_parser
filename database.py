from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Adjust this to your local MySQL credentials
# Example: mysql+pymysql://USER:PASSWORD@HOST/DBNAME
DB_URL = "mysql+pymysql://root:lucifer@localhost/resume_db"

Base = declarative_base()

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    email = Column(String(255))
    phone = Column(String(50))
    skills = Column(Text)       # ✅ Changed from String(1000) → Text
    education = Column(Text)    # ✅ Changed from String(1000) → Text
    experience = Column(Text)   # ✅ Changed from String(4000) → Text

engine = create_engine(DB_URL, pool_pre_ping=True, future=True)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def _list_to_csv(values):
    if not values:
        return None
    if isinstance(values, list):
        return ",".join([str(v) for v in values])
    return str(values)

def _csv_to_list(value):
    if not value:
        return []
    return [v.strip() for v in value.split(",") if v.strip()]

def save_to_db(data: dict) -> None:
    session = SessionLocal()
    try:
        c = Candidate(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            skills=_list_to_csv(data.get("skills")),
            education=_list_to_csv(data.get("education")),
            experience=_list_to_csv(data.get("experience")),
        )
        session.add(c)
        session.commit()
    finally:
        session.close()

def get_all_resumes():
    session = SessionLocal()
    try:
        rows = session.query(Candidate).all()
        out = []
        for r in rows:
            out.append({
                "id": r.id,
                "name": r.name,
                "email": r.email,
                "phone": r.phone,
                "skills": _csv_to_list(r.skills),
                "education": _csv_to_list(r.education),
                "experience": _csv_to_list(r.experience),
            })
        return out
    finally:
        session.close()

def delete_resume(resume_id: int) -> None:
    session = SessionLocal()
    try:
        obj = session.query(Candidate).filter(Candidate.id == resume_id).first()
        if obj:
            session.delete(obj)
            session.commit()
    finally:
        session.close()
