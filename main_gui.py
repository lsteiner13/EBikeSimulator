import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog, QVBoxLayout
from PySide6.QtGui import QPixmap
from gui.MainWindow import Ui_MainWindow
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView

import logging
import sys
from src.data_io.route_loader import load_route_file
from pathlib import Path
from src.models.bike import EBike, EBikeConfig
from src.models.motor import Motor
from src.models.battery import LiPo, NMC
from src.physics.route_analyzer import RouteAnalyzer
from src.simulator.simulator import Simulator
from tools.plot_gps_data import FoliumMap
from tools.plotter import Plotter
from src.data_io.report_generator import ReportGenerator


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.motor = None
        self.battery = None
        self.ebike = None
        self.ebike_config = None
        self.route = None
        self.simulator = None
        self.route_name = None

        self.pushButton_loadSettings.clicked.connect(self.loadsettings)
        self.pushButton_loadFile.clicked.connect(self.loadfile)
        self.pushButton_startSimulation.clicked.connect(self.startsimulation)
        

    # 3. Definiere die Aktion, die ausgeführt werden soll
    def loadsettings(self):
        # Hier kannst du jeden beliebigen Python-Code ausführen
        #self.statusbar.showMessage("Daten erfolgreich geladen", 3000) # Zeigt Text in der Statusbar für 3 Sek.
        self.motor = Motor(self.doubleSpinBox_efficiency.value(), self.doubleSpinBox_torque_constant.value())
        #check which battery to use
        match self.comboBox_batterytype.currentText():
            case "LiPo":
                self.battery = LiPo(self.doubleSpinBox_cell_capacity.value(), self.spinBox_cell_para.value(), initial_soc=self.doubleSpinBox_initial_soc.value())
            case "NMC":
                self.battery = NMC(self.doubleSpinBox_cell_capacity.value(), self.spinBox_cell_para.value(), initial_soc=self.doubleSpinBox_initial_soc.value())
            case _:
                #unkown type, use lipo
                self.battery = LiPo(self.doubleSpinBox_cell_capacity.value(), self.spinBox_cell_para.value(), initial_soc=self.doubleSpinBox_initial_soc.value())
        
        self.ebike_config = EBikeConfig(mass=self.doubleSpinBox_bikeweight.value(), wheel_diameter=self.spinBox_wheel_diameter.value(), c_w_a=self.doubleSpinBox_cwA.value(), rolling_resistance=self.doubleSpinBox_rolling_resistance.value())
        self.ebike = EBike(self.motor, self.battery, self.ebike_config)
        self.statusbar.showMessage("Konfiguration erfolgreich geladen", 3000)

    def loadfile(self):
        # getOpenFileName() öffnet den Dialog und gibt ein Tuple zurück: (Dateipfad, Filter)
        # Mit '_' ignorieren wir den Filter, da wir nur den Pfad brauchen.
        file_path, _ = QFileDialog.getOpenFileName(
            self,                     # Das Eltern-Fenster
            "Datei auswählen",        # Titel des Fensters
            str(Path(__file__).resolve().parents[0] / "data"),                       # Start-Verzeichnis (leer bedeutet aktueller Ordner)
            "GPS-Dateien (*.csv *.gpx)" # Filter für Dateitypen
        )
        
        # Prüfen, ob der Nutzer überhaupt eine Datei ausgewählt oder abgebrochen hat
        if file_path:
            self.statusbar.showMessage(f"Geladen: {file_path}", 4000)
            
            # Hier kannst du die Datei nun verarbeiten, z.B. einlesen:
            self.lineEdit_loadedFile.setText(file_path)
            self.route = load_route_file(Path(file_path))
            self.route_name = Path(file_path).stem
        else:
            self.statusbar.showMessage("Der Ladevorgang wurde abgebrochen.")

    def startsimulation(self):
        try:
            self.simulator = Simulator(self.route)
            self.statusbar.showMessage("Erfolgreich simuliert.", 3000)
            self.results = self.simulator.run(self.ebike)
        except Exception as e:
            self.statusbar.showMessage("Fehler in Simulation.", 3000)
            import traceback
            traceback.print_exc()

        #erstelle plots
        projekt_ordner = Path(__file__).resolve().parents[0]
        output_ordner = projekt_ordner / "output"
        output_filename = output_ordner / self.route_name
        str_output_filename = str(output_filename)

        
        Plotter.plot_all(self.results, self.route_name)
        FoliumMap.plot_route(self.route, output_file=str_output_filename + "_map.html", open_browser=False)

        #assign elements on gui file paths
        html_pfad = Path(str_output_filename + "_map.html").absolute()
        html_inhalt = html_pfad.read_text(encoding='utf-8')
        self.widget_browser.setHtml(html_inhalt, "")

        pixmap = QPixmap(str_output_filename + "_speed.png")
        self.graphic_plotspeed.setPixmap(pixmap)

        pixmap = QPixmap(str_output_filename + "_power.png")
        self.graphic_plotpower.setPixmap(pixmap)
    
        pixmap = QPixmap(str_output_filename + "_current.png")
        self.graphic_plotcurrent.setPixmap(pixmap)

        pixmap = QPixmap(str_output_filename + "_voltage.png")
        self.graphic_plotvoltage.setPixmap(pixmap)

        pixmap = QPixmap(str_output_filename + "_soc.png")
        self.graphic_plotsoc.setPixmap(pixmap)

        pixmap = QPixmap(str_output_filename + "_batterytemp.png")
        self.graphic_plotbatterytemp.setPixmap(pixmap)

        #raw data lists
        #clear lists
        self.listWidget_batterytemp.clear()
        self.listWidget_current.clear()
        self.listWidget_power.clear()
        self.listWidget_soc.clear()
        self.listWidget_speed.clear()
        self.listWidget_time.clear()
        self.listWidget_voltage.clear()

        #add data
        for temp, current, power, soc, speed, time, voltage  in zip(self.results.battery_temp, self.results.current, self.results.power, self.results.soc, self.results.speed, self.results.time, self.results.voltage):
            self.listWidget_batterytemp.addItem(str(temp))
            self.listWidget_current.addItem(str(current))
            self.listWidget_power.addItem(str(power))
            self.listWidget_soc.addItem(str(soc))
            self.listWidget_speed.addItem(str(speed))
            self.listWidget_time.addItem(str(time))
            self.listWidget_voltage.addItem(str(voltage)) 
            
       

        #summary page
        #get summary data of route and bike
        stats = self.simulator.get_summary(self.results)

        #assign data
        #keywords
        # total_distance_m
        # total_duration_s
        # average_speed_kmh
        # max_speed_kmh
        # max_acceleration_mps2
        # total_ascent_m
        # total_descent_m
        # max_gradient_percent
        # soc_start
        # soc_ende
        # battery_v_start
        # battery_v_ende
        # battery_temp_start
        # battery_temp_ende
        # highest_power
        # highest_battery_temp
        # start_time
        # end_time
        # Werte formatierten, runden und Einheiten anhängen
        self.text_averagespeed.setText(f"{stats['average_speed_kmh']:.1f} km/h")
        self.text_batteryTempend.setText(f"{stats['battery_temp_ende']:.1f} °C")
        self.text_batteryTempstart.setText(f"{stats['battery_temp_start']:.1f} °C")
        self.text_batteryVend.setText(f"{stats['battery_v_ende']:.1f} V")
        self.text_batteryVstart.setText(f"{stats['battery_v_start']:.1f} V")

        # Dauer in Minuten umrechnen und auf ganze Minuten runden
        self.text_duration.setText(f"{round(stats['total_duration_s'] / 60)} min")

        self.text_elevgain.setText(f"{stats['total_ascent_m']:.0f} m")
        self.text_elevloss.setText(f"{stats['total_descent_m']:.0f} m")
        self.text_end.setText(str(stats["end_time"]))

        self.text_highestBatterytemp.setText(f"{stats['highest_battery_temp']:.1f} °C")
        self.text_highestpower.setText(f"{stats['highest_power']:.0f} W")
        self.text_highestspeed.setText(f"{stats['max_speed_kmh']:.0f} km/h")
        self.text_maxgradient.setText(f"{stats['max_gradient_percent']:.1f} %")

        # Distanz von Metern in Kilometer umrechnen
        self.text_routelength.setText(f"{(stats['total_distance_m'] / 1000):.2f} km")
        self.text_start.setText(str(stats["start_time"]))

        #soc start und ende
        self.text_socstart.setText(f"{(stats['soc_start'] * 100):.0f} %")
        self.text_socend.setText(f"{(stats['soc_ende'] * 100):.0f} %")
        
         # Text-Report generieren und speichern
        report_pfad = str(output_ordner / f"{self.route_name}_report.txt")
        ReportGenerator.generate_txt_report(report_pfad, stats)    

    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()