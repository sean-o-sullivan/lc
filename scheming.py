import pandas as pd
import plotly.express as px
import pandas as pd




# ______________________ works ? ________________________________ #

df = pd.read_csv("graphingWorld.csv")
def create_plots(years,values,unit,flo,pro):

   df = pd.DataFrame({
       'Year': years,
       f'{unit}': values
   })

   ti = f"{flo} - {pro}"
   fig = px.line(df, x='Year', y=f'{unit}', title=ti, markers=True)
   fig.write_html(f"static/plot-{ti}.html")

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
grap = pd.DataFrame(columns=['graphName','years', 'values'])
toting=False

for index, row in df.iterrows():    

    # Other columns
    chart = df.loc[index, 'FLOW'] 
    pro = df.loc[index, 'PRODUCT']
    unit = df.loc[index, 'UNIT'] 
    scenario = df.loc[index, 'SCENARIO'] 

    # Actual data
    year = df.loc[index, 'YEAR'] 
    value = df.loc[index, 'VALUE'] 


    # If this is the total section
    if pro.lower() == 'total':
        totaling = True
        print('>> total detected <<')
        nam2 = f'{chart} - Total'
        grap.loc[len(grap)] = [nam2, year, value]
        print(grap)
    else:
        if totaling:
            #need to save to that graph for the totaling and exit 
            pass
        
        totaling = False
        Sgraph = pd.DataFrame(columns=['graphName','years', 'values'])
        Agraph = pd.DataFrame(columns=['graphName','years', 'values'])
        Ngraph = pd.DataFrame(columns=['graphName','years', 'values'])

        state=int()

        # We need to recognize when the scenario column changes
        if (chart == pre) and not index != 0:

            #need to append to the dataframe for stated policies 
            if scenario == 'Stated Policies Scenario':
                if state != 0:
                    ah=lookup(state)
                    fullgraph = f'{ah}graph'
                    fullgraph.loc[len(grap)] = [chart, year, value]
                    state=0
                else:
                    Sgraph.loc[len(grap)] = [chart, year, value]
                    state=0


            if scenario == 'Announced Pledges Scenario':
                if state !=1:
                    ah=lookup(state)
                    fullgraph = f'{ah}graph'
                    fullgraph.loc[len(grap)] = [chart, year, value]
                    state=1
                else:
                    Agraph.loc[len(grap)] = [chart, year, value]
                    state=1


            if scenario == 'Net Zero Emissions by 2050 Scenario':
                if state != 2:
                    ah=lookup(state)
                    fullgraph = f'{ah}graph'
                    fullgraph.loc[len(grap)] = [chart, year, value]
                    state=2
                else:
                    Ngraph.loc[len(grap)] = [chart, year, value]
                    state=2

        elif (chart != pre and index!=0):
            

            #when the flow changes we save the dataframes and reset
            l = ['S', 'A', 'N']
            for i in l:
                current_graph = globals()[f'{i}graph']
                years = current_graph['years'].tolist()
                values = current_graph['values'].tolist() 
                create_plots(years, values, unit, chart, pro)

            Sgraph = pd.DataFrame(columns=['graphName','years', 'values'])
            Agraph = pd.DataFrame(columns=['graphName','years', 'values'])
            Ngraph = pd.DataFrame(columns=['graphName','years', 'values'])

    pre=chart



#this is broken, we need something which will create and append to 3 dataframes until flow changes.  

#we actually have 2 cases: total and not. 


# v = df.iloc[r]['']

# I need to make dataframes for each general chart, need to split each into three for the 3 different scenarios, and then just compare the totals. 
# each general chart will have 4 entires, total, and then the three
#we will use plotly
#we then can use plotly
#so theres no need to 


#we will read down the entire csv, and when we run into a change of 