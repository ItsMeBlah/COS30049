import pandas as pd
import numpy as np
import requests

from geopy import distance

# Class to handle geographical data and perform geocoding using external APIs
class Geography:
    def __init__(self):
        # Initializes the central addresses for Melbourne and Sydney
        self.melbourneCenterAddress = "Melbourne CBD, Victoria, Australia" 
        self.sydneyCenterAddress = "Sydney CBD, New South Wales, Australia" 

    def get_address_attributes(self, address):
        # Sends a request to the Nominatim API to retrieve address details in JSON format
        address = address.replace(",", "")
        address = address.replace(" ", "+")
        url = f"https://nominatim.openstreetmap.org/search.php?q={address}&format=jsonv2"

        headers = {
            "User-Agent": "MyGeocodingApp/1.0 (caominh418@gmail.com)"  
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            if response:
                return response
            else:
                return "No results found for the given address."
        else:
            return f"Error: Request failed with status code {response.status_code}"
        
    def get_coordinates(self, address):
        # Gets latitude and longitude coordinates of an address using the Nominatim API
        response = self.get_address_attributes(address)

        if response.status_code == 200:
            data = response.json()
            if data:
                coordinates = [data[0]["lat"], data[0]["lon"]]
                return coordinates
            else:
                return "No results found for the given address."
        else:
            return f"Error: Request failed with status code {response.status_code}"
        
    def get_suburb(self, address):
        # Retrieves the suburb name from an address using the Nominatim API
        response = self.get_address_attributes(address)

        if response.status_code == 200:
            data = response.json()
            if data:
                suburb = data[0]["display_name"].split(",")[1]
                return suburb
            else:
                return "No results found for the given address."
        else:
            return f"Error: Request failed with status code {response.status_code}"
        
    def get_city(self, address):
        # Identifies the city (Sydney or Melbourne) from an address using the Nominatim API
        response = self.get_address_attributes(address)

        if response.status_code == 200:
            data = response.json()
            if data:
                parts = data[0]["display_name"].split(",")
                city = None
                for part in parts:
                    part = part.strip()  # Clean up whitespace
                    if part.lower() == "sydney" or part.lower() == "melbourne":
                        city = part
                        break  # Stop once the city is found
                return city if city else "City not found."
            else:
                return "No results found for the given address."
        else:
            return f"Error: Request failed with status code {response.status_code}"

        
    def get_council_area(self, address):
        # Retrieves the council area from an address using the Nominatim API
        response = self.get_address_attributes(address)

        if response.status_code == 200:
            data = response.json()
            if data:
                council_area = data[0]["display_name"].split(",")[3]
                return council_area
            else:
                return "No results found for the given address."
        else:
            return f"Error: Request failed with status code {response.status_code}"
        
    def get_postcode(self, address):
        # Extracts the postal code from an address using the Nominatim API
        response = self.get_address_attributes(address)

        if response.status_code == 200:
            data = response.json()
            if data:
                parts = data[0]["display_name"].split(",")
                postcode = None
                for part in parts:
                    part = part.strip()  
                    if part.isdigit() and len(part) == 4:  # Check for a 4-digit postal code
                        postcode = part  
                        break  
                return postcode if postcode else "Postal code not found."
            else:
                return "No results found for the given address."
        else:
            return f"Error: Request failed with status code {response.status_code}"

                
    def get_melbourne_center_coordinates(self):
        # Returns the coordinates of Melbourne's city center
        coor = self.get_coordinates(self.melbourneCenterAddress)
        return coor
    
    def get_sydney_center_coordinates(self):
        # Returns the coordinates of Sydney's city center
        coor = self.get_coordinates(self.sydneyCenterAddress)
        return coor

    def get_distance(self, address):
        # Calculates the distance between the given address and the city center (Melbourne or Sydney)
        addressCity = self.get_city(address)
        addressCity = addressCity.replace(" ", "")
        addressSearchCoor = self.get_coordinates(address)

        if addressCity == "Melbourne":
            centerAddress = self.get_melbourne_center_coordinates()
            return distance.distance(centerAddress, addressSearchCoor).km 
        
        elif addressCity == "Sydney":
            centerAddress = self.get_sydney_center_coordinates()
            return distance.distance(centerAddress, addressSearchCoor).km
        
    def address(self, lat, lon):
        # Uses reverse geocoding to get an address from latitude and longitude coordinates
        try:
            lat = float(lat)
            lon = float(lon)
            
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=jsonv2"
            headers = {
                "User-Agent": "MyGeocodingApp/1.0 (caominh418@gmail.com)"  
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if data and 'display_name' in data:
                    return data['display_name']
                else:
                    return "Unknown"
            else:
                return f"Error: Request failed with status code {response.status_code}"

        except Exception as e:
            print(f"Error retrieving address: {e}")
            return "Unknown"
