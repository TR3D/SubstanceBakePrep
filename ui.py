import bpy

from .preferences import (BakePrepAddonPreferences, TR3D_OT_bakePrep_addon_prefs)
from .visibility import (TR3D_OT_bakeprep_unhide, TR3D_OT_bakeprep_hide)
from .data import (TR3D_OT_BakeSet_Add, TR3D_OT_BakeSet_Remove, set_global_collection_data)
from .operators import (TR3D_OT_bakeprep_rename, 
                        TR3D_OT_bakeprep_export, 
                        TR3D_OT_bakeprep_material_assign, 
                        TR3D_OT_bakeprep_start_painter, 
                        search_collection, ) 

class VIEW3D_PT_TR3DBakePrep(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BakePrep"
    bl_context = 'objectmode'
    bl_label = "Bake Prep"


    def draw(self, context):
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[__package__].preferences
        collectionNames_lo = addon_prefs.lo_names.split(" ")
        collectionNames_hi = addon_prefs.hi_names.split(" ")

        layout = self.layout

        col = layout.column()
        # ---------------------
        # Scene collections
        col.label(text="Scene collections")
        if search_collection(collectionNames_lo):
            set_global_collection_data(True, True)
            col.label(text="Lowpoly collection", icon="CHECKMARK")
        else:
            set_global_collection_data(False, True)
            col.label(text="Can't find lowpoly scene collection!", icon="ERROR")

        if search_collection(collectionNames_hi):
            set_global_collection_data(True, False)
            col.label(text="Highpoly collection", icon="CHECKMARK")
        else:
            set_global_collection_data(False, False)
            col.label(text="Can't find highpoly scene collection!", icon="ERROR")
        col.separator(factor=2.5)
        
        # ---------------------
        # Bake set
        col.label(text="Bake Set")
        col.prop(context.scene.bakeprep_global_data, "bake_sets", text='')  
        col.separator(factor=0.5)
        row = col.row(align=True)
        props = row.operator('tr3d.bake_set_add', text= 'Add')
        props = row.operator('tr3d.bake_set_remove', text = 'Remove')
        col.separator(factor=2.5)

        # Display string property values
        ''' for node in context.scene.bakeprep_data:
            row = col.row()
            row.prop(node, "bakeset_name")
            row.prop(node, "ui_lp_meshes")
            row.prop(node, "ui_hp_meshes")'''

        col.separator(factor=2.5)
        # ---------------------
        # Renaming
        col.prop(context.scene.bakeprep_global_data, "new_name", text='Name')
        props = col.operator("tr3d.rename")   
        col.separator(factor=2.5)

        # ---------------------
        # Visibility
        props = col.operator("tr3d.unhide",
                             text="Unhide all", icon="HIDE_OFF")
        props.unhide_low = True
        props.unhide_high = True
        row = col.row(align=True)
        props = row.operator("tr3d.unhide",
                             text="Lowpoly", icon="HIDE_OFF")
        props.unhide_low = True
        props.unhide_high = False
        props = row.operator("tr3d.unhide",
                             text="Highpoly",
                             icon="HIDE_OFF")
        props.unhide_low = False
        props.unhide_high = True
        row = col.row(align=True)
        props = row.operator("tr3d.hide",
                             text="Lowpoly",
                             icon="HIDE_ON")
        props.unhide_low = True
        props.unhide_high = False
        props = row.operator("tr3d.hide",
                             text="Highpoly",
                             icon="HIDE_ON")
        props.unhide_low = False
        props.unhide_high = True

        col.separator(factor=2.5)

        # ---------------------
        # Material colors
        row = layout.row(align=True)
        row.label(text="Material color")
        row = layout.row(align=True)
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_01")
        props.mat_color = (1, 0, 0)
        props.mat_name = "ID Red"
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_04")
        props.mat_color = (0, 1, 0)
        props.mat_name = "ID Green"
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_05")
        props.mat_color = (0, 0, 1)
        props.mat_name = "ID Blue"
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_03")
        props.mat_color = (1, 1, 0)
        props.mat_name = "ID Yellow"
        row = layout.row(align=True)
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_02")
        props.mat_color = (1, .25, 0)
        props.mat_name = "ID Orange"
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_06")
        props.mat_color = (.262, 0.1, .7)
        props.mat_name = "ID Purple"
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_08")
        props.mat_color = (.536, 0.268, 0.134)
        props.mat_name = "ID Brown"
        props = row.operator("tr3d.assign_mat",
                             text="ID",
                             icon="COLLECTION_COLOR_07")
        props.mat_color = (1, 0.3, 0.85)
        props.mat_name = "ID Pink"

        # ---------------------
        # Scene collections
        col = layout.column()
        col.separator(factor=2.5)
        col.label(text="Export")
        row = layout.row(align=True, heading="Export")
        props = row.operator("tr3d.export",
                             text="Lowpoly",
                             icon="EXPORT")
        props.export_lowpoly = True
        props.export_highpoly = False

        props = row.operator("tr3d.export",
                             text="Highpoly",
                             icon="EXPORT")
        props.export_lowpoly = False
        props.export_highpoly = True

        col = layout.column()
        col.separator(factor=1.25)
        props = col.operator("tr3d.start_painter")