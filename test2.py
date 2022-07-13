#dc7387ac-68c0-436d-a31f-30565219b974.msapp folder

''' Detail Screen'''




from dataclasses import browserGallery


def screenEdit():
    print("as")

def screenListe():
    print("as")

def screenDetail():
    userChoice = "asd"
    if(userChoice == "IconBackarrow1"):
        #Navigate(Liste)
        screenListe()
    elif(userChoice == "IconEdit1"):
        #Navigate(Edit)
        screenEdit()
    elif(userChoice == "IconDelete1"):
        #"IsEmpty(Errors([@Projekte],BrowseGallery1.Selected))",
        myCondition = True
        if(myCondition):
            prevScreen = screenStack.pop()
            if(prevScreen == "Liste"):
                print("asdict")
            #Back()

screenStack = []

screenStack.append(screenListe)