from model import MLmodel
import pandas as pd

address = '155 Macquarie Street, Sydney, NSW 2000'

model = MLmodel()


prediction, distance, coordinates, centerCoor, median_price, shap_df = model.predict(address , type = 'unit', bathrooms = 1, bedrooms = 1, cars = 0, building_area = 70, land_size = 100)
recommend = model.recommend_nearby_houses(address, prediction)

print('---------------------------------')
print(f"The predicted price is", prediction)
print(f"The distance between the property and the city center is", distance)
print(f"The coordinates of the property are", coordinates[0], coordinates[1])
print(f"The coordinates of the city center are", centerCoor[0], centerCoor[1])

print(shap_df)

print('---------------------------------')


if isinstance(recommend, str) and recommend == "No results found for the given address.":
    print(recommend)
elif isinstance(recommend, pd.DataFrame) and not recommend.empty:
    for _, row in recommend.iterrows():
        longitude = row['Longitude']
        latitude = row['Latitude']
        price = row['Price']
        address = row['Address']

        print(f"Longitude: {longitude}, Latitude: {latitude}, Price: {price}, Address: {address}")
else:
    print("No similar properties found.")


#uvicorn main:app --reload
