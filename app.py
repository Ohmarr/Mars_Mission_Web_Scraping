from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")



# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_collection.find()
    # Return template and data
    print(mars_data)

    return render_template("index.html", mars_data=mars_data)

@app.route("/hemispheres")
def hemispheres():

    # Find one record of data from the mongo database
    mars_data = mongo.db.mars_collection.find()
    # Return template and data
    print(mars_data)
    
    return render_template("hemispheres.html", mars_data=mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mongo.db.mars_collection.drop()
    # Run the scrape function
    all_mars_urls = scrape_mars.scrape_info()

    for url in all_mars_urls:
        # Dictionary to be inserted into MongoDB
        mongo.db.mars_collection.insert_one(url)

    # Update the Mongo database using update and upsert=True
    #collection.update({}, scrape_mars, upsert=True)
    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
