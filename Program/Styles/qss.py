QSS =  {"BINANCE" : """
/* === Global === */
QWidget {
    background-color: #0d0f1a;
    color: #EAECEF;
    font-family: "Segoe UI", "Ubuntu", "Arial";
    font-size: 13px;
}

/* === Buttons === */
QPushButton {
    background-color: #1f2640;
    border: 1px solid #1f2640;
    border-radius: 4px;
    padding: 6px 10px;
    color: #EAECEF;
}
QPushButton:hover {
    background-color: #2b335a;
    border: 1px solid #4a90e2;
}
QPushButton:pressed {
    background-color: #14182b;
}
QPushButton:disabled {
    background-color: #202630;
    color: #777;
    border: 1px solid #202630;
}

/* Special Buttons */
QPushButton#buyButton {
    background-color: #4a90e2;
    border: 1px solid #4a90e2;
    color: #fff;
}
QPushButton#buyButton:hover {
    background-color: #3b78c2;
}
QPushButton#sellButton {
    background-color: #6c63ff;
    border: 1px solid #6c63ff;
    color: #fff;
}
QPushButton#sellButton:hover {
    background-color: #5348cc;
}

/* === LineEdits === */
QLineEdit {
    background-color: #1f2640;
    border: 1px solid #1f2640;
    border-radius: 4px;
    padding: 4px;
    color: #EAECEF;
    selection-background-color: #4a90e2;
    selection-color: #000;
}
QLineEdit:focus {
    border: 1px solid #6c63ff;
}

/* === Labels === */
QLabel {
    color: #EAECEF;
}

/* === ComboBox === */
QComboBox {
    background-color: #1f2640;
    border: 1px solid #1f2640;
    border-radius: 4px;
    color: #EAECEF;
}
QComboBox:hover {
    border: 1px solid #4a90e2;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #1f2640;
    border: 1px solid #2b335a;
    selection-background-color: #4a90e2;
    selection-color: #000;
}

/* === Tabs === */
QTabWidget::pane {
    border: 1px solid #1f2640;
}
QTabBar::tab {
    background-color: #14182b;
    padding: 6px 12px;
    margin: 1px;
    color: #AAB0C6;
}
QTabBar::tab:selected {
    background-color: #1f2640;
    color: #6c63ff;
}

/* === ScrollBars === */
QScrollBar:vertical {
    border: none;
    background: #14182b;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #1f2640;
    border-radius: 4px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #4a90e2;
}
QScrollBar:horizontal {
    border: none;
    background: #14182b;
    height: 10px;
}
QScrollBar::handle:horizontal {
    background: #1f2640;
    border-radius: 4px;
    min-width: 20px;
}
QScrollBar::handle:horizontal:hover {
    background: #6c63ff;
}

/* === Table === */
QTableWidget {
    gridline-color: #1f2640;
    background-color: #0d0f1a;
    alternate-background-color: #14182b;
    selection-background-color: #2b335a;
    selection-color: #4a90e2;
}
QHeaderView::section {
    background-color: #14182b;
    color: #AAB0C6;
    padding: 4px;
    border: 1px solid #1f2640;
}

/* === Lists === */
QListWidget {
    background-color: #0d0f1a;
    border: 1px solid #1f2640;
    outline: 0;
    padding: 2px;
    color: #EAECEF;
}
QListWidget::item {
    padding: 6px 10px;
    min-height: 26px;
}
QListWidget::item:hover {
    background: #1f2640;
}
QListWidget::item:selected {
    background: #1f2640;
    color: #6c63ff;
    border-left: 2px solid #4a90e2;
}
QComboBox::down-arrow {
    image: url(/home/broo-dev/.valtrida/ASSETS/icons/svg/arrow-down.svg);
    width: 30px;
    height: 30px;
    margin-right: 6px;
}
"""
,

"MAIN_W_TOOL_BAR" : """
QWidget {
    background: #7a7a7a;
    border-top: none;
    border-radius: 12px;
}
QPushButton {
    background: transparent;
    border-radius: 12px;
    padding: 5px 10px;
    font-size: 12px;
    color: #EAECEF;
}
QPushButton:hover {
    background: #2B3139;
    color: #FCD535;
}
QPushButton:pressed {
    background: #3C3F44;
    color: #F0B90B;
}
QToolTip {
        background-color: #181A20;  
        color: #FCD535;             
        border: 1px solid #222;     
        border-radius: 5px;        
        padding: 2px 10px;               
        font-size: 12px;
    }

QPushButton:checked {
    background: #FCD535;
    color: #181A20;    
    font-weight: bold;
    border: 1px solid #F0B90B;
}
""",

"POPUP_W" : """
/* === Popup Window === */
QWidget#popupWindow {
    background-color: #2C2C2C;     /* خلفية أغمق شوي عشان تبرز فوق باقي النوافذ */
    border: 1px solid #444;        /* حدود خفيفة رمادية */
    border-radius: 8px;            /* زوايا دائرية */
    color: #F0F0F0;                /* النصوص بالرمادي الفاتح */
    font-family: "Segoe UI", "Ubuntu", "Arial";
    font-size: 13px;
}

/* === Popup Buttons === */
QWidget#popupWindow QPushButton {
    background-color: #2B3139;
    border: 1px solid #2B3139;
    border-radius: 4px;
    padding: 6px 10px;
    color: #EAECEF;
}
QWidget#popupWindow QPushButton:hover {
    background-color: #333A45;
    border: 1px solid #F0B90B;
}
QWidget#popupWindow QPushButton:pressed {
    background-color: #1E2329;
}
QWidget#popupWindow QPushButton:disabled {
    background-color: #202630;
    color: #777;
    border: 1px solid #202630;
}

/* Special Buttons inside Popup */
QWidget#popupWindow QPushButton#buyButton {
    background-color: #0ECB81;
    border: 1px solid #0ECB81;
    color: #fff;
}
QWidget#popupWindow QPushButton#buyButton:hover {
    background-color: #12A86D;
}
QWidget#popupWindow QPushButton#sellButton {
    background-color: #F6465D;
    border: 1px solid #F6465D;
    color: #fff;
}
QWidget#popupWindow QPushButton#sellButton:hover {
    background-color: #C23544;
}

/* === Popup LineEdits === */
QWidget#popupWindow QLineEdit {
    background-color: #2B3139;
    border: 1px solid #2B3139;
    border-radius: 4px;
    padding: 4px;
    color: #EAECEF;
    selection-background-color: #F0B90B;
    selection-color: #000;
}
QWidget#popupWindow QLineEdit:focus {
    border: 1px solid #F0B90B;
}

/* === Popup Labels === */
QWidget#popupWindow QLabel {
    color: #EAECEF;
}

/* === Popup ComboBox === */
QWidget#popupWindow QComboBox {
    background-color: #2B3139;
    border: 1px solid #2B3139;
    border-radius: 4px;
    color: #EAECEF;
}
QWidget#popupWindow QComboBox:hover {
    border: 1px solid #F0B90B;
}
QWidget#popupWindow QComboBox::drop-down {
    border: none;
    width: 20px;
}
QWidget#popupWindow QComboBox::down-arrow {
    image: url(./Styles/icons/arrow-down.svg);
    width: 30px;
    height: 30px;
    margin-right: 6px;
}
QWidget#popupWindow QComboBox QAbstractItemView {
    background-color: #2B3139;
    border: 1px solid #333A45;
    selection-background-color: #F0B90B;
    selection-color: #000;
}

/* === Popup ScrollBars === */
QWidget#popupWindow QScrollBar:vertical {
    border: none;
    background: #1E2329;
    width: 10px;
}
QWidget#popupWindow QScrollBar::handle:vertical {
    background: #2B3139;
    border-radius: 4px;
    min-height: 20px;
}
QWidget#popupWindow QScrollBar::handle:vertical:hover {
    background: #F0B90B;
}
QWidget#popupWindow QScrollBar:horizontal {
    border: none;
    background: #1E2329;
    height: 10px;
}
QWidget#popupWindow QScrollBar::handle:horizontal {
    background: #2B3139;
    border-radius: 4px;
    min-width: 20px;
}
QWidget#popupWindow QScrollBar::handle:horizontal:hover {
    background: #F0B90B;
}
""",

"AUTH_TOOL_BAR":"""
/* === AUTH TOOL BAR === */

QWidget#options_bar {
    background-color: #14182b;
    border-bottom: 1px solid #1f2640;
    border-radius:8px;
}

/* === Toolbar Buttons === */

QWidget#options_bar QPushButton {
    background: transparent;
    border: none;
    border-radius: 4px;
    

    color: #AAB0C6;
    font-size: 13px;
    font-weight: 500;
}

/* Hover */
QWidget#options_bar QPushButton:hover {
    background-color: #1f2640;
    color: #EAECEF;
}

/* Pressed */
QWidget#options_bar QPushButton:pressed {
    background-color: #0d0f1a;
}

/* Active Page */
QWidget#options_bar QPushButton:checked {
    background-color: #1f2640;
    color: #6c63ff;

    border-bottom: 2px solid #6c63ff;
}

/* Disabled */
QWidget#options_bar QPushButton:disabled {
    color: #555;
}

/* Optional icon spacing */
QWidget#options_bar QPushButton::icon {
    padding-right: 6px;
}

QToolTip {
        background-color: #181A20;  
        color: #FCD535;             
        border: 1px solid #222;     
        border-radius: 5px;        
        padding: 2px 10px;               
        font-size: 12px;
    }
"""


}