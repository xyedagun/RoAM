from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import User, Folder, Place, Place_folder, connect_to_db, db
import sample_query 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Show homepage."""



    user_id = session.get('user_id')
    folders = Folder.query.filter_by(user_id=user_id).all()

    if user_id in session:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
        session['user_id'] = existing_user.user_id



    return render_template("base.html", folders=folders)



@app.route('/folder')
def opening_folder():
    """This shows the places in user's folder when a folder is clicked"""
    folder_id = request.args.get('folder_id')
    user_id = session.get('user_id')

    folder = Folder.query.get(folder_id)
    user_places = Place_folder.query.filter_by(folder_id = folder_id).all()
    places = Place.query.filter(user_places==user_places).all()

    return render_template("main.html", user_id=user_id, user_places=user_places, places=places, folder=folder)
    



@app.route('/results', methods=['POST'])
def get_result():
    """Shows the top results"""

    location = request.form.get("location")

    attraction_results = sample_query.search_attractions(location)
    hotel_results = sample_query.search_hotels(location)
    restaurant_results = sample_query.search_restaurants(location)
    museum_results = sample_query.search_museums(location)
    festival_results = sample_query.search_festivals(location)

    user_id = session.get('user_id')
    # import pdb; pdb.set_trace()
    folders = Folder.query.filter_by(user_id=user_id).all()

    print attraction_results, hotel_results,location

    return render_template('index.html', location=location, folders=folders, attraction_results=attraction_results, hotel_results=hotel_results, restaurant_results=restaurant_results, museum_results=museum_results, festival_results=festival_results)
        




@app.route('/process-search-form', methods=["POST"])
def process_form():

    search = request.form.get("query")
    location = request.form.get("location")

    api_result = sample_query.search_places(search, location)
    # print location, api_result

    return render_template('index.html', api_result=api_result) # the api_result will be included on the map.html



@app.route('/add-to-folder', methods=["POST"])
def add_to_folder():

    username = session['logged_in_user']
    print username
    folderName = request.form.get("folder_name")
    business_id = request.form.get("business_id")
    existing_place = Place.query.filter_by(business_id = business_id).first()



    
    business = sample_query.yelp_api.business_query(id=business_id)
    if business['location']['address']:
        address = business['location']['address'][0]
    else:
        address = ""
    if business['categories'][0]:
        category_description, category = business['categories'][0]
    else:
        category = ""

    if business['name']:
        name = business['name']
    else:
        name = ""

    if business['location']['coordinate']['latitude']:
        latitude = business['location']['coordinate']['latitude']
    else:
        latitude = None

    if business['location']['coordinate']['longitude']:
        longitude = business['location']['coordinate']['longitude']
    else:
        longitude = None

    if business['location']['city']:
        city = business['location']['city']
    else:
        city = ""

    if business['location']['country_code']:
        country = business['location']['country_code']
    else:
        country = ""
    
    print session['user_id']
    print folderName
    if not existing_place:
        
        new_place = Place(business_id=business_id, category=category, name=name, address=address, latitude=latitude, longitude=longitude, city=city, country=country)

        db.session.add(new_place)
        db.session.commit()
        place_id = new_place.place_id
    else:
        place_id = existing_place.place_id

    folder = Folder.query.filter_by(user_id = session['user_id'], folder_name = folderName).first()
    print folder
    folder_id = folder.folder_id
    print folder_id, place_id
    new_place_folder = Place_folder(place_id=place_id, folder_id=folder_id)
    db.session.add(new_place_folder)
    db.session.commit()


    return redirect("/results")





@app.route('/folders')
def show_folders():
    """This is to query folder based on logged in user"""
    
    user_id = session.get('user_id')
    folders = Folder.query.filter_by(user_id=user_id).all()

    # we're done - we just need to serialize these folders and return them
    folder_dicts = []
    for folder in folders:
        folder_dicts.append(folder.to_dict())

    return jsonify({'folders': folder_dicts})




@app.route('/new_folder', methods=["POST"])
def create_folder():

    user_id = session.get('user_id')
    print user_id
    folderName = request.form.get("FolderName")
    # business_id = request.form.get("business_id")

    
    
    new_folder = Folder(user_id=user_id, folder_name=folderName)
    # existing_folder = Folder.query.filter(Folder.folder_name == folderName).first()
    db.session.add(new_folder)
    db.session.commit()
    folder_id = new_folder.folder_id

    folder = new_folder


    return "success"






@app.route('/submit', methods=["POST"])
def submit():
    """Sign in page."""

    user = request.form.get("username")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")

    existing_user = User.query.filter(User.user_name == user).first()

    if not existing_user:
    	new_user = User(user_name=user, fname=first_name, lname=last_name, email=email, password=password)
    	#white is column name from route, orange is the variable from model.py
    	db.session.add(new_user)
    	db.session.commit()
    	session['logged_in_user'] = new_user.user_name
        session['firstname'] = new_user.fname
        #
    else:
    	session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
        folder = Folder.query.filter_by(user_id = session['user_id'], folder_name = folderName).first()
    
    return render_template("base.html")
    

@app.route('/logged-in', methods=["POST"])
def log_in():
    """Log in page. Need to make sure the user enter correct password."""

    user = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(user_name=user, password=password).first()


    if user == existing_user.user_name:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
        session['user_id'] = existing_user.user_id
    else:
        print "Try again"

    user_id = session.get('user_id')    
    folders = Folder.query.filter_by(user_id=user_id).all()

    return render_template("base.html", folders=folders)



@app.route('/modal-loggedIn', methods=["POST"])
def modalLoggedIn():
    """Log in in modal window"""

    user = request.form.get("username")
    password = request.form.get("password")

    existing_user = User.query.filter_by(user_name=user, password=password).first()

    if user == existing_user.user_name:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
    else:
        print "Try again"

    return redirect("/results")



@app.route('/signup', methods=["POST"])
def signUp():
    """Sign up page in modal window"""

    user = request.form.get("username")
    first_name = request.form.get("firstname")
    last_name = request.form.get("lastname")
    email = request.form.get("email")
    password = request.form.get("password")


    existing_user = User.query.filter(User.user_name == user).first()

    if not existing_user:
        new_user = User(user_name=user, fname=first_name, lname=last_name, email=email, password=password)
        #white is column name from route, orange is the variable from model.py
        db.session.add(new_user)
        db.session.commit()
        session['logged_in_user'] = new_user.user_name
        session['firstname'] = new_user.fname
        session['user_id'] = new_user.user_id
        #
    else:
        session['logged_in_user'] = existing_user.user_name
        session['firstname'] = existing_user.fname
        session['user_id'] = existing_user.user_id

    folders = Folder.query.filter_by(user_id=user_id).all()

    return render_template("base.html", folders=folders)


@app.route('/log-out')
def log_out():
    """Log out page"""


    session.clear()

    # if not 'logged_in_user' in session:
    # 	message = "You're not logged in"
    # else:
    # 	message = "You've been logged out"
    # 	del session['logged_in_user']
    	#to delete user from session
    return redirect("/") 



    

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()