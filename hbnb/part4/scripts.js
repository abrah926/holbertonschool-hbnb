document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Get form data
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            // Call the login function
            await loginUser(email, password);
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
            credentials: 'include', // Include cookies in the request
        });

        if (response.ok) {
            const data = await response.json();
            console.log('Login successful:', data);

            // Store the token in a cookie manually (for debugging or backup)
            document.cookie = `token=${data.access_token}; path=/; SameSite=None; Secure`;


            // Redirect to the main page
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
function fetchPlaces(maxPrice = '') {
    const url = `http://127.0.0.1:5000/api/v1/places?max_price=${maxPrice}`;
    fetch(url, { credentials: 'include' }) // Include cookies in the request
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
        credentials: 'include' // Include cookies in the request
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
