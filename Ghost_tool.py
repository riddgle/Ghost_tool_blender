bl_info = {
    "name": "Show Mesh",
    "author": "Bingo",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Show Mesh",
    "description": "Shows only the mesh of an animated object at the current frame",
    "warning": "",
    "doc_url": "",
    "category": "Animation",
}

import bpy

class OBJECT_OT_show_mesh(bpy.types.Operator):
    """Shows only the mesh of an animated object at the current frame"""
    bl_idname = "object.show_mesh"
    bl_label = "Show Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        C = bpy.context
        src_obj = bpy.context.active_object

        # Hide all objects except the source object
        for obj in C.scene.objects:
            if obj != src_obj:
                obj.hide_set(True)
        
        # Duplicate the mesh
        depsgraph = bpy.context.evaluated_depsgraph_get()
        src_obj_eval = src_obj.evaluated_get(depsgraph)
        new_obj = src_obj.copy()
        new_obj.data = bpy.data.meshes.new_from_object(src_obj_eval)
        new_obj.animation_data_clear()
        C.collection.objects.link(new_obj)
        
        # Remove armature modifier
        for mod in new_obj.modifiers:
            if mod.type == 'ARMATURE':
                new_obj.modifiers.remove(mod)
        
        # Remove vertex groups
        new_obj.vertex_groups.clear()
        
        return {'FINISHED'}

class VIEW3D_PT_show_mesh(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Show Mesh"
    bl_idname = "VIEW3D_PT_show_mesh"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Show Mesh"

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("object.show_mesh")

def register():
    bpy.utils.register_class(OBJECT_OT_show_mesh)
    bpy.utils.register_class(VIEW3D_PT_show_mesh)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_show_mesh)
    bpy.utils.unregister_class(VIEW3D_PT_show_mesh)

if __name__ == "__main__":
    register()