Notes on Cave Maping Application


   First, to anyone who may take the time to check out my project, Thank you for your time. Here in these notes, I will quickly explain the basis of the application.  I was inspired to create this after realizing how difficult it is to access the location of caves. This application tries to help solve that issue by creating an easy-to-use map tool to view the cave locations. 
 It provides highly accurate co-ordinates of cave locations across the state of Missouri. I chose the state of Missouri as it contains many caves and is my current home state. 

![Screenshot 2024-04-21 154341](https://github.com/JohnathonCrowder/Missouri_Cave_Map/assets/139363360/ddc7621a-89d2-42aa-86f8-e4c2eedb80a9)

As you can see above, there are many caves in Missouri. Here i have created tools to filter through these many cave systems. On the right of the application, you can see a list of all the caves. The user also has several options to filter these caves. First, the user can search for the cave by name. Second, ther user can filter the caves by the distance in miles from there current city. The users location is automatically obtained and is a general estimation as opposed to an exact location. With either searching by name or miles, both the map and the list box are updated with each character. This provides for a fluent and active filtering experience. Here is an example search:

![Screenshot 2024-04-21 155321](https://github.com/JohnathonCrowder/Missouri_Cave_Map/assets/139363360/4f9a2a7b-c4c5-4045-90ed-9f7bde8d43b3)


The user can also select caves from the list or on the map to view more detail:

![Screenshot 2024-04-21 155424](https://github.com/JohnathonCrowder/Missouri_Cave_Map/assets/139363360/5391a0bb-9b30-431d-81e3-f108ff890d98)

The user also has the option to turn the map into satellite mode:

![Screenshot 2024-04-21 155632](https://github.com/JohnathonCrowder/Missouri_Cave_Map/assets/139363360/f67a8a15-6097-45ae-8e6e-2b82d959d67e)

It should be noted that this project is still ongoing and is still experiencing some errors.

If you are interested in where I got the cave locations, You should check out this link here and remember that caving can be dangerous:

https://grottocenter.org/ui/map


If you are interested in the code, Then it is well documented there and provides many insightful comments to help you understand how it works. As a brief overview:

1. It loads the cave locations from a csv into a pandas dataframe 
2. It then uses pyqt5 to create and setup the gui
3. It uses folium to create the map and geocoder to get the user location
4. The gui is displayed for the user
