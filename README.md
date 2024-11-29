
# Full Stack Predict Housing Price Web Application

This project is a full-stack web application that predicts housing prices based on user-provided inputs such as location, size, and property features. It uses a machine learning model to generate accurate price estimates and provides an intuitive user interface for easy interaction. The backend API handles data processing and model predictions, while the frontend displays results and visual insights. The application is designed for homebuyers, real estate agents, and investors, offering a seamless and efficient way to analyze housing prices.

## Demo

**Homepage**

<img width="1265" alt="Screenshot 2024-11-29 133551" src="https://github.com/user-attachments/assets/a1be440f-fc5b-42c6-83d7-766603465e26">

**Formpage**

<img width="1268" alt="Screenshot 2024-11-29 133711" src="https://github.com/user-attachments/assets/58451579-6f58-42b0-aaec-aea00e7ecb54">

**Visualization Page**

<img width="1267" alt="Screenshot 2024-11-29 133831" src="https://github.com/user-attachments/assets/d6b25b19-8365-42d8-a785-2d04aa17a142">

<img width="1265" alt="Screenshot 2024-11-29 133947" src="https://github.com/user-attachments/assets/26d76532-e300-4b79-945b-b892d4a71a4f">

## API Reference

**openstreetmap.org**

Using method ```GET``` to take all the necessary data

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Your personal emai` | `string` | **Required**. OpenStreetMap requires your email in the header for accountability, troubleshooting, compliance, and ensuring responsible API usage while preventing abuse. Update your personal email in the header of the backend file ```geographyProcess.py``` |

## Installation

**Front End**

Ensure that the terminal directory is strictly navigated to the right directory of ```./Assignmen3VangaRealEstate-11a6cbcda3f19c545ac8d7af6f1f6675a698847d```
```Installation
npm install
```

**Back End**

Using ```pip install``` to download all the dependencies

```Installation
numpy
pandas
scikit-learn
xgboost
shap
joblib
geopy
pytz
requests
fastapi
uvicorn
pydantic
```



## Usage/Examples

**Front End**

Ensure that the terminal directory is strictly navigated to the right directory of ```./Assignmen3/VangaRealEstate-11a6cbcda3f19c545ac8d7af6f1f6675a698847d```

```Usage
npm start
```

**Back End**

Ensure that the terminal directory is strictly navigated to the right directory of ```./Assignmen3/backend```

```Usage
uvicorn main:app --reload
```
