from  app import db

from datetime import datetime

class Sales(db.Model):
    __tablename__='sales'
    id=db.Column(db.Integer,primary_key=True)
    inv_id=db.Column(db.Integer,db.ForeignKey('inventories.id')) # for thhe foreign KEY  you must also decloeare it at the parent table
    quantity=db.Column(db.Integer)
    created_at=db.Column(db.DateTime,default=datetime.utcnow)

    def add_records(self):
        db.session.add(self)
        db.session.commit()

        # Fetch all records

    @classmethod
    def fetch_all_records(cls):
        return cls.query.all()

    # fetch one record
    @classmethod
    def fetch_one_record(cls, id):
        return cls.query.filter_by(id=id).first()


