from flask import flash,render_template,redirect,url_for,request,Blueprint,abort,jsonify,request
from covid import db,mail,app
from covid.models import requirement,ngo
from covid.requirements.forms import Requirement
from covid.requirements.picture_handler import add_image
from datetime import datetime
import string, random
from flask_mail import Message
from covid.requirements.qrcode import send_qr

requirements = Blueprint('requirements',__name__)

@requirements.route('/require',methods=['GET','POST'])
def require():
   
    requirement_data=request.get_json()

    new_requirement=requirement(name=requirement_data['name'],location=requirement_data['location'],
                                    district=requirement_data['district'],state=requirement_data['State'],
                                    email=requirement_data['email'],contact=requirement_data['contact'],
                                    req=requirement_data['requirements'])

        # code = ''.join(random.choices(string.ascii_lowercase,k=20))  #code is stored in the db
        # f = send_qr(code,email)
        # print("1")
        # msg = Message(subject='Here is your QRCode',recipients=[requirement_data['email']])
        # print("2")
        # with app.open_resource('requirements\\qrcodes\\'+f) as fi:
        #     msg.attach('QRCode.png','image/png',fi.read())
        # print("3")
        # mail.send(msg)
        # print("4")
        # document_image = add_image(form.doc.data,name)    #document file name is getting stored in the db
        
    db.session.add(new_requirement)
    db.session.commit()

    return "Done"

@requirements.route('/reqlist')
def reqlist():
    reqs = requirement.query.order_by(requirement.cur_time.desc())
    
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
def accept(req_id):

    data=request.get_json()

    volunteer = ngo(name=data['ngo_name'],contact=data['ngo_contact'],email=data['ngo_email'])
    req = requirement.query.filter_by(id=data['req_id']).first()

    req.ngo_id = volunteer.id
    req.accept_time = datetime.now()

    db.session.add(volunteer)
    db.session.commit()

    requ = requirement.query.filter_by(id=data['req_id']).first()   #for debugging purpose. check it
    print(requ.ngo_id)
    print(requ.accept_time)

    #msg1 = Message(subject='Request Confirmed',body='You have accepted the request.\nRequest ID:'+str(req.id)+'\nPlease contact them and do the needful as early as possible.\nThank You.',recipients=[volunteer.email])
    #msg2 = Message(subject='Request accepted',body='Your request has been accpeted by'+volunteer.name+'\n.They will contact you soon.',recipients=[req.email])
    #mail.send([msg1,msg2])

    return "Done"