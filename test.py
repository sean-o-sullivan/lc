    # Dynamically initialise the totalData list of lists
total_data = []

    # Outer loop to create 3 sublists -- This is for the three scenarios' total data.
for _ in range(3):
    total_data.append([[],[]])    



print(total_data)

total_data[0][0].append('test')


print(total_data)
