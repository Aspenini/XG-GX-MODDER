import os
import json
import shutil
import sys
import zipfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QFileDialog, QTabWidget, QTextEdit, QMessageBox, QComboBox, QListWidget, 
                             QListWidgetItem, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon
from PIL import Image

class OperaGXModMaker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Opera GX Mod Maker")
        self.setFixedSize(900, 700)  # Increased size to accommodate payload tab

        self.projects_dir = os.path.join(os.path.dirname(__file__), "projects")
        os.makedirs(self.projects_dir, exist_ok=True)

        self.current_mod_path = None
        self.show_main_menu()

    def show_main_menu(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        title_label = QLabel("Opera GX Mod Maker")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(title_label)

        create_button = QPushButton("Create New Mod")
        create_button.clicked.connect(self.create_new_mod)
        create_button.setStyleSheet("""
            QPushButton {
                background-color: #1f538d;
                color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 15px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a6bbf;
            }
        """)
        self.layout.addWidget(create_button)

        scan_label = QLabel("Existing Mods:")
        scan_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        scan_label.setStyleSheet("color: #ffffff;")
        self.layout.addWidget(scan_label)

        self.mod_list = QListWidget()
        self.mod_list.setStyleSheet("""
            QListWidget {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 5px;
                min-width: 300px;
            }
            QListWidget::item {
                padding: 10px;
                margin: 2px;
                border-radius: 5px;
            }
            QListWidget::item:hover {
                background-color: #444444;
            }
        """)
        self.scan_mods()
        self.mod_list.itemDoubleClicked.connect(self.load_mod)
        self.layout.addWidget(self.mod_list)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)

    def scan_mods(self):
        self.mod_list.clear()
        for folder in os.listdir(self.projects_dir):
            mod_path = os.path.join(self.projects_dir, folder)
            if os.path.isdir(mod_path) and os.path.exists(os.path.join(mod_path, "manifest.json")):
                self.mod_list.addItem(QListWidgetItem(folder))

    def create_new_mod(self):
        self.current_mod_path = None
        self.show_edit_window("New Mod")

    def load_mod(self, item):
        mod_name = item.text()
        self.current_mod_path = os.path.join(self.projects_dir, mod_name)
        self.show_edit_window(mod_name)

    def show_edit_window(self, mod_name):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Tabs for different sections
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget {
                background-color: #3a3a3a;
                border: 1px solid #555555;
                border-radius: 10px;
            }
            QTabBar::tab {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px 10px 0 0;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1f538d;
                border-bottom: none;
            }
            QTabWidget::pane {
                border: 1px solid #555555;
                border-radius: 0 0 10px 10px;
                background-color: #2b2b2b;
                padding: 15px;
            }
        """)
        layout.addWidget(tabs)

        # General Info Tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        general_layout.setSpacing(15)

        self.mod_name_entry = QLineEdit()
        self.mod_name_entry.setPlaceholderText("e.g., My Cool Mod")
        self.mod_name_entry.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 1px solid #1f538d;
            }
        """)
        self.mod_name_entry.textChanged.connect(self.update_mod_folder)
        general_layout.addWidget(QLabel("Mod Name:"))
        general_layout.addWidget(self.mod_name_entry)

        self.dev_name_entry = QLineEdit()
        self.dev_name_entry.setPlaceholderText("e.g., John Doe")
        self.dev_name_entry.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 1px solid #1f538d;
            }
        """)
        self.dev_name_entry.textChanged.connect(self.auto_save)
        general_layout.addWidget(QLabel("Your Name:"))
        general_layout.addWidget(self.dev_name_entry)

        self.desc_entry = QLineEdit()
        self.desc_entry.setPlaceholderText("e.g., A cool mod")
        self.desc_entry.setStyleSheet("""
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 1px solid #555555;
                border-radius: 10px;
                padding: 8px;
                font-size: 14px;
                min-width: 400px;
            }
            QLineEdit:focus {
                border: 1px solid #1f538d;
            }
        """)
        self.desc_entry.textChanged.connect(self.auto_save)
        general_layout.addWidget(QLabel("Description:"))
        general_layout.addWidget(self.desc_entry)

        tabs.addTab(general_tab, "General")

        # Payload Options Tab
        payload_tab = QWidget()
        payload_layout = QVBoxLayout(payload_tab)
        payload_layout.setSpacing(20)

        payload_options = [
            ("App Icon", "app_icon", ["id", "name", "path"]),
            ("Wallpaper", "wallpaper", ["id", "name", "dark.image", "light.image"]),
            ("Background Music", "background_music", ["tracks"]),
            ("Browser Sounds", "browser_sounds", ["sounds.CLICK", "sounds.FEATURE_SWITCH_OFF", "sounds.FEATURE_SWITCH_ON", 
                                                  "sounds.HOVER", "sounds.HOVER_UP", "sounds.IMPORTANT_CLICK", 
                                                  "sounds.LEVEL_UPGRADE", "sounds.LIMITER_OFF", "sounds.LIMITER_ON", 
                                                  "sounds.SWITCH_TOGGLE", "sounds.TAB_CLOSE", "sounds.TAB_INSERT", 
                                                  "sounds.TAB_SLASH"]),
            ("Keyboard Sounds", "keyboard_sounds", ["sounds.TYPING_BACKSPACE", "sounds.TYPING_ENTER", "sounds.TYPING_LETTER", 
                                                    "sounds.TYPING_SPACE"]),
            ("Fonts", "fonts", ["header.name", "variants.path"]),
            ("Image Overrides", "image_overrides", ["images.sidebar_bookmarks_button", "images.sidebar_gx_booster_button", 
                                                    "images.sidebar_limiters_button", "images.sidebar_mods_button", 
                                                    "images.sidebar_settings_button", "images.sidebar_shaders_button"]),
            ("Mobile Image Overrides", "mobile_image_overrides", ["images.start_page_logo"]),
            ("Page Styles", "page_styles", ["css", "matches"]),
            ("Shaders", "shaders", ["path"]),
            ("Splash Screen", "splash_screen", ["path"]),
            ("Stickers", "stickers", ["images", "preview"]),
            ("Theme", "theme", ["dark.gx_accent.h", "dark.gx_accent.s", "dark.gx_accent.l", "dark.gx_secondary_base.h", 
                                "dark.gx_secondary_base.s", "dark.gx_secondary_base.l", "light.gx_accent.h", "light.gx_accent.s", 
                                "light.gx_accent.l", "light.gx_secondary_base.h", "light.gx_secondary_base.s", 
                                "light.gx_secondary_base.l"])
        ]

        self.payload_entries = {}
        for label, key, fields in payload_options:
            group_layout = QVBoxLayout()
            group_layout.setSpacing(10)
            group_label = QLabel(f"{label}:")
            group_label.setStyleSheet("color: #ffffff; font-size: 14px; font-weight: bold;")
            group_layout.addWidget(group_label)
            for field in fields:
                field_label = QLabel(f"{field.replace('.', ' > ')}:")
                field_label.setStyleSheet("color: #ffffff; font-size: 12px;")
                h_layout = QHBoxLayout()
                h_layout.setSpacing(10)

                entry = QLineEdit()
                entry.setPlaceholderText(f"Enter {field.replace('.', ' ')} path or value")
                entry.setStyleSheet("""
                    QLineEdit {
                        background-color: #3a3a3a;
                        color: #ffffff;
                        border: 1px solid #555555;
                        border-radius: 10px;
                        padding: 8px;
                        font-size: 12px;
                        min-width: 400px;
                    }
                    QLineEdit:focus {
                        border: 1px solid #1f538d;
                    }
                """)
                entry.textChanged.connect(self.auto_save)
                h_layout.addWidget(field_label)
                h_layout.addWidget(entry)

                browse_button = QPushButton("Browse")
                browse_button.clicked.connect(lambda checked, e=entry, k=key, f=field: self.browse_file(e, k, f))
                browse_button.setStyleSheet("""
                    QPushButton {
                        background-color: #1f538d;
                        color: #ffffff;
                        border: none;
                        border-radius: 10px;
                        padding: 5px 15px;
                        font-size: 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2a6bbf;
                    }
                """)
                h_layout.addWidget(browse_button)
                group_layout.addLayout(h_layout)
                if key not in self.payload_entries:
                    self.payload_entries[key] = {}
                self.payload_entries[key][field] = entry
            payload_layout.addLayout(group_layout)

        tabs.addTab(payload_tab, "Payload Options")

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        zip_button = QPushButton("Create ZIP")
        zip_button.clicked.connect(self.create_zip)
        zip_button.setStyleSheet("""
            QPushButton {
                background-color: #1f538d;
                color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a6bbf;
            }
        """)
        button_layout.addWidget(zip_button)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.manual_save)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #1f538d;
                color: #ffffff;
                border: none;
                border-radius: 15px;
                padding: 10px 30px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a6bbf;
            }
        """)
        button_layout.addWidget(save_button)

        layout.addLayout(button_layout)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)

        if self.current_mod_path:
            self.load_manifest()
        else:
            self.mod_name_entry.setText(mod_name)
            self.dev_name_entry.setText("Anonymous")
            self.desc_entry.setText("A custom Opera GX mod.")

    def browse_file(self, entry, key, field):
        if key in ["app_icon", "wallpaper", "image_overrides", "mobile_image_overrides", "splash_screen", "stickers"]:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {field.replace('.', ' ')}", "", "Image Files (*.jpg *.png *.webp)")
        elif key in ["background_music", "browser_sounds", "keyboard_sounds"]:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {field.replace('.', ' ')}", "", "Audio Files (*.mp3 *.wav)")
        elif key in ["shaders"]:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {field.replace('.', ' ')}", "", "Text Files (*.txt)")
        elif key in ["fonts"]:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {field.replace('.', ' ')}", "", "Font Files (*.ttf)")
        elif key in ["page_styles"]:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {field.replace('.', ' ')}", "", "CSS Files (*.css)")
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, f"Select {field.replace('.', ' ')}", "")

        if file_path:
            entry.setText(file_path)

    def auto_save(self, text=None):
        if self.current_mod_path:
            self.save_manifest()

    def manual_save(self):
        if self.current_mod_path:
            self.save_manifest()
            QMessageBox.information(self, "Success", "Mod saved successfully!")

    def update_mod_folder(self, text):
        new_name = self.mod_name_entry.text().strip() or "My_GX_Mod"
        new_folder = os.path.join(self.projects_dir, f"{new_name.replace(' ', '_')}_Mod")
        
        if self.current_mod_path and self.current_mod_path != new_folder:
            if os.path.exists(self.current_mod_path):
                try:
                    # Rename the folder
                    shutil.move(self.current_mod_path, new_folder)
                    self.current_mod_path = new_folder
                    # Update manifest name if it exists
                    manifest_path = os.path.join(self.current_mod_path, "manifest.json")
                    if os.path.exists(manifest_path):
                        with open(manifest_path, "r") as f:
                            manifest = json.load(f)
                        manifest["name"] = new_name
                        with open(manifest_path, "w") as f:
                            json.dump(manifest, f, indent=2)
                    self.save_manifest()  # Ensure manifest reflects the new name
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to rename folder: {e}")
            else:
                self.current_mod_path = new_folder
                os.makedirs(self.current_mod_path, exist_ok=True)
                self.save_manifest()

    def save_manifest(self):
        mod_name = self.mod_name_entry.text().strip() or "My GX Mod"
        dev_name = self.dev_name_entry.text().strip() or "Anonymous"
        description = self.desc_entry.text().strip() or "A custom Opera GX mod."

        manifest = {
            "manifest_version": 3,
            "name": mod_name,
            "version": "1.0",
            "description": description,
            "developer": {"name": dev_name},
            "icons": {"512": "icon_512.png"},
            "mod": {
                "schema_version": 2,
                "flavor": {
                    "features": [],
                    "hash": "74be16979710d4c4e7c6647856088456",
                    "parent_hash": "d41d8cd98f00b204e9800998ecf8427e"
                },
                "license": "license.txt",
                "payload": {
                    "app_icon": [],
                    "wallpaper": [],
                    "background_music": [],
                    "browser_sounds": [],
                    "keyboard_sounds": [],
                    "fonts": [],
                    "image_overrides": [],
                    "mobile_image_overrides": [],
                    "page_styles": [],
                    "shaders": [],
                    "splash_screen": [],
                    "stickers": [],
                    "theme": []
                }
            },
            "update_url": "https://api.gx.me/store/mods/update"
        }

        # Populate payload from entries
        for key, entries in self.payload_entries.items():
            if key in ["app_icon", "wallpaper", "background_music", "splash_screen", "stickers"]:
                item = {"id": "0", "name": f"{mod_name} {key.capitalize()}"}
                for field, entry in entries.items():
                    value = entry.text().strip()
                    if value:
                        if field == "dark.image" or field == "light.image":
                            self.handle_image(value, key, field.split('.')[1])
                            item[field] = os.path.basename(value) if os.path.exists(value) else value
                        elif field == "tracks" or field == "sounds" or field == "images":
                            item[field] = [v.strip() for v in value.split(',') if v.strip()]
                        else:
                            item[field] = value
                if any(item.values()):
                    manifest["mod"]["payload"][key].append(item)
            elif key == "shaders":
                for field, entry in entries.items():
                    value = entry.text().strip()
                    if value:
                        manifest["mod"]["payload"][key].append({"name": f"{mod_name} Shader", "path": value})
            elif key == "theme":
                dark_accent_h = entries.get("dark.gx_accent.h", QLineEdit()).text().strip() or "211"
                dark_accent_s = entries.get("dark.gx_accent.s", QLineEdit()).text().strip() or "100"
                dark_accent_l = entries.get("dark.gx_accent.l", QLineEdit()).text().strip() or "54"
                dark_base_h = entries.get("dark.gx_secondary_base.h", QLineEdit()).text().strip() or "234"
                dark_base_s = entries.get("dark.gx_secondary_base.s", QLineEdit()).text().strip() or "35"
                dark_base_l = entries.get("dark.gx_secondary_base.l", QLineEdit()).text().strip() or "16"
                light_accent_h = entries.get("light.gx_accent.h", QLineEdit()).text().strip() or "224"
                light_accent_s = entries.get("light.gx_accent.s", QLineEdit()).text().strip() or "100"
                light_accent_l = entries.get("light.gx_accent.l", QLineEdit()).text().strip() or "66"
                light_base_h = entries.get("light.gx_secondary_base.h", QLineEdit()).text().strip() or "210"
                light_base_s = entries.get("light.gx_secondary_base.s", QLineEdit()).text().strip() or "47"
                light_base_l = entries.get("light.gx_secondary_base.l", QLineEdit()).text().strip() or "88"

                theme = {"id": "0", "name": f"{mod_name} Theme"}
                if any([dark_accent_h, dark_accent_s, dark_accent_l, dark_base_h, dark_base_s, dark_base_l]):
                    theme["dark"] = {
                        "gx_accent": {"h": int(dark_accent_h), "s": int(dark_accent_s), "l": int(dark_accent_l)},
                        "gx_secondary_base": {"h": int(dark_base_h), "s": int(dark_base_s), "l": int(dark_base_l)}
                    }
                if any([light_accent_h, light_accent_s, light_accent_l, light_base_h, light_base_s, light_base_l]):
                    theme["light"] = {
                        "gx_accent": {"h": int(light_accent_h), "s": int(light_accent_s), "l": int(light_accent_l)},
                        "gx_secondary_base": {"h": int(light_base_h), "s": int(light_base_s), "l": int(light_base_l)}
                    }
                if theme.get("dark") or theme.get("light"):
                    manifest["mod"]["payload"][key].append(theme)
            else:
                for field, entry in entries.items():
                    value = entry.text().strip()
                    if value:
                        if key not in manifest["mod"]["payload"]:
                            manifest["mod"]["payload"][key] = []
                        manifest["mod"]["payload"][key].append({field: value})

        # Ensure mod folder exists and copy files
        if not self.current_mod_path:
            self.current_mod_path = os.path.join(self.projects_dir, f"{mod_name.replace(' ', '_')}_Mod")
            os.makedirs(self.current_mod_path, exist_ok=True)
        else:
            # Ensure the folder exists with the current name
            if not os.path.exists(self.current_mod_path):
                os.makedirs(self.current_mod_path, exist_ok=True)

        # Create subdirectories
        subdirs = ["app_icon", "css", "font", "icons", "mobile_logo", "music", "shaders", "sounds", "splash", "stickers", "wallpaper"]
        for subdir in subdirs:
            os.makedirs(os.path.join(self.current_mod_path, subdir), exist_ok=True)

        # Save manifest
        with open(os.path.join(self.current_mod_path, "manifest.json"), "w") as f:
            json.dump(manifest, f, indent=2)

    def load_manifest(self):
        if self.current_mod_path:
            manifest_path = os.path.join(self.current_mod_path, "manifest.json")
            if os.path.exists(manifest_path):
                with open(manifest_path, "r") as f:
                    manifest = json.load(f)

                self.mod_name_entry.setText(manifest.get("name", ""))
                self.dev_name_entry.setText(manifest["developer"]["name"])
                self.desc_entry.setText(manifest.get("description", ""))

                payload = manifest["mod"]["payload"]
                for key, entries in self.payload_entries.items():
                    data = payload.get(key, [])
                    if data:
                        if key in ["app_icon", "wallpaper", "background_music", "splash_screen", "stickers"]:
                            item = data[0]
                            for field, entry in entries.items():
                                value = item.get(field, "")
                                if isinstance(value, list):
                                    value = ", ".join(value)
                                entry.setText(value)
                        elif key == "shaders":
                            for i, item in enumerate(data):
                                if i < len(entries):
                                    entries[list(entries.keys())[i]].setText(item.get("path", ""))
                        elif key == "theme":
                            theme = data[0] if data else {}
                            dark_accent = theme.get("dark", {}).get("gx_accent", {"h": 211, "s": 100, "l": 54})
                            dark_base = theme.get("dark", {}).get("gx_secondary_base", {"h": 234, "s": 35, "l": 16})
                            light_accent = theme.get("light", {}).get("gx_accent", {"h": 224, "s": 100, "l": 66})
                            light_base = theme.get("light", {}).get("gx_secondary_base", {"h": 210, "s": 47, "l": 88})
                            entries.get("dark.gx_accent.h", QLineEdit()).setText(str(dark_accent.get("h", 211)))
                            entries.get("dark.gx_accent.s", QLineEdit()).setText(str(dark_accent.get("s", 100)))
                            entries.get("dark.gx_accent.l", QLineEdit()).setText(str(dark_accent.get("l", 54)))
                            entries.get("dark.gx_secondary_base.h", QLineEdit()).setText(str(dark_base.get("h", 234)))
                            entries.get("dark.gx_secondary_base.s", QLineEdit()).setText(str(dark_base.get("s", 35)))
                            entries.get("dark.gx_secondary_base.l", QLineEdit()).setText(str(dark_base.get("l", 16)))
                            entries.get("light.gx_accent.h", QLineEdit()).setText(str(light_accent.get("h", 224)))
                            entries.get("light.gx_accent.s", QLineEdit()).setText(str(light_accent.get("s", 100)))
                            entries.get("light.gx_accent.l", QLineEdit()).setText(str(light_accent.get("l", 66)))
                            entries.get("light.gx_secondary_base.h", QLineEdit()).setText(str(light_base.get("h", 210)))
                            entries.get("light.gx_secondary_base.s", QLineEdit()).setText(str(light_base.get("s", 47)))
                            entries.get("light.gx_secondary_base.l", QLineEdit()).setText(str(light_base.get("l", 88)))
                        else:
                            for i, (field, entry) in enumerate(entries.items()):
                                value = data[i].get(field, "") if i < len(data) else ""
                                if isinstance(value, list):
                                    value = ", ".join(value)
                                entry.setText(value)

    def handle_image(self, path, category, sub_category):
        if not os.path.exists(path):
            return
        dest_dir = os.path.join(self.current_mod_path, category)
        os.makedirs(dest_dir, exist_ok=True)
        filename = os.path.basename(path)
        dest_path = os.path.join(dest_dir, filename)
        try:
            with Image.open(path) as img:
                if category == "app_icon":
                    img.resize((256, 256), Image.Resampling.LANCZOS).save(dest_path, "PNG")
                elif category in ["wallpaper", "splash_screen"]:
                    if sub_category == "image" or sub_category == "path":
                        if img.size[0] < 1920 or img.size[1] < 1080:
                            img.resize((1920, 1080), Image.Resampling.LANCZOS).save(dest_path, "JPEG" if path.endswith('.jpg') else "PNG")
                        else:
                            shutil.copy(path, dest_path)
                else:
                    shutil.copy(path, dest_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process image {filename}: {e}")

    def create_zip(self):
        if self.current_mod_path:
            zip_name = os.path.join(self.current_mod_path, f"{os.path.basename(self.current_mod_path)}.zip")
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(self.current_mod_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, self.current_mod_path)
                        zipf.write(file_path, arcname)
            QMessageBox.information(self, "Success", f"Mod zipped to:\n{zip_name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OperaGXModMaker()
    window.show()
    sys.exit(app.exec())