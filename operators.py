import bpy # type: ignore
from bpy.props import EnumProperty # type: ignore

import os 
import pathlib
from .data import set_active_bake_set

from mathutils import Vector # type: ignore


def error(self, message):
    self.report({'ERROR'}, message)
    return{'CANCELLED'}

def search_collection(needed_collection):
    for item in needed_collection:
        if item in bpy.data.collections:
            #needed_collection = [item]
            return(True)
        continue

def rename_selected(self, context):
    newname = context.scene.bakeprep_global_data.new_name
    bake_set_name = context.scene.bakeprep_global_data.active_bakeset_name
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons[__package__].preferences
    collectionNames_lo = addon_prefs.lo_names.split(" ")
    collectionNames_hi = addon_prefs.hi_names.split(" ")
    
    # deselect everything that is not a mesh:
    for obj in bpy.context.selected_objects:
        if obj.type not in {'MESH'}:
            obj.select_set(False)
    view_layer = bpy.context.view_layer
    selection = bpy.context.selected_objects
    bpy.ops.object.select_all(action='DESELECT')
    
    if len(selection) > 0:
        # search for bake set in custom data. If not found, create new
        n = None
        if context.scene.bakeprep_data:
            for data in context.scene.bakeprep_data:
                if(data.bakeset_name == bake_set_name):
                    n = data
                    break

        # no matching set or no set in scene; create new    
        if n == None:
            n = context.scene.bakeprep_data.add()
            n.bakeset_name = bake_set_name
            
        iteration = 0
        # loop through selected objects
        for obj in selection:
            view_layer.objects.active = obj
            finalname = ""
            
            for item in collectionNames_lo:
                if (obj.users_collection[0].name == item):
                    finalname = f"{bake_set_name}_{newname}_low.0{iteration}"
                    obj.name = finalname
                    n.lp_meshes += ":" + finalname
                    # print(f"added LP mesh {finalname} to: {n.bakeset_name}")
                    break

            for item in collectionNames_hi:
                if (obj.users_collection[0].name == item):
                    finalname = f"{bake_set_name}_{newname}_high_ignorebf.0{iteration}"
                    obj.name = finalname
                    n.hp_meshes += ":" + finalname
                    # print(f"added HP mesh {finalname} to: {n.bakeset_name}")
                    break
            iteration += 1
            if finalname == "":
                error(self, "Did not find any matching Collections! Please name your collections ""low / high"" or ""lowpoly / highpoly"" etc.")
                break
            obj.hide_set(True)
            # print(obj.data.name)
                
        # save mesh names and update active bake set data
        n.low_poly_meshes = n.lp_meshes.split(":")
        n.high_poly_meshes = n.hp_meshes.split(":")
        set_active_bake_set(self, context)
    else:
        error(self, "Please select scene mesh objects to rename!")


def export_meshes(name, objects_lists):
    context = bpy.context
    preferences = context.preferences
    addon_prefs = preferences.addons[__package__].preferences
    view_layer = context.view_layer
    
    bake_set = context.scene.bakeprep_global_data.active_bakeset_name + "_"

    bpy.ops.object.select_all(action='DESELECT')
    for list in objects_lists:
        for o in list:
            obj = bpy.context.scene.objects.get(o)
            obj.select_set(True)       
            view_layer.objects.active = obj
            bpy.ops.object.modifier_add(type='TRIANGULATE')

    selection = context.selected_objects

    # Create export path:
    if not bpy.data.filepath:
        raise Exception("Blend file was not saved yet")
    
    scene_file_name = bpy.path.display_name(bpy.data.filepath)
    # local export
    if addon_prefs.m_export_local:
        # export to blend file location       
        basedir = bpy.path.abspath(bpy.data.filepath)
        basedir = basedir[:-len(bpy.path.basename(bpy.data.filepath))]
        print("EXPORTING FILES PARALLEL TO .blend FILE")

    else:
        # fixed directory
        print("EXPORTING FILES TO FIXED DIRECTORY")
        basedir = addon_prefs.filepath
    
    fn = pathlib.Path(basedir, (bake_set + scene_file_name + name))
    print(fn)

    bpy.ops.export_scene.fbx(filepath=str(fn) + ".fbx", use_selection=True,
                             object_types={'MESH'})
    
    # delete the triangulation modifier from selection
    for obj in selection:
        obj.select_set(True)
        view_layer.objects.active = obj
        bpy.ops.object.modifier_remove(modifier='Triangulate')
        

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


class TR3D_OT_bakeprep_rename(bpy.types.Operator):
    """Exports the lowpoly and highpoly meshes"""
    bl_idname = "tr3d.rename"
    bl_label = "Rename selected"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.scene.bakeprep_global_data.valid_collection_lo and context.scene.bakeprep_global_data.valid_collection_hi

    def execute(self, context):
        rename_selected(self, context)
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
    ) # type: ignore


    export_highpoly: bpy.props.BoolProperty(
        name="export highpoly",
        description="Export the highpoly meshes?",
        default=True,
    ) # type: ignore


    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.scene.bakeprep_global_data.active_low_poly_meshes and context.scene.bakeprep_global_data.active_high_poly_meshes

    def execute(self, context):
        # export the lowpoly
        if(self.export_lowpoly):
            export_meshes("_low", [context.scene.bakeprep_global_data.active_low_poly_meshes])
            print("export lowpoly")

        # export the highpoly
        if(self.export_highpoly):
            export_meshes("_hi", [context.scene.bakeprep_global_data.active_high_poly_meshes])
            print("export highpoly")
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
    ) # type: ignore


    mat_name: bpy.props.StringProperty(
        name="mat_ID_name",
        description="Name of the created ID material",
        default="ID_red",
    ) # type: ignore


    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.scene.bakeprep_global_data.active_high_poly_meshes

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
        addon_prefs = preferences.addons[__package__].preferences
        return context.area.type == 'VIEW_3D' and addon_prefs.painter_file_path

    def execute(self, context):
        preferences = context.preferences
        addon_prefs = preferences.addons[__package__].preferences

        os.startfile(addon_prefs.painter_file_path)
        return {"FINISHED"}    