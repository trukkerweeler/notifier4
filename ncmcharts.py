import matplotlib.pyplot as plt
import pandas as pd
import utils
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from icecream import ic
import ast

def getCreatedData():
    """Gets the summary NCM data for the last 12 months"""
    
    sql = """
    SELECT 
        DATE_FORMAT(NCM_DATE, '%Y-%m-01') AS month, 
        COUNT(*) AS count
    FROM 
        NONCONFORMANCE
    WHERE 
        NCM_DATE >= DATE_FORMAT(CURDATE() - INTERVAL 12 MONTH, '%Y-%m-01')
    GROUP BY 
        month
    ORDER BY 
        month;
    """
    ncmData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    ncmData = [{'month': x[0], 'count': x[1]} for x in ncmData]
    # convert the month to month name
    ncmData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in ncmData]
    # convert the output to a pandas dataframe
    ncmData = pd.DataFrame(ncmData)
    # add label month to the month column
    # ncmData['month'] = ncmData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return ncmData


def getClosedData():
    """Gets the summary NCM data for the last 12 months"""
    
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
    ncmData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    ncmData = [{'month': x[0], 'count': x[1]} for x in ncmData]
    # convert the month to month name
    ncmData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in ncmData]
    # convert the output to a pandas dataframe
    ncmData = pd.DataFrame(ncmData)
    # add label month to the month column
    # ncmData['month'] = ncmData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return ncmData

def ncmCreatedChart(ncmData):
    """Creates a chart of the NCM data"""
    # create a new figure
    fig, ax = plt.subplots()
    # plot the data
    ax.plot(ncmData['month'], ncmData['count'])
    # set the x-axis labels
    ax.set_xticklabels(ncmData['month'], rotation=45)
    # set the title
    ax.set_title('NCM Summary: Created 2024')
    # set the x-axis label
    ax.set_xlabel('Month')
    # set the y-axis label
    ax.set_ylabel('Count')
    # save the chart to a pdf
    pdf = PdfPages('ncm_chart.pdf')
    pdf.savefig(fig)
    pdf.close()
    # display the chart
    plt.show()


def ncmClosedChart1(ncmData):
    """Creates a chart of the NCM data for closed NCMs"""
    # create a new figure
    fig, ax = plt.subplots()
    # plot the data
    ax.plot(ncmData['month'], ncmData['count'])
    # set the x-axis labels
    ax.set_xticklabels(ncmData['month'], rotation=45)
    # set the title
    ax.set_title('NCM Summary: Closed 2024')
    # set the x-axis label
    ax.set_xlabel('Month')
    # set the y-axis label
    ax.set_ylabel('Count')
    # save the chart to a pdf
    pdf = PdfPages('ncm_chart.pdf')
    pdf.savefig(fig)
    pdf.close()
    # display the chart
    plt.show()


def getOpenData():
    """Gets the summary NCM data for the last 12 months"""
    
    sql = """
    SELECT 
        DATE_FORMAT(NCM_DATE, '%Y-%m-01') AS month, 
        COUNT(*) AS count
    FROM 
        NONCONFORMANCE
    WHERE 
        CLOSED_DATE IS NULL
    GROUP BY 
        month
    ORDER BY 
        month;
    """
    ncmData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    ncmData = [{'month': x[0], 'count': x[1]} for x in ncmData]
    # convert the month to month name
    ncmData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in ncmData]
    # convert the output to a pandas dataframe
    ncmData = pd.DataFrame(ncmData)
    # add label month to the month column
    # ncmData['month'] = ncmData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return ncmData


def getAgingData():
    """Gets the summary NCM data for the last 12 months"""
    sql = """
    SELECT 
        DATE_FORMAT(NCM_DATE, '%Y-%m-01') AS month, 
        AVG(DATEDIFF(CURDATE(), NCM_DATE)) AS avg_age
    FROM 
        NONCONFORMANCE
    WHERE 
        CLOSED_DATE IS NULL and NCM_DATE > CURDATE() - INTERVAL 12 MONTH
    GROUP BY 
        month
    ORDER BY 
        month;
    """

    ncmData = utils.getDatabaseData(sql)
    # convert the 0th field to a month string
    ncmData = [{'month': x[0], 'count': x[1]} for x in ncmData]
    # convert the month to month name
    ncmData = [{'month': datetime.strptime(x['month'], '%Y-%m-%d').strftime('%b'), 'count': x['count']} for x in ncmData]
    # convert the output to a pandas dataframe
    ncmData = pd.DataFrame(ncmData)
    # add label month to the month column
    # ncmData['month'] = ncmData['month'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').strftime('%b %Y'))
        
    return ncmData

def ncmAgingChart(ncmData):
    """Creates a chart of the NCM data for closed NCMs"""
    # create a new figure
    fig, ax = plt.subplots()
    # plot the data
    ax.plot(ncmData['month'], ncmData['count'])
    # set the x-axis labels
    ax.set_xticklabels(ncmData['month'], rotation=45)
    # set the title
    ax.set_title('NCM Summary: Aging 2024')
    # set the x-axis label
    ax.set_xlabel('Month')
    # set the y-axis label
    ax.set_ylabel('Days')
    # Set a target line of 30 days
    ax.axhline(y=30, color='r', linestyle='--')
    # save the chart to a pdf
    pdf = PdfPages('ncm_chart.pdf')
    pdf.savefig(fig)
    pdf.close()
    # display the chart
    plt.show()

def main():
    # ncmData = getCreatedData()
    # # ic(ncmData)
    # ncmCreatedChart(ncmData)
    # ncmData = getClosedData()
    # # ic(ncmData)
    # ncmClosedChart1(ncmData)
    # ncmData = getOpenData()
    # ic(ncmData)
    ncmData = getAgingData()
    ic(ncmData)
    ncmAgingChart(ncmData)


    


if __name__ == '__main__':
    main()