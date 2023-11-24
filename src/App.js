import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [destinationId, setDestinationId] = useState('');
  const [adultsCount, setAdultsCount] = useState('');
  const [childrenCount, setChildrenCount] = useState('');
  const [roomsCount, setRoomsCount] = useState('');
  const [hotels, setHotels] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const payload = {
        srch_destination_id: destinationId,
        srch_adults_cnt: adultsCount,
        srch_children_cnt: childrenCount,
        srch_rm_cnt: roomsCount
      };
  
      const response = await axios.post('http://localhost:5000/recommend', payload);
      console.log("Response from server:", response.data); 

      if (response.data && Array.isArray(response.data.hotel_recommendations)) {
        console.log("Hotel recommendations:", response.data.hotel_recommendations);  // Log the recommendations
        setHotels(response.data.hotel_recommendations);
    }else {
        setHotels([]);
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
        <input 
          type="text" 
          value={destinationId} 
          onChange={(e) => setDestinationId(e.target.value)} 
          placeholder="Destination ID" 
          className="input-field" 
        />
        <input 
          type="number" 
          value={adultsCount} 
          onChange={(e) => setAdultsCount(e.target.value)} 
          placeholder="Number of Adults" 
          className="input-field" 
        />
        <input 
          type="number" 
          value={childrenCount} 
          onChange={(e) => setChildrenCount(e.target.value)} 
          placeholder="Number of Children" 
          className="input-field" 
        />
        <input 
          type="number" 
          value={roomsCount} 
          onChange={(e) => setRoomsCount(e.target.value)} 
          placeholder="Number of Rooms" 
          className="input-field" 
        />
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
