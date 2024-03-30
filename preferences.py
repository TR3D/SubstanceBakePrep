import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, BoolProperty
import os

def addon_name():
    name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))
    return name

class BakePrepAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__ 

    lo_names: StringProperty(
        name="lowpoly collection names",
        subtype='NONE',
        description='Add custom scene collection names so that the script detects which scene object is a lowpoly mesh. Names are separated by spaces!',
        default="lo low lowpoly lo_poly low_poly",
    ) # type: ignore

    hi_names: StringProperty(
        name="highpoly collection names",
        subtype='NONE',
        description='Add custom scene collection names so that the script detects which scene object is a highpoly mesh. Names are separated by spaces!',
        default="hi high highpoly hi_poly high_poly",
    ) # type: ignore

    file_path: StringProperty(
        name="Export File Path",
        description="Fixed export location for exported files.",
        subtype='FILE_PATH',
    ) # type: ignore

    m_export_local: BoolProperty(
        name="Export files relative to .blend file?",
        description="If true, exported meshes are store in the same folder as the .blend file",
        default=True,
    ) # type: ignore

    painter_file_path: StringProperty(
        name="Substance 3D Painter executable",
        description="Point to the 3D Painter executable on your PC. This let's you start Paitner directly from Blender.",
        subtype='FILE_PATH',
    ) # type: ignore

    def draw(self, context):
        layout = self.layout
        column=layout.column(align=False)
        
        box = column.box()
        box.label(text="Scene Collections")
        box.prop(self,"lo_names")
        box.prop(self,"hi_names")
        box.separator(factor=0.5)
        column.separator(factor=2.5)
        box = column.box()
        box.label(text="Export")
        box.prop(self, "m_export_local")
        sub = box.row()
        sub.prop(self, "file_path")
        if(self.m_export_local):
            sub.enabled = False
        box.separator(factor=0.5)
        box.prop(self, "painter_file_path")
        box.separator(factor=0.5)


class TR3D_OT_bakePrep_addon_prefs(bpy.types.Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        info = ("Path: %s,  Boolean %r" %
                (addon_prefs.file_path, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}

