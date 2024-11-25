document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication(); // Check if the user is logged in and fetch places if authenticated

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            await loginUser(email, password);
        });
    }

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            fetchPlaces(selectedPrice);
        });
    }
});

async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
            credentials: 'include',
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Login successful:', data);

            const expiry = new Date();
            expiry.setTime(expiry.getTime() + 24 * 60 * 60 * 1000); // 1 day expiry
            document.cookie = `token=${data.access_token}; path=/; expires=${expiry.toUTCString()}; SameSite=None; Secure`;

            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            alert(`Login failed: ${errorData.error || 'Invalid credentials'}`);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again later.');
    }
}

async function fetchPlaces(maxPrice = '') {
    const url = `http://127.0.0.1:5000/api/v1/places?max_price=${maxPrice}`;
    try {
        const response = await fetch(url, {
            method: 'GET',
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error('Failed to fetch places. Check your authentication.');
        }

        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error('Error fetching places:', error);
        alert('Unable to fetch places. Please check your authentication.');
    }
}

function submitReview() {
    const reviewText = document.getElementById('review-text').value;
    const rating = document.getElementById('rating').value;

    const reviewData = {
        text: reviewText,
        rating: parseInt(rating),
    };

    fetch('http://127.0.0.1:5000/api/v1/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(reviewData),
        credentials: 'include'
    })
        .then(response => {
            if (response.ok) {
                alert('Review added successfully!');
                window.location.reload();
            } else {
                alert('Error adding review');
            }
        })
        .catch(error => console.error('Error submitting review:', error));
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!loginLink) {
        console.error('Login link element not found in the DOM');
        return;
    }
    

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces();
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    if (places.length === 0) {
        placesList.innerHTML = '<p>No places available.</p>';
    }

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>${place.description}</p>
            <p>Price: $${place.price}</p>
            <button class="details-button" onclick="viewDetails('${place.id}')">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

function viewDetails(placeId) {
    window.location.href = `place.html?place_id=${placeId}`;
}
