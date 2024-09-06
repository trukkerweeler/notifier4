import utils
from datetime import datetime, timedelta

def getNotDones():
    """Goes through tables and returns recurring items w/o future action."""
    # sql = """select USER_DEFINED_2 from quality.PPL_INPT_RCUR pir left join PEOPLE_INPUT pi on pir.RECUR_ID = pi.USER_DEFINED_2 
    #         where CLOSED = 'N' and pi.DUE_DATE > LAST_DAY(CURRENT_DATE())"""
    # sql = """select USER_DEFINED_2, FREQUENCY, DUE_DATE from quality.PPL_INPT_RCUR pir left join PEOPLE_INPUT pi on pir.RECUR_ID = pi.USER_DEFINED_2 
    #         where CLOSED = 'N' and pi.DUE_DATE > LAST_DAY(CURRENT_DATE())"""
    sql = """select USER_DEFINED_2, FREQUENCY, DUE_DATE from quality.PPL_INPT_RCUR pir left join PEOPLE_INPUT pi on pir.RECUR_ID = pi.USER_DEFINED_2 
            where CLOSED = 'N' and pi.DUE_DATE > CURRENT_DATE()"""
    alreadyDone = utils.getDatabaseData(sql)
    done = []
    notDone = []
    for rid in alreadyDone:
        done.append(rid[0])
    recurrers = utils.getDatabaseData("select * from PPL_INPT_RCUR")
    for row in recurrers:
        if row[0] in done:
            print(f"Future action already exists: {row[0]}")
        else:
            notDone.append(row)
            print(f"Not done: {row[0]}")
    
    return notDone


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
    print("Starting recurring action items...")
    notdones = getNotDones()
    # print(notdones)
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