import json
import time
import os
import shutil


def summarize():
    start = time.time()
    for name in os.listdir(".\BlobFolder"):
        folderPathName = "./BlobFolder/" + name + "/"
        pathName = folderPathName + name.split(" ")[0] + " unpacked" + "/Entropy/"
        if(os.path.exists(pathName + "AppCheckerResult.sarif")):
            shutil.copyfile(pathName + "AppCheckerResult.sarif", pathName + "AppCheckerResult.json")
            f = open(pathName + "AppCheckerResult.json")


            data = json.load(f)
            warningIssueDict = {
                "accessibility": {
                    "High": 0,
                    "Medium": 0,
                    "Low": 0
                },
                "performance": {
                    "High": 0,
                    "Medium": 0,
                    "Low": 0
                },
                "formula": {
                    "High": 0,
                    "Medium": 0,
                    "Low": 0
                }
            }


            rulesObj = data["runs"][0]["tool"]["driver"]["rules"]
            ruleCount = len(rulesObj)


            w, h = 4, ruleCount+1
            Matrix = [[0 for x in range(w)] for y in range(h)]
            Matrix[0][0] = "name"
            Matrix[0][1] = "level"
            Matrix[0][2] = "category"
            Matrix[0][3] = "count"

            # get primary cat and level

            counter = 1
            for val in rulesObj:
                Matrix[counter][0] = val["id"]
                Matrix[counter][1] = val["properties"]["level"]
                Matrix[counter][2] = val["properties"]["primaryCategory"]
                counter += 1

            # print(Matrix)
                # if(i["properties"]["primaryCategory"] not in counterDict):
                #     counterDict.append()


            for rule in Matrix:
                for result in data["runs"][0]["results"]:
                    if(result["ruleId"] == rule[0]):
                        rule[3] += 1

            for category in warningIssueDict:
                # print(warningIssueDict[category])
                for rule in Matrix:
                    if(rule[2] == category):
                        if(rule[1] == "High"):
                            warningIssueDict[category]["High"] = warningIssueDict[category]["High"]+rule[3]
                        if(rule[1] == "Medium"):
                            warningIssueDict[category]["Medium"] = warningIssueDict[category]["Medium"]+rule[3]
                        if(rule[1] == "Low"):
                            warningIssueDict[category]["Low"] = warningIssueDict[category]["Low"]+rule[3]

            with open(folderPathName + 'WarnIssueSummaryResult.json', 'w') as fp:
                json.dump(warningIssueDict, fp)
    end = time.time()
    dif = end - start
    print("creating WarnIssueJSON took:",dif,"s")
    return dif


def getAdditionalInfo():
    print("nothing")
    # for j in data["runs"][0]["results"]:
    #     print(j["locations"][0]["properties"]["type"])
    #     print(j["properties"]["level"])
    #     print(j["ruleId"])
    #     print(j["ruleIndex"])
    #     print("")

    # Get Rules definition
    # for i in data["runs"][0]["tool"]["driver"]["rules"]:
    #     print(i["id"])
    #     print(i["messageStrings"]["issue"]["text"])
    #     print(i["properties"]["howToFix"][0])
    #     print(i["properties"]["level"])
    #     print(i["properties"]["primaryCategory"])
    #     print(i["properties"]["whyFix"])
    #     print("")

