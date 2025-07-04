import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [dishes, setDishes] = useState([]);

  useEffect(() => {
    fetchRestaurants();
    fetchDishes();
  }, []);

  const fetchRestaurants = async () => {
    try {
      const res = await axios.get('/api/restaurants');
      setRestaurants(res.data);
      setSelectedRestaurant(res.data[0]);
      fetchReviews(res.data[0].id);
    } catch (error) {
      console.error("Error fetching restaurants:", error);
    }
  };

  const fetchReviews = async (restaurantId) => {
    try {
      const res = await axios.get(`/api/reviews/${restaurantId}`);
      setReviews(res.data);
    } catch (error) {
      console.error("Error fetching reviews:", error);
    }
  };

  const fetchDishes = async () => {
    try {
      const res = await axios.get('/api/dishes');
      setDishes(res.data);
    } catch (error) {
      console.error("Error fetching dishes:", error);
    }
  };

  const addRestaurant = async () => {
    const name = prompt('Enter restaurant name:');
    if (name) {
      try {
        await axios.post('/api/restaurants', { name });
        fetchRestaurants();
      } catch (error) {
        console.error("Error adding restaurant:", error);
      }
    }
  };

  const addReview = async () => {
    const user = prompt('Your name:');
    const rating = prompt('Rating (1–5):');
    const comment = prompt('Your review:');
    if (user && comment && selectedRestaurant) {
      try {
        await axios.post('/api/reviews', {
          restaurant_id: selectedRestaurant.id,
          user,
          rating,
          comment,
        });
        fetchReviews(selectedRestaurant.id);
      } catch (error) {
        console.error("Error adding review:", error);
      }
    }
  };

  return (
    <div className="App">
      <header>Tatescape</header>
      <h3>Discover the best restaurants in town</h3>
      <div className="main">
        <div className="left">
          <h3>Restaurants</h3>
          {restaurants.map(r => (
            <div
              key={r.id}
              onClick={() => {
                setSelectedRestaurant(r);
                fetchReviews(r.id);
              }}
              className={selectedRestaurant?.id === r.id ? 'active' : ''}
            >
              {r.name} <span>★{r.rating}</span>
            </div>
          ))}
          <button onClick={addRestaurant}>add restaurant</button>
        </div>

        <div className="middle">
          <h3>Popular Dishes</h3>
          {dishes.map(d => (
            <div key={d.id}>
              <strong>{d.name}</strong> - ${d.price}
              <br />
              {d.description}
              <br />
              ★{d.rating}
              <hr />
            </div>
          ))}
          <button onClick={addReview}>add review</button>
        </div>

        <div className="right">
          <h3>Customer Reviews</h3>
          {reviews.map(r => (
            <div key={r.id}>
              <strong>{r.user}</strong> ★{r.rating}
              <p>{r.comment}</p>
              <hr />
            </div>
          ))}
        </div>
      </div>
      <footer>© 2025 Tatescape. All rights reserved.</footer>
    </div>
  );
}

export default App;