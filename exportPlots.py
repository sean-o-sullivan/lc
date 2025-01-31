
# This file defines the functions which will load the regional and world data, proceess the contiguous csvs and pass the lists to the generate plots python file which ultimately passes the html graph to the app.py file

#the main function will be called when the app.py starts, and then this file will return a lookup table of PLOT.NAME | 3 plots:

# the 4 exported plots are the following: the three key scenarios total values compared over the projected timeline, then the individual high information breakdowns for each of them.

# maybe lets get this working for hte world for now, and then look into regional after...


# need to make the auto populating plot of percentage divergence

# GRAPH THE % DIVERGENCE OVER TIME
# GRAPH THE % DIVERGENCE OVER TIME
# GRAPH THE % DIVERGENCE OVER TIME


# make recommendations based 

#what do we need, we need to save all of the total fi

import pandas as pd
import plotly.express as px
import pandas as pd



# ______________________ works ________________________________ #

df = pd.read_csv("cleanedGlobal.csv")

def create_plot(years,values,unit,flow,product):

   df = pd.DataFrame({
       'Year': years,
       f'{unit}': values
   })

   titleName = f"{flow} - {product}"
   fig = px.line(df, x='Year', y=f'{unit}', title=titleName, markers=True)
   fig.write_html(f"static/plot-{titleName}.html")



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
            'Category': name  # For line differentiation
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



# def lookup(state):
#     if state==0:
#         return 'S'
#     elif state==1:
#         return 'A'
#     elif state==2:
#         return 'N'
#     else:
#         return '?'
    

    
totaling=False
previous_flow=''
previous_flow = df.loc[0,'FLOW']

for index, row in df.iterrows():    

    # Other columns
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

    # Outer loop to create 4 sublists (rows)
    for i in range(4):
        total_data.append([] * 1)


    # Dynamically initialise the individual data lists of lists
    # The individual,
    # names = ['Stated','Announced','Net Zero']
    # for name in names:
    #     list_name = f'{name}_list'
    #     list_name = list()

    #     for i in range(4):
    #         list_name.append([] * 1)


    # print(f'the pre is {previous_flow}')

    # Checks that we are in the same plot 

    # print(f'the flow is {flow}')
    if (previous_flow.lower() == flow.lower()):
            
            # print('flow is equal to pre')

            # Check if in the total section
            if product == 'Total':

                print(f'>> total detected <<, for chart: {flow}')

                totaling = True
                TotalPlotname = f'{flow} - Total'

                #Save the year to the year column
                total_data[3].append(year)

                #Save the speicif recorded value to its respective sublist
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
                

                # Sgraph = pd.DataFrame(columns=['graphName','years', 'values'])
                # Agraph = pd.DataFrame(columns=['graphName','years', 'values'])
                # Ngraph = pd.DataFrame(columns=['graphName','years', 'values'])

                # state=int()

                # We need to recognize when the scenario column changes

                    #need to append to the dataframe for stated policies 
                # if scenario == 'Stated Policies Scenario':
                #         if state != 0:
                #             ah=lookup(state)
                #             fullgraph = f'{ah}graph'
                #             fullgraph.loc[len(graph)] = [chart, year, value]
                #             state=0
                #         else:
                #             Sgraph.loc[len(graph)] = [chart, year, value]
                #             state=0

                # if scenario == 'Announced Pledges Scenario':
                #         if state !=1:
                #             ah=lookup(state)
                #             fullgraph = f'{ah}graph'
                #             fullgraph.loc[len(graph)] = [chart, year, value]
                #             state=1
                #         else:
                #             Agraph.loc[len(graph)] = [chart, year, value]
                #             state=1

                # if scenario == 'Net Zero Emissions by 2050 Scenario':
                #         if state != 2:
                #             ah=lookup(state)
                #             fullgraph = f'{ah}graph'
                #             fullgraph.loc[len(grap)] = [chart, year, value]
                #             state=2
                #         else:
                #             Ngraph.loc[len(grap)] = [chart, year, value]
                #             state=2

                # elif (chart != pre):
                    

                #     #when the flow changes we save the dataframes and reset
                #     l = ['S', 'A', 'N']
                #     for i in l:
                #         current_graph = globals()[f'{i}graph']
                #         years = current_graph['years'].tolist()
                #         values = current_graph['values'].tolist() 
                #         create_plots(years, values, unit, chart, pro)

                #     Sgraph = pd.DataFrame(columns=['graphName','years', 'values'])
                #     Agraph = pd.DataFrame(columns=['graphName','years', 'values'])
                #     Ngraph = pd.DataFrame(columns=['graphName','years', 'values'])
    else:
        print(f'flow has changed..... from {previous_flow} to {flow}')
        previous_flow=flow
            



    #this is broken, we need something which will create and append to 3 dataframes until flow changes.  

    #we actually have 2 cases: total and not. 


    # v = df.iloc[r]['']

    # I need to make dataframes for each general chart, need to split each into three for the 3 different scenarios, and then just compare the totals. 
    # each general chart will have 4 entires, total, and then the three
    #we will use plotly
    #we then can use plotly
    #so theres no need to 


    #we will read down the entire csv, and when we run into a change of 



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
    - need to update
    """

    print('create_total_plot called!')

    # Create a combined DataFrame
    df = pd.DataFrame()

    # we have to append 2 nans to the beginning of the announced pledges and net zero projections as they dont have data from 2010 and 2022    
    for i in [1, 2]:
        total_data[i] = [0, 0] + total_data[i]

    print(f'Hi we have just popped the years list from total data.... Here it is! {total_data}')
    for sub in total_data:
        print(len(sub))


    # This is constant throughout the dataset
    years = [2010, 2022, 2023, 2030, 2035, 2040, 2050]

    print(f'the years are {years}')
    print(len(years))

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

# Dynamically initialise the totalData list of lists
total_data = []

# Outer loop to create 3 sublists -- This is for the three scenarios.
for i in range(3):
    total_data.append([] * 1)


for index, row in df.iterrows():    

    # Label columns
    flow = df.loc[index, 'FLOW'] 
    product = df.loc[index, 'PRODUCT']
    unit = df.loc[index, 'UNIT'] 
    scenario = df.loc[index, 'SCENARIO'] 

    # Actual data
    year = df.loc[index, 'YEAR'] 
    value = df.loc[index, 'VALUE'] 


    # print(f'the pre is {previous_flow}')
    # print(f'the flow is {flow}'
    
    # Checks that we are in the same plot, prevents mixing of non standard data
    if (previous_flow.lower() == flow.lower()):
            
            # Check if in the total section
            if product == 'Total':

                print(f'>> total detected <<, for chart: {flow}')

                totaling = True
                TotalPlotname = f'{flow} - Total'

                

                # Save the specific recorded value to its respective sublist
                if scenario == 'Stated Policies Scenario':
                    total_data[0].append(value)

                elif scenario == 'Announced Pledges Scenario':
                    total_data[1].append(value)

                elif scenario == 'Net Zero Emissions by 2050 Scenario':
                    total_data[2].append(value)

                print(f'''the value we just tried to append was {value}
                        appending to {scenario}, heres it: {total_data}'''
                     )

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

        # Re-initialise the totalData list of lists
        total_data = []

        # Outer loop to create 3 sublists -- This is for the three scenarios.
        for i in range(3):
            total_data.append([] * 1)