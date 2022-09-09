## Overview
Quickly setup object names and material IDs for baking in Substance Painter or Designer. <br>
![blender_fuKptJ4bza](https://user-images.githubusercontent.com/63724445/189341070-a75e36af-bca0-4707-9c70-e3ac30ef8757.gif)


## Installation
To install the add-on in Blender, follow these steps:
- In Blenders top menu, go to **Edit -> Preferences**, choose the Add-ons section in the Preferences panel and click the Install button
- In the browser window that appears, select the location of the add-on and click Install
- Search for the "Bake preparation Toolkit" add-on in the list and enable it using the checkbox
- The tool can be found in the *BakePrep* panel in the right side menu in Blenders 3D viewport

## Preferences
![Weo7b4XJ58](https://user-images.githubusercontent.com/63724445/189339768-46ca6a07-36cd-4e8f-bebe-b1d014660aa3.jpg)
### Scene collection
Provide possible names for the scene collections that the script recognizes for the export process. Names are separated by spaces. <br>
![Weo7basdsad4XJ58](https://user-images.githubusercontent.com/63724445/189339811-6a19d75a-52fd-40ab-87ac-0371d8511a7a.jpg)

With the default setup, you can choose between different names for the lowpoly scene collection:
- lo
- low
- lowpoly
- lo_poly
- low_poly

### Export
Choose if the exported files should be stored in the same folder as your blender scene or in a default path.
You can also add the filepath of your Substance Painter executable here if you want to be able to start Substance 3D Painter directly from Blender. The path has to look something like this: *C:\Program Files\Allegorithmic\Substance Painter\Substance Painter.exe* <br>
![Weo7b4eawewaXJ58](https://user-images.githubusercontent.com/63724445/189340177-72938f82-1508-4ece-9dd9-acace56f9e9f.jpg)


## Usage

### Prerequisites
First, make sure that you have two collections in the scene: one for all highpoly meshes and one for all lowpoly meshes. The names of the collection are important because the script relies on the collection names to detect which objects are intended to be the highpoly and which are the lowpoly objects. <br> **Possible collection names can be setup in the addon preferences.** <br>
![hnK5udnwob](https://user-images.githubusercontent.com/63724445/189340357-734fd9d2-c351-4895-b26a-e8997c8c64af.jpg) <br>
If everything is fine, you see these messages at the top of the UI and all buttons are activated: <br>
![j0whgcasdsav9E2](https://user-images.githubusercontent.com/63724445/189340404-e8678e1c-36c0-4882-a4ec-72aa8d7aad34.jpg) <br>
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
![j0whadsagcv9E2](https://user-images.githubusercontent.com/63724445/189340536-251e20bf-0b3f-4077-a660-fb508887012d.jpg)
