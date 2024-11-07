import utils
from datetime import datetime, timedelta

def getNotDones():
    """Goes through tables and returns recurring items w/o future action."""
    sql = f"""SELECT pir.*, pi.INPUT_ID, pi.INPUT_DATE
            FROM quality.PPL_INPT_RCUR pir
            JOIN (
                SELECT INPUT_ID, INPUT_DATE, USER_DEFINED_2,
                    ROW_NUMBER() OVER (PARTITION BY USER_DEFINED_2 ORDER BY INPUT_DATE DESC) AS rn
                FROM PEOPLE_INPUT
            ) pi ON pir.RECUR_ID = pi.USER_DEFINED_2
            WHERE pi.rn = 1
            AND pir.STATUS = 'A';"""
    latestRecurs = utils.getDatabaseData(sql)
    # print(latestRecurs)
    done = []
    makeTheseActions = []
    thisWeekNumber = datetime.today().isocalendar()[1]
    print(f"This week number: {thisWeekNumber}")
    for rid in latestRecurs:
        done.append(rid[0])
        match rid[3]:
            case "W":
                # if the INPUT_DATE week number is less this week number, then add to makeTheseActions
                if rid[7].isocalendar()[1] < thisWeekNumber and rid[7].year == datetime.today().year:
                    makeTheseActions.append(rid)
            case _:
                if rid[7].month < datetime.today().month and rid[7].year == datetime.today().year:
                    makeTheseActions.append(rid)
    
    return makeTheseActions


def prepareInputRecords(notDones):
    """Prepares PPL_INPT records for insertion, then inserts."""
    # input_date = datetime.today()
    nextMonth = datetime.today() + timedelta(days=32)

    for notDone in notDones:
        rid = notDone[0]
        iid = notDone[1]
        assto = notDone[2]
        frequency = notDone[3]
        subject = notDone[4]
        projectid = utils.getProjectId(iid)
        startdate = datetime.today().strftime('%Y-%m-%d')

        #determine due date
        match frequency:
            case "W":
                due_date = datetime.today() + timedelta(days=7)
                #get the first day of next week
                fdonw = datetime.today() + timedelta(days=7) 
                fdonw = fdonw - timedelta(days=fdonw.weekday())
                startdate = fdonw.strftime('%Y-%m-%d')
                due_date = fdonw + timedelta(days=5)
                due_date = due_date.strftime('%Y-%m-%d')
                if subject == "QTPC":
                    if utils.week_of_month(startdate) > 1:
                        assto = "OGOLUBOVIC"

            # Annually
            case "A":
                due_date = datetime.today() + timedelta(days=365)
                due_date = due_date.replace(day=1)
                startdate = due_date - timedelta(days=10)

            # Monthly
            case "M": 
                # nextMonth = datetime.today() + timedelta(days=32)
                due_date = nextMonth.replace(day=1)
                fdonm = nextMonth.replace(day=1)    
                startdate = fdonm
            
            # Every other month (Copilot says bimonthly)     
            case "O":
                due_date = datetime.today() + timedelta(weeks=8)
                due_date = due_date.replace(day=1)
                startdate = due_date

            # Quarterly
            case "Q":
                due_date = datetime.today() + timedelta(weeks=12)
                due_date = due_date.replace(day=1)
                startdate = due_date            

            case "S":
                due_date = datetime.today() + timedelta(weeks=27)
                due_date = due_date.replace(day=1)
                startdate = due_date
                
            case "BE":
                intwoyears = datetime.today() + timedelta(days=365*2)
                due_date = intwoyears
                startdate = due_date - timedelta(days=10)
            
        
        insertRecurringRecord(startdate, due_date, subject, assto, projectid, rid, iid)
        

def insertRecurringRecord(startdate, duedate, subject, assto, projectid, rid, iid):
    """Inserts a recurring record into PPL_INPT_RCUR."""
    nid = utils.getNextSysid("INPUT_ID")
    updateSql = (f"insert into PEOPLE_INPUT (INPUT_ID"
        ", INPUT_DATE"
        ", PEOPLE_ID"
        ", INPUT_TYPE"
        ", SUBJECT"
        ", ASSIGNED_TO"
        ", DUE_DATE"
        ", CLOSED"
        ", PROJECT_ID"
        ", USER_DEFINED_2"
        ", CREATE_BY"
        ", CREATE_DATE) values ("
        "'{nid}'"
        ", '{date}'"
        ", 'TKENT'"
        ", 'DATA'"
        ", '{subject}'"
        ", '{assto}'"
        ", '{duedate}'"
        ", 'N'"
        ", '{projectid}'"
        ", '{rid}'"
        ", 'RCUR'"
        ", NOW() )".format(nid=nid, date=startdate, duedate=duedate, subject=subject, assto=assto, projectid=projectid, rid=rid))
    print(updateSql)
    utils.updateDatabaseData(updateSql)

    # copy text from recurring item to new input record
    text = utils.getDatabaseData(f"select INPUT_TEXT from PPL_INPT_TEXT where INPUT_ID = '{iid}'")
    text = text[0][0]
    text = text.replace("'", "\\'")
    updateSql = f"insert into PPL_INPT_TEXT values ('{nid}', '{text}')"
    utils.updateDatabaseData(updateSql)


def main():
    """Goes through tables and identifies recurring items w/o future action. Creates PPL_INPT record for those."""
    # print(getNotDones())
    # print("Starting recurring action items...")
    notdones = getNotDones()
    print(notdones)
    # prepareInputRecords(notdones)
    

if __name__ == '__main__':
    main()