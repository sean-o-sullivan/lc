from flask import Flask, jsonify, render_template
from exportTotalPlots import run, plots_dict

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/get_dropdown_titles')
def get_titles():
   return jsonify(list(plots_dict.keys()))

@app.route('/get_plot/<title>')
def get_plot(title):
   return plots_dict[title]

if __name__ == '__main__':
   run()
   app.run(debug=True)