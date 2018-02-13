from app import db, app
from sqlalchemy import create_engine, text
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from flask import flash, jsonify
from flask_login import UserMixin
import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class User(UserMixin):
    meta = db.MetaData()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    table = db.Table('user', meta, autoload=True, autoload_with=engine)
    uid = table.columns.id
    username = table.columns.userName
    password = table.columns.password
    name = table.columns.name
    surname = table.columns.surname
    picture = table.columns.picture
    role = table.columns.role

    conn = engine.connect()
    trans = conn.begin()

    def __init__(self, role = None, username = None, password = None, name=None, surname=None, uid = None, aboutme = None, picture = None):
        self.role = role
        self.username = username
        self.password = password
        self.name = name
        self.surname = surname
        self.id = uid
        self.aboutme = aboutme
        self.picture = picture
        super(User, self).__init__()

    def __repr__(self):
        return '<User %s>' % self.id

    def is_active(self):
        return True

    @property
    def is_authenticated(self): 
            return True

    def get_id(self):
        return unicode(self.id)

    def exists(self):
        sql = text('select 1 from user where username = :username')
        result = self.engine.execute(sql, username = self.username) 
        res = []
        for r in result:
            res.append(r)
        if len(res) > 0:
            return True
        else:
            return False
        
    def register(self):
       sql = text('insert into user(userName, password, name, surname, aboutme, role) values (:username,:password,:name,:surname,:aboutme, :role)') 
       self.engine.execute(sql, username=self.username, password=self.password, name=self.name, surname=self.surname, aboutme=self.aboutme, role=self.role)
       return True 


    def login(self):
        username = self.username
        password = self.password
        sql = text('select * from user where username = :username and password = :password')         
        result = self.engine.execute(sql, username = username, password = password)
        res = result.fetchone()
        
        if res:
           return res
        else:
           return False

    def updateInfo(self):
        name = self.name
        surname = self.surname
        uid = self.id
        aboutme = self.aboutme
        role = self.role
        sql = text('update user set name = :name, surname = :surname, aboutme = :aboutme, role = :role where id = :uid')
        result = self.engine.execute(sql, name = name, surname = surname, uid = uid, aboutme = aboutme, role = role)
        return self

    def updateAllInfo(self):
        name = self.name
        surname = self.surname
        uid = self.id
        aboutme = self.aboutme
        role = self.role
        sql = text('update user set name = :name, surname = :surname, aboutme = :aboutme, picture = :picture, role = :role where id = :uid')
        result = self.engine.execute(sql, name = name, surname = surname, uid = uid, picture = self.picture, aboutme = aboutme, role = role)
        return self

    def getUserData(self):
        sql = text('select * from user u inner join roles r on u.role = r.role where id = :uid')
        result = self.engine.execute(sql, uid = self.id)
        return json.dumps([dict(r) for r in result])

    def getUserProfileInfo(self):
        sql = text('select * from user where id = :uid')
        result = self.engine.execute(sql, uid = self.id)
        return json.dumps([dict(r) for r in result])


    def getAllEvents(self):
        uid = self.id
        #sql = text('select * from events')
        sql = text('select *, (select count(comment) from comments where eid = ev.id group by eid) as numberOfComments,'+ 
                              '(select count(reaction) from comments where eid = ev.id and reaction = "like" group by eid) as likes,'+
                              '(select count(reaction) from comments where eid = ev.id and reaction = "love" group by eid) as love '+ 
                            'from events ev')
        result = self.engine.execute(sql)
        return json.dumps([dict(r) for r in result]) 

    def getMyEvents(self):
        uid = self.id
        sql = text('select * from events where userId =:uid')
        result = self.engine.execute(sql, uid = uid)
        return json.dumps([dict(r) for r in result]) 

    def setProfilePic(self):
        sql = text('update user set picture = :picture where id = :uid')
        res = self.engine.execute(sql, picture = self.picture, uid = self.id)
        return True

    def updatePassword(self):
        p = self.password
        u = self.username
        sql = text('update user set password = :password where username = :username')
        result = self.engine.execute(sql, password = p, username = u)
        return True  

    def returnUserData(self):
        res = self.engine.execute('select * from user')
        return [dict(r) for r in res]

    def getToken(self, expiration=100):
        s = Serializer('SECRET_KEY', expiration)
        return s.dumps({'username': self.username}).decode('utf-8')

    def verifyToken(self,token):
        s = Serializer('SECRET_KEY')
        try:
            data = s.loads(token)
        except:
            return None
        username = data.get('username')
        print username
        return username
        
class Event():
    meta = db.MetaData()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    table = db.Table('events', meta, autoload=True, autoload_with=engine)
    
    eid = table.columns.id
    uid = table.columns.userId
    title = table.columns.eventTitle 
    image = table.columns.eventImage
    created = table.columns.eventCreated
    time = table.columns.eventTime
    description = table.columns.eventDescription
    lat = table.columns.lat
    lng = table.columns.lng
    
    conn = engine.connect()
    trans = conn.begin()

    def __init__(self, eid = None, title = None, created = None, time=None, description = None, image=None,  uid=None, lng=None, lat=None):
        self.title = title
        self.image = image
        self.created = created
        self.time = time
        self.uid = uid
        self.description = description
        self.lat = lat
        self.lng = lng
        self.eid = eid

    def add(self):
        sql = text('insert into events(userId, eventTitle, eventCreated, eventTime, eventImage, eventDescription, lat, lng) values (:uid, :eTitle, :eCreated, :eTime, :eImage, :eDescription, :lat, :lng)')

        res = self.engine.execute(sql, uid = self.uid, eTitle = self.title, eCreated = self.created, eTime = self.time, eImage = self.image, eDescription = self.description, lat = self.lat, lng = self.lng)
        return self

    def removeEvent(self):
        sql = text('delete from events where id = :id') 
        res = self.engine.execute(sql, id = self.eid)
        print self.eid
        print res
        return self

    def getEventData(self):
        sql = text('select * from events where id = :id')
        res = self.engine.execute(sql, id = self.eid)
        return json.dumps([dict(r) for r in res])

    def returnId(self):
        sql = text("select id from events where eventCreated = :eCreated")
        res = self.engine.execute(sql, eCreated = self.created)
        return [dict(r) for r in res][0]['id']

class Comment():
    meta = db.MetaData()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    table = db.Table('comments', meta, autoload=True, autoload_with=engine)
    
    cid = table.columns.id
    eid = table.columns.eid
    uid = table.columns.uid
    comment = table.columns.comment
    reaction = table.columns.reaction
    
    conn = engine.connect()
    trans = conn.begin()

    def __init__(self, eid = None, uid = None, comment = None, reaction = None):
        self.eid = eid
        self.uid = uid
        self.comment = comment
        self.reaction = reaction

    def postComment(self):
        sql = text('insert into comments (eid, uid, comment) values (:eid, :uid, :comment)')
        res = self.engine.execute(sql, eid = self.eid, uid = self.uid, comment = self.comment)
        return self

    def loadComments(self):
        sql = text('select * from comments c inner join user u on u.id = c.uid where eid = :eid and comment is not null')
        res = self.engine.execute(sql, eid = self.eid)
        return json.dumps([dict(r) for r in res])

    def addReaction(self):
        sql = text('insert into comments(eid, uid, reaction) values (:eid, :uid, :reaction)')
        res = self.engine.execute(sql, eid = self.eid, uid = self.uid, reaction = self.reaction)
        return self

class Ticket():
    meta = db.MetaData()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    table = db.Table('tickets', meta, autoload=True, autoload_with=engine)
    
    tid = table.columns.id
    eid = table.columns.eid
    type = table.columns.type
    price = table.columns.price
    currency = table.columns.currency
    
    conn = engine.connect()
    trans = conn.begin()

    def __init__(self, eid = None, tid = None, type = None, price = None, currency = None):
        self.tid = tid
        self.eid = eid
        self.type = type
        self.price = price
        self.currency = currency

    def save(self):
        sql = text('insert into tickets (eid, type, price, currency) values (:eid, :type, :price, :currency)')
        res = self.engine.execute(sql, eid = self.eid, type = self.type, price = self.price, currency = self.currency)
        return self

    def get(self):
        sql = text('select * from tickets where eid = :eid')
        res = self.engine.execute(sql, eid = self.eid)
        return json.dumps([dict(r) for r in res])

    def getTicketData(self):
        sql = text('select * from tickets t '+ 
                        'join events e on t.eid = e.id ' +
                        'join user u on e.userId = u.id ' +
                        'where t.id = :tid')
        res = self.engine.execute(sql, tid = self.tid)
        return json.dumps([dict(r) for r in res])
