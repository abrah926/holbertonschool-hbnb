document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display places
    fetchPlaces();

    // Filter places by price
    const priceFilter = document.getElementById('price-filter');
    priceFilter.addEventListener('change', () => {
        fetchPlaces(priceFilter.value);
    });

    // Add review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (event) => {
            event.preventDefault();
            submitReview();
        });
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('.login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Extract email and password from form inputs
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // Call the login function
            await loginUser(email, password);
        });
    }
});


function fetchPlaces(maxPrice = '') {
    const url = `http://127.0.0.1:5000/api/v1/places?max_price=${maxPrice}`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const placesList = document.getElementById('places-list');
            placesList.innerHTML = ''; // Clear existing places
            data.forEach(place => {
                const placeCard = `
                    <div class="place-card">
                        <h2>${place.title}</h2>
                        <p>Price: $${place.price}</p>
                        <button class="details-button" onclick="viewDetails('${place.id}')">View Details</button>
                    </div>
                `;
                placesList.insertAdjacentHTML('beforeend', placeCard);
            });
        })
        .catch(error => console.error('Error fetching places:', error));
}

function viewDetails(placeId) {
    window.location.href = `place.html?place_id=${placeId}`;
}

function submitReview() {
    const reviewText = document.getElementById('review').value;
    const rating = document.getElementById('rating').value;

    const reviewData = {
        text: reviewText,
        rating: parseInt(rating),
    };

    fetch('http://127.0.0.1:5000/api/v1/reviews', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(reviewData)
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

async function loginUser(email, password) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (response.ok) {
            const data = await response.json();
            
            // Store the JWT token in a cookie
            document.cookie = `token=${data.access_token}; path=/; secure`;

            // Redirect to the main page
            window.location.href = 'index.html';
        } else {
            // Display an error message if the login fails
            const errorData = await response.json();
            alert(`Login failed: ${errorData.error || 'Invalid credentials'}`);
        }
    } catch (error) {
        console.error('Error during login:', error);
        alert('An error occurred. Please try again later.');
    }
}

