from flask import Flask, request, jsonify, send_file, abort, render_template, render_template_string
from flask_sqlalchemy import SQLAlchemy
import time
import matplotlib.pyplot as plt
plt.switch_backend('Agg')
import io
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

API_KEY = 'SmileAndWave'

app.static_folder = 'static'

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    epoch_time = db.Column(db.Integer, nullable=False)
    temp1 = db.Column(db.Float, nullable=False)
    dist1 = db.Column(db.Float, nullable=False)
    dist2 = db.Column(db.Float, nullable=False)

@app.before_request
def create_tables():
    db.create_all()

def check_api_key():
    api_key = request.args.get('api_key')
    if api_key != API_KEY:
        abort(401)

@app.route('/', methods=['GET'])
def index():
    html = '''
    Avalible endpoints
    <a href="/add_data">/add_data</a> (requires api_key)
    <a href="/view_data">/view_data</a>
    <a href="/graph">/graph</a>
    <a href="/about">/about</a>
    '''
    return render_template_string(html)

@app.route('/add_data', methods=['POST'])
def add_data():
    check_api_key()
    data = request.json
    epoch_time = int(time.time())
    new_data = Data(
        epoch_time=epoch_time,
        temp1=data['temp1'],
        dist1=data['dist1'],
        dist2=data['dist2']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data added successfully'}), 201

@app.route('/view_data', methods=['GET'])
def view_data():
    two_weeks_ago = int(time.time()) - 2 * 7 * 24 * 60 * 60
    rows = Data.query.filter(Data.epoch_time >= two_weeks_ago).all()

    return render_template('table.html', rows=rows)


@app.route('/about', methods=['GET'])
def about_page():
    return render_template('about.html')

@app.route('/view_graph_data', methods=['GET'])
def view_graph_data():
    two_weeks_ago = datetime.now() - timedelta(days=14)
    data = Data.query.filter(Data.epoch_time >= int(two_weeks_ago.timestamp())).all()
    dates = [datetime.fromtimestamp(d.epoch_time).isoformat() for d in data]
    temp1 = [d.temp1 for d in data]
    dist1 = [d.dist1 for d in data]
    dist2 = [d.dist2 for d in data]
    return jsonify({'dates': dates, 'temp1': temp1, 'dist1': dist1, 'dist2': dist2})



@app.route('/graph', methods=['GET'])
def view_graph_page():

    return render_template('graph.html')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
