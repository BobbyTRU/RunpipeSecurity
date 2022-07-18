from msilib import datasizemask
import os
import json
from collections import Counter
import re
from yaml import Loader, Dumper, dump
import yaml
import wrapt
StatisticsDict = []

class Tagged(wrapt.ObjectProxy):
    tag = None

    def __init__(self, tag, wrapped):
        super().__init__(wrapped)
        self.tag = tag

    def __repr__(self):
        return f"{type(self).__name__}({self.tag!r}, {self.__wrapped__!r})"


def construct_undefined(self, node):
    if isinstance(node, yaml.nodes.ScalarNode):
        value = self.construct_scalar(node)
    elif isinstance(node, yaml.nodes.SequenceNode):
        value = self.construct_sequence(node)
    elif isinstance(node, yaml.nodes.MappingNode):
        value = self.construct_mapping(node)
    else:
        assert False, f"unexpected node: {node!r}"
    return Tagged(node.tag, value)


Loader.add_constructor(None, construct_undefined)


allTableFunctions = ["Patch",
                     "Remove",
                     "RemoveIf",
                     "Update",
                     "UpdateIf",
                     "SubmitForm"
                     ]

def findEndOfFunction(myFunction):
    BracketCounter = 0
    results = re.search(r'\w*\(',myFunction)
    if(results):
        firstBracketLocationTuple = results.span()
    else:
        return len(myFunction)
    

    for idx,character in enumerate(myFunction):
        if(idx<firstBracketLocationTuple[1]-1):
            continue
        else:
            if character == "(": 
                BracketCounter = BracketCounter + 1
            if character == ")": 
                BracketCounter = BracketCounter - 1
            if(BracketCounter==0):
                    return idx + 1
            


counter = 0
for name in os.listdir(".\BlobFolder"):
    appID = name.split(" ")[0]
    # print()
    print(appID)
    mainFolder = ".\BlobFolder\\"+appID+" folder\\"
    workingFolder = mainFolder + appID+" unpacked\\"

    toOpen = "CanvasManifest.json"
    if(len(os.listdir(workingFolder)) > 0):
        f = open(workingFolder + toOpen, encoding='utf8')
        data = json.load(f)
        screens = data["ScreenOrder"]
        screens.append("App")
    dataSourceFolder = workingFolder+"DataSources"
    dataSourcesList = []
    if(os.path.isdir(dataSourceFolder)):
        if(os.path.isdir(dataSourceFolder)):
            for dataSource in os.listdir(dataSourceFolder):
                dataSourceName = dataSource.split(".")[0]
                dataSourceObject = {
                    "dataSourceName": dataSourceName,
                    "usedWithFunction":[]
                }
                isBeingUsed = False
                for screen in screens:
                    toOpen = "Src\\" + screen + ".fx.yaml"
                    try:
                        stream = open(workingFolder + toOpen,
                                      'r', encoding="utf8")
                    except:
                        for filename in os.listdir(workingFolder + "Src"):
                            myFileName = screen
                            allMatches = re.findall(r'%.{2}', myFileName)
                            for el in allMatches:
                                mySpan = re.finditer(r'%.{2}', myFileName).__next__().span()
                                newlist = (str(mySpan).replace("(", "").replace(")", "").split(","))
                                firstIdx = int(newlist[0])
                                scndIdx = int(newlist[1])
                                specialEl = myFileName[firstIdx:scndIdx].replace("%", "")
                                myFileName = chr(int(specialEl, 16)).join([myFileName[:firstIdx], myFileName[scndIdx:]])
                            if(screen == myFileName):
                                screen = filename.replace(".fx.yaml", "")
                                toOpen = "Src\\" + screen + ".fx.yaml"
                                stream = open(workingFolder +toOpen, 'r', encoding="utf8")
                                break

                    screenFileAsString = stream.read()
                    newFileAsString = []
                    isPartOfCommentBlock = False
                    for line in screenFileAsString.split(r'\n\n\s{4}'):
                        #remove comments somehow
                        if(isPartOfCommentBlock):
                            continue
                        elif(line.startswith("//")):
                            continue
                        elif("/*" in line):
                            isPartOfCommentBlock = True
                            continue
                        elif("*/" in line):
                            isPartOfCommentBlock = False
                            continue
                        else:
                            newFileAsString.append(line)


                        # if("/*" in line):
                        #     #remove that line

                        # if("//" in line or "/*" in line):
                        #     #remove everything after // and remove everthing between /* and */
                        # print(line.replace(r'\n\n\s{4}',""))
                    
                    with open('./'+mainFolder+screen+'fileAsString.txt', 'w') as json_file:
                        json.dump(screenFileAsString, json_file)
                    
                    with open('./'+mainFolder+screen+'newFileAsString.txt', 'w') as json_file:
                        json.dump(newFileAsString, json_file)   
                    
                    exit()

                    if("@"+dataSourceName in screenFileAsString or dataSourceName in screenFileAsString):
                        isBeingUsed = True
                        for function in allTableFunctions:
                            if(function in screenFileAsString):
                                StatisticsDict.append(function)
                                # print(screenFileAsString)
                                screenFileWithNoBreaks = screenFileAsString.replace("\n","")

                                stuff = re.findall(r''+function+r'\(.*\)',screenFileWithNoBreaks)
                                # print(screen)
                                for i in stuff:
                                    
                                    print(function)
                                    endIdx = findEndOfFunction(i)
                                    dataSourceUsedInFunction = i[0:endIdx].replace("\n","").replace(" ","")
                                    justDataSource = dataSourceUsedInFunction.split(",")[0].split("(")[1]
                                    print(justDataSource)

                                counter += 1
                                if(counter == 10):
                                    exit()

                                dataSourceObject["usedWithFunction"].append(function)
                
                dataSourceObject["isBeingUsed"] = str(isBeingUsed)
                dataSourcesList.append(dataSourceObject)
            
            with open('./'+mainFolder+'DataSourceSummary.json', 'w') as json_file:
                json.dump(dataSourcesList, json_file)



stats = Counter(StatisticsDict)
stats = json.dumps(stats)
stats = json.loads(stats)
stats = sorted(stats.items(), key=lambda kv:(kv[1], kv[0]))
for val in stats:
    print(val)

