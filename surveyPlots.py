from plotly.subplots import make_subplots
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd


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
    survey_plots_dict={}

    Barfig = make_subplots(subplot_titles=["Age", "Gender"],rows=1, cols=2)
    
    Piefig = make_subplots(rows=2, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}],[{"type": "pie"}, {"type": "pie"}]],
            subplot_titles=["Do you think we are going to <br>reach Net-Zero by 2050<br>",
                            "How concerned are you about <br>climate change's impact on your life?<br>",
                            "Would you support stricter government <br>policies to reduce carbon emissions?<br>",
                            "Are you willing to make major lifestyle <br>changes to reduce your carbon footprint?<br>"]
    )

    pr=1
    pc=1
    br=1

    for nam in df.columns:
        if nam != "comments":

            if (df[f"{nam}"][1] in ["no", "yes", "very", "somewhat", "not"]):

                print('making pie')
                value_counts = df[f'{nam}'].value_counts()
                print(f'{pr},{pc}')
                Piefig.add_trace(go.Pie(values=value_counts.values), row=pr, col=pc)
                if pc % 2 == 0:
                    pr+=1
                pc+=1
                if pc > 2:
                    pc=1
            
            else:
                if nam.lower() == 'age':
                    Barfig.add_trace(
                        go.Histogram(
                            x=df[nam],
                        ),
                        row=1, col=br
                    )
                    br+=1
                elif nam.lower() == 'gender':
                    
                    counts = df[nam].value_counts()
                    color_map = {
                        'male': 'cyan',
                        'female': 'pink',
                        'other': 'gray'
                    }

                    color_list = [color_map.get(str(cat).lower(), 'gray') for cat in counts.index]
                    Barfig.add_trace(
                        go.Bar(
                            x=counts.index,
                            y=counts.values,
                            marker=dict(color=color_list),
                            
                        ),
                        row=1, col=br
                    )
                    br+=1
        else:
            text=""
            for item in df[f"{nam}"]:
                text = text+item
             
            wordcloud = WordCloud(width=750, height=500, background_color='white').generate(text)
            plt.figure(figsize=(7.5, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")  # Remove axes
            plt.show()


    # Update layout
    Barfig.update_layout(
        height=500,
        width=750,
        showlegend=False,
        font_color="black",
        title_font_color="black",
        legend_title_font_color="black",
        margin=dict(l=0, r=0, t=80, b=0, pad=0),  # increased top margin
        plot_bgcolor='#f8f9fa',   
        paper_bgcolor='white'    
    )

    Piefig.update_layout(
        height=500,
        width=750,
        showlegend=False,
        font_color="black",
        title_font_color="black",
        legend_title_font_color="black",
        margin=dict(l=0, r=0, t=80, b=0, pad=0),  # increased top margin
        plot_bgcolor='#f8f9fa',   
        paper_bgcolor='white'    
    )
    Barfig.show()
    Piefig.show()

    survey_plots_dict["bar"] = Barfig.to_html()
    survey_plots_dict["pie"] = Piefig.to_html()
    survey_plots_dict["cloud"] = wordcloud

    return survey_plots_dict