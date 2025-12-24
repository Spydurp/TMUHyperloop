import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QPushButton, QGraphicsDropShadowEffect, QPlainTextEdit, QProgressBar, QScrollArea
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import time




class HyperloopControlGUI(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Hyperloop Pod Control System")
        self.setGeometry(100, 100, 1500, 900)


        # ------------------------- SCROLL AREA WRAPPER ----------------------------
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { background-color: #0b0e19; }")


        container = QWidget()
        scroll_area.setWidget(container)


        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(30)


        self.setCentralWidget(scroll_area)


        # ----------------------------- GLOBAL STYLE ------------------------------
        self.setStyleSheet("""
            QMainWindow { background-color: #0b0e19; }
            QWidget { background-color: transparent; color: white; }
            QLabel { color: white; font-family: 'Eurostile'; }
        """)


        # =========================================================================
        #                           CURRENT STATE BOX
        # =========================================================================
       
        # Bigger glowing box with inner glowing panel and subtitle
        state_frame = QGroupBox("")  # title handled by internal label to place it exactly
        state_frame.setObjectName("state_frame")
        state_frame.setFixedHeight(200)
        state_frame.setStyleSheet("""
            #state_frame {
                background-color: #0d1220;
                border-radius: 25px;
                border: 3px solid rgba(0,255,120,0.30);
                padding-top: 10px;
            }
        """)
        # Outer glow
        outer_glow = QGraphicsDropShadowEffect()
        outer_glow.setBlurRadius(120)
        outer_glow.setColor(QColor(0, 255, 120))
        outer_glow.setOffset(0, 0)
        state_frame.setGraphicsEffect(outer_glow)


        main_layout.addWidget(state_frame)
        state_layout = QVBoxLayout(state_frame)
        state_layout.setAlignment(Qt.AlignCenter)


        # Title inside (so it appears inside the frame like your image)
        self.state_title = QLabel("CURRENT STATE")
        self.state_title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            font-family: 'Times New Roman';
            color: #28ff9c;
            letter-spacing: 3px;
        """)
        state_layout.addWidget(self.state_title, alignment=Qt.AlignTop | Qt.AlignHCenter)


        # inner glowing panel
        inner = QWidget()
        inner.setStyleSheet("""
            background-color: #0d1220;
            border-radius: 20px;
            border: 2px solid rgba(0,255,120,0.35);
        """)
        inner.setFixedHeight(90)
        inner_glow = QGraphicsDropShadowEffect()
        inner_glow.setBlurRadius(80)
        inner_glow.setColor(QColor(0, 255, 120))
        inner_glow.setOffset(0, 0)
        inner.setGraphicsEffect(inner_glow)


        inner_layout = QVBoxLayout(inner)
        inner_layout.setAlignment(Qt.AlignCenter)


        self.status_label = QLabel("SAFE")
        self.status_label.setStyleSheet("""
            font-size: 55px;
            font-family: 'Times New Roman';
            font-weight: bold;
            color: #28ff7a;
        """)
        inner_layout.addWidget(self.status_label, alignment=Qt.AlignCenter)


        self.status_subtitle = QLabel("System Status: Operational")
        self.status_subtitle.setStyleSheet("""
            font-size: 20px;
            font-family: 'Times New Roman';
        """)
        # Add inner and subtitle to outer state frame
        state_layout.addWidget(inner)
        state_layout.addWidget(self.status_subtitle, alignment=Qt.AlignHCenter)


        # =========================================================================
        #                             3 COLUMN LAYOUT
        # =========================================================================
        content_layout = QHBoxLayout()
        content_layout.setSpacing(30)
        main_layout.addLayout(content_layout)


        col1, col2, col3 = QVBoxLayout(), QVBoxLayout(), QVBoxLayout()


        # =========================================================================
        #                             LIM SYSTEM BOX
        # =========================================================================
        lim_box = QGroupBox("LIM SYSTEM")
        lim_box.setObjectName("lim_box")
        lim_box.setStyleSheet("""
            QGroupBox#lim_box {
                background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #0c1726, stop:1 #0f1b2e);
                border-radius: 18px;
                border: 2px solid rgba(0,255,120,0.12);
                font-size: 18px;
                font-family: 'Times New Roman';
                font-weight: bold;
                color: #26ff7a;
                padding-top: 25px;
            }
            QGroupBox::title {
                /*left: 12px;
                top: -8px;
                font-size: 20px;
                color: #7fbcff; */
                             
                subcontrol-origin: margin;
                subcontrol-position: top left;


                padding: 25px 15px;
                margin-top: 0px;       /* keep title inside */
                margin-left: 8px;


                color: rgb(180,200,255);
                font-size: 14pt;
                background-color: transparent;  /* keeps glowframe background clean */
            }
        """)
        lim_layout = QVBoxLayout(lim_box)
        lim_layout.setSpacing(18)
        lim_layout.setContentsMargins(18, 35, 18, 25)


        # small card style for each parameter row
        row_card_style = """
            background-color: rgba(10,16,26,1);
            border-radius: 12px;
            padding: 14px;
        """
        label_style = "font-size: 14px; color: #bcdfff;"


        def make_lim_row(name, value_text, bar_color_hex, bar_val=65):
            # whole card widget
            card = QWidget()
            card.setStyleSheet(row_card_style)
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(10, 6, 10, 6)
            card_layout.setSpacing(10)


            # top line (label + value)
            top = QWidget()
            top_layout = QHBoxLayout(top)
            top_layout.setContentsMargins(0, 0, 0, 0)
            top_layout.setSpacing(6)
            lbl = QLabel(name)
            lbl.setStyleSheet(label_style)
            val = QLabel(value_text)
            val.setStyleSheet("font-weight:bold; color:#9bd3ff; font-size:14px;")
            top_layout.addWidget(lbl)
            top_layout.addStretch()
            top_layout.addWidget(val)


            # progress bar
            bar = QProgressBar()
            bar.setRange(0, 100)
            bar.setValue(bar_val)
            bar.setTextVisible(False)
            bar.setFixedHeight(12)
            bar.setStyleSheet(f"""
                QProgressBar {{
                    border: 0px;
                    background-color: #2a3946;
                    border-radius: 6px;
                }}
                QProgressBar::chunk {{
                    background-color: {bar_color_hex};
                    border-radius: 6px;
                }}
            """)


            card_layout.addWidget(top)
            card_layout.addWidget(bar)
            return card


        lim_layout.addWidget(make_lim_row("Voltage", "516 V", "#4a8cff", 58))
        lim_layout.addWidget(make_lim_row("Current", "160 A", "#ffb400", 45))
        lim_layout.addWidget(make_lim_row("Temperature", "61°C", "#ff7b2c", 35))
        lim_layout.addWidget(make_lim_row("Inverter Voltage", "738 V", "#ca6aff", 70))


        col1.addWidget(lim_box)


        # =========================================================================
        #                           BRAKE SYSTEM BOX
        # =========================================================================
        brake_box = QGroupBox("BRAKE SYSTEM")
        brake_box.setObjectName("brake_box")
        brake_box.setStyleSheet("""
            QGroupBox#brake_box {
                background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #0c1726, stop:1 #0f1b2e);
                border-radius: 18px;
                border: 2px solid rgba(255,90,90,0.08);
                font-size: 18px;
                font-family: 'Times New Roman';
                font-weight: bold;
                color: #ff7070;
                padding-top: 25px;
            }
            QGroupBox::title {
                /*left: 12px;
                top: -8px;
                font-size: 20px;
                color: #ff6b6b;*/
                               
                subcontrol-origin: margin;
                subcontrol-position: top left;


                padding: 25px 15px;
                margin-top: 0px;       /* keep title inside */
                margin-left: 8px;


                color: rgb(180,200,255);
                font-size: 14pt;
                background-color: transparent;  /* keeps glowframe background clean */
            }
        """)
        brake_layout = QVBoxLayout(brake_box)
        brake_layout.setSpacing(18)
        brake_layout.setContentsMargins(18, 32, 18, 25)


        # inner dark cards for brake entries (to match screenshot)
        brake_row_style = """
            background-color: rgba(8,12,18,0.9);
            border-radius: 12px;
            padding: 16px;
        """


        def brake_position_row(label_text, deployed=True):
            card = QWidget()
            card.setStyleSheet(brake_row_style)
            l = QHBoxLayout(card)
            l.setContentsMargins(8, 4, 8, 4)
            l.setSpacing(10)


            label = QLabel(label_text)
            label.setStyleSheet("font-size: 15px; color: #dfefff;")
            l.addWidget(label)


            l.addStretch()


            dot = QLabel("●")
            dot_color = "#ff4040" if deployed else "#25ff75"
            dot.setStyleSheet(f"font-size:18px; color: {dot_color}; padding-right:8px;")
            status_text = "DEPLOYED" if deployed else "UNDEPLOYED"
            status_label = QLabel(status_text)
            status_label.setStyleSheet(f"font-size:14px; font-weight:bold; color: {dot_color};")


            l.addWidget(dot)
            l.addWidget(status_label)
            return card


        brake_layout.addWidget(brake_position_row("Brake Position 1", deployed=True))
        brake_layout.addWidget(brake_position_row("Brake Position 2", deployed=False))


        # distance card (centered large number)
        distance_card = QWidget()
        distance_card.setStyleSheet("""
            background-color: rgba(10,18,28,0.9);
            border-radius: 12px;
            padding: 16px;
        """)
        dlay = QVBoxLayout(distance_card)
        dlay.setContentsMargins(12, 12, 12, 12)
        dlay.setSpacing(10)
        title = QLabel("Distance Traveled")
        title.setStyleSheet("font-size:14px; color:#cfd8e6;")
        title.setAlignment(Qt.AlignCenter)
        self.dist_value = QLabel("2847 m")
        self.dist_value.setStyleSheet("font-size:40px; font-weight:bold; color:#30ff7a;")
        self.dist_value.setAlignment(Qt.AlignCenter)
        dlay.addWidget(title)
        dlay.addWidget(self.dist_value)
        brake_layout.addWidget(distance_card)


        col2.addWidget(brake_box)


        # =========================================================================
        #                           MISSION CONTROL BOX (kept minimal)
        # =========================================================================
        mc_box = QGroupBox("MISSION CONTROL")
        mc_box.setObjectName("mc_box")
        mc_box.setStyleSheet("""
            QGroupBox#mc_box {
                background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 #0c1726, stop:1 #0f1b2e);
                border-radius: 18px;
                border: 2px solid rgba(96,165,250,0.12);
                font-family: 'Times New Roman';
                font-weight: bold;
                font-size: 18px;
                color: #9bbdff;
                padding-top: 25px;
            }
            QGroupBox::title {
                /*left: 12px;
                top: -8px;
                font-size: 20px;
                color: #9bbdff;*/
                             
                font-family: 'Times New Roman';
                font-weight: bold;
                subcontrol-origin: margin;
                subcontrol-position: top left;


                padding: 25px 15px;
                margin-top: 0px;       /* keep title inside */
                margin-left: 8px;


                color: rgb(180,200,255);
                font-size: 14pt;
                background-color: transparent;  /* keeps glowframe background clean */
            }
        """)


        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(45)
        glow.setColor(QColor(96,165,250))
        glow.setOffset(0, 0)
        mc_box.setGraphicsEffect(glow)


        mc_layout = QVBoxLayout(mc_box)
        mc_layout.setSpacing(12)
        mc_layout.setContentsMargins(20, 40, 20, 20)


        def make_button(text, color):
            btn = QPushButton(text)
            btn.setFixedHeight(48)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    padding: 6px;
                }}
                QPushButton:hover {{
                    background-color: rgba(255,255,255,0.08);
                }}
            """)
            return btn


        mc_layout.addWidget(make_button("PREP FOR LAUNCH", "#377dff"))
        mc_layout.addWidget(make_button("ABORT LAUNCH", "#e08c17"))
        mc_layout.addWidget(make_button("LAUNCH", "#28b44a"))
        mc_layout.addWidget(make_button("STOP", "#e64800"))
        mc_layout.addWidget(make_button("STOP NOW", "#6b2b2b"))  # muted red to match disabled look
        mc_layout.addWidget(make_button("RESET FAULT", "#6f7d90"))


        col3.addWidget(mc_box)


        # Add the 3 columns to main content layout
        content_layout.addLayout(col1, 1)
        content_layout.addLayout(col2, 1)
        content_layout.addLayout(col3, 1)


       
        # ---------------- COMMAND LOG WINDOW -----------------
        # ------------------- Add terminal-style logs -------------------
        # Group boxes + terminal text areas placed at bottom of the window
        system_group = QGroupBox("SYSTEM LOGS")
        system_group.setStyleSheet("QGroupBox { color: #65ff9c; font-weight: bold; }")
        self.system_logs = QPlainTextEdit()
        self.system_logs.setReadOnly(True)
        self.system_logs.setPlainText("")  # start empty
        self.system_logs.setStyleSheet("""
            QPlainTextEdit {
                background: #0f1216;
                color: #9ef08a;
                border: 1px solid #224;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }
        """)
        sg_layout = QVBoxLayout(system_group)
        sg_layout.addWidget(self.system_logs)




        rover_group = QGroupBox("ROVER LOGS")
        rover_group.setStyleSheet("QGroupBox { color: #ffb86b; font-weight: bold; }")
        self.rover_logs = QPlainTextEdit()
        self.rover_logs.setReadOnly(True)
        self.rover_logs.setStyleSheet("""
            QPlainTextEdit {
                background: #0f1216;
                color: #ffb86b;
                border: 1px solid #224;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11pt;
            }
        """)
        rg_layout = QVBoxLayout(rover_group)
        rg_layout.addWidget(self.rover_logs)




        # place side-by-side under the main content
        logs_layout = QHBoxLayout()
        logs_layout.addWidget(system_group, stretch=3)
        logs_layout.addWidget(rover_group, stretch=3)
        main_layout.addLayout(logs_layout)
        # ------------------- end logs -------------------




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HyperloopControlGUI()
    window.show()
    sys.exit(app.exec())
