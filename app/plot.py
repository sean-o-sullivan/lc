import plotly.express as px
import pandas as pd

def create_plots():
   df = pd.DataFrame({
       'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
       'Sales': [100, 120, 90, 140]
   })

   fig = px.line(df, x='Month', y='Sales', title='Monthly Sales', markers=True)
   fig.write_html("static/plot.html")

if __name__ == "__main__":
   create_plots()