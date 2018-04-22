from cloudant import Cloudant
from flask import Flask, render_template, request, jsonify, flash, url_for, redirect, make_response
import atexit
import cf_deployment_tracker
import os
import json
from connection_backend import(cb_get_results)

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

db_name = 'mydb'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/')
def principal():
    return render_template('index.html')

@app.route('/crearOferta')
def buscar():
    return render_template('crearOferta.html')

@app.route('/historialOfertas')
def historialOfertas():
    return render_template('HistorialOfertas.html')

@app.route('/informacion')
def informacion():
    return render_template('informacion.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/enviar')
def enviar():
    flash("Enviado")
    return render_template('index.html')

@app.route('/resultados', methods=['POST'])
def resultados_busqueda():
    aniosExp = request.form['aniosExp']
    nombre = ''
    if aniosExp == '0':
        nombre = 'listaEmpleado2.html'
    elif aniosExp == '1':
        nombre = 'listaEmpleado1.html'
    elif aniosExp == '2':
        nombre = 'listaEmpleado3.html'
    else:
        nombre = 'listaEmpleado1.html'
    return render_template(nombre)


# /* Endpoint to greet and add a new visitor to database.
# * Send a POST request to localhost:8000/api/visitors with body
# * {
# *     "name": "Bob"
# * }
# */
@app.route('/api/visitors', methods=['GET'])
def get_visitor():
    if client:
        return jsonify(list(map(lambda doc: doc['name'], db)))
    else:
        print('No database')
        return jsonify([])

# /**
#  * Endpoint to get a JSON array of all the visitors in the database
#  * REST API example:
#  * <code>
#  * GET http://localhost:8000/api/visitors
#  * </code>
#  *
#  * Response:
#  * [ "Bob", "Jane" ]
#  * @return An array of all the visitor names
#  */
@app.route('/api/visitors', methods=['POST'])
def put_visitor():
    user = request.json['name']
    if client:
        data = {'name':user}
        db.create_document(data)
        return 'Hello %s! I added you to the database.' % user
    else:
        print('No database')
        return 'Hello %s!' % user

@atexit.register
def shutdown():
    if client:
        client.disconnect()

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=port, debug=False)
