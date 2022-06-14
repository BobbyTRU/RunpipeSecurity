import xml.etree.ElementTree as ET
import os
import json



for name in os.listdir(".\BlobFolder"):
    appID = name.split(" ")[0]
    mainFolder =".\BlobFolder\\"+appID+" folder\\"
    toOpen = "ConnectorSummary.json"
    f = open(mainFolder + toOpen)
    loadedJson = json.load(f)
    if(not loadedJson == []):
        for idx,connector in enumerate(loadedJson):
            if(not connector["FunctionsUsed"] == []):
                if(connector["FunctionsUsed"] == ["Run"]):
                    print(connector)
                    loadedJson[idx]["Type"] = "Flow"
                    continue
                else:
                    loadedJson[idx]["Type"] = "Connector"

                    root = ET.parse(mainFolder+appID+' unpacked/pkgs/Wadl/' + connector["Name"] + '.xml').getroot()
                    for idx2,usedFunc in enumerate(connector["FunctionsUsed"]):  
                        hasDeprecatedParam = False
                        try:
                            for el in root:
                                if("resources" in el.tag):
                                    for subEl in el:
                                        for subSubEl in subEl:
                                            if("method" in subSubEl.tag):
                                                
                                                for att in subSubEl.attrib:
                                                    if(usedFunc == subSubEl.attrib["id"]):
                                                        if("isDeprecated" in att):
                                                            hasDeprecatedParam = True
                                                            if(subSubEl.attrib[att]=="true"):
                                                                loadedJson[idx]["FunctionsUsed"][idx2]= {"Name":usedFunc,"isDeprecated":True}
                                                            else:
                                                                loadedJson[idx]["FunctionsUsed"][idx2]= {"Name":usedFunc,"isDeprecated":False}  
                                                            raise StopIteration
                        except StopIteration:
                            pass
                        if(not hasDeprecatedParam):
                            loadedJson[idx]["FunctionsUsed"][idx2]= {"Name":usedFunc,"isDeprecated":"n/a"}

                                            
                                                    
        with open(mainFolder + toOpen, 'w') as fp:
            json.dump(loadedJson, fp)


                


    
