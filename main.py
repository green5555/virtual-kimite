import sys
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QAction

from config import AppConfig
from overlay import OverlayWindow
from settings_window import SettingsWindow

class MainApp:
    def __init__(self):
        # PySide6 Application 초기화
        self.app = QApplication(sys.argv)
        
        # 마지막 창이 닫혀도 애플리케이션이 완전히 종료되지 않게 설정 (트레이 상주용)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 설정 관리 객체 생성
        self.config = AppConfig()
        
        # 오버레이 윈도우 및 설정 컨트롤러 윈도우 생성
        self.overlay = OverlayWindow(self.config)
        self.settings_window = SettingsWindow(self.config)
        
        # 설정 창의 X 단추를 클릭할 때 완전히 종료하지 않고 트레이로 숨기도록 훅(Hook) 처리
        self.settings_window.closeEvent = self.on_settings_close
        
        # 초기 활성화 상태에 따라 오버레이 표시
        if self.config.enabled:
            self.overlay.show()
            
        self.settings_window.show()
        
        # 시스템 트레이 아이콘 설정
        self.setup_tray()
        
        # 실행 알림 메시지 띄우기
        self.show_welcome_message()

    def on_settings_close(self, event):
        event.ignore()  # 닫기 이벤트 취소
        self.settings_window.hide()  # 설정 창만 숨김
        self.tray_icon.showMessage(
            "멀미 방지 프로그램",
            "설정 창이 트레이로 최소화되었습니다. 오버레이는 백그라운드에서 계속 작동합니다.",
            QSystemTrayIcon.Information,
            2000
        )

    def setup_tray(self):
        # 임시 생성한 동적 아이콘을 트레이 아이콘으로 등록
        self.tray_icon = QSystemTrayIcon(self.create_tray_icon(), self.app)
        self.tray_icon.setToolTip("멀미 방지 오버레이")
        
        # 우클릭 메뉴 구성
        menu = QMenu()
        
        action_show = QAction("설정 창 열기", self.app)
        action_show.triggered.connect(self.show_settings_window)
        
        self.action_toggle = QAction("오버레이 활성화", self.app, checkable=True)
        self.action_toggle.setChecked(self.config.enabled)
        self.action_toggle.triggered.connect(self.toggle_overlay)
        
        # 설정 변경이 일어날 때 트레이 메뉴 상태도 함께 동기화
        self.config.changed.connect(self.sync_tray_menu)
        
        action_exit = QAction("종료 (Exit)", self.app)
        action_exit.triggered.connect(self.exit_app)
        
        menu.addAction(action_show)
        menu.addAction(self.action_toggle)
        menu.addSeparator()
        menu.addAction(action_exit)
        
        self.tray_icon.setContextMenu(menu)
        
        # 트레이 아이콘 더블클릭 이벤트 바인딩
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        self.tray_icon.show()

    def create_tray_icon(self):
        # 파일이 없을 시를 고려해 QPixmap으로 직접 노란색 둥근 사각형 아이콘 그리기
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor("#e6c300"))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, 16, 16, 4, 4)
        painter.end()
        
        return QIcon(pixmap)

    def show_settings_window(self):
        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

    def toggle_overlay(self, checked):
        self.config.enabled = checked

    def sync_tray_menu(self):
        self.action_toggle.setChecked(self.config.enabled)

    def on_tray_activated(self, reason):
        # 트레이 아이콘을 더블클릭하면 설정 창을 노출
        if reason == QSystemTrayIcon.DoubleClick:
            self.show_settings_window()

    def show_welcome_message(self):
        self.tray_icon.showMessage(
            "멀미 방지 프로그램",
            "시스템 백그라운드에서 오버레이가 작동 중입니다.",
            QSystemTrayIcon.Information,
            3000
        )

    def exit_app(self):
        self.tray_icon.hide()
        self.app.quit()
        sys.exit(0)

    def run(self):
        return self.app.exec()

if __name__ == "__main__":
    app = MainApp()
    sys.exit(app.run())
