from asyncio.windows_events import NULL
import json
import pyodbc
import os 
import time
import config
server = 'runpipe.database.windows.net'
database = 'runpipe-dev-tenant'
username = config.username
password = config.password
driver= '{SQL Server}' 

def writeToDB():
    start = time.time()
    with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+',1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
        with conn.cursor() as cursor:
            for name in os.listdir(".\BlobFolder"):
                mainJson = {
                    "WarnIssueSummary":{},
                    "ConnectorSummary":{}
                }
                appID = name.split(" ")[0].split(".msapp")[0]
                if(os.path.exists("./BlobFolder/" + name + "/WarnIssueSummaryResult.json")):
                    f = open("./BlobFolder/" + name + "/WarnIssueSummaryResult.json")
                    mainJson["WarnIssueSummary"] = json.load(f)
                    # data = "NULL"
                if(os.path.exists("./BlobFolder/" + name + "/ConnectorSummary.json")):
                    f = open("./BlobFolder/" + name + "/ConnectorSummary.json")
                    mainJson["ConnectorSummary"]  = json.load(f)
                    # data = "NULL"
                cursor.execute("UPDATE [dbo].[ProjectItems] SET [WarnIssueSummarizer] = ? WHERE [PpItemId] = ?", json.dumps(mainJson), appID)
                conn.commit()
    end = time.time()
    dif = end - start
    print("writing to DB took:", dif,"s")
    return dif
    
writeToDB()
