from distutils.log import debug
from flask import Flask, render_template, request
#import configparser for api
import configparser
import requests

#puts module(congifparser)'s class (ConfigParser) inside config(object)
def get_api_key():
    config=configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']

#city name accepts as parameters..remove the city bame in api url and add format() to fill in curly brackets
def get_weather_result(city_name,api_key):
    api_url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}".format(city_name,api_key)
    r=requests.get(api_url)
    return r.json()

#get_weather_result("bokaro",get_api_key())

app = Flask(__name__)

@app.route("/")
def weather_dashboard():
    return render_template('home.html')

@app.route('/results',methods=['POST'])
def render_results():
    city_name=request.form['nameofcity']  #return form's data which is text input and store in city_name
    
    api_key=get_api_key()
    data=get_weather_result(city_name,api_key)
    #formatting floating numbers are present into strings

    temp="{0:.2f}".format(data["main"]["temp"])
    feels_like="{0:.2f}".format(data["main"]["feels_like"])
    #weather is array which has dictinary object and only one elemt at index 0 so 
    weather=data["weather"][0]["main"]
    pressure="{0:.2f}".format(data["main"]["pressure"])
    humidity="{0:.2f}".format(data["main"]["humidity"])
    wind_speed="{0:.2f}".format(data["wind"]["speed"])

    CITY_name=city_name.upper()

    #calling and retrundinf results page and passing the variavbles to results.html which has jinja variables with same name(jinja variables can have any name)
    return render_template('results.html', city_name=CITY_name,
                                            temp=temp ,
                                            feels_like=feels_like, 
                                            weather=weather,
                                            pressure=pressure,
                                            humidity=humidity,
                                            wind_speed=wind_speed)
    #return "result page"

#ensures app only runs once and multipke instance are not craeted
if __name__=='__main__':
    app.debug=True
    app.run()