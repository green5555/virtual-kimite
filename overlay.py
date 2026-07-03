import ctypes
from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import QPainter, QColor, QPolygonF, QBrush, QPen
from PySide6.QtWidgets import QWidget, QApplication

# Windows API 설정을 위한 ctypes 정의
user32 = ctypes.windll.user32
GWL_EXSTYLE = -20
WS_EX_TRANSPARENT = 0x00000020
WS_EX_LAYERED = 0x00080000

class OverlayWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        # 윈도우 플래그 설정: 테두리 없음, 항상 위, 작업표시줄 제외, 포커스 무시
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowDoesNotAcceptFocus
        )
        # 배경 투명화
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        
        # 설정 변경 시 오버레이 화면 자동 갱신 및 위치 재조정
        self.config.changed.connect(self.on_config_changed)
        
        # 위치 및 크기 설정 초기화
        self.update_geometry()

    def showEvent(self, event):
        super().showEvent(event)
        # 윈도우가 화면에 보일 때 마우스 클릭 관통(Click-through) 속성 부여
        hwnd = self.winId()
        self.apply_click_through(hwnd)

    def apply_click_through(self, hwnd):
        try:
            # PySide6 winId()는 HWND 포인터 역할을 하므로 정수로 변환하여 API에 넘김
            hwnd_val = int(hwnd)
            style = user32.GetWindowLongW(hwnd_val, GWL_EXSTYLE)
            
            # WS_EX_TRANSPARENT(클릭 관통)만 적용하고 WS_EX_LAYERED는 강제 지정하지 않음.
            # Qt의 TranslucentBackground 속성이 설정되면 이미 WS_EX_LAYERED가 내부적으로 설정되므로,
            # 수동으로 다시 덮어쓰면 렌더링 버그가 발생하여 오버레이가 아예 보이지 않게 될 수 있습니다.
            style |= WS_EX_TRANSPARENT
            user32.SetWindowLongW(hwnd_val, GWL_EXSTYLE, style)
            
            # 스타일 변경 사항을 OS에 즉시 적용하도록 SetWindowPos 호출
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            SWP_NOZORDER = 0x0004
            SWP_FRAMECHANGED = 0x0020
            user32.SetWindowPos(hwnd_val, 0, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED)
        except Exception as e:
            print(f"Error applying click-through style: {e}")

    def update_geometry(self):
        screens = QApplication.screens()
        idx = self.config.monitor_index
        
        if idx < len(screens):
            screen = screens[idx]
        else:
            screen = QApplication.primaryScreen()
            
        if screen:
            geom = screen.geometry()
            self.setGeometry(geom)
            
    def on_config_changed(self):
        # 켜짐/꺼짐 상태 확인
        if self.config.enabled:
            self.show()
            self.update_geometry()
            self.update()  # paintEvent 트리거
        else:
            self.hide()

    def paintEvent(self, event):
        if not self.config.enabled:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 헥스 색상 코드 분석 및 투명도(alpha) 적용
        hex_color = self.config.color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        alpha = int(self.config.opacity * 2.55)  # 0~100 범위를 0~255로 변환
        
        tape_color = QColor(r, g, b, alpha)
        brush = QBrush(tape_color)
        painter.setPen(Qt.NoPen)  # 외곽선 없음
        painter.setBrush(brush)   # 브러시 설정 추가 (색상 채우기)

        w = self.width()
        h = self.height()
        cx = w / 2
        cy = h / 2
        
        thickness = self.config.thickness
        length = self.config.length
        center_size = self.config.center_size

        # 1. 상단 테이프 (Top)
        painter.drawRect(QRectF(cx - thickness / 2, 0, thickness, length))

        # 2. 하단 테이프 (Bottom)
        painter.drawRect(QRectF(cx - thickness / 2, h - length, thickness, length))

        # 3. 좌측 테이프 (Left)
        painter.drawRect(QRectF(0, cy - thickness / 2, length, thickness))

        # 4. 우측 테이프 (Right)
        painter.drawRect(QRectF(w - length, cy - thickness / 2, length, thickness))

        # 5. 중앙 테이프 / 마크 (Center)
        # 투명도 동시 조절 여부에 따른 중앙 점 투명도(Alpha) 재설정
        c_opacity = self.config.opacity if self.config.sync_opacity else self.config.center_opacity
        c_alpha = int(c_opacity * 2.55)
        c_color = QColor(r, g, b, c_alpha)
        painter.setBrush(QBrush(c_color))

        shape = self.config.shape
        if shape == "diamond":
            # 마름모 모양 다각형 그리기
            points = [
                QPointF(cx, cy - center_size),
                QPointF(cx + center_size, cy),
                QPointF(cx, cy + center_size),
                QPointF(cx - center_size, cy)
            ]
            polygon = QPolygonF(points)
            painter.drawPolygon(polygon)
            
        elif shape == "circle":
            # 원 그리기
            painter.drawEllipse(QPointF(cx, cy), center_size, center_size)
            
        elif shape == "square":
            # 정사각형 그리기
            painter.drawRect(QRectF(cx - center_size, cy - center_size, center_size * 2, center_size * 2))
            
        painter.end()
