# -*- coding: utf-8 -*-
from importlib.metadata import files
import os
from os import path
import json
import re
from sqlite3 import connect
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
    myList = getConnectorList(appID)
    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    allConnectors = []
    for connector in myList:
        connectorDict = {
            "Name": connector,
            "FunctionsUsed":[],
            "Type":""
        }
    
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
                datalines = stream.readlines()                    
                for line in datalines:
                    if(connector in line):
                        myFindings = re.findall(r""+re.escape(connector)+r".*?\(",line)
                        for finding in myFindings:
                            functionName = finding.split(".")[1].replace("(","")
                            if(not functionName in connectorDict["FunctionsUsed"]):
                                    connectorDict["FunctionsUsed"].append(functionName)      
                            
        allConnectors.append(connectorDict)     
            
            
               
    filename = mainFolder + 'ConnectorSummary.json'

    with open(filename, 'w') as fp:
        json.dump(allConnectors, fp)                    