# E-Bike Compare Web Application

This is a web application that allows users to compare electric bikes from various manufacturers.

## Architecture

The application has a modern architecture:

- **Backend**: Flask-based API server that provides data endpoints
- **Frontend**: JavaScript/jQuery client-side application that consumes the API

## Key Features

- View all available e-bikes with images and basic details
- Compare multiple e-bikes side by side
- Filter by manufacturer
- Highlight differences between bikes
- Responsive design works on mobile and desktop

## API Endpoints

- `/api/bikes` - Get all available bikes
- `/api/compare?bike_ids=...` - Get detailed information for specific bikes

## Frontend Pages

- **Home Page** (`/`) - Shows all available bikes in a card layout
- **Compare Page** (`/compare`) - Allows selecting bikes to compare and displays the comparison table

## Development

The application uses:

- Flask for the backend API
- jQuery for frontend functionality
- Bootstrap for responsive styling
- AJAX for asynchronous data loading
- Client-side rendering of all UI elements

## Benefits of the New Architecture

1. **Better Performance**: Client-side rendering reduces server load
2. **Improved Responsiveness**: No full page reloads when selecting bikes
3. **Simpler Backend**: API-only server is easier to maintain
4. **Better Error Handling**: AJAX provides better error handling and retry capabilities 