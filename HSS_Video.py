import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.camera import Camera
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import os

class VideoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.video_player = VideoPlayer()
        self.layout.add_widget(self.video_player)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        self.comment_button = Button(text=u'\uF0E0', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.comment_button.bind(on_press=self.add_comment)
        buttons_layout.add_widget(self.comment_button)

        self.upload_button = Button(text=u'\uF093', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.upload_button.bind(on_press=self.upload_video)
        buttons_layout.add_widget(self.upload_button)

        self.delete_button = Button(text=u'\uF1F8', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.delete_button.bind(on_press=self.delete_video)
        buttons_layout.add_widget(self.delete_button)

        self.record_button = Button(text=u'\uF030', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.record_button.bind(on_press=self.record_video)
        buttons_layout.add_widget(self.record_button)

        self.pause_button = Button(text=u'\uF04C', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.pause_button.bind(on_press=self.pause_video)
        buttons_layout.add_widget(self.pause_button)

        self.play_button = Button(text=u'\uF04B', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.play_button.bind(on_press=self.play_video)
        buttons_layout.add_widget(self.play_button)

        self.mute_button = Button(text=u'\uF028', font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf', font_size=30, size_hint_x=None, width=50)
        self.mute_button.bind(on_press=self.mute_video)
        buttons_layout.add_widget(self.mute_button)

        self.layout.add_widget(buttons_layout)
        return self.layout

    def upload_video(self, instance):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView(filters=['*.mp4', '*.avi', '*.mkv'], path='/storage/emulated/0/')
        content.add_widget(filechooser)

        select_button = Button(text='Select')
        content.add_widget(select_button)

        popup = Popup(title='Upload Video', content=content, size_hint=(0.9, 0.9))

        def select(instance):
            selected_file = filechooser.selection
            if selected_file:
                self.video_player.source = selected_file[0]
                self.video_player.state = 'play'
            popup.dismiss()

        select_button.bind(on_press=select)
        popup.open()

    def delete_video(self, instance):
        self.video_player.source = ''
        self.video_player.state = 'stop'

    def pause_video(self, instance):
        self.video_player.state = 'pause'

    def play_video(self, instance):
        self.video_player.state = 'play'

    def mute_video(self, instance):
        # Toggle mute functionality
        if self.video_player.volume > 0:
            self.video_player.volume = 0
        else:
            self.video_player.volume = 1

    def add_comment(self, instance):
        content = BoxLayout(orientation='vertical')
        text_input = TextInput(hint_text='Add a comment', multiline=True, font_size=20, size_hint_y=None, height=100)
        content.add_widget(text_input)

        post_button = Button(text='Post')
        content.add_widget(post_button)

        popup = Popup(title='Add Comment', content=content, size_hint=(0.9, 0.9))

        def post(instance):
            comment = text_input.text
            # Add code to save or display the comment
            popup.dismiss()

        post_button.bind(on_press=post)
        popup.open()

    def record_video(self, instance):
        # Start camera recording
        content = BoxLayout(orientation='vertical')

        self.camera = Camera(play=True, resolution=(640, 480))
        content.add_widget(self.camera)

        record_button = Button(text='Start Recording')
        content.add_widget(record_button)

        stop_button = Button(text='Stop Recording', disabled=True)
        content.add_widget(stop_button)

        popup = Popup(title='Record Video', content=content, size_hint=(0.9, 0.9))

        def start_record(instance):
            record_button.disabled = True
            stop_button.disabled = False

            # Set up file path for saving the video
            self.video_file_path = '/storage/emulated/0/Movies/recorded_video.mp4'

            # Start recording using Android's media recorder (using Kivy's camera)
            self.camera.start()

        def stop_record(instance):
            record_button.disabled = False
            stop_button.disabled = True

            # Stop the camera and save the video
            self.camera.stop()
            self.camera.export_to_png(self.video_file_path)  # Saving as video
            popup.dismiss()

            # Load the recorded video into the video player
            self.video_player.source = self.video_file_path
            self.video_player.state = 'play'

        record_button.bind(on_press=start_record)
        stop_button.bind(on_press=stop_record)
        popup.open()

if __name__ == '__main__':
    Window.clearcolor = (1, 1, 1, 1)
    VideoApp().run()