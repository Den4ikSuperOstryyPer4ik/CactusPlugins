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

from android.content import DialogInterface
from android.text import SpannableStringBuilder
from android.view import Gravity
from android.widget import FrameLayout, LinearLayout, ScrollView
from android_utils import log
from androidx.core.content import ContextCompat
from com.exteragram.messenger.preferences.components import AltSeekbar
from elyx import OnClickListener, gen, strings
from org.telegram.messenger import AndroidUtilities, R
from org.telegram.ui.ActionBar import AlertDialog
from org.telegram.ui.Components import (ColoredImageSpan, LayoutHelper,
                                        RLottieImageView)
from org.telegram.ui.Stories.recorder import ButtonWithCounterView
from ui.bulletin import BulletinHelper

dp = AndroidUtilities.dp
OnDismissListener = gen(DialogInterface.OnDismissListener, "onDismiss")


def show_icon_full(activity, icon):
    try:
        builder = AlertDialog.Builder(activity)

        frameLayout = FrameLayout(activity)
        builder.setView(frameLayout)

        scrollView = ScrollView(activity)
        scrollView.setFillViewport(True)
        frameLayout.addView(scrollView, LayoutHelper.createFrame(-1, -1))

        linearLayout = LinearLayout(activity)
        linearLayout.setOrientation(LinearLayout.VERTICAL)
        linearLayout.setGravity(Gravity.CENTER_HORIZONTAL)
        scrollView.addView(linearLayout, LayoutHelper.createFrame(-1, -2, Gravity.LEFT | Gravity.TOP))

        lockImageView = RLottieImageView(activity)
        lockImageView.setImageResource(getattr(R.drawable, icon))
        linearLayout.addView(lockImageView, LayoutHelper.createLinear(256, 256, Gravity.CENTER_HORIZONTAL))

        def on_change(p):
            lockImageView.setLayoutParams(LayoutHelper.createLinear(int(p), int(p)))
            lockImageView.invalidate()
            seek.invalidate()

        seek = AltSeekbar(activity, gen(AltSeekbar.OnDrag, "run")(lambda p: on_change(p)), 24, 256, strings["icon_size"], strings["min"], strings["max"])
        seek.setProgress(1)
        linearLayout.addView(seek, LayoutHelper.createLinear(-1, -2))

        copy_button = ButtonWithCounterView(activity, False, None)
        span = ColoredImageSpan(ContextCompat.getDrawable(activity, R.drawable.msg_copy))
        string_builder = SpannableStringBuilder()
        string_builder.append("d ").setSpan(span, 0, 1, 0)
        string_builder.append(icon)
        copy_button.setText(string_builder, False)
        copy_button.setOnClickListener(OnClickListener(
            lambda _: (
                BulletinHelper.show_copied_to_clipboard()
                if AndroidUtilities.addToClipboard(icon)
                else None
            )
        ))

        linearLayout.addView(copy_button, LayoutHelper.createLinear(-1, 48, 0, 16, 28, 16, 16))

        dialog = builder.create()
        dialog.show()
    except:
        log(traceback.format_exc())


def show_full_animation(activity, animation, play_all):
    try:
        builder = AlertDialog.Builder(activity)

        frameLayout = FrameLayout(activity)
        builder.setView(frameLayout)

        scrollView = ScrollView(activity)
        scrollView.setFillViewport(True)
        frameLayout.addView(scrollView, LayoutHelper.createFrame(-1, -1))

        linearLayout = LinearLayout(activity)
        linearLayout.setOrientation(LinearLayout.VERTICAL)
        linearLayout.setGravity(Gravity.CENTER_HORIZONTAL)
        scrollView.addView(linearLayout, LayoutHelper.createFrame(-1, -2, Gravity.LEFT | Gravity.TOP))

        animationView = RLottieImageView(activity)
        animationView.setAutoRepeat(True)
        animationView.setAnimation(getattr(R.raw, animation), 256, 256)
        animationView.playAnimation()
        linearLayout.addView(animationView, LayoutHelper.createLinear(256, 256, Gravity.CENTER_HORIZONTAL))

        def on_change(p):
            animationView.setLayoutParams(LayoutHelper.createLinear(int(p), int(p)))
            animationView.invalidate()
            seek.invalidate()

        seek = AltSeekbar(activity, gen(AltSeekbar.OnDrag, "run")(lambda p: on_change(p)), 24, 256, strings["animation_size"], strings["min"], strings["max"])
        seek.setProgress(1)
        linearLayout.addView(seek, LayoutHelper.createLinear(-1, -2))

        def on_click(_=None, first: bool = False):
            if not first:
                if animationView.isPlaying():
                    animationView.stopAnimation()
                else:
                    animationView.playAnimation()
            
            span = ColoredImageSpan(ContextCompat.getDrawable(activity, R.drawable.msg_round_pause_m if first or animationView.isPlaying() else R.drawable.msg_round_play_m))
            string_builder = SpannableStringBuilder()
            string_builder.append("d ").setSpan(span, 0, 1, 0)
            string_builder.append(strings["pause"] if first or animationView.isPlaying() else strings["play"])
            play_button.setText(string_builder, False)
        
        play_button = ButtonWithCounterView(activity, True, None)
        play_button.setOnClickListener(OnClickListener(on_click))
        on_click(None, True)
        linearLayout.addView(play_button, LayoutHelper.createLinear(-1, 48, 0, 16, 28, 16, 4))

        copy_button = ButtonWithCounterView(activity, False, None)
        span = ColoredImageSpan(ContextCompat.getDrawable(activity, R.drawable.msg_copy))
        string_builder = SpannableStringBuilder()
        string_builder.append("d ").setSpan(span, 0, 1, 0)
        string_builder.append(animation)
        copy_button.setText(string_builder, False)
        copy_button.setOnClickListener(OnClickListener(
            lambda _: (
                BulletinHelper.show_copied_to_clipboard()
                if AndroidUtilities.addToClipboard(animation)
                else None
            )
        ))
        linearLayout.addView(copy_button, LayoutHelper.createLinear(-1, 48, 0, 16, 4, 16, 8))

        builder.setOnPreDismissListener(OnDismissListener(lambda _: play_all()))

        dialog = builder.create()
        dialog.show()
    except:
        log(traceback.format_exc())
