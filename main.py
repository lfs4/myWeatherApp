import yfinance as yt
import requests
import json
import sys
import random
from flask import (
    Flask,
    jsonify,
    request,
    render_template,
    Response,
)
from flask_bootstrap import Bootstrap


app = Flask(__name__)


def proccessJson(obj):
    rjson = obj.json()
    print(type(rjson))
    #city = json.loads(rjson)
    json_string = json.dumps(rjson) #([ob for ob in rjson])
    json_ob = json.loads(json_string)
    return json_ob

def buildImgUrl(reqData):

    return f"https://farm{reqData['farm']}.staticflickr.com/{reqData['server']}/{reqData['id']}_{reqData['secret']}.jpg"

def getBackgroundImage(tag):
    r = requests.get(f"https://www.flickr.com/services/rest/?method=flickr.photos.search&api_key=0a12eec13a89cc01a758a10671c78fcc&tags={tag}&safe_search=&format=json&nojsoncallback=1")
    jData = proccessJson(r)
    randIndex = random.randrange(0,len(jData["photos"]["photo"]) - 1);
    print(randIndex, file=sys.stdout)
    img = jData["photos"]["photo"][randIndex]
    print(img, file=sys.stdout)
    return buildImgUrl(img)




def getWeatherHourly(city):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/forcast/hourly?q={city}&appid=d6b5eb04a714a1bbeb1771261b1a2c47")
    return proccessJson(r)

def getCurrentWeather(city):
    r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=d6b5eb04a714a1bbeb1771261b1a2c47")

    return proccessJson(r)

@app.route('/weather/<city>')
def currentWeather(city):
    json_ob = getCurrentWeather(city)
    imgSearchTag = json_ob["weather"][0]['description']
    background = getBackgroundImage(imgSearchTag)
    return render_template("current.html",request_data=json_ob , img_data=imgSearchTag, bg=background)

@app.route('/hourly/<city>')
def hourlyWeather(city):
    json_ob = getWeatherHourly(city)


    return render_template("hourly.html",request_data=json_ob)

@app.route('/weather/<city>.json')
def dumpJson(city):
    return returnApiJson(city);


@app.route('/weather/<city>.html')
def dumpHtml(city):
    return returnApiJson(city);


if __name__ == '__main__':
    app.run(debug=True)



# def get_stock_data(company, period="1d"):
#     company = yt.Ticker(company)
#     return company.history(period=period)

# @app.route('/ping')
# def pong():
#     return jsonify({
#         "pong": 1,
#     })
#
# @app.route('/company/<company>.json')
# def stock_price_1d_json(company):
#     stock_data = get_stock_data(company).to_json()
#     r = requests.get("https://www.metaweather.com/api/location/search/?query=san")
#     return Response(
#         jsonify(r.json()),
#         mimetype="application/json")
#
#
# @app.route('/company/<company>.html')
# def stock_price_1d_html(company):
#     stock_data = get_stock_data(company).to_html()
#     # r = requests.get("https://www.metaweather.com/api/location/search/?query=san")
#     return render_template("company.html", name=company, data=stock_data)
