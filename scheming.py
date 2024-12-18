import pandas as pd

df = pd.read_csv("graphingWorld.csv")
print("Dataset\n")
heads = list(df.head(1))
print(heads)


#need to start trying to detect the boundaries of graphs, we are checking flow, need to make new pandas dataframes and cut and paste rows into them, we could either copy and paste rows or we could just create a new list which indexes (inclusively) the row index of the start and end of a specific data series for a given graph




#sp denotes the name start and end of the data for a specific plot
sp = pd.DataFrame(columns=['graphName', 'startIndex', 'endIndex'])
print(sp)


#returns a df: sp  which includes the start and end positions within the csv for all of the 
# ______________________ works ! ________________________________ #
prev=''
start=0
end=0
for index, row in df.iterrows():    
    name = df.loc[index, 'FLOW'] 
    if (name != prev) and index != 0:
        print(index)
        input('yo')
        end=index
        sp.loc[len(sp)] = [name, start, index]    
        start = end+1
    prev=name


print(sp.head(500))