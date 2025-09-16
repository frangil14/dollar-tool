from apscheduler.schedulers.background import BackgroundScheduler
from flask_compress import Compress
import flask
import logging
import os

from app.modules.cripto import routes as routes_dollar_cripto
from app.modules.dollar_blue import routes as routes_dollar_blue
from app.modules.historic_data import routes as routes_historic_data
from app.modules.historic_data.views import write_historic_data
from app.error_handlers import register_error_handlers
from app.config import Config

ROOT_PATH = os.getcwd()
logger = logging.getLogger("dollar-tool")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(os.path.join(ROOT_PATH, 'logfile.log'))
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=write_historic_data, 
    trigger="interval", 
    seconds=Config.SCHEDULER_INTERVAL_SECONDS, 
    kwargs={'logger': logger}
)
scheduler.start()

app = flask.Flask(__name__)
app.config['COMPRESS_ALGORITHM'] = 'gzip'
app.config['COMPRESS_LEVEL'] = 9
Compress(app)

register_error_handlers(app, logger)

routes_dollar_blue.add_routes_module(app, logger)
routes_dollar_cripto.add_routes_module(app, logger)
routes_historic_data.add_routes_module(app, logger)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return "<h1>HOME</h1><p>This site is a prototype API for dollar-tool application.</p>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)