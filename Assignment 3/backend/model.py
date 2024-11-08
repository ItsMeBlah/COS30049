import pandas as pd
import numpy as np
import pytz
import joblib
import re
import shap

from datetime import datetime
from custom_encoder import CustomLabelEncoder
from geographyProcess import Geography
from sklearn.metrics import mean_squared_error, r2_score, silhouette_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor
from sklearn.cluster import DBSCAN
from sklearn.metrics.pairwise import euclidean_distances


class MLmodel:

    # Initializes the MLmodel class by loading datasets and configuring the XGBRegressor model with specific hyperparameters.
    def __init__(self):
        self.originData = pd.read_csv("dataset/origin_combined_data.csv")
        self.medianPrice = pd.read_csv("dataset/median_price.csv")

        self.model = XGBRegressor(
            tree_method='auto',
            reg_lambda=1.819922238917205e-05,
            alpha=1.9292397183394133e-05,
            learning_rate=0.019165144383718857,
            n_estimators=828,
            max_depth=10,
            min_child_weight=10,
            gamma=2.2392510449716075e-06,
            subsample=0.5087275903255652,
            colsample_bytree=0.6309998023125251,
            random_state=42
        )

    def train_DBScan(self):
        # Trains a DBSCAN clustering model to group properties based on their geographical coordinates and price.
        # It scales data, applies DBSCAN clustering, calculates the silhouette score if there are enough clusters, 
        # and saves the trained model and scaler for later use.

        dataTemp = self.originData.copy()
        dataTemp = dataTemp.drop(columns=['Unnamed: 0']) 

        dataTemp = dataTemp.rename(columns={'Longtitude': 'Longitude', 'Lattitude': 'Latitude'})

        dataTemp = dataTemp[['Longitude', 'Latitude', 'Price']]  

        dbscanScaler = MinMaxScaler()
        dataScaled = dbscanScaler.fit_transform(dataTemp)

        dbscan = DBSCAN(eps=0.3, min_samples=2)
        labels = dbscan.fit_predict(dataScaled)
        dataTemp['Cluster'] = labels

        core_samples_mask = labels != -1
        if np.sum(core_samples_mask) > 1:
                silhouette = silhouette_score(dataScaled[core_samples_mask], labels[core_samples_mask])
                print(f"DBScan model trained. Silhouette score: {silhouette}")
        else:
                print("Not enough clusters to calculate silhouette score.")

        joblib.dump(dbscan, 'model/dbscan_model.pkl')
        joblib.dump(dbscanScaler, 'model/dbscan_scaler.pkl')


    def recommend_nearby_houses(self, address, price):
        # Recommends nearby properties based on the provided address and price.
        # Uses the DBSCAN model to find properties within the same cluster as the input property.
        # If the input property is noise (not part of any cluster), it finds the closest properties by distance.

        addressDataDBScan = Geography()

        coordinates = addressDataDBScan.get_coordinates(address)

        if coordinates == "No results found for the given address.":
            return "No results found for the given address."

        lat, long = coordinates[0], coordinates[1]

        dbscan = joblib.load('model/dbscan_model.pkl')
        dbscanScaler = joblib.load('model/dbscan_scaler.pkl')

        input_data = np.array([[long, lat, price]])
        input_scaled = dbscanScaler.transform(input_data)

        input_label = dbscan.fit_predict(input_scaled)[0]

        if input_label == -1:
                print("Input data is considered noise. Searching for closest properties.")

                dataTemp = self.originData.copy()
                dataTemp = dataTemp.drop(columns=['Unnamed: 0'])

                dataTemp = dataTemp.rename(columns={'Longtitude': 'Longitude', 'Lattitude': 'Latitude'})

                dataTemp = dataTemp[['Longitude', 'Latitude', 'Price']]
                dataScaled = dbscanScaler.transform(dataTemp)

                distances = euclidean_distances(input_scaled, dataScaled)
                dataTemp['Distance'] = distances[0]

                recommended_closest = dataTemp.sort_values(by='Distance').head(5)

                recommended_closest['Address'] = recommended_closest.apply(
                        lambda row: addressDataDBScan.address(row['Latitude'], row['Longitude']), axis=1
                )

                return recommended_closest[['Longitude', 'Latitude', 'Price', 'Address']]

        dataTemp = self.originData.copy()
        dataTemp = dataTemp.drop(columns=['Unnamed: 0'])

        dataTemp = dataTemp.rename(columns={'Longtitude': 'Longitude', 'Lattitude': 'Latitude'})

        dataTemp = dataTemp[['Longitude', 'Latitude', 'Price']]
        dataScaled = dbscanScaler.transform(dataTemp)
        labels = dbscan.fit_predict(dataScaled)
        dataTemp['Cluster'] = labels

        recommended_houses = dataTemp[dataTemp['Cluster'] == input_label]

        if recommended_houses.empty:
                print("No similar properties found in the cluster. Searching for closest properties.")
                distances = euclidean_distances(input_scaled, dataScaled)
                dataTemp['Distance'] = distances[0]
                recommended_closest = dataTemp.sort_values(by='Distance').head(5)

                recommended_closest['Address'] = recommended_closest.apply(
                        lambda row: addressDataDBScan.address(row['Latitude'], row['Longitude']), axis=1
                )

                return recommended_closest[['Longitude', 'Latitude', 'Price', 'Address']]

        recommended_houses['Address'] = recommended_houses.apply(
                lambda row: addressDataDBScan.address(row['Latitude'], row['Longitude']), axis=1
        )

        return recommended_houses[['Longitude', 'Latitude', 'Price', 'Address']]


    def train(self):
        # Trains the XGBoost model for property price prediction.
        # Encodes categorical features, scales the data, splits it into training and test sets, trains the model, 
        # and saves the trained model, encoders, and scalers for future predictions.
        # It also prints evaluation metrics for model performance (MSE and R²).

        self.originData = self.originData.drop(columns='Unnamed: 0')

        suburb_encoder = CustomLabelEncoder()
        city_encoder = CustomLabelEncoder()
        council_area_encoder = CustomLabelEncoder()
        type_encoder = CustomLabelEncoder()
        scaler_X = MinMaxScaler()  
        scaler_y = MinMaxScaler()  

        for i in self.originData.select_dtypes(include='object').columns:
                self.originData[i] = self.originData[i].str.replace('city', '')

        self.originData['Suburb'] = suburb_encoder.fit_transform(self.originData['Suburb'])
        self.originData['City'] = city_encoder.fit_transform(self.originData['City'])
        self.originData['CouncilArea'] = council_area_encoder.fit_transform(self.originData['CouncilArea'])
        self.originData['Type'] = type_encoder.fit_transform(self.originData['Type'])

        X = self.originData.drop(columns=["Price"])
        y = self.originData["Price"].values.reshape(-1, 1)

        X_scaled = scaler_X.fit_transform(X)
        y_scaled = scaler_y.fit_transform(y)

        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

        self.model.fit(X_train, y_train.ravel())

        joblib.dump(self.model, 'model/xgb_model.pkl')
        joblib.dump(suburb_encoder, 'model/suburb_encoder.pkl')
        joblib.dump(city_encoder, 'model/city_encoder.pkl')
        joblib.dump(council_area_encoder, 'model/council_area_encoder.pkl')
        joblib.dump(type_encoder, 'model/type_encoder.pkl')
        joblib.dump(scaler_X, 'model/scaler_X.pkl')
        joblib.dump(scaler_y, 'model/scaler_y.pkl')

        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        print(f"Model trained. MSE: {mse}, R²: {r2}")


    def preprocess(self, coordinates, distance, suburb, city, councilArea, postcode, type, bathrooms, bedrooms, cars, building_area, land_size):
        # Preprocesses input data for prediction by encoding categorical variables, scaling numerical features, 
        # and organizing data into a structured DataFrame for model input. Adjusts for specific property indices based on city.

        cashrate = 0.1
        property_index_melbourne = [185.7, 144.4]
        property_index_sydney = [218.7, 179.4]
        latitude = coordinates[0]
        longitude = coordinates[1]

        councilArea = re.sub(r'\b(City|Council|of|city|Of)\b', '', councilArea).strip()
        suburb = suburb.lower().replace(" ", "")
        city = city.lower().replace(" ", "")
        councilArea = councilArea.lower().replace(" ", "")

        melbourne_tz = pytz.timezone('Australia/Melbourne')
        date = datetime.now(melbourne_tz)
        daySold = date.day
        monthSold = date.month
        yearSold = date.year

        suburb_encoder = joblib.load('model/suburb_encoder.pkl')
        city_encoder = joblib.load('model/city_encoder.pkl')
        council_area_encoder = joblib.load('model/council_area_encoder.pkl')
        type_encoder = joblib.load('model/type_encoder.pkl')
        scaler_X = joblib.load('model/scaler_X.pkl')

        suburb_encoded = suburb_encoder.transform([suburb])[0]
        city_encoded = city_encoder.transform([city])[0]
        councilArea_encoded = council_area_encoder.transform([councilArea])[0]
        type_encoded = type_encoder.transform([type])[0]

        data_dict = {
                'Suburb': [suburb_encoded],
                'Type': [type_encoded],
                'Distance': [distance],
                'Postcode': [postcode],
                'Bedroom': [bedrooms],
                'Bathroom': [bathrooms],
                'Car': [cars],
                'Landsize': [land_size],
                'BuildingArea': [building_area],
                'CouncilArea': [councilArea_encoded],
                'Lattitude': [latitude],
                'Longtitude': [longitude],
                'City': [city_encoded],
                'CashRate': [cashrate],
                'Residential Property Price Index': [property_index_melbourne[0]],  
                'Attached Dwellings Price Index': [property_index_melbourne[1]],          
                'DaySold': [daySold],
                'MonthSold': [monthSold],
                'YearSold': [yearSold]
        }

        data = pd.DataFrame(data_dict)

        if city_encoded == 1:  
                data['Residential Property Price Index'] = property_index_sydney[0]
                data['Attached Dwellings Price Index'] = property_index_sydney[1]

        data_scaled = scaler_X.transform(data)

        return data_scaled
    
    def feature_importance(self, model, single_prediction):
        # Computes feature importance using SHAP (SHapley Additive exPlanations) for a single prediction.
        # Filters SHAP values for selected features and returns them in a structured DataFrame for interpretability.

        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(single_prediction)
        
        filtered_feature_names = ['Type', 'Bedroom', 'Bathroom', 'Car', 'Landsize', 'BuildingArea', 'Latitude', 'Longitude']
        filtered_shap_values = [shap_values[0][1], shap_values[0][4], shap_values[0][5], shap_values[0][6], shap_values[0][7], shap_values[0][8], shap_values[0][10], shap_values[0][11]]

        shap_df = pd.DataFrame({
                'Feature': filtered_feature_names,
                'SHAP Value': np.abs(filtered_shap_values)
        })

        return shap_df
        

    def predict(self, address, type, bathrooms, bedrooms, cars, building_area, land_size):
        # Predicts the price of a property based on input details like address, type, and features.
        # Preprocesses the input data, loads the trained XGBoost model, and predicts the property price.
        # Returns the predicted price, distance to the city center, and SHAP values for feature importance analysis.

        model = joblib.load('model/xgb_model.pkl')

        addressData = Geography()

        coordinates = addressData.get_coordinates(address)
        suburb = addressData.get_suburb(address)
        city = addressData.get_city(address)
        councilArea = addressData.get_council_area(address)
        postcode = addressData.get_postcode(address)
        distance = addressData.get_distance(address)

        type = type.lower().strip()
        if type == 'house':
            type = 'h'
        elif type == 'unit' or type == 'apartment':
            type = 'u'
        elif type == 'townhouse':
            type = 't'
        else:
            return "Invalid property type."

        print(city)

        if city.lower() == "melbourne":
            centerCoordinates = addressData.get_melbourne_center_coordinates()
        elif city.lower() == "sydney":
            centerCoordinates = addressData.get_sydney_center_coordinates()
        else:
            return "No results found for the given address.", "No results found for the given address.", "No results found for the given address.", "No results found for the given address.", "No results found for the given address.", "No results found for the given address."


        data_scaled = self.preprocess(coordinates, distance, suburb, city, councilArea, postcode, type, bathrooms, bedrooms, cars, building_area, land_size)

        prediction_scaled = model.predict(data_scaled)

        scaler_y = joblib.load('model/scaler_y.pkl')
        prediction_original_scale = scaler_y.inverse_transform(prediction_scaled.reshape(-1, 1))

        median_price_cop = self.medianPrice.copy()
        median_price_cop = median_price_cop.drop(columns='Unnamed: 0')

        median_price_cop = pd.DataFrame(median_price_cop)

        median_price_cop = median_price_cop.values.tolist()

        shap_df = self.feature_importance(model, data_scaled)

        return prediction_original_scale[0, 0], distance, coordinates, centerCoordinates, median_price_cop, shap_df

if __name__ == "__main__":
    # Instantiates the MLmodel class, trains the DBSCAN clustering model, and trains the XGBoost price prediction model.

    model = MLmodel()
    model.train_DBScan()
    model.train()