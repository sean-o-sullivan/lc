from flask import Flask, jsonify
import exportTotalPlots

app = Flask(__name__)

@app.route('/get_dropdown_titles')
def get_titles():
   return jsonify(list(exportTotalPlots.plots_dict.keys()))


@app.route('/get_plot/<title>')
def get_plot(title):
   return exportTotalPlots.plots_dict[title]

if __name__ == '__main__':
   exportTotalPlots.run()
   app.run(debug=True)

