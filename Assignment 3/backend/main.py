from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import MLmodel
from fastapi import HTTPException
from pydantic import BaseModel

# Initialize FastAPI application
app = FastAPI() 

# Configure CORS settings to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows requests from local frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Instantiate the ML model
model = MLmodel()

# Define the schema for the request body using Pydantic to validate input
class PredictionRequest(BaseModel):
    address: str
    houseType: str
    bathrooms: int
    bedrooms: int
    carpark: int
    buildingArea: float
    landsize: float

# Define a root endpoint for basic connection testing
@app.get("/")
async def root():
    return {"message": "Welcome to the House Price Prediction API"}

# Endpoint to handle POST requests for predicting house price
@app.post("/predict")
async def predict_price(data: PredictionRequest):
    try:
        # Use the data from the JSON request body to make a prediction
        prediction, distance, propertyCoordinates, centerCoordinates, median_price, shap_df = model.predict(
            data.address, 
            data.houseType, 
            data.bathrooms, 
            data.bedrooms, 
            data.carpark, 
            data.buildingArea, 
            data.landsize
        )
        
        error = False

        print(prediction)
        if prediction == "No results found for the given address.":
            error = True
            
        if error == False:    
            # Get nearby house recommendations based on the prediction
            recommendation = model.recommend_nearby_houses(data.address, prediction)

        # Log the prediction and other key data for debugging purposes
        print(round(float(prediction), 2))
        print(round(distance, 2))
        print(propertyCoordinates[0], propertyCoordinates[1])
        print(centerCoordinates[0], centerCoordinates[1])

        # Return the prediction results and additional details
        return {
            "predicted_price": round(float(prediction), 2),
            "distance_between_cities": round(distance, 2),  
            "house_location": {"lat": propertyCoordinates[0], "lng": propertyCoordinates[1]},
            "city_center_location": {"lat": centerCoordinates[0], "lng": centerCoordinates[1]},
            "median_price": median_price,
            "recommended_properties": recommendation,
            "shap_values": shap_df.to_dict(orient="records")  # SHAP values for feature importance
        }
    except Exception as e:
        # Return a 500 error if an exception occurs during prediction
        raise HTTPException(status_code=500, detail=str(e))

# Run the application using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
