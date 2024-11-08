import React, { useState } from 'react';
import Button from '../Button/Button.js'; 
import './SearchForm.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import CircularProgress from '@mui/material/CircularProgress';

function SearchForm() {
    const [formData, setFormData] = useState({
        address: '',
        bathrooms: '',
        bedrooms: '',
        carpark: '',
        houseType: '',
        buildingArea: '',
        landsize: '',
    });

    const [loading, setLoading] = useState(false); // State for loading
    const [showError, setShowError] = useState(false); // State for error messages
    const navigate = useNavigate();

    // Check if all fields are filled
    const isFormValid = () => {
        return Object.values(formData).every(value => value !== '');
    };

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!isFormValid()) {
            setShowError(true);
            alert('Please fill out all fields before submitting.');
            return;
        }
        setLoading(true); // Start loading when the form is submitted
        setShowError(false); // Hide error if the form is valid
        try {
            // Make API call to the backend
            const response = await axios.post('http://localhost:8000/predict', formData);

            // Navigate to the Prediction page with the response data
            navigate('/predict', { 
                state: { 
                    prediction: response.data.predicted_price, 
                    formData, 
                    distance: response.data.distance_between_cities,
                    houseLocation: response.data.house_location, 
                    cityCenterLocation: response.data.city_center_location,
                    medianPrice: response.data.median_price,
                    recommendedProperties: response.data.recommended_properties,
                    shapValues: response.data.shap_values   
                } 
            });
        } catch (error) {
            console.error('Error making prediction:', error);
            navigate('/error');
        } finally {
            setLoading(false); // Stop loading after API call is complete
        }
    };

    return (
        <div className="search-form-wrapper-outer">
            <div className="search-form-wrapper-inner">
                {loading ? (
                    // Display the loading spinner when loading is true
                    <div className="loading-spinner">
                        <CircularProgress />
                        <p>Loading, please wait...</p>
                    </div>
                ) : (
                    <form onSubmit={handleSubmit} className="search-form">
                        <div className="form-group">
                            <label>Enter your Address:</label>
                            <input
                                type="text"
                                name="address"
                                placeholder="Enter your Address"
                                value={formData.address}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.address ? 'highlight-error' : ''}`}
                            />
                        </div>

                        <div className="form-group">
                            <label>Number of Bathrooms:</label>
                            <input
                                type="number"
                                name="bathrooms"
                                placeholder="Number of Bathrooms"
                                value={formData.bathrooms}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.bathrooms ? 'highlight-error' : ''}`}
                                min="0"
                            />
                        </div>
                        
                        <div className="form-group">
                            <label>Number of Bedrooms:</label>
                            <input
                                type="number"
                                name="bedrooms"
                                placeholder="Number of Bedrooms"
                                value={formData.bedrooms}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.bedrooms ? 'highlight-error' : ''}`}
                                min="0"
                            />
                        </div>

                        <div className="form-group">
                            <label>Number of Carparks:</label>
                            <input
                                type="number"
                                name="carpark"
                                placeholder="Carpark"
                                value={formData.carpark}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.carpark ? 'highlight-error' : ''}`}
                                min="0"
                            />
                        </div>

                        <div className="form-group">
                            <label>Type Of House (e.g., townhouse, unit/apartment):</label>
                            <select
                                name="houseType"
                                value={formData.houseType}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.houseType ? 'highlight-error' : ''}`}
                            >
                                <option value="">Select a Type</option> 
                                <option value="Townhouse">Townhouse</option>
                                <option value="House">House</option>
                                <option value="Unit">Unit/Apartment</option>
                            </select>
                        </div>


                        <div className="form-group">
                            <label>Building Area:</label>
                            <input
                                type="number"
                                name="buildingArea"
                                placeholder="Building Area"
                                value={formData.buildingArea}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.buildingArea ? 'highlight-error' : ''}`}
                                min="0"
                            />
                        </div>

                        <div className="form-group">
                            <label>Landsize:</label>
                            <input
                                type="number"
                                name="landsize"
                                placeholder="Landsize"
                                value={formData.landsize}
                                onChange={handleChange}
                                className={`input-field ${showError && !formData.landsize ? 'highlight-error' : ''}`}
                                min="0"
                            />
                        </div>

                        {showError && (
                            <div className="error-message">
                                <p>* Please Enter All Required Fields.</p>
                            </div>
                        )}

                        <Button label={"Make A Prediction"} buttonType={"primary"} />
                    </form>
                )}
            </div>
        </div>
    );
} 

export default SearchForm;