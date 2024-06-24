import matplotlib.pyplot as plt
import pandas as pd
import utils
import re
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
from icecream import ic
import ast


def createChart(chartdata):    
    """Creates a chart from the given data and saves it as a PDF."""
    # ic(chartdata)
    thiscomputer = utils.getcomputername()
    filedate = utils.sixdigitdate(datetime.today())
    thischart = chartdata[0]
    thischartlabel = thischart['label']

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
        case 'Quench Tank':
            if thiscomputer == 'DESKTOP-473QAMH':
                base = r'C:\Users\tim\OneDrive\Documents\Python\charts'
                quenchfile = PdfPages(base + f'\\{filedate}_{thischartlabel} Trend.pdf')
            else:
                quenchbase = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Heat Treat\Quench Tank'
                quenchfile = PdfPages(quenchbase + f'\\{filedate}_{thischartlabel} Trend.pdf')            
        case _:
            ic("No match for saving Trend PDF.")
            plt.show()
    chartno = 0

    # ic(chartdata)
    for i in chartdata:
        # ic(i)
        
        units = i['type']
        label = i['label']
        chartlabel = i['label'] + ' - ' + units
        
        chartno += 1
        plt.subplot(len(chartdata), 1, chartno)
        plt.plot(i['x'], i['y'])

        plt.ylabel(units, rotation=0, labelpad=20)
        
        # plt.title('Trend of ' + units + ' in ' + label[1])
        plt.title(chartlabel + ' Trend')
    

    plt.tight_layout()

    # Save the chart as a PDF
    match label:
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
        case 'Quench Tank':
            quenchfile.savefig(plt.gcf())            
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
    sql = f'''with myalias as (SELECT pir.*, pi.CREATE_DATE FROM PPL_INPT_RSPN pir inner join PEOPLE_INPUT pi on pir.INPUT_ID = pi.INPUT_ID 
    where pi.SUBJECT = '{actioncode[0]}' and pi.CLOSED = 'Y' and CREATE_DATE > '2023-11-01'order by CREATE_DATE desc limit 12 ) select * from myalias order by CREATE_DATE asc;'''
    mydata = utils.getDatabaseData(sql)
    # ic(mydata)
    myset = []
    # myvalues = []
    mymonths = []
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

        yyyymm = re.search(r'(\d+.\d+)', mydata[i][1])
        if yyyymm:
            yearmonth = yyyymm.group(0)
            monthonly = utils.threelettermonth(yearmonth)
            # monthonly = yearmonth[5:]
            # if monthonly == '01':
            #     monthonly = 'Jan' + yearmonth[2:4]
            mymonths.append(monthonly)
        
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
                            arrgd.append(monthonly)
                    case 'pH':
                        if 'pH' in myobject:
                            valueonly = myobject['pH']
                            # ic(valueonly)
                            arrpHv.append(valueonly)
                            arrpHd.append(monthonly)
                    case 'mL':
                        if 'mL' in myobject:
                            valueonly = myobject['mL']
                            # ic(valueonly)
                            arrmLv.append(valueonly)
                            arrmLd.append(monthonly)
                    case 'F':
                        if 'F' in myobject:
                            valueonly = myobject['F']
                            # ic(valueonly)
                            arrFv.append(valueonly)
                            arrFd.append(monthonly)
                    case 's':
                        if 's' in myobject:
                            valueonly = myobject['s']
                            # ic(valueonly)
                            arrsv.append(valueonly)
                            arrsd.append(monthonly)
                    case 'Brix':
                        if 'Brix' in myobject:
                            valueonly = myobject['Brix']
                            # ic(valueonly)
                            arrdBv.append(valueonly)
                            arrdBd.append(monthonly)
                    case 'PBV':
                        if 'PBV' in myobject:
                            valueonly = myobject['PBV']
                            # ic(valueonly)
                            arrPBVv.append(valueonly)
                            arrPBVd.append(monthonly)
                    case 'Fe':
                        if 'Fe' in myobject:
                            valueonly = myobject['Fe']
                            # ic(valueonly)
                            arrFEv.append(valueonly)
                            arrFEd.append(monthonly)
                    case 'Pct':
                        if 'Pct' in myobject:
                            valueonly = myobject['Pct']
                            # ic(valueonly)
                            arrPctv.append(valueonly)
                            arrPctd.append(monthonly)
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
    labels = [['01TE','Clean Tank 01',['Pct','F']],['05TE', 'Deox Tank 05', ['mL', 'Pct', 'F','g']],['11PH','Alodine Tank 11',['pH']],['08TE','Alodine Tank 08',['mL','pH', 'F']], ['07TE', 'Passivation Tank 07', ['PBV', 'Fe', 'F']]]
    # labels = [['11PH','Alodine Tank 11',['pH']],['13TE','Tank 13 Pass Citric',['pH']],['QTPH','Quench Tank',['pH']],['08TE','Alodine Tank 08',['mL','pH', 'F']], ['07TE', 'Passivation Tank 07', ['PBV', 'Fe', 'F']]]
    # labels = [['01TE','Clean Tank 01',['Pct','F']]] #not yet working wait until have 2 data points 
    # labels = [['03TE','Etch Tank 03',['Causticity','Al','F']]]
    # labels = [['05TE', 'Deox Tank 05', ['mL', 'Pct', 'F','g']]]
    # labels = [['07TE', 'Passivation Tank 07', ['PBV', 'Fe', 'F']]]
    # labels = [['08TE','Alodine Tank 08',['mL','pH', 'F']], ['05TE', 'Deox Tank 05', ['mL', 'Pct', 'F','g']]]
    # labels = [['11PH','Alodine Tank 11',['pH']]]
    # labels = [['13TE','Tank 13 Pass Citric',['pH']]]
    labels = [['QTPC','Quench Tank Polymer',['s']]]
    labels = [['QTPH','Quench Tank',['pH']]]

    for label in labels:
        # ic(label)
        mydataset = getdataset(label)
        # ic(mydataset)
        createChart(mydataset)
        


if __name__ == "__main__":
    """For month-end reporting, create a chart for each action code in the labels list. Not set up for weekly or quarterly reporting."""
    main()
    print("done")