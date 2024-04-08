import bpy

def toggle_hidden_meshes(context, objects_lists, hide=False):
    #loop over lists and set visibility
    for list in objects_lists:
        for o in list:
            #print(f"set hide to {hide} for {o}")
            obj = bpy.context.scene.objects.get(o)
            obj.hide_set(hide)


class TR3D_OT_bakeprep_unhide(bpy.types.Operator):
    """Unhide the lowpoly and highpoly meshes"""
    bl_idname = "tr3d.unhide"
    bl_label = "Unhide"
    bl_options = {'REGISTER', 'UNDO'}

    unhide_low: bpy.props.BoolProperty(
        name="unhide lowpoly",
        description="Unhide lowpoly?",
        default=True,
    ) # type: ignore

    unhide_high: bpy.props.BoolProperty(
        name="unhide highpoly",
        description="Unhide highpoly?",
        default=True,
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.scene.bakeprep_global_data.active_low_poly_meshes and context.scene.bakeprep_global_data.active_high_poly_meshes

    def execute(self, context):
        #unhide low only
        if(self.unhide_low and not self.unhide_high): 
            toggle_hidden_meshes(context, [context.scene.bakeprep_global_data.active_low_poly_meshes], False)
        #unhide high only
        elif (not self.unhide_low and self.unhide_high): 
            toggle_hidden_meshes(context, [context.scene.bakeprep_global_data.active_high_poly_meshes], False)
        # unhide low and high
        elif (self.unhide_low and self.unhide_high): 
            toggle_hidden_meshes(context, [context.scene.bakeprep_global_data.active_low_poly_meshes, 
                                           context.scene.bakeprep_global_data.active_high_poly_meshes], False) 
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
    ) # type: ignore

    unhide_high: bpy.props.BoolProperty(
        name="unhide highpoly",
        description="Unhide highpoly?",
        default=True,
    ) # type: ignore

    @classmethod
    def poll(cls, context):
        return context.area.type == 'VIEW_3D' and context.scene.bakeprep_global_data.active_low_poly_meshes and context.scene.bakeprep_global_data.active_high_poly_meshes

    def execute(self, context):
        #unhide low only
        if(self.unhide_low and not self.unhide_high): 
            toggle_hidden_meshes(context, [context.scene.bakeprep_global_data.active_low_poly_meshes], True)
        #unhide high only
        elif (not self.unhide_low and self.unhide_high): 
            toggle_hidden_meshes(context, [context.scene.bakeprep_global_data.active_high_poly_meshes], True) 
        # unhide low and high
        elif (self.unhide_low and self.unhide_high): 
            toggle_hidden_meshes(context, [context.scene.bakeprep_global_data.active_low_poly_meshes, 
                                           context.scene.bakeprep_global_data.active_high_poly_meshes], True) 
        return {"FINISHED"}

