import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import utils
from datetime import datetime
import os

def getsupplierdata():
    sql = "SELECT * FROM EIGHTYFOURELEVEN where SAMPLE_DATE between NOW() - INTERVAL 1 YEAR AND NOW() ORDER BY INPUT_ID DESC;"
    
    data = utils.getDatabaseData(sql)
    return data


def getsuppliertrend():
    
    data = getsupplierdata()
    # print(data)

    # Extract unique suppliers
    suppliers = set(row[2] for row in data if row[2])
    
    # determine previous quarter for the filename with the format YYYYQn
    quarter = (datetime.now().month - 1) // 3

    # Create a plot for each supplier with both samples (OTD and Q) on the same plot
    for supplier in suppliers:
        # Filter data for the current supplier
        filtered_data = [row for row in data if row[2] == supplier]
        
        if not filtered_data:
            continue
        
        # Separate data by sample type
        otd_data = [row for row in filtered_data if row[3] == "OTD"]
        q_data = [row for row in filtered_data if row[3] == "Q"]
        
        # Extract dates and values for OTD
        otd_dates = [row[5] for row in otd_data]
        otd_values = [float(row[4]) for row in otd_data]
        
        # Extract dates and values for Q
        q_dates = [row[5] for row in q_data]
        q_values = [float(row[4]) for row in q_data]
        
        # Sort by date
        otd_dates_values = sorted(zip(otd_dates, otd_values))
        otd_dates = [dv[0] for dv in otd_dates_values]
        otd_values = [dv[1] for dv in otd_dates_values]
        
        q_dates_values = sorted(zip(q_dates, q_values))
        q_dates = [dv[0] for dv in q_dates_values]
        q_values = [dv[1] for dv in q_dates_values]
        
        # Plot the trendline
        plt.figure(figsize=(10,5))
        
        plt.plot(otd_dates, otd_values,label='OTD')
        plt.plot(q_dates,q_values,label='Q')
        
        # Format the date on x-axis to show quarters
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        
        plt.title(f'Trendline for Supplier: {supplier}')
        plt.xlabel('Date')
        plt.ylabel('Value')
        
        plt.legend()
        
        plt.grid(True)
        
        # Save each plot to a file
        # Create directory if it doesn't exist
        output_dir = "suppliertrendcharts"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Save each plot to a file in the specified directory
        plt.savefig(os.path.join(output_dir, f"{supplier} trend_{datetime.now().year}Q{quarter}.png"))
        # plt.savefig(f"{supplier} trend_{datetime.now().year}Q{quarter}.png")
        # plt.show()



if __name__ == "__main__":
    # data = getsupplierdata()
    # print(data)
    getsuppliertrend()