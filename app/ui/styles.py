"""
Stylesheet CSS cho PyQt6
"""
from app.utils.config import get_theme_colors

def get_stylesheet(theme: str = "light") -> str:
    """Lấy stylesheet theo theme"""
    colors = get_theme_colors(theme)
    if theme == "dark":
        colors = {
            "bg": "#181818",
            "sidebar_bg": "#202020",
            "card_bg": "#242424",
            "input_bg": "#2B2B2B",
            "bg_secondary": "#242424",
            "text": "#F5F5F5",
            "text_secondary": "#B8B8B8",
            "border": "#3A3A3A",
            "primary": "#3EA6FF",
            "primary_hover": "#4BB0FF",
            "success": "#4CAF50",
            "error": "#F44336",
            "warning": "#FF9800",
        }
    else:
        colors = {
            **colors,
            "sidebar_bg": colors["bg_secondary"],
            "card_bg": colors["bg_secondary"],
            "input_bg": colors["bg_secondary"],
        }
    
    stylesheet = f"""
    * {{
        font-family: "Segoe UI", Arial, sans-serif;
        font-size: 10pt;
    }}
    
    QMainWindow {{
        background-color: {colors['bg']};
    }}

    #centralWidget,
    #mainContent,
    #scrollArea,
    #scrollViewport,
    #scrollContent {{
        background-color: {colors['bg_secondary']};
    }}
    
    /* Sidebar */
    #sidebar {{
        background-color: {colors['sidebar_bg']};
        border-right: 1px solid {colors['border']};
    }}
    
    #sidebarTitle {{
        font-size: 30px;
        font-weight: 700;
        color: {colors['primary']};
        letter-spacing: 0.5px;
        margin-bottom: 2px;
        padding-left: 6px;
    }}

    #sidebarSubtitle {{
        font-size: 15px;
        font-weight: 500;
        color: {colors['text_secondary']};
        letter-spacing: 0.3px;
        margin-bottom: 18px;
        padding-left: 6px;
    }}
    
    /* Navigation buttons */
    QPushButton[nav="true"] {{
        background-color: transparent;
        border: 1px solid transparent;
        padding: 10px 14px;
        text-align: left;
        color: {colors['text']};
        border-radius: 8px;
    }}
    
    QPushButton[nav="true"]:hover {{
        background-color: {colors['border']};
    }}
    
    QPushButton[nav="true"]:pressed,
    QPushButton[nav="true"][active="true"] {{
        background-color: {colors['primary']};
        color: white;
        border: 1px solid {colors['primary']};
    }}
    
    #primaryButton {{
        background-color: {colors['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        min-height: 28px;
    }}

    #primaryButton:hover {{
        background-color: {colors['primary_hover']};
    }}

    #successButton {{
        background-color: {colors['success']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        min-height: 28px;
    }}

    #successButton:hover {{
        background-color: #45a049;
    }}

    #outlineButton {{
        background-color: {colors['bg']};
        color: {colors['primary']};
        border: 1px solid {colors['primary']};
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        min-height: 28px;
    }}

    #outlineButton:hover {{
        background-color: {colors['primary']};
        color: white;
    }}

    #dangerButton {{
        background-color: {colors['error']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
        min-height: 28px;
    }}

    #dangerButton:hover {{
        background-color: #da190b;
    }}

    #toggleButton {{
        background-color: {colors['bg']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 10px 18px;
        font-weight: 600;
    }}

    #toggleButton:checked {{
        background-color: {colors['primary']};
        color: white;
        border: 1px solid {colors['primary']};
    }}

    #historyTable {{
        background-color: {"#ffffff" if theme == "light" else "#1f1f1f"};
        color: {"#000000" if theme == "light" else "#ffffff"};
        gridline-color: {"#dddddd" if theme == "light" else "#444444"};
        border: 1px solid {"#dddddd" if theme == "light" else "#444444"};
        selection-background-color: {"#dbeafe" if theme == "light" else "#2196f3"};
        selection-color: {"#000000" if theme == "light" else "#ffffff"};
    }}

    #historyTable::item {{
        background-color: {"#ffffff" if theme == "light" else "#1f1f1f"};
        color: {"#000000" if theme == "light" else "#ffffff"};
    }}

    #historyTable::item:selected {{
        background-color: {"#dbeafe" if theme == "light" else "#2196f3"};
        color: {"#000000" if theme == "light" else "#ffffff"};
    }}

    #historyTable QHeaderView::section:vertical {{
        background-color: {"#ffffff" if theme == "light" else "#121212"};
        color: {"#000000" if theme == "light" else "#ffffff"};
        border: 1px solid {"#dddddd" if theme == "light" else "#444444"};
        padding: 4px;
    }}

    #historyTable QHeaderView::section:horizontal {{
        background-color: {"#ffffff" if theme == "light" else "#121212"};
        color: {"#000000" if theme == "light" else "#ffffff"};
        border: 1px solid {"#dddddd" if theme == "light" else "#444444"};
        padding: 6px;
    }}

    #historyTable QTableCornerButton::section {{
        background-color: {"#ffffff" if theme == "light" else "#121212"};
        border: 1px solid {"#dddddd" if theme == "light" else "#444444"};
    }}
    
    /* Line Edit */
    QLineEdit {{
        background-color: {colors['input_bg']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 10px 12px;
        selection-background-color: {colors['primary']};
    }}
    
    QLineEdit:focus {{
        border: 2px solid {colors['primary']};
    }}
    
    QLineEdit:disabled {{
        background-color: {colors['border']};
        color: {colors['text_secondary']};
    }}
    
    /* Text Edit */
    QTextEdit {{
        background-color: {colors['input_bg']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 8px 10px;
        selection-background-color: {colors['primary']};
    }}
    
    QTextEdit:focus {{
        border: 2px solid {colors['primary']};
    }}
    
    /* Combo Box */
    QComboBox {{
        background-color: {colors['input_bg']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
        border-radius: 8px;
        padding: 8px 12px;
        selection-background-color: {colors['primary']};
    }}
    
    QComboBox:hover {{
        border: 1px solid {colors['primary']};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox::down-arrow {{
        image: none;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {colors['input_bg']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
        selection-background-color: {colors['primary']};
        outline: none;
    }}
    
    /* Labels */
    QLabel {{
        color: {colors['text']};
        background: transparent;
    }}
    
    QLabel[type="title"] {{
        font-size: 12pt;
        font-weight: bold;
    }}

    QLabel[type="subtitle"] {{
        font-size: 10.5pt;
        font-weight: 600;
    }}
    
    QLabel[type="secondary"] {{
        color: {colors['text_secondary']};
    }}
    
    /* Progress Bar */
    QProgressBar {{
        background-color: {colors['input_bg']};
        border: 1px solid {colors['border']};
        border-radius: 6px;
        text-align: center;
        color: {colors['text']};
        height: 18px;
    }}
    
    QProgressBar::chunk {{
        background-color: {colors['primary']};
        border-radius: 6px;
    }}
    
    /* Scroll Bar */
    QScrollBar:vertical {{
        background-color: {colors['input_bg']};
        width: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {colors['border']};
        border-radius: 5px;
        min-height: 20px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {colors['text_secondary']};
    }}
    
    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
    }}
    
    QScrollBar:horizontal {{
        background-color: {colors['input_bg']};
        height: 10px;
        margin: 0px 0px 0px 0px;
        border-radius: 5px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {colors['border']};
        border-radius: 5px;
        min-width: 20px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {colors['text_secondary']};
    }}
    
    QScrollBar::add-line:horizontal,
    QScrollBar::sub-line:horizontal {{
        border: none;
        background: none;
    }}
    
    /* Frame */
    QFrame {{
        border: none;
    }}

    #card {{
        background-color: {colors['bg']};
        border: 1px solid {colors['border']};
        border-radius: 12px;
        padding: 14px;
    }}

    #thumbnail {{
        background-color: {colors['bg']};
        border: 1px solid {colors['border']};
        border-radius: 10px;
    }}

    #video_title {{
        font-size: 13pt;
        font-weight: 700;
    }}

    
    /* Table Widget */
    QTableWidget {{
        background-color: {colors['card_bg']};
        gridline-color: {colors['border']};
        border: 1px solid {colors['border']};
        border-radius: 5px;
    }}
    
    QTableWidget::item {{
        padding: 5px;
    }}
    
    QTableWidget::item:selected {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    QHeaderView::section {{
        background-color: {colors['bg']};
        color: {colors['text']};
        padding: 8px;
        border: none;
        border-right: 1px solid {colors['border']};
        border-bottom: 1px solid {colors['border']};
    }}
    
    /* List Widget */
    QListWidget {{
        background-color: {colors['card_bg']};
        border: 1px solid {colors['border']};
        border-radius: 5px;
    }}
    
    QListWidget::item {{
        padding: 5px;
    }}
    
    QListWidget::item:selected {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    QListWidget::item:hover {{
        background-color: {colors['border']};
    }}
    
    /* Dialogs */
    QDialog {{
        background-color: {colors['bg']};
    }}
    
    QMessageBox {{
        background-color: {colors['bg']};
    }}
    
    QMessageBox QLabel {{
        color: {colors['text']};
    }}
    
    /* Menu Bar */
    QMenuBar {{
        background-color: {colors['card_bg']};
        color: {colors['text']};
        border-bottom: 1px solid {colors['border']};
    }}
    
    QMenuBar::item:selected {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    QMenu {{
        background-color: {colors['card_bg']};
        color: {colors['text']};
        border: 1px solid {colors['border']};
    }}
    
    QMenu::item:selected {{
        background-color: {colors['primary']};
        color: white;
    }}
    
    QMenu::separator {{
        background-color: {colors['border']};
        height: 1px;
    }}
    """
    
    return stylesheet
