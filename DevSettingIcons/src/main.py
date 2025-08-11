"""
>>==================================================================<<
||    ____           _             ____  _             _            ||
||   / ___|__ _  ___| |_ _   _ ___|  _ \| |_   _  __ _(_)_ __  ___  ||
||  | |   / _` |/ __| __| | | / __| |_) | | | | |/ _` | | '_ \/ __| ||
||  | |__| (_| | (__| |_| |_| \__ \  __/| | |_| | (_| | | | | \__ \ ||
||   \____\__,_|\___|\__|\__,_|___/_|   |_|\__,_|\__, |_|_| |_|___/ ||
||     ____           _ _   _     _              |___/              ||
||    / __ \__      _(_) |_| |__ | | _____   _____                  ||
||   / / _` \ \ /\ / / | __| '_ \| |/ _ \ \ / / _ \                 ||
||  | | (_| |\ V  V /| | |_| | | | | (_) \ V /  __/                 ||
||   \ \__,_| \_/\_/ |_|\__|_| |_|_|\___/ \_/ \___|                 ||
||                                                                  ||
||                   https://t.me/CactusPlugins                     ||
||     https://github.com/Den4ikSuperOstryyPer4ik/CactusPlugins     ||
||                                                                  ||
||          ПОЖАЛУЙСТА НЕ КОПИРУЙТЕ КОД НЕ УВЕДОМИВ МЕНЯ.           ||
||        PLEASE DO NOT COPY THIS CODE WITHOUT NOTIFYING ME.        ||
>>==================================================================<<
"""
from base_plugin import BasePlugin
from elyx import strings
from org.telegram.messenger import R
from ui.settings import Divider, Header, Input, Selector, Text

from ..assets import drawables_blacklist, raw_types
from .sheets import AnimationSheet, IconsSheet


class DevSettingIcons(BasePlugin):
    def __init__(self):
        super().__init__()
        self.icons = {}
        self.animations = {}

    def on_plugin_load(self) -> None:
        self.icons = {
            i: getattr(R.drawable, i)
            for i in dir(R.drawable)
            if all([x in ('abcdefghijklmnopqrstuvwxyz' + '0123456789' + '_') for x in i]) and not i.startswith('_') and i not in drawables_blacklist["list"]
        }
        self.animations = {
            anim_id: getattr(R.raw, anim_id)
            for anim_id in raw_types["json"]
        }
 
    def create_settings(self):
        return [
            Header(text=strings["icons"]),
            Input(key="icon_filter", text=strings["search"], icon="msg_search", default=""),
            Selector(
                key="icon_type",
                text=strings["type"],
                default=0,
                items=[strings["all"], "Solar", "Remix", "Default"],
                icon="menu_select_quote_solar"
            ),
            Text(
                text=strings["show_as_grid"],
                accent=True,
                on_click=lambda _: IconsSheet(self, 0).show(),
                icon="input_bot2_solar"
            ),
            Text(
                text=strings["show_as_list"],
                accent=True,
                on_click=lambda _: IconsSheet(self, 1).show(),
                icon="msg_reorder"
            ),
            Divider(),
            Header(text=strings["animations"]),
            Input(key="animation_filter", text=strings["search"], icon="msg_search", default=""),
            Text(
                text=strings["show_as_grid"],
                accent=True,
                on_click=lambda _: AnimationSheet(self, 0).show(),
                icon="input_bot2_solar"
            ),
            Text(
                text=strings["show_as_list"],
                accent=True,
                on_click=lambda _: AnimationSheet(self, 1).show(),
                icon="msg_reorder"
            ),
        ]
