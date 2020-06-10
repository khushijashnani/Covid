from flask import flash,render_template,redirect,url_for,request,Blueprint,abort,jsonify,request
from covid import db,mail,app
from covid.models import requirement,ngo
from covid.requirements.forms import Requirement
from covid.requirements.picture_handler import add_image
from datetime import datetime
import string,random
from flask_mail import Message
from covid.requirements.qrcode import send_qr

requirements = Blueprint('requirements',__name__)

@requirements.route('/require',methods=['GET','POST'])
def require():
    
    requirement_data=request.get_json()
    code = ''.join(random.choices(string.ascii_lowercase,k=5))
    f = send_qr(code,requirement_data['email'])
    new_requirement=requirement(name=requirement_data['name'],location=requirement_data['location'],
                                    district=requirement_data['district'],state=requirement_data['State'],
                                    email=requirement_data['email'],contact=requirement_data['contact'],
                                    req=requirement_data['requirements'],code=code)
    print(new_requirement)
    msg = Message(subject='Here is your QRCode',recipients=[requirement_data['email']])
    print("2")
    with app.open_resource('requirements\\qrcodes\\'+f) as fi:
        msg.attach('QRCode.png','image/png',fi.read())
    print("3")
    mail.send(msg)
    print("4")
    #document_image = add_image(form.doc.data,name)
    db.session.add(new_requirement)
    db.session.commit()
    return "Done"


@requirements.route('/reqlist')
def reqlist():
    reqs = requirement.query.filter_by(status='orderplaced').order_by(requirement.cur_time.desc())
    
    requests=[]

    for request in reqs:
        requests.append({'id':request.id,'Name': request.name ,'Location': request.location+","+request.district+","+request.state , 'Requirement': request.req ,'ContactNo': request.contact})

    return jsonify({'requests': requests})
    
@requirements.route('/track')
def track():
    reqs = requirement.query.order_by(requirement.cur_time.desc())
    acceptedRequests = []
    completedRequests = []
    for request in reqs:
        if request.status == 'orderAccepted' :
            acceptedRequests.append({'id':request.id,'Name': request.name ,'Location': request.location+","+request.district+","+request.state , 'Requirement': request.req ,'ContactNo': request.contact})
        elif request.status == 'orderCompleted' :
            completedRequests.append({'id':request.id,'Name': request.name ,'Location': request.location+","+request.district+","+request.state , 'Requirement': request.req ,'ContactNo': request.contact})
    return jsonify({'acceptedRequests': acceptedRequests ,'completedRequests':completedRequests})

@requirements.route('/reqlist/accept',methods=['GET','POST'])
def accept():

    data=request.get_json()
    vol = ngo.query.filter_by(email=data['ngo_email']).first()
    req = requirement.query.filter_by(id=data['req_id']).first()

    if vol is not None :
        vol.reqs.append(req)
        # db.session.commit()
        req.ngo_id = vol.id
        msg1 = Message(subject='Request Confirmed',body='You have accepted the request.\nRequest ID:'+str(req.id)+'\nPlease contact them and do the needful as early as possible.\nThank You.',recipients=[vol.email])
        msg2 = Message(subject='Request accepted',body='Your request has been accpeted by '+vol.name+'\n.They will contact you soon.',recipients=[req.email])
    else:
        volunteer = ngo(name=data['ngo_name'],contact=data['ngo_contact'],email=data['ngo_email'])
        db.session.add(volunteer)
        # db.session.commit()
        req.ngo_id = volunteer.id
        print(volunteer)
        msg1 = Message(subject='Request Confirmed',body='You have accepted the request.\nRequest ID:'+str(req.id)+'\nPlease contact them and do the needful as early as possible.\nThank You.',recipients=[volunteer.email])
        msg2 = Message(subject='Request accepted',body='Your request has been accpeted by'+volunteer.name+'\n.They will contact you soon.',recipients=[req.email])

    req.accept_time = datetime.now()
    req.status="orderAccepted"
    
    mail.send(msg1)
    mail.send(msg2)

    db.session.commit()

    #for debugging purpose.
    requ = requirement.query.filter_by(id=data['req_id']).first()   
    print(requ)
    print(vol)

    return "Done"

@requirements.route('/validate',methods=['GET','POST'])
def validate():
    data = request.get_json()
    volunteer = ngo.query.filter_by(email=data['email']).first()
    for x in volunteer.reqs :
        if int(data['reqID']) == x.id and x.code == data['code']: 
            x.status = 'orderCompleted'
            x.complete_time = datetime.now()
            db.session.commit()
            return {'status':'Right'}
    return {'status':'Wrong'}
