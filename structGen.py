import json
import os
import yaml
import re
import time
import wrapt
from yaml import Loader 
# -*- coding: utf-8 -*-
pattern = r'\bOn[a-zA-Z]+'


start = time.time() 

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

def findEndOfFunction(functionIndicator,myFunction):
    BracketCounter = 0
    firstIfLocationTuple = re.search(r''+functionIndicator+r'',myFunction).span()
    for idx,character in enumerate(myFunction):
        if(idx<firstIfLocationTuple[1]):
            continue
        else:
            if character == "(": BracketCounter = BracketCounter + 1
            if character == ")": BracketCounter = BracketCounter - 1
            
            if(BracketCounter==0):
                return idx


def removeComments(codeString):
    #remove multiline comments
   
    codeString= re.sub(r'\/\*[\S\s]+?\*\/',"",codeString)

    #split at every newline
    codeString = codeString.split("\n")
    #list where the non-comment lines will be stored
    newString = []
    for line in codeString:
        if("//" in line):
            """
            partition splits the string
            head is before the seperator
            sep is the seperator (in this case //)
            tail is the string following the seperator
            """
            head, sep, tail = line.partition("//")
            # isspace should be sufficient but did not work, therefore the additional check with ascii encoding
            # if there is any actual code before the comment, add it to the list
            if(not head.encode("ascii") == b''):
                if(not head.isspace()):
                    newString.append(head)                                                 
        else:
            # here the line does not contain any comment and can therefore be just copied to the new list
            newString.append(line)

    return "\n".join(newString)

def findEndOfFunction(myFunction):
    BracketCounter = 0
    results = re.search(r'\w*\(',myFunction)
    if(results):
        firstIfLocationTuple = results.span()
    else:
        return len(myFunction)
    

    for idx,character in enumerate(myFunction):
        if(idx<firstIfLocationTuple[1]-1):
            continue
        else:
            if character == "(": 
                BracketCounter = BracketCounter + 1
            if character == ")": 
                BracketCounter = BracketCounter - 1

            if(BracketCounter==0):
                if(character == ";"):
                    return idx + 1

StatisticsDict = []
def decideOnName(element,parent):
    elementDict = {}
    if(not element is None):
        for subelement in element:
            hasBeenChanged = False 
            elementDict = {
                    "Name":"",
                    "ActionName":"",
                    "Statements":[],
                    "Subelements":[],   
                }
            if("As" in subelement):
                hasBeenChanged = True
                elementDict["Name"] = subelement
                # go this path if the subelement has an "As" in its Name. This means that the subelement is actually a subelement and not a property
                elementName = subelement
                decideOnName(element[subelement],elementDict)
                
            else:
                if(re.search(pattern, subelement)):
                    if(element[subelement] == "="):
                        continue
                    #here we search for the "On" properties

                    #first character is always "=" followed by the name of the function and then an opening bracket or a commented-out function
                    # either =something()
                    # or = /* for multiline comments
                    # or = // for single line comment
                    
                    element[subelement] = removeComments(element[subelement])
                    if(element[subelement].replace("=","").isspace()):
                        continue

                    element[subelement] = re.sub(r'\n\n',"",element[subelement]).replace("=","",1)
                    # removes the first "=" because its unnecessary
                    # removes double newlines
                    functionDict = [] 

                    #splits the code of a On-Property into the function (nested are not regarded)
                    while len(element[subelement])>0:
                        if(not "(" in element[subelement]):
                            #if there is no bracket, no function is being used and therefore nothing is changing
                            break
                        try:
                            substring = element[subelement][0:findEndOfFunction(element[subelement])]
                            #try to get get a single function call written in the code
                        except:
                            print("element[subelement]",element[subelement])
                            raise Exception()
                        functionDict.append(substring)
                        #append it to the function dict and remove it from further processing
                        element[subelement] = element[subelement].replace(substring,"",1)
                        if(element[subelement].isspace()):
                            #if the code area is empty after the removal of the element, break since there is nothing else to do
                            break
                    importantLines = []   
                    
                    for idx,actualElement in enumerate(functionDict):
                        statsRegex = re.compile(r'.*?\(')
                        StatisticsDict.append(statsRegex.findall(functionDict[idx])[0].replace(" ",""))

                        #acutalElement is an entire function, currently the functions are seen as non-nested functions
                        functionDict[idx] = functionDict[idx].replace(" ","").replace("\n","")
                        if(functionDict[idx].endswith(";")):
                            #if the last character is a ";", remove it. removing it like above could remove important ";" and we only want the last to be removed
                            functionDict[idx] = functionDict[idx][:-1]

                        # VARIABLE DECLARATION ________________________________
                        if(functionDict[idx].startswith("Set(")):
                            functionDict[idx] = (functionDict[idx][4:-1].replace(","," = ",1))
                            functionDict[idx] = functionDict[idx] + ";global"
                            importantLines.append(functionDict[idx])
                        
                        elif(functionDict[idx]).startswith("UpdateContext("):
                            firstIfLocationTuple = re.search(r''+"UpdateContext"+r'',functionDict[idx]).span()
                            parameters = functionDict[idx][firstIfLocationTuple[1]:][1:-1]
                            splitIndexList = []
                            BracketCounter = 0
                            for idx2,character in enumerate(parameters):
                                if character == "(": 
                                    BracketCounter = BracketCounter + 1
                                if character == ")": 
                                    BracketCounter = BracketCounter - 1
                                if(BracketCounter==0):
                                    if(character == ","):
                                        splitIndexList.append(idx2)
                            splitIndexList.append(len(parameters))
                            functionComponents = []
                            firstIndex = 0 
                            for indices in splitIndexList:
                                functionComponents.append(parameters[firstIndex:indices].replace("\n",""))
                                firstIndex=indices+1
                            
                            list_length = len(functionComponents)
                            functionComponents[0] = functionComponents[0][1:]
                            functionComponents[len(functionComponents)-1] = functionComponents[len(functionComponents)-1][:-1]
                            for indx,el in enumerate(functionComponents):
                                functionComponents[indx] = el.replace(":"," = ") + ";local"
                                importantLines.append(functionComponents[indx])
  
                        # LOGICAL OPERATORS ________________________________

                        # elif(functionDict[idx]).startswith("Not("): #or !
                        #     print()

                        # elif(functionDict[idx]).startswith("And("): #or &&
                        #     print() 

                        # elif(functionDict[idx]).startswith("Or("): #or ||
                        #     print() 

                        elif(functionDict[idx]).startswith("Switch("): 
                            firstIfLocationTuple = re.search(r''+"Switch"+r'',functionDict[idx]).span()
                            parameters = functionDict[idx][firstIfLocationTuple[1]:][1:-1]
                            splitIndexList = []
                            BracketCounter = 0
                            #switch is rather complicated
                            #the first parameter is the switch value aka the variable that is being checked
                            #this can already be a nested function
                            #so for the first parameter we check if before the first comma appears a bracket is being opened
                            #if yes, then count the number of opening and closing brackets until its evened out agaiin
                            # only then the first occurence of a comma will be selected as a valid seperator
                            for idx2,character in enumerate(parameters):
                                if character == "(": 
                                    BracketCounter = BracketCounter + 1
                                if character == ")": 
                                    BracketCounter = BracketCounter - 1
                                if(BracketCounter==0):
                                    if(character == ","):
                                        splitIndexList.append(idx2)
                            splitIndexList.append(len(parameters))
                            functionComponents = []
                            firstIndex = 0 
                            for indices in splitIndexList:
                                functionComponents.append(parameters[firstIndex:indices].replace("\n",""))
                                firstIndex=indices+1
                            
                            
                            list_length = len(functionComponents)
                            pairedList = []
                            pairedList.append(functionComponents[0])
                            # the first parameter of a switch is always the "to-be-checked" value and is thereby required
                            # after that the cases and the corresponding actions follow. There must be atleast one case and the corresponding actionn
                            #this means that the least amount of parameters for a switch is 3
                            # the default case is getting called if none of the other cases has been triggered
                            # the default case has no case-value but instead only action(s) thereby increases the number of parameters by one
                            # this means that if there is just the to-be-checkd value and specifically defined cases, the number of parameters is uneven
                            # if there is additionally a default case, the number of parameters is even
                            for i in range(1, list_length-1, 2):
                                pair = [functionComponents[i],functionComponents[i+1] ]
                                pairedList.append(pair)     
                            if(list_length%2==0):
                                #is even therefore with a default case
                                pair = ["DEFAULT",functionComponents[list_length-1]]
                                pairedList.append(pair)     
                            pairedList.append("Switch")
                            importantLines.append(pairedList)

                        elif((functionDict[idx]).startswith("If(") or (functionDict[idx]).startswith("If (")): 
                            firstIfLocationTuple = re.search(r''+"If"+r'',functionDict[idx]).span()
                            parameters = functionDict[idx][firstIfLocationTuple[1]:][1:-1]
                            splitIndexList = []
                            BracketCounter = 0
                            for idx2,character in enumerate(parameters):
                                if character == "(": 
                                    BracketCounter = BracketCounter + 1
                                if character == ")": 
                                    BracketCounter = BracketCounter - 1
                                if(BracketCounter==0):
                                    if(character == ","):
                                        splitIndexList.append(idx2)
                            splitIndexList.append(len(parameters))
                            functionComponents = []
                            functionComponents.append("If")
                            firstIndex = 0 
                            for indices in splitIndexList:
                                functionComponents.append(parameters[firstIndex:indices].replace("\n",""))
                                firstIndex=indices+1
                            
                            importantLines.append(functionComponents)

                        #DATA SOURCE OPERATIONS ________________________________
                        # not as important for control flow graph

                        # elif(functionDict[idx]).startswith("Remove("):
                            
                        #     print() 

                        # elif(functionDict[idx]).startswith("RemoveIf("):
                        #     print() 

                        # elif(functionDict[idx]).startswith("Patch("):
                        #     print() 

                        # elif(functionDict[idx]).startswith("Submitform("):
                        #     print() 

                        # elif(functionDict[idx]).startswith("Update("):
                        #     print() 

                        # elif(functionDict[idx]).startswith("UpdateIf("):
                        #     print() 


                        #NAVIGATION ________________________________    
                        elif(functionDict[idx].startswith("Back(") or functionDict[idx].startswith("Exit(")):
                            #not much to do, just take as is
                            importantLines.append(functionDict[idx])

                        elif(functionDict[idx]).startswith("Navigate("):
                            functionDict[idx] = (functionDict[idx].split(",",1))[0]
                            if(functionDict[idx].endswith(")")):
                                functionDict[idx] = functionDict[idx][:-1]
                            functionDict[idx] = functionDict[idx].replace("("," = ")
                            importantLines.append(functionDict[idx])
                        else:
                            continue
                    # a statement does not end with the first ; 
                    # instead count the number of brackets split at the ; following the corresponding closing bracket

                    #TODO group summarizer feature would also be very helpful
                    lines = (element[subelement].replace("\n","")).split(";")
                    parent["ActionName"] = subelement
                                


                    if(not importantLines == []):
                        parent["Statements"] = importantLines
                elif(subelement == "Visible"):
                    if(not element[subelement] == "=false"):
                        parent["Visible"] = element[subelement].replace("=","")
                elif(subelement == "Items"):
                    parent["Items"] = element[subelement].replace("=","")
                elif(subelement == "DisplayMode"):
                    parent["DisplayMode"] = element[subelement].replace("=","")
                
                
                else:
                    continue
            # print(elementDict)
            if(hasBeenChanged):
                if(not elementDict["Statements"]==[] or not elementDict["Subelements"]==[]):
                    if(elementDict["Statements"]==[]):
                        elementDict.pop("Statements",None)
                    if(elementDict["Subelements"]==[]):
                        elementDict.pop("Subelements",None)
                    if(elementDict["ActionName"]==""):
                        elementDict.pop("ActionName",None)
                    parent["Subelements"].append(elementDict)

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
                
            try:
                key = list(parsed_yaml.keys())[0]
            except:
                print(appID, "is empty")
                continue
            main={
                "Name":key,
                "ActionName":"",
                "Statements":[],
                "Subelements":[],  
            } 
            try:
                decideOnName(parsed_yaml[key],main)
            except Exception as e:
                print("Screen was",screen)
                print(e)
                raise Exception()

            # print(json.dumps(main,indent = 4))

            if not os.path.exists('./'+mainFolder+"JSONs/"):
                os.makedirs('./'+mainFolder+"JSONs/")

            with open('./'+mainFolder+"JSONs/"+screen+'_JSON.json', 'w') as json_file:
                json.dump(main, json_file)


counter = 0
print("Creating Jsons, please wait...")
for name in os.listdir(".\BlobFolder"):
    appID = name.split(" ")[0]
    try:
        generateCFG(appID)
    except:
        print(appID)
        exit()
    counter += 1

# generateCFG("44b9e688-36dc-4f5f-a3fc-c7fed42debcc.msapp")


from collections import Counter
stats = Counter(StatisticsDict)
print(stats)
end = time.time()
dif = end - start
print("creating JSONs took: " +  str(dif) + "s for " + str(counter) + " Power Apps") 