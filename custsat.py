import utils
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from icecream import ic

# Load the data
# mysql statement to select all records in the last 13 months
sql = "SELECT * FROM NINETYONETWENTY WHERE SAMPLE_DATE >= DATE_SUB(NOW(), INTERVAL 12 MONTH)"
data = utils.getDatabaseData(sql)
# ic(data)

# Create a DataFrame
df = pd.DataFrame(data, columns=['COLLECTION_ID','INPUT_ID', 'CUSTOMER_ID', 'UNIT', 'VALUE', 'SAMPLE_DATE', 'PEOPLE_ID'])
# Get the unique customers
customers = df['CUSTOMER_ID'].unique()

# For each customer, get the data and plot
for customer in customers:
    customer_data = df[df['CUSTOMER_ID'] == customer]
    # Get the unique units
    units = customer_data['UNIT'].unique()
    # ic(collections)
    for unit in units:
        # filter the date by customer and unit
        unit_data_df = df[(df['CUSTOMER_ID'] == customer) & (df['UNIT'] == unit)]
        months = []
        values = []
        for index, row in unit_data_df.iterrows():
            myvalue = row['VALUE']
            sample_date = pd.to_datetime(row['SAMPLE_DATE'])
            # sample date string first 10 characters
            sample_date = sample_date.strftime('%Y-%m-%d')
            month = utils.threelettermonth(sample_date)
            months.append(month)
            # convert the value to float
            myvalue = float(myvalue)
            values.append(myvalue)
            # Set the plot title
            plt.title(f"{customer} {unit}")

        if (unit == 'OTIF') or (unit == 'OTD'):
            # plt.ylim(0, 100)
            plt.axis([0, len(months), 0, 100])
            # plot the graduatons eqally
            plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.plot(months, values, marker='o', color='b')
        plt.show()
