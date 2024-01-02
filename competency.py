import utils
from datetime import datetime, timedelta

def main():
    """Goes through tables and identifies overdue items. Sends email to appropriate people."""
    # Training==================================================
    sql2 = """SELECT COURSE_ID, PEOPLE_ID, EXPIRATION_DATE
            FROM (
            SELECT *, ROW_NUMBER() OVER (PARTITION BY COURSE_ID ORDER BY EXPIRATION_DATE DESC) AS rn
            FROM CTA_ATTENDANCE
            ) AS sub
            WHERE rn = 1 and EXPIRATION_DATE is not null;"""

    overDueTraining = utils.getDatabaseData(sql2)
    
    for training in overDueTraining:
        if training[2] < datetime.today():
            notification = '''This person's training expired on %s. Please review and take appropriate action. \nTraining id: %s, name: %s''' % (training[2], training[0], training[1])        
            utils.sendMail(to_email=["tim.kent@ci-aviation.com"], subject="Overdue Training", message=notification)


if __name__ == '__main__':
    main()
    print("Competency, Done.")