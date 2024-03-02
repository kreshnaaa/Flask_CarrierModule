from app import app, db, ma, Base
from sqlalchemy.orm import class_mapper


TblJobDetails = Base.classes.JOB_DETAILS
TblApplicantDetails = Base.classes.APPLICANT_DETAILS
TblAppliedJobs = Base.classes.APPLIED_JOBS
TblLookUptable=Base.classes.LOOKUPTABLE
TblApplicantverif=Base.classes.APPLICANT_VERIFICATION

def create(data):
    db.session.add(data)
    db.session.commit()
    db.session.refresh(data)

def update(data):
    db.session.update(data)
    db.session.commit()
    db.session.refresh(data)


def serialize(model): 
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c,getattr(model,c)) for c in columns)

