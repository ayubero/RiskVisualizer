import gi
import folium
import tempfile
import requests
import json

gi.require_version("Gtk", "3.0")
gi.require_version("WebKit2", "4.0")
from gi.repository import Gtk as Gtk, WebKit2

def mod(number):
    if(number<0):
        abs = -number
    else:
        abs = number
    return abs
    
class Data:
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

    def getEvents():
        resp = requests.get('https://eonet.sci.gsfc.nasa.gov/api/v2.1/events?status=open')
        json_file=resp.text
        data = json.loads(json_file)
        events = data['events']
        return events

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
        self.label1 = Gtk.Label()
        self.label1.set_text("Zaragoza data:")
        self.label1.set_justify(Gtk.Justification.LEFT)
        self.vbox.add(self.label1)

        # Map
        coordinates = Data.getCoordinates(self.location)
        self.events = Data.getEvents()
        map = folium.Map(location = coordinates, zoom_start = self.zoom_start, tiles="Stamen Toner")
        distance = 5
        colors = ['gray','gray','gray','gray','gray','gray','beige','orange','lightred','blue','darkblue','red','lightgreen','lightgray','lightblue','black','cadetblue','darkred','purple']
        risk_text = "Near risks:"
        for i in range(len(self.events)):
            event = self.events[i]
            try:
                title = event['title']
                description = event['categories'][0]['title'] + event['description']
                cat_id = int(event['categories'][0]['id'])
                location = event['geometries'][0]['coordinates']
                location = location[::-1]
                
                isNearLat = mod(coordinates[0])-distance <= mod(location[0]) < mod(coordinates[0])+distance
                isNearLon = mod(coordinates[1])-distance <= mod(location[1]) < mod(coordinates[1])+distance

                isNear = isNearLat and isNearLon

                if(isNear==True):
                    risk_text = risk_text + "\n" + title
                folium.Marker(location, popup="<b>"+description+"</b>", tooltip=title,icon=folium.Icon(color=colors[cat_id],icon="info-sign")).add_to(map)
            except:
                pass
        map.save(self.path)

        scrolled_window = Gtk.ScrolledWindow()
        self.webview = WebKit2.WebView()
        self.webview.load_uri("file://" + self.path)
        scrolled_window.add(self.webview)
        self.vbox.pack_start(scrolled_window, True, True, 0)

        # Risk label
        self.label2 = Gtk.Label()
        self.label2.set_text(risk_text)
        self.label2.set_justify(Gtk.Justification.LEFT)
        self.vbox.add(self.label2)

        self.add(self.vbox)

    def on_button_load_data_clicked(self, button):
        self.label1.set_text(self.location + " data:")

        # Create the map
        coordinates = Data.getCoordinates(self.location)
        map = folium.Map(location = coordinates, zoom_start = self.zoom_start, tiles="Stamen Toner")

        distance = 5
        colors = ['gray','gray','gray','gray','gray','gray','beige','orange','lightred','blue','darkblue','red','lightgreen','lightgray','lightblue','black','cadetblue','darkred','purple']
        risk_text = "Near risks:"
        for i in range(len(self.events)):
            event = self.events[i]
            try:
                title = event['title']
                description = event['categories'][0]['title'] + event['description']
                cat_id = int(event['categories'][0]['id'])
                location = event['geometries'][0]['coordinates']
                location = location[::-1]
                
                isNearLat = mod(coordinates[0])-distance <= mod(location[0]) < mod(coordinates[0])+distance
                isNearLon = mod(coordinates[1])-distance <= mod(location[1]) < mod(coordinates[1])+distance

                isNear = isNearLat and isNearLon

                if(isNear==True):
                    risk_text = risk_text + "\n" + title
                folium.Marker(location, popup="<b>"+description+"</b>", tooltip=title,icon=folium.Icon(color=colors[cat_id],icon="info-sign")).add_to(map)
            except:
                pass
        
        self.label2.set_text(risk_text)

        # Display the map
        map.save(self.path)
        self.webview.load_uri("file://" + self.path)
    
    '''def on_combo_contaminant_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            self.contaminant = model[tree_iter][0]'''
    
    def on_entry_location_changed(self, entry):
        self.location = entry.get_text()
        self.label1.set_text(self.location + " data:")
    
    '''def render_map(self, coordinates):
        distance = 5
        colors = ['gray','gray','gray','gray','gray','gray','beige','orange','lightred','blue','darkblue','red','lightgreen','lightgray','lightblue','black','cadetblue','darkred','purple']
        risk_text = "Near risks:"
        for i in range(len(self.events)):
            event = self.events[i]
            try:
                title = event['title']
                description = event['categories'][0]['title'] + event['description']
                cat_id = int(event['categories'][0]['id'])
                location = event['geometries'][0]['coordinates']
                location = location[::-1]
                
                isNearLat = mod(coordinates[0])-distance <= mod(location[0]) < mod(coordinates[0])+distance
                isNearLon = mod(coordinates[1])-distance <= mod(location[1]) < mod(coordinates[1])+distance

                isNear = isNearLat and isNearLon

                if(isNear==True):
                    risk_text = risk_text + "\n" + title
                folium.Marker(location, popup="<b>"+description+"</b>", tooltip=title,icon=folium.Icon(color=colors[cat_id],icon="info-sign")).add_to(map)
            except:
                pass
        return risk_text'''
        
win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()