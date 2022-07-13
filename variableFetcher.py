
from staticfg import CFGBuilder
import json 
import re 



cfg = CFGBuilder().build_from_file('test.py', './test.py')

# cfg.build_visual('exampleCFG', 'pdf')


sourceCodeArray = []    

for i in cfg.__iter__():
    sourceCodeArray.append((i.get_source().split("\n")[:-1],i.at()))

# print(sourceCodeArray)
with open("cfgGraph.json", "r") as read_file:
    data = json.load(read_file)

individualLines = data["objects"]


functionArray = []
declarationArray = []
comparisonArray = []

declarationPattern = r'=|\+=|-='
comparisonPattern = r'==|!=|<|>|>=|<=|'



for i in individualLines:
    if ("nodes" in i):
        functionArray.append(i)
    if("=" in i["label"]):
        linesOfCode = (i["label"].split("\n")[:-1])
        for line in linesOfCode:
            z = re.search(declarationPattern,line)
            if(z):
                declarationArray.append((line,i["_gvid"]))
            z = re.search(comparisonPattern,line)
            if(z):
                comparisonArray.append((line,i["_gvid"]))
        

declarationList = []

for sourceCodeLine in sourceCodeArray:
    value,lineNumber =  sourceCodeLine
    for idx,val in enumerate(declarationArray):
        if(declarationArray[idx][0] in value):
            tempDict = {
                "code":declarationArray[idx][0],
                "node":declarationArray[idx][1],
                "codeLine":lineNumber
            }
            declarationList.append(tempDict)

for idx,val in enumerate(declarationList):
    print(val)