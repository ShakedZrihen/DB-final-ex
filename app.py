from flask import Flask, request, Response, render_template
from flask_restful import Resource, Api
import db
import json

app = Flask(__name__)
api = Api(app)

my_db = db.MyDB()
my_db.connect()


@app.route('/')
def index():
    my_db.init_db()
    return render_template('index.html')


@app.route('/projects')
def projects():
    projects_table = my_db.show_table("projects")
    return render_template('projects.html', data=projects_table)


@app.route('/engineers', methods=['GET', 'POST', 'DELETE'])
def engineers():
    if request.method == 'GET':
        engineers_table = my_db.show_table("Engineers")
        return render_template('engineers.html', data=engineers_table)
    elif request.method == 'POST':
        data = request.json
        my_db.insert_into['engineers'](
            first_name=data["first_name"],
            last_name=data["last_name"],
            engineer_id=data["id"],
            field_id=data["field_id"],
            address=data["address"],
            birthday=data["birthday"])
        engineers_table = my_db.show_table("Engineers")
        if data["phones"]:
            for phone in data["phones"]:
                my_db.insert_into['phones'](
                    engineer_id=data["id"],
                    phone_number=phone
                )
        return render_template('engineers.html', data=engineers_table)
    else:
        data = request.data
        print "enid: {}".format(data)
        my_db.delete_from_engineer(data)
        return Response("success", 200)

@app.route('/phones/<string:engineer_id>')
def show_phones(engineer_id):
    phones_table = my_db.get_phones(engineer_id)
    resp = Response(json.dumps(phones_table))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/expertise')
def expertise():
    expertise_table = my_db.show_table("SoftwareField")
    return render_template('expertise.html', data=expertise_table)


if __name__ == '__main__':
    app.run(debug=True)