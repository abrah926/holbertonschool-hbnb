# HBnB Project

HBnB is a web application designed to showcase places for users to explore, view details, and add reviews. This project involves creating multiple HTML pages, implementing API interactions, and dynamically updating content using JavaScript. The application includes authentication, place listing, detailed views, and review submission functionalities.

## Features

1. **User Authentication**

   - Login functionality with JWT token stored in cookies.
   - Logout functionality.
   - Login link is hidden for authenticated users.

2. **Place Listing**

   - Dynamic display of available places fetched from an API.
   - Price filtering functionality.

3. **Place Details**

   - View detailed information about a specific place.
   - Includes title, description, price, amenities, and reviews.

4. **Review Submission**
   - Authenticated users can add reviews to specific places.
   - Reviews are displayed dynamically below place details.

## Project Structure

project/ │ ├── index.html # Main page displaying the list of places ├── place.html # Page showing details of a specific place ├── login.html # Login page for user authentication ├── add_review.html # Form for adding a new review │ ├── css/ │ └── styles.css # Styling for the entire project │ ├── images/ # Image assets │ ├── logo.png # Logo for the website │ ├── icon.png # Favicon │ └── other_images/ # Any other images used in the project │ ├── scripts.js # Main JavaScript file handling dynamic functionality │ └── README.md # Project documentation

## Tasks

**1. Login Page**

- **Objective**: Create a login form for user authentication and validate user credentials using the API.
- **Implementation**:
  - **File**: `login.html`
  - **JavaScript**:
    - `loginUser(email, password)` sends a POST request to `/auth/login`.
    - JWT token is stored in cookies.
    - Redirects to `index.html` upon successful login.

**2. Place Listing**

- **Objective**: Display a list of all available places dynamically fetched from the API and implement price-based filtering.
- **Implementation**:
  - **File**: `index.html`
  - **JavaScript**:
    - `fetchPlaces(maxPrice)` fetches places using the API.
    - Places are displayed dynamically using `displayPlaces()`.
    - Filtering is implemented through a dropdown menu in the UI.

**3. Place Details**

- **Objective**: Show detailed information about a specific place, including title, description, price, amenities, and reviews. Allow authenticated users to add reviews.
- **Implementation**:
  - **File**: `place.html`
  - **JavaScript**:
    - `fetchPlaceDetails(placeId)` fetches details for the selected place.
    - Reviews are fetched using `fetchReviews(placeId)`.
    - `addReview()` allows authenticated users to submit reviews.

**4. Add Review**

- **Objective**: Create a form for users to add reviews for a place with input validation.
- **Implementation**:
  - **File**: `add_review.html`
  - **JavaScript**:
    - Form submission triggers `addReview()` function.
    - Sends a POST request to the `/reviews` endpoint.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/username/hbnb.git
   cd hbnb

    Run a Local HTTP Server Use Python's built-in HTTP server to serve the files locally:

    python3 -m http.server

    Access the app at http://127.0.0.1:8000.

    API Setup Ensure your backend API is running at http://127.0.0.1:5000. Update scripts.js if the API base URL changes.

    Dependencies
        Ensure your API supports CORS.
        Install necessary Python libraries for your backend, such as Flask and Flask-JWT-Extended.
   ```

API Endpoints

Authentication

    POST /auth/login
        Body: { "email": "user@example.com", "password": "password" }
        Response: { "access_token": "JWT_TOKEN" }

Places

    GET /places/
        Query Params: ?max_price=50
        Response: List of places.

    GET /places/<place_id>
        Response: Details of a specific place.

Reviews

    GET /places/<place_id>/reviews
        Response: List of reviews for a place.

    POST /places/<place_id>/reviews
        Body: { "text": "Great place!", "rating": 5 }
        Requires authentication.

Testing Instructions

    Login Page
        Test with valid and invalid credentials.
        Verify JWT token is stored in cookies.

    Place Listing
        Ensure places are displayed dynamically.
        Test price filtering functionality.

    Place Details
        Navigate to place.html?id=<place_id>.
        Verify detailed information is displayed.
        Ensure reviews are fetched dynamically.

    Review Submission
        Log in and add a review to a place.
        Ensure the review appears in the reviews section.

Contributing

    Fork the repository.
    Create a feature branch:

git checkout -b feature/new-feature

Commit your changes:

git commit -m "Add new feature"

Push to the branch:

    git push origin feature/new-feature

    Submit a pull request.

License

This project is licensed under the MIT License. See LICENSE for details.

GPT

Here’s the updated README.md with an Authors section added:

# HBnB Project

HBnB is a web application designed to showcase places for users to explore, view details, and add reviews. This project involves creating multiple HTML pages, implementing API interactions, and dynamically updating content using JavaScript. The application includes authentication, place listing, detailed views, and review submission functionalities.

## Features

1. **User Authentication**

   - Login functionality with JWT token stored in cookies.
   - Logout functionality.
   - Login link is hidden for authenticated users.

2. **Place Listing**

   - Dynamic display of available places fetched from an API.
   - Price filtering functionality.

3. **Place Details**

   - View detailed information about a specific place.
   - Includes title, description, price, amenities, and reviews.

4. **Review Submission**
   - Authenticated users can add reviews to specific places.
   - Reviews are displayed dynamically below place details.

## Project Structure

project/ │ ├── index.html # Main page displaying the list of places ├── place.html # Page showing details of a specific place ├── login.html # Login page for user authentication ├── add_review.html # Form for adding a new review │ ├── css/ │ └── styles.css # Styling for the entire project │ ├── images/ # Image assets │ ├── logo.png # Logo for the website │ ├── icon.png # Favicon │ └── other_images/ # Any other images used in the project │ ├── scripts.js # Main JavaScript file handling dynamic functionality │ └── README.md # Project documentation

## Tasks

**1. Login Page**

- **Objective**: Create a login form for user authentication and validate user credentials using the API.
- **Implementation**:
  - **File**: `login.html`
  - **JavaScript**:
    - `loginUser(email, password)` sends a POST request to `/auth/login`.
    - JWT token is stored in cookies.
    - Redirects to `index.html` upon successful login.

**2. Place Listing**

- **Objective**: Display a list of all available places dynamically fetched from the API and implement price-based filtering.
- **Implementation**:
  - **File**: `index.html`
  - **JavaScript**:
    - `fetchPlaces(maxPrice)` fetches places using the API.
    - Places are displayed dynamically using `displayPlaces()`.
    - Filtering is implemented through a dropdown menu in the UI.

**3. Place Details**

- **Objective**: Show detailed information about a specific place, including title, description, price, amenities, and reviews. Allow authenticated users to add reviews.
- **Implementation**:
  - **File**: `place.html`
  - **JavaScript**:
    - `fetchPlaceDetails(placeId)` fetches details for the selected place.
    - Reviews are fetched using `fetchReviews(placeId)`.
    - `addReview()` allows authenticated users to submit reviews.

**4. Add Review**

- **Objective**: Create a form for users to add reviews for a place with input validation.
- **Implementation**:
  - **File**: `add_review.html`
  - **JavaScript**:
    - Form submission triggers `addReview()` function.
    - Sends a POST request to the `/reviews` endpoint.

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/username/hbnb.git
   cd hbnb

    Run a Local HTTP Server Use Python's built-in HTTP server to serve the files locally:

    python3 -m http.server

    Access the app at http://127.0.0.1:8000.

    API Setup Ensure your backend API is running at http://127.0.0.1:5000. Update scripts.js if the API base URL changes.

    Dependencies
        Ensure your API supports CORS.
        Install necessary Python libraries for your backend, such as Flask and Flask-JWT-Extended.
   ```

API Endpoints

Authentication

    POST /auth/login
        Body: { "email": "user@example.com", "password": "password" }
        Response: { "access_token": "JWT_TOKEN" }

Places

    GET /places/
        Query Params: ?max_price=50
        Response: List of places.

    GET /places/<place_id>
        Response: Details of a specific place.

Reviews

    GET /places/<place_id>/reviews
        Response: List of reviews for a place.

    POST /places/<place_id>/reviews
        Body: { "text": "Great place!", "rating": 5 }
        Requires authentication.

Testing Instructions

    Login Page
        Test with valid and invalid credentials.
        Verify JWT token is stored in cookies.

    Place Listing
        Ensure places are displayed dynamically.
        Test price filtering functionality.

    Place Details
        Navigate to place.html?id=<place_id>.
        Verify detailed information is displayed.
        Ensure reviews are fetched dynamically.

    Review Submission
        Log in and add a review to a place.
        Ensure the review appears in the reviews section.

Contributing

    Fork the repository.
    Create a feature branch:

git checkout -b feature/new-feature

Commit your changes:

git commit -m "Add new feature"

Push to the branch:

    git push origin feature/new-feature

    Submit a pull request.

License

This project is licensed under the MIT License. See LICENSE for details.

Authors

    Abraham Vidal - Abrah926
