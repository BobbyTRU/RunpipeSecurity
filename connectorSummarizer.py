# -*- coding: utf-8 -*-
from importlib.metadata import files
import os
from os import path
import json
import re
import wrapt
from yaml import Loader 
import yaml

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

def getConnectorList(appID):
    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    workingFolder = mainFolder + appID+" unpacked\\"
    wadlFolder = workingFolder + "pkgs\\Wadl"
    connectorList = []
    if os.path.exists(wadlFolder):
        for filename in os.listdir(wadlFolder):
            connectorList.append(filename.replace(".xml",""))

    return connectorList

for name in os.listdir(".\BlobFolder"):
    appID = name.split(" ")[0]
    appID = "d38f485a-5a36-4ce2-a4cb-35a9ff2c29da.msapp"

    myList = getConnectorList(appID)

    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    workingFolder = mainFolder + appID+" unpacked\\"
    toOpen = "CanvasManifest.json"
    if(len(os.listdir(workingFolder))>0):
        f = open(workingFolder + toOpen,encoding='utf8')
        data = json.load(f)
        screens = data["ScreenOrder"]
        screens.append("App")
        mainJson = {
            "allSummaries":[]
        }
        for screen in screens: 
            screenSummary = {
                "screenName" : screen,
                "ConnectorsUsed":[]
            }
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

            datalines = stream.readlines()     
            for element in myList:
                connectorSummary = {
                    "ConnectorName":element,
                    "FunctionsUsed":[
                    ]
                }
                
                for line in datalines:
                    findings = re.findall(rf'{element}',line)
                    if(element in line):
                        
                        myFindings = re.findall(r""+re.escape(element)+r".*?\(",line)
                        for finding in myFindings:
                            functionName = finding.split(".")[1].replace("(","")
                            usedFunction = {
                                    "FunctionName":functionName,
                                    "Counter": 1
                                }
                            if(connectorSummary["FunctionsUsed"]):
                                #check here if there is already an element with the function and add a 
                                for functionDict in connectorSummary["FunctionsUsed"]:
                                    if(functionDict["FunctionName"] == functionName):
                                        functionDict["Counter"] = functionDict["Counter"] + 1
                                    else:   
                                        connectorSummary["FunctionsUsed"].append(usedFunction)
                            else:
                                connectorSummary["FunctionsUsed"].append(usedFunction)
                            
                
                if(connectorSummary["FunctionsUsed"]):
                    screenSummary["ConnectorsUsed"].append(connectorSummary)
                
            mainJson["allSummaries"].append(screenSummary)


        filename = mainFolder + 'ConnectorSummary.json'

        totalJson = {
            "connectorsUsed":[]
        }

        connectorJson = {
            "ConnectorName": "",
            "FunctionsUsed":[]
        }



        exit()


            

        with open(filename, 'w') as fp:
            json.dump(mainJson, fp)
                    