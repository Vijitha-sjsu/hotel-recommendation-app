import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [userLocationCity, setUserLocationCity] = useState('');
  const [origDestinationDistance, setOrigDestinationDistance] = useState('');
  const [destinationId, setDestinationId] = useState('');
  const [adultsCount, setAdultsCount] = useState('');
  const [childrenCount, setChildrenCount] = useState('');
  const [roomsCount, setRoomsCount] = useState('');
  const [hotelCountry, setHotelCountry] = useState('');
  const [hotels, setHotels] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        user_location_city: userLocationCity,
        orig_destination_distance: origDestinationDistance,
        srch_destination_id: destinationId,
        srch_adults_cnt: adultsCount,
        srch_children_cnt: childrenCount,
        srch_rm_cnt: roomsCount,
        hotel_country: hotelCountry
      };

      const response = await axios.post('http://localhost:5000/predict', payload);
      
      if (response.data.error) {
        console.error("Error from server:", response.data.error);
      } else {
        console.log("Response from server:", response.data);

        if (response.data && Array.isArray(response.data.top5_recommendations)) {
          console.log("Top 5 hotel recommendations:", response.data.top5_recommendations);
          setHotels(response.data.top5_recommendations);
        } else {
          setHotels([]);
        }
      }
    } catch (error) {
      console.error('Error fetching hotel recommendations:', error);
      setHotels([]);
    }
  };

  return (
    <div className="app-container">
      <h1>Hotel Recommendation</h1>
      <form onSubmit={handleSubmit} className="form-container">
        <div className = "input-row">
        <label className='input-label'>User Location City ID:</label>
        <input 
          type="text" 
          value={userLocationCity} 
          onChange={(e) => setUserLocationCity(e.target.value)} 
          className="input-field" 
        />
        </div>
        <div className = "input-row">
        <label className='input-label'>Original Destination Distance:</label>
        <input 
          type="text" 
          value={origDestinationDistance} 
          onChange={(e) => setOrigDestinationDistance(e.target.value)} 
          className="input-field" 
        />
        </div>
        <div className = "input-row">
        <label className='input-label'>Search Destination ID:</label>
        <input 
          type="text" 
          value={destinationId} 
          onChange={(e) => setDestinationId(e.target.value)} 
          className="input-field" 
        />
        </div>
        <div className = "input-row">
        <label className='input-label'>Number of Adults:</label>
        <input 
          type="number" 
          value={adultsCount} 
          onChange={(e) => setAdultsCount(e.target.value)} 
          className="input-field" 
        />
        </div>
        <div className = "input-row">
        <label className='input-label'>Number of Children:</label>
        <input 
          type="number" 
          value={childrenCount} 
          onChange={(e) => setChildrenCount(e.target.value)} 
          className="input-field" 
        />
        </div>
         <div className = "input-row">
        <label className='input-label'>Number of Rooms:</label>
        <input 
          type="number" 
          value={roomsCount} 
          onChange={(e) => setRoomsCount(e.target.value)} 
          className="input-field" 
        />
        </div>
         <div className = "input-row">
        <label className='input-label'>Hotel Country ID:</label>
        <input 
          type="text" 
          value={hotelCountry} 
          onChange={(e) => setHotelCountry(e.target.value)} 
          className="input-field" 
        />
        </div>
        <button type="submit" className="submit-button">Get Recommendations</button>
      </form>

      {hotels.length > 0 && (
        <ul className="hotels-list">
          {hotels.map((hotelClusterId, index) => (
            <li key={index}>Hotel Cluster ID: {hotelClusterId}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default App;
