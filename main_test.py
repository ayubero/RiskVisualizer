import gi
import folium
import tempfile
import requests
import json

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk as Gtk, WebKit2

def getCoordinates(city_name):
    api_key = "52ad0a11d97a6f74c6efb726b51fc89f"
    open_weather_map_url = "https://api.openweathermap.org/data/2.5/weather"
    url = open_weather_map_url + "?q=" + city_name + "&appid=" + api_key
    resp = requests.get(url)
    json_file=resp.text
    data = json.loads(json_file)
    coordinates = data["coord"]
    lat = coordinates["lat"]
    lon = coordinates["lon"]
    return [lat, lon]

class MyWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Risk Visualizer")
        self.set_size_request(900, 700)
        self.set_resizable(False)
        self.set_border_width(15)

        # Parameters
        self.path = tempfile.gettempdir() + "/map.html"
        self.zoom_start = 13
        self.location = 'Zaragoza'
        self.contaminant = 'CO'

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        # Location entry
        entry_location = Gtk.Entry()
        entry_location.set_text("Zaragoza")
        entry_location.set_placeholder_text("Location")
        entry_location.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, "system-search-symbolic") # Icon
        entry_location.connect("changed", self.on_entry_location_changed)
        self.vbox.add(entry_location)

        # Load data button
        button_load_data = Gtk.Button(label="Get data")
        button_load_data.connect("clicked", self.on_button_load_data_clicked)
        self.vbox.add(button_load_data)

        # Data label
        self.label = Gtk.Label()
        self.label.set_text("Zaragoza data:")
        self.label.set_justify(Gtk.Justification.LEFT)
        self.vbox.add(self.label)

        # Map
        map = folium.Map(location = getCoordinates(self.location), zoom_start = self.zoom_start)
        map.save(self.path)
        scrolled_window_1 = Gtk.ScrolledWindow()
        self.webview1 = WebKit2.WebView()
        self.webview1.load_uri("file://" + self.path)
        scrolled_window_1.add(self.webview1)
        self.vbox.pack_start(scrolled_window_1, True, True, 0)

        # Contaminant combo
        contaminant_store = Gtk.ListStore(str)
        contaminants = [
            "CO",
            "NO2",
            "SO2"
        ]
        for contaminant in contaminants:
            contaminant_store.append([contaminant])
        self.combo_contaminant = Gtk.ComboBox.new_with_model(contaminant_store)
        self.combo_contaminant.set_active(0)
        self.combo_contaminant.connect("changed", self.on_combo_contaminant_changed)
        renderer_text = Gtk.CellRendererText()
        self.combo_contaminant.pack_start(renderer_text, True)
        self.combo_contaminant.add_attribute(renderer_text, "text", 0)
        self.vbox.pack_start(self.combo_contaminant, False, False, 0)

        scrolled_window_2 = Gtk.ScrolledWindow()
        self.webview2 = WebKit2.WebView()
        self.webview2.load_uri("https://raw.githubusercontent.com/ayubero/RiskVisualizer/main/images/NO2.png")
        scrolled_window_2.add(self.webview2)
        self.vbox.pack_start(scrolled_window_2, True, True, 0)

        self.add(self.vbox)

    def on_button_load_data_clicked(self, button):
        self.label.set_text(self.location + " data:")
        coords = getCoordinates(self.location)
        self.showMap(center = coords)
    
    def showMap(self, center):
        # Create the map
        map = folium.Map(location = center, zoom_start = self.zoom_start)

        # Display the map
        map.save(self.path)
        self.webview.load_uri("file://" + self.path)
    
    def on_combo_contaminant_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.contaminant = model[tree_iter][0]
    
    def on_entry_location_changed(self, entry):
        self.location = entry.get_text()
        self.label.set_text(self.location + " data:")
        if self.location == 'Zaragoza':
            self.vbox.add(self.combo_contaminant)
            self.vbox.add(self.webview2)
        else:
            self.vbox.remove(self.combo_contaminant)
            self.vbox.remove(self.webview2)
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()