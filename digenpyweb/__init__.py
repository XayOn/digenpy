from flask import Flask, render_template, abort, Response, request, redirect, flash, url_for
import Digenpy_, json
from Digenpy_ import *
app = Flask(__name__)
app.config['DEBUG'] = True
app.secret_key = "SECRETKEY"
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')



def do_digenpy(country, company, mac, essid):
    error = False
    try:
        result = getattr(getattr(Digenpy_, country),
            company)(['', mac, essid]).dictionary
    except Exception, err:
        result = err
        error = True

    if not result:
        abort(404)

    return (result, error)

@app.route('/get/<country>/<company>/<mac>/<essid>')
def ajax_file(country, company, mac, essid):
    result, error = do_digenpy(country, company, mac, essid)
    if error:
        flash(result)
        return redirect(url_for('index'))
    if request.environ['REQUEST_METHOD'] == "POST":
        return json.dumps(result)
    return '\n'.join(result)

@app.route('/get_file/<country>/<company>/<mac>/<essid>')
def download_file(country, company, mac, essid):
    result, error = do_digenpy(country, company, mac, essid)
    if error:
        flash(result)
        return redirect(url_for('index'))
    return Response(result, mimetype='application/x-digenpy-dic' )

def server():
    """ Main server, will allow us to make it wsgi'able """
    app.run(host='0.0.0.0', port=8022)

if __name__ == "__main__":
    server()
