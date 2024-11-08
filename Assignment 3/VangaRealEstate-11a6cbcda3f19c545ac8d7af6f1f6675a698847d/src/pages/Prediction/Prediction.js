import React, { useEffect, useState, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import Plot from 'react-plotly.js';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';
import './Prediction.css'; 

// Define custom icons for markers
const redIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

const greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

const blueIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41],
});

function Prediction() {
    const location = useLocation();
    const { prediction, formData, distance, houseLocation, cityCenterLocation, medianPrice, recommendedProperties, shapValues } = location.state || {};
    const contentRef = useRef();  

    const [formattedRecommendedProperties, setFormattedRecommendedProperties] = useState([]);
    const [selectedYear, setSelectedYear] = useState(null);
    const [chartData, setChartData] = useState({ months: [], prices: [] });

    const uniqueYears = [...new Set(medianPrice.map(data => data[0]))]; 

    useEffect(() => {
        if (recommendedProperties && typeof recommendedProperties === 'object') {
            const { Longitude, Latitude, Price, Address } = recommendedProperties;
            const keys = Object.keys(Longitude);

            const convertedArray = keys.map(key => ({
                latitude: Latitude[key],
                longitude: Longitude[key],
                price: Price[key],
                address: Address[key] || 'Unknown',
            }));
            setFormattedRecommendedProperties(convertedArray);
        }
    }, [recommendedProperties]);

    useEffect(() => {
        if (selectedYear) {
            const filteredData = medianPrice.filter(data => data[0] === selectedYear);
            setChartData({ months: filteredData.map(data => `Month ${data[1]}`), prices: filteredData.map(data => data[2]) });
        }
    }, [selectedYear, medianPrice]);

    const houseLatLng = houseLocation ? [houseLocation.lat, houseLocation.lng] : null;
    const cityCenterLatLng = cityCenterLocation ? [cityCenterLocation.lat, cityCenterLocation.lng] : null;
    const shapLabels = shapValues.map((item) => item.Feature);
    const shapValuesData = shapValues.map((item) => item['SHAP Value']);

    const exportToPDF = () => {
        const input = contentRef.current;
        html2canvas(input).then((canvas) => {
            const imgData = canvas.toDataURL('image/png');
            const pdf = new jsPDF('p', 'mm', 'a4');
            const imgWidth = 190;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;
            pdf.addImage(imgData, 'PNG', 10, 10, imgWidth, imgHeight);
            pdf.save('report.pdf');
        });
    };

    return (
        <div className="prediction-container" ref={contentRef}>
            <button onClick={exportToPDF} className="hover-button">
                Export to PDF
            </button>

            <div className="prediction-main-content">
                <div className="prediction-details">
                    <h2>Prediction Result</h2>
                    <div>
                        <p><strong>Predicted Price:</strong> ${prediction.toLocaleString()}</p>
                        <h3>Details Entered:</h3>
                        <ul className="details-list">
                            <li><strong>Address:</strong> {formData.address}</li>
                            <li><strong>Bathrooms:</strong> {formData.bathrooms}</li>
                            <li><strong>Bedrooms:</strong> {formData.bedrooms}</li>
                            <li><strong>Carpark:</strong> {formData.carpark}</li>
                            <li><strong>House Type:</strong> {formData.houseType}</li>
                            <li><strong>Building Area:</strong> {formData.buildingArea}</li>
                            <li><strong>Landsize:</strong> {formData.landsize}</li>
                        </ul>
                        <h3>Distance to City Center:<br /></h3>
                        <p className="distance-info">{distance} kilometers</p>
                    </div>
                </div>

                <div className="prediction-map">
                    <MapContainer center={cityCenterLatLng || [0, 0]} zoom={13} style={{ height: '600px', width: '100%' }}>
                        <TileLayer
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        />
                        {houseLatLng && (
                            <Marker position={houseLatLng} icon={redIcon}>
                                <Popup>
                                    <div>
                                        <h4>Property Information</h4>
                                        <p><strong>Predicted Price:</strong> ${prediction.toLocaleString()}</p>
                                        <p><strong>Address:</strong> {formData.address}</p>
                                        <p><strong>Bathrooms:</strong> {formData.bathrooms}</p>
                                        <p><strong>Bedrooms:</strong> {formData.bedrooms}</p>
                                        <p><strong>Carpark:</strong> {formData.carpark}</p>
                                        <p><strong>House Type:</strong> {formData.houseType}</p>
                                        <p><strong>Building Area:</strong> {formData.buildingArea} sqm</p>
                                        <p><strong>Landsize:</strong> {formData.landsize} sqm</p>
                                    </div>
                                </Popup>
                            </Marker>
                        )}
                        {cityCenterLatLng && (
                            <Marker position={cityCenterLatLng} icon={greenIcon}>
                                <Popup><strong>City Center CBD</strong></Popup>
                            </Marker>
                        )}
                        {houseLatLng && cityCenterLatLng && (
                            <Polyline positions={[houseLatLng, cityCenterLatLng]} color="blue" />
                        )}
                        {formattedRecommendedProperties.map((property, index) => (
                            <Marker key={index} position={[property.latitude, property.longitude]} icon={blueIcon}>
                                <Popup>
                                    <div>
                                        <h4>Recommended Property</h4>
                                        <p><strong>Price:</strong> ${property.price ? property.price.toLocaleString() : 'N/A'}</p>
                                        <p><strong>Address:</strong> {property.address}</p>
                                    </div>
                                </Popup>
                            </Marker>
                        ))}
                    </MapContainer>
                </div>
            </div>

            <div className="chart-section">
                <div className="chart-container">
                    <h3>Factors Influencing the Price</h3>
                    <Plot
                        data={[{ type: 'pie', labels: shapLabels, values: shapValuesData, textinfo: 'label+percent', hole: 0.3 }]}
                        layout={{ title: 'Feature Importance for Price (SHAP)', autosize: true }}
                        useResizeHandler
                        style={{ width: '100%', height: '500px' }}
                    />
                </div>

                <div className="chart-container">
                    <h3>Select Year to View Median Price per Month</h3>
                    <select onChange={(e) => setSelectedYear(parseInt(e.target.value))} value={selectedYear || ''} style={{ padding: '10px', marginBottom: '20px' }}>
                        <option value='' disabled>Select Year</option>
                        {uniqueYears.map(year => (
                            <option key={year} value={year}>{year}</option>
                        ))}
                    </select>

                    {selectedYear && chartData.months.length > 0 && (
                        <Plot
                            data={[
                                { x: chartData.months, y: chartData.prices, type: 'scatter', mode: 'lines+markers', name: `Median Price in ${selectedYear}`, line: { color: 'blue' }},
                                { x: chartData.months, y: Array(chartData.months.length).fill(prediction), type: 'scatter', mode: 'lines', name: 'Predicted Price', line: { color: 'red', dash: 'dot' }},
                            ]}
                            layout={{ title: `Median Price by Month - ${selectedYear}`, xaxis: { title: 'Month' }, yaxis: { title: 'Price (AUD)' }, hovermode: 'closest', autosize: true }}
                            useResizeHandler
                            style={{ width: '100%', height: '500px' }}
                        />
                    )}
                </div>
            </div>
        </div>
    );
}

export default Prediction;