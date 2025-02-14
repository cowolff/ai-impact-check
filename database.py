import sqlite3
import googlemaps

class AffiliationLocator:
    def __init__(self, db_path='affiliations.db', api_key=''):
        # Initialize Google Maps client with the provided API key
        self.gmaps = googlemaps.Client(key=api_key)
        
        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
        # Create the table to store affiliations and coordinates if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS affiliations (
                institution TEXT,
                country TEXT,
                latitude REAL,
                longitude REAL,
                PRIMARY KEY (institution, country)
            )
        ''')
        self.conn.commit()

    def get_geolocation(self, address):
        
        # Geocode the address
        geocode_result = self.gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            return location['lat'], location['lng']
        return None, None

    def get_location(self, institution, country):
        # Check if affiliation is already in the database
        self.cursor.execute("SELECT latitude, longitude FROM affiliations WHERE institution = ? AND country = ?", 
                            (institution, country))
        result = self.cursor.fetchone()

        if result:
            return result  # Return coordinates if found

        # If not found, get geolocation and add to database
        address = f"{institution}, {country}"
        lat, lng = self.get_geolocation(address)
        
        if lat is not None and lng is not None:
            self.cursor.execute("INSERT INTO affiliations (institution, country, latitude, longitude) VALUES (?, ?, ?, ?)", 
                                (institution, country, lat, lng))
            self.conn.commit()
            return lat, lng
        else:
            print(f"Coordinates for {institution}, {country} could not be found.")
            return None, None

    def close(self):
        # Close the database connection
        self.conn.close()