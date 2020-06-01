from covid import db
from datetime import datetime
class requirement(db.Model):
    __tablename__ = 'requirement'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(200),nullable=False)
    district = db.Column(db.String(100),nullable=False)
    state = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(30),nullable=False)
    req = db.Column(db.Integer,nullable=False)
    document_image = db.Column(db.String(64))
    contact = db.Column(db.String(10),nullable=False)    
    status = db.Column(db.String,default='orderplaced')
    cur_time = db.Column(db.DateTime,default=datetime.now())
    ngo_id = db.Column(db.Integer,db.ForeignKey('ngo.id'))
    code = db.Column(db.String)
    ngo = db.relationship('ngo',backref='order',lazy=True)
    def __init__(self,name=name,location=location,district=district,state=state,email=email,req=req,contact=contact):
        self.name = name
        self.location=location
        self.contact=contact
        self.district=district
        self.state=state
        self.email=email
        # self.document_image=document_image
        self.req=req
        # self.code=code

class ngo(db.Model):
    __tablename__='ngo'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    