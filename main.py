from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import json
import urllib.request
import threading

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        # Фон
        with layout.canvas.before:
            Color(0.2, 0.6, 0.8, 1)
            Rectangle(size=Window.size, pos=layout.pos)
        
        # Элементы интерфейса
        self.username = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.6},
            hint_text='Логин',
            multiline=False
        )
        
        self.password = TextInput(
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.45},
            hint_text='Пароль',
            password=True,
            multiline=False
        )
        
        login_btn = Button(
            text='Войти',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.3}
        )
        login_btn.bind(on_press=self.check_credentials)
        
        self.error_label = Label(
            text='',
            size_hint=(0.8, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.15},
            color=(1, 0, 0, 1)
        )
        
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(self.error_label)
        self.add_widget(layout)
    
    def check_credentials(self, instance):
        threading.Thread(target=self._check_credentials_thread).start()
    
    def _check_credentials_thread(self):
        try:
            # Загружаем данные с GitHub (используем raw ссылку)
            url = 'https://raw.githubusercontent.com/ateistsatanic/keys/main/info.json'
            with urllib.request.urlopen(url) as response:
                data = json.loads(response.read().decode())
            
            username = self.username.text.strip()
            password = self.password.text.strip()
            
            print(f"Введено: {username}/{password}")  # Для отладки
            print(f"Данные из JSON: {data}")  # Для отладки
            
            # Ищем пользователя в массиве объектов
            user_found = False
            for user in data:
                if (user.get('Username') == username and 
                    user.get('Password') == password):
                    user_found = True
                    break
            
            if user_found:
                Clock.schedule_once(lambda dt: self.show_main_screen())
            else:
                Clock.schedule_once(lambda dt: self.show_error("Неверный логин или пароль"))
                
        except Exception as e:
            print(f"Ошибка: {e}")  # Для отладки
            Clock.schedule_once(lambda dt: self.show_error(f"Ошибка подключения: {str(e)}"))
    
    def show_error(self, message):
        self.error_label.text = message
    
    def show_main_screen(self):
        self.manager.current = 'main'

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.3, 0.7, 0.3, 1)
            Rectangle(size=Window.size, pos=layout.pos)
        
        enable_btn = Button(
            text='Включить автотайпер',
            size_hint=(0.8, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        enable_btn.bind(on_press=self.show_info)
        
        layout.add_widget(enable_btn)
        self.add_widget(layout)
    
    def show_info(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        
        content = BoxLayout(orientation='vertical', padding=10)
        content.add_widget(Label(
            text='Функционал overlay кнопки и автотайпера\nбудет работать на Android',
            text_size=(300, None)
        ))
        
        popup = Popup(
            title='Информация',
            content=content,
            size_hint=(0.7, 0.4)
        )
        popup.open()

class AutotyperApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    AutotyperApp().run()