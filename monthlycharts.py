import matplotlib.pyplot as plt
import pandas as pd
import utils
import re
from datetime import datetime

def createChart(data, label, units):
    """Creates a chart from the given data and saves it as a PDF."""
    # Create the chart
    plt.plot(data[0], data[1])
    # plt.xlabel('Month')
    plt.ylabel(units)
    # plt.title('Trend of ' + units + ' in ' + label[1])
    plt.title(label + ' Trend')
    filedate = utils.sixdigitdate(datetime.today())

    # Save the chart as a PDF
    match label:
        case 'Tank 11':
            base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Chem Film\Tank11 - Type2'
            ph11path = base + f'\\{filedate}_pH-Trend.pdf'
            plt.savefig(ph11path, format='pdf')
        case 'Tank 13':
            base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Passivation\Tank13 - Passivation-Citric'
            ph13path = base + f'\\{filedate}_pH-Trend.pdf'
            plt.savefig(ph13path, format='pdf')
        case 'Quench Tank':
            base = r'K:\Quality - Records\8512 - Validation and Control of Special Processes\Heat Treat\Quench Tank'
            quenchpath = base + f'\\{filedate}_QTPC-Trend.pdf'
            plt.savefig(quenchpath, format='pdf')
        case _:
            print("No match for saving Trend PDF.")
            plt.show()


    # Show the chart (optional)
    # plt.show()

    # Close the chart
    plt.close()


def getdataset(actioncode):
    """Returns a dataset for the given action code."""
    sql = f'''with myalias as (SELECT pir.*, pi.CREATE_DATE FROM PPL_INPT_RSPN pir inner join PEOPLE_INPUT pi on pir.INPUT_ID = pi.INPUT_ID 
    where pi.SUBJECT = '{actioncode[0]}' and pi.CLOSED = 'Y' and CREATE_DATE > '2023-11-01'order by CREATE_DATE desc limit 12 ) select * from myalias order by CREATE_DATE asc;'''
    mydata = utils.getDatabaseData(sql)
    print(mydata)
    myset = []
    myvalues = []
    mymonths = []
    for i in range(len(mydata)):
        valueonly = -1
        yyyymm = re.search(r'(\d+.\d+)', mydata[i][1])
        if yyyymm:
            yearmonth = yyyymm.group(0)
            monthonly = yearmonth[5:]
            # convert 2-digit month to 3-letter month            
            if monthonly == '01':
                monthonly = 'Jan-' + yearmonth[2:4]
            elif monthonly == '02':
                monthonly = 'Feb'
            elif monthonly == '03':                    
                monthonly = 'Mar'
            elif monthonly == '04':
                monthonly = 'Apr'
            elif monthonly == '05':                    
                monthonly = 'May'
            elif monthonly == '06':
                monthonly = 'Jun'
            elif monthonly == '07':
                monthonly = 'Jul'
            elif monthonly == '08':
                monthonly = 'Aug'
            elif monthonly == '09':
                monthonly = 'Sep'
            elif monthonly == '10':
                monthonly = 'Oct'
            elif monthonly == '11':
                monthonly = 'Nov'
            elif monthonly == '12':
                monthonly = 'Dec'
            # print(monthonly)
            pass
            mymonths.append(monthonly)
        else:
            print("No match")
        pH = re.search(r'([0-9]\.[0-9]{1,2}[ ]*(pH|s))', mydata[i][1])
        # if pH:
        #     # print(pH.group(0))
        #     # print(f"i am ph: '{pH.group(0)}'")
        #     valueonly = pH.group(0)
        #     valueonly = re.sub(r'pH', '', valueonly)
        #     valueonly = re.sub(r's', '', valueonly)
        #     try:
        #         valueonly = float(valueonly)
        #     except:
        #         print("No match valueonly")
        #     myvalues.append(valueonly)

        # else:
        #     # print("No match loose")
        #     # print(mydata[i][0])
        #     pHobject = re.search(r'(\{.*\})', mydata[i][1])
        #     if pHobject:
        #         # print(pHobject.group(0))
        #         # convert it to a dictionary
        #         mydict = eval(pHobject.group(0))
        #         myvalues.append(float(mydict[actioncode[2]]))
        #     else:
        #         print("No match object")
        
    # myset.append(mymonths)
    # myset.append(myvalues)
    # return myset


def main():
    labels = [['08TE','Alodine Tank','mult']]
    # labels = [['11PH','Tank 11','pH'],['13TE','Tank 13','pH'],['QTPH','Quench Tank','pH'],['08TE','Alodine Tank','mult']]
    for label in labels:
        mydataset = getdataset(label)
        print(mydataset)
        createChart(mydataset, label[1], label[2])


if __name__ == "__main__":
    """For month-end reporting, create a chart for each action code in the labels list. Not set up for weekly or quarterly reporting."""
    main()
    print("done")