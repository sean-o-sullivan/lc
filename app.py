from flask import Flask, jsonify, render_template
from exportTotalPlots import run, plots_dict, divergence_plots_dict, textData
from exportThreePlots import run2, three_plots_dict

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/get_dropdown_titles')
def get_titles():
   return jsonify(sorted(list(plots_dict.keys())))

@app.route('/get_total_plot/<title>')
def get_total_plot(title):
    return jsonify({
        'plotHtml': plots_dict[title],
        'textData': textData[title]
    })


@app.route('/get_3_plots/<title>')
def get_total_plot(title):
    return jsonify({
        'plotHtml': three_plots_dict[title],
    })


@app.route('/get_divergence_plot/<title>')  
def get_divergence_plot(title):           
    return divergence_plots_dict[title]


if __name__ == '__main__':
   run()
   run2()
   app.run(debug=True)