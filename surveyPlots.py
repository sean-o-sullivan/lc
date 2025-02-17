import pandas as pd
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import csv


# ______________________________________________________ #


# This python file creates the total plots and also the percentage divergence plots and table data, across all of the charts present in the dataset.
# It iterates through all of the rows in the contiguous cleaned data csv and only processes rows which are of the "Total" info across a plot.

# Graphing the % divergence over time

# need to make table !!!!

# ______________________________________________________ #


df = pd.read_csv("cleanedGlobal.csv")


def create_survey_plot():
    """
    Plots the current results from the users survey

    Parameters:
    - need to update
    """

    df = pd.read_csv('responses.csv')

    plots = {}


    Barfig = make_subplots(rows=1, cols=2)
    Piefig = make_subplots(
    rows=3, cols=2)

    pr=1
    pc=1
    br=1

    for nam in df.columns:
        print('Ya1')
        if (df[f"{nam}"][1] == "no") or (df[f"{nam}"][1] == "yes"):
            print('wehaveapie')

            value_counts = df[f'{nam}'].value_counts()
            Piefig.add_trace(go.Pie(values=value_counts.values, name=f'{nam} Pie'), row=pr,col=pc)

            cr+=1
            if cr % 2 == 0:
                pr+=1
             
        else:
            print('wehaveaBar')

            value_counts = df[nam].value_counts()
            
            Barfig.add_trace(go.Bar(x=value_counts.index, y=value_counts.values, name=f'{nam} Distribution'),row=br,col=br)
            br+=1


    # Update layout
    Barfig.update_layout(
    height=1000,
    width=2000,
    showlegend=False,
    font_color="black",
    title_font_color="black",
    legend_title_font_color="black",
    margin=dict(l=20, r=20, t=40, b=20, pad=0),
    plot_bgcolor='#f8f9fa',   
    paper_bgcolor='white'    
    )
    Piefig.update_layout(
    height=1000,
    width=2000,
    showlegend=False,
    font_color="black",
    title_font_color="black",
    legend_title_font_color="black",
    margin=dict(l=20, r=20, t=40, b=20, pad=0),
    plot_bgcolor='#f8f9fa',   
    paper_bgcolor='white'    
    )
 
    Barfig.show()
    Piefig.show()
    # title = f"{flow.strip()} - {clean_category}"
    # plots_dict[title] = fig.to_html()
    # textData[title] = fillerDescription


create_survey_plot()
