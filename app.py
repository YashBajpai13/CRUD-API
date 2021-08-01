import sqlalchemy
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, desc
import json
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True, nullable = False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    company_name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zip = db.Column(db.Integer)
    email = db.Column(db.String(100))
    web = db.Column(db.String(256))
    age = db.Column(db.Integer)


    def __repr__(self):
        result = {"id" : self.id, "first_name" : self.first_name, "last_name" : self.last_name, "company_name" : self.company_name,
                  "city" : self.city, "state" : self.state, "zip" : self.zip, "email" : self.email, "web" : self.web, "age" : self.age}
        return json.dumps(result)

@app.route('/', methods = ['GET'])
def test():
    return "API Running"


@app.route('/users', methods = ['GET', 'POST'])
def get_or_create_users():
    if request.method == 'POST':
        if type(request.json) == type(list()):
            for x in request.json:
                id = x['id']
                first_name = x['first_name']
                last_name = x['last_name']
                company_name = x['company_name']
                city = x['city']
                state = x['state']
                zip = x['zip']
                email = x['email']
                web = x['web']
                age = x['age']
                new_user = Users(id=id, first_name=first_name, last_name=last_name, company_name=company_name,
                                 city=city,
                                 state=state, zip=zip, email=email, web=web, age=age)
                db.session.add(new_user)
                db.session.commit()
        return "Multiple Users Added"

        id = request.json['id']
        first_name = request.json['first_name']
        last_name = request.json['last_name']
        company_name = request.json['company_name']
        city = request.json['city']
        state = request.json['state']
        zip = request.json['zip']
        email = request.json['email']
        web = request.json['web']
        age = request.json['age']
        new_user = Users(id = id, first_name = first_name, last_name = last_name, company_name = company_name, city = city,
                         state = state,zip = zip, email = email, web = web , age = age)
        try:
            db.session.add(new_user)
            db.session.commit()
            return "User Added", 201
        except:
            return "Failed"

    if request.method == "GET" :
        page = 1
        limit = 5
        if "name" in request.args:
            substr = request.args["name"]
            if "sort" in request.args :
                sort = request.args["sort"]
                if '-' in sort:
                    sort = sort[1:len(sort)]
                    query = Users.query.filter(or_(Users.first_name.like(f'%{substr}%'), Users.last_name.like(f'%{substr}%'))).order_by(desc(sort)).limit(limit).all()
                else:
                    query = Users.query.filter(sqlalchemy.or_(Users.first_name.like(f'%{substr}%'), Users.last_name.like(f'%{substr}%'))).order_by(sort).limit(limit).all()
            else :
                query = Users.query.filter(or_(Users.first_name.like(f'%{substr}%'), Users.last_name.like(f'%{substr}%'))).limit(limit).all()
            return str(query)
        elif "sort" in request.args:
            sort = request.args["sort"]
            if "-" in sort:
                sort = sort[1:len(sort)]
                query = Users.query.order_by(desc(sort)).limit(limit).all()
            else:
                query = Users.query.order_by(sort).limit(limit).all()
            return str(query)
        else:
            query = Users.query.limit(limit).all()
            return str(query)


@app.route("/users/<int:id>", methods = ["GET", "PUT", "DELETE"])
def get_delete_update_by_id(id):
    if request.method == "GET":
        query = Users.query.filter(Users.id == id).all()
        return str(query)
    if request.method == "DELETE":
        delete_user = Users.query.get_or_404(id)
        try :
            db.session.delete(delete_user)
            db.session.commit()
            return "Deleted successfully"
        except:
            return "Failed to delete"
    if request.method == "PUT":
        new_first_name = request.json["first_name"]
        new_last_name = request.json["last_name"]
        new_age = request.json["age"]
        query = Users.query.get_or_404(id)
        query.first_name = new_first_name
        query.last_name = new_last_name
        query.age = new_age
        try:
            db.session.commit()
            return "Updated Successfully"
        except:
            return "Failed to update"

if __name__ == "__main__":
    app.run(debug = True)