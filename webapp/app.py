'''
    app.py
    Ariana Borlak, Elek Thomas-Toth

    A small Flask application
'''
import flask
import argparse
import api

app = flask.Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(api.api, url_prefix='/api')

@app.route('/')
def home():
    return flask.render_template('index.html')

@app.route('/search/<option>/<search_text>')
def results(option, search_text):
    return flask.render_template('mockup2.html', option = option, search_text = search_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A billboard songs application, including API & DB')
    parser.add_argument('host', help='the host to run on')
    parser.add_argument('port', type=int, help='the port to listen on')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
