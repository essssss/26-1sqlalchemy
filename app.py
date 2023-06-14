"""Demo app using SQLAlchemy."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()


@app.route('/')
def list_pets():
    """Shows list of all pets in database"""
    
    pets = Pet.query.all()
    return render_template('list.html', pets=pets)


@app.route("/", methods=["POST"])
def create_new_pet():
    name = request.form["name"]
    species = request.form["species"]
    hunger = request.form["hunger"]
    hunger = int(hunger) if hunger else None

    new_pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(new_pet)
    db.session.commit()

    return redirect(f"/{new_pet.id}")

@app.route("/<int:pet_id>")
def show_pet(pet_id):
    """Show details about a single pet"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template("details.html", pet=pet)

@app.route('/species/<species_name>')
def show_pet_by_species(species_name):
    pets = Pet.get_by_species(species_name)
    return render_template("species.html", pets=pets, species=species_name)