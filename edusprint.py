import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget,
                             QPushButton, QHBoxLayout, QLineEdit, QToolBar, QAction,
                             QMessageBox, QLabel, QComboBox, QCheckBox)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QPixmap

os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu --disable-software-rasterizer'


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌐 VagoBrowser PRO")
        self.setGeometry(100, 100, 1200, 800)

        self.dark_mode = True
        self.incognito_mode = False
        self.history = []
        self.bookmarks = []

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_on_tab_change)
        self.setCentralWidget(self.tabs)

        self.create_navbar()
        self.apply_theme()

        self.add_new_tab("https://google.com", "Home")

    def create_navbar(self):
        self.nav_bar = QToolBar()
        self.addToolBar(self.nav_bar)

        # Logo (replace with your custom logo path)
        logo_label = QLabel()
        pixmap = QPixmap("your_logo.png")  # Replace with your logo file path
        logo_label.setPixmap(pixmap.scaled(32, 32, Qt.KeepAspectRatio))
        self.nav_bar.addWidget(logo_label)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.nav_bar.addWidget(self.url_bar)

        # Buttons
        buttons = {
            "⬅️": self.go_back,
            "➡️": self.go_forward,
            "🔄": self.refresh_page,
            "➕ New Tab": self.new_tab,
            "🕒 History": self.show_history,
            "⭐ Bookmarks": self.show_bookmarks,
            "🌗 Theme": self.toggle_theme,
            "🛡️ AdBlock": self.toggle_adblock,
            "👀 Incognito": self.toggle_incognito
        }

        for name, action in buttons.items():
            btn = QAction(name, self)
            btn.triggered.connect(action)
            self.nav_bar.addAction(btn)

        # Language Selector
        self.language_selector = QComboBox()
        self.language_selector.addItems(["🌍 English", "🌐 Hindi", "🌏 Marathi"])
        self.language_selector.currentIndexChanged.connect(self.switch_language)
        self.nav_bar.addWidget(self.language_selector)

        # Frequent Sites
        nav_buttons = QHBoxLayout()
        for name, url in self.get_frequent_sites().items():
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, u=url: self.add_new_tab(u, name))
            nav_buttons.addWidget(btn)
        nav_widget = QWidget()
        nav_widget.setLayout(nav_buttons)
        self.nav_bar.addWidget(nav_widget)

    def get_frequent_sites(self):
        return {
            "📚 EduSprint+": "https://jns.edusprint.in",
            "📺 YouTube": "https://youtube.com",
            "💻 LeetCode": "https://leetcode.com",
            "🗨️ Discord": "https://discord.com",
            "🎮 Poki": "https://poki.com",
            "💡 ChatGPT": "https://chat.openai.com",
            "📌 Jira": "https://jira.atlassian.com"
        }

    def add_new_tab(self, url, label):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))

        browser.settings().setAttribute(QWebEngineSettings.AutoLoadImages, True)
        browser.page().titleChanged.connect(lambda title, browser=browser: self.update_tab_title(browser, title))
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_url_bar(qurl, browser))

        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        self.url_bar.setText(url)
        if not self.incognito_mode:
            self.history.append(url)

    def update_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title)

    def update_url_bar(self, qurl, browser):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(qurl.toString())

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser = self.tabs.currentWidget()
        if isinstance(current_browser, QWebEngineView):
            current_browser.setUrl(QUrl(url))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def update_url_on_tab_change(self, index):
        browser = self.tabs.widget(index)
        if isinstance(browser, QWebEngineView):
            self.url_bar.setText(browser.url().toString())

    def go_back(self):
        browser = self.tabs.currentWidget()
        if browser:
            browser.back()

    def go_forward(self):
        browser = self.tabs.currentWidget()
        if browser:
            browser.forward()

    def refresh_page(self):
        browser = self.tabs.currentWidget()
        if browser:
            browser.reload()

    def new_tab(self):
        self.add_new_tab("https://google.com", "New Tab")

    def show_history(self):
        if self.history:
            history_text = "\n".join(self.history)
            QMessageBox.information(self, "Browsing History", history_text)
        else:
            QMessageBox.information(self, "History", "No browsing history found.")

    def show_bookmarks(self):
        if self.bookmarks:
            bookmarks_text = "\n".join(self.bookmarks)
            QMessageBox.information(self, "Bookmarks", bookmarks_text)
        else:
            QMessageBox.information(self, "Bookmarks", "No bookmarks yet.")

        # Save current page to bookmarks
        url = self.url_bar.text()
        if url not in self.bookmarks:
            self.bookmarks.append(url)
            QMessageBox.information(self, "Bookmarks", f"Saved: {url}")
        else:
            self.bookmarks.remove(url)
            QMessageBox.information(self, "Bookmarks", f"Removed: {url}")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #121212;
                    color: white;
                }
                QPushButton, QLineEdit, QComboBox {
                    background-color: #1e1e1e;
                    color: #00ffc8;
                    border-radius: 8px;
                    padding: 6px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #333;
                    color: white;
                }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #f0f0f0;
                    color: black;
                }
                QPushButton, QLineEdit, QComboBox {
                    background-color: white;
                    color: black;
                    border-radius: 8px;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #ddd;
                }
            """)

    def switch_language(self, index):
        lang = self.language_selector.currentText()
        QMessageBox.information(self, "Language Switched", f"Current Language: {lang}")

    def toggle_incognito(self):
        self.incognito_mode = not self.incognito_mode
        status = "ON" if self.incognito_mode else "OFF"
        QMessageBox.information(self, "Incognito Mode", f"Incognito Mode is {status}")

    def toggle_adblock(self):
        # Placeholder feature: Add actual AdBlock functionality if needed
        QMessageBox.information(self, "AdBlock", "AdBlock toggled (simulation only).")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
