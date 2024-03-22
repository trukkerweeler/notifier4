import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from icecream import ic

# Load the data
# mysql statement to select all records in the last 13 months
sql = "SELECT * FROM NINETYONETWENTY WHERE SAMPLE_DATE >= DATE_SUB(NOW(), INTERVAL 13 MONTH)"
data = utils.getDatabaseData(sql)
# ic(data)

# Create a DataFrame
df = pd.DataFrame(data, columns=['COLLECTION_ID','INPUT_ID', 'CUSTOMER_ID', 'UNIT', 'VALUE', 'SAMPLE_DATE', 'PEOPLE_ID'])
# ic(df)
# For each customer, trend each collection by Unit in a separate plot
# Get the unique customers
customers = df['CUSTOMER_ID'].unique()

# For each customer, get the data and plot
for customer in customers:
    customer_data = df[df['CUSTOMER_ID'] == customer]
    # ic(customer_data)
    # Get the unique units
    units = customer_data['UNIT'].unique()
    # ic(collections)
    for unit in units:
        ic("====================")
        # filter the date by customer and unit
        unit_data = customer_data[customer_data['UNIT'] == unit]
        # ic(unit_data)
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(unit_data['SAMPLE_DATE'], unit_data['VALUE'], marker='o')
        plt.title(f'Customer {customer} - {unit}')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.grid(True)
        plt.gca().xaxis.set_major_locator(ticker.MaxNLocator(nbins=12))
        plt.gca().xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: pd.to_datetime(x).strftime('%Y-%m')))
        plt.show()
        


        