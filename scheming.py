import pandas as pd
import plotly.express as px
import pandas as pd




# ______________________ works ? ________________________________ #

df = pd.read_csv("graphingWorld.csv")
def create_plots(years,values,unit,flo,pro):
   
   df = pd.DataFrame({
       'Year': years,
       'f{unit}': values
   })
   ti = f"{flo} - {pro}"
   fig = px.line(df, x='Year', y=f'{unit}', title=ti, markers=True)
   fig.write_html(f"static/plot-{ti}.html")


prev=''
pre=''
uniques = pd.DataFrame(columns=['graphName', 'startIndex', 'endIndex'])
grap = pd.DataFrame(columns=['graphName','years', 'values'])

for index, row in df.iterrows():    

    # Other columns
    flo = df.loc[index, 'FLOW'] 
    pro = df.loc[index, 'PRODUCT']
    unit = df.loc[index, 'UNIT'] 
    scen = df.loc[index, 'SCENARIO'] 

    # Actual data
    year = df.loc[index, 'UNIT'] 
    value = df.loc[index, 'UNIT'] 
    
    # If this is the total section
    if pro.lower() == 'total':
        na = f'{flo} - Total'
        grap.loc[len(grap)] = [na, year, value]
        toting = True

    else:
        # We need to recognize when the scenario column changes
        if toting and (len(grap) > 1):
            years = grap['years'].tolist()
            values = grap['values'].tolist()
            create_plots(years, values, unit, flo, pro)
            grap = pd.DataFrame(columns=['graphName', 'years', 'values'])
        else:
            if (scen != pre) and index != 0:
                years = grap['years'].tolist()
                values = grap['values'].tolist()
                create_plots(years, values, unit, flo, pro)
                grap = pd.DataFrame(columns=['graphName', 'years', 'values'])
        
    pre=scen
    





# v = df.iloc[r]['']

# I need to make dataframes for each general chart, need to split each into three for the 3 different scenarios, and then just compare the totals. 
# each general chart will have 4 entires, total, and then the three
#we will use plotly
#we then can use plotly
#so theres no need to 


#we will read down the entire csv, and when we run into a change of 