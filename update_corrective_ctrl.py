import os
from dotenv import load_dotenv

load_dotenv()


def main():
    """update corrective ctrl from csv file."""
    import mysql.connector
    from mysql.connector import Error
    try:
        connection = mysql.connector.connect(host=os.getenv('DB_HOST'),
                                             database=os.getenv('DB_NAME'),
                                             user=os.getenv('DB_USER'),
                                             password=os.getenv('DB_PASS'))
        if connection.is_connected():
            cursor = connection.cursor()
            # open csv file
            with open("CC_2023-0911.csv", "r") as f:
                lines = f.readlines()
            # print(lines)
            # print(len(lines))
            # print(lines[0])
                for line in lines:
                    print(line)
                    if len(line.split(",")) > 1:
                        caid = line.split(",")[0]
                        print(caid)
                        controlText = line.split(",")[1]
                        
                        print(controlText)
                        sql = 'UPDATE CORRECTIVE_CTRL SET CONTROL_TEXT = %s WHERE CORRECTIVE_ID = %s;'
                        # print(sql)
                        # cursor.execute(sql, (controlText, caid))
                        # connection.commit()
                        # print(f"Inserted into CORRECTIVE_CTRL")
                        if len(line.split(",")) > 6:
                            causeText = line.split(",")[6]
                            sql = 'UPDATE CORRECTIVE_CTRL SET CAUSE_TEXT = %s WHERE CORRECTIVE_ID = %s;'
                            print(sql)
                            cursor.execute(sql, (causeText, caid))
                            connection.commit()
                            # print(f"Inserted into CORRECTIVE_CTRL")

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()


if __name__ == "__main__":
    main()
    print("Done.")