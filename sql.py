import utils

# sql = "update CORRECTIVE set CLOSED_DATE = current_date(), CLOSED = 'Y' where CORRECTIVE_ID = '0001219'"
caid = "0001219"
actionby = "TKENT"

#Correction
correction = (f'The quench tank pH was measured and found within limits.')
correctionSql = f"update CORRECTION set CORRECTION_DATE = current_date(), ACTION_BY = '{actionby}', CORRECTION_TEXT = '{correction}' where CORRECTIVE_ID = '{caid}'" 
print(correctionSql)
utils.updateDatabaseData(correctionSql)