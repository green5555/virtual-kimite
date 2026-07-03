from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QComboBox,
    QPushButton, QColorDialog, QCheckBox, QGroupBox, QFormLayout, QApplication
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

# 다크 테마 QSS 스타일시트 정의
STYLE_SHEET = """
QWidget {
    background-color: #18181b;
    color: #f4f4f5;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    font-size: 13px;
}
QGroupBox {
    border: 1px solid #27272a;
    border-radius: 8px;
    margin-top: 16px;
    padding-top: 20px;
    font-weight: bold;
    color: #e6c300;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 6px;
}
QLabel {
    color: #a1a1aa;
}
QSlider::groove:horizontal {
    border: 1px solid #27272a;
    height: 6px;
    background: #27272a;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #e6c300;
    border: 1px solid #b59a00;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}
QSlider::handle:horizontal:hover {
    background: #ffd60a;
}
QPushButton {
    background-color: #e6c300;
    color: #18181b;
    border-radius: 6px;
    padding: 8px 16px;
    font-weight: bold;
    border: none;
}
QPushButton:hover {
    background-color: #ffd60a;
}
QPushButton:pressed {
    background-color: #b59a00;
}
QPushButton#btn_color {
    background-color: #27272a;
    color: #f4f4f5;
    border: 1px solid #3f3f46;
}
QPushButton#btn_color:hover {
    background-color: #3f3f46;
}
QPushButton#btn_reset {
    background-color: #3f3f46;
    color: #f4f4f5;
}
QPushButton#btn_reset:hover {
    background-color: #52525b;
}
QComboBox {
    border: 1px solid #27272a;
    border-radius: 6px;
    padding: 6px;
    background-color: #27272a;
    color: #f4f4f5;
}
QComboBox QAbstractItemView {
    background-color: #27272a;
    color: #f4f4f5;
    selection-background-color: #e6c300;
    selection-color: #18181b;
    border: 1px solid #3f3f46;
}
QCheckBox {
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 1px solid #3f3f46;
    border-radius: 4px;
    background-color: #27272a;
}
QCheckBox::indicator:checked {
    background-color: #e6c300;
    border: 1px solid #e6c300;
}
"""

class SettingsWindow(QWidget):
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.setWindowTitle("멀미 방지 오버레이 설정")
        self.resize(400, 500)
        self.setStyleSheet(STYLE_SHEET)
        
        self.init_ui()
        self.load_values_to_ui()
        self.connect_signals()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. 활성화 토글 그룹
        top_layout = QHBoxLayout()
        self.chk_enable = QCheckBox("멀미 방지 오버레이 활성화")
        self.chk_enable.setStyleSheet("font-size: 14px; font-weight: bold;")
        top_layout.addWidget(self.chk_enable)
        main_layout.addLayout(top_layout)

        # 2. 오버레이 세부 설정 그룹
        group_overlay = QGroupBox("오버레이 디자인 커스텀")
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        # 테이프 두께 슬라이더
        self.slider_thickness = QSlider(Qt.Horizontal)
        self.slider_thickness.setRange(5, 100)
        self.lbl_thickness_val = QLabel("30px")
        h_thick = QHBoxLayout()
        h_thick.addWidget(self.slider_thickness)
        h_thick.addWidget(self.lbl_thickness_val)
        form_layout.addRow("테이프 두께:", h_thick)

        # 테이프 길이 슬라이더
        self.slider_length = QSlider(Qt.Horizontal)
        self.slider_length.setRange(50, 1000)
        self.lbl_length_val = QLabel("250px")
        h_len = QHBoxLayout()
        h_len.addWidget(self.slider_length)
        h_len.addWidget(self.lbl_length_val)
        form_layout.addRow("테이프 길이:", h_len)

        # 중앙 마크 크기 슬라이더
        self.slider_center_size = QSlider(Qt.Horizontal)
        self.slider_center_size.setRange(5, 150)
        self.lbl_center_size_val = QLabel("20px")
        h_cs = QHBoxLayout()
        h_cs.addWidget(self.slider_center_size)
        h_cs.addWidget(self.lbl_center_size_val)
        form_layout.addRow("중앙 점 크기:", h_cs)

        # 투명도 슬라이더
        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(5, 100)
        self.lbl_opacity_val = QLabel("50%")
        h_op = QHBoxLayout()
        h_op.addWidget(self.slider_opacity)
        h_op.addWidget(self.lbl_opacity_val)
        form_layout.addRow("투명도 (Alpha):", h_op)

        # 중앙 모양 콤보박스
        self.combo_shape = QComboBox()
        self.combo_shape.addItem("마름모 (Diamond)", "diamond")
        self.combo_shape.addItem("원형 (Circle)", "circle")
        self.combo_shape.addItem("정사각형 (Square)", "square")
        form_layout.addRow("중앙 점 모양:", self.combo_shape)

        # 색상 선택 버튼 및 미리보기
        self.btn_color = QPushButton("색상 변경")
        self.btn_color.setObjectName("btn_color")
        self.view_color_box = QWidget()
        self.view_color_box.setFixedSize(24, 24)
        self.view_color_box.setStyleSheet("border-radius: 4px; border: 1px solid #3f3f46;")
        
        h_color = QHBoxLayout()
        h_color.addWidget(self.btn_color)
        h_color.addWidget(self.view_color_box)
        h_color.addStretch()
        form_layout.addRow("테이프 색상:", h_color)

        group_overlay.setLayout(form_layout)
        main_layout.addWidget(group_overlay)

        # 3. 시스템 설정 그룹 (모니터 선택 등)
        group_system = QGroupBox("시스템 설정")
        system_layout = QFormLayout()
        system_layout.setSpacing(12)

        self.combo_monitor = QComboBox()
        self.update_monitor_list()
        system_layout.addRow("대상 모니터:", self.combo_monitor)

        group_system.setLayout(system_layout)
        main_layout.addWidget(group_system)

        # 4. 하단 버튼 영역 (저장, 리셋)
        main_layout.addStretch()
        h_buttons = QHBoxLayout()
        
        self.btn_reset = QPushButton("초기화")
        self.btn_reset.setObjectName("btn_reset")
        self.btn_save = QPushButton("설정 저장")
        
        h_buttons.addWidget(self.btn_reset)
        h_buttons.addStretch()
        h_buttons.addWidget(self.btn_save)
        main_layout.addLayout(h_buttons)

        self.setLayout(main_layout)

    def update_monitor_list(self):
        self.combo_monitor.clear()
        screens = QApplication.screens()
        for i, screen in enumerate(screens):
            self.combo_monitor.addItem(f"모니터 {i+1} ({screen.size().width()}x{screen.size().height()})", i)

    def load_values_to_ui(self):
        # Config 객체에서 값을 읽어와 UI를 업데이트
        self.chk_enable.setChecked(self.config.enabled)
        self.slider_thickness.setValue(self.config.thickness)
        self.slider_length.setValue(self.config.length)
        self.slider_center_size.setValue(self.config.center_size)
        self.slider_opacity.setValue(self.config.opacity)
        
        self.lbl_thickness_val.setText(f"{self.config.thickness}px")
        self.lbl_length_val.setText(f"{self.config.length}px")
        self.lbl_center_size_val.setText(f"{self.config.center_size}px")
        self.lbl_opacity_val.setText(f"{self.config.opacity}%")

        # 중앙 모양 매칭
        idx = self.combo_shape.findData(self.config.shape)
        if idx >= 0:
            self.combo_shape.setCurrentIndex(idx)

        # 모니터 인덱스 매칭
        mon_idx = self.config.monitor_index
        if mon_idx < self.combo_monitor.count():
            self.combo_monitor.setCurrentIndex(mon_idx)
        else:
            self.combo_monitor.setCurrentIndex(0)

        # 색상 박스 표시
        self.update_color_box_preview(self.config.color)

    def update_color_box_preview(self, hex_color):
        self.view_color_box.setStyleSheet(
            f"background-color: {hex_color}; border-radius: 4px; border: 1px solid #3f3f46;"
        )

    def connect_signals(self):
        # UI 요소 조작 시 Config 값을 즉시 변경 -> 오버레이 실시간 반응
        self.chk_enable.toggled.connect(self._on_enable_toggled)
        self.slider_thickness.valueChanged.connect(self._on_thickness_changed)
        self.slider_length.valueChanged.connect(self._on_length_changed)
        self.slider_center_size.valueChanged.connect(self._on_center_size_changed)
        self.slider_opacity.valueChanged.connect(self._on_opacity_changed)
        self.combo_shape.currentIndexChanged.connect(self._on_shape_changed)
        self.combo_monitor.currentIndexChanged.connect(self._on_monitor_changed)
        
        self.btn_color.clicked.connect(self._on_color_pick_clicked)
        self.btn_reset.clicked.connect(self._on_reset_clicked)
        self.btn_save.clicked.connect(self._on_save_clicked)

    # --- 시그널 처리 핸들러 ---
    def _on_enable_toggled(self, checked):
        self.config.enabled = checked

    def _on_thickness_changed(self, value):
        self.config.thickness = value
        self.lbl_thickness_val.setText(f"{value}px")

    def _on_length_changed(self, value):
        self.config.length = value
        self.lbl_length_val.setText(f"{value}px")

    def _on_center_size_changed(self, value):
        self.config.center_size = value
        self.lbl_center_size_val.setText(f"{value}px")

    def _on_opacity_changed(self, value):
        self.config.opacity = value
        self.lbl_opacity_val.setText(f"{value}%")

    def _on_shape_changed(self, index):
        shape_data = self.combo_shape.currentData()
        if shape_data:
            self.config.shape = shape_data

    def _on_monitor_changed(self, index):
        mon_idx = self.combo_monitor.currentData()
        if mon_idx is not None:
            self.config.monitor_index = mon_idx

    def _on_color_pick_clicked(self):
        current_qcolor = QColor(self.config.color)
        color = QColorDialog.getColor(current_qcolor, self, "테이프 색상 선택")
        if color.isValid():
            hex_color = color.name()  # #RRGGBB 포맷
            self.config.color = hex_color
            self.update_color_box_preview(hex_color)

    def _on_reset_clicked(self):
        # 기본값으로 리셋
        self.config.enabled = True
        self.config.thickness = 30
        self.config.length = 250
        self.config.center_size = 20
        self.config.opacity = 50
        self.config.color = "#e6c300"
        self.config.shape = "diamond"
        self.config.monitor_index = 0
        
        # UI 동기화
        self.load_values_to_ui()

    def _on_save_clicked(self):
        self.config.save()
        # 시각적 피드백 제공 (저장 완료 표시 등)
        self.btn_save.setText("저장 완료!")
        self.btn_save.setEnabled(False)
        self.btn_save.setStyleSheet("background-color: #10b981; color: #18181b;") # 초록색 계열로 변경
        
        # 1.5초 후 버튼 원래대로 복구
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1500, self._restore_save_button)

    def _restore_save_button(self):
        self.btn_save.setText("설정 저장")
        self.btn_save.setEnabled(True)
        self.btn_save.setStyleSheet("") # 기본 QSS로 롤백
