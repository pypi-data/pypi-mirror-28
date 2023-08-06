# -*- coding:utf-8 -*-

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

# <pep8 compliant>

# ----------------------------------------------------------
# Author: Stephen Leger (s-leger)
#
# ----------------------------------------------------------

bl_info = {
    'name': 'Archipack',
    'description': 'Architectural objects and 2d polygons detection from unordered splines',
    'author': 's-leger',
    'license': 'GPL',
    'deps': 'shapely',
    'version': (1, 2, 5),
    'blender': (2, 7, 8),
    'location': 'View3D > Tools > Create > Archipack',
    'warning': '',
    'wiki_url': 'https://github.com/s-leger/archipack/wiki',
    'tracker_url': 'https://github.com/s-leger/archipack/issues',
    'link': 'https://github.com/s-leger/archipack',
    'support': 'COMMUNITY',
    'category': 'Add Mesh'
    }

import os

if "bpy" in locals():
    import importlib as imp
    imp.reload(archipack_snap)
    imp.reload(archipack_manipulator)
    imp.reload(archipack_reference_point)
    imp.reload(archipack_autoboolean)
    imp.reload(archipack_door)
    imp.reload(archipack_window)
    imp.reload(archipack_stair)
    imp.reload(archipack_wall)
    imp.reload(archipack_wall2)
    # imp.reload(archipack_roof2d)
    imp.reload(archipack_slab)
    imp.reload(archipack_fence)
    imp.reload(archipack_truss)
    # imp.reload(archipack_toolkit)
    imp.reload(archipack_floor)
    imp.reload(archipack_rendering)
    imp.reload(addon_updater_ops)
    try:
        imp.reload(archipack_polylib)
        HAS_POLYLIB = True
    except:
        HAS_POLYLIB = False
        pass

    print("archipack: reload ready")
else:
    from . import archipack_snap
    from . import archipack_manipulator
    from . import archipack_reference_point
    from . import archipack_autoboolean
    from . import archipack_door
    from . import archipack_window
    from . import archipack_stair
    from . import archipack_wall
    from . import archipack_wall2
    # from . import archipack_roof2d
    from . import archipack_slab
    from . import archipack_fence
    from . import archipack_truss
    # from . import archipack_toolkit
    from . import archipack_floor
    from . import archipack_rendering
    from . import addon_updater_ops
    try:
        """
            polylib depends on shapely
            raise ImportError when not meet
        """
        from . import archipack_polylib
        HAS_POLYLIB = True
    except:
        print("archipack: Polylib failed to load, missing shapely ?")
        HAS_POLYLIB = False
        pass

    print("archipack: ready")

# noinspection PyUnresolvedReferences
import bpy
# noinspection PyUnresolvedReferences
from bpy.types import (
    Panel, WindowManager, PropertyGroup,
    AddonPreferences, Menu
    )
from bpy.props import (
    EnumProperty, PointerProperty,
    StringProperty, BoolProperty,
    IntProperty, FloatProperty, FloatVectorProperty
    )

from bpy.utils import previews
icons_collection = {}


# ----------------------------------------------------
# Addon preferences
# ----------------------------------------------------

def update_panel(self, context):
    try:
        bpy.utils.unregister_class(TOOLS_PT_Archipack_PolyLib)
        bpy.utils.unregister_class(TOOLS_PT_Archipack_Tools)
        bpy.utils.unregister_class(TOOLS_PT_Archipack_Create)
    except:
        pass
    prefs = context.user_preferences.addons[__name__].preferences
    TOOLS_PT_Archipack_PolyLib.bl_category = prefs.tools_category
    bpy.utils.register_class(TOOLS_PT_Archipack_PolyLib)
    TOOLS_PT_Archipack_Tools.bl_category = prefs.tools_category
    bpy.utils.register_class(TOOLS_PT_Archipack_Tools)
    TOOLS_PT_Archipack_Create.bl_category = prefs.create_category
    bpy.utils.register_class(TOOLS_PT_Archipack_Create)


class Archipack_Pref(AddonPreferences):
    bl_idname = __name__

    tools_category = StringProperty(
        name="Tools",
        description="Choose a name for the category of the Tools panel",
        default="Tools",
        update=update_panel
    )
    create_category = StringProperty(
        name="Create",
        description="Choose a name for the category of the Create panel",
        default="Create",
        update=update_panel
    )
    create_submenu = BoolProperty(
        name="Use Sub-menu",
        description="Put Achipack's object into a sub menu (shift+a)",
        default=True
    )
    # Arrow sizes (world units)
    arrow_size = FloatProperty(
            name="Arrow",
            description="Manipulators arrow size (blender units)",
            default=0.05
            )
    # Handle area size (pixels)
    handle_size = IntProperty(
            name="Handle",
            description="Manipulators handle sensitive area size (pixels)",
            min=2,
            default=10
            )
    # Font sizes and basic colour scheme
    # kept outside of addon prefs until now
    # as for a generic toolkit it is not appropriate
    # we could provide a template for addon prefs
    # matching those one
    feedback_size_main = IntProperty(
            name="Main",
            description="Main title font size (pixels)",
            min=2,
            default=16
            )
    feedback_size_title = IntProperty(
            name="Title",
            description="Tool name font size (pixels)",
            min=2,
            default=14
            )
    feedback_size_shortcut = IntProperty(
            name="Shortcut",
            description="Shortcuts font size (pixels)",
            min=2,
            default=11
            )
    feedback_shortcut_area = FloatVectorProperty(
            name="Background Shortcut",
            description="Shortcut area background color",
            subtype='COLOR_GAMMA',
            default=(0, 0.4, 0.6, 0.2),
            size=4,
            min=0, max=1
            )
    feedback_title_area = FloatVectorProperty(
            name="Background Main",
            description="Title area background color",
            subtype='COLOR_GAMMA',
            default=(0, 0.4, 0.6, 0.5),
            size=4,
            min=0, max=1
            )
    feedback_colour_main = FloatVectorProperty(
            name="Font Main",
            description="Title color",
            subtype='COLOR_GAMMA',
            default=(0.95, 0.95, 0.95, 1.0),
            size=4,
            min=0, max=1
            )
    feedback_colour_key = FloatVectorProperty(
            name="Font Shortcut key",
            description="KEY label color",
            subtype='COLOR_GAMMA',
            default=(0.67, 0.67, 0.67, 1.0),
            size=4,
            min=0, max=1
            )
    feedback_colour_shortcut = FloatVectorProperty(
            name="Font Shortcut hint",
            description="Shortcuts text color",
            subtype='COLOR_GAMMA',
            default=(0.51, 0.51, 0.51, 1.0),
            size=4,
            min=0, max=1
            )

    # addon updater preferences

    auto_check_update = BoolProperty(
        name="Auto-check for Update",
        description="If enabled, auto-check for updates using an interval",
        default=False,
        )

    updater_intrval_months = IntProperty(
        name='Months',
        description="Number of months between checking for updates",
        default=0,
        min=0
        )
    updater_intrval_days = IntProperty(
        name='Days',
        description="Number of days between checking for updates",
        default=7,
        min=0,
        )
    updater_intrval_hours = IntProperty(
        name='Hours',
        description="Number of hours between checking for updates",
        default=0,
        min=0,
        max=23
        )
    updater_intrval_minutes = IntProperty(
        name='Minutes',
        description="Number of minutes between checking for updates",
        default=0,
        min=0,
        max=59
        )

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row = box.row()
        col = row.column()
        col.label(text="Tab Category:")
        col.prop(self, "tools_category")
        col.prop(self, "create_category")
        col.prop(self, "create_submenu")
        box = layout.box()
        row = box.row()
        split = row.split(percentage=0.5)
        col = split.column()
        col.label(text="Colors:")
        row = col.row(align=True)
        row.prop(self, "feedback_title_area")
        row = col.row(align=True)
        row.prop(self, "feedback_shortcut_area")
        row = col.row(align=True)
        row.prop(self, "feedback_colour_main")
        row = col.row(align=True)
        row.prop(self, "feedback_colour_key")
        row = col.row(align=True)
        row.prop(self, "feedback_colour_shortcut")
        col = split.column()
        col.label(text="Font size:")
        col.prop(self, "feedback_size_main")
        col.prop(self, "feedback_size_title")
        col.prop(self, "feedback_size_shortcut")
        col.label(text="Manipulators:")
        col.prop(self, "arrow_size")
        col.prop(self, "handle_size")
        addon_updater_ops.update_settings_ui(self, context)


# ----------------------------------------------------
# Archipack panels
# ----------------------------------------------------


class TOOLS_PT_Archipack_PolyLib(Panel):
    bl_label = "Archipack 2d to 3d"
    bl_idname = "TOOLS_PT_Archipack_PolyLib"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"

    @classmethod
    def poll(self, context):

        global archipack_polylib
        return HAS_POLYLIB and ((archipack_polylib.vars_dict['select_polygons'] is not None) or
                (context.object is not None and context.object.type == 'CURVE'))

    def draw(self, context):
        global icons_collection
        icons = icons_collection["main"]
        layout = self.layout
        row = layout.row(align=True)
        box = row.box()
        row = box.row(align=True)
        row.operator(
            "archipack.polylib_detect",
            icon_value=icons["detect"].icon_id,
            text='Detect'
            ).extend = context.window_manager.archipack_polylib.extend
        row.prop(context.window_manager.archipack_polylib, "extend")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "resolution")
        row = box.row(align=True)
        row.label(text="Polygons")
        row = box.row(align=True)
        row.operator(
            "archipack.polylib_pick_2d_polygons",
            icon_value=icons["selection"].icon_id,
            text='Select'
            ).action = 'select'
        row.operator(
            "archipack.polylib_pick_2d_polygons",
            icon_value=icons["union"].icon_id,
            text='Union'
            ).action = 'union'
        row.operator(
            "archipack.polylib_output_polygons",
            icon_value=icons["polygons"].icon_id,
            text='All')
        row = box.row(align=True)
        row.operator(
            "archipack.polylib_pick_2d_polygons",
            text='Wall',
            icon_value=icons["wall"].icon_id).action = 'wall'
        row.prop(context.window_manager.archipack_polylib, "solidify_thickness")
        row = box.row(align=True)
        row.operator("archipack.polylib_pick_2d_polygons",
            text='Window',
            icon_value=icons["window"].icon_id).action = 'window'
        row.operator("archipack.polylib_pick_2d_polygons",
            text='Door',
            icon_value=icons["door"].icon_id).action = 'door'
        row.operator("archipack.polylib_pick_2d_polygons", text='Rectangle').action = 'rectangle'
        row = box.row(align=True)
        row.label(text="Lines")
        row = box.row(align=True)
        row.operator(
            "archipack.polylib_pick_2d_lines",
            icon_value=icons["selection"].icon_id,
            text='Lines').action = 'select'
        row.operator(
            "archipack.polylib_pick_2d_lines",
            icon_value=icons["union"].icon_id,
            text='Union').action = 'union'
        row.operator(
            "archipack.polylib_output_lines",
            icon_value=icons["polygons"].icon_id,
            text='All')
        # row = layout.row(align=True)
        # box = row.box()
        # row = box.row(align=True)
        # row.operator("archipack.polylib_solidify")
        row = box.row(align=True)
        row.label(text="Points")
        row = box.row(align=True)
        row.operator(
            "archipack.polylib_pick_2d_points",
            icon_value=icons["selection"].icon_id,
            text='Points').action = 'select'
        row = layout.row(align=True)
        box = row.box()
        row = box.row(align=True)
        row.operator("archipack.polylib_simplify")
        row.prop(context.window_manager.archipack_polylib, "simplify_tolerance")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "simplify_preserve_topology")
        row = layout.row(align=True)
        box = row.box()
        row = box.row(align=True)
        row.operator("archipack.polylib_offset")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "offset_distance")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "offset_side")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "offset_resolution")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "offset_join_style")
        row = box.row(align=True)
        row.prop(context.window_manager.archipack_polylib, "offset_mitre_limit")


class TOOLS_PT_Archipack_Tools(Panel):
    bl_label = "Archipack Tools"
    bl_idname = "TOOLS_PT_Archipack_Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Tools"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        wm = context.window_manager
        layout = self.layout
        row = layout.row(align=True)
        box = row.box()
        box.label("Auto boolean")
        row = box.row(align=True)
        # row.operator("archipack.auto_boolean", text="Robust", icon='HAND').mode = 'ROBUST'
        # row.operator("archipack.auto_boolean", text="Interactive", icon='AUTO').mode = 'INTERACTIVE'
        row.operator("archipack.auto_boolean", text="AutoBoolean", icon='AUTO').mode = 'HYBRID'
        row = layout.row(align=True)
        box = row.box()
        box.label("Rendering")
        row = box.row(align=True)
        row.prop(wm.archipack, 'render_type', text="")
        row = box.row(align=True)
        row.operator("archipack.render", icon='RENDER_STILL')


class TOOLS_PT_Archipack_Create(Panel):
    bl_label = "Add Archipack"
    bl_idname = "TOOLS_PT_Archipack_Create"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Create"

    @classmethod
    def poll(self, context):
        return True

    def draw(self, context):
        global icons_collection

        addon_updater_ops.check_for_update_background(context)

        icons = icons_collection["main"]
        layout = self.layout
        row = layout.row(align=True)
        box = row.box()
        box.label("Objects")
        row = box.row(align=True)
        # col = row.column()
        # subrow = col.row(align=True)
        row.operator("archipack.window_preset_menu",
                    text="Window",
                    icon_value=icons["window"].icon_id
                    ).preset_operator = "archipack.window"
        row.operator("archipack.window_preset_menu",
                    text="",
                    icon='GREASEPENCIL'
                    ).preset_operator = "archipack.window_draw"
        # col = row.column()
        # subrow = col.row(align=True)
        row = box.row(align=True)
        row.operator("archipack.door_preset_menu",
                    text="Door",
                    icon_value=icons["door"].icon_id
                    ).preset_operator = "archipack.door"
        row.operator("archipack.door_preset_menu",
                    text="",
                    icon='GREASEPENCIL'
                    ).preset_operator = "archipack.door_draw"
        row = box.row(align=True)
        row.operator("archipack.stair_preset_menu",
                    text="Stair",
                    icon_value=icons["stair"].icon_id
                    ).preset_operator = "archipack.stair"
        row = box.row(align=True)
        row.operator("archipack.wall2",
                    icon_value=icons["wall"].icon_id
                    )
        row.operator("archipack.wall2_draw", text="Draw", icon='GREASEPENCIL')
        row.operator("archipack.wall2_from_curve", text="", icon='CURVE_DATA')

        row = box.row(align=True)
        row.operator("archipack.fence_preset_menu",
                    text="Fence",
                    icon_value=icons["fence"].icon_id
                    ).preset_operator = "archipack.fence"
        row.operator("archipack.fence_from_curve", text="", icon='CURVE_DATA')
        row = box.row(align=True)
        row.operator("archipack.truss",
                    icon_value=icons["truss"].icon_id
                    )
        row = box.row(align=True)
        row.operator("archipack.slab_from_curve",
                    icon_value=icons["slab"].icon_id
                    )

        row = box.row(align=True)
        row.operator("archipack.wall2_from_slab",
                    icon_value=icons["wall"].icon_id)
        row.operator("archipack.slab_from_wall",
                    icon_value=icons["slab"].icon_id
                    ).ceiling = False
        row.operator("archipack.slab_from_wall",
                    text="->Ceiling",
                    icon_value=icons["slab"].icon_id
                    ).ceiling = True

        addon_updater_ops.update_notice_box_ui(self, context)

        # row = box.row(align=True)
        # row.operator("archipack.roof", icon='CURVE_DATA')

        # toolkit
        # row = box.row(align=True)
        # row.operator("archipack.myobject")

        row = box.row(align=True)
        row.operator("archipack.floor_preset_menu",
                    text="Floor",
                    icon_value=icons["floor"].icon_id
                    ).preset_operator = "archipack.floor"

# ----------------------------------------------------
# ALT + A menu
# ----------------------------------------------------


def draw_menu(self, context):
    global icons_collection
    icons = icons_collection["main"]
    layout = self.layout
    layout.operator_context = 'INVOKE_REGION_WIN'

    layout.operator("archipack.wall2",
                    text="Wall",
                    icon_value=icons["wall"].icon_id
                    )
    layout.operator("archipack.window_preset_menu",
                    text="Window",
                    icon_value=icons["window"].icon_id
                    ).preset_operator = "archipack.window"
    layout.operator("archipack.door_preset_menu",
                    text="Door",
                    icon_value=icons["door"].icon_id
                    ).preset_operator = "archipack.door"
    layout.operator("archipack.stair_preset_menu",
                    text="Stair",
                    icon_value=icons["stair"].icon_id
                    ).preset_operator = "archipack.stair"
    layout.operator("archipack.fence_preset_menu",
                    text="Fence",
                    icon_value=icons["fence"].icon_id
                    ).preset_operator = "archipack.fence"
    layout.operator("archipack.truss",
                    text="Truss",
                    icon_value=icons["truss"].icon_id
                    )
    layout.operator("archipack.floor_preset_menu",
                    text="Floor",
                    icon_value=icons["floor"].icon_id
                    )


class ARCHIPACK_create_menu(Menu):
    bl_label = 'Archipack'
    bl_idname = 'ARCHIPACK_create_menu'

    def draw(self, context):
        draw_menu(self, context)


def menu_func(self, context):
    layout = self.layout
    layout.separator()
    global icons_collection
    icons = icons_collection["main"]

    # either draw sub menu or right at end of this one
    if context.user_preferences.addons[__name__].preferences.create_submenu:
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.menu("ARCHIPACK_create_menu", icon_value=icons["archipack"].icon_id)
    else:
        draw_menu(self, context)


# ----------------------------------------------------
# Datablock to store global addon variables
# ----------------------------------------------------


class archipack_data(PropertyGroup):
    render_type = EnumProperty(
        items=(
            ('1', "Draw over", "Draw over last rendered image"),
            ('2', "OpenGL", ""),
            ('3', "Animation OpenGL", ""),
            ('4', "Image", "Render image and draw over"),
            ('5', "Animation", "Draw on each frame")
            ),
        name="Render type",
        description="Render method"
        )


def register():
    global icons_collection
    icons = previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    for icon in os.listdir(icons_dir):
        name, ext = os.path.splitext(icon)
        icons.load(name, os.path.join(icons_dir, icon), 'IMAGE')
    icons_collection["main"] = icons

    archipack_snap.register()
    archipack_manipulator.register()
    archipack_reference_point.register()
    archipack_autoboolean.register()
    archipack_door.register()
    archipack_window.register()
    archipack_stair.register()
    archipack_wall.register()
    archipack_wall2.register()
    # archipack_roof2d.register()
    archipack_slab.register()
    archipack_fence.register()
    archipack_truss.register()
    # archipack_toolkit.register()
    archipack_floor.register()
    archipack_rendering.register()

    if HAS_POLYLIB:
        archipack_polylib.register()

    bpy.utils.register_class(archipack_data)
    WindowManager.archipack = PointerProperty(type=archipack_data)
    bpy.utils.register_class(Archipack_Pref)
    update_panel(None, bpy.context)
    bpy.utils.register_class(ARCHIPACK_create_menu)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

    addon_updater_ops.register(bl_info)
    # bpy.utils.register_module(__name__)


def unregister():
    global icons_collection
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(ARCHIPACK_create_menu)

    bpy.utils.unregister_class(TOOLS_PT_Archipack_PolyLib)
    bpy.utils.unregister_class(TOOLS_PT_Archipack_Tools)
    bpy.utils.unregister_class(TOOLS_PT_Archipack_Create)
    bpy.utils.unregister_class(Archipack_Pref)
    # unregister subs
    archipack_snap.unregister()
    archipack_manipulator.unregister()
    archipack_reference_point.unregister()
    archipack_autoboolean.unregister()
    archipack_door.unregister()
    archipack_window.unregister()
    archipack_stair.unregister()
    archipack_wall.unregister()
    archipack_wall2.unregister()
    # archipack_roof2d.unregister()
    archipack_slab.unregister()
    archipack_fence.unregister()
    archipack_truss.unregister()
    # archipack_toolkit.unregister()
    archipack_floor.unregister()
    archipack_rendering.unregister()

    if HAS_POLYLIB:
        archipack_polylib.unregister()

    bpy.utils.unregister_class(archipack_data)
    del WindowManager.archipack

    for icons in icons_collection.values():
        previews.remove(icons)
    icons_collection.clear()

    addon_updater_ops.unregister()

    # bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()

