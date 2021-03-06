"""
Routes and views for the flask application.
"""

from flask import render_template, request, session
from FlaskWebProject1 import app, babel
from flask_babel import gettext
import json, urllib2

# Babel config
SUPPORTED_LANGUAGES = {'id': 'Bahasa', 'en': 'English'}

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(SUPPORTED_LANGUAGES.keys())

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html')

@app.route('/results/<id>')
def result(id):
    """Renders the result page."""
    try:
        url = "http://hprimary.lelah.ga/result"
        data = json.dumps({'id':id})
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        result = json.loads(response)
        fact_p = result["scores"][1]
        hoax_p = result["scores"][2]
        conclude = result["conclusion"]
        unkn_p = result["scores"][3]
        totalp = fact_p + hoax_p + unkn_p
        conclusion = "Kami tidak dapat menyimpulkan. "
        box = "alert-warning"
        if conclude == 'hoax':
            conclusion = str(round(100*(hoax_p/totalp),2)) + "% mengatakan "
            box = "alert-danger"
        elif conclude == 'fact' and fact_p!=0:
            conclusion = str(round(100*(fact_p/totalp),2))  + "% mengatakan "
            box = "alert-info"
        return render_template('result.html', result=result, conclusion=conclusion, box=box)
    except Exception as e:
        print(e)

@app.route('/feedback/result', methods=['POST'])
def feedbackResult():
    if request.method == 'POST':
        try:
            data = request.json
            data["ip"] = _get_user_ip(request)
            data["browser"] = request.headers.get('User-Agent')
            url = "http://hprimary.lelah.ga/feedback/result"
            req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
            return response
        except Exception as e:
            print(e)

@app.route('/feedback/reference', methods=['POST'])
def feedbackReference():
    if request.method == 'POST':
        try:
            data = request.json
            data["ip"] = _get_user_ip(request)
            data["browser"] = request.headers.get('User-Agent')
            url = "http://hprimary.lelah.ga/feedback/reference"
            req = urllib2.Request(url, json.dumps(data), {'Content-Type': 'application/json'})
            f = urllib2.urlopen(req)
            response = f.read()
            f.close()
            return response
        except Exception as e:
            print(e)

def _get_user_ip(request):
    ip = request.headers.get('X-Forwarded-For')
    if ip is None:
        ip = request.remote_addr
    
    return ip

@app.errorhandler(404)
def page_not_found(error):
    app.logger.error('Page not found: %s', (request.path, error))
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))