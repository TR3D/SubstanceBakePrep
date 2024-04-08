import bpy
from bpy.props import EnumProperty

def enum_items_generator(self,context):
    global_data = context.scene.bakeprep_global_data
    global_data.enum_data.clear()

    active_set = None
    if context.scene.bakeprep_data:
        # look in custom data for bake set if not found, create new
        for data in context.scene.bakeprep_data:
           global_data.enum_data.append( (f"{data.bakeset_name}", f"{data.bakeset_name}", "") )
           
    return global_data.enum_data
    

def set_active_bake_set(self, context):
    # set global data to active bake set
    context.scene.bakeprep_global_data.active_bakeset_name = context.scene.bakeprep_global_data.bake_sets

    # add associated high and low poly meshes
    for data in context.scene.bakeprep_data:
        # search needed bake set
        if(data.bakeset_name == context.scene.bakeprep_global_data.active_bakeset_name):
            # convert string property to list
            active_set = data
            context.scene.bakeprep_global_data.active_low_poly_meshes.clear()
            context.scene.bakeprep_global_data.active_high_poly_meshes.clear()
            lp_objs = active_set.lp_meshes.split(":")
            hp_objs = active_set.hp_meshes.split(":")
            # remove empty first entry
            lp_objs.pop(0)
            hp_objs.pop(0)

            # save object names 
            for obj in lp_objs:
                context.scene.bakeprep_global_data.active_low_poly_meshes.append(obj)
            for obj in hp_objs:
                context.scene.bakeprep_global_data.active_high_poly_meshes.append(obj)
            break

def set_global_collection_data(value, low):
    if low:
        TR3D_DT_global_data.valid_collection_lo = value
    else:
        TR3D_DT_global_data.valid_collection_hi = value

def report(self,message): # report errors
	self.report({'ERROR'}, message)
	return{'CANCELLED'}

class TR3D_DT_global_data(bpy.types.PropertyGroup):
    valid_collection_lo = False
    valid_collection_hi = False

    new_name: bpy.props.StringProperty(default="new_name")
    
    active_bakeset_name: bpy.props.StringProperty(default="Bakeset")
    active_low_poly_meshes = []
    active_high_poly_meshes = []
                    
    enum_data = [] # holds tmp data information to construct the enumproperty from it

    bake_sets: bpy.props.EnumProperty(
                    name = "Active Bake Set",  
                    description = "All available bake sets",
                    items = enum_items_generator, # get_bake_sets_callback
                    update = set_active_bake_set  # set active bake set on value change
                    ) # type: ignore

    

class TR3D_DT_bake_data(bpy.types.PropertyGroup):
    bakeset_name: bpy.props.StringProperty(default="Bakeset")

    lp_meshes : bpy.props.StringProperty(default="")
    hp_meshes : bpy.props.StringProperty(default="")
    

# https://blenderartists.org/t/add-remove-enumproperty-items/1305166/8
class TR3D_OT_BakeSet_Add(bpy.types.Operator):
    bl_idname = 'tr3d.bake_set_add'
    bl_label = 'TR3D_OT_BakeSet_Add'
    bl_description = 'Add new bake set item'

    new_name: bpy.props.StringProperty(default= 'Bake Set name', name = 'BakeSet name')

    def execute(self, context):
        data = context.scene.bakeprep_global_data

        if context.scene.bakeprep_data:
            # look in custom data for bake set if not found, create new
            for set_data in context.scene.bakeprep_data:
                if self.new_name == set_data.bakeset_name:
                    report(self, "Bake set already exists. Please choose a different name")
                    return{'FINISHED'}
                
        # create new bake set data 
        n = context.scene.bakeprep_data.add()
        n.bakeset_name = self.new_name

        # add bake set name to global data
        data.enum_data.append((self.new_name, self.new_name, ''))  # add new set to enum_data    
        data.bake_sets = self.new_name # match value with newly created preset
        return{'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=200)


class TR3D_OT_BakeSet_Remove(bpy.types.Operator):
    bl_idname = 'tr3d.bake_set_remove'
    bl_label = 'TR3D_OT_BakeSet_Remove'
    bl_description = 'Remove current bake set item'
    
    @classmethod
    def poll(cls, context):
            return len(context.scene.bakeprep_global_data.enum_data) > 0

    def execute(self, context):
        data = context.scene.bakeprep_global_data
        bake_set = context.scene.bakeprep_data

        index = data.enum_data.index( (data.active_bakeset_name, data.active_bakeset_name, '') )
        data.enum_data.pop(index)

        # delete scene data
        i=0
        for item in bake_set:
            if item.bakeset_name == data.bake_sets:
                bake_set.remove(i)
                break
            i += 1
 
        # set enum to first entry
        if index >= len(data.enum_data)-1 and len(data.enum_data)-1 > 1:
            data.bake_sets = data.enum_data[0][0]
        # or 
        elif index == 0 and data.enum_data != []:
            if len(data.enum_data) > 1:
                data.bake_sets = data.enum_data[1][0]
            else:
                data.active_bakeset_name = ""
                data.active_low_poly_meshes.clear()
                data.active_high_poly_meshes.clear()

        return{'FINISHED'}
