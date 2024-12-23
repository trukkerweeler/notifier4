import utils
from datetime import datetime, timedelta
from icecream import ic

def getNoFuture():
    """Goes through tables and returns recurring items w/o future action."""
    sql = f"""SELECT pir.*, pi.INPUT_ID, pi.INPUT_DATE
            FROM quality.PPL_INPT_RCUR pir
            left JOIN (
                SELECT INPUT_ID, INPUT_DATE, USER_DEFINED_2,
                    ROW_NUMBER() OVER (PARTITION BY USER_DEFINED_2 ORDER BY INPUT_DATE DESC) AS rn
                FROM PEOPLE_INPUT
            ) pi ON pir.RECUR_ID = pi.USER_DEFINED_2
            WHERE (pi.rn = 1 or pi.rn is null)
            AND pir.STATUS = 'A';"""
    latestRecurs = utils.getDatabaseData(sql)
    # ic(latestRecurs)
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
                # if null, then add to makeTheseActions
                if rid[7] == None:
                    makeTheseActions.append(rid)
                
                elif rid[7].month <= datetime.today().month and rid[7].year == datetime.today().year:
                    makeTheseActions.append(rid)
    
    return makeTheseActions


def prepareInputRecords(notDones):
    """Prepares PPL_INPT records for insertion, then inserts."""
    # input_date = datetime.today()
    nextMonth = datetime.today() + timedelta(days=32)
    thisMonth = datetime.today()

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
                # Should this be the current month or the next month? 2024-1203
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
                if datetime.today().month < 4:
                    next_quarter = datetime(datetime.today().year, 4, 1)
                elif datetime.today().month < 7:
                    next_quarter = datetime(datetime.today().year, 7, 1)
                elif datetime.today().month < 10:
                    next_quarter = datetime(datetime.today().year, 10, 1)
                else:
                    next_quarter = datetime(datetime.today().year + 1, 1, 1)
                
                startdate = next_quarter
                due_date = next_quarter - timedelta(days=10)
                
                
                

            case "S":
                due_date = datetime.today() + timedelta(weeks=27)
                due_date = due_date.replace(day=1)
                startdate = due_date
                
            case "BE": # Biennially
                intwoyears = datetime.today() + timedelta(days=365*2)
                due_date = intwoyears
                startdate = due_date - timedelta(days=10)
            
            case "H": # Biannually
                # Calculate the first day of the next year
                first_day_next_year = datetime(datetime.today().year + 1, 1, 1)

                # Calculate the first day of next July
                first_day_next_july = datetime(datetime.today().year, 7, 1)
                if datetime.today() >= first_day_next_july:
                    first_day_next_july = datetime(datetime.today().year + 1, 7, 1)

                # Determine which date comes first
                startdate = min(first_day_next_year, first_day_next_july)
                due_date = startdate + timedelta(days=10)
            
        
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
    # print(updateSql)
    utils.updateDatabaseData(updateSql)

    # copy text from recurring item to new input record
    text = utils.getDatabaseData(f"select INPUT_TEXT from PPL_INPT_TEXT where INPUT_ID = '{iid}'")
    formattedaitext = text[0][0]
    formattedaitext = formattedaitext.replace('\\', '\\\\')
    values = (nid, formattedaitext)
    sql = f"insert into PPL_INPT_TEXT values (%s, %s)"
    utils.insertSqlValues(sql, values)


def testformattedaitext(iid):
    sqlGetAiText = f"select INPUT_TEXT from PPL_INPT_TEXT where INPUT_ID = '{iid}'"
    text = utils.getDatabaseData(sqlGetAiText)
    ic(text)    
    formattedaitext = text[0][0]
    print(formattedaitext)
    sqlInsertAiText = f"insert into PPL_INPT_TEXT values (%s, %s), ('{iid}', '{formattedaitext}')"
    print(sqlInsertAiText)


def main():
    """Goes through tables and identifies recurring items w/o future action. Creates PPL_INPT record for those."""
    # print(getNotDones())
    print("Starting recurring action items...")
    notdones = getNoFuture()
    # ic(notdones)
    prepareInputRecords(notdones)
    
    
    # #Need to refactor this in main process...
    # weeklynotdones = []
    # for notdone in notdones:
    #     if notdone[3] == "W" and utils.futureExists(notdone) == False:
    #         weeklynotdones.append(notdone)
    #     else:
    #         print(f"Future action already exists for recurring id: {notdone[0]}")
    
    # if weeklynotdones:
    #     prepareInputRecords(weeklynotdones)
    # print("Done.")
    

if __name__ == '__main__':
    main()
    # testinsertintotext('0000989')
    print("Recurring done.")
    