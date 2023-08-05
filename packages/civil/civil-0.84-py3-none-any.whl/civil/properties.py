# coding=utf-8
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
This file contains various settings used throughout the application. All settings are global values
and can be used as needed. They should not be changed though.
"""

import os

from pygame.locals import *

from civil import version as vs

# general settings. The setting base path is a directory used as the base path for all other
# directories. This setting should always be used to get the top level directory of the installation,
# as it makes the game easier to relocate without too much hassle. Some day this setting gets set by
# autoconf or something similar.

version = vs.__version__
HERE = os.path.abspath(os.path.dirname(__file__))
base_path = os.path.join(HERE, 'data')

# Change to 1 if we're in the editor
is_civil_editor = 0

# set to 1 to enable global debugging. this can be used for heavy debugging. A value of 1 also
# implies that we're doing local development.
debug = 0

# hardcoded theatre
theatre = 'us-civil'

# common paths
path_fonts = os.path.join(base_path, 'fonts')
path_gfx = os.path.join(base_path, 'gfx')
path_doc = os.path.join(base_path, 'doc')
path_sound = os.path.join(base_path, 'sound')
path_scenarios = os.path.join(base_path, 'scenarios')
path_source = 'civil'
path_terrains = os.path.join(path_gfx, 'terrains')
path_features = os.path.join(path_gfx, 'objects')
path_help = os.path.join(path_doc, 'help')
path_dialogs = os.path.join(path_gfx, 'dialogs')

# theater specific paths. note that the theater is not yet given here, it will be appended in later
# when we know the actual theater path
path_units = os.path.join(path_gfx,  'units', theatre)
path_periphery = os.path.join(path_gfx, 'periphery', theatre)
path_cursors = os.path.join(path_gfx, 'pointers', theatre)

# paths for the setup dialogs
path_cursors_setup = os.path.join(path_gfx,  'pointers', 'setup')

# paths for custom user data
path_home = 'this must be set!'
path_saved_games = 'this must be set!'
path_custom_scenarios = 'this must be set!'

# path to server and the ai client
path_server = os.path.join(path_source, 'civil-server')
path_ai_client = os.path.join(path_source, 'civil-ai')

# platform name
platform_name = 'unknown'

# font info
font_normal = 'freesansbold.ttf'
font_title = 'freesansbold.ttf'

# turns and time
# minutes_per_turn                    = 10
seconds_per_step = 10
animation_interval = 500

# playfield and layer settings
layer_grid_icon = os.path.join(path_periphery, 'grid.png')
layer_objective_icon_union = os.path.join(path_units, 'obj-gold.png')
layer_objective_icon_rebel = os.path.join(path_units, 'obj-gold.png')
layer_objective_icon_unknown = os.path.join(path_units, 'obj-gold.png')
layer_locations_font = os.path.join(path_fonts, font_normal)
layer_locations_font_size = 12
layer_locations_color = (255, 255, 255)
layer_locations_shadow = (10, 10, 10)
layer_unit_icon_main = os.path.join(path_units, 'unit-highlight-mainsel.png')
layer_unit_icon_extra = os.path.join(path_units, 'unit-highlight.png')
layer_unit_strength_height = 4
layer_unit_strength_color_poor = (255, 0, 0)
layer_unit_strength_color_good = (255, 255, 0)
layer_unit_strength_color_excellent = (0, 255, 0)
layer_help_font = os.path.join(path_fonts, font_normal)
layer_help_font_size = 14
layer_help_color = (255, 255, 128)
layer_help_button = os.path.join(path_dialogs, 'butt-help-close.png')
layer_dialog_font = os.path.join(path_fonts, font_normal)
layer_dialog_font_size = 14
layer_dialog_color = (255, 255, 128)
layer_help_browser_font = os.path.join(path_fonts, font_normal)
layer_help_browser_font_size = 16
layer_help_browser_color = (255, 255, 0)
layer_help_browser_color2 = (120, 120, 255)
layer_help_browser_color_link = (255, 120, 120)
layer_help_browser_color_activelink = (255, 255, 255)
layer_help_browser_button = os.path.join(path_dialogs, 'butt-help-close.png')
layer_chat_font = os.path.join(path_fonts, font_normal)
layer_chat_font_size = 14
layer_chat_color = (255, 255, 128)
layer_question_ok = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_question_cancel = os.path.join(path_dialogs, 'butt-cancel-small.png')
layer_question_font = os.path.join(path_fonts, font_normal)
layer_question_font_size = 14
layer_question_color = (255, 255, 128)
layer_input_ok = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_input_cancel = os.path.join(path_dialogs, 'butt-cancel-small.png')
layer_input_font = os.path.join(path_fonts, font_normal)
layer_input_font_size = 14
layer_input_text_size = 14
layer_input_label_color = (255, 255, 128)
layer_input_text_color = (255, 255, 255)
layer_input_bg_color = (128, 128, 128)
layer_menu_font = os.path.join(path_fonts, font_normal)
layer_menu_font_size = 14
layer_menu_color_fg = (200, 200, 200)
layer_menu_color_bg = (0, 0, 0)
layer_menu_color_hi = (255, 255, 0)
layer_targets_mode_color = [(50, 50, 255), (255, 50, 50), (50, 255, 50)]
layer_combatpolicy_checks_y = [20, 50, 80]
layer_combatpolicy_button = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_unit_orders_waypoint_main = os.path.join(path_periphery, 'waypoint-mainsel.png')
layer_unit_orders_waypoint = os.path.join(path_periphery, 'waypoint.png')
layer_unit_orders_move = (255, 255, 255)
layer_unit_orders_movefast = (255, 128, 128)
layer_unit_orders_retreat = (100, 255, 100)
layer_unit_orders_rotate = (160, 160, 255)
layer_unit_orders_attack = (255, 60, 60)
layer_unit_orders_assault = (255, 160, 160)
layer_unit_orders_skirmish = (255, 100, 100)
layer_messages_font_name = os.path.join(path_fonts, font_normal)
layer_messages_font_size = 14
layer_messages_max_width = 300
layer_messages_shadow_color = (0, 0, 0)
layer_weapon_range_color = (255, 50, 50)
layer_weapon_range_width = 2
layer_setresolution_delta_y = 30
layer_setresolution_button = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_togglefeatures_button = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_minimap_unit_colors = ((255, 255, 255), (60, 60, 255))
layer_chooseunits_button = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_armystatus_color_brigade = (255, 255, 255)
layer_armystatus_color_regiment = (255, 128, 128)
layer_armystatus_color_battalion = (160, 160, 255)
layer_armystatus_color_company = (128, 128, 128)
layer_armystatus_color_data_ok = (255, 255, 255)
layer_armystatus_color_data_dead = (255, 80, 80)
layer_armystatus_button_ok = os.path.join(path_dialogs, 'butt-ok-small.png')
layer_armystatus_button_up = os.path.join(path_dialogs, 'butt-up-small.png')
layer_armystatus_button_down = os.path.join(path_dialogs, 'butt-down-small.png')

layer_unit_info_name_pos = (0, 0)
layer_unit_info_type_pos = (0, 15)
layer_unit_info_men_pos = (0, 30)
layer_unit_info_morale_pos = (0, 45)
layer_unit_info_fatigue_pos = (0, 60)
layer_unit_info_experience_pos = (0, 75)
layer_unit_info_terrain_pos = (0, 90)
layer_unit_info_time_pos = (0, 110)

layer_unit_info_cmdr_name_pos = (180, 0)
layer_unit_info_cmdr_exp_pos = (180, 15)
layer_unit_info_cmdr_agg_pos = (180, 30)
layer_unit_info_cmdr_rally_pos = (180, 45)
layer_unit_info_cmdr_motivation_pos = (180, 60)
layer_unit_info_weapon_name_pos = (180, 80)
layer_unit_info_weapon_range_pos = (180, 95)
layer_unit_info_weapon_num_pos = (180, 110)

layer_unit_info_font_name = os.path.join(path_fonts, font_normal)
layer_unit_info_heading_font_size = 10
layer_unit_info_main_font_size = 10
layer_unit_info_font_color = (255, 255, 255)
layer_unit_info_font_name_color = (255, 255, 0)
layer_unit_info_font_type_color = (128, 255, 128)
layer_unit_info_font_mode_color = (200, 200, 255)
layer_unit_info_font_weapon_color = (180, 180, 255)
layer_unit_info_font_status_colors = [(50, 255, 50), (255, 255, 0), (255, 0, 0)]

layer_unit_info_menu_pos = (270, 105)
layer_unit_info_menu_button = os.path.join(path_dialogs, 'butt-infomenu.png')

layer_selection_color = (255, 255, 255)

layer_los_debug_icon = os.path.join(path_periphery, 'grid-los.png')

# setup dialog font and color settings
title_font_name = os.path.join(path_fonts, font_title)
title_font_size = 48
title_font_color = (0, 0, 128)
title_font_background = (0, 0, 0)
normal_font_name = os.path.join(path_fonts, font_normal)
normal_font_size = 24
normal_font_color = (0, 0, 0)
normal_font_color2 = (0, 0, 128)
normal_font_background = (0, 0, 0)
tiny_font_name = os.path.join(path_fonts, font_normal)
tiny_font_size = 14
tiny_font_color = (0, 0, 128)
tiny_font_background = (0, 0, 0)
textfont = os.path.join(path_fonts, font_normal)

checkbox_font_name = os.path.join(path_fonts, font_normal)
checkbox_font_size = 24
checkbox_font_color = (0, 0, 0)
editfield_font_name = os.path.join(path_fonts, font_normal)
editfield_font_size = 24
editfield_font_color = (0, 0, 128)
editfield_background_color = (250, 250, 250)
editfield_use_colorkey = 0
editfield_colorkey_color = (255, 255, 255)
button_use_colorkey = 1
button_colorkey_color = (255, 255, 255)

menu_color = (0, 0, 0)
menu_color_hi = (250, 0, 0)

# window settings
window_size_x = 1024
window_size_y = 768
window_depth = 24
window_hwflags = DOUBLEBUF | HWSURFACE
window_safeflags = 0
window_caption = 'Civil ' + version
window_icon_text = 'Civil'
window_background = os.path.join(path_dialogs, 'dialog-bdrp.png')
credits_background = os.path.join(path_dialogs, 'splash-credits.png')
civil_icon = os.path.join(path_periphery, 'civil-icon-48x48.png')

# dialog settings
dialog_splash = os.path.join(path_dialogs, 'splash-network-loading.png')
messagebox_background = os.path.join(path_dialogs, 'message-background.png')
messagebox_dialog = os.path.join(path_dialogs, 'message.png')
endgame_background = os.path.join(path_dialogs, 'splash-gameover-001.png')
progress_dialog = os.path.join(path_dialogs, 'splash-network-loading.png')
progress_background = os.path.join(path_dialogs, 'message-background.png')
progress_bar_start = os.path.join(path_periphery, 'splash-progressbar-left.png')
progress_bar_mid = os.path.join(path_periphery, 'splash-progressbar-mid2.png')
progress_bar_end = os.path.join(path_periphery, 'splash-progressbar-rht.png')
button_enter_leave = 1

# sounds
widget_button_clicked = os.path.join(path_sound, 'button-clicked.wav')
widget_checkbox_toggled = os.path.join(path_sound, 'checkbox-toggled.wav')
music_intro = os.path.join(path_sound, 'music-intro.mod')
music_main = os.path.join(path_sound, 'music-intro.mod')

# setup dialogs
setup_cursor_normal_data = os.path.join(path_cursors_setup, 'cursors-map-point-001.xbm')
setup_cursor_normal_mask = os.path.join(path_cursors_setup, 'cursors-map-point-mask-001.xbm')
setup_cursor_wait_data = os.path.join(path_cursors_setup, 'cursors-wait-001.xbm')
setup_cursor_wait_mask = os.path.join(path_cursors_setup, 'cursors-wait-001.xbm')

# various states
state_base_cursor_data = os.path.join(path_cursors, 'cursors-map-point-001.xbm')
state_base_cursor_mask = os.path.join(path_cursors, 'cursors-map-point-mask-001.xbm')
state_move_cursor_data = os.path.join(path_cursors, 'cursors-move-001.xbm')
state_move_cursor_mask = os.path.join(path_cursors, 'cursors-move-mask-001.xbm')
state_movefast_cursor_data = os.path.join(path_cursors, 'cursors-move-fast-001.xbm')
state_movefast_cursor_mask = os.path.join(path_cursors, 'cursors-move-fast-mask-001.xbm')
state_retreat_cursor_data = os.path.join(path_cursors, 'cursors-retreat-001.xbm')
state_retreat_cursor_mask = os.path.join(path_cursors, 'cursors-retreat-mask-001.xbm')
state_rotate_cursor_data = os.path.join(path_cursors, 'cursors-map-turn-001.xbm')
state_rotate_cursor_mask = os.path.join(path_cursors, 'cursors-map-turn-mask-001.xbm')
state_attack_cursor_data = os.path.join(path_cursors, 'cursors-map-attack-001.xbm')
state_attack_cursor_mask = os.path.join(path_cursors, 'cursors-map-attack-mask-001.xbm')
state_assault_cursor_data = os.path.join(path_cursors, 'cursors-map-attack-001.xbm')
state_assault_cursor_mask = os.path.join(path_cursors, 'cursors-map-attack-mask-001.xbm')
state_check_los_cursor_data = os.path.join(path_cursors, 'cursors-map-attack-001.xbm')
state_check_los_cursor_mask = os.path.join(path_cursors, 'cursors-map-attack-mask-001.xbm')
state_check_terrain_cursor_data = os.path.join(path_cursors, 'cursors-map-attack-001.xbm')
state_check_terrain_cursor_mask = os.path.join(path_cursors, 'cursors-map-attack-mask-001.xbm')

state_select_delay = 100

# plan settings
plan_font_name = os.path.join(path_fonts, font_normal)
plan_font_size = 10

# hex settings
hex_size = 48
hex_delta_x = 48
hex_delta_y = 36
hex_data_file = os.path.join(path_terrains, "terrains.txt")

hex_los_size = 16
hex_los_delta_x = 16
hex_los_delta_y = 12

# network settings
network_port = 20000
lounge_port = 20002
lounge_host = 'localhost'

# engine and module settings
module_unitsdestroyed_percentage = 0.25
module_morale_minimum = 30

# misc
messages_animation_interval = 10000
messages_max_labels = 15

# In-game pygame event codes for USEREVENTs
USEREVENT_DATA_FROM_SOCKET = 1
