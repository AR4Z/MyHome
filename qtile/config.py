from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook

from typing import List
import os
import subprocess


mod = "mod4"

keys = [
    # Applications
    Key([mod], "Return", lazy.spawn("alacritty")),
    Key([mod], "b", lazy.spawn("fi-refox")),
    Key([mod], "d", lazy.spawn("rofi -show run")),
    
    # Simple window managment
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod, "shift"], "h", lazy.layout.swap_left()),
    Key([mod, "shift"], "l", lazy.layout.swap_right()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    #Key([mod], "i", lazy.layout.grow()),
    #Key([mod], "m", lazy.layout.shrink()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    Key([mod, "shift"], "space", lazy.layout.flip()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    
    # RESIZE UP, DOWN, LEFT, RIGHT
    Key([mod, "control"], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


    # qtile controls
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    
    # audio controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -q set Master 5%+')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -q set Master 5%-')),
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q set Master toggle')),
   
    # brighness controls
    Key([], 'XF86MonBrightnessUp', lazy.spawn('xbacklight -inc 10')),
    Key([], 'XF86MonBrightnessDown', lazy.spawn('xbacklight -dec 10')),

]

groups = []

group_names = [i for i in '1234567']
group_labels = ['', '', '', '', '', '', '']
for i in range(len(group_names)):
    groups.append(Group(
        name=group_names[i],
        layout="monadtall",
        label=group_labels[i]
    ))

for i in groups:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.MonadTall(),
]

widget_defaults = dict(
    font='sans',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        bottom=bar.Bar(
            [
                widget.GroupBox(font="FontAwesome",
                    fontsize=16,
                    foreground="#ffffff",
                    highlight_method = "text"
                ),
                widget.Sep(),
                widget.WindowName(),
                widget.Wlan(
                    font="FontAwesome",
                    interface='wlp3s0',
                    format="  {essid} {quality}/70",

                ),
                widget.Sep(),
                widget.Volume(emoji=True),
                widget.Sep(),
		        widget.Battery(),
                widget.Sep(),
                widget.Systray(),
                
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            24
        ),
    ),
]

@hook.subscribe.client_new
def assign_app_group(client):
    d = {}
    # assign apps to groups
    d["1"] = ["Alacritty", "alacritty"]
    d["2"] = [ "Code", "code", "code-oss", "Insomnia", "insomnia" ]
    d["3"] = ["Navigator", "navigator","Firefox", "firefox"]
    d["4"] = ["Ranger", "ranger", "mupdf" ]
    d["5"] = ["Spotify", "spotify", "Spotify Free", "Spotify Premmium",  "Vlc", "vlc"]
    d["6"] = ["Franz", "franz", "Mailspring", "mailspring" ]

    print(client.window)
    try:
        wm_class = client.window.get_wm_class()[0]
    except:
        wm_class = client.window.get_name()

    if wm_class in ['alacritty', 'Alacritty'] and client.window.get_name() == 'ranger':
        wm_class = 'ranger'

    for i in range(len(d)):
        if wm_class in list(d.values())[i]:
            group = list(d.keys())[i]
            client.togroup(group)
            client.group.cmd_toscreen()

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"
wmname = "LG3D"
