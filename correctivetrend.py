import pandas as pd

import matplotlib.pyplot as plt
import utils

def getcorrectivedata():
    sql = "SELECT * FROM CORRECTIVE where CORRECTIVE_DATE between NOW() - INTERVAL 1 YEAR AND NOW() ORDER BY CORRECTIVE_ID DESC;"
    data = utils.getDatabaseData(sql)
    return data


def getcorrectivetrend():
    # group by month
    data = getcorrectivedata()
    for row in data:
        correctivedate = row[14].strftime('%Y-%m')
        closeddate = row[20].strftime('%Y-%m')
        
    df = pd.DataFrame(data)
    df[14] = pd.to_datetime(df[14])
    df = df.groupby(df[14]).size()
    df.plot()
    plt.show()
    return df


if __name__ == "__main__":
    # data = getcorrectivedata()
    # print(data)
    getcorrectivetrend()