import datetime, os
from flask import Flask, jsonify, redirect, request, url_for
# from flask_bcrypt import Bcrypt
from flask_hashing import Hashing
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{os.path.join(project_dir, 'firearm.db')}"


app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)
hashing = Hashing(app)
ma = Marshmallow(app)


class Firearm(db.Model):
    """Model for managing firearms

    Record each firearm sold to licensed firearm user.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    state = db.Column(db.String(120))
    nin = db.Column(db.Integer)
    dob = db.Column(db.DateTime) # Date of birth
    gun = db.Column(db.String(225)) # Gun Serial Number
    bullet = db.Column(db.String(225)) # Bullet Serial Number
    
    def __repr__(self) -> str:
        return f"{self.name}"


class FirearmSchema(ma.Schema):
    """Serializes and deserializes firearm object."""
    class Meta:
        fields = (
            'name', 'state', 'nin', 'dob', 'gun', 'bullet'
        )


firearm_schema = FirearmSchema()
firearms_schema = FirearmSchema(many=True)


@app.route('/create/', methods=["GET", "POST"])
def create_firearm():
    if request.form:
        firearm = Firearm(
            name=request.form.get("name"),
            dob=datetime.datetime.strptime(
                request.form.get("dob"), "%m-%d-%Y"),
            state=request.form.get("state"),
            nin=request.form.get("nin"),
            # gun=bcrypt.generate_password_hash(request.form.get("gun").lower()),
            # bullet=bcrypt.generate_password_hash(request.form.get("bullet").lower())
            gun=hashing.hash_value(
                request.form.get("gun").lower(), salt="gunHash"
            ),
            bullet=hashing.hash_value(
                request.form.get("bullet").lower(), salt="bulletHash"
            )
        )
        db.session.add(firearm)
        db.session.commit()
        return jsonify(firearm_schema.dump(firearm))
    return jsonify({"status": "Created"})


@app.route('/search/<bullet>/', methods=["GET"])
def search(bullet):
    # bullet_hash = bcrypt.generate_password_hash(bullet.lower())
    bullet_hash = hashing.hash_value(bullet.lower(), salt="bulletHash")
    firearms = Firearm.query.filter_by(bullet=bullet_hash)
    if firearms:
        return redirect(url_for("results", bullet=bullet))
    return jsonify({"message": "No record found"})


@app.route('/results/<bullet>/', methods=["GET"])
def results(bullet):
    # bullet_hash = bcrypt.generate_password_hash(bullet.lower())
    bullet_hash = hashing.hash_value(bullet.lower(), salt="bulletHash")
    firearms = Firearm.query.filter_by(bullet=bullet_hash)
    if firearms:
        return jsonify(firearms_schema.dump(firearms))
    return jsonify({"message": "No record found"})



if __name__ == "__main__":
    app.run()
