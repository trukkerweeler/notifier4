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
    ic(customer)
    # Create a plot for each customer with 3 subplots
    fig, ax = plt.subplots(3, 1, figsize=(10, 10))
    # set the title of the plot
    fig.suptitle('Customer Trends: ' + str(customer), fontsize=16, fontweight='bold')

    customer_data = df[df['CUSTOMER_ID'] == customer]
    # Get the unique units
    units = customer_data['UNIT'].unique()
    # ic(collections)
    for unit in units:
        ic(unit)
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
            
        match unit:
            case 'OTIF':
                ax[0].plot(months, values, marker='P', color='b')
                ax[0].set_title('OTIF (Delivery)')
                plt.axis([0, len(months), 0, 100])
                # plot the graduatons equally
                plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
            case 'OTD':
                ax[0].plot(months, values, marker='P', color='b')
                ax[0].set_title('OTD (Delivery)')
                plt.axis([0, len(months), 0, 100])
                # plot the graduatons equally
                plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(10))
            case 'CUSTSAT':
                plt.cla()
                ax[2].plot(months, values, marker='o', color='g')
                ax[2].set_title('CUSTSAT')
            case 'PPM':
                plt.cla()
                # flip the y axis
                ax[2].invert_yaxis()
                ax[2].plot(months, values, marker='*', color='y')
                ax[2].set_title('PPM (k)')
            case 'ESCAPES':
                # plt.cla()
                # flip the y axis
                ax[1].invert_yaxis()
                ax[1].plot(months, values, marker='x', color='m')
                ax[1].set_title('Escapes')
            case 'C':
                ic(unit)
                ax[2].plot(months, values, marker='o', color='m')
                ax[2].set_title('Composite')
            case 'Q':
                ic(unit)
                ax[1].plot(months, values, marker='o', color='m')
                ax[1].set_title('Quality')
            case _:
                ic('No match: ' + unit)
            
    plt.tight_layout()
    plt.show()
