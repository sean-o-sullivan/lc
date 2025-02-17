import pandas as pd
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.colors as pc


# ______________________________________________________ #


# This python file creates the total plots and also the percentage divergence plots and table data, across all of the charts present in the dataset.
# It iterates through all of the rows in the contiguous cleaned data csv and only processes rows which are of the "Total" info across a plot.

# ______________________________________________________ #


df = pd.read_csv("cleanedGlobal.csv")


# Define a color mapping for each product
color_palette = pc.qualitative.Plotly_r 
product_color_map = {}

# Ensures each product has a consistent color across all plots.
def get_product_color(product):

    if product not in product_color_map:
        product_color_map[product] = color_palette[len(product_color_map) % len(color_palette)]
    return product_color_map[product]



def create_3_plots(total_data, unit, product, flow, category, line_names):
    """
    Plots three charts of the projected scenarios with shared years and units.
    """
    # Check if we only have data for the first scenario
    is_incomplete = len(total_data[1][0]) < 4 and len(total_data[2][0]) <4

    is_empty = all(not any(sublist) for group in total_data for sublist in group)
    if is_empty:
        is_incomplete=True
        
    # we have to append 2 nans to the beginning of the announced pledges and net zero projections as they dont have data from 2010 and 2022    
    for i in [1, 2]:           # For Announced Pledges and Net Zero scenarios
        for j in [0, 1]:       # For both product names and values
            original_list = total_data[i][j]
            new_list = []
            # Process the list in chunks of 5
            for k in range(0, len(original_list), 5):
                group = original_list[k:k+5]
                new_list.extend([None, None] + group)
            total_data[i][j] = new_list

    # This is constant throughout the dataset
    years = [2010, 2022, 2023, 2030, 2035, 2040, 2050]

    # If we have incomplete data, create simplified plot
    if is_incomplete:
        # Create subplot figure
        fig = make_subplots(rows=3, cols=1, 
                        shared_xaxes=True,
                        subplot_titles=(f"Stated Policies", 
                                        "Announced Pledges",
                                        "Net Zero Emissions 2050"),
                        vertical_spacing=0.12
        )

        for i in [1, 2, 3]:
            fig.add_annotation(
                x=2,
                y=1.5,
                xref=f"x{i}",
                yref=f"y{i}",
                text="No Relevant Data (N/A)",
                showarrow=False,
                font=dict(size=30, color='gray'),
                textangle=0,
                opacity=0.5
            )

        # Update 
        fig.update_layout(
        height=575,
        width=725,
        showlegend=True,
        font_color="black",
        title_font_color="black",
        legend_title_font_color="black",
        margin=dict(l=20, r=20, t=40, b=20, pad=0),
        plot_bgcolor='#f8f9fa',   
        paper_bgcolor='white'     
        )

        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        fig.update_yaxes(title_text=unit, row=1, col=1)
        fig.update_yaxes(title_text=unit, row=2, col=1)
        fig.update_yaxes(title_text=unit, row=3, col=1)

        clean_category = category.split(',')[0].strip()
        title = f"{flow.strip()} - {clean_category}"
        three_plots_dict[title] = fig.to_html()

    else:

        # Create dataframes for the 3 scenarios
        stated_df = pd.DataFrame()  # index 0 
        announced_df = pd.DataFrame()
        zero_df = pd.DataFrame()   

        dataframes = {'stated': pd.DataFrame(), 'announced': pd.DataFrame(), 'zero': pd.DataFrame()}
        c = 0
        for scenario_key in dataframes:
            products = total_data[c][0]
            values = total_data[c][1]
            # For stated, products come in groups of 7; for announced and net zero, they come in groups of 5 (with 2 Nones inserted)
            step = 7 if c == 0 else 7  # They all should be 7 now
            for j in range(0, len(products), 7):
                group_products = products[j:j+7]

                # Must choose the first non-None product name from the group:
                product_name = next((p for p in group_products if p is not None), None)

                prod_values = values[j:j+7]
                temp_df = pd.DataFrame({
                    'Year': years,
                    'Value': prod_values,
                    'Product': [product_name] * len(years),
                    'Category': [line_names[0]] * len(years)
                })
                dataframes[scenario_key] = pd.concat([dataframes[scenario_key], temp_df], ignore_index=True)
            c += 1

        stated_df = dataframes['stated']
        announced_df = dataframes['announced']
        zero_df = dataframes['zero']

        print(stated_df)
        print(announced_df)
        print(zero_df)
        
        # make ze subplot figure
        fig = make_subplots(rows=3, cols=1, 
                            shared_xaxes=True,
                            subplot_titles=(f"Stated Policies", 
                                            "Announced Pledges",
                                            "Net Zero Emissions 2050"),
                            vertical_spacing=0.125
            )

        # Add traces for plots
        for i, (df_name, df) in enumerate(dataframes.items(), 1):
            for cat in df['Category'].unique():
                cat_df = df[df['Category'] == cat]
                for prod in cat_df['Product'].unique(): 
                    prod_df = cat_df[cat_df['Product'] == prod]
                    fig.add_trace(
                        go.Scatter(
                            x=prod_df['Year'], 
                            y=prod_df['Value'], 
                            name=f"{prod}", 
                            mode='lines+markers',
                            line=dict(color=get_product_color(prod)),  
                            showlegend=(i == 1),  # only show legend for the first subplot

                            hovertemplate=(
                        "<b>%{text}</b><br>" 
                        "Year: %{x}<br>"
                        "Value: %{y:,.2f} " + unit + "<br>"  
                        "<extra></extra>"  
                            ),
                    text=[prod] * len(prod_df)  
                        ),
                        row=i, col=1
                    )

    # Update 
    fig.update_layout(
    height=575, 
    width=725,
    showlegend=True,
    font_color="black",
    title_font_color="black",
    legend_title_font_color="black",
    margin=dict(l=20, r=20, t=40, b=20, pad=0),
    plot_bgcolor='#f8f9fa',   
    paper_bgcolor='white'     
    )

    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    fig.update_yaxes(title_text=unit, row=1, col=1)
    fig.update_yaxes(title_text=unit, row=2, col=1)
    fig.update_yaxes(title_text=unit, row=3, col=1)

    clean_category = category.split(',')[0].strip()
    title = f"{flow.strip()} - {clean_category}"
    three_plots_dict[title] = fig.to_html()



def save_to_sublist(total_data,product,value,scenario):

    # Save the specific recorded value to its respective sublist
    if product != 'Total':
        
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
    else:
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