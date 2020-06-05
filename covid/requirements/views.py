
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
    # form = Requirement()
    # if form.validate_on_submit():
        
    #     name = form.name.data.lower()
    #     location = form.location.data.lower()
    #     district = form.district.data.lower()
    #     state = form.state.data.lower()
    #     req = form.requirements.data
    #     email = form.email.data
    #     code = ''.join(random.choices(string.ascii_lowercase,k=20))
    #     f = send_qr(code,email)

        requirement_data=request.get_json()

        new_requirement=requirement(name=requirement_data['name'],location=requirement_data['location'],
                                    district=requirement_data['district'],state=requirement_data['State'],
                                    email=requirement_data['email'],contact=requirement_data['contact'],
                                    req=requirement_data['requirements'])

        # print("1")
        # msg = Message('Here is your QRCode',recipients=[email])
        # print("2")
        # with app.open_resource('requirements\\qrcodes\\'+f) as fi:
        #     msg.attach(f,'image/png',fi.read())
        # print("3")
        # mail.send(msg)
        # print("4")
        # document_image = add_image(form.doc.data,name)
        # contact = form.contact.data
        # req = requirement(name=name,location=location,email=email,district=district,state=state,code=code,req=req,document_image=document_image,contact=contact)
        db.session.add(new_requirement)
        db.session.commit()
        # print(req.name)
        # flash('Requirement submitted successfully!')
        # return redirect(url_for('requirements.reqlist'))

        return "Done"


    # return render_template('requests.html',form=form)
    # order_by(requirement.cur_time.desc())

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

    volunteer = ngo(name=data['ngo_name'],contact=data['ngo_contact'],email=data['ngo_email'])
    req = requirement.query.filter_by(id=data['req_id']).first()

    req.ngo_id = volunteer.id
    req.accept_time = datetime.now()
    req.status="orderAccepted"

    db.session.add(volunteer)
    db.session.commit()

    requ = requirement.query.filter_by(id=data['req_id']).first()   #for debugging purpose. check it
    print(requ.ngo_id)
    print(requ.accept_time)

    return "Done"