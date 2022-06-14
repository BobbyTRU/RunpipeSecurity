import re


myFunction = """
=If(User().Email in Filter('Event Registration', EventID = Text(Gallery2.Selected.ID)).ParticipantMail,
RemoveIf('Event Registration', User().Email = ParticipantMail,EventID = Text(Gallery2.Selected.ID));
Notify("You have successfully unregistered to the "&Gallery2.Selected.Name&" Training",NotificationType.Success),
Patch('Event Registration',Defaults('Event Registration'), {Title: Gallery2.Selected.EventTitle, EventID: Gallery2.Selected.ID, ParticipantMail: User().Email});
Notify("You have successfully registered to the "& Gallery2.Selected.Name&" Training",NotificationType.Success))
asd
asdasdasdasdasd()
"""


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
    
lastBracketIndex = findEndOfFunction("If",myFunction)
print(lastBracketIndex)
firstIfLocationTuple = re.search(r''+"If"+r'',myFunction).span()
parameters = myFunction[firstIfLocationTuple[1]:lastBracketIndex+1][1:-1]
BracketCounter = 0
splitIndexList = []
for idx,character in enumerate(parameters):
    if character == "(": BracketCounter = BracketCounter + 1
    if character == ")": BracketCounter = BracketCounter - 1
    if(character == "," and BracketCounter==0):
        splitIndexList.append(idx)

splitIndexList.append(len(parameters))
    
functionComponents = []
firstIndex = 0    

for indices in splitIndexList:
    functionComponents.append(parameters[firstIndex:indices].replace("\n",""))
    firstIndex=indices+1


#now check split the if statements into its 2 or 3 elements which are condition, true case [, optional false case]
# these element are seperated by commas, which are outside of brackets, so essentially break whenever a comma appears that is not in a bracket