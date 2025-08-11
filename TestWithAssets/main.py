from android.media import SoundPool
from base_plugin import BasePlugin
from elyx import assets
from ui.bulletin import BulletinHelper
from ui.settings import Divider, Header, Text


class TestWithAssets(BasePlugin):
    def on_plugin_load(self):
        self.sound_pool = SoundPool(1, 3, 0)
        self.sound_id = self.sound_pool.load(assets.notification.path_str, 1)

    def create_settings(self):
        return [
            Header("Sounds"),
            Text(
                text="Play sound-asset notification.wav",
                accent=True,
                on_click=lambda *_: self.play_sound(),
                icon="msg_filled_data_music"
            ),
            Divider(),
            Header("Lottie-animations"),
            Text(
                text="Run simple bulletin with custom lottie-animation",
                accent=True,
                on_click=lambda *_: self.show_bulletin_with_lottie_anim()
            ),
            Text(
                text="Run two-line bulletin with custom lottie-animation",
                accent=True,
                on_click=lambda *_: self.show_bulletin_with_lottie_anim(True)
            ),
            Divider(),
            Header("Assets-images"),
            Text(
                text="Run simple bulletin with custom image",
                accent=True,
                on_click=lambda *_: self.show_bulletin()
            ),
            Text(
                text="Run two-line bulletin with custom image",
                accent=True,
                on_click=lambda *_: self.show_bulletin(True)
            ),
            Divider(),
            Header("Assets-svg"),
            Text(
                text="Run simple bulletin with custom svg",
                accent=True,
                on_click=lambda *_: self.show_bulletin(svg=True)
            ),
            Text(
                text="Run two-line bulletin with custom svg",
                accent=True,
                on_click=lambda *_: self.show_bulletin(True, svg=True)
            ),
        ]
    
    def play_sound(self):
        self.sound_pool.play(self.sound_id, 1.0, 1.0, 1, 0, 1.0)

    def show_bulletin_with_lottie_anim(self, two_line: bool = False):
        lottie_drawable = assets.check.to_lottie_drawable(48, 48)
        if two_line:
            BulletinHelper.show_two_line("Test title", "Test subtitle", lottie_drawable)
        else:
            BulletinHelper.show_simple("Test bulletin", lottie_drawable)

    def show_bulletin(self, two_line: bool = False, svg: bool = False):
        if svg:
            drawable = assets.cactus_logo.to_svg_drawable(64, 64)
        else:
            drawable = assets.folder.to_bitmap_drawable(64, 64)
        
        if two_line:
            BulletinHelper.show_two_line("Test title", "Test subtitle", drawable)
        else:
            BulletinHelper.show_simple("Test bulletin", drawable)
