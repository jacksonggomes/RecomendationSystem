from flask import Flask
from flask import request
from mongo import mongo_requests
from libs import recomendationLib
app = Flask(__name__)


@app.route('/recomend', methods=['POST'])
def recomend():
    if request.method == 'POST':
        return {'recomendation': recomendationLib.recomend_api(request.form['username'], request.form['service'])}

@app.route('/evaluate', methods=['POST'])
def evaluate():
    if request.method == 'POST':
        return {'evaluate': mongo_requests.evaluate(request.form['username'],
                                                    request.form['service'], request.form['evaluation_elment'],
                                                    request.form['point'], is_company=request.form['is_company'])}

@app.route('/getservices')
def get_services():
    return {'services': mongo_requests.get_all_services()}

@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        return {'login': mongo_requests.login(request.form['username'], request.form['password'])}

if __name__ == '__main__':

    app.run(host='192.168.137.1')