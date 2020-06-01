from flask import flash,render_template,redirect,url_for,request,Blueprint,abort,jsonify
from covid import db,mail,app
from covid.models import requirement
from covid.requirements.forms import Requirement
from covid.requirements.picture_handler import add_image
from datetime import datetime
import string, random
from flask_mail import Message
from covid.requirements.qrcode import send_qr

requirements = Blueprint('requirements',__name__)

@requirements.route('/require',methods=['GET','POST'])
def require():
    form = Requirement()
    if form.validate_on_submit():
        name = form.name.data.lower()
        location = form.location.data.lower()
        district = form.district.data.lower()
        state = form.state.data.lower()
        req = form.requirements.data
        email = form.email.data
        code = ''.join(random.choices(string.ascii_lowercase,k=20))
        f = send_qr(code,email)
        print("1")
        msg = Message('Here is your QRCode',recipients=[email])
        print("2")
        with app.open_resource('requirements\\qrcodes\\'+f) as fi:
            msg.attach(f,'image/png',fi.read())
        print("3")
        mail.send(msg)
        print("4")
        document_image = add_image(form.doc.data,name)
        contact = form.contact.data
        req = requirement(name=name,location=location,email=email,district=district,state=state,code=code,req=req,document_image=document_image,contact=contact)
        db.session.add(req)
        db.session.commit()
        print(req.name)
        flash('Requirement submitted successfully!')
        return redirect(url_for('requirements.reqlist'))
    return render_template('requests.html',form=form)

@requirements.route('/reqlist')
def reqlist():
    reqs = requirement.query.order_by(requirement.cur_time.desc())
    requests = [] 
    for reqs in reqs:
        requests.append({'name':reqs.name,'location':reqs.location,'district':reqs.district,'state':reqs.state,'code':reqs.code,'email':reqs.email,'document_image':reqs.document_image,'req':reqs.req,'contact':reqs.contact})
    return jsonify({'requests' : requests})