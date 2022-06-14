import re 



myFileName ="%dc%25bersicht"
allMatches = re.findall(r'%.{2}', myFileName)
for el in allMatches:
    mySpan = re.finditer(r'%.{2}', myFileName).__next__().span()
    newlist = (str(mySpan).replace("(","").replace(")","").split(","))
    firstIdx = int(newlist[0])
    scndIdx = int(newlist[1])
    specialEl = myFileName[firstIdx:scndIdx].replace("%","")
    myFileName =  chr(int(specialEl, 16)).join([myFileName[:firstIdx],myFileName[scndIdx:]])   

