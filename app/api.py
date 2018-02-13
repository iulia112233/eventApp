import os 
from flask import render_template, request, g, url_for, redirect, flash, session, jsonify, make_response, Response
from flask_login import login_required, login_user, current_user, logout_user
from sqlalchemy import create_engine, inspect
from app import app, db, lm, mail
from .forms import LoginForm, RegistrationForm, EditForm
from models import User, Event, Comment, Ticket
from config import SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER, GALLERY_FOLDER, DEFAULT_EVENT_IMAGE, STRIPE_SK, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, ADMINS
from werkzeug.utils import secure_filename
import json
from json import dumps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import stripe
from flask_mail import Message
import smtplib
from email.mime.multipart import MIMEMultipart
from email.MIMEImage import MIMEImage
from email.mime.text import MIMEText
import email.message
from string import Template

@app.route('/api/register', methods = ['POST'])
def api_register():
    result = {}
    formData = dict(request.form)

    if formData is None:
         return jsonify({'outcome': 'Please provide username and password'}), 422

    user = User(username=formData['username'], password=formData['password'], surname=formData['surname'], name=formData['name'], role=formData['role'])
    
    if user.exists():
        return jsonify({'outcome': 'Username already exists!'}), 422
    else:
        user.register() 
        return jsonify({'outcome': 'Your registration was successful!'}), 201


@app.route('/api/login', methods = ['POST'])
def api_login():
    formData = request.get_json()

    if formData is None:
         return jsonify({'outcome': 'Please provide username and password'}), 422
    
    user = User(username=formData['username'], password=formData['password'])
    resp = user.login()
    print(resp) 
    if resp:
        session['logged_in'] = True
        session['user'] = user.__dict__
        session['user']['id'] = resp.id
        session['user']['surname'] = resp.surname
        session['user']['name'] = resp.name
        session['user']['aboutme'] = resp.aboutme
        session['user']['picture'] = resp.picture
        session['user']['role'] = resp.role
        return jsonify({'outcome': 'Login successful!'}), 200
    else:
        return jsonify({'outcome': 'Invalid username or password'}), 422


@app.route('/api/user', methods = ['GET'])
def api_get_user():
    if session.get('user'):
        user = User(uid = session.get('user')['id'])
        return user.getUserProfileInfo(), 200
    else:
        return jsonify({'outcome': 'Could not get user data'}), 422


@app.route('/api/allevents', methods = ['GET'])
def api_get_all_events():
    if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action.'}), 401
    
    userData = session.get('user')
    user = User(username = userData['username'], password = userData['password'], uid = userData['id'])
    return user.getAllEvents(), 200

@app.route('/api/myevents', methods = ['GET'])
def api_get_my_events():
    if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action.'}), 401
    
    userData = session.get('user')
    user = User(username = userData['username'], password = userData['password'], uid = userData['id'])
    return user.getMyEvents(), 200

@app.route('/api/event', methods = ['POST'])
def api_post_event():
    if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action.'}), 401
    
    formData = dict(request.form)
    sessionData = session.get('user')
    filePath  = ''

    if dict(request.files):
        if dict(request.files)['file']:
            image = dict(request.files)['file'][0]
            imageName = formData['fileName'][0]
            filePath = os.path.join(UPLOAD_FOLDER, imageName)
            image.save(filePath)

    if formData:
        title = formData['title'][0]
        description = formData['description'][0]
        eventTime = formData['eventTime'][0]
        createdAt = formData['createdAt'][0]
        lat = formData['lat'][0]
        lng = formData['lng'][0]
        
        if not filePath:
            filePath = os.path.join(UPLOAD_FOLDER, DEFAULT_EVENT_IMAGE)
        if formData['savedTickets'][0]:
            tickets = json.loads(formData['savedTickets'][0])
            for t in tickets:
                ticket = Ticket(type=t['type'], price=t['price'], currency=t['currency'])
            
    event = Event(title = title, created = createdAt, time = eventTime, image = filePath, uid = sessionData['id'], description = description, lat = lat, lng = lng)
    event.add()
    eid = event.returnId()

    if formData['savedTickets'][0]:
       print formData['savedTickets'][0]
       tickets = json.loads(formData['savedTickets'][0])
       print tickets
       for t in tickets:
           print t
           ticket = Ticket(eid = eid, type=t['type'], price=t['price'], currency=t['currency'])
           ticket.save()
    return jsonify({'outcome': 'Created'}), 201


@app.route('/api/edit', methods = ['POST'])
def api_edit_user():
    if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action.'}), 401
    
    sessionData = session.get('user')
    formData = dict(request.form)
    firstName = ''
    lastName = ''
    aboutMe = ''

    if formData:
        firstName = formData['firstName'][0]
        lastName = formData['lastName'][0]
        aboutMe = formData['aboutMe'][0]

    user = User(username = sessionData['username'], password = sessionData['password'], uid = sessionData['id'], name = lastName, surname = firstName, aboutme = aboutMe)
    res = user.updateInfo()
    return jsonify({'status': 'Success!'}), 200

@app.route('/api/avatars', methods = ['GET'])
def get_img_src():
   if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action.'}), 401

   names = os.listdir(os.path.join(app.static_folder, 'gallery'))
   
   imagePaths = []
   for x in names:
 	imagePaths.append(os.path.join(GALLERY_FOLDER, x))
		 
   return jsonify({'imagePaths': imagePaths}), 200

@app.route('/api/setProfilePicture', methods = ['POST'])
def set_profile_picture():
    if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action. '}), 401
   
    sessionData = session.get('user')
    formData = dict(request.form) 
    filePath = None

    if dict(request.files):
        if dict(request.files)['file']:
            image = dict(request.files)['file'][0]
            imageName = formData['fileName'][0]
            filePath = os.path.join(UPLOAD_FOLDER, imageName)
            image.save(filePath)
    elif formData:
            if formData.has_key('fileName'):
                filePath = formData['fileName']

    user = User(username = sessionData['username'], password = sessionData['password'], uid = sessionData['id'], picture = filePath)
    user.setProfilePic()
    return jsonify({'outcome': 'OK'}), 200

@app.route('/api/getUsers', methods = ['GET'])
def get_users():
    if not session.get('user'):
       return jsonify({'outcome': 'You need to be logged in to perform this action. '}), 401
    if session.get('user')['role'] != 'admin':
       return jsonify({'outcome': 'You do not have permission to view this page'}), 403
    user = User()
    return jsonify({'data':user.returnUserData()}), 200

@app.route('/api/editUser', methods=['POST'])
def edit_specific_user():
    if not session.get('user'):
       return jsonify({'outcome': 'You need to be logged in to perform this action. '}), 401
    if session.get('user')['role'] != 'admin':
       return jsonify({'outcome': 'You do not have permission to view this page'}), 403
    
    formData = dict(request.form)
    
    if formData:
        uid = formData['id'][0]
        surname = formData['surname'][0]
        name = formData['name'][0]
        aboutme = formData['aboutme'][0]
        image = formData['image'][0]
        role = formData['role'][0]

    user = User(uid = uid, name = name, surname = surname, aboutme = aboutme, picture = image, role = role)
    user.updateAllInfo()
  
    return jsonify({'outcome': 'User has been successfully updated!'}), 200

@app.route('/api/reset', methods = ['GET','POST'])
def api_reset_form():
   
    fd = dict(request.form)
    username = fd['username'][0]
    user = User(username=username)
    if not user.exists():
        flash('User does not exist!')
        return jsonify({'outcome': 'User does not exist'}), 422
    t = user.getToken()
    
    msg = MIMEMultipart('related')
    msg['From'] = 'iulia@phyramid.com'
    msg['To'] = 'iulia@phyramid.com'
    msg['Subject'] = 'Password reset'

    body = "Please access the following link to reset your password: </br> <a href ='http://localhost:5000/reset?token="+ t +"'>Reset</a>";
    body = MIMEText(body, 'html')
    msg.attach(body)

    server = smtplib.SMTP(MAIL_SERVER+ ':' + MAIL_PORT)
    server.starttls()
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    u = user.verifyToken(t)
    return jsonify({'outcome': 'Success '}), 200

@app.route('/api/resetPassword', methods = ['POST'])
def api_reset_password():

    fd = dict(request.form)
    if fd:
        password = fd['password'][0]
        username = fd['username'][0]
        user = User(username=username, password=password) 
        r = user.updatePassword()
        return jsonify({'outcome': 'The password has been successfully updated. You can log in now'}), 200
    return jsonify({'outcome': 'Missing parameters!'}), 422

@app.route('/api/removeEvent', methods = ['POST'])
def api_remove_event():
    fd = dict(request.form)
    if not fd:
        return jsonify({'outcome': 'Missing parameters!'}), 422
    e = Event(eid=fd['id'][0])
    e.removeEvent()
    return jsonify({'outcome': 'Succes!'}), 200

@app.route('/api/fullEvent', methods = ['POST'])
def api_get_full_event():
    fd = dict(request.form)
    print fd
    if not fd:
       return jsonify({'outcome': 'Missing parameters!'}), 422
    e = Event(eid=fd['id'][0])
    return e.getEventData(), 200

@app.route('/api/postComment', methods = ['POST'])
def api_post_comment():
    fd = dict(request.form)
    if not fd:
       return jsonify({'outcome': 'Missing parameters!'}), 422

    c = Comment(eid=fd['event'][0], uid=session.get('user')['id'], comment=fd['comment'][0])
    c.postComment()
    return jsonify({'outcome': 'Comment successfully posted!'}), 200

@app.route('/api/loadComments', methods = ['POST'])
def api_load_comments():
    
    fd = dict(request.form)
    if not fd:
       return jsonify({'outcome': 'Missing parameters!'}), 422

    c = Comment(eid=fd['event'][0])
    return c.loadComments(), 200

@app.route('/api/addReaction', methods = ['POST'])
def api_add_reaction():
    
    fd = dict(request.form)
    if not fd:
       return jsonify({'outcome': 'Missing parameters!'}), 422

    c = Comment(eid=fd['event'][0], uid=session.get('user')['id'], reaction=fd['reaction'][0])
    c.addReaction()
    return jsonify({'outcome': 'Reaction successfully saved!'}), 200

@app.route('/api/charge', methods = ['POST'])
def api_charge():
    
    source =  request.json['token_from_stripe']
    description = request.json['engravingText']
    amount = request.json['amount']
    currency = request.json['currency']
    print currency

    res = stripe.Charge.create(
        amount = amount,
        currency = currency,
        source = source,
        api_key = STRIPE_SK,
        receipt_email = "iulia@phyramid.com",
        description = description)

    return jsonify({'charge': dict(res)}), 200

@app.route('/api/order-completed', methods = ['POST'])
def api_get_order_complete():
    if not session.get('user'):
        return jsonify({'outcome': 'You need to be logged in to perform this action. '}), 401

    charge_id = request.json['charge_id']
    print charge_id

    stripe.api_key = STRIPE_SK
    charge = stripe.Charge.retrieve(charge_id)
    ch = dict(charge)

    msg = MIMEMultipart('related')
    msg['From'] = 'iulia@phyramid.com'
    msg['To'] = 'iulia@phyramid.com'
    msg['Subject'] = 'Order Information'

    print ch['description']

    body =  'Hello ' + session.get('user')['surname'] + ' ' + session.get('user')['name'] + '!</br></br> Congratulations on ordering ' + ch['description'] + '</br> Amount: '+ str(ch['amount']/100) + ' ' + ch['currency'] + '</br> Order Status: ' + ch['status']  ;   
    body = MIMEText(body, 'html')
    msg.attach(body)

    server = smtplib.SMTP(MAIL_SERVER+ ':' + MAIL_PORT)
    server.starttls()
    server.login(MAIL_USERNAME, MAIL_PASSWORD)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()
    print('message sent')

    return jsonify({'charge': dict(charge)}), 200
    
@app.route('/api/loadTickets', methods = ['POST'])
def api_load_tickets():

    fd = dict(request.form)
    if not fd:
       return jsonify({'outcome': 'Missing parameters!'}), 422
 
    ticket = Ticket(eid = fd['event'])
    tickets = ticket.get()
    
    return tickets, 200

@app.route('/api/loadTicketData', methods = ['POST'])
def api_load_ticket_data():

    fd = dict(request.form)
    if not fd:
       return jsonify({'outcome': 'Missing parameters!'}), 422

    ticket = Ticket(tid = fd['id'])
    return ticket.getTicketData(), 200

@app.route('/api/verifyLogin', methods = ['GET'])
def api_verify_login():
    if not session.get('user'):
        return jsonify({'outcome': False}), 200
    else:
        return jsonify({'outcome': True}), 200




