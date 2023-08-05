# -*- coding: UTF-8 -*-
import json
import os
from proxy import crawl_product
from flask import request
from flask import Flask
from flask import make_response
from flask_cors import CORS
from modules.tools.translate import translator
from modules.repository import repositories
from offcrawler.downloader import get_today_covers

app = Flask(__name__)
CORS(app)


@app.route('/proxy/product', methods=["POST", "GET"])
def product():
    catalog = {
        "source_type": 1,
        "catalog_id": 7909,
        "language_id": 1,
        "source_id": "12587559",
        "url": "/cn/shopping/women/dolce-gabbana-leopard-trim-cropped-trousers-item-12587559.aspx?storeid=9306&from=listing",
        "thumbnail": "https://cdn-images.farfetch-contents.com/12/58/75/59/12587559_12078291_255.jpg",
        "product_name": "leopard trim cropped trousers",
        "catalog_status": 0
    }

    if request.method == 'POST':
        response = make_response(json.dumps(crawl_product(request.get_json())))
    else:
        response = make_response(json.dumps(crawl_product(catalog)))

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return response


@app.route('/translate', methods=["POST", "GET"])
def translate():
    if request.method == 'POST':
        string = translator.en_to_zh(request.get_json()["text"])
    else:
        string = translator.en_to_zh(
            "Jet Set Travel saffiano leather tote bag<br>Model in saffiano print calf leather<br />Central zip closure<br />2 flat handles with buckle<br />2 internal compartments and a central partition with zip<br />1 inside pocket with zip<br />3 inside flat pockets<br />1 pocket for mobilephone<br />1 removable logoed charm<br />Gold-tone hardware<br />Fabric lining with allover logo<br />Length: 38 cm<br />Height: 28 cm<br />Depth: 15 cm<br>Posizione del logo: Metallic logo on front<br>100%, Leather<br>Confezione: Acetate<br>Colore: black<br>Product Model: Jet Set Travel")
    response = make_response(string)
    print(string)
    return response


@app.route('/covers')
def covers():
    today_covers = get_today_covers()
    data = {
        "covers": today_covers,
        "length": len(today_covers),
        "status": 0,
        "message": "success"
    }
    return make_response(json.dumps(data))


app.config['SECRET_KEY'] = 'off'
if __name__ == '__main__':
    repositories.connect()
    app.run(debug=False, port=9604, host="0.0.0.0")
