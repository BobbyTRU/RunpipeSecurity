# 98b82dc7-3d62-44d6-8dcb-4b365fba5a0f.msapp folder

# App.fx.yaml

#   OnStart:
# =ClearCollect(col_LL,'Lunch and Learn'); #adds "Lunch and Learn" to the collection col_LL
# has to do with datasources so important for later

# Set(v_myProfile, 'Office365-Benutzer'.MyProfileV2().displayName);
from DataSources import colShopping
from DataSources import MaterialRequests
v_myProfile = "'Office365-Benutzer'.MyProfileV2().displayName"
# Set(v_today,Today())
v_today = "Today()"  # some value
# Set(v_today2,v_today)
v_today = v_today


# Screen3.fx.yaml
# has nothing

# Screen2.fx.yaml
# Gallery2 As gallery.galleryVertical:
#   Items: =MaterialRequests


#       Label1 As label:
#           OnSelect: =Select(Parent)


#       Icon3 As icon.CancelBadge
#           OnSelect: =Collect(colShopping,  ThisItem)

colShopping.add(MaterialRequests.ThisItem)


# von wo kommen daten > was sind die daten
# Geben DataSource an und thisItem / a Record


# Button3 As button:
# =Set(varHtml,'<Table style=''border: 1px solid black;width:100%;border-collapse: collapse;border-spacing: 5px;''><tr><th>Name</th><th colspan=''2''>ID</th></tr>'& Concat(colShopping, '<tr><td>' & Title & '</td><td>' & ID & '</td></td>') & '</table>')

varHtml="'<Table style=''border: 1px solid black;width:100%;border-collapse: collapse;border-spacing: 5px;''><tr><th>Name</th><th colspan=''2''>ID</th></tr>'& Concat(colShopping, '<tr><td>' & Title & '</td><td>' & ID & '</td></td>') & '</table>'"

#Screen1 
#"Gallery1_1 As gallery.'BrowseLayout_Vertical_TwoTextOneImageVariant_ver4.0'":
#   Items: =Mitarbeiter
#       Separator1 As rectangle:
#           OnSelect: =Select(Parent) 
#       TextInput1 As text:
#           OnChange: =Patch(Mitarbeiter,Gallery1_1.Selected,{Name: Gallery1_1.Selected.TextInput1.Text})
#Patch( DataSource, BaseRecord, ChangeRecord1 [, ChangeRecord2, … ])
from DataSources import Mitarbeiter

#Gallery1_1.Selected = a record from Mitarbeiter
#Get Value in Items of Gallery1_1 
# Name = something from DataSource Mitarbeiter

#Modifies or creates
#in Mitarbeiter look for Gallery1_1.Selected (a record from Mitarbeiter) and set {Name: Gallery1_1.Selected.TextInput1.Text} aka set name to some value from the record from Mitarbeiter 


#OnSelect: =Select(Parent)


#Screen MyEvents
#"Gallery_Navigation_1 As gallery.'BrowseLayout_Horizontal_TwoTextOneImageVariant_ver4.0'":
#Items: =[
# {title:Home, screen: 'My Events'},
# {title:Icon.Person, screen: 'My Profile'},
# {title:Printing3D, screen: Screen_Upcoming_Events},
# {title:Icon.Add, screen: Screen_New_Event}
# ]
#OnSelect: =Navigate(Gallery_Navigation_1.Selected.Value.screen,ScreenTransition.Fade)
# Hier ein sonderfall wo die screens in den items einer Gallery sind. Not part of PoC
# ususally in the brackets of the navigate function the actual screen name is written so
# whenever the case happens where the the screen to be navigated to is a variable, we are going to assume that every screen can be navigated to



#Gallery_Navigation_1.Selected.Value.screen points to the items of the Gallery
# 

