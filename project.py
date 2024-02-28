import utils
import datetime as dt

def main(person):
    """Goes through tables and identifies overdue items. Sends email for each project to assignee with open actions."""
    personprojectswithopenactions = utils.getDatabaseData(f"select distinct PROJECT_ID from PEOPLE_INPUT where ASSIGNED_TO = '{person}' and CLOSED = 'N' and PROJECT_ID is not null")
    # print(personprojectswithopenactions)
    for project in personprojectswithopenactions:
        print(f"---project---")
        print(project)
        thisprojectopenactions = utils.getDatabaseData(
            f"""select pi.INPUT_ID, SUBJECT, ASSIGNED_TO, pi.PROJECT_ID, p.NAME, pit.INPUT_TEXT, pi.INPUT_DATE, pi.DUE_DATE 
            from PEOPLE_INPUT pi left join PROJECT p on pi.PROJECT_ID = p.PROJECT_ID left join PPL_INPT_TEXT pit on pi.INPUT_ID = pit.INPUT_ID
            where ASSIGNED_TO = '{person}' and pi.CLOSED = 'N' and pi.PROJECT_ID = '{project[0]}' and pi.DUE_DATE < date_add(NOW(), interval 6 day)
            and INPUT_DATE > NOW() order by pi.DUE_DATE asc""")
        print(f"---actions---")
        if thisprojectopenactions:
            print(thisprojectopenactions[0])
            print(len(thisprojectopenactions))
            # eaddress = "tim.kent@ci-aviation.com"
            eaddress = utils.emailAddress(person)
            if thisprojectopenactions[0][4] is None:
                emailsubject = "Open Actions - No project"
            else:
                emailsubject = "Open Actions - " + thisprojectopenactions[0][4]
            emessage = ""
            if len(thisprojectopenactions) > 0:
                for action in thisprojectopenactions:
                    emessage += f"\n\nAction ID: {action[0]}\nRequest date: {action[6]}\nDue date: {action[7]}\nAction text:\n{action[5]}"
            
                # emessage += '\n\nIf any of these actions are complete, please close them out in the system.'
                emessage += '\n\nIf any of these actions are complete, please tell the QA Manager.'
                utils.sendMail(eaddress, subject=emailsubject, message=emessage)


if __name__ == "__main__":
    # test = 1
    print("Starting project/person emailer...")
    lastsentweek = utils.WeekLastSent('project')
    # print(f"Last sent week: {lastsentweek}")
    runtimeweek = dt.datetime.today()
    # get the week number of the year
    runtime = runtimeweek.isocalendar()[1]
    # print(f"Current week of year: {runtime}")
    
    if lastsentweek < runtime:
        main('CHARRISON')
        main('MTIPPETTS')
        main('RMATSAMAS')
        utils.setLastSentFile('project')
    else:
        print("Not sending person/project email, too soon or off-hours. Last week: " + str(lastsentweek) + " Current week: " + str(runtime))
        # if test == 1:
        #     main('CHARRISON')

    
    print("Done.")
    
