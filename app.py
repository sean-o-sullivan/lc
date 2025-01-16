from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/plotly_chart')
def plotly_chart():
    return render_template_string(html_str)

onChange for dropdown in the html page


form post back to a webserver.


if __name__ == '__main__':
    app.run(debug=True)
