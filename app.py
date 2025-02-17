from flask import Flask, jsonify, render_template
from exportTotalPlots import run, plots_dict, divergence_plots_dict, textData
from exportThreePlots import run2, three_plots_dict
from flask import request, jsonify
import csv

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/get_dropdown_titles')
def get_titles():
   return jsonify(sorted(list(plots_dict.keys())))


@app.route('/appendSurveyData', methods=['POST'])
def appendData():
    data = request.get_json()
    with open('responses.csv', 'a', newline='\n') as f:
        writer = csv.writer(f)
        writer.writerow([
            data['age'],
            data['gender'],
            data['comments'],
            data['netzero'],
            data['climate_impact'],
            data['renewable_energy'],
            data['policy_support'], 
            data['lifestyle_change']
        ])
    return jsonify({'status': 'success'})



@app.route('/get_total_plot/<title>')
def get_total_plot(title):
    if title not in plots_dict:
        return jsonify({'error': 'Title not found in plots_dict'}), 404
    if title not in three_plots_dict:
        return jsonify({'error': 'Title not found in three_plots_dict'}), 404
        
    return jsonify({
        'plotHtml': plots_dict[title],
        'textData': textData[title],
        'threePlotHtml': three_plots_dict[title],
    })


@app.route('/get_divergence_plot/<title>')  
def get_divergence_plot(title):           
    return divergence_plots_dict[title]


if __name__ == '__main__':

    # generates the total plots
    run()
    # print("Total plots generated:", len(plots_dict))
        
    # generates the three plots
    run2()
    # print("Three plots generated:", len(three_plots_dict))
        
    # Print some keys to compare
    # print("Plot dict keys:", list(plots_dict.keys())[:3])
    # print("Three plot dict keys:", list(three_plots_dict.keys())[:3])

    app.run(debug=True)