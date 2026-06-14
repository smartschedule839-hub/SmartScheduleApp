# Authentication system completed
import json
import os
import hashlib

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from datetime import datetime
import re
from kivy.uix.checkbox import CheckBox
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.checkbox import CheckBox

USERS_FILE = "smart_schedule_users.json"
SCHEDULE_FILE = "smart_schedule_items.json"

Window.size = (430, 720)
Window.clearcolor = (0.92, 0.95, 0.99, 1)

PRIMARY = (0.10, 0.30, 0.72, 1)
SUCCESS = (0.08, 0.55, 0.30, 1)
WARNING = (0.90, 0.50, 0.10, 1)
DANGER = (0.78, 0.10, 0.12, 1)
SECONDARY = (0.35, 0.37, 0.42, 1)
TEXT_DARK = (0.12, 0.14, 0.18, 1)
TEXT_MUTED = (0.40, 0.43, 0.48, 1)
CARD_BG = (1, 1, 1, 1)


def load_json(filename, default_data):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as file:
                return json.load(file)
        except:
            return default_data
    return default_data


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class RoundedButton(Button):
    def __init__(self, text="", colour=PRIMARY, **kwargs):
        super().__init__(**kwargs)

        self.text = text
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = 14
        self.bold = True

        with self.canvas.before:
            Color(*colour)
            self.rect = RoundedRectangle(radius=[18])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class Card(BoxLayout):
    def __init__(self, bg_colour=CARD_BG, radius=18, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*bg_colour)
            self.rect = RoundedRectangle(radius=[radius])

        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


def create_button(text, colour=PRIMARY, height=46):
    return RoundedButton(
        text=text,
        colour=colour,
        size_hint=(1, None),
        height=height
    )


def create_input(hint, password=False, multiline=False, height=45):
    return TextInput(
        hint_text=hint,
        password=password,
        multiline=multiline,
        size_hint=(1, None),
        height=height,
        font_size=14,
        padding=(12, 10),
        background_normal="",
        background_active="",
        background_color=(1, 1, 1, 1),
        foreground_color=TEXT_DARK,
        cursor_color=PRIMARY
    )


def temporary_message(label, text, seconds=4):
    label.text = text
    Clock.schedule_once(lambda dt: setattr(label, "text", ""), seconds)

class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=16
        )

        layout.add_widget(Label(
            text="Smart Schedule",
            font_size=34,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=75
        ))

        layout.add_widget(Label(
            text="Plan classes, study sessions, tasks, and deadlines in one place.",
            font_size=15,
            color=TEXT_MUTED,
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=90,
            text_size=(360, None)
        ))

        login_button = create_button("→ LOGIN", PRIMARY, height=52)
        login_button.bind(on_press=self.go_to_login)
        layout.add_widget(login_button)

        register_button = create_button("+ CREATE ACCOUNT", SUCCESS, height=52)
        register_button.bind(on_press=self.go_to_register)
        layout.add_widget(register_button)

        layout.add_widget(Label(
            text="A simple mobile planner for academic scheduling.",
            font_size=13,
            color=TEXT_MUTED,
            size_hint=(1, None),
            height=45
        ))

        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = "login"

    def go_to_register(self, instance):
        self.manager.current = "register"


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=22,
            spacing=10
        )

        layout.add_widget(Label(
            text="Create Account",
            font_size=27,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=55
        ))

        self.full_name = create_input("Full name")
        layout.add_widget(self.full_name)

        self.username = create_input("Username")
        layout.add_widget(self.username)

        self.password = create_input("Password", password=True)
        layout.add_widget(self.password)

        self.confirm_password = create_input("Confirm password", password=True)
        layout.add_widget(self.confirm_password)

        self.message = Label(
            text="",
            color=DANGER,
            font_size=13,
            size_hint=(1, None),
            height=40
        )
        layout.add_widget(self.message)

        register_button = create_button("✓ REGISTER", SUCCESS, height=50)
        register_button.bind(on_press=self.register_user)
        layout.add_widget(register_button)

        back_button = create_button("← BACK TO WELCOME", SECONDARY, height=50)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def register_user(self, instance):
        full_name = self.full_name.text.strip()
        username = self.username.text.strip()
        password = self.password.text.strip()
        confirm_password = self.confirm_password.text.strip()

        if full_name == "" or username == "" or password == "" or confirm_password == "":
            temporary_message(self.message, "All fields are required")
            return

        if not full_name.replace(" ", "").isalpha():
            temporary_message(self.message, "Full name should contain letters only")
            return

        if len(username) < 3:
            temporary_message(self.message, "Username must be at least 3 characters")
            return

        password_pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,}$"

        if not re.match(password_pattern, password):
            temporary_message(
                self.message,
                "Password needs uppercase, lowercase, number and 6+ characters"
            )
            return

        if password != confirm_password:
            temporary_message(self.message, "Passwords do not match")
            return

        users = load_json(USERS_FILE, {})

        if username in users:
            temporary_message(self.message, "Username already exists")
            return

        users[username] = {
            "full_name": full_name,
            "password": hash_password(password),
            "profile_picture": ""
        }

        save_json(USERS_FILE, users)

        self.full_name.text = ""
        self.username.text = ""
        self.password.text = ""
        self.confirm_password.text = ""

        self.message.color = SUCCESS
        temporary_message(self.message, "Account created. You can now login.")

    def go_back(self, instance):
        self.manager.current = "welcome"


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=12
        )

        layout.add_widget(Label(
            text="Welcome Back",
            font_size=28,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=65
        ))

        layout.add_widget(Label(
            text="Login to continue managing your schedule.",
            font_size=14,
            color=TEXT_MUTED,
            size_hint=(1, None),
            height=35
        ))

        self.username = create_input("Username")
        layout.add_widget(self.username)

        self.password = create_input("Password", password=True)
        layout.add_widget(self.password)

        self.message = Label(
            text="",
            color=DANGER,
            font_size=13,
            size_hint=(1, None),
            height=32
        )
        layout.add_widget(self.message)

        login_button = create_button("→ LOGIN", PRIMARY, height=50)
        login_button.bind(on_press=self.login_user)
        layout.add_widget(login_button)

        back_button = create_button("← BACK TO WELCOME", SECONDARY, height=50)
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def login_user(self, instance):
        username = self.username.text.strip()
        password = self.password.text.strip()

        if username == "" or password == "":
            temporary_message(self.message, "Username and password are required")
            return

        users = load_json(USERS_FILE, {})

        if username not in users:
            temporary_message(self.message, "Account does not exist")
            return

        if users[username]["password"] != hash_password(password):
            temporary_message(self.message, "Incorrect password")
            return

        app = App.get_running_app()
        app.current_user = username

        self.username.text = ""
        self.password.text = ""
        self.message.text = ""

        self.manager.get_screen("dashboard").refresh_dashboard()
        self.manager.current = "dashboard"

    def go_back(self, instance):
        self.manager.current = "welcome"


class ProtectedScreen(Screen):
    def on_pre_enter(self):
        app = App.get_running_app()

        if app.current_user is None:
            self.manager.current = "welcome"


class DashboardScreen(ProtectedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=26,
            spacing=12
        )

        layout.add_widget(Label(
            text="Dashboard",
            font_size=30,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=58
        ))

        self.welcome_label = Label(
            text="",
            font_size=17,
            bold=True,
            color=TEXT_DARK,
            size_hint=(1, None),
            height=38
        )
        layout.add_widget(self.welcome_label)

        self.summary_label = Label(
            text="",
            font_size=14,
            color=TEXT_MUTED,
            size_hint=(1, None),
            height=45
        )
        layout.add_widget(self.summary_label)

        progress_card = Card(
            orientation="vertical",
            padding=12,
            spacing=6,
            size_hint=(1, None),
            height=115
        )

        self.progress_title = Label(
            text="Completion Progress",
            font_size=15,
            bold=True,
            color=TEXT_DARK,
            size_hint=(1, None),
            height=28
        )
        progress_card.add_widget(self.progress_title)

        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(1, None),
            height=18
        )
        progress_card.add_widget(self.progress_bar)

        self.progress_label = Label(
            text="0% completed",
            font_size=13,
            color=TEXT_MUTED,
            size_hint=(1, None),
            height=28
        )
        progress_card.add_widget(self.progress_label)

        layout.add_widget(progress_card)

        schedule_button = create_button(
            "📅 SCHEDULE MANAGEMENT",
            PRIMARY,
            height=52
        )
        schedule_button.bind(on_press=self.open_schedule)
        layout.add_widget(schedule_button)

        add_button = create_button(
            "+ ADD SCHEDULE ITEM",
            SUCCESS,
            height=52
        )
        add_button.bind(on_press=self.open_add_schedule)
        layout.add_widget(add_button)

        settings_button = create_button(
            "⚙ SETTINGS / PROFILE",
            SECONDARY,
            height=52
        )
        settings_button.bind(on_press=self.open_settings)
        layout.add_widget(settings_button)

        logout_button = create_button(
            "⏻ LOGOUT",
            DANGER,
            height=48
        )
        logout_button.bind(on_press=self.logout)
        layout.add_widget(logout_button)

        self.add_widget(layout)

    def refresh_dashboard(self):
        app = App.get_running_app()

        users = load_json(USERS_FILE, {})

        schedules = load_json(SCHEDULE_FILE, [])

        user_schedules = []

        for item in schedules:
            if item.get("username") == app.current_user:
                user_schedules.append(item)

        completed = []

        for item in user_schedules:
            if item.get("completed") is True:
                completed.append(item)

        pending = len(user_schedules) - len(completed)

        if len(user_schedules) == 0:
            progress_value = 0
        else:
            progress_value = int((len(completed) / len(user_schedules)) * 100)

        if app.current_user in users:
            self.welcome_label.text = f"Welcome, {users[app.current_user]['full_name']}"
        else:
            self.welcome_label.text = "Welcome"

        self.summary_label.text = (
            f"Schedule Items: {len(user_schedules)} | "
            f"Completed: {len(completed)} | "
            f"Pending: {pending}"
        )

        self.progress_bar.value = progress_value

        self.progress_label.text = f"{progress_value}% completed"

    def open_schedule(self, instance):
        self.manager.current = "schedule"

    def open_add_schedule(self, instance):
        add_screen = self.manager.get_screen("add_schedule")
        add_screen.prepare_new_schedule()
        self.manager.current = "add_schedule"

    def open_settings(self, instance):
        self.manager.current = "settings"

    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = "welcome"


class ScheduleManagementScreen(ProtectedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.user_schedules = []

        layout = BoxLayout(orientation="vertical", padding=14, spacing=8)

        layout.add_widget(Label(
            text="Schedule Management",
            font_size=25,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=48
        ))

        self.search_input = create_input("Search schedule items", height=42)
        self.search_input.bind(text=self.search_schedules)
        layout.add_widget(self.search_input)

        top_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint=(1, None),
            height=38
        )

        back_button = create_button("← BACK", SECONDARY, height=38)
        back_button.bind(on_press=self.go_back)
        top_buttons.add_widget(back_button)

        refresh_button = create_button("↻ REFRESH", PRIMARY, height=38)
        refresh_button.bind(on_press=self.refresh_schedules)
        top_buttons.add_widget(refresh_button)

        layout.add_widget(top_buttons)

        self.message = Label(
            text="",
            color=SUCCESS,
            font_size=12,
            size_hint=(1, None),
            height=24
        )
        layout.add_widget(self.message)

        scroll = ScrollView()

        self.schedule_list = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.schedule_list.bind(minimum_height=self.schedule_list.setter("height"))

        scroll.add_widget(self.schedule_list)
        layout.add_widget(scroll)

        self.add_widget(layout)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.refresh_schedules(None)

    def refresh_schedules(self, instance):
        app = App.get_running_app()
        all_schedules = load_json(SCHEDULE_FILE, [])

        self.user_schedules = [
            item for item in all_schedules
            if item.get("username") == app.current_user
        ]

        self.display_schedules(self.user_schedules)
        temporary_message(self.message, "Schedules refreshed")

    def save_user_schedules(self):
        app = App.get_running_app()
        all_schedules = load_json(SCHEDULE_FILE, [])

        other_users_schedules = [
            item for item in all_schedules
            if item.get("username") != app.current_user
        ]

        save_json(SCHEDULE_FILE, other_users_schedules + self.user_schedules)

    def display_schedules(self, schedules):
        self.schedule_list.clear_widgets()

        if len(schedules) == 0:
            self.schedule_list.add_widget(Label(
                text="No schedule items found.\nTap ADD SCHEDULE ITEM from the dashboard.",
                size_hint_y=None,
                height=80,
                color=TEXT_MUTED,
                font_size=15
            ))
            return

        for item in schedules:
            real_index = self.user_schedules.index(item)
            status = "Completed" if item.get("completed") else "Pending"

            card = Card(
                orientation="horizontal",
                padding=10,
                spacing=8,
                size_hint_y=None,
                height=158
            )

            details_side = BoxLayout(
                orientation="vertical",
                spacing=3,
                size_hint_x=0.68
            )

            details_side.add_widget(Label(
                text=f"{item.get('title')}",
                bold=True,
                font_size=15,
                halign="left",
                text_size=(260, None),
                color=SUCCESS if item.get("completed") else TEXT_DARK
            ))

            details_side.add_widget(Label(
                text=f"Module: {item.get('module')}",
                font_size=13,
                halign="left",
                text_size=(260, None),
                color=TEXT_MUTED
            ))

            details_side.add_widget(Label(
                text=f"Date: {item.get('date')} | Time: {item.get('time')}",
                font_size=13,
                halign="left",
                text_size=(260, None),
                color=TEXT_MUTED
            ))

            details_side.add_widget(Label(
                text=f"Priority: {item.get('priority')}",
                font_size=13,
                halign="left",
                text_size=(260, None),
                color=WARNING if item.get("priority") == "High" else TEXT_MUTED
            ))

            details_side.add_widget(Label(
                text=f"Status: {status}",
                font_size=13,
                halign="left",
                text_size=(260, None),
                color=SUCCESS if item.get("completed") else WARNING
            ))

            button_side = BoxLayout(
                orientation="vertical",
                spacing=6,
                size_hint_x=0.32
            )

            complete_button = create_button(
                "UNDO" if item.get("completed") else "DONE",
                SUCCESS,
                height=34
            )
            complete_button.bind(on_press=lambda instance, i=real_index: self.toggle_complete(i))
            button_side.add_widget(complete_button)

            edit_button = create_button("EDIT", WARNING, height=34)
            edit_button.bind(on_press=lambda instance, i=real_index: self.edit_schedule(i))
            button_side.add_widget(edit_button)

            delete_button = create_button("DELETE", DANGER, height=34)
            delete_button.bind(on_press=lambda instance, i=real_index: self.delete_schedule(i))
            button_side.add_widget(delete_button)

            card.add_widget(details_side)
            card.add_widget(button_side)

            self.schedule_list.add_widget(card)

    def toggle_complete(self, index):
        self.user_schedules[index]["completed"] = not self.user_schedules[index]["completed"]
        self.save_user_schedules()
        self.display_schedules(self.user_schedules)
        temporary_message(self.message, "Schedule status updated")

    def edit_schedule(self, index):
        selected_item = self.user_schedules[index]
        add_screen = self.manager.get_screen("add_schedule")
        add_screen.prepare_edit_schedule(index, selected_item)
        self.manager.current = "add_schedule"

    def delete_schedule(self, index):
        self.user_schedules.pop(index)
        self.save_user_schedules()
        self.display_schedules(self.user_schedules)
        temporary_message(self.message, "Schedule item deleted")

    def search_schedules(self, instance, value):
        keyword = value.lower().strip()

        if keyword == "":
            self.display_schedules(self.user_schedules)
            return

        filtered = []

        for item in self.user_schedules:
            status = "completed" if item.get("completed") else "pending"

            if (
                keyword in item.get("title", "").lower()
                or keyword in item.get("module", "").lower()
                or keyword in item.get("date", "").lower()
                or keyword in item.get("time", "").lower()
                or keyword in item.get("priority", "").lower()
                or keyword in item.get("notes", "").lower()
                or keyword in status
            ):
                filtered.append(item)

        self.display_schedules(filtered)

    def go_back(self, instance):
        self.manager.get_screen("dashboard").refresh_dashboard()
        self.manager.current = "dashboard"


class AddScheduleScreen(ProtectedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.edit_index = None

        layout = BoxLayout(
            orientation="vertical",
            padding=16,
            spacing=8
        )

        self.page_title = Label(
            text="Add Schedule Item",
            font_size=25,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=48
        )
        layout.add_widget(self.page_title)

        top_buttons = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint=(1, None),
            height=38
        )

        back_button = create_button("← BACK", SECONDARY, height=38)
        back_button.bind(on_press=self.go_back)
        top_buttons.add_widget(back_button)

        clear_button = create_button("CLEAR", WARNING, height=38)
        clear_button.bind(on_press=self.clear_form)
        top_buttons.add_widget(clear_button)

        layout.add_widget(top_buttons)

        self.title_input = create_input("Activity title", height=42)
        layout.add_widget(self.title_input)

        self.module_input = create_input("Module / Subject", height=42)
        layout.add_widget(self.module_input)

        self.date_input = create_input("Date e.g. 2026-06-11", height=42)
        layout.add_widget(self.date_input)

        self.time_input = create_input("Time e.g. 09:00", height=42)
        layout.add_widget(self.time_input)

        priority_label = Label(
            text="Select Priority",
            font_size=14,
            bold=True,
            color=TEXT_DARK,
            size_hint=(1, None),
            height=26
        )
        layout.add_widget(priority_label)

        priority_row = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint=(1, None),
            height=38
        )

        self.high_priority = CheckBox(group="priority", size_hint=(None, None), size=(30, 30))
        self.medium_priority = CheckBox(group="priority", size_hint=(None, None), size=(30, 30))
        self.low_priority = CheckBox(group="priority", size_hint=(None, None), size=(30, 30))

        self.medium_priority.active = True

        priority_row.add_widget(Label(text="High", color=TEXT_DARK, font_size=13))
        priority_row.add_widget(self.high_priority)

        priority_row.add_widget(Label(text="Medium", color=TEXT_DARK, font_size=13))
        priority_row.add_widget(self.medium_priority)

        priority_row.add_widget(Label(text="Low", color=TEXT_DARK, font_size=13))
        priority_row.add_widget(self.low_priority)

        layout.add_widget(priority_row)

        self.notes_input = create_input("Notes", multiline=True, height=80)
        layout.add_widget(self.notes_input)

        self.message = Label(
            text="",
            color=DANGER,
            font_size=12,
            size_hint=(1, None),
            height=28
        )
        layout.add_widget(self.message)

        self.save_button = create_button("SAVE SCHEDULE", SUCCESS, height=46)
        self.save_button.bind(on_press=self.save_schedule)
        layout.add_widget(self.save_button)

        self.add_widget(layout)

    def get_selected_priority(self):
        if self.high_priority.active:
            return "High"
        elif self.low_priority.active:
            return "Low"
        else:
            return "Medium"

    def set_selected_priority(self, priority):
        self.high_priority.active = False
        self.medium_priority.active = False
        self.low_priority.active = False

        if priority == "High":
            self.high_priority.active = True
        elif priority == "Low":
            self.low_priority.active = True
        else:
            self.medium_priority.active = True

    def prepare_new_schedule(self):
        self.edit_index = None
        self.page_title.text = "Add Schedule Item"
        self.save_button.text = "SAVE SCHEDULE"
        self.clear_form(None)

    def prepare_edit_schedule(self, index, item):
        self.edit_index = index
        self.page_title.text = "Edit Schedule Item"
        self.save_button.text = "UPDATE SCHEDULE"

        self.title_input.text = item.get("title", "")
        self.module_input.text = item.get("module", "")
        self.date_input.text = item.get("date", "")
        self.time_input.text = item.get("time", "")
        self.set_selected_priority(item.get("priority", "Medium"))
        self.notes_input.text = item.get("notes", "")
        self.message.text = ""

    def save_schedule(self, instance):
        title = self.title_input.text.strip()
        module = self.module_input.text.strip()
        date = self.date_input.text.strip()
        time = self.time_input.text.strip()
        priority = self.get_selected_priority()
        notes = self.notes_input.text.strip()

        if len(title) < 3:
            temporary_message(self.message, "Title must contain at least 3 characters")
            return

        if module == "":
            temporary_message(self.message, "Module is required")
            return

        if date == "":
            temporary_message(self.message, "Date is required")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            temporary_message(self.message, "Date must be YYYY-MM-DD")
            return

        if time != "":
            try:
                datetime.strptime(time, "%H:%M")
            except:
                temporary_message(self.message, "Time must be HH:MM")
                return

        app = App.get_running_app()
        schedules = load_json(SCHEDULE_FILE, [])

        user_schedules = []
        other_users_schedules = []

        for item in schedules:
            if item.get("username") == app.current_user:
                user_schedules.append(item)
            else:
                other_users_schedules.append(item)

        schedule_item = {
            "username": app.current_user,
            "title": title,
            "module": module,
            "date": date,
            "time": time,
            "priority": priority,
            "notes": notes,
            "completed": False
        }

        if self.edit_index is None:
            user_schedules.append(schedule_item)
        else:
            schedule_item["completed"] = user_schedules[self.edit_index]["completed"]
            user_schedules[self.edit_index] = schedule_item

        save_json(SCHEDULE_FILE, other_users_schedules + user_schedules)

        schedule_screen = self.manager.get_screen("schedule")
        schedule_screen.refresh_schedules(None)

        self.clear_form(None)
        self.manager.current = "schedule"

    def clear_form(self, instance):
        self.title_input.text = ""
        self.module_input.text = ""
        self.date_input.text = ""
        self.time_input.text = ""
        self.set_selected_priority("Medium")
        self.notes_input.text = ""
        self.message.text = ""

    def go_back(self, instance):
        self.manager.get_screen("dashboard").refresh_dashboard()
        self.manager.current = "dashboard"


class SettingsScreen(ProtectedScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        layout.add_widget(Label(
            text="Settings / Profile",
            font_size=26,
            bold=True,
            color=PRIMARY,
            size_hint=(1, None),
            height=50
        ))

        self.profile_image = Image(
            source="",
            size_hint=(1, None),
            height=120
        )
        layout.add_widget(self.profile_image)

        select_picture_button = create_button(
            "SELECT PROFILE PICTURE",
            PRIMARY,
            height=42
        )
        select_picture_button.bind(on_press=self.open_file_chooser)
        layout.add_widget(select_picture_button)

        self.profile_label = Label(
            text="",
            font_size=14,
            color=TEXT_DARK,
            size_hint=(1, None),
            height=230
        )
        layout.add_widget(self.profile_label)

        dark_row = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint=(1, None),
            height=42
        )

        dark_row.add_widget(Label(
            text="Dark Mode",
            font_size=15,
            bold=True,
            color=TEXT_DARK
        ))

        self.dark_checkbox = CheckBox(
            size_hint=(None, None),
            size=(35, 35)
        )
        self.dark_checkbox.bind(active=self.toggle_dark_mode)

        dark_row.add_widget(self.dark_checkbox)
        layout.add_widget(dark_row)

        button_row = BoxLayout(
            orientation="horizontal",
            spacing=8,
            size_hint=(1, None),
            height=44
        )

        back_button = create_button("← BACK", SECONDARY, height=44)
        back_button.bind(on_press=self.go_back)
        button_row.add_widget(back_button)

        logout_button = create_button("⏻ LOGOUT", DANGER, height=44)
        logout_button.bind(on_press=self.logout)
        button_row.add_widget(logout_button)

        layout.add_widget(button_row)

        self.add_widget(layout)

    def on_pre_enter(self):
        super().on_pre_enter()
        self.refresh_profile()

    def refresh_profile(self):
        app = App.get_running_app()

        users = load_json(USERS_FILE, {})
        schedules = load_json(SCHEDULE_FILE, [])

        user_schedules = [
            item for item in schedules
            if item.get("username") == app.current_user
        ]

        completed = [
            item for item in user_schedules
            if item.get("completed") is True
        ]

        pending = len(user_schedules) - len(completed)

        if app.current_user in users:
            user = users[app.current_user]

            picture_path = user.get("profile_picture", "")

            if picture_path != "" and os.path.exists(picture_path):
                self.profile_image.source = picture_path
            else:
                self.profile_image.source = ""

            self.profile_image.reload()

            self.dark_checkbox.active = user.get("dark_mode", False)

            self.profile_label.text = (
                f"Full Name: {user['full_name']}\n\n"
                f"Username: {app.current_user}\n\n"
                f"Saved Schedule Items: {len(user_schedules)}\n\n"
                f"Completed Items: {len(completed)}\n\n"
                f"Pending Items: {pending}\n\n"
                f"Storage Method: Local JSON files\n\n"
                f"Application: Smart Schedule"
            )

            self.apply_theme(user.get("dark_mode", False))

        else:
            self.profile_label.text = "No profile information found."

    def open_file_chooser(self, instance):
        chooser = FileChooserIconView(
            filters=["*.png", "*.jpg", "*.jpeg"]
        )

        popup_layout = BoxLayout(
            orientation="vertical",
            spacing=8,
            padding=8
        )

        popup_layout.add_widget(chooser)

        select_button = Button(
            text="Use Selected Image",
            size_hint=(1, None),
            height=45
        )

        popup_layout.add_widget(select_button)

        popup = Popup(
            title="Select Profile Picture",
            content=popup_layout,
            size_hint=(0.95, 0.85)
        )

        select_button.bind(
            on_press=lambda btn: self.save_profile_picture(
                chooser.selection,
                popup
            )
        )

        popup.open()

    def save_profile_picture(self, selection, popup):
        if len(selection) == 0:
            return

        selected_path = selection[0]

        app = App.get_running_app()
        users = load_json(USERS_FILE, {})

        if app.current_user in users:
            users[app.current_user]["profile_picture"] = selected_path
            save_json(USERS_FILE, users)

        popup.dismiss()
        self.refresh_profile()

    def toggle_dark_mode(self, checkbox, value):
        app = App.get_running_app()
        users = load_json(USERS_FILE, {})

        if app.current_user in users:
            users[app.current_user]["dark_mode"] = value
            save_json(USERS_FILE, users)

        self.apply_theme(value)

    def apply_theme(self, dark_mode):
        if dark_mode:
            Window.clearcolor = (0.10, 0.11, 0.14, 1)
            self.profile_label.color = (0.95, 0.95, 0.95, 1)
        else:
            Window.clearcolor = (0.92, 0.95, 0.99, 1)
            self.profile_label.color = TEXT_DARK

    def go_back(self, instance):
        self.manager.get_screen("dashboard").refresh_dashboard()
        self.manager.current = "dashboard"

    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        self.manager.current = "welcome"

class SmartScheduleApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user = None

    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(WelcomeScreen(name="welcome"))
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(ScheduleManagementScreen(name="schedule"))
        sm.add_widget(AddScheduleScreen(name="add_schedule"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm


if __name__ == "__main__":
    SmartScheduleApp().run()
