from flask import Flask, render_template, abort, Response
import Digenpy_, json
from Digenpy_ import *
app = Flask(__name__)
app.config['DEBUG'] = True
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/get/<country>/<company>/<mac>/<essid>')
def do_digenpy(country, company, mac, essid):
    result = getattr(getattr(Digenpy_, country), company)(['', 
        mac, essid]).dictionary
    if not result:
        abort(404)
    return json.dumps(result)

@app.route('/get_file/<country>/<company>/<mac>/<essid>')
def download_file(country, company, mac, essid):
    return Response(do_digenpy(country, company, mac, essid), 
        mimetype='application/x-digenpy-dic' )

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=22)

if __name__ == "__main__":
    server()
