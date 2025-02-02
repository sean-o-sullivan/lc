import pandas as pd
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# ______________________________________________________ #


# This python file creates the total plots and also the percentage divergence plots and table data, across all of the charts present in the dataset.
# It iterates through all of the rows in the contiguous cleaned data csv and only processes rows which are of the "Total" info across a plot.

# GRAPH THE % DIVERGENCE OVER TIME
# GRAPH THE % DIVERGENCE OVER TIME
# GRAPH THE % DIVERGENCE OVER TIME

# and export a table comparison and other statistics!!

# make **recommendations** based 

# ______________________________________________________ #


df = pd.read_csv("cleanedGlobal.csv")


def create_total_plot(total_data, unit, flow, category, line_names):
    """
    Plots three lines on the same chart with shared years and units.

    Parameters:
    - need to update
    """

    # print('create_total_plot called!')

    # Create a combined DataFrame
    total_df = pd.DataFrame()
    divergence_df = pd.DataFrame()  # For total plot


    # we have to append 2 nans to the beginning of the announced pledges and net zero projections as they dont have data from 2010 and 2022    
    for i in [1, 2]:
        total_data[i] = [None, None] + total_data[i]

    # print(f'We are in Flow: {flow}, Here total_data is! {total_data}')

    # for sub in total_data:
    #     print(f'The length of {sub} is {len(sub)}')


    # This is constant throughout the dataset
    years = [2010, 2022, 2023, 2030, 2035, 2040, 2050]

    # print(f'the years are {years}')
    # print(len(years))

    for name, values in zip(line_names, total_data):
        temp_df = pd.DataFrame({
            'Year': years,
            'Value': values,
            'Category': name 
        })

        total_df = pd.concat([total_df, temp_df], ignore_index=True)
        

    c=0
    # % Divergence between what we are actually predicted to do and what we need to do
    for i in range(len(years)):

        if c > 2:
            try:
                divergence_temp_df = pd.DataFrame({
                    'Year': [years[i]], 
                    'Value': [(total_data[0][i]/total_data[2][i])],  
                    'Category': ['Percentage Difference']  
                })

            except ZeroDivisionError:
                divergence_temp_df = pd.DataFrame({
                    'Year': years,
                    'Value': None,
                    'Category': name 
                })
        else: 
            divergence_temp_df = pd.DataFrame({
                'Year': years,
                'Value': None,
                'Category': 'Percentage Difference' 
            })
        c+=1
        divergence_df = pd.concat([divergence_df, divergence_temp_df], ignore_index=True)

    # Create subplot figure
    fig = make_subplots(rows=2, cols=1, 
                    shared_xaxes=True,
                    subplot_titles=(f"{flow} - {category}", 
                                    "Percentage Divergence between Stated and Net Zero"))

    # Add traces for total plot
    for name in total_df['Category'].unique():
        plot_df = total_df[total_df['Category'] == name]
        fig.add_trace(
            go.Scatter(x=plot_df['Year'], y=plot_df['Value'], name=name, mode='lines+markers'),
            row=1, col=1
        )

    # Add trace for divergence plot
    fig.add_trace(
    go.Scatter(x=divergence_df['Year'], y=divergence_df['Value'], 
                name='Percentage Divergence', mode='lines+markers'),
    row=2, col=1
    )

    # Update layout
    fig.update_layout(
    height=500,
    width=700,
    showlegend=True,
    font_color="black",
    title_font_color="black",
    legend_title_font_color="black"
    )

    # Update y-axes labels
    fig.update_yaxes(title_text=unit, row=1, col=1)
    fig.update_yaxes(title_text="% Diff", row=2, col=1)
    title = f"{flow} - {category}"
    plots_dict[title] = fig.to_html()




def save_to_sublist(total_data,value,scenario):

    # Save the specific recorded value to its respective sublist
    if scenario == 'Stated Policies Scenario':
        total_data[0].append(value)

    elif scenario == 'Announced Pledges Scenario':
        total_data[1].append(value)

    elif scenario == 'Net Zero Emissions by 2050 Scenario':
        total_data[2].append(value)

    return total_data

# Stores plot titles & html bundles, this has to be defined globally
plots_dict = {}
divergence_plots_dict = {}

def run():
        
    totaling=False
    previous_flow=''
    previous_category=''
    previous_flow = df.loc[0,'FLOW']

    # Dynamically initialise the totalData list of lists
    total_data = []

    # Outer loop to create 3 sublists -- This is for the three scenarios' total data.
    for i in range(3):
        total_data.append([] * 1)


    for index, row in df.iterrows():    

        # Label columns
        flow = df.loc[index, 'FLOW'] 
        product = df.loc[index, 'PRODUCT']
        unit = df.loc[index, 'UNIT'] 
        scenario = df.loc[index, 'SCENARIO'] 
        category = df.loc[index, 'CATEGORY'] 

        # Actual data
        year = df.loc[index, 'YEAR'] 
        value = df.loc[index, 'VALUE'] 
                    

        if (previous_flow.lower() == flow.lower()) and (previous_category.lower() == category.lower()):

            # Check if in the total section
            if product == 'Total':

                totaling = True
                TotalPlotname = f'{flow} - Total'
                    
                # Save the specific recorded value to its respective sublist
                total_data = save_to_sublist(total_data,value,scenario)

                # print(f'''the value we just tried to append was {value}
                #         appending to {scenario}, heres it: {total_data}'''
                #     )
                
            # Save the data collected while totalling and make a plot for this 
            elif totaling:
                    # print('now saving because we are no longer totaling!')
                    create_total_plot(
                        total_data=total_data,
                        unit=unit,
                        flow=flow,
                        category=category,
                        line_names=['Stated Policies Scenario','Announced Pledges Scenario','Net Zero Emissions by 2050 Scenario']
                    )
                    totaling=False
        else:
            totaling=False

            # Re-initialise the totalData list of lists
            total_data = []

            # Outer loop to create 3 sublists -- This is for the three scenarios.
            for i in range(3):
                total_data.append([] * 1)

            # This is for when the flow changes and we encounter the first total value of that next flow
            total_data = save_to_sublist(total_data,value,scenario)

        previous_flow=flow
        previous_category=category
