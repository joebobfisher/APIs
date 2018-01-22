from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




#foursquare_client_id = 'PPLTRCLFQWHDYILXAT3G3B0RLK15VFLQIUT4KT51AXAVFAL2'

#foursquare_client_secret = 'D2FQPOZDFUQGYURIAGEJZRYN1XG3BFRYNEHWXSR1DPF41HYY'

#google_api_key = 'AIzaSyDMJe0NqKhTlH9L6LxdfosucGk4CDwHHOY'

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
  #YOUR CODE HERE
    if request.method == 'GET':
        # get all the restaurants in Restaurant DB
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants = [i.serialize for i in restaurants])
    elif request.method == 'POST':
        location = request.args.get('location', '')
        mealType = request.args.get('mealType', '')
        restaurant_info = findARestaurant(mealType, location)
        if restaurant_info != "No Restaurants Found":
            restaurant = Restaurant(restaurant_name = unicode(restaurant_info['name']), restaurant_address = unicode(restaurant_info['address']), restaurant_image = restaurant_info['image'])
            session.add(restaurant)
            session.commit() 
            return jsonify(restaurant = restaurant.serialize)
        else:
            return jsonify({"error":"No Restaurants Found for %s in %s" % (mealType, location)})

@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
  #YOUR CODE HERE
    restaurant = session.query(Restaurant).filter_by(id = id).one()
    if request.method == 'GET':
        # from the models.py decorator
        return jsonify(restaurant = restaurant.serialize)
    elif request.method == 'PUT':
        address = request.args.get('address')
        image = request.args.get('image')
        name = request.args.get('name')
        if address:
            restaurant.restaurant_address = address
        if image:
            restaurant.restaurant_image = image
        if name:
            restaurant.restaurant_name = name
        session.commit()
        return jsonify(restaurant = restaurant.serialize)

    elif request.method == 'DELETE':
        session.delete(restaurant)
        session.commit()
        return "Restaurant Deleted"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


  
