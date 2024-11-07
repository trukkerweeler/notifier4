import matplotlib.pyplot as plt
import pandas as pd
import utils
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from icecream import ic
import ast

def getCreatedData():
    """Gets the summary CA data for the last 12 months"""
    
    sql = """
    SELECT 
        DATE_FORMAT(CORRECTIVE_DATE, '%Y-%m-01') AS month, 
        COUNT(*) AS count
    FROM 
        CORRECTIVE
    WHERE 
        CORRECTIVE_DATE >= DATE_FORMAT(CURDATE() - INTERVAL 12 MONTH, '%Y-%m-01')
    GROUP BY 
        month
    ORDER BY 
        month;
    """
    caData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    caData = [{'month': x[0], 'count': x[1]} for x in caData]
    # convert the month to month name
    caData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in caData]
    # convert the output to a pandas dataframe
    caData = pd.DataFrame(caData)
    # add label month to the month column
    # caData['month'] = caData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return caData


def getClosedData():
    """Gets the summary CA data for the last 12 months"""
    
    sql = """
    SELECT 
        DATE_FORMAT(CLOSED_DATE, '%Y-%m-01') AS month, 
        COUNT(*) AS count
    FROM 
        NONCONFORMANCE
    WHERE 
        CLOSED_DATE >= DATE_FORMAT(CURDATE() - INTERVAL 12 MONTH, '%Y-%m-01')
    GROUP BY 
        month
    ORDER BY 
        month;
    """
    caData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    caData = [{'month': x[0], 'count': x[1]} for x in caData]
    # convert the month to month name
    caData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in caData]
    # convert the output to a pandas dataframe
    caData = pd.DataFrame(caData)
    # add label month to the month column
    caData['month'] = caData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return caData

def caCreatedChart(caData):
    """Creates a chart of the CA data"""
    # create a new figure
    fig, ax = plt.subplots()
    # plot the data
    ax.plot(caData['month'], caData['count'])
    # set the x-axis labels
    ax.set_xticklabels(caData['month'], rotation=45)
    # set the title
    ax.set_title('Corrective Summary: Created 2024')
    # set the x-axis label
    ax.set_xlabel('Month')
    # set the y-axis label
    ax.set_ylabel('Count')
    # save the chart to a pdf
    pdf = PdfPages('ca_chart.pdf')
    pdf.savefig(fig)
    pdf.close()
    # display the chart
    plt.show()


def getOpenData():
    """Gets the summary CA data for the last 12 months"""
    
    sql = """
    SELECT 
        DATE_FORMAT(CORRECTIVE_DATE, '%Y-%m-01') AS month, 
        COUNT(*) AS count
    FROM 
        CORRECTIVE
    WHERE 
        CLOSED_DATE IS NULL
    GROUP BY 
        month
    ORDER BY 
        month;
    """
    caData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    caData = [{'month': x[0], 'count': x[1]} for x in caData]
    # convert the month to month name
    caData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in caData]
    # convert the output to a pandas dataframe
    caData = pd.DataFrame(caData)
    # add label month to the month column
    # caData['month'] = caData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return caData


def getAgingData():
    """Gets the summary CA data for the last 12 months"""
    sql = """
    SELECT 
        DATE_FORMAT(CORRECTIVE_DATE, '%Y-%m-01') AS month, 
        AVG(DATEDIFF(CURDATE(), CORRECTIVE_DATE)) AS avg_age
    FROM 
        CORRECTIVE
    WHERE 
        CLOSED_DATE IS NULL and CORRECTIVE_DATE > CURDATE() - INTERVAL 12 MONTH
    GROUP BY 
        month
    ORDER BY 
        month;
    """

    caData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    caData = [{'month': x[0], 'count': x[1]} for x in caData]
    # convert the month to month name
    caData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in caData]
    # convert the output to a pandas dataframe
    caData = pd.DataFrame(caData)
    # add label month to the month column
    # caData['month'] = caData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return caData

def caAgingChart(caData):
    """Creates a chart of the CA data for closed CAs"""
    # create a new figure
    fig, ax = plt.subplots()
    # plot the data
    ax.plot(caData['month'], caData['count'])
    # set the x-axis labels
    ax.set_xticklabels(caData['month'], rotation=45)
    # set the title
    ax.set_title('Corrective Summary: Aging 2024')
    # set the x-axis label
    ax.set_xlabel('Month')
    # set the y-axis label
    ax.set_ylabel('Count')
    # Set a target line of 60 days
    ax.axhline(y=60, color='r', linestyle='--')
    # save the chart to a pdf
    pdf = PdfPages('ca_chart.pdf')
    pdf.savefig(fig)
    pdf.close()
    # display the chart
    plt.show()

def main():
    """Creates charts for CA trend information"""
    caData = getCreatedData()
    # ic(ncmData)
    caCreatedChart(caData)
    caData = getAgingData()
    # ic(caData)
    caAgingChart(caData)


if __name__ == '__main__':
    main()