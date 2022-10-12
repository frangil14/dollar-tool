from apscheduler.schedulers.background import BackgroundScheduler
import flask
from flask_compress import Compress
from werkzeug.exceptions import HTTPException
import simplejson
import logging
import os

from app.modules.dollar_blue import routes as routes_dollar_blue
from app.modules.cripto import routes as routes_dollar_cripto

# -------------------------- Initialize logger file ------------------------------
ROOT_PATH = os.getcwd()
logger = logging.getLogger("dollar-tool")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(os.path.join(ROOT_PATH, 'logfile.log'))

formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# -------------------------- Initialize Schedule for Cleaning ------------------------------
scheduler = BackgroundScheduler()
#scheduler.add_job(func=clean_parquets, trigger="interval", seconds=86400)
scheduler.start()


app = flask.Flask(__name__)
app.config['COMPRESS_ALGORITHM'] = 'gzip'
app.config['COMPRESS_LEVEL'] = 9
Compress(app)

# ---------------------------- Routes --------------------------------------------
routes_dollar_blue.add_routes_module(app, logger)
routes_dollar_cripto.add_routes_module(app, logger)



# ---------------------------- Start Parse Exception --------------------------------------------
@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    if isinstance(e, HTTPException):
        response = e.get_response()
    else:
        response = HTTPException(e)
        e.code = 500
        e.name = 'Internal Server Error'
        e.description = str(e)

    response.data = simplejson.dumps({
        "code": e.code or 500,
        "name": e.name,
        "description": e.description,
    })

    output = flask.Response(
        response.data, status=e.code or 500, mimetype='application/json')
    return output

# ---------------------------- END Parse Exception --------------------------------------------


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return f"<h1>HOME</h1><p>This site is a prototype API for dollar-tool application.</p>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)