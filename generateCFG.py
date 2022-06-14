import json
from multiprocessing import Condition
from typing import List


f = open("C:/Users/Robert/Desktop/WarnIssue/BlobFolder/44b9e688-36dc-4f5f-a3fc-c7fed42debcc.msapp folder/JSONs/HomeScreen_JSON.json")
data = json.load(f)


# for each element
# get the statements
# each statement gets 

#if multiple subelements, fork

# if all subelements of a group have the same statements, the group will get the statement




#what types of nodes are there
#normal nodes
#   have a statement which either kills or generates variables
#   has only one node before and one node after
#free user decision nodes
#   these nodes dont have a statement, the path which gets selected is essentially random. 
#   During the analysis multiple approaches will be taken, one where random paths will be taken with repetition and one without, then compare
#   has one node before and can have multiple nodes after with no real condition to which path gets taken
#if statement nodes
#   here the statement 
#   has one node before and two nodes after (true and false)
#Beginning node & End Node
#   Dont have any statement, are just for convenience


class startOrEndNode:
    def __init__(self,isEndNode = False):
        self.nextNode = None
        self.isEndNode = isEndNode

class ifNode:
    def __init__(self,statement,thenNode,elseNode = None):
        self.statement = statement
        self.thenNode = thenNode
        self.elseNode = elseNode

class freeChoiceNode:
    def __init__(self,choiceNodes = []):
        self.choiceNodes = choiceNodes

class normalNode:
    def __init__(self, statement=None,isLocal = False):
        self.statement = statement
        self.nextNode = []
        self.isLocal = isLocal



entryNode = startOrEndNode()
exitNode = startOrEndNode(isEndNode=True)
previousNode = entryNode
choiceNode = None

#1. for every element in the screen file
    #2. check if it has statements
        #3.  if yes, for each statement do the corresponding node
            # check if statement is an if
            # check if statement is an updatecontext
            # check if statement is an set

        #4.  if no, check if it has subelements
            #5. if yes, do #1 again but for subelements
            #6. if no, do nothing aka go to the next element in the for loop

def graphCreator(element):
    
    if("Statements" in element):
        for statement in element["Statements"]:
            if(type(statement)==list):
                if(statement[0]=="If"):
                    if(len(statement[0])==3):
                        newNode = ifNode(statement[1],statement[2])
                    elif(len(statement[0])==4):
                        newNode = ifNode(statement[1],statement[2],statement[3])
                if(statement[len(statement)-1] == "Switch"):
                    # a switch is essentially multiple ifs
                    # the switch in the json is a list consisting of the to-be-checkd value and then some number of 2-element lists followed by the string "Switch"
                    print()
                    
            if(statement.endswith(";local")):
                newNode = normalNode(statement = statement.split(";")[0],isLocal = True)
                if(type(previousNode)==normalNode or type(previousNode)==startOrEndNode):
                    previousNode.nextNode = newNode
                elif(type(previousNode) == freeChoiceNode):
                    previousNode.choiceNodes.append(newNode)
            if(statement.startswith("Navigate")):
                newNode = startOrEndNode(isEndNode=True)
                if(choiceNode != None):
                    previousNode = choiceNode

                        


    elif("Subelements" in element):
        print(element["Subelements"])
    else:
        print("nope")


graphCreator(data)
exit()


for element in data:
    if(element == "Name"):
        if("As group" in element):
            #check subelements
            # take statements of first subelement and check if every other element has the same
            isFirst = True
            hasSameStatements = True
            combinedAsOneNode = False
            Statements = []
            isLocal = False
            for subelement in data[element]["Subelements"]:
                if(isFirst):
                    if(subelement["Statements"]):
                        Statements = subelement["Statements"]
                        if("local" in  Statements):
                            isLocal = True   
                    isFirst = False
                else:
                    if(subelement["Statements"]):
                        #if it has statements
                        if(not Statements == subelement["Statements"]):
                            #check if it has the same statements as the first
                            print("not same statments")
                            hasSameStatements = False
        
            if(not subelement.has_key("Subelements") and hasSameStatements):
                #ignore the individual subelements and just put the group as a node
                print("combined")
                combinedAsOneNode = True
                singleNode = cfgNode(statement=Statements,isLocal = isLocal)
                previousNode.nextNodes.append(singleNode)
                previousNode = singleNode
                #otherwise repeat for the subelements
                
    if(element == "Statements"):
        for statement in data[element]:
            isLocal = False
            
            if(not (";(local)" in statement or ";(global)" in statement)):
                if("Navigate" in statement or "Back" in statement):
                    #NOTE for the analysis its important to remember the screen to which back leads
                    singleNode = cfgNode(statement=statement)
                    previousNode.nextNodes.append(singleNode)
                    singleNode.nextNodes.append(exitNode)
                    #TODO previousNode = last fork node
                
                else:
                    continue
            else:
                #if the statement has either local or global in its contents create a node otherwise ignore the statement
                if(";(local)" in statement):
                    isLocal = True
                singleNode = cfgNode(statement=statement,isLocal = isLocal)
                previousNode.nextNodes.append(singleNode)
                previousNode = singleNode
            
    if(element == "Subelements"):
        if(not combinedAsOneNode):
            if(data[element]):
                if(len(data[element])>1):
                    print("forking time baby")
                if(len(data[element])==1):
                    print("no fork")
        else:
            singleNode




thisNode = entryNode
while thisNode:
    print(thisNode.statement,"local =",thisNode.isLocal)
    if(thisNode.nextNodes):
        thisNode = thisNode.nextNodes[0]
    else:
        thisNode = None