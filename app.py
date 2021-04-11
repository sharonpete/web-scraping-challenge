from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import scrape_mars

app = Flask(__name__)

#mongo = PyMongo(app, uri="mongodb://localhost:27017/nasa_db")
app.config["MONGO_URI"] = "mongodb://localhost:27017/nasa_db"
mongo = PyMongo(app)

@app.route('/')
def index():
    data = list(mongo.db.items.find_one())
    print(f'THIS IS MARS!!! {data}')
    return render_template('index.html', data=data)
    

@app.route('/scrape')
def scrape():
    mars = mongo.db.items
    data = scrape_mars.scrape()
    print(data)
    mars.update_many(  #changed per deprecation warning
        {},
        data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
