import cv2
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.camera import Camera
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.textinput import TextInput
import threading

class VideoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.video_player = VideoPlayer()
        self.layout.add_widget(self.video_player)

        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)

        self.record_button = Button(
            text='Record Video',
            font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf',
            font_size=30
        )
        self.record_button.bind(on_press=self.record_video)
        buttons_layout.add_widget(self.record_button)

        self.upload_button = Button(
            text=u'\uF093',
            font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf',
            font_size=30
        )
        self.upload_button.bind(on_press=self.upload_video)
        buttons_layout.add_widget(self.upload_button)

        self.delete_button = Button(
            text=u'\uF1F8',
            font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf',
            font_size=30
        )
        self.delete_button.bind(on_press=self.delete_video)
        buttons_layout.add_widget(self.delete_button)

        self.comment_button = Button(
            text=u'\uF0E0',
            font_name='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf',
            font_size=30
        )
        self.comment_button.bind(on_press=self.add_comment)
        buttons_layout.add_widget(self.comment_button)

        self.layout.add_widget(buttons_layout)
        return self.layout

    def record_video(self, instance):
        self.camera = Camera(play=True)
        self.layout.add_widget(self.camera)
        self.record_button.text = 'Stop Recording'
        self.record_button.unbind(on_press=self.record_video)
        self.record_button.bind(on_press=self.stop_recording)

    def stop_recording(self, instance):
        self.camera.play = False
        self.layout.remove_widget(self.camera)
        self.record_button.text = 'Record Video'
        self.record_button.unbind(on_press=self.stop_recording)
        self.record_button.bind(on_press=self.record_video)
        self.save_video()

    def save_video(self):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView(path='/storage/emulated/0/')
        content.add_widget(filechooser)
        save_button = Button(text='Save')
        content.add_widget(save_button)
        popup = Popup(title='Save Video', content=content, size_hint=(0.9, 0.9))

        def save(instance):
            selected_path = filechooser.selection
            if selected_path:
                # Use opencv-python to save the video
                cap = cv2.VideoCapture(0)
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(selected_path[0] + '/recorded_video.mp4', fourcc, 20.0, (640, 480))
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    out.write(frame)
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                self.video_player.source = selected_path[0] + '/recorded_video.mp4'
                self.video_player.state = 'play'
                popup.dismiss()

        save_button.bind(on_press=save)
        popup.open()

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

if __name__ == '__main__':
    VideoApp().run()
