import pandas as pd
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go


# ______________________________________________________ #


# This python file creates the total plots and also the percentage divergence plots and table data, across all of the charts present in the dataset.
# It iterates through all of the rows in the contiguous cleaned data csv and only processes rows which are of the "Total" info across a plot.

# ______________________________________________________ #


df = pd.read_csv("cleanedGlobal.csv")

def create_3_plots(total_data, unit, product, flow, category, line_names):
    """
    Plots three charts of the projected scenarios with shared years and units.

    Parameters:
    - need to update
    """

    # Create dataframes for the 3 scenarios
    stated_df = pd.DataFrame()  # index 0 
    announced_df = pd.DataFrame()
    zero_df = pd.DataFrame()

    is_empty = all(not any(sublist) for group in total_data for sublist in group)
    if is_empty:
        return
        
    # we have to append 2 nans to the beginning of the announced pledges and net zero projections as they dont have data from 2010 and 2022    
    for i in [1, 2]:
        for j in [0,1]:
            total_data[i][j] = [None, None] + total_data[i][j]

    # This is constant throughout the dataset
    years = [2010, 2022, 2023, 2030, 2035, 2040, 2050]

    c = 0
    dfs = {'stated_df': stated_df, 'announced_df': announced_df, 'zero_df': zero_df}
    for df_key in dfs.keys():
        products = total_data[c][0]  # Get list of products for this scenario
        values = total_data[c][1]    # Get list of values for this scenario
        
        for prod, val in zip(products, values):
            temp_df = pd.DataFrame({
                'Year': years,
                'Value': val,
                'Product': prod,
                'Category': line_names[c]  # Use the scenario name
            })
            dfs[df_key] = pd.concat([dfs[df_key], temp_df], ignore_index=True)
        c += 1

    # Assign values back to original variables
    stated_df, announced_df, zero_df = dfs['stated_df'], dfs['announced_df'], dfs['zero_df']

    # Create subplot figure
    fig = make_subplots(rows=3, cols=1, 
                    shared_xaxes=True,
                    subplot_titles=(f"Stated Policies", 
                                    "Announced Pledges",
                                    "Net Zero Emissions 2050"),
                    vertical_spacing=0.125
    )



    # Add traces for plots
    for i, (df_name, df) in enumerate(dfs.items(), 1):  # enumerate starting from 1
        for cat in df['Category'].unique():
            cat_df = df[df['Category'] == cat]

            for prod in cat_df['Product'].unique(): 
                prod_df = cat_df[cat_df['Product'] == prod]

                fig.add_trace(
                    go.Scatter(
                        x=prod_df['Year'], 
                        y=prod_df['Value'], 
                        name=f"{prod}", 
                        mode='lines+markers'
                    ),
                    row=i, col=1  # Use the enumerated index to place traces in correct subplot
                )
                
    # Update layout
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20, pad=0),
        height=600,  # Increase height
        width=700,
        showlegend=True,
        font_color="black",
        title_font_color="black",
        legend_title_font_color="black"
    )

    # Add gridlines
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Update y-axes labels
    fig.update_yaxes(title_text=unit, row=1, col=1)
    fig.update_yaxes(title_text=unit, row=2, col=1)
    fig.update_yaxes(title_text=unit, row=3, col=1)

    title = f"{flow} - {category}"
    three_plots_dict[title] = fig.to_html()


# This includes both the value recorded for each scenario and the product also, allowing us to make the multiple streams
def save_to_sublist(total_data,product,value,scenario):

    # Save the specific recorded value to its respective sublist
    if scenario == 'Stated Policies Scenario':
        total_data[0][0].append(product)
        total_data[0][1].append(value)

    elif scenario == 'Announced Pledges Scenario':
        total_data[1][0].append(product)
        total_data[1][1].append(value)

    elif scenario == 'Net Zero Emissions by 2050 Scenario':
        total_data[2][0].append(product)
        total_data[2][1].append(value)

    return total_data


# Stores plot titles & html bundles, this has to be defined globally
three_plots_dict = {}
divergence_three_plots_dict = {}


def run2():
        
    previous_flow=''
    previous_category=''
    previous_flow = df.loc[0,'FLOW']

    # Dynamically initialise the totalData list of lists
    total_data = []

    # Outer loop to create 3 sublists -- This is for the three scenarios' individual data.
    for _ in range(3):
        total_data.append([[],[]])   

    for index, _ in df.iterrows():    

        # Label columns
        flow = df.loc[index, 'FLOW'] 
        product = df.loc[index, 'PRODUCT']
        unit = df.loc[index, 'UNIT'] 
        scenario = df.loc[index, 'SCENARIO'] 
        category = df.loc[index, 'CATEGORY'] 

        # Actual data
        value = df.loc[index, 'VALUE'] 
                    

        if (previous_flow.lower() == flow.lower()) and (previous_category.lower() == category.lower()):

            # Check if in the total section
            if product != 'Total':

                # Save the specific recorded value to its respective sublist
                total_data = save_to_sublist(total_data,product,value,scenario)

        else:
            # Save the data collected 
            create_3_plots(
                total_data=total_data,
                unit=unit,
                product=product,
                flow=flow,
                category=category,
                line_names=['Stated Policies Scenario','Announced Pledges Scenario','Net Zero Emissions by 2050 Scenario']
            )

            # Dynamically initialise the totalData list of lists
            total_data = []

            # Outer loop to create 3 sublists -- This is for the three scenarios' individual data.
            for _ in range(3):
                total_data.append([[],[]])   

            # This is for when the flow changes and we encounter the first total value of that next flow
            total_data = save_to_sublist(total_data,product,value,scenario)

        previous_flow=flow
        previous_category=category

run2()