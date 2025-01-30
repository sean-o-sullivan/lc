
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


def create_total_plot(years, values_list, unit, flow, product, line_names):
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
    for name, values in zip(line_names, values_list):
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
    fig.write_html(f"Total_plot-{title}.html")



def lookup(state):
    if state==0:
        return 'S'
    elif state==1:
        return 'A'
    elif state==2:
        return 'N'
    else:
        return '?'
    

# def saveProcedure():
    
prev=''
pre=''
uniques = pd.DataFrame(columns=['graphName', 'startIndex', 'endIndex'])
graph = pd.DataFrame(columns=['graphName','years', 'values'])
totaling=False



pre = df.loc[0,'FLOW']
for index, row in df.iterrows():    

    # Other columns
    flow = df.loc[index, 'FLOW'] 
    product = df.loc[index, 'PRODUCT']
    unit = df.loc[index, 'UNIT'] 
    scenario = df.loc[index, 'SCENARIO'] 

    # Actual data
    year = df.loc[index, 'YEAR'] 
    value = df.loc[index, 'VALUE'] 

    totalData = [[0] * 2 for _ in range(1)]

    if (flow == pre):

        # Check if in the total section
        if product.lower() == 'Total':

            print('>> total detected <<')
            totaling = True
            TotalPlotname = f'{flow} - Total'
            totalData.append[year,value]
            print(totalData)

        else:
            #save the data collected while totalling and make a plot for this 
            if totaling:
                years, values = totalData
                years = [2020, 2021, 2022, 2023]

                this is how we add;

                                # Add 160 to Line 1 (Production)
                values_data[0].append(160)

                # Add 155 to Line 2 (Consumption)
                values_data[1].append(155)

                # Add 165 to Line 3 (Exports)
                values_data[2].append(165)


                values_data = [
                    [100, 120, 130, 145],  # Line 1 values, shall be Stated Policies
                    [95, 115, 125, 140],   # Line 2 values, shall be Announced Pledges
                    [105, 125, 135, 150]   # Line 3 values, shall be net zero emissions
                ]

                create_plot(
                    years=years,
                    values_list=values_data,
                    unit="Metric Tons",
                    flow="Agriculture",
                    product="Wheat",
                    line_names=["Production", "Consumption", "Exports"]
                )


                create_plot(years,values,unit,flow,product)
                totaling=False


            Sgraph = pd.DataFrame(columns=['graphName','years', 'values'])
            Agraph = pd.DataFrame(columns=['graphName','years', 'values'])
            Ngraph = pd.DataFrame(columns=['graphName','years', 'values'])

            state=int()

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
        print(f'flow has changed..... from {pre} to {chart}')
        pre=chart
        continue



#this is broken, we need something which will create and append to 3 dataframes until flow changes.  

#we actually have 2 cases: total and not. 


# v = df.iloc[r]['']

# I need to make dataframes for each general chart, need to split each into three for the 3 different scenarios, and then just compare the totals. 
# each general chart will have 4 entires, total, and then the three
#we will use plotly
#we then can use plotly
#so theres no need to 


#we will read down the entire csv, and when we run into a change of 
