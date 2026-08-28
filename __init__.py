bl_info = {
    "name": "Wythoph",
    "blender": (4, 0, 0),
    "category": "Mesh",
}

import os
import sys
import bpy
from bpy.types import LayoutPanelState

# Set up clean local import path tracking
addon_dir = os.path.dirname(os.path.abspath(__file__))
if "rust_core" in sys.modules:
    del sys.modules["rust_core"]
if addon_dir not in sys.path:
    sys.path.insert(0, addon_dir)

import rust_core

class MESH_OT_rust_cube_generator(bpy.types.Operator):
    bl_idname = "mesh.generate_polytope"
    bl_label = "Generate Polytope"
    bl_options = {'REGISTER', 'UNDO'}
    
    ringing: bpy.props.FloatVectorProperty( # type: ignore[reportIncompatibleMethodOverride]
        min=0,
        max=1,
        name="Ringing",
        default=[1,0,0]
    )
    # --- A -> B Properties ---
    ab_num: bpy.props.IntProperty( # type: ignore[reportIncompatibleMethodOverride]
        name="Num",
        default=5,
        min=2,
        description="Numerator for A->B"
    )
    ab_den: bpy.props.IntProperty( # type: ignore[reportIncompatibleMethodOverride]
        name="Den",
        default=1,
        min=1, # Prevent division by zero
        description="Denominator for A->B"
    )

    # --- B -> C Properties ---
    bc_num: bpy.props.IntProperty( # type: ignore[reportIncompatibleMethodOverride]
        name="Num",
        default=3,
        min=2,
        description="Numerator for B->C"
    )
    bc_den: bpy.props.IntProperty( # type: ignore[reportIncompatibleMethodOverride]
        name="Den",
        default=1,
        min=1,
        description="Denominator for B->C"
    )

    # --- C -> A Properties ---
    ca_num: bpy.props.IntProperty( # type: ignore[reportIncompatibleMethodOverride]
        name="Num",
        default=2,
        min=2,
        description="Numerator for C->A"
    )
    ca_den: bpy.props.IntProperty( # type: ignore[reportIncompatibleMethodOverride]
        name="Den",
        default=1,
        min=1,
        description="Denominator for C->A"
    )

    def draw(self, context):
        layout = self.layout
        
        # We use align=True to clip the numerator and denominator inputs together cleanly
        
        # Row for A -> B
        row_ab = layout.row(align=True)
        row_ab.label(text="A->B:")
        row_ab.prop(self, "ab_num")
        row_ab.prop(self, "ab_den")
        
        # Row for B -> C
        row_bc = layout.row(align=True)
        row_bc.label(text="B->C:")
        row_bc.prop(self, "bc_num")
        row_bc.prop(self, "bc_den")
        
        # Row for C -> A
        row_ca = layout.row(align=True)
        row_ca.label(text="C->A:")
        row_ca.prop(self, "ca_num")
        row_ca.prop(self, "ca_den")
        
        ringing = layout.row(align=True)
        ringing.prop(self, "ringing")

    def execute(self, context):
        # Calculate the floats to pass down to your Rust core library
        ab_val = self.ab_num / self.ab_den
        bc_val = self.bc_num / self.bc_den
        ca_val = self.ca_num / self.ca_den
        
        # Pass the processed float values to your Rust backend
        geometry = rust_core.generate_cube_geometry([self.ab_num,self.bc_num,self.ca_num], [self.ab_den, self.bc_den, self.ca_den], self.ringing)
        
        mesh = bpy.data.meshes.new("Rust_Cube_Mesh")
        obj = bpy.data.objects.new("Rust_Cube", mesh)
        context.collection.objects.link(obj)
        
        mesh.from_pydata(geometry.vertices, [], geometry.faces)
        mesh.update()
        
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(MESH_OT_rust_cube_generator.bl_idname, icon='MESH_CUBE')

def register():
    bpy.utils.register_class(MESH_OT_rust_cube_generator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func) # type: ignore[reportArgumentType]

def unregister():
    bpy.utils.unregister_class(MESH_OT_rust_cube_generator)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func) # type: ignore[reportArgumentType]

if __name__ == "__main__":
    register()

