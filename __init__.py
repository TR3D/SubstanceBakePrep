bl_info = {
    "name": "Bake preparation toolkit",
    "description": "Quickly setup object names and material IDs for baking in Substance Painter.",
    "author": "Thorsten Ruploh, X: @TRuploh",
    "version": (1, 0, 0),
    "blender": (3, 6, 0),
    "location": "View3D > SidePanel > BakePrep",
    "tracker_url": "https://github.com/TR3D/SubstanceBakePrep/issues",
    "doc_url": "https://github.com/TR3D/SubstanceBakePrep/tree/main",
    "support": "COMMUNITY",
    "category": "3D View"
}

import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import EnumProperty, StringProperty, PointerProperty

from .preferences import (BakePrepAddonPreferences, TR3D_OT_bakePrep_addon_prefs,)
from .data import (TR3D_DT_global_data,
                   TR3D_DT_bake_data, 
                   TR3D_OT_BakeSet_Add,
                   TR3D_OT_BakeSet_Remove,)
from .visibility import (TR3D_OT_bakeprep_unhide, TR3D_OT_bakeprep_hide)
from .operators import (TR3D_OT_bakeprep_rename, 
                        TR3D_OT_bakeprep_export, 
                        TR3D_OT_bakeprep_material_assign, 
                        TR3D_OT_bakeprep_start_painter, )
from .ui import VIEW3D_PT_TR3DBakePrep
print("Imported BakePrepToolkit ...")
  
    
# BUG:
#   - when loading scene with bake sets, visibility options are not enabled until bake set was selected from list


blender_classes = [
    preferences.BakePrepAddonPreferences, preferences.TR3D_OT_bakePrep_addon_prefs,
    data.TR3D_DT_bake_data, data.TR3D_DT_global_data, data.TR3D_OT_BakeSet_Add, data.TR3D_OT_BakeSet_Remove,
    visibility.TR3D_OT_bakeprep_unhide, visibility.TR3D_OT_bakeprep_hide,
    operators.TR3D_OT_bakeprep_rename, operators.TR3D_OT_bakeprep_export, operators.TR3D_OT_bakeprep_material_assign, operators.TR3D_OT_bakeprep_start_painter,
    ui.VIEW3D_PT_TR3DBakePrep,
]

def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
   
    # initialize global data
    bpy.types.Scene.bakeprep_global_data = PointerProperty(type=TR3D_DT_global_data)
    
    # initialize bakeprep data per bake set
    bpy.types.Scene.bakeprep_data = bpy.props.CollectionProperty(
        type=TR3D_DT_bake_data,
    )
    
    bpy.types.Scene.placeholder = PointerProperty(type=TR3D_DT_bake_data)

def unregister():
    del bpy.types.Scene.bakeprep_data 
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)

if __name__ == "__main__":
    register()