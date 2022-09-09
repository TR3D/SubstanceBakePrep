* TOC
{:toc}

## Overview
Quickly setup object names and material IDs for baking in Substance Painter or Designer. <br>
![image](https://user-images.githubusercontent.com/63724445/135817875-614cf4ad-c5ff-4993-919b-ee4694cdaaad.png)

## Installation
To install the add-on in Blender, follow these steps:
- In Blenders top menu, go to **Edit -> Preferences**, choose the Add-ons section in the Preferences panel and click the Install button
- In the browser window that appears, select the location of the add-on and click Install
- Search for the "Bake preparation Toolkit" add-on in the list and enable it using the checkbox
- The tool can be found in the *BakePrep* panel in the right side menu in Blenders 3D viewport

## Preferences
### Scene collection
Setup possible names for the scene collections that the script recognizes for the export process. Names are separated by spaces. <br>
![image](https://user-images.githubusercontent.com/63724445/135819086-96b99639-4f4b-470b-8012-7eb764cf2899.png)

With the default setup, you can choose between different names for the lowpoly scene collection:
- lo
- low
- lowpoly
- lo_poly
- low_poly

### Export
Choose if the exported files should be stored in the same folder as your blender scene or in a default path.
You can also add the filepath of your Substance Painter executable here if you want to be able to start Substance 3D Painter directly from Blender. The path has to look something like this: *C:\Program Files\Allegorithmic\Substance Painter\Substance Painter.exe* <br>
![image](https://user-images.githubusercontent.com/63724445/135819257-24122d49-a001-4390-adcc-6138bddf891b.png)

## Usage

### Prerequisites
First, make sure that you have two collections in the scene: one for all highpoly meshes and one for all lowpoly meshes. The names of the collection are important because the script relies on the collection names to detect which objects are intended to be the highpoly and which are the lowpoly objects. <br> **Possible collection names can be setup in the addon preferences.** <br>
![image](https://user-images.githubusercontent.com/63724445/136044069-952fb784-45cc-4a3f-afb8-e9e85c38bd58.png) <br>
If everything is fine, you see these messages at the top of the UI and all buttons are activated: <br>
![image](https://user-images.githubusercontent.com/63724445/136048434-1d93ef4e-7afd-48e4-b070-9ca3c179091d.png) <br>
If not, please double check if you have the needed scene collections and they have the correct names.


### Renaming
Enter the new name in the textbox, select every object in the scene you want to rename and click the *Rename selected* button. The Objects will then be hidden to provide a better overview of which objects still have to be renamed. <br>
![vreeEtmPTk](https://user-images.githubusercontent.com/63724445/136046554-f643dd77-6261-48cb-918b-d796d32bbd97.gif)


### Hide/Unhide
Toggle visibility for every renamed mesh in the scene or just for the highpoly or lowpoly meshes. <br>
![Zlyfm9mlEP](https://user-images.githubusercontent.com/63724445/136045125-bdab7133-58ae-4039-a7fe-ae083fac3c90.gif)



### Highpoly Colors
While the lowpoly is hidden, select different highpoly meshes and click on one of the colors to quickly assign a new color ID material to your selection. <br>
![wsZOr2PHCt](https://user-images.githubusercontent.com/63724445/136045108-fbb0330e-a8ea-461e-b9cc-cb0f869047d3.gif)


### Export
Export your lowpoly and highpoly meshes. If you setup your Subtance 3D Painter path, you can also choose to start the application here. <br>
![image](https://user-images.githubusercontent.com/63724445/136047921-b6e41f10-f74e-4d3a-a015-df2782280e82.png)
