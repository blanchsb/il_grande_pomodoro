# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# This addon was created with the Serpens - Visual Scripting Addon.
# This code is generated from nodes and is not intended for manual editing.
# You can find out more about Serpens at <https://blendermarket.com/products/serpens>.


bl_info = {
    "name": "IL GRANDE POMODORO",
    "description": "Useful set of Time Based Applications (Project Tracker and Pomodoro Timer) to help you keep track of your time spent in each blender Project.",
    "author": "Shawn Blanch (blanchsb)",
    "version": (1, 0, 0),
    "blender": (2, 92, 0),
    "location": "View 3D and Scene Properties",
    "warning": "Recommend to use a Save option if enabling Notifications. The file will only save if there is an existing file path.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "3D View"
}


###############   IMPORTS
import bpy
from bpy.utils import previews
import os
import math
from bpy.app.handlers import persistent
from datetime import datetime
import random


###############   INITALIZE VARIABLES
fn__end_tracking = {
    "var_temp_session_time_min": 0, 
    }
pomodoro = {
    "pomo_toggle": False, 
    "pomo_notify": False, 
    "pomo_minutes": 0, 
    "pomos_completed": 0, 
    "pomo_big_break_count": 0, 
    "pomo_chef_list": [], 
    "pomo_chef_messages_break": [], 
    "pomo_chef_messages_work": [], 
    "pomo_chef_message_break": "A break is worth a thousand works ", 
    "pomo_chef_message_work": "Slice and Dice be working soo nice ", 
    }


###############   SERPENS FUNCTIONS
def exec_line(line):
    exec(line)

def sn_print(tree_name, *args):
    if tree_name in bpy.data.node_groups:
        item = bpy.data.node_groups[tree_name].sn_graphs[0].prints.add()
        for arg in args:
            item.value += str(arg) + ";;;"
        if bpy.context and bpy.context.screen:
            for area in bpy.context.screen.areas:
                area.tag_redraw()
    print(*args)

def sn_cast_string(value):
    return str(value)

def sn_cast_boolean(value):
    if type(value) == tuple:
        for data in value:
            if bool(data):
                return True
        return False
    return bool(value)

def sn_cast_float(value):
    if type(value) == str:
        try:
            value = float(value)
            return value
        except:
            return float(bool(value))
    elif type(value) == tuple:
        return float(value[0])
    elif type(value) == list:
        return float(len(value))
    elif not type(value) in [float, int, bool]:
        try:
            value = len(value)
            return float(value)
        except:
            return float(bool(value))
    return float(value)

def sn_cast_int(value):
    return int(sn_cast_float(value))

def sn_cast_boolean_vector(value, size):
    if type(value) in [str, bool, int, float]:
        return_value = []
        for i in range(size):
            return_value.append(bool(value))
        return tuple(return_value)
    elif type(value) == tuple:
        return_value = []
        for i in range(size):
            return_value.append(bool(value[i]) if len(value) > i else bool(value[0]))
        return tuple(return_value)
    elif type(value) == list:
        return sn_cast_boolean_vector(tuple(value), size)
    else:
        try:
            value = tuple(value)
            return sn_cast_boolean_vector(value, size)
        except:
            return sn_cast_boolean_vector(bool(value), size)

def sn_cast_float_vector(value, size):
    if type(value) in [str, bool, int, float]:
        return_value = []
        for i in range(size):
            return_value.append(sn_cast_float(value))
        return tuple(return_value)
    elif type(value) == tuple:
        return_value = []
        for i in range(size):
            return_value.append(sn_cast_float(value[i]) if len(value) > i else sn_cast_float(value[0]))
        return tuple(return_value)
    elif type(value) == list:
        return sn_cast_float_vector(tuple(value), size)
    else:
        try:
            value = tuple(value)
            return sn_cast_float_vector(value, size)
        except:
            return sn_cast_float_vector(sn_cast_float(value), size)

def sn_cast_int_vector(value, size):
    return tuple(map(int, sn_cast_float_vector(value, size)))

def sn_cast_color(value, use_alpha):
    length = 4 if use_alpha else 3
    value = sn_cast_float_vector(value, length)
    tuple_list = []
    for data in range(length):
        data = value[data] if len(value) > data else value[0]
        tuple_list.append(sn_cast_float(min(1, max(0, data))))
    return tuple(tuple_list)

def sn_cast_list(value):
    if type(value) in [str, tuple, list]:
        return list(value)
    elif type(value) in [int, float, bool]:
        return [value]
    else:
        try:
            value = list(value)
            return value
        except:
            return [value]

def sn_cast_blend_data(value):
    if hasattr(value, "bl_rna"):
        return value
    elif type(value) in [tuple, bool, int, float, list]:
        return None
    elif type(value) == str:
        try:
            value = eval(value)
            return value
        except:
            return None
    else:
        return None

def sn_cast_enum(string, enum_values):
    for item in enum_values:
        if item[1] == string:
            return item[0]
        elif item[0] == string.upper():
            return item[0]
    return string


###############   IMPERATIVE CODE
#######   IL GRANDE POMODORO
@persistent
def save_pre_handler_465EE(dummy):
    function_return_3024F = fn_end_tracking()
    sn_redraw()

def changelog_interface_snippet_ED613(layout, changes_list, icon, ):
    try:


        layout.label(text=(r"Changelog for Version " + sn_cast_string(bl_info["version"]).replace(r"(", r"").replace(r")", r"").replace(r",", r".") + r" :"),icon_value=0)
        if sn_cast_boolean(changes_list):
            for_node_F9F28 = 0
            for_node_index_F9F28 = 0
            for for_node_index_F9F28, for_node_F9F28 in enumerate(sn_cast_list(changes_list)):
                layout.label(text=sn_cast_string(for_node_F9F28),icon_value=icon)
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function Changelog Interface")

def sn_redraw():
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()

def update_pomo_big_break_amount_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount = self.pomo_big_break_amount
    sn_redraw()

def update_pomo_big_break_time_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomo_big_break_time = self.pomo_big_break_time
    sn_redraw()

def update_pomo_user_notify_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify = self.pomo_user_notify
    sn_redraw()

def update_pomo_work_time_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomo_work_time = self.pomo_work_time
    sn_redraw()

def update_pomo_break_time_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomo_break_time = self.pomo_break_time
    sn_redraw()

def update_pomo_save_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomodoro_save = self.pomo_save
    sn_redraw()

def update_pomo_save_single_copy_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy = self.pomo_save_single_copy
    sn_redraw()

def update_pomo_save_dated_copy_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_dated_copy = self.pomo_save_dated_copy
    sn_redraw()

def update_pomo_run_on_load_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomodoro_run_on_load = self.pomo_run_on_load
    sn_redraw()

def update_pomo_user_notify_and_pause_BA4EB(self, context):
    sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause = self.pomo_user_notify_and_pause
    sn_redraw()


@persistent
def load_post_handler_8F2AE(dummy):
    pass # Script_Addon_Prefs_Setup.py Script Start
    #Set Properties from Pomodoro Addon Preferences on File Load
    bpy.context.scene.pomo_work_time = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_work_time
    bpy.context.scene.pomo_break_time = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_break_time
    bpy.context.scene.pomo_big_break_amount = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_big_break_amount
    bpy.context.scene.pomo_big_break_time = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_big_break_time
    bpy.context.scene.pomodoro_save = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_save
    bpy.context.scene.pomodoro_save_a_single_copy = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_save_single_copy
    bpy.context.scene.pomodoro_save_a_dated_copy = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_save_dated_copy
    bpy.context.scene.pomodoro_user_notify = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_user_notify
    bpy.context.scene.pomodoro_notify_and_pause = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_user_notify_and_pause
    bpy.context.scene.pomodoro_run_on_load = bpy.context.preferences.addons['il_grande_pomodoro'].preferences.pomo_run_on_load
    pass # Script_Addon_Prefs_Setup.py Script End
    function_return_07F5D = fn_start_tracking_and_set_prev_session()
    if sn_cast_blend_data(bpy.context.scene).pomodoro_run_on_load:
        bpy.ops.sna.start_pomodoro("INVOKE_DEFAULT",)
    else:
        pass
    function_return_E77E0 = fn_first_pass_pomodoro()
    sn_redraw()


#######   UI FN Addon Prefs Project Tracker
def ui_fn_addon_prefs_proj_timer(layout, ):
    try:
        row = layout.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=(r"Total Time: " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).total_time_min)),icon_value=bpy.context.scene.il_grande_pomodoro_icons['TOTAL_TIME'].icon_id)
        if sn_cast_blend_data(bpy.context.scene).total_time_min != 0:
            op = row.operator("sna.reset_total_time",text=r"",emboss=True,depress=False,icon_value=715)
        else:
            pass
        row = layout.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=(r"Session Time: " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).session_time_min)),icon_value=bpy.context.scene.il_grande_pomodoro_icons['SESSION_TIME'].icon_id)
        if sn_cast_blend_data(bpy.context.scene).session_time_min != 0:
            op = row.operator("sna.reset_session_time",text=r"",emboss=True,depress=False,icon_value=715)
        else:
            pass
        row = layout.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=(r"Prev. Session Time: " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).prev_session_time_min)),icon_value=bpy.context.scene.il_grande_pomodoro_icons['PREV_TIME'].icon_id)
        if sn_cast_blend_data(bpy.context.scene).prev_session_time_min != 0:
            op = row.operator("sna.reset_prev_session_time",text=r"",emboss=True,depress=False,icon_value=715)
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Addon Prefs Proj Timer")


#######   UI FN - DEBUGGER
def ui_fn_debugger(layout, ):
    try:
        col = layout.column(align=False)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.0
        col.prop(sn_cast_blend_data(bpy.context.scene),'opened_or_saved_date_vec3_yymd',icon_value=0,text=r"Opened or Saved Date Vec3 (YYMD)",emboss=True,slider=False,)
        col.prop(sn_cast_blend_data(bpy.context.scene),'opened_or_saved_time_vec3_hms',icon_value=0,text=r"Opened or Saved Time Vec3 (HMS)",emboss=True,slider=False,)
        col.separator(factor=1.0)
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 2.0
        op = col.operator("sna.ot_start_tracking",text=r"Start Tracking",emboss=True,depress=False,icon_value=bpy.context.scene.il_grande_pomodoro_icons['GREEN_CLOCK'].icon_id)
        op = col.operator("sna.ot_end_tracking",text=r"End Tracking",emboss=True,depress=False,icon_value=bpy.context.scene.il_grande_pomodoro_icons['RED_CLOCK'].icon_id)
        col.separator(factor=1.0)
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.5
        col.prop(sn_cast_blend_data(bpy.context.scene),'opened_or_saved_time_min',icon_value=0,text=r"Opened or Saved Time (Min)",emboss=True,slider=False,)
        col.prop(sn_cast_blend_data(bpy.context.scene),'total_time_min',icon_value=0,text=r"Total Time (min)",emboss=True,slider=False,)
        col.prop(sn_cast_blend_data(bpy.context.scene),'session_time_min',icon_value=0,text=r"Session Time (Min)",emboss=True,slider=False,)
        col.prop(sn_cast_blend_data(bpy.context.scene),'prev_session_time_min',icon_value=0,text=r"Prev Session Time (Min)",emboss=True,slider=False,)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN DEBUGGER")


#######   FN - Start Tracking
def sn_redraw():
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()

def fn_start_tracking():
    try:
        function_return_4FE6E = fn_get_time()
        sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_vec3_hms = function_return_4FE6E[0]
        sn_cast_blend_data(bpy.context.scene).opened_or_saved_date_vec3_yymd = function_return_4FE6E[1]
        sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min = function_return_4FE6E[2]
        sn_redraw()
    except Exception as exc:
        print(str(exc) + " | Error in function FN Start Tracking")


#######   FN - End Tracking
def fn_reset_temp_session_time():
    try:
        fn__end_tracking["var_temp_session_time_min"] = 0
    except Exception as exc:
        print(str(exc) + " | Error in function FN Reset Temp Session Time")

def sn_branch(v1,v2,condition):
    if condition:
        return v1
    return v2

def sn_redraw():
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()

def fn_end_tracking():
    try:
        function_return_7232F = fn_get_time()
        sn_cast_blend_data(bpy.context.scene).current_time_min = function_return_7232F[2]
        if sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min == 0:
            sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min = sn_cast_blend_data(bpy.context.scene).current_time_min
        else:
            pass
        sn_cast_blend_data(bpy.context.scene).total_time_min = int((sn_cast_float(sn_branch(int((sn_cast_float(int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).current_time_min) + 1440.0))) - sn_cast_float(sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min))),int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).current_time_min) - sn_cast_float(sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min))),sn_cast_blend_data(bpy.context.scene).current_time_min < sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min)) + sn_cast_float(sn_cast_blend_data(bpy.context.scene).total_time_min)))
        fn__end_tracking["var_temp_session_time_min"] = int((sn_cast_float(sn_branch(int((sn_cast_float(int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).current_time_min) + 1440.0))) - sn_cast_float(sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min))),int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).current_time_min) - sn_cast_float(sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min))),sn_cast_blend_data(bpy.context.scene).current_time_min < sn_cast_blend_data(bpy.context.scene).opened_or_saved_time_min)) + sn_cast_float(fn__end_tracking["var_temp_session_time_min"])))
        sn_cast_blend_data(bpy.context.scene).session_time_min = fn__end_tracking["var_temp_session_time_min"]
        function_return_56CAA = fn_start_tracking()
        sn_redraw()
    except Exception as exc:
        print(str(exc) + " | Error in function FN End Tracking")


#######   FN - Start Tracking and Set Prev Session
def fn_start_tracking_and_set_prev_session():
    try:
        function_return_CE58F = fn_start_tracking()
        sn_cast_blend_data(bpy.context.scene).prev_session_time_min = sn_cast_blend_data(bpy.context.scene).session_time_min
    except Exception as exc:
        print(str(exc) + " | Error in function FN Start Tracking and Set Prev Session")


#######   FN - Get Time
def fn_get_time():
    try:
        return sn_cast_int_vector((datetime.now().time().hour,datetime.now().time().minute,datetime.now().time().second,), 3), (datetime.now().date().year,datetime.now().date().month,datetime.now().date().day,), int((sn_cast_float(int((sn_cast_float(sn_cast_int_vector((datetime.now().time().hour,datetime.now().time().minute,datetime.now().time().second,), 3)[0]) * 60.0))) + sn_cast_float(sn_cast_int_vector((datetime.now().time().hour,datetime.now().time().minute,datetime.now().time().second,), 3)[1]))), 
    except Exception as exc:
        print(str(exc) + " | Error in function FN Get Time")


#######   Pomodoro
def sn_branch(v1,v2,condition):
    if condition:
        return v1
    return v2

def ui_fn_pomodoro_add_to_menu(layout, ):
    try:
        op = layout.operator("sna.toggle_pomodoro",text=sn_cast_string(sn_branch(r"Start",sn_branch(int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) - sn_cast_float(pomodoro["pomo_minutes"]))),sn_branch(r"Start",sn_branch(int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_break_time) - sn_cast_float(pomodoro["pomo_minutes"]))),int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_big_break_time) - sn_cast_float(pomodoro["pomo_minutes"]))),pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount),(sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_notify"])),not sn_cast_blend_data(bpy.context.scene).pomo_break_active),(not sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_notify"]))),emboss=False,depress=False,icon_value=sn_cast_int(bpy.context.scene.il_grande_pomodoro_icons['POMO_STOPPED'].icon_id if (not pomodoro["pomo_toggle"] and not pomodoro["pomo_notify"]) else bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id if (not pomodoro["pomo_toggle"] and pomodoro["pomo_notify"] and sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMOS_BIG_COMPLETED'].icon_id if (not pomodoro["pomo_toggle"] and pomodoro["pomo_notify"] and sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] >= sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id if (sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMO_BIG_BREAK'].icon_id if (sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] >= sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMO_5'].icon_id if (not pomodoro["pomo_toggle"] and pomodoro["pomo_notify"] and not sn_cast_blend_data(bpy.context.scene).pomo_break_active) else bpy.context.scene.il_grande_pomodoro_icons['POMO_4'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.800000011920929)) and pomodoro["pomo_minutes"] < sn_cast_blend_data(bpy.context.scene).pomo_work_time) else bpy.context.scene.il_grande_pomodoro_icons['POMO_3'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.6000000238418579)) and pomodoro["pomo_minutes"] < int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.800000011920929))) else bpy.context.scene.il_grande_pomodoro_icons['POMO_2'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.4000000059604645)) and pomodoro["pomo_minutes"] < int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.6000000238418579))) else bpy.context.scene.il_grande_pomodoro_icons['POMO_1'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.20000000298023224)) and pomodoro["pomo_minutes"] < int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.4000000059604645))) else bpy.context.scene.il_grande_pomodoro_icons['POMO_0'].icon_id))
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Add to Menu")

def ui_fn_reset_pomodoro(layout, ):
    try:
        row = layout.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        op = row.operator("sna.reset_pomodoro",text=r"",emboss=True,depress=False,icon_value=715)
        row.label(text=r"  Reset Pomodoro",icon_value=0)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Reset Pomodoro")

def ui_fn_pomodoro(layout, ):
    try:
        box = layout.box()
        box.enabled = True
        box.alert = False
        box.scale_x = 1.0
        box.scale_y = 1.0
        box.label(text=r"Grande Pomodoro",icon_value=0)
        row = box.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.5
        split = row.split(align=False,factor=0.25)
        split.enabled = True
        split.alert = False
        split.scale_x = 1.0
        split.scale_y = 1.0
        op = split.operator("sna.toggle_pomodoro",text=sn_cast_string(sn_branch(r"Start",sn_branch(int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) - sn_cast_float(pomodoro["pomo_minutes"]))),sn_branch(r"Start",sn_branch(int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_break_time) - sn_cast_float(pomodoro["pomo_minutes"]))),int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_big_break_time) - sn_cast_float(pomodoro["pomo_minutes"]))),pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount),(sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_notify"])),not sn_cast_blend_data(bpy.context.scene).pomo_break_active),(not sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_notify"]))),emboss=True,depress=False,icon_value=sn_cast_int(bpy.context.scene.il_grande_pomodoro_icons['POMO_STOPPED'].icon_id if (not pomodoro["pomo_toggle"] and not pomodoro["pomo_notify"]) else bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id if (not pomodoro["pomo_toggle"] and pomodoro["pomo_notify"] and sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMOS_BIG_COMPLETED'].icon_id if (not pomodoro["pomo_toggle"] and pomodoro["pomo_notify"] and sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] >= sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id if (sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMO_BIG_BREAK'].icon_id if (sn_cast_blend_data(bpy.context.scene).pomo_break_active and pomodoro["pomo_big_break_count"] >= sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount) else bpy.context.scene.il_grande_pomodoro_icons['POMO_5'].icon_id if (not pomodoro["pomo_toggle"] and pomodoro["pomo_notify"] and not sn_cast_blend_data(bpy.context.scene).pomo_break_active) else bpy.context.scene.il_grande_pomodoro_icons['POMO_4'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.800000011920929)) and pomodoro["pomo_minutes"] < sn_cast_blend_data(bpy.context.scene).pomo_work_time) else bpy.context.scene.il_grande_pomodoro_icons['POMO_3'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.6000000238418579)) and pomodoro["pomo_minutes"] < int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.800000011920929))) else bpy.context.scene.il_grande_pomodoro_icons['POMO_2'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.4000000059604645)) and pomodoro["pomo_minutes"] < int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.6000000238418579))) else bpy.context.scene.il_grande_pomodoro_icons['POMO_1'].icon_id if (pomodoro["pomo_minutes"] >= int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.20000000298023224)) and pomodoro["pomo_minutes"] < int((sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomo_work_time) * 0.4000000059604645))) else bpy.context.scene.il_grande_pomodoro_icons['POMO_0'].icon_id))
        split.label(text=sn_cast_string(sn_branch(r"Pomodoro Break",sn_branch(r"Pomodoro Active",r"Pomodoro Stopped",pomodoro["pomo_toggle"]),(pomodoro["pomo_toggle"] and sn_cast_blend_data(bpy.context.scene).pomo_break_active))),icon_value=0)
        box.separator(factor=1.0)
        box.label(text=r"Muro di Pomodori",icon_value=0)
        box.label(text=sn_cast_string((r"Your Kitchen Rank:  " + sn_cast_blend_data(bpy.context.scene).pomo_chef_earned + r"")),icon_value=bpy.context.scene.il_grande_pomodoro_icons['CHEFS_HAT'].icon_id)
        box.label(text=sn_cast_string(sn_branch((sn_cast_string(sn_cast_blend_data(bpy.context.scene).pomodoros_completed) + r" Pomodoros Sliced and Diced" + r""),sn_branch((sn_cast_string(sn_cast_blend_data(bpy.context.scene).pomodoros_completed) + r" Pomodoro Sliced and Diced" + r""),r"Build il Muro di Pomodori",sn_cast_blend_data(bpy.context.scene).pomodoros_completed > 0),sn_cast_blend_data(bpy.context.scene).pomodoros_completed > 1)),icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id if sn_cast_blend_data(bpy.context.scene).pomodoros_completed > 0 else bpy.context.scene.il_grande_pomodoro_icons['POMO_0'].icon_id)
        ui_fn_pomodoro_tracker(box, )
        box.separator(factor=1.0)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro")

def sn_redraw():
    if bpy.context and bpy.context.screen:
        for a in bpy.context.screen.areas:
            a.tag_redraw()

def fn_pomo_back_to_work():
    try:
        if sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify:
            bpy.ops.sna.back_to_work("INVOKE_DEFAULT",)
        else:
            bpy.ops.sna.back_to_work("EXEC_DEFAULT",)
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomo Back to Work")

def fn_pomo_take_a_break():
    try:
        if sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify:
            bpy.ops.sna.take_a_break("INVOKE_DEFAULT",)
        else:
            bpy.ops.sna.take_a_break("EXEC_DEFAULT",)
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomo Take a Break")

def fn_pomo_big_break():
    try:
        if sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify:
            bpy.ops.sna.oh_yeah_big_break("INVOKE_DEFAULT",)
        else:
            bpy.ops.sna.oh_yeah_big_break("EXEC_DEFAULT",)
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomo Big Break")

def fn_pomodoro_save():
    try:
        if sn_cast_blend_data(bpy.context.scene).pomodoro_save:
            if sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy:
                if sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_dated_copy:
                    print(r"File saved to ", os.path.join(sn_cast_string(os.path.dirname(bpy.data.filepath)),sn_cast_string((sn_cast_string(os.path.basename(bpy.data.filepath).split(r".blend")[0]) + r"_" + str(datetime.now().date()).replace(r"-", r"") + r"_" + str(datetime.now().time()).split(".")[0].replace(r":", r"") + r".blend"))))
                    function_return_1D8A3 = fn_pomodoro_save_a_dated_copy_at_break()
                else:
                    print(r"File saved to ", os.path.join(sn_cast_string(os.path.dirname(bpy.data.filepath)),sn_cast_string((sn_cast_string(os.path.basename(bpy.data.filepath).split(r".blend")[0]) + r"_" + r"copy" + r".blend"))))
                    function_return_6F2EF = fn_pomodoro_save_a_copy_at_break()
            else:
                print(r"File saved to ", bpy.data.filepath)
                function_return_4D28C = fn_pomodoro_save_at_break()
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomodoro Save")

def fn_first_pass_pomodoro():
    try:
        sn_cast_blend_data(bpy.context.scene).pomodoro_scene_loaded = True
        pomodoro["pomo_minutes"] = 0
        sn_cast_blend_data(bpy.context.scene).pomo_break_active = False
        sn_redraw()
    except Exception as exc:
        print(str(exc) + " | Error in function FN First Pass Pomodoro")

def fn_pomodoro_save_a_dated_copy_at_break():
    try:
        if os.path.exists(bpy.data.filepath):
            bpy.ops.wm.save_as_mainfile("EXEC_DEFAULT",filepath=os.path.join(sn_cast_string(os.path.dirname(bpy.data.filepath)),sn_cast_string((sn_cast_string(os.path.basename(bpy.data.filepath).split(r".blend")[0]) + r"_" + str(datetime.now().date()).replace(r"-", r"") + r"_" + str(datetime.now().time()).split(".")[0].replace(r":", r"") + r".blend"))),copy=True,)
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomodoro Save a Dated Copy at Break")

def fn_pomodoro_save_at_break():
    try:
        if os.path.exists(bpy.data.filepath):
            pass
        else:
            pass
        bpy.ops.wm.save_mainfile("EXEC_DEFAULT",filepath=bpy.data.filepath,)
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomodoro Save at Break")

def fn_pomodoro_save_a_copy_at_break():
    try:
        if os.path.exists(bpy.data.filepath):
            bpy.ops.wm.save_as_mainfile("EXEC_DEFAULT",filepath=os.path.join(sn_cast_string(os.path.dirname(bpy.data.filepath)),sn_cast_string((sn_cast_string(os.path.basename(bpy.data.filepath).split(r".blend")[0]) + r"_" + r"copy" + r".blend"))),copy=True,)
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function FN Pomodoro Save a Copy at Break")

def update_pomodoros_completed(self, context):
    if sn_cast_blend_data(bpy.context.scene).pomodoros_completed <= 11:
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][sn_cast_int(sn_cast_blend_data(bpy.context.scene).pomodoros_completed)])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 15 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 20):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][12])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 20 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 25):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][13])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 25 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 30):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][14])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 30 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 35):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][15])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 35 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 40):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][16])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 40 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 45):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][17])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 45 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 50):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][18])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 50 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 75):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][19])
    else:
        pass
    if (sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 75 and sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 100):
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][20])
    else:
        pass
    if sn_cast_blend_data(bpy.context.scene).pomodoros_completed >= 100:
        sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = sn_cast_string(pomodoro["pomo_chef_list"][21])
    else:
        pass

def update_pomo_break_active(self, context):
    if sn_cast_blend_data(bpy.context.scene).pomodoro_scene_loaded:
        sn_cast_blend_data(bpy.context.scene).pomodoro_scene_loaded = False
    else:
        pomodoro["pomo_chef_message_break"] = (sn_cast_string(pomodoro["pomo_chef_messages_break"][random.randint(int(min(0.0, 21.0)), int(max(0.0, 21.0)))]) + sn_cast_blend_data(bpy.context.scene).pomo_chef_earned + r"!")
        pomodoro["pomo_chef_message_work"] = (sn_cast_string(pomodoro["pomo_chef_messages_work"][random.randint(int(min(0.0, 21.0)), int(max(0.0, 21.0)))]) + sn_cast_blend_data(bpy.context.scene).pomo_chef_earned + r"!")
        if sn_cast_blend_data(bpy.context.scene).pomo_break_active:
            function_return_73D72 = fn_pomodoro_save()
        else:
            pass
        if sn_cast_blend_data(bpy.context.scene).pomo_break_active:
            if pomodoro["pomo_big_break_count"] < sn_cast_blend_data(bpy.context.scene).pomo_big_break_amount:
                function_return_8A466 = fn_pomo_take_a_break()
            else:
                function_return_DFF19 = fn_pomo_big_break()
        else:
            function_return_3B09A = fn_pomo_back_to_work()


#######   Pomodoro UI
def sn_branch(v1,v2,condition):
    if condition:
        return v1
    return v2

def ui_fn_pomodoro_properties(layout, ):
    try:
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.0
        ui_fn_pomodoro_debug_1(col, )
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=r"Set Pomodoro For",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_5'].icon_id)
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomo_work_time',text=r"",emboss=True,slider=False,)
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=r"Then Take a Break",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id)
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomo_break_time',text=r"",emboss=True,slider=False,)
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=r"Every # of Pomodoros",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id)
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomo_big_break_amount',text=r"",emboss=True,slider=False,)
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.label(text=r"Take a Big Break",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_BIG_BREAK'].icon_id)
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomo_big_break_time',text=r"",emboss=True,slider=False,)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Properties")

def ui_fn_pomodoro_save_menu(layout, ):
    try:
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.0
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoro_save',icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
        row.label(text=r"  Save at each Pomodoro Break",icon_value=0)
        row = col.row(align=True)
        row.enabled = sn_cast_blend_data(bpy.context.scene).pomodoro_save
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoro_save_a_single_copy',icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE_A_COPY'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
        row.label(text=r"  Save a Copy Instead",icon_value=0)
        row = col.row(align=True)
        row.enabled = (sn_cast_blend_data(bpy.context.scene).pomodoro_save and sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy)
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoro_save_a_dated_copy',icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE_A_DATED_COPY'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
        row.label(text=r"  Save a Dated Copy",icon_value=0)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Save Menu")

def ui_fn_pomodoro_notify(layout, ):
    try:
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.0
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoro_user_notify',icon_value=110 if sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify else 3,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
        row.label(text=r"  Notify me at each Pomodoro Event (Experimental, recommend enabling a Save Option as well)",icon_value=0)
        row = col.row(align=True)
        row.enabled = sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoro_notify_and_pause',icon_value=498 if sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause else 495,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
        row.label(text=r"  Pause Pomodoro with Each Event",icon_value=0)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Notify")

def ui_fn_pomodoro_run_on_load(layout, ):
    try:
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.0
        row = col.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoro_run_on_load',icon_value=bpy.context.scene.il_grande_pomodoro_icons['POWER_ON'].icon_id if sn_cast_blend_data(bpy.context.scene).pomodoro_run_on_load else bpy.context.scene.il_grande_pomodoro_icons['POWER_OFF'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
        row.label(text=r"  Auto Start on File Load",icon_value=0)
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Run On Load")

def ui_fn_pomodoro_tracker(layout, ):
    try:
        col = layout.column(align=True)
        col.enabled = True
        col.alert = False
        col.scale_x = 1.0
        col.scale_y = 1.0
        ui_fn_pomodoro_counter_1(col, sn_cast_blend_data(bpy.context.scene).pomodoros_completed > 0, sn_cast_int(sn_branch(sn_cast_blend_data(bpy.context.scene).pomodoros_completed,10,sn_cast_blend_data(bpy.context.scene).pomodoros_completed < 10)), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(10), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(20), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(30), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(40), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(50), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(60), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(70), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(80), )
        ui_fn_pomodoro_counter_2(col, sn_cast_float(sn_cast_blend_data(bpy.context.scene).pomodoros_completed), sn_cast_float(90), )
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Tracker")

def ui_fn_pomodoro_counter_2(layout, _of_pomos, greater_than_x, ):
    try:
        ui_fn_pomodoro_counter_1(layout, _of_pomos >= greater_than_x, sn_cast_int(sn_branch(int((sn_cast_float(_of_pomos) - sn_cast_float(greater_than_x))),10,(int((sn_cast_float(_of_pomos) - sn_cast_float(greater_than_x))) >= 0 and _of_pomos < int((sn_cast_float(greater_than_x) + 10.0))))), )
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Counter 2")

def ui_fn_pomodoro_counter_1(layout, condition, repetitions, ):
    try:
        if condition:
            row = layout.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            repeat_node_C7FFC = 0
            for repeat_node_C7FFC in range(repetitions):
                row.label(text=r"",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id)
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Counter 1")

def ui_fn_pomodoro_debug_1(layout, ):
    try:
        if not True:
            row = layout.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            row.label(text=r"Pomo Timer Freq",icon_value=bpy.context.scene.il_grande_pomodoro_icons['GRAY_CLOCK'].icon_id)
            row.prop(sn_cast_blend_data(bpy.context.scene),'pomo_debug_timer_freq',text=r"",emboss=True,slider=False,)
            row = layout.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            row.label(text=sn_cast_string((r"Your Kitchen Rank: " + sn_cast_blend_data(bpy.context.scene).pomo_chef_earned + r"")),icon_value=bpy.context.scene.il_grande_pomodoro_icons['CHEFS_HAT'].icon_id)
            row.prop(sn_cast_blend_data(bpy.context.scene),'pomodoros_completed',text=sn_cast_blend_data(bpy.context.scene).pomo_chef_earned,emboss=True,slider=False,)
            row = layout.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            row.label(text=r"Pomo Break Status",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_5'].icon_id if sn_cast_blend_data(bpy.context.scene).pomo_break_active else bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id)
            row.prop(sn_cast_blend_data(bpy.context.scene),'pomo_break_active',icon_value=0,text=sn_cast_string(sn_cast_blend_data(bpy.context.scene).pomo_break_active),emboss=False,toggle=True,invert_checkbox=False,)
        else:
            pass
    except Exception as exc:
        print(str(exc) + " | Error in function UI FN Pomodoro Debug 1")


###############   EVALUATED CODE
#######   IL GRANDE POMODORO
pass # Script_Pomo_Timer.py Script Start

def pomo_timer():
    pomodoro["pomo_minutes"] += 1
    fn_end_tracking()
    for a in bpy.context.screen.areas:
        a.tag_redraw()
    if not bpy.context.scene.pomo_break_active:
        if pomodoro["pomo_minutes"] >= bpy.context.scene.pomo_work_time:
            pomodoro["pomo_minutes"] = 0
            bpy.context.scene.pomodoros_completed += 1
            pomodoro["pomo_big_break_count"] += 1
            bpy.context.scene.pomo_break_active = True
    elif pomodoro["pomo_big_break_count"] >= bpy.context.scene.pomo_big_break_amount:
        if pomodoro["pomo_minutes"] >= bpy.context.scene.pomo_big_break_time:
            pomodoro["pomo_minutes"] = 0
            pomodoro["pomo_big_break_count"] = 0
            bpy.context.scene.pomo_break_active = False
    elif pomodoro["pomo_minutes"] >= bpy.context.scene.pomo_break_time:
        pomodoro["pomo_minutes"] = 0
        bpy.context.scene.pomo_break_active = False


#    print('Number of Minutes: ', pomodoro["pomo_minutes"])
#    print('Pomodoro Break Status: ', bpy.context.scene.pomo_break_active)
    return bpy.context.scene.pomo_debug_timer_freq
pass # Script_Pomo_Timer.py Script End
pass # Script_Pomo_Chef_List.py Script Start


#Set up Pomodoro Chef Lists
pomodoro["pomo_chef_list"] = ['Aboyeur','Pioniere','Impiegato Capo','Orto','Verdura','Macellaio','Gastronomia','Grillardin','Friggitrice','Pescivendolo','Scala','Pasticcere','Chef Panettiere','Chef Salsicciotto','Chef Torrefattore','Chef Dispensa','Chef Entremetier','Chef de Toumant','Chef Comune','Sous Chef','Chef de Cuisine','Direttore Esecutivo']
pomodoro["pomo_chef_messages_break"] = ['The dinner rush can wait ','''Time to enjoy that bakers' dozen ''','Enjoy the fruit of the dinner pail tree ','''You'll clean this up later ''','Wash those tomato stains from your apron ','Take a power nap ','Nottin wrong with this ','Breaks are the bees knees ','''That's how you slice a tomato ''','''It's not a break, it's a balanced living ''','Go ahead. Eat a tomato ','Pomo-morigato Mr. ','''Tomatos are red, violets are blue, this break is ready and it's all for you ''','Take a load off ','''This one's for you ''','Take a breather ','Get some air ','''Do you hear that? It's your freedom calling ''','''This'll be here when you get back ''','Hand Yoga is calling for you ','''Stick it to the man ''','Take 5... or 10... or whatever ']
pomodoro["pomo_chef_messages_work"] = ['Productemys demands more from you ','Work work ','''Some day you'll rule this kitchen ''','''Time to make that Baker's dozen ''','''That tomato won't sauce itself ''','You got this ','''Somebody's gotta pay the bills ''','''You're up ''','''Let's get cookin'  ''','Go for the big Pomo ','Get up so you can get down ','Go gettum ','''I'm counting on you ''','Saucy needs the worky ','Make your mark ','Time to get after that Pomodoro ','You can do it ','You can do it ','Slice those tomatoes ','Get to choppin ','Basil needs ','''We're all counting on you ''']
pass # Script_Pomo_Chef_List.py Script End


class SNA_PT_DEBUGGER_F1E13(bpy.types.Panel):
    bl_label = "DEBUGGER"
    bl_idname = "SNA_PT_DEBUGGER_F1E13"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'
    bl_order = 0


    @classmethod
    def poll(cls, context):
        return not True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in DEBUGGER panel header")

    def draw(self, context):
        try:
            layout = self.layout
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            ui_fn_debugger(box, )
            ui_fn_pomodoro_properties(box, )
            ui_fn_pomodoro_save_menu(box, )
            ui_fn_pomodoro_notify(box, )
            ui_fn_pomodoro_run_on_load(box, )
        except Exception as exc:
            print(str(exc) + " | Error in DEBUGGER panel")


class SNA_AddonPreferences_BA4EB(bpy.types.AddonPreferences):
    bl_idname = 'il_grande_pomodoro'
    menu: bpy.props.EnumProperty(name='Menu',description='Select Menu',options=set(),items=[('Pomodoro', 'Pomodoro', 'Pomodoro User Settings'), ('Project Tracker', 'Project Tracker', 'Project Tracker User Settings'), ('Support', 'Support', 'Support and Contact.')])
    pomo_work_time: bpy.props.IntProperty(name='Pomo Work Time',description='How much time you should work on your Pomodoro.',subtype='NONE',options=set(),update=update_pomo_work_time_BA4EB,default=25,min=1,soft_min=5,soft_max=1440)
    pomo_break_time: bpy.props.IntProperty(name='Pomo Break Time',description='How much break time after completing a Pomodoro.',subtype='NONE',options=set(),update=update_pomo_break_time_BA4EB,default=5,min=1,soft_min=5,soft_max=1440)
    pomo_big_break_amount: bpy.props.IntProperty(name='Pomo Big Break Amount',description='After X number of Pomodoros completed: reward yourself with a Big Break',subtype='NONE',options=set(),update=update_pomo_big_break_amount_BA4EB,default=3,min=1,soft_min=3,soft_max=1440)
    pomo_big_break_time: bpy.props.IntProperty(name='Pomo Big Break Time',description='How much time is needed for your big break (usually double the Break Time)',subtype='NONE',options=set(),update=update_pomo_big_break_time_BA4EB,default=10,min=1,soft_min=10,soft_max=1440)
    pomo_save: bpy.props.BoolProperty(name='Pomo Save',description='Save your Blend File at the start of each Pomodoro Break',options=set(),update=update_pomo_save_BA4EB,default=False)
    pomo_save_single_copy: bpy.props.BoolProperty(name='Pomo Save Single Copy',description='Save a Copy of your Blend File at the start of each Pomodoro Break',options=set(),update=update_pomo_save_single_copy_BA4EB,default=False)
    pomo_save_dated_copy: bpy.props.BoolProperty(name='Pomo Save Dated Copy',description='Save a Dated Copy of your Blend File at the start of each Pomodoro Break',options=set(),update=update_pomo_save_dated_copy_BA4EB,default=False)
    pomo_user_notify: bpy.props.BoolProperty(name='Pomo User Notify',description='Notify me when Pomodoro Timers Finish (Note, this feature is experimental. Please turn on a Pomodoro Save Option to ensure project saves if you like using the notifications)',options=set(),update=update_pomo_user_notify_BA4EB,default=False)
    pomo_user_notify_and_pause: bpy.props.BoolProperty(name='Pomo User Notify and Pause',description='Pause Pomodoro at each Popup Event. If active then Click the Popup to Continue or Click the Pomodoro Button Again.',options=set(),update=update_pomo_user_notify_and_pause_BA4EB,default=False)
    pomo_run_on_load: bpy.props.BoolProperty(name='Pomo Run On Load',description='Start Pomodoro after you open Blender or Load a File',options=set(),update=update_pomo_run_on_load_BA4EB,default=False)

    def draw(self, context):
        try:
            layout = self.layout
            col = layout.column(align=True)
            col.enabled = True
            col.alert = False
            col.scale_x = 1.5
            col.scale_y = 1.5
            row = col.row(align=False)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'menu',icon_value=sn_cast_int(bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id if context.preferences.addons['il_grande_pomodoro'].preferences.menu == r"Pomodoro" else bpy.context.scene.il_grande_pomodoro_icons['GRAY_CLOCK'].icon_id if context.preferences.addons['il_grande_pomodoro'].preferences.menu == r"Project Tracker" else 1 if context.preferences.addons['il_grande_pomodoro'].preferences.menu == r"Support" else 101),text=r"Menu",emboss=True,expand=True,)
            col.separator(factor=2.5)
            if context.preferences.addons['il_grande_pomodoro'].preferences.menu == r"Pomodoro":
                col.label(text=r"Customize Your Pomodoro:",icon_value=bpy.context.scene.il_grande_pomodoro_icons['CHEFS_HAT'].icon_id)
                ui_fn_pomodoro_debug_1(col, )
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"Set Pomodoro For",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_5'].icon_id)
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_work_time',text=r"",emboss=True,slider=False,)
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"Then Take a Break",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id)
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_break_time',text=r"",emboss=True,slider=False,)
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"Every # of Pomodoros",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id)
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_big_break_amount',text=r"",emboss=True,slider=False,)
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"Take a Big Break",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMO_BIG_BREAK'].icon_id)
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_big_break_time',text=r"",emboss=True,slider=False,)
                col.separator(factor=2.0)
                col.label(text=r"4 out of 5 Chefs recommend Auto-Save:",icon_value=0)
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(self,'pomo_save',icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
                row.label(text=r"  Save at each Pomodoro Break",icon_value=0)
                row = col.row(align=True)
                row.enabled = sn_cast_blend_data(bpy.context.scene).pomodoro_save
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"",icon_value=101)
                row.prop(self,'pomo_save_single_copy',icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE_A_COPY'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
                row.label(text=r"  Save a Copy Instead",icon_value=0)
                row = col.row(align=True)
                row.enabled = (sn_cast_blend_data(bpy.context.scene).pomodoro_save and sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy)
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"",icon_value=101)
                row.label(text=r"",icon_value=101)
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_save_dated_copy',icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE_A_DATED_COPY'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
                row.label(text=r"  Save a Dated Copy",icon_value=0)
                col.separator(factor=2.0)
                col.label(text=r"For Chefs who like notifications:",icon_value=0)
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_user_notify',icon_value=110 if sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify else 3,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
                row.label(text=r"  Notify me at each Pomodoro Event   (experimental)",icon_value=0)
                row = col.row(align=True)
                row.enabled = sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.label(text=r"",icon_value=101)
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_user_notify_and_pause',icon_value=498 if sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause else 495,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
                row.label(text=r"  Pause Pomodoro with Each Event",icon_value=0)
                col.separator(factor=2.0)
                col.label(text=r"Real Chefs don't manually clock in:",icon_value=0)
                row = col.row(align=True)
                row.enabled = True
                row.alert = False
                row.scale_x = 1.0
                row.scale_y = 1.0
                row.prop(context.preferences.addons['il_grande_pomodoro'].preferences,'pomo_run_on_load',icon_value=bpy.context.scene.il_grande_pomodoro_icons['POWER_ON'].icon_id if sn_cast_blend_data(bpy.context.scene).pomodoro_run_on_load else bpy.context.scene.il_grande_pomodoro_icons['POWER_OFF'].icon_id,text=r"",emboss=True,toggle=True,invert_checkbox=False,)
                row.label(text=r"  Auto Start on File Load",icon_value=0)
                col.separator(factor=2.0)
                col.label(text=r"If you need a Reset Button:",icon_value=0)
                ui_fn_reset_pomodoro(col, )
            else:
                pass
            if context.preferences.addons['il_grande_pomodoro'].preferences.menu == r"Project Tracker":
                col.label(text=r"Project Tracker Settings:",icon_value=bpy.context.scene.il_grande_pomodoro_icons['GRAY_CLOCK'].icon_id)
                ui_fn_addon_prefs_proj_timer(col, )
            else:
                pass
            if context.preferences.addons['il_grande_pomodoro'].preferences.menu == r"Support":
                col.label(text=r"Support:",icon_value=1)
                op = col.operator("wm.url_open",text=r"Serpens Discord",emboss=True,depress=False,icon_value=698)
                op.url = r"https://discord.com/invite/NK6kyae"
                col.separator(factor=2.0)
                col.label(text=r"Check for Updates:",icon_value=0)
                op = col.operator("wm.url_open",text=r"Blender Market",emboss=True,depress=False,icon_value=bpy.context.scene.il_grande_pomodoro_icons['BLENDER_MARKET'].icon_id)
                op.url = r"https://blendermarket.com/"
                op = col.operator("wm.url_open",text=r"Gumroad",emboss=True,depress=False,icon_value=bpy.context.scene.il_grande_pomodoro_icons['GUMROAD'].icon_id)
                op.url = r"https://gumroad.com/"
            else:
                pass
            layout.separator(factor=2.0)
            snippet_return_ED613 = changelog_interface_snippet_ED613(layout, [r"Initial Release", ], bpy.context.scene.il_grande_pomodoro_icons['POMO_BREAK'].icon_id, )
        except Exception as exc:
            print(str(exc) + " | Error in addon preferences")


#######   UI FN Addon Prefs Project Tracker
class SNA_OT_Reset_Total_Time(bpy.types.Operator):
    bl_idname = "sna.reset_total_time"
    bl_label = "Reset Total Time"
    bl_description = "Click if you need to reset the Project Total Time"
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            sn_cast_blend_data(bpy.context.scene).total_time_min = 0
            function_return_98563 = fn_start_tracking()
            function_return_83761 = fn_end_tracking()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Reset Total Time")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Reset Total Time")
        return self.execute(context)


class SNA_OT_Reset_Session_Time(bpy.types.Operator):
    bl_idname = "sna.reset_session_time"
    bl_label = "Reset Session Time"
    bl_description = "Click if you need to reset the Active Session Time"
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            sn_cast_blend_data(bpy.context.scene).session_time_min = 0
            function_return_7EFEC = fn_reset_temp_session_time()
            function_return_6BE58 = fn_start_tracking()
            function_return_20430 = fn_end_tracking()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Reset Session Time")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Reset Session Time")
        return self.execute(context)


class SNA_OT_Reset_Prev_Session_Time(bpy.types.Operator):
    bl_idname = "sna.reset_prev_session_time"
    bl_label = "Reset Prev. Session Time"
    bl_description = "Click if you need to reset the Previous Session Time"
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            sn_cast_blend_data(bpy.context.scene).prev_session_time_min = 0
            function_return_BFA24 = fn_start_tracking()
            function_return_AC727 = fn_end_tracking()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Reset Prev. Session Time")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Reset Prev. Session Time")
        return self.execute(context)


#######   Add To Menu - VIEW_3D
def sn_append_menu_4EF93(self,context):
    try:
        layout = self.layout
        row = layout.row(align=True)
        row.enabled = True
        row.alert = False
        row.scale_x = 1.0
        row.scale_y = 1.0
        ui_fn_pomodoro_add_to_menu(row, )
        row.menu("SNA_MT_Project_Tracker_09E1C",text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).total_time_min)),icon_value=bpy.context.scene.il_grande_pomodoro_icons['TOTAL_TIME'].icon_id)
    except Exception as exc:
        print(str(exc) + " | Error in View3D Mt Editor Menus when adding to menu")


class SNA_MT_Project_Tracker_09E1C(bpy.types.Menu):
    bl_idname = "SNA_MT_Project_Tracker_09E1C"
    bl_label = "Project Tracker"


    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        try:
            layout = self.layout
            layout.label(text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).total_time_min) + r" min"),icon_value=bpy.context.scene.il_grande_pomodoro_icons['TOTAL_TIME'].icon_id)
            layout.label(text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).session_time_min) + r" min"),icon_value=bpy.context.scene.il_grande_pomodoro_icons['SESSION_TIME'].icon_id)
            layout.label(text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).prev_session_time_min) + r" min"),icon_value=bpy.context.scene.il_grande_pomodoro_icons['PREV_TIME'].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in Project Tracker menu")


#######   OT - Start Tracking
class SNA_OT_Ot_Start_Tracking(bpy.types.Operator):
    bl_idname = "sna.ot_start_tracking"
    bl_label = "OT Start Tracking"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            function_return_F8DAB = fn_start_tracking_and_set_prev_session()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of OT Start Tracking")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of OT Start Tracking")
        return self.execute(context)


#######   OT - End Tracking
class SNA_OT_Ot_End_Tracking(bpy.types.Operator):
    bl_idname = "sna.ot_end_tracking"
    bl_label = "OT End Tracking"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            function_return_5C633 = fn_end_tracking()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of OT End Tracking")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of OT End Tracking")
        return self.execute(context)


#######   Pomodoro
class SNA_OT_Oh_Yeah_Big_Break(bpy.types.Operator):
    bl_idname = "sna.oh_yeah_big_break"
    bl_label = "Oh Yeah! Big Break!"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            pomodoro["pomo_notify"] = False
            bpy.ops.sna.start_pomodoro("EXEC_DEFAULT",)
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Oh Yeah! Big Break!")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            if sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause:
                bpy.ops.sna.stop_pomodoro("EXEC_DEFAULT",)
                pomodoro["pomo_notify"] = True
                sn_redraw()
            else:
                sn_redraw()
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Oh Yeah! Big Break!")
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        try:
            layout.label(text=pomodoro["pomo_chef_message_break"],icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMOS_BIG_COMPLETED'].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in draw function of Oh Yeah! Big Break!")


class SNA_OT_Take_A_Break(bpy.types.Operator):
    bl_idname = "sna.take_a_break"
    bl_label = "Take a Break"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            pomodoro["pomo_notify"] = False
            bpy.ops.sna.start_pomodoro("INVOKE_DEFAULT",)
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Take a Break")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            if sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause:
                bpy.ops.sna.stop_pomodoro("INVOKE_DEFAULT",)
                pomodoro["pomo_notify"] = True
                sn_redraw()
            else:
                sn_redraw()
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Take a Break")
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        try:
            layout.label(text=pomodoro["pomo_chef_message_break"],icon_value=bpy.context.scene.il_grande_pomodoro_icons['POMOS_COMPLETED'].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in draw function of Take a Break")


class SNA_OT_Reset_Pomodoro(bpy.types.Operator):
    bl_idname = "sna.reset_pomodoro"
    bl_label = "Reset Pomodoro"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            bpy.ops.sna.stop_pomodoro('INVOKE_DEFAULT' if True else 'EXEC_DEFAULT',)
            pomodoro["pomo_minutes"] = 0
            pomodoro["pomos_completed"] = 0
            pomodoro["pomo_big_break_count"] = 0
            sn_cast_blend_data(bpy.context.scene).pomodoro_scene_loaded = True
            sn_cast_blend_data(bpy.context.scene).pomo_chef_earned = r"Aboyeur"
            sn_cast_blend_data(bpy.context.scene).pomodoros_completed = 0
            sn_cast_blend_data(bpy.context.scene).pomo_break_active = False
            sn_redraw()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Reset Pomodoro")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Reset Pomodoro")
        return self.execute(context)


class SNA_OT_Back_To_Work(bpy.types.Operator):
    bl_idname = "sna.back_to_work"
    bl_label = "Back to Work"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            pomodoro["pomo_notify"] = False
            bpy.ops.sna.start_pomodoro("EXEC_DEFAULT",)
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Back to Work")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            if sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause:
                bpy.ops.sna.stop_pomodoro("EXEC_DEFAULT",)
                pomodoro["pomo_notify"] = True
                sn_redraw()
            else:
                sn_redraw()
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Back to Work")
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        try:
            layout.label(text=pomodoro["pomo_chef_message_work"],icon_value=bpy.context.scene.il_grande_pomodoro_icons['CHEFS_HAT'].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in draw function of Back to Work")


class SNA_OT_Toggle_Pomodoro(bpy.types.Operator):
    bl_idname = "sna.toggle_pomodoro"
    bl_label = "Toggle Pomodoro"
    bl_description = "Toggle Pomodoro Timer"
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            if pomodoro["pomo_toggle"]:
                bpy.ops.sna.stop_pomodoro("EXEC_DEFAULT",)
            else:
                bpy.ops.sna.start_pomodoro("EXEC_DEFAULT",)
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Toggle Pomodoro")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Toggle Pomodoro")
        return self.execute(context)


class SNA_OT_Start_Pomodoro(bpy.types.Operator):
    bl_idname = "sna.start_pomodoro"
    bl_label = "Start Pomodoro"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            pass # Script_Pomo_Start.py Script Start
            if not bpy.app.timers.is_registered(pomo_timer):
                pomodoro["pomo_minutes"] -= 1
                bpy.app.timers.register(pomo_timer)
            pass # Script_Pomo_Start.py Script End
            pomodoro["pomo_toggle"] = True
            pomodoro["pomo_notify"] = False
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Start Pomodoro")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Start Pomodoro")
        return self.execute(context)


class SNA_OT_Stop_Pomodoro(bpy.types.Operator):
    bl_idname = "sna.stop_pomodoro"
    bl_label = "Stop Pomodoro"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}


    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        try:
            pass # Script_Pomo_Stop.py Script Start
            if bpy.app.timers.is_registered(pomo_timer):
                bpy.app.timers.unregister(pomo_timer)
            pass # Script_Pomo_Stop.py Script End
            pomodoro["pomo_toggle"] = False
            pomodoro["pomo_notify"] = False
            sn_redraw()
        except Exception as exc:
            print(str(exc) + " | Error in execute function of Stop Pomodoro")
        return {"FINISHED"}

    def invoke(self, context, event):
        try:
            pass
        except Exception as exc:
            print(str(exc) + " | Error in invoke function of Stop Pomodoro")
        return self.execute(context)


#######   Pomodoro UI
class SNA_PT_Pomodoro_Save_Settings_93C71(bpy.types.Panel):
    bl_label = "Pomodoro Save Settings:"
    bl_idname = "SNA_PT_Pomodoro_Save_Settings_93C71"
    bl_parent_id = "SNA_PT_Pomodoro_03BD2"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'


    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
            row = layout.row(align=False)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            if (sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save) and not sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy)):
                row.label(text=r"",icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE'].icon_id)
            else:
                pass
            if (sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save) and sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy) and True and not sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_dated_copy)):
                row.label(text=r"",icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE_A_COPY'].icon_id)
            else:
                pass
            if (sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save) and sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_single_copy) and True and sn_cast_boolean(sn_cast_blend_data(bpy.context.scene).pomodoro_save_a_dated_copy)):
                row.label(text=r"",icon_value=bpy.context.scene.il_grande_pomodoro_icons['SAVE_A_DATED_COPY'].icon_id)
            else:
                pass
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro Save Settings: subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.separator(factor=1.0)
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            ui_fn_pomodoro_save_menu(box, )
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro Save Settings: subpanel")


class SNA_PT_Pomodoro_Notify_Settings_D828E(bpy.types.Panel):
    bl_label = "Pomodoro Notify Settings:"
    bl_idname = "SNA_PT_Pomodoro_Notify_Settings_D828E"
    bl_parent_id = "SNA_PT_Pomodoro_03BD2"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'


    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
            row = layout.row(align=False)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            if sn_cast_blend_data(bpy.context.scene).pomodoro_user_notify:
                row.label(text=r"",icon_value=2)
            else:
                pass
            if sn_cast_blend_data(bpy.context.scene).pomodoro_notify_and_pause:
                row.label(text=r"",icon_value=498)
            else:
                pass
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro Notify Settings: subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.separator(factor=1.0)
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            ui_fn_pomodoro_notify(box, )
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro Notify Settings: subpanel")


class SNA_PT_Pomodoro_Extra_Settings_26044(bpy.types.Panel):
    bl_label = "Pomodoro Extra Settings:"
    bl_idname = "SNA_PT_Pomodoro_Extra_Settings_26044"
    bl_parent_id = "SNA_PT_Pomodoro_03BD2"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'


    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
            row = layout.row(align=False)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            if sn_cast_blend_data(bpy.context.scene).pomodoro_run_on_load:
                row.label(text=r"",icon_value=bpy.context.scene.il_grande_pomodoro_icons['POWER_OFF'].icon_id)
            else:
                pass
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro Extra Settings: subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.separator(factor=1.0)
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            ui_fn_pomodoro_run_on_load(box, )
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro Extra Settings: subpanel")


class SNA_PT_Customize_Your_Pomodoro_65555(bpy.types.Panel):
    bl_label = "Customize Your Pomodoro:"
    bl_idname = "SNA_PT_Customize_Your_Pomodoro_65555"
    bl_parent_id = "SNA_PT_Pomodoro_03BD2"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'


    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
            layout.label(text=r"",icon_value=bpy.context.scene.il_grande_pomodoro_icons['CHEFS_HAT'].icon_id)
        except Exception as exc:
            print(str(exc) + " | Error in Customize Your Pomodoro: subpanel header")

    def draw(self, context):
        try:
            layout = self.layout
            layout.separator(factor=1.0)
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            ui_fn_pomodoro_properties(box, )
        except Exception as exc:
            print(str(exc) + " | Error in Customize Your Pomodoro: subpanel")


class SNA_PT_Pomodoro_03BD2(bpy.types.Panel):
    bl_label = "Pomodoro"
    bl_idname = "SNA_PT_Pomodoro_03BD2"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = 'scene'
    bl_order = 0


    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        try:
            layout = self.layout
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro panel header")

    def draw(self, context):
        try:
            layout = self.layout
            ui_fn_pomodoro(layout, )
            box = layout.box()
            box.enabled = True
            box.alert = False
            box.scale_x = 1.0
            box.scale_y = 1.0
            col = box.column(align=True)
            col.enabled = True
            col.alert = False
            col.scale_x = 1.0
            col.scale_y = 1.0
            col.label(text=r"Project Tracker",icon_value=0)
            col.separator(factor=1.0)
            row = col.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            split = row.split(align=False,factor=0.699999988079071)
            split.enabled = True
            split.alert = False
            split.scale_x = 1.0
            split.scale_y = 1.0
            split.label(text=r"Total Project Time",icon_value=bpy.context.scene.il_grande_pomodoro_icons['TOTAL_TIME'].icon_id)
            split.label(text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).total_time_min) + r" min"),icon_value=0)
            row = col.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            split = row.split(align=False,factor=0.699999988079071)
            split.enabled = True
            split.alert = False
            split.scale_x = 1.0
            split.scale_y = 1.0
            split.label(text=r"Current Session Time",icon_value=bpy.context.scene.il_grande_pomodoro_icons['SESSION_TIME'].icon_id)
            split.label(text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).session_time_min) + r" min"),icon_value=0)
            row = col.row(align=True)
            row.enabled = True
            row.alert = False
            row.scale_x = 1.0
            row.scale_y = 1.0
            split = row.split(align=False,factor=0.699999988079071)
            split.enabled = True
            split.alert = False
            split.scale_x = 1.0
            split.scale_y = 1.0
            split.label(text=r"Previous Session Time",icon_value=bpy.context.scene.il_grande_pomodoro_icons['PREV_TIME'].icon_id)
            split.label(text=(r" " + sn_cast_string(sn_cast_blend_data(bpy.context.scene).prev_session_time_min) + r" min"),icon_value=0)
        except Exception as exc:
            print(str(exc) + " | Error in Pomodoro panel")


###############   REGISTER ICONS
def sn_register_icons():
    icons = ["GRAY_CLOCK","TOTAL_TIME","SESSION_TIME","PREV_TIME","GREEN_CLOCK","YELLOW_CLOCK","RED_CLOCK","POMO_0","POMO_1","POMO_2","POMO_3","POMO_4","POMO_5","POMO_STOPPED","POMO_BREAK","POMO_BIG_BREAK","POMOS_COMPLETED","POMOS_BIG_COMPLETED","CHEFS_HAT","SAVE","SAVE_A_COPY","SAVE_A_DATED_COPY","POWER_OFF","POWER_ON","BLENDER_MARKET","GUMROAD",]
    bpy.types.Scene.il_grande_pomodoro_icons = bpy.utils.previews.new()
    icons_dir = os.path.join( os.path.dirname( __file__ ), "icons" )
    for icon in icons:
        bpy.types.Scene.il_grande_pomodoro_icons.load( icon, os.path.join( icons_dir, icon + ".png" ), 'IMAGE' )

def sn_unregister_icons():
    bpy.utils.previews.remove( bpy.types.Scene.il_grande_pomodoro_icons )


###############   REGISTER PROPERTIES
def sn_register_properties():
    bpy.types.Scene.opened_or_saved_time_vec3_hms = bpy.props.IntVectorProperty(name='Opened or Saved Time Vec3 (HMS)',description='',subtype='NONE',options=set(),default=(0, 0, 0),size=3,min=0)
    bpy.types.Scene.opened_or_saved_date_vec3_yymd = bpy.props.IntVectorProperty(name='Opened or Saved Date Vec3 (YYMD)',description='',subtype='NONE',options=set(),default=(0, 0, 0),size=3,min=0)
    bpy.types.Scene.opened_or_saved_time_min = bpy.props.IntProperty(name='Opened or Saved Time (Min)',description='',subtype='NONE',options=set(),default=0,min=0)
    bpy.types.Scene.current_time_min = bpy.props.IntProperty(name='Current Time (Min)',description='',subtype='NONE',options=set(),default=0,min=0)
    bpy.types.Scene.total_time_min = bpy.props.IntProperty(name='Total Time (min)',description='',subtype='NONE',options=set(),default=0,min=0)
    bpy.types.Scene.session_time_min = bpy.props.IntProperty(name='Session Time (Min)',description='',subtype='NONE',options=set(),default=0,min=0)
    bpy.types.Scene.prev_session_time_min = bpy.props.IntProperty(name='Prev Session Time (Min)',description='',subtype='NONE',options=set(),default=0,min=0)
    bpy.types.Scene.pomo_debug_timer_freq = bpy.props.FloatProperty(name='Pomo Debug Timer Freq',description='',subtype='TIME',unit='TIME',options=set(),precision=1, default=60.0,min=0.10000000149011612,soft_min=1.0,soft_max=1.0)
    bpy.types.Scene.pomo_work_time = bpy.props.IntProperty(name='Pomo Work Time',description='How much time you should work on your Pomodoro.',subtype='TIME',options=set(),default=25,min=1,soft_min=5,soft_max=1440)
    bpy.types.Scene.pomo_break_time = bpy.props.IntProperty(name='Pomo Break Time',description='How much break time after completing a Pomodoro.',subtype='TIME',options=set(),default=5,min=1,soft_min=5,soft_max=1440)
    bpy.types.Scene.pomo_big_break_amount = bpy.props.IntProperty(name='Pomo Big Break Amount',description='After X number of Pomodoros completed: reward yourself with a Big Break',subtype='NONE',options=set(),default=3,min=1,soft_min=3,soft_max=1440)
    bpy.types.Scene.pomo_big_break_time = bpy.props.IntProperty(name='Pomo Big Break Time',description='How much time is needed for your big break (usually double the Break Time)',subtype='TIME',options=set(),default=10,min=1,soft_min=10,soft_max=1440)
    bpy.types.Scene.pomo_break_active = bpy.props.BoolProperty(name='Pomo Break Active',description='',options=set(),update=update_pomo_break_active,default=False)
    bpy.types.Scene.pomodoros_completed = bpy.props.IntProperty(name='Pomodoros Completed',description='Number of Pomodoros Completed',subtype='NONE',options=set(),update=update_pomodoros_completed,default=0,min=0)
    bpy.types.Scene.pomo_chef_earned = bpy.props.StringProperty(name='Pomo Chef Earned',description='Your current Rank in the Kitchen',subtype='NONE',options=set(),default='Aboyeur')
    bpy.types.Scene.pomodoro_save = bpy.props.BoolProperty(name='Pomodoro Save',description='Save your Blend File at the start of each Pomodoro Break',options=set(),default=False)
    bpy.types.Scene.pomodoro_save_a_single_copy = bpy.props.BoolProperty(name='Pomodoro Save a Single Copy',description='Save a Copy of your Blend File at the start of each Pomodoro Break',options=set(),default=False)
    bpy.types.Scene.pomodoro_save_a_dated_copy = bpy.props.BoolProperty(name='Pomodoro Save a Dated Copy',description='Save a Dated Copy of your Blend File at the start of each Pomodoro Break',options=set(),default=False)
    bpy.types.Scene.pomodoro_user_notify = bpy.props.BoolProperty(name='Pomodoro User Notify',description='Notify me when Pomodoro Timers Finish',options=set(),default=False)
    bpy.types.Scene.pomodoro_notify_and_pause = bpy.props.BoolProperty(name='Pomodoro Notify and Pause',description='Pause Pomodoro at each Popup Event. If active then Click the Popup to Continue or Click the Pomodoro Button Again.',options=set(),default=False)
    bpy.types.Scene.pomodoro_run_on_load = bpy.props.BoolProperty(name='Pomodoro Run on Load',description='Start Pomodoro after you open Blender or Load a File',options=set(),default=False)
    bpy.types.Scene.pomodoro_scene_loaded = bpy.props.BoolProperty(name='Pomodoro Scene Loaded',description='',options=set(),default=False)

def sn_unregister_properties():
    del bpy.types.Scene.opened_or_saved_time_vec3_hms
    del bpy.types.Scene.opened_or_saved_date_vec3_yymd
    del bpy.types.Scene.opened_or_saved_time_min
    del bpy.types.Scene.current_time_min
    del bpy.types.Scene.total_time_min
    del bpy.types.Scene.session_time_min
    del bpy.types.Scene.prev_session_time_min
    del bpy.types.Scene.pomo_debug_timer_freq
    del bpy.types.Scene.pomo_work_time
    del bpy.types.Scene.pomo_break_time
    del bpy.types.Scene.pomo_big_break_amount
    del bpy.types.Scene.pomo_big_break_time
    del bpy.types.Scene.pomo_break_active
    del bpy.types.Scene.pomodoros_completed
    del bpy.types.Scene.pomo_chef_earned
    del bpy.types.Scene.pomodoro_save
    del bpy.types.Scene.pomodoro_save_a_single_copy
    del bpy.types.Scene.pomodoro_save_a_dated_copy
    del bpy.types.Scene.pomodoro_user_notify
    del bpy.types.Scene.pomodoro_notify_and_pause
    del bpy.types.Scene.pomodoro_run_on_load
    del bpy.types.Scene.pomodoro_scene_loaded


###############   REGISTER ADDON
def register():
    sn_register_icons()
    sn_register_properties()
    bpy.app.handlers.save_pre.append(save_pre_handler_465EE)
    bpy.utils.register_class(SNA_PT_DEBUGGER_F1E13)
    bpy.utils.register_class(SNA_AddonPreferences_BA4EB)
    bpy.app.handlers.load_post.append(load_post_handler_8F2AE)
    bpy.utils.register_class(SNA_OT_Reset_Total_Time)
    bpy.utils.register_class(SNA_OT_Reset_Session_Time)
    bpy.utils.register_class(SNA_OT_Reset_Prev_Session_Time)
    bpy.utils.register_class(SNA_MT_Project_Tracker_09E1C)
    bpy.utils.register_class(SNA_OT_Ot_Start_Tracking)
    bpy.utils.register_class(SNA_OT_Ot_End_Tracking)
    bpy.utils.register_class(SNA_OT_Oh_Yeah_Big_Break)
    bpy.utils.register_class(SNA_OT_Take_A_Break)
    bpy.utils.register_class(SNA_OT_Reset_Pomodoro)
    bpy.utils.register_class(SNA_OT_Back_To_Work)
    bpy.utils.register_class(SNA_OT_Toggle_Pomodoro)
    bpy.utils.register_class(SNA_OT_Start_Pomodoro)
    bpy.utils.register_class(SNA_OT_Stop_Pomodoro)
    bpy.utils.register_class(SNA_PT_Pomodoro_03BD2)
    bpy.types.VIEW3D_MT_editor_menus.append(sn_append_menu_4EF93)
    bpy.utils.register_class(SNA_PT_Pomodoro_Save_Settings_93C71)
    bpy.utils.register_class(SNA_PT_Pomodoro_Notify_Settings_D828E)
    bpy.utils.register_class(SNA_PT_Pomodoro_Extra_Settings_26044)
    bpy.utils.register_class(SNA_PT_Customize_Your_Pomodoro_65555)


###############   UNREGISTER ADDON
def unregister():
    sn_unregister_icons()
    sn_unregister_properties()
    bpy.utils.unregister_class(SNA_PT_Customize_Your_Pomodoro_65555)
    bpy.utils.unregister_class(SNA_PT_Pomodoro_Extra_Settings_26044)
    bpy.utils.unregister_class(SNA_PT_Pomodoro_Notify_Settings_D828E)
    bpy.utils.unregister_class(SNA_PT_Pomodoro_Save_Settings_93C71)
    bpy.types.VIEW3D_MT_editor_menus.remove(sn_append_menu_4EF93)
    bpy.utils.unregister_class(SNA_PT_Pomodoro_03BD2)
    bpy.utils.unregister_class(SNA_OT_Stop_Pomodoro)
    bpy.utils.unregister_class(SNA_OT_Start_Pomodoro)
    bpy.utils.unregister_class(SNA_OT_Toggle_Pomodoro)
    bpy.utils.unregister_class(SNA_OT_Back_To_Work)
    bpy.utils.unregister_class(SNA_OT_Reset_Pomodoro)
    bpy.utils.unregister_class(SNA_OT_Take_A_Break)
    bpy.utils.unregister_class(SNA_OT_Oh_Yeah_Big_Break)
    bpy.utils.unregister_class(SNA_OT_Ot_End_Tracking)
    bpy.utils.unregister_class(SNA_OT_Ot_Start_Tracking)
    bpy.utils.unregister_class(SNA_MT_Project_Tracker_09E1C)
    bpy.utils.unregister_class(SNA_OT_Reset_Prev_Session_Time)
    bpy.utils.unregister_class(SNA_OT_Reset_Session_Time)
    bpy.utils.unregister_class(SNA_OT_Reset_Total_Time)
    bpy.app.handlers.load_post.remove(load_post_handler_8F2AE)
    bpy.utils.unregister_class(SNA_AddonPreferences_BA4EB)
    bpy.utils.unregister_class(SNA_PT_DEBUGGER_F1E13)
    bpy.app.handlers.save_pre.remove(save_pre_handler_465EE)