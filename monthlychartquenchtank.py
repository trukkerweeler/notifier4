import matplotlib.pyplot as plt
import pandas as pd
import utils
import re
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from icecream import ic
import ast
maxperiod = 0

def createChart(chartdata):    
    """Creates a chart from the given data and saves it as a PDF."""
    # ic(chartdata)
    thiscomputer = utils.getcomputername()
    filedate = utils.sixdigitdate(datetime.today())
    for i in chartdata:
        # ic(i)
        thischart = i[0]
        thischartlabel = thischart['label']

        try:
            base
        except NameError:
            match thischartlabel:
                case 'Clean Tank 01':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        clean01file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        clean01base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Tank01'
                        clean01file = PdfPages(clean01base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                case 'Deox Tank 05':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        deox05file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        deox05base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Chem Film\Tank05 - Deox'
                        deox05file = PdfPages(deox05base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                case 'Passivation Tank 07':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        passivation07file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Passivation\Tank07 - Passivation-Nitric'
                        passivation07file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                case 'Alodine Tank 08':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        alodine08file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        alodine08base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Chem Film\Tank08 - Type1'
                        alodine08file = PdfPages(alodine08base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                case 'Alodine Tank 11':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        alodine11file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        alodine11base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Chem Film\Tank11 - Type2'
                        alodine11file = PdfPages(alodine11base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                case 'Tank 13 Pass Citric':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        tank13file = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                    else:
                        tank13base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Passivation\Tank13 - Passivation-Citric'
                        tank13file = PdfPages(tank13base + f'\\{filedate}_{thischartlabel} Trend.pdf')
                case 'Quench Tank Polymer':
                    if thiscomputer == 'DESKTOP-473QAMH':
                        base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                        quenchfile = PdfPages(base + f'\\{filedate}_Quench Tank Trend.pdf')
                    else:
                        quenchbase = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Heat Treat\Quench Tank'
                        quenchfile = PdfPages(quenchbase + f'\\{filedate}_Quench Tank Trend.pdf')      
                   
                case _:
                    ic("No match for saving Trend PDF.")
                    plt.show()


    chartno = 0
    for j in chartdata:
        chartno += 1
        mychart = j[0]
        chartlabel = mychart['label']
        units = mychart['type']
        xranges = mychart['x']
        yvalues = mychart['y']
        # ic(chartno, chartlabel, units, xranges, yvalues)

        # Create subplots
        fig, axs = plt.subplots(len(chartdata), 1, figsize=(10, 5 * len(chartdata)))
        
        # This works for the case of a single chart...
        # fig.text(0.5, 0.04, 'XXXXX', ha='center')
        
        if len(chartdata) == 1:
            axs = [axs]  # Ensure axs is iterable when there's only one subplot

        for idx, ax in enumerate(axs):
            mychart = chartdata[idx][0]
            chartlabel = mychart['label']
            units = mychart['type']
            xranges = mychart['x']
            yvalues = mychart['y']
          
            ax.plot(xranges, yvalues, marker='o')
            ax.set_title(f'{chartlabel}')

            if 'Quench Tank Polymer' in chartlabel:
                ax.set_xlabel('Week')
                ax.text(maxperiod-30, 15.75, 'Polymer Limits: 15-18', style='italic', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
                # fig.text(0.5, 0.04, 'Polymer Limits: 15-18 | pH limits: 7.5-9.2', ha='center')
            else :
                ax.set_xlabel('Month')
                ax.text(0.60, 8.92, 'pH Limits: 7.5-9.2', style='italic', bbox={'facecolor': 'white', 'alpha': 0.5, 'pad': 10})
            
            ax.set_ylabel(units)
            ax.grid(True)

        # Save the chart as a PDF
        match chartlabel:
            case 'Clean Tank 01':
                # clean01file.savefig(f'{filedate}_{label[1]} Trend.pdf')
                clean01file.savefig(plt.gcf())
            case 'Deox Tank 05':
                deox05file.savefig(plt.gcf())            
            case 'Passivation Tank 07':
                passivation07file.savefig(plt.gcf())
            case 'Alodine Tank 08':
                alodine08file.savefig(plt.gcf())
            case 'Alodine Tank 11':
                alodine11file.savefig(plt.gcf())
            case 'Tank 13 Pass Citric':
                tank13file.savefig(plt.gcf())
            case 'Quench Tank Polymer':
                plt.ylim(13, 18)
                quenchfile.savefig(plt.gcf(), orientation='landscape')       
            case 'Quench Tank pH':
                # Add sample text to the current figure
                plt.text(0.5, 0.5, 'Hello World', fontsize=12)  
                plt.ylim(7.5, 9.2)
                quenchfile.savefig(plt.gcf(), orientation='landscape')  
            case 'Quench Tank':
                # Add sample text to the current figure
                plt.text(0.5, 0.5, 'Hello World', fontsize=12)  
                quenchfile.savefig(plt.gcf(), orientation='landscape')  
                    #  set the y-axis limits
            case _:
                ic("No match for saving Trend PDF.")
                plt.show()
            
        try:
            clean01file.close()
        except:
            pass
        try:
            deox05file.close()
        except:
            pass
        try: 
            passivation07file.close()
        except:
            pass
        try:
            alodine08file.close()
        except:
            pass
        try:
            alodine11file.close()
        except:
            pass
        try:
            tank13file.close()
        except:
            pass
        try:
            quenchfile.close()
        except:
            pass

        plt.close()


def getdataset(actioncode):
    """Returns a dataset for the given action code."""
    match actioncode[0]:
        case 'QTPC': #Weekly
            sql = f'''with myalias as (SELECT pir.*, pi.RESPONSE_DATE, WEEK(pi.CREATE_DATE, 1) as week_of_year FROM PPL_INPT_RSPN pir inner join PEOPLE_INPUT pi on pir.INPUT_ID = pi.INPUT_ID 
            where pi.SUBJECT like '{actioncode[0]}%' and pi.CLOSED = 'Y' and CREATE_DATE > '2023-11-01' order by week_of_year desc limit 26 ) select * from myalias order by week_of_year asc;'''
        case _:
             sql = f'''with myalias as (SELECT pir.*, pi.RESPONSE_DATE, pi.CREATE_DATE FROM PPL_INPT_RSPN pir inner join PEOPLE_INPUT pi on pir.INPUT_ID = pi.INPUT_ID 
            where pi.SUBJECT like '{actioncode[0]}%' and pi.CLOSED = 'Y' and CREATE_DATE > '2023-11-01' order by CREATE_DATE desc limit 12 ) select * from myalias order by CREATE_DATE asc;'''

        # ic(sql)
    mydata = utils.getDatabaseData(sql)
    ic(mydata)
    myset = []
    # myvalues = []
    myperiod = []
    arrpHv = []
    arrmLv = []
    arrFv = []
    arrsv = []
    arrpHd = []
    arrmLd = []
    arrFd = []
    arrsd = []
    arrdBv = [] # degrees Brix
    arrPBVv = []
    arrPBVd = []
    arrFEv = []
    arrFEd = []
    arrPctv = []
    arrPctd = []
    arrgd = []
    arrgv = []
    
    arrdBd = []
    mypHobj = {}
    mymLobj = {}
    myFobj = {}
    mysobj = {}
    mydBobj = {}
    myPBVobj = {}
    myFEobj = {}
    myPctobj = {}
    mygobj = {}

    for i in range(len(mydata)):
        valueonly = -1
        responseText = mydata[i][1]
        global maxperiod
        # iterate through the data
        # for j in range(2, len(mydata[i])):
        #     ic(mydata[i][j])

        # Because the response date is not always populated, we need to get the date from the response text
        furDate = mydata[i][2] # followup response date
        if 'QTPH' in actioncode[0]: # monthly
            # ic(mydata[i][1])
            if furDate == None:
                yyyymm = re.search(r'(\d+.\d+)', mydata[i][1])
                if yyyymm:
                    yearmonth = yyyymm.group(0)
                    period = utils.threelettermonth(yearmonth)
                    myperiod.append(period)
            else:
                # convert the date to a string and get the year and month
                strFurDate = str(furDate)
                period = utils.threelettermonth(strFurDate[:7])
                myperiod.append(period)
                

            # determine greatest period for the x-axis set maxperiod as the global variable
            try:
                if period > maxperiod:
                    maxperiod = period
            except:
                # ic(period)
                # ic(maxperiod)
                pass

        else: # weekly
            if furDate == None:
                mydate = re.search(r'(\d+-\d+-\d+)', mydata[i][1])
                period = utils.weekofyear(mydate.group(0))
                myperiod.append(period)
            else:
                period = utils.weekofyear(furDate[:10])
                myperiod.append(period)
            
            # determine greatest period for the x-axis set maxperiod as the global variable
            # global maxperiod
            try:
                if period > maxperiod:
                    maxperiod = period
            except:
                # ic(period)
                # ic(maxperiod)
                pass

        
        
        # use regex to match curly brace dictionary item
        mymatch = re.search(r'({.*})', mydata[i][1])        
        
        # ic(mymatch)
        if mymatch:
            myobject = ast.literal_eval(mymatch.group(0))
            # ic(myobject)

            # for each unit in the action code, get the value from the dictionary
            for j in myobject:
                # ic(j)
                # thisunit = myobject.keys()[0]
                # ic(thisunit)
                match j:
                    case 'g':
                        if 'g' in myobject:
                            valueonly = myobject['g']
                            # ic(valueonly)
                            arrgv.append(valueonly)
                            arrgd.append(period)
                    case 'pH':
                        if 'pH' in myobject:
                            valueonly = myobject['pH']
                            # ic(valueonly)
                            arrpHv.append(valueonly)
                            arrpHd.append(period)
                    case 'mL':
                        if 'mL' in myobject:
                            valueonly = myobject['mL']
                            # ic(valueonly)
                            arrmLv.append(valueonly)
                            arrmLd.append(period)
                    case 'F':
                        if 'F' in myobject:
                            valueonly = myobject['F']
                            # ic(valueonly)
                            arrFv.append(valueonly)
                            arrFd.append(period)
                    case 's':
                        if 's' in myobject:
                            valueonly = myobject['s']
                            # ic(valueonly)
                            arrsv.append(valueonly)
                            arrsd.append(period)
                    case 'Brix':
                        if 'Brix' in myobject:
                            valueonly = myobject['Brix']
                            # ic(valueonly)
                            arrdBv.append(valueonly)
                            arrdBd.append(period)
                    case 'PBV':
                        if 'PBV' in myobject:
                            valueonly = myobject['PBV']
                            # ic(valueonly)
                            arrPBVv.append(valueonly)
                            arrPBVd.append(period)
                    case 'Fe':
                        if 'Fe' in myobject:
                            valueonly = myobject['Fe']
                            # ic(valueonly)
                            arrFEv.append(valueonly)
                            arrFEd.append(period)
                    case 'Pct':
                        if 'Pct' in myobject:
                            valueonly = myobject['Pct']
                            # ic(valueonly)
                            arrPctv.append(valueonly)
                            arrPctd.append(period)
                    case _:
                        ic("No match this unit: ", j)

    # for each of the arrays if not empty, append to myset
    if arrgv:
        mygobj['label'] = actioncode[1]
        mygobj['type'] = 'g'
        mygobj['x'] = arrgd
        mygobj['y'] = arrgv
        myset.append(mygobj)
    if arrpHv:
        mypHobj['label'] = actioncode[1]
        mypHobj['type'] = 'pH'
        mypHobj['x'] = arrpHd
        mypHobj['y'] = arrpHv

        myset.append(mypHobj)
    if arrmLv:
        mymLobj['label'] = actioncode[1]
        mymLobj['type'] = 'mL'
        mymLobj['x'] = arrmLd
        mymLobj['y'] = arrmLv
        myset.append(mymLobj)
    if arrFv:
        myFobj['label'] = actioncode[1]
        myFobj['type'] = 'F'
        myFobj['x'] = arrFd
        myFobj['y'] = arrFv
        myset.append(myFobj)
    if arrsv:
        mysobj['label'] = actioncode[1]
        mysobj['type'] = 's'
        mysobj['x'] = arrsd
        mysobj['y'] = arrsv
        myset.append(mysobj)
    if arrdBv:
        mydBobj['label'] = actioncode[1]
        mydBobj['type'] = 'Brix'
        mydBobj['x'] = arrdBd
        mydBobj['y'] = arrdBv
        myset.append(mydBobj)
    if arrPBVv:
        myPBVobj['label'] = actioncode[1]
        myPBVobj['type'] = 'PBV'
        myPBVobj['x'] = arrPBVd
        myPBVobj['y'] = arrPBVv
        myset.append(myPBVobj)
    if arrFEv:
        myFEobj['label'] = actioncode[1]
        myFEobj['type'] = 'Fe'
        myFEobj['x'] = arrFEd
        myFEobj['y'] = arrFEv
        myset.append(myFEobj)
    if arrPctv:
        myPctobj['label'] = actioncode[1]
        myPctobj['type'] = 'Pct'
        myPctobj['x'] = arrPctd
        myPctobj['y'] = arrPctv
        myset.append(myPctobj)

    # ic(myset)
    return myset


def main():
    # labels = [['QTP','Quench Tank',['pH', 's']]]
    labels = ['QTPC','QTPH']
    # labels = ['QTPC']
    datasets = []

    for label in labels:
        # ['QTPC', 'Quench Tank Polymer', ['s']]
        match label:
            case 'QTPC':
                # ic(label + "====================")
                mylabel = getdataset(['QTPC','Quench Tank Polymer',['s']])
            case 'QTPH':
                # ic(label + "====================")
                mylabel = getdataset(['QTPH','Quench Tank pH',['pH']])
            case _:
                ic("No match for label.")
        
        # mydataset = getdataset(mylabel)
        # ic(mydataset)
        datasets.append(mylabel)
    # ic(datasets)
    createChart(datasets)


if __name__ == "__main__":
    """For month-end reporting, create a chart for each action code in the labels list. Not set up for weekly or quarterly reporting."""
    main()
    print("done")