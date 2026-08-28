bl_info = {
    "name": "Wythoph",
    "blender": (4, 0, 0),
    "category": "Mesh",
}

import os
import sys
import bpy

# Set up clean local import path tracking
addon_dir = os.path.dirname(os.path.abspath(__file__))
if "rust_core" in sys.modules:
    del sys.modules["rust_core"]
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

import rust_core

class MESH_OT_rust_cube_generator(bpy.types.Operator):
    bl_idname = "mesh.rust_cube_generator"
    bl_label = "Create Placeholder Cube"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Expose a parameter property directly inside Blender's UI
    edge_length: bpy.props.FloatProperty(
        name="Edge Length",
        default=2.0,
        min=0.001,
        description="Edge Length"
    )
    
    def execute(self, context):
        # 1. Fetch data arrays calculated inside Rust
        geometry = rust_core.generate_cube_geometry(self.edge_length)
        
        # 2. Build a fresh new mesh container inside Blender
        mesh = bpy.data.meshes.new("Rust_Cube_Mesh")
        obj = bpy.data.objects.new("Rust_Cube", mesh)
        
        # 3. Link the object to the active workspace collection
        context.collection.objects.link(obj)
        
        # 4. Populate mesh topology instantly using fast internal geometry mapping
        mesh.from_pydata(geometry.vertices, [], geometry.faces)
        mesh.update()
        
        # Select and highlight the newly made object
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MESH_OT_rust_cube_generator.bl_idname, icon='MESH_CUBE')

def register():
    bpy.utils.register_class(MESH_OT_rust_cube_generator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_rust_cube_generator)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()

