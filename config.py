import json
import os
from PySide6.QtCore import QObject, Signal

class AppConfig(QObject):
    # 설정이 변경될 때 발생하는 시그널
    changed = Signal()

    def __init__(self, filename="config.json"):
        super().__init__()
        self.filename = filename
        
        # 기본값 설정
        self._enabled = True
        self._thickness = 30
        self._length = 250
        self._center_size = 20
        self._opacity = 50  # 0 to 100
        self._center_opacity = 50  # 0 to 100 (중앙 점 개별 투명도)
        self._sync_opacity = True  # 투명도 동시 조절 여부
        self._color = "#e6c300"  # 기본 따뜻한 반투명 노란색
        self._shape = "diamond"  # diamond, circle, square
        self._monitor_index = 0  # 0: 주 모니터, 1..: 보조 모니터
        
        self.load()

    def to_dict(self):
        return {
            "enabled": self._enabled,
            "thickness": self._thickness,
            "length": self._length,
            "center_size": self._center_size,
            "opacity": self._opacity,
            "center_opacity": self._center_opacity,
            "sync_opacity": self._sync_opacity,
            "color": self._color,
            "shape": self._shape,
            "monitor_index": self._monitor_index
        }

    def from_dict(self, data):
        self._enabled = data.get("enabled", True)
        self._thickness = data.get("thickness", 30)
        self._length = data.get("length", 250)
        self._center_size = data.get("center_size", 20)
        self._opacity = data.get("opacity", 50)
        self._center_opacity = data.get("center_opacity", 50)
        self._sync_opacity = data.get("sync_opacity", True)
        self._color = data.get("color", "#e6c300")
        self._shape = data.get("shape", "diamond")
        self._monitor_index = data.get("monitor_index", 0)

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.from_dict(data)
            except Exception as e:
                print(f"Error loading config: {e}")

    def save(self):
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    # Properties
    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if self._enabled != value:
            self._enabled = bool(value)
            self.changed.emit()

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if self._thickness != value:
            self._thickness = int(value)
            self.changed.emit()

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        if self._length != value:
            self._length = int(value)
            self.changed.emit()

    @property
    def center_size(self):
        return self._center_size

    @center_size.setter
    def center_size(self, value):
        if self._center_size != value:
            self._center_size = int(value)
            self.changed.emit()

    @property
    def opacity(self):
        return self._opacity

    @opacity.setter
    def opacity(self, value):
        if self._opacity != value:
            self._opacity = int(value)
            self.changed.emit()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if self._color != value:
            self._color = str(value)
            self.changed.emit()

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        if self._shape != value:
            self._shape = str(value)
            self.changed.emit()

    @property
    def monitor_index(self):
        return self._monitor_index

    @monitor_index.setter
    def monitor_index(self, value):
        if self._monitor_index != value:
            self._monitor_index = int(value)
            self.changed.emit()

    @property
    def center_opacity(self):
        return self._center_opacity

    @center_opacity.setter
    def center_opacity(self, value):
        if self._center_opacity != value:
            self._center_opacity = int(value)
            self.changed.emit()

    @property
    def sync_opacity(self):
        return self._sync_opacity

    @sync_opacity.setter
    def sync_opacity(self, value):
        if self._sync_opacity != value:
            self._sync_opacity = bool(value)
            self.changed.emit()
