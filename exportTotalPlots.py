import pandas as pd
import plotly.express as px
import pandas as pd


# This python file creates the total plots and also the percentage divergence plots and table data, across all of the charts present in the dataset.
# It iterates through all of the rows in the contiguous cleaned data csv and only processes rows which are of the "Total" info across a plot.

# GRAPH THE % DIVERGENCE OVER TIME
# GRAPH THE % DIVERGENCE OVER TIME
# GRAPH THE % DIVERGENCE OVER TIME

# and export a table comparison and other statistics!!

# make **recommendations** based 

# ______________________________________________________ #

df = pd.read_csv("cleanedGlobal.csv")


def create_total_plot(total_data, unit, flow, product, line_names):
    """
    Plots three lines on the same chart with shared years and units.

    Parameters:
    - years: List of years (shared by all lines)
    - values_list: List of three value lists (one per line)
    - unit: Y-axis unit (string, shared by all lines)
    - flow: Flow category (string)
    - product: Product category (string)
    - line_names: List of three names for the legend
    """
    
    # Create a combined DataFrame
    df = pd.DataFrame()
    years=total_data[3]

    for name, values in zip(line_names, total_data):
        temp_df = pd.DataFrame({
            'Year': years,
            'Value': values,
            'Category': name 
        })
        df = pd.concat([df, temp_df], ignore_index=True)

    # Generate plot
    title = f"{flow} - {product}"
    fig = px.line(
        df,
        x='Year',
        y='Value',
        color='Category',
        title=title,
        markers=True,
        labels={'Value': unit}
    )

    # Save plot
    # fig.write_html(f"Total_plot-{title}.html")

    
totaling=False
previous_flow=''
previous_flow = df.loc[0,'FLOW']

for index, row in df.iterrows():    

    # Label columns
    flow = df.loc[index, 'FLOW'] 
    print(flow)
    product = df.loc[index, 'PRODUCT']
    unit = df.loc[index, 'UNIT'] 
    scenario = df.loc[index, 'SCENARIO'] 

    # Actual data
    year = df.loc[index, 'YEAR'] 
    value = df.loc[index, 'VALUE'] 

    # Dynamically initialise the totalData list of lists
    total_data = []

    # Outer loop to create 4 sublists -- This is for the three scenarios and also the year column.
    for i in range(4):
        total_data.append([] * 1)


    # print(f'the pre is {previous_flow}')
    # print(f'the flow is {flow}'
    
    # Checks that we are in the same plot, prevents mixing of non standard data
    if (previous_flow.lower() == flow.lower()):
            # print('flow is equal to pre')

            # Check if in the total section
            if product == 'Total':

                print(f'>> total detected <<, for chart: {flow}')

                totaling = True
                TotalPlotname = f'{flow} - Total'

                # Save the year to the year column
                total_data[3].append(year)

                # Save the specific recorded value to its respective sublist
                if scenario == 'Stated Policies Scenario':
                    total_data[0].append(value)

                elif scenario == 'Announced Pledges Scenario':
                    total_data[1].append(value)

                elif scenario == 'Net Zero Emissions by 2050 Scenario':
                    total_data[2].append(value)

            # Save the data collected while totalling and make a plot for this 
            elif totaling:
                    print('now saving because we are no longer totaling!')
                    create_total_plot(
                        total_data=total_data,
                        unit=unit,
                        flow=flow,
                        product=product,
                        line_names=['Stated Policies Scenario','Announced Pledges Scenario','Net Zero Emissions by 2050 Scenario']
                    )
            
                    totaling=False
    else:
        print(f'flow has changed..... from {previous_flow} to {flow}')
        previous_flow=flow
            