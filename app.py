# app.py

from flask import Flask, render_template, request, redirect, url_for, send_file, make_response
from stock_analyse import stock_info, perf_graph
import re



app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def index():
    ipo_dict ={}

    if request.method == 'POST':
        text_input = request.form['ticker']

        if text_input != '':
            # extracted_text = list((text_input.split(',')))
            list_stocks = list(text_input.split(','))
            list_stocks = [x.upper() for x in list_stocks]
            list_without_spaces = [re.sub(r'\s+', '', item) for item in list_stocks]
            # print('hey list of stocks is', list_without_spaces)
            ipo_dict = stock_info(list_without_spaces)

            # print(extracted_text)
            # print(ipo_dict)

    return render_template('index.html', ipo_dict=ipo_dict)


@app.route("/ipo_detail/<name>", methods =['GET','POST'])
def ipo_stock_details(name):
    graph1_url = perf_graph(name)

    return render_template("ipo_detail.html", name=name, graph1=graph1_url)


if __name__ == '__main__':
    app.run(debug=True)
