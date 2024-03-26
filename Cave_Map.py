import sys
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import folium
import geocoder
from geopy.distance import geodesic

class CaveMapper(QWidget):
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.df = self.csv_to_dataframe()
        self.user_location = None
        self.map_widget = None
        self.initUI()

    def csv_to_dataframe(self):
        try:
            df = pd.read_csv(self.filepath)
            return df
        except FileNotFoundError:
            print(f"File not found: {self.filepath}")
            return None
        except pd.errors.EmptyDataError:
            print(f"Empty file: {self.filepath}")
            return None
        except pd.errors.ParserError:
            print(f"Error parsing the CSV file: {self.filepath}")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None

    def show_all_cave_locations(self):
        self.search_entry.clear()
        self.distance_input.clear()
        self.filter_caves("")

        if self.df is not None:
            # Calculate the mean latitude and longitude of all caves
            mean_lat = self.df['latitude'].mean()
            mean_lon = self.df['longitude'].mean()

            # Create a map centered on the mean latitude and longitude
            cave_map = folium.Map(location=[mean_lat, mean_lon], zoom_start=6)

            # Add markers for each cave location with the cave name, coordinates, and a button
            for idx, row in self.df.iterrows():
                cave = row['cave']
                latitude = row['latitude']
                longitude = row['longitude']
                popup_html = f'''
                    <b>{cave}</b><br>
                    Latitude: {latitude}<br>
                    Longitude: {longitude}<br>
                    <button onclick="console.log('{cave}')">Print Cave Name</button>
                '''
                popup = folium.Popup(popup_html, max_width=300)
                folium.Marker([latitude, longitude], popup=popup).add_to(cave_map)

            # Save the map as an HTML file
            cave_map.save("caves.html")

            # Load the HTML file in the map widget
            self.map_widget.load(QUrl.fromLocalFile(os.path.abspath("caves.html")))
        else:
            print("DataFrame is empty or None")

    def show_cave_at_index(self, index):
        if not self.search_entry.text():
            # If the search entry is empty, use the original DataFrame
            if not self.df.empty:
                if 0 <= index < len(self.df):
                    cave = self.df.iloc[index]['cave']
                    latitude = self.df.iloc[index]['latitude']
                    longitude = self.df.iloc[index]['longitude']
                else:
                    print(f"Invalid index. Please select a cave from the list.")
                    return
            else:
                print("No caves found in the DataFrame.")
                return
        else:
            # If the search entry is not empty, use the filtered DataFrame
            if not self.filtered_caves.empty:
                if 0 <= index < len(self.filtered_caves):
                    cave = self.filtered_caves.iloc[index]['cave']
                    latitude = self.filtered_caves.iloc[index]['latitude']
                    longitude = self.filtered_caves.iloc[index]['longitude']
                else:
                    print(f"Invalid index. Please select a cave from the list.")
                    return
            else:
                print("No caves found in the filtered list.")
                return

        # Create a map centered on the cave location
        cave_map = folium.Map(location=[latitude, longitude], zoom_start=10)

        # Add a marker for the cave location with the cave name, coordinates, and a button
        popup_html = f'''
            <b>{cave}</b><br>
            Latitude: {latitude}<br>
            Longitude: {longitude}<br>
            <button onclick="console.log('{cave}')">Print Cave Name</button>
        '''
        popup = folium.Popup(popup_html, max_width=300)
        folium.Marker([latitude, longitude], popup=popup).add_to(cave_map)

        # Save the map as an HTML file
        cave_map.save("selected_cave.html")

        # Load the HTML file in the map widget
        self.map_widget.load(QUrl.fromLocalFile(os.path.abspath("selected_cave.html")))

    def show_user_location(self):
        if self.user_location is not None:
            user_lat, user_lon = self.user_location

            # Create a map centered on the user's location
            user_map = folium.Map(location=[user_lat, user_lon], zoom_start=10)

            # Add a marker for the user's location
            folium.Marker([user_lat, user_lon], popup="Your Location", icon=folium.Icon(color='red')).add_to(user_map)

            # Save the map as an HTML file
            user_map.save("user_location.html")

            # Load the HTML file in the map widget
            self.map_widget.load(QUrl.fromLocalFile(os.path.abspath("user_location.html")))
        else:
            print("User location is not available.")

    def show_filtered_cave_locations(self):
        if not self.filtered_caves.empty:
            # Calculate the mean latitude and longitude of filtered caves
            mean_lat = self.filtered_caves['latitude'].mean()
            mean_lon = self.filtered_caves['longitude'].mean()

            # Create a map centered on the mean latitude and longitude
            cave_map = folium.Map(location=[mean_lat, mean_lon], zoom_start=6)

            # Add markers for each filtered cave location with the cave name, coordinates, and a button
            for idx, row in self.filtered_caves.iterrows():
                cave = row['cave']
                latitude = row['latitude']
                longitude = row['longitude']
                popup_html = f'''
                    <b>{cave}</b><br>
                    Latitude: {latitude}<br>
                    Longitude: {longitude}<br>
                    <button onclick="console.log('{cave}')">Print Cave Name</button>
                '''
                popup = folium.Popup(popup_html, max_width=300)
                folium.Marker([latitude, longitude], popup=popup).add_to(cave_map)

            # Save the map as an HTML file
            cave_map.save("filtered_caves.html")

            # Load the HTML file in the map widget
            self.map_widget.load(QUrl.fromLocalFile(os.path.abspath("filtered_caves.html")))
        else:
            self.map_widget.setHtml("No caves found.")

    def show_caves_within_distance(self, distance):
        if self.df is not None and self.user_location is not None:
            user_lat, user_lon = self.user_location

            # Filter caves within the specified distance from the user's location
            nearby_caves = self.df.loc[self.df.apply(lambda row: geodesic((user_lat, user_lon), (row['latitude'], row['longitude'])).miles <= distance, axis=1)]

            if not nearby_caves.empty:
                # Create a map centered on the user's location
                nearby_caves_map = folium.Map(location=[user_lat, user_lon], zoom_start=8)

                # Add a marker for the user's location
                folium.Marker([user_lat, user_lon], popup="Your Location", icon=folium.Icon(color='red')).add_to(nearby_caves_map)

                # Add markers for nearby caves with the cave name
                for idx, row in nearby_caves.iterrows():
                    cave = row['cave']
                    latitude = row['latitude']
                    longitude = row['longitude']
                    folium.Marker([latitude, longitude], popup=cave).add_to(nearby_caves_map)

                # Save the map as an HTML file
                nearby_caves_map.save("nearby_caves.html")

                # Load the HTML file in the map widget
                self.map_widget.load(QUrl.fromLocalFile(os.path.abspath("nearby_caves.html")))
            else:
                print("No caves found within the specified distance.")
        else:
            print("DataFrame is empty or user location is not available.")

    def filter_caves_by_distance(self, text):
        if self.user_location is None:
            self.get_user_location()
        self.filter_caves(self.search_entry.text())

    def filter_caves(self, text):
        self.cave_list.clear()
        if text:
            self.filtered_caves = self.df[self.df['cave'].str.lower().str.startswith(text.lower())]
        else:
            self.filtered_caves = self.df

        if self.distance_input.text() and self.user_location is not None:
            try:
                distance = float(self.distance_input.text())
                user_lat, user_lon = self.user_location
                self.filtered_caves = self.filtered_caves.loc[self.filtered_caves.apply(lambda row: geodesic((user_lat, user_lon), (row['latitude'], row['longitude'])).miles <= distance, axis=1)]
            except ValueError:
                pass

        self.cave_list.addItems(self.filtered_caves['cave'].tolist())
        self.show_filtered_cave_locations()

    def initUI(self):
        if self.df is not None:
            layout = QVBoxLayout()

            # Create a horizontal layout for the map and controls
            main_layout = QHBoxLayout()

            # Create the map widget
            self.map_widget = QWebEngineView()
            main_layout.addWidget(self.map_widget, 3)  # Set the map widget to take up 3/4 of the space

            # Create a vertical layout for the controls
            controls_layout = QVBoxLayout()

            # Create a search entry box
            self.search_entry = QLineEdit()
            self.search_entry.setPlaceholderText("Search caves...")
            self.search_entry.textChanged.connect(self.filter_caves)
            controls_layout.addWidget(self.search_entry)

            # Create a list widget for cave names
            self.cave_list = QListWidget()
            self.cave_list.addItems(self.df['cave'].tolist())
            controls_layout.addWidget(self.cave_list)

            # Create a button to show the selected cave on the map
            show_cave_button = QPushButton("Show on Map")
            show_cave_button.clicked.connect(lambda: self.show_cave_at_index(self.cave_list.currentRow()))
            controls_layout.addWidget(show_cave_button)

            # Create a button to show the user's location
            user_location_button = QPushButton("Show My Location")
            user_location_button.clicked.connect(self.get_user_location)
            controls_layout.addWidget(user_location_button)

             # Create a label and input for distance
            distance_label = QLabel("Distance (miles):")
            controls_layout.addWidget(distance_label)

            self.distance_input = QLineEdit()
            self.distance_input.textChanged.connect(self.filter_caves_by_distance)
            controls_layout.addWidget(self.distance_input)



            # Create a button to show all cave locations
            show_all_button = QPushButton("Show All Caves")
            show_all_button.clicked.connect(self.show_all_cave_locations)
            controls_layout.addWidget(show_all_button)

            main_layout.addLayout(controls_layout, 1)  # Set the controls layout to take up 1/4 of the space
            layout.addLayout(main_layout)

            self.setLayout(layout)
            self.setGeometry(100, 100, 800, 600)
            self.setWindowTitle('Cave Mapper')

            # Show all cave locations when the application starts
            self.show_all_cave_locations()

            self.show()
        else:
            print("DataFrame is empty or None")

    def get_user_location(self):
        location = geocoder.ip('me')
        if location.ok:
            self.user_location = location.latlng
            print("User location retrieved successfully.")
            self.show_user_location()
        else:
            print("Unable to retrieve user location.")

if __name__ == '__main__':
    filepath = r"C:\Users\Admin\Downloads\caves.csv"
    app = QApplication(sys.argv)
    cave_mapper = CaveMapper(filepath)
    sys.exit(app.exec_())