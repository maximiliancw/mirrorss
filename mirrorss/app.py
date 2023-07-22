import os
from urllib.parse import unquote
from flask import Flask, Response, render_template, request

from mirrorss.model import Mirror


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fpiouafhreu9ghqp4')


@app.route('/', methods=['GET'])
def index():
    query = {k: unquote(v) for k, v in request.args.items()}
    return render_template('pages/index.html', q=query)

@app.route('/about', methods=['GET'])
def about():
    return render_template('pages/about.html')


@app.route('/feed', methods=['GET'])
def feed():
    if "title" not in request.args:
        e = "Missing required parameter 'title'"
        return render_template("pages/error.html", error=e), 400
    
    if "sources" not in request.args:
        e = "Missing required parameter 'sources'"
        return render_template("pages/error.html", error=e), 400

    params = dict()
    for key, value in request.args.items():
        if key == "limit":
            params[key] = int(value)
            continue
        if any([key == k for k in ["sources", "keywords"]]):
            params[key] = value.split("\n")
            continue
        params[key] = value

    try:
        mirror = Mirror(**params)
        xml_format = request.args.get("format", "rss")
        html = render_template(f"data/{xml_format}.xml", feed=mirror)
        return Response(html, status=200, mimetype="application/xml")
    except Exception as e:
        return render_template("pages/error.html", error=str(e)), 400
