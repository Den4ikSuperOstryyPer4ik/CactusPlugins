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
||            ПОЖАЛУЙСТА НЕ КОПИРУЙТЕ КОД НЕ УВЕДОМИВ МЕНЯ.         ||
||          PLEASE DO NOT COPY THIS CODE WITHOUT NOTIFYING ME.      ||
>>==================================================================<<
"""
import traceback

from android.util import TypedValue
from android.view import Gravity
from android.widget import FrameLayout, ImageView, LinearLayout, TextView
from android_utils import log as logcat
from android_utils import run_on_ui_thread
from androidx.appcompat.widget import AppCompatImageView
from androidx.core.content import ContextCompat
from client_utils import get_last_fragment, run_on_queue
from com.exteragram.messenger import ExteraResources
from elyx import OnClickListener, gen, strings
from org.telegram.messenger import AndroidUtilities, Utilities
from org.telegram.ui.ActionBar import BottomSheet, Theme
from org.telegram.ui.Components import (LayoutHelper, RLottieImageView, UItem,
                                        UniversalRecyclerView)

from .dialogs import show_full_animation, show_icon_full

_types = {
    1: "Solar",
    2: "Remix",
    3: "Default"
}


Callback2 = gen(Utilities.Callback2, "run")
Callback5 = gen(Utilities.Callback5, "run")


class ResourcesBottomSheet:
    title = ""
    filter_setting = ""
    type_setting = ""

    def __init__(self, lib, vtype):
        self.lib = lib
        self.vtype = vtype
        self.fragment = get_last_fragment()
        self.activity = self.fragment.getParentActivity()
        self.context = self.fragment.getContext()

        self._loaded = False
        self._items = []
        self.count = 0
        self.filter = self.lib.get_setting(self.filter_setting, "").lower()

        self.builder = None
        self.bottomSheet = None

        run_on_queue(lambda: self._load_all())

    def _load_all(self):
        pass

    def fill_items(self, items, adapter):
        try:
            _type = self.lib.get_setting(self.type_setting, 0) if self.type_setting else None
            title = self.title + (" • " + self.filter if self.filter else "") + (" • " + _types[_type] if _type and _type != 0 else "")

            if not self._loaded:
                items.add(UItem.asHeader(strings["loading"]))
            else:
                for item in self._items:
                    items.add(item)
                
                title += f" ({self.count})"

            (self.bottomSheet if self.bottomSheet else self.builder).setTitle(title, True)
        except:
            items.add(UItem.asShadow(traceback.format_exc()))

    def on_click(self, *_):
        pass

    def show(self):
        self.builder = builder = BottomSheet.Builder(self.activity)

        builder.setApplyTopPadding(False)
        builder.setApplyBottomPadding(False)

        contentView = FrameLayout(self.activity)
        builder.setCustomView(contentView)

        contentView.setBackgroundColor(Theme.getColor(Theme.key_windowBackgroundGray))

        self.listView = listView = UniversalRecyclerView(self.fragment, Callback2(self.fill_items), Callback5(self.on_click), None)
        contentView.addView(listView, LayoutHelper.createFrame(-1, 700))

        self.bottomSheet = builder.show()
        self.bottomSheet.setCanDismissWithSwipe(False)


class IconsSheet(ResourcesBottomSheet):
    title = strings["icons"]
    filter_setting = "icon_filter"
    type_setting = "icon_type"

    def _load_all(self):
        if self._loaded:
            return
    
        try:
            _filter = self.filter
            _type = self.lib.get_setting(self.type_setting, 0)

            try:
                exteraResources = self.context.getResources()
                if not isinstance(exteraResources, ExteraResources):
                    exteraResources = ExteraResources(exteraResources)
            except:
                logcat(traceback.format_exc())
                exteraResources = None
            
            if self.vtype == 0:
                linear_layout = LinearLayout(self.activity)

                width = self.context.getResources().getDisplayMetrics().widthPixels
                icon_width = (64 + AndroidUtilities.dp(28 + 7))
                row_size = width // icon_width

                frame = LayoutHelper.createFrame(64, 64, 0, 0, 0, int((width - icon_width*row_size) / row_size), 0)
                scale = ImageView.ScaleType.CENTER

                k = 0

                for icon, icon_res_id in self.lib.icons.items():
                    try:
                        if _filter:
                            if _filter not in icon:
                                continue

                        if _type != 0:
                            if _type == 1 and "solar" not in icon:
                                continue
                            elif _type == 2 and "remix" not in icon:
                                continue
                            elif (
                                _type == 3
                                and (
                                    ("solar" in icon or "remix" in icon)
                                    or not (
                                        f"{icon}_remix" in self.lib.icons
                                        or f"{icon}_solar" in self.lib.icons
                                    )
                                )
                            ):
                                continue
                        
                        k += 1
                        self.count += 1

                        icb = AppCompatImageView(self.activity)
                        icb.setScaleType(scale)
                        icb.setImageDrawable((exteraResources.getOriginalDrawable(icon_res_id) if exteraResources else ContextCompat.getDrawable(self.activity, icon_res_id)).mutate())
                        icb.setBackground(Theme.createSelectorDrawable(Theme.getColor(Theme.key_dialogButtonSelector), 1, AndroidUtilities.dp(28)))
                        icb.setOnClickListener(OnClickListener(self.open_icon(icon)))
                        linear_layout.addView(icb, frame)

                        if k == row_size:
                            self._items.append(UItem.asCustom(linear_layout))
                            linear_layout = LinearLayout(self.activity)
                            k = 0
                    except:
                        self.lib.log(f"Icon {icon} is not found: {traceback.format_exc()}")
                
                if k != 0:
                    self._items.append(UItem.asCustom(linear_layout))
            elif self.vtype == 1:
                for icon, icon_res_id in self.lib.icons.items():
                    try:
                        if _filter:
                            if _filter not in icon:
                                continue

                        if _type != 0:
                            if _type == 1 and "solar" not in icon:
                                continue
                            elif _type == 2 and "remix" not in icon:
                                continue
                            elif (
                                _type == 3
                                and (
                                    ("solar" in icon or "remix" in icon)
                                    or not (
                                        f"{icon}_remix" in self.lib.icons
                                        or f"{icon}_solar" in self.lib.icons
                                    )
                                )
                            ):
                                continue
                        
                        drawable = (exteraResources.getOriginalDrawable(icon_res_id) if exteraResources else ContextCompat.getDrawable(self.activity, icon_res_id)).mutate()
                        self._items.append(UItem.asButton(0, drawable, icon))
                        self.count += 1
                    except:
                        self.lib.log(f"Icon {icon} is not found: {traceback.format_exc()}")
        except:
            self.items.append(UItem.asShadow(traceback.format_exc()))
        
        self._loaded = True
        run_on_ui_thread(lambda: self.listView.adapter.update(True))
    
    def open_icon(self, icon):
        def _fn(_=None):
            try:
                show_icon_full(self.activity, icon)
            except:
                logcat(traceback.format_exc())
        return _fn

    def on_click(self, item, *_):
        if self.vtype == 1:
            self.open_icon(item.text)()


class AnimationSheet(ResourcesBottomSheet):
    title = strings["animations"]
    filter_setting = "animation_filter"

    def _load_all(self):
        if self._loaded:
            return
    
        self.all = []
        try:
            _filter = self.filter

            try:
                exteraResources = self.context.getResources()
                if not isinstance(exteraResources, ExteraResources):
                    exteraResources = ExteraResources(exteraResources)
            except:
                logcat(traceback.format_exc())
                exteraResources = None
            
            scale = ImageView.ScaleType.CENTER

            if self.vtype == 0:
                linear_layout = LinearLayout(self.activity)

                width = self.context.getResources().getDisplayMetrics().widthPixels
                icon_width = (AndroidUtilities.dp(56))
                row_size = width // icon_width - 1

                frame = LayoutHelper.createFrame(48, 48, 0, 0, 0, int((width - icon_width*row_size) / row_size), 0)

                k = 0

                for animation, anim_res_id in self.lib.animations.items():
                    try:
                        if _filter:
                            if _filter not in animation:
                                continue

                        k += 1
                        self.count += 1

                        icb = RLottieImageView(self.activity)
                        icb.setScaleType(scale)
                        icb.setAutoRepeat(True)
                        icb.setAnimation(anim_res_id, 46, 46)
                        icb.playAnimation()
                        icb.setBackground(Theme.createSelectorDrawable(Theme.getColor(Theme.key_dialogButtonSelector), 1, AndroidUtilities.dp(28)))
                        icb.setOnClickListener(OnClickListener(self.open_animation(animation)))
                        linear_layout.addView(icb, frame)

                        self.all.append(icb)

                        if k == row_size:
                            self._items.append(UItem.asCustom(linear_layout))
                            linear_layout = LinearLayout(self.activity)
                            k = 0
                    except:
                        self.lib.log(f"Animation {animation} is not found: {traceback.format_exc()}")
                
                if k != 0:
                    self._items.append(UItem.asCustom(linear_layout))
            elif self.vtype == 1:
                frame = LayoutHelper.createFrame(48, 48, 0, 8, 4, 0, 4)
                frame2 = LayoutHelper.createFrame(-2, -2, Gravity.CENTER_VERTICAL, 12, 0, 0, 0)
                text_color = Theme.getColor(Theme.key_windowBackgroundWhiteBlackText)

                for animation, anim_res_id in self.lib.animations.items():
                    try:
                        if _filter:
                            if _filter not in animation:
                                continue

                        layout = LinearLayout(self.activity)
                        
                        icb = RLottieImageView(self.activity)
                        icb.setScaleType(scale)
                        icb.setAutoRepeat(True)
                        icb.setAnimation(anim_res_id, 46, 46)
                        icb.playAnimation()
                        self.all.append(icb)
                        layout.addView(icb, frame)

                        text_view = TextView(self.activity)
                        text_view.setTextColor(text_color)
                        text_view.setTextSize(TypedValue.COMPLEX_UNIT_DIP, 18)
                        text_view.setGravity(Gravity.CENTER_VERTICAL)
                        text_view.setText(animation)
                        layout.addView(text_view, frame2)

                        item = UItem.asCustom(layout)
                        item.object2 = animation
                        self._items.append(item)
                        self.count += 1
                    except:
                        self.lib.log(f"Animation {animation} is not found: {traceback.format_exc()}")
        except:
            self.items.append(UItem.asShadow(traceback.format_exc()))
        
        self._loaded = True
        run_on_ui_thread(lambda: self.listView.adapter.update(True))
    
    def open_animation(self, anim):
        def _fn(_=None):
            try:
                for dr in self.all:
                    dr.stopAnimation()
                
                def play_all():
                    for dr in self.all:
                        dr.playAnimation()
                
                show_full_animation(self.activity, anim, play_all)
            except:
                logcat(traceback.format_exc())
        return _fn

    def on_click(self, item, *_):
        if self.vtype == 1:
            self.open_animation(item.object2)()
