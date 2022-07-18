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

def generateCFG(appID):
    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    workingFolder = mainFolder + appID+" unpacked\\"
    toOpen = "CanvasManifest.json"
    if(len(os.listdir(workingFolder))>0):
        f = open(workingFolder + toOpen,encoding='utf8')
        data = json.load(f)
        screens = data["ScreenOrder"]
        screens.append("App")
        for screen in screens:
            toOpen = "Src\\" + screen + ".fx.yaml" 
            try:
                stream = open(workingFolder + toOpen, 'r',encoding="utf8")
            except:
                for filename in os.listdir(workingFolder + "Src"):
                    myFileName = screen
                    allMatches = re.findall(r'%.{2}', myFileName)
                    for el in allMatches:
                        mySpan = re.finditer(r'%.{2}', myFileName).__next__().span()
                        newlist = (str(mySpan).replace("(","").replace(")","").split(","))
                        firstIdx = int(newlist[0])
                        scndIdx = int(newlist[1])
                        specialEl = myFileName[firstIdx:scndIdx].replace("%","")
                        myFileName =  chr(int(specialEl, 16)).join([myFileName[:firstIdx],myFileName[scndIdx:]]) 
                    if(screen == myFileName):
                        screen = filename.replace(".fx.yaml","")
                        toOpen = "Src\\" + screen + ".fx.yaml" 
                        stream = open(workingFolder + toOpen, 'r',encoding="utf8")
                        break
            try:
                parsed_yaml=yaml.load(stream,Loader=Loader )
                

                # except yaml.YAMLError as exc:
            except Exception as e:
                print(appID, "yaml failed", e)
                continue

            print(parsed_yaml)
            exit()


counter = 0
for name in os.listdir(".\BlobFolder"):
    appID = name.split(" ")[0]
    # generateCFG(appID)
    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    workingFolder = mainFolder + appID+" unpacked\\"
    # toOpen = "Connections\Connections.json"
    # if(len(os.listdir(workingFolder))>0):
    #     f = open(workingFolder + toOpen,encoding='utf8')
    #     data = json.load(f)
     

    # for i in data:
    #     for j in data[i]:
    #         if("connectionRef" in j):
    #             connectionType = data[i][j]["id"].split("/")[-1]
    #             StatisticsDict.append(connectionType)
    #             # check which datasource is being used
    
    # for element in StatisticsDict:
    #     print("tew")

    toOpen = "CanvasManifest.json"
    if(len(os.listdir(workingFolder))>0):
        f = open(workingFolder + toOpen,encoding='utf8')
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
                    "dataSourceName":dataSourceName
                }
                isBeingUsed = False
                for screen in screens:
                    print(screen)
                    toOpen = "Src\\" + screen + ".fx.yaml" 
                    try:
                        stream = open(workingFolder + toOpen, 'r',encoding="utf8")
                    except:
                        for filename in os.listdir(workingFolder + "Src"):
                            myFileName = screen
                            allMatches = re.findall(r'%.{2}', myFileName)
                            for el in allMatches:
                                mySpan = re.finditer(r'%.{2}', myFileName).__next__().span()
                                newlist = (str(mySpan).replace("(","").replace(")","").split(","))
                                firstIdx = int(newlist[0])
                                scndIdx = int(newlist[1])
                                specialEl = myFileName[firstIdx:scndIdx].replace("%","")
                                myFileName =  chr(int(specialEl, 16)).join([myFileName[:firstIdx],myFileName[scndIdx:]]) 
                            if(screen == myFileName):
                                screen = filename.replace(".fx.yaml","")
                                toOpen = "Src\\" + screen + ".fx.yaml" 
                                stream = open(workingFolder + toOpen, 'r',encoding="utf8")
                                
                                break

                    screenFileAsString = stream.read()
                    if("@"+dataSourceName in screenFileAsString or dataSourceName in screenFileAsString):
                        isBeingUsed = True
                
                dataSourceObject["isBeingUsed"] = str(isBeingUsed)
                dataSourcesList.append(dataSourceObject)
            with open('./'+mainFolder+'DataSourceSummary.json', 'w') as json_file:
                json.dump(dataSourcesList, json_file)
            exit()
            
            
    # for each file in DataSources check if @DataSource is being used in any of the screens
    
                
                    
                        
                    # f = open(workingFolder+"Src\\"+screenFile)
                # exit()

    
        


stats = Counter(StatisticsDict)
stats = json.dumps(stats)
stats = json.loads(stats)
for idx,val in enumerate(stats):
    print(val,stats[val])


#for each power app
#for each datasource check each screen if its being used there
