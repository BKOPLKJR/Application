import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import sqlite3
import os
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.graphics.texture import Texture
from kivy.uix.filechooser import FileChooserIconView
from kivy.core.window import Window
from kivy.core.text import LabelBase

# Ensure the font file is in the correct directory
LabelBase.register(name='FontAwesome',
                   fn_regular='/storage/emulated/0/Movies/fontawesome-free-6.6.0-web/webfonts/fa-solid-900.ttf')

class SocialMediaApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.comments_label = Label(text='', font_size=20)
        self.layout.add_widget(self.comments_label)
        self.image_widget = AsyncImage()
        self.layout.add_widget(self.image_widget)
        self.comment_input = TextInput(hint_text='Comment', multiline=False, font_size=20)
        self.layout.add_widget(self.comment_input)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.comment_button = Button(text=u'\uF0E0', font_name='FontAwesome', font_size=30)
        self.comment_button.bind(on_press=self.add_comment)
        buttons_layout.add_widget(self.comment_button)
        self.upload_button = Button(text=u'\uF093', font_name='FontAwesome', font_size=30)
        self.upload_button.bind(on_press=self.upload_image)
        buttons_layout.add_widget(self.upload_button)
        self.delete_button = Button(text=u'\uF1F8', font_name='FontAwesome', font_size=30)
        self.delete_button.bind(on_press=self.delete_image)
        buttons_layout.add_widget(self.delete_button)
        self.camera_button = Button(text=u'\uF030', font_name='FontAwesome', font_size=30)
        self.camera_button.bind(on_press=self.take_photo)
        buttons_layout.add_widget(self.camera_button)
        self.layout.add_widget(buttons_layout)
        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_once(self.load_image, 1)
        return self.layout
    def load_image(self, dt):
        # Load image from database or storage
        self.image_widget.source = 'image1.png'

    def add_comment(self, instance):
        # Add comment to database
        comment = self.comment_input.text
        self.comments_label.text += comment + '\n'
        self.comment_input.text = ''

    def delete_image(self, instance):
        # Delete image from database or storage
        self.image_widget.source = ''

    def upload_image(self, instance):
        # Open file chooser to select image from storage
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView()
        content.add_widget(filechooser)
        select_button = Button(text='Select')
        content.add_widget(select_button)
        popup = Popup(title='Upload Image', content=content, size_hint=(0.9, 0.9))
        def select_image(instance):
            selected_file = filechooser.selection
            if selected_file:
                self.image_widget.source = selected_file[0]
                popup.dismiss()
        select_button.bind(on_press=select_image)
        popup.open()

    def take_photo(self, instance):
        # Take photo using camera
        self.camera = Camera(play=False)
        self.layout.add_widget(self.camera)
        self.camera_button.text = u'\uF03D'
        self.camera_button.unbind(on_press=self.take_photo)
        self.camera_button.bind(on_press=self.capture_photo)

    def capture_photo(self, instance):
        # Capture photo and display
        texture = self.camera.texture
        self.image_widget.texture = texture
        self.camera_button.text = u'\uF030'
        self.camera_button.unbind(on_press=self.capture_photo)
        self.camera_button.bind(on_press=self.take_photo)
        self.layout.remove_widget(self.camera)

    def on_key_down(self, window, keycode, scancode, codepoint, modifier):
        if keycode == 13:  # Enter key
            self.add_comment(None)

if __name__ == '__main__':
    SocialMediaApp().run()