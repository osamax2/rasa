#coding: utf-8

from flask import Flask, url_for, request, jsonify, abort, make_response , session
import json
import logging
from pyjsonq import JsonQ
import time
from flask_session import Session
import random

app = Flask(__name__)
# Check Configuration section for more details
Session(app)
sess = Session()

messages = [
    {
        'id': 1,
        'title': u'not enough information',
        'question': u'Auf welchem Campus?',
        'type': u'campus'
    },
    {
        'id': 2,
        'title': u'not enough information',
        'question': u'Zu welcher Uhrzeit?',
        'type': u'time'
    },
     {
        'id': 3,
        'title': u'not enough information',
        'question': u'Zu welcher Datum?',
        'type': u'date'
    },
     {
        'id': 3,
        'title': u'not enough information',
        'question': u'Welches Zimmer bevorzugen Sie?',
        'type': u'room_number'
    },
     {
        'id': 4,
        'title': u'not enough information',
        'question': u'Welches Location bevorzugen Sie?',
        'type': u'room_location'
    }
]
# finde einen passend raum



def getroom() :
    if session.get('date').find(".") >= 0 :
        newdate1 = time.strptime(session.get('date'), "%d.%m.%Y")
    if session.get('date').find("/") >= 0 :
        newdate1 = time.strptime(session.get('date'), "%d/%m/%Y")
    restfinal =[]
    qu = JsonQ("data.json")
    if session.get('campus').find("Wi") >= 0 :
        res = qu.at('room.VCALENDAR.VEVENT').where('LOCATION', 'startswith', 'WH')\
                        .where("LOCATION", "endswith", session.get('room_number'))\
                        .where("LOCATION", "contains", session.get('room_location'))\
                        .get()
        for temp in res :
            dtstart = time.strptime(temp['DTSTART'], "%Y%m%dT%H%M%S")
            dtend = time.strptime(temp['DTEND'], "%Y%m%dT%H%M%S")
            if newdate1 < dtstart or  newdate1 > dtend :
                restfinal.append(temp)
        res = restfinal
        return res
    if session.get('campus').find("Ta") >= 0:
        res = qu.at('room.VCALENDAR.VEVENT').where('LOCATION', 'startswith', 'TA')\
                        .where("LOCATION", "endswith", session.get('room_number'))\
                        .where("LOCATION", "contains", session.get('room_location'))\
                        .get()
        for temp in res :
            dtstart = time.strptime(temp['DTSTART'], "%Y%m%dT%H%M%S")
            dtend = time.strptime(temp['DTEND'], "%Y%m%dT%H%M%S")
            if newdate1 < dtstart or  newdate1 > dtend :
                restfinal.append(temp)
        res = restfinal
        return res
    else :
        res = [
            {
                'id': 12,
                'title': u'not found',
                'question': u'Es gibt kein frei Raum',
                'type': u'date'
            }]
    return res

def getrooms(date, campus) :
    if date.find(".") >= 0 :
        newdate1 = time.strptime(date, "%d.%m.%Y")
    if date.find("/") >= 0 :
        newdate1 = time.strptime(date, "%d/%m/%Y")
    print(campus)
    restfinal =[]
    qu = JsonQ("data.json")
    if campus.find("Wi") >= 0 :
        res = qu.at('room.VCALENDAR.VEVENT').where('LOCATION', 'startswith', 'WH').get()
        for temp in res :
            dtstart = time.strptime(temp['DTSTART'], "%Y%m%dT%H%M%S")
            dtend = time.strptime(temp['DTEND'], "%Y%m%dT%H%M%S")
            if newdate1 < dtstart or  newdate1 > dtend :
                restfinal.append(temp)
        res = restfinal
        return res
    if campus.find("Ta") >= 0:
        res = qu.at('room.VCALENDAR.VEVENT').where('LOCATION', 'startswith', 'TA').get()
        return res
    else :
        res = [
            {
                'id': 12,
                'title': u'not found',
                'question': u'Es gibt kein frei Raum',
                'type': u'date'
            }]
    return res

# 1 entity
@app.route('/todo/api/v1.0/day/<string:m_day>', methods=['GET'])
def get_day(m_day):
    session['day'] = m_day
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/room_number/<string:m_room_number>', methods=['GET'])
def get_room_number(m_room_number):
    session['room_number'] = m_room_number
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/location/<string:m_room_location>', methods=['GET'])
def get_room_location(m_room_location):
    session['room_location'] = m_room_location
    messag = checkEntity()
    return jsonify({'message': messag})

# date wurde erkannt
@app.route('/todo/api/v1.0/date/<string:m_date>', methods=['GET'])
def get_date(m_date):
    session['date'] = m_date
    messag = checkEntity()
    return jsonify({'message': messag})


# campus wurde erkannt
@app.route('/todo/api/v1.0/campus/<string:m_campus>', methods=['GET'])
def get_campus(m_campus):
    session['campus'] = m_campus
    messag = checkEntity()
    return jsonify({'message': messag})




def checkEntity():
    if  session.get('date') and session.get('day')  and session.get('room_location')  and session.get('room_number') and session.get('campus') : # all Entity is there
        ####
    if session.get('date') and session.get('day')  and session.get('room_location')  and session.get('room_number') :  # 4 Entity is there
        room = getroom()
        return jsonify({'message': room})
    if session.get('date') and session.get('day')  and session.get('room_location')  and session.get('campus') :  # 4 Entity is there
        room = getroom()
        return jsonify({'message': room})
    if session.get('date') and session.get('day')  and session.get('campus')  and session.get('room_number') :  # 4 Entity is there
        room = getroom()
        return jsonify({'message': room})
    if session.get('date') and session.get('campus')  and session.get('room_location')  and session.get('room_number') :  # 4 Entity is there
        room = getroom()
        return jsonify({'message': room})
    if session.get('campus') and session.get('day')  and session.get('room_location')  and session.get('room_number') :  # 4 Entity is there
        room = getroom()
        return jsonify({'message': room})
    else :
        if session.get('day') and session.get('room_number')  and session.get('room_location') :
            #if this data is hier ruf function room
        if session.get('date') and session.get('day')  and session.get('campus') :
            #if this data is hier ruf function room
        if session.get('date') and session.get('room_location')  and session.get('day') :
            #if this data is hier ruf function room
        if session.get('date') and session.get('day')  and session.get('room_number') :
            #if this data is hier ruf function room
        if session.get('day') and session.get('room_location')  and session.get('room_number') :
            #if this data is hier ruf function room
        if session.get('date') and session.get('room_location')  and session.get('campus') :
            #if this data is hier ruf function room
        if session.get('date') and session.get('campus')  and session.get('room_number') :
            #if this data is hier ruf function room
        if session.get('campus') and session.get('room_location')  and session.get('room_number') :
            #if this data is hier ruf function room
        if session.get('day') and session.get('room_location')  and session.get('campus') :
            #if this data is hier ruf function room
        if session.get('day') and session.get('campus')  and session.get('room_number') :
            #if this data is hier ruf function room
        else :
            if session.get('date') and session.get('day'):
                x =  random.randint(2,4)
                message = [message for message in messages if message['id'] == x]
                if len(message) == 0:
                    abort(404)
                return message
            if session.get('day')  and session.get('room_location'):
                ####
            if session.get('room_location') and  session.get('date'):
                ####
            if session.get('day')  and session.get('room_number'):
                ###
            if session.get('room_number') and session.get('date'):
                ###
            if session.get('room_number') and session.get('room_location'):
                ###
            if session.get('date') and session.get('campus'):
                rooms = getrooms(session.get('date'),session.get('campus'))
                return rooms 
            if session.get('day') and session.get('campus'):
                ###
            if session.get('room_location') and session.get('campus'):
                ###
            if session.get('room_number') and session.get('campus'):
                ###
            else :
                if  session.get('date') :
                    ##
                if session.get('day'):
                    ##
                if session.get('room_location'):
                    ##
                if session.get('room_number'):
                    ##
                if session.get('campus'):
                    ##
                else:







# 2 entity
@app.route('/todo/api/v1.0/room_number/<string:m_room_number>/day/<string:m_day>', methods=['GET'])
def get_day_room_number(m_room_number,m_day):
    session['room_number'] = m_room_number
    session['day'] = m_day
    messag = checkEntity()
    return jsonify({'message': messag})

# date und campus wurde erkannt
# @app.route('/todo/api/v1.0/room/<string:m_date_campus>', methods=['GET'])
@app.route('/todo/api/v1.0/date/<string:m_date>/campus/<string:m_campus>', methods=['GET'])
def get_date_campus(m_date, m_campus):
    session['date'] = m_date
    session['campus'] = m_campus
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/date/<string:m_date>/day/<string:m_day>', methods=['GET'])
def get_date_day(m_date, m_day):
    session['date'] = m_date
    session['day'] = m_day
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/date/<string:m_date>/room_location/<string:m_room_location>', methods=['GET'])
def get_date_room_location(m_date, m_room_location):
    session['date'] = m_date
    session['room_location'] = m_room_location
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/date/<string:m_date>/room_number/<string:m_room_number>', methods=['GET'])
def get_date_room_number(m_date, m_room_number):
    session['date'] = m_date
    session['room_number'] = m_room_number
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/day/<string:m_day>/campus/<string:m_campus>', methods=['GET'])
def get_day_campus(m_day, m_campus):
    session['day'] = m_day
    session['campus'] = m_campus
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/day/<string:m_day>/room_location/<string:m_room_location>', methods=['GET'])
def get_day_room_location(m_day, m_room_location):
    session['day'] = m_day
    session['room_location'] = m_room_location
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/room_location/<string:m_room_location>/room_number/<string:m_room_number>', methods=['GET'])
def get_room_location_room_number(m_room_location, m_room_number):
    session['room_location'] = m_room_location
    session['room_number'] = m_room_number
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/room_location/<string:m_room_location>/campus/<string:m_campus>', methods=['GET'])
def get_room_location_campus(m_room_location, m_campus):
    session['room_location'] = m_room_location
    session['campus'] = m_campus
    messag = checkEntity()
    return jsonify({'message': messag})

@app.route('/todo/api/v1.0/room_number/<string:m_room_number>/campus/<string:m_campus>', methods=['GET'])
def get_room_number_campus(m_room_number, m_campus):
    session['room_number'] = m_room_number
    session['campus'] = m_campus
    messag = checkEntity()
    return jsonify({'message': messag})



# 3 entity
@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    message = checkEntity()
    return jsonify({'message': message})


# 4 entity not finich
@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>/date/<string:m_date>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number,m_date):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    session['date'] = m_date
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>/date/<string:m_date>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number,m_date):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    session['date'] = m_date
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>/date/<string:m_date>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number,m_date):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    session['date'] = m_date
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>/date/<string:m_date>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number,m_date):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    session['date'] = m_date
    message = checkEntity()
    return jsonify({'message': message})

@app.route('/todo/api/v1.0/campus/<string:m_campus>/day/<string:m_day>/room_number/<string:m_room_number>/date/<string:m_date>', methods=['GET'])
def get_data_2(m_campus,m_day,m_room_number,m_date):
    session['campus'] = m_campus 
    session['day'] = m_day
    session['room_number'] = m_room_number
    session['date'] = m_date
    message = checkEntity()
    return jsonify({'message': message})

# 5 entity


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.run(debug=False, host='0.0.0.0')