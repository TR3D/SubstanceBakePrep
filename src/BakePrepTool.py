import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty
import os
import pathlib

bl_info = {
    "name": "Bake preparation toolkit",
    "description": "Quickly setup object names and material IDs for baking in Substance Painter.",
    "author": "Thorsten Ruploh, twitter: @TRuploh",
    "version": (0, 1, 0),
    "blender": (2, 83, 0),
    "location": "View3D > SidePanel > BakePrep",
    # "wiki_url": "",
    # "tracker_url": "",
    "support": "COMMUNITY",
    "category": "3D View"
}

class BakePrepAddonPreferences(bpy.types.AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    lo_names: StringProperty(
        name="lowpoly collection names",
        subtype='NONE',
        description='Add custom scene collection names so that the script detects which scene object is a lowpoly mesh. Names are separated by spaces!',
        default="lo low lowpoly lo_poly low_poly",
    )

    hi_names: StringProperty(
        name="highpoly collection names",
        subtype='NONE',
        description='Add custom scene collection names so that the script detects which scene object is a highpoly mesh. Names are separated by spaces!',
        default="hi high highpoly hi_poly high_poly",
    )

    filepath: StringProperty(
        name="Export File Path",
        description="Fixed export location for exported files.",
        subtype='FILE_PATH',
    )

    m_exportLocal: BoolProperty(
        name="Export files relative to .blend file?",
        description="If true, exported meshes are store in the same folder as the .blend file",
        default=True,
    )

    painter_filepath: StringProperty(
        name="Substance 3D Painter executable",
        description="Point to the 3D Painter executable on your PC. This let's you start Paitner directly from Blender.",
        subtype='FILE_PATH',
    )

    def draw(self, context):
        layout = self.layout
        column=layout.column(align=False)
        
        box = column.box()
        box.label(text="Scene Collection")
        box.prop(self,"lo_names")
        box.prop(self,"hi_names")

        box = column.box()
        box.label(text="Export")
        box.prop(self, "m_exportLocal")
        sub = box.row()
        sub.prop(self, "filepath")
        if(self.m_exportLocal):
            sub.enabled = False
        box.prop(self, "painter_filepath")
        


class TR3D_OT_bakePrep_addon_prefs(bpy.types.Operator):
    """Display example preferences"""
    bl_idname = "object.addon_prefs_example"
    bl_label = "Add-on Preferences Example"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        info = ("Path: %s,  Boolean %r" %
                (addon_prefs.filepath, addon_prefs.boolean))

        self.report({'INFO'}, info)
        print(info)

        return {'FINISHED'}


class VIEW3D_PT_TR3DBakePrep(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "BakePrep"
    bl_context = 'objectmode'
    bl_label = "Bake Prep"

    found_collection_lo = False
    found_collection_hi = False

    def draw(self, context):
        preferences = bpy.context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        collectionNames_lo = addon_prefs.lo_names.split(" ")
        collectionNames_hi = addon_prefs.hi_names.split(" ")

        layout = self.layout

        col = layout.column()
        col.label(text="Scene collections")
        if search_collection(collectionNames_lo):
            col.label(text="Lowpoly collection", icon="CHECKMARK")
            VIEW3D_PT_TR3DBakePrep.found_collection_lo=True
        else:
            col.label(text="Can't find lowpoly scene collection!", icon="ERROR")
            VIEW3D_PT_TR3DBakePrep.found_collection_lo=False

        if search_collection(collectionNames_hi):
            col.label(text="Highpoly collection", icon="CHECKMARK")
            VIEW3D_PT_TR3DBakePrep.found_collection_hi=True
        else:
            col.label(text="Can't find highpoly scene collection!", icon="ERROR")
            VIEW3D_PT_TR3DBakePrep.found_collection_hi=False
        col.separator(factor=2.5)

        col.prop(context.scene, 'bakeprep_new_name', text='Name')
        col.operator("tr3d.rename")
        col.separator(factor=2.5)
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

class TR3D_OT_bakeprep_rename(bpy.types.Operator):
    """Exports the lowpoly and highpoly meshes"""
    bl_idname = "tr3d.rename"
    bl_label = "Rename selected"
    bl_options = {'REGISTER', 'UNDO'}

    found_collection_lo = False
    found_collection_hi = False
    hidden_meshes_low = []
    hidden_meshes_high = []

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and VIEW3D_PT_TR3DBakePrep.found_collection_lo and VIEW3D_PT_TR3DBakePrep.found_collection_hi

    def execute(self, context):
        rename_selected(context.scene.bakeprep_new_name)
        return {"FINISHED"}


class TR3D_OT_bakeprep_unhide(bpy.types.Operator):
    """Unhide the lowpoly and highpoly meshes"""
    bl_idname = "tr3d.unhide"
    bl_label = "Unhide"
    bl_options = {'REGISTER', 'UNDO'}

    unhide_low: bpy.props.BoolProperty(
        name="unhide lowpoly",
        description="Unhide lowpoly?",
        default=True,
    )

    unhide_high: bpy.props.BoolProperty(
        name="unhide highpoly",
        description="Unhide highpoly?",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and TR3D_OT_bakeprep_rename.hidden_meshes_low and TR3D_OT_bakeprep_rename.hidden_meshes_high


    def execute(self, context):
        toggle_hidden_meshes(self.unhide_low, self.unhide_high, False)
        return {"FINISHED"}


class TR3D_OT_bakeprep_hide(bpy.types.Operator):
    """Unhide the lowpoly and highpoly meshes"""
    bl_idname = "tr3d.hide"
    bl_label = "Unhide"
    bl_options = {'REGISTER', 'UNDO'}

    unhide_low: bpy.props.BoolProperty(
        name="unhide lowpoly",
        description="Unhide lowpoly?",
        default=True,
    )

    unhide_high: bpy.props.BoolProperty(
        name="unhide highpoly",
        description="Unhide highpoly?",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and TR3D_OT_bakeprep_rename.hidden_meshes_low and TR3D_OT_bakeprep_rename.hidden_meshes_high


    def execute(self, context):
        toggle_hidden_meshes(self.unhide_low, self.unhide_high, True)
        return {"FINISHED"}


class TR3D_OT_bakeprep_export(bpy.types.Operator):
    """Export meshes"""
    bl_idname = "tr3d.export"
    bl_label = "Export"
    bl_options = {'REGISTER', 'UNDO'}

    export_lowpoly: bpy.props.BoolProperty(
        name="export lowpoly",
        description="Export the lowpoly meshes?",
        default=True,
    )

    export_highpoly: bpy.props.BoolProperty(
        name="export highpoly",
        description="Export the highpoly meshes?",
        default=True,
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and TR3D_OT_bakeprep_rename.hidden_meshes_low and TR3D_OT_bakeprep_rename.hidden_meshes_high

    def execute(self, context):
        #       export the lowpoly
        if(self.export_lowpoly):
            bpy.ops.object.select_all(action='DESELECT')
            for obj in TR3D_OT_bakeprep_rename.hidden_meshes_low:
                obj.select_set(True)
            # bpy.ops.object.select_same_collection(collection="lowpoly")
            export_selected("_low")
            print("export lowpoly")
            bpy.ops.object.select_all(action='DESELECT')

        # export the highpoly
        if(self.export_highpoly):
            bpy.ops.object.select_all(action='DESELECT')
            for obj in TR3D_OT_bakeprep_rename.hidden_meshes_high:
                obj.select_set(True)
            # bpy.ops.object.select_same_collection(collection="highpoly")
            export_selected("_hi")
            print("export highpoly")
            bpy.ops.object.select_all(action='DESELECT')
        return {"FINISHED"}


class TR3D_OT_bakeprep_material_assign(bpy.types.Operator):
    """Assign colored material to selected highpoly mesh"""
    bl_idname = "tr3d.assign_mat"
    bl_label = "Material #1"
    bl_options = {'REGISTER', 'UNDO'}

    mat_color: bpy.props.FloatVectorProperty(
        name="material color",
        description="color definition of material",
        default=(0.0, 0.0, 0.0),
    )

    mat_name: bpy.props.StringProperty(
        name="mat_ID_name",
        description="Name of the created ID material",
        default="ID_red",
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and TR3D_OT_bakeprep_rename.hidden_meshes_high

    def execute(self, context):
        assign_material(self.mat_color, self.mat_name)
        return {"FINISHED"}


class TR3D_OT_bakeprep_start_painter(bpy.types.Operator):
    """Start Substance Painter (Please point to the startup file in the settings first!)"""
    bl_idname = "tr3d.start_painter"
    bl_label = "Launch Painter"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences
        return context.area.type == 'VIEW_3D' and addon_prefs.painter_filepath

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__name__].preferences

        os.startfile(addon_prefs.painter_filepath)
        return {"FINISHED"}


blender_classes = [
    VIEW3D_PT_TR3DBakePrep,
    TR3D_OT_bakeprep_rename,
    TR3D_OT_bakeprep_unhide,
    TR3D_OT_bakeprep_hide,
    TR3D_OT_bakeprep_material_assign,
    TR3D_OT_bakeprep_start_painter,
    TR3D_OT_bakeprep_export,
    BakePrepAddonPreferences,
]


def register():
    bpy.types.Scene.bakeprep_new_name = bpy.props.StringProperty(
        name="bakeprep_new_name",
    )
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    del bpy.types.Scene.bakeprep_new_name
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)


if __name__ == "__main__":
    register()

def oops(self, context):
    self.layout.label(text="Did not find any matching Collections! Please name your collections ""low / high"" or ""lowpoly / highpoly"" etc.")

def search_collection(needed_collection):
    for item in needed_collection:
        if item in bpy.data.collections:
            needed_collection = [item]
            found_collection_lo=True
            return(True)
        continue

def rename_selected(newname):
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__name__].preferences
    collectionNames_lo = addon_prefs.lo_names.split(" ")
    collectionNames_hi = addon_prefs.hi_names.split(" ")
    # deselect everything that is not a mesh:
    for obj in bpy.context.selected_objects:
        if obj.type not in {'MESH'}:
            obj.select_set(False)
    view_layer = bpy.context.view_layer
    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    # loop through selected objects
    for obj in selection:
        view_layer.objects.active = obj
        finalname = ""
        for item in collectionNames_lo:
            if (obj.users_collection[0].name == item):
                finalname = newname + "_low"
                TR3D_OT_bakeprep_rename.hidden_meshes_low.append(obj)
                break
        for item in collectionNames_hi:
            if (obj.users_collection[0].name == item):
                finalname = newname + "_high_ignorebf"
                TR3D_OT_bakeprep_rename.hidden_meshes_high.append(obj)
                break
        if finalname == "":
            bpy.context.window_manager.popup_menu(oops, title="Error", icon='ERROR')
            break
        obj.name = finalname
        obj.hide_set(True)


def export_selected(name):
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__name__].preferences
    view_layer = bpy.context.view_layer
    obj_active = view_layer.objects.active
    selection = bpy.context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')
    # loop through selected objects and add triangulation
    for obj in selection:
        # some exporters only use the active object
        view_layer.objects.active = obj
        bpy.ops.object.modifier_add(type='TRIANGULATE')
        obj.select_set(True)

    # Create export path:
    if not bpy.data.filepath:
            raise Exception("Blend file is not saved")
    
    scenefilename = bpy.path.display_name(bpy.data.filepath)
    # local export
    if addon_prefs.m_exportLocal:
        # export to blend file location       
        basedir = bpy.path.abspath(bpy.data.filepath)
        basedir = basedir[:-len(bpy.path.basename(bpy.data.filepath))]
        print("EXPORTING FILES PARALLEL TO .blend FILE")

    else:
        # fixed directory
        print("EXPORTING FILES TO FIXED DIRECTORY")
        basedir = addon_prefs.filepath
    
    fn = pathlib.Path(basedir, (scenefilename + name))
    print(fn)

    bpy.ops.export_scene.fbx(filepath=str(fn) + ".fbx", use_selection=True,
                             object_types={'MESH'})
    # delete the triangulation modifier from selection
    for obj in selection:
        view_layer.objects.active = obj
        bpy.ops.object.modifier_remove(modifier='Triangulate')
    view_layer.objects.active = obj_active
    for obj in selection:
        obj.select_set(True)


def toggle_hidden_meshes(low=True, high=True, hide=False):
    # print(f" unhide low: {low}, unhide high: {high}")
    if(low):
        for item in TR3D_OT_bakeprep_rename.hidden_meshes_low:
            if(hide):
                item.hide_set(True)
            else:
                item.hide_set(False)
    if(high):
        for item in TR3D_OT_bakeprep_rename.hidden_meshes_high:
            if(hide):
                item.hide_set(True)
            else:
                item.hide_set(False)


def assign_material(color_3, name):
    # create material if none existent
    if name not in bpy.data.materials:
        m_mat = bpy.data.materials.new(name=name)
        m_color = (color_3[0], color_3[1], color_3[2], 1)
        m_mat.diffuse_color = m_color

    # deselect objects that are not meshes
    for obj in bpy.context.selected_objects:
        if obj.type not in {'MESH'}:
            obj.select_set(False)
    selection = bpy.context.selected_objects

    # assign material to remaining selection
    for obj in selection:
        obj.active_material = bpy.data.materials[name]
