# index.js - Express Server Setup

## File Location
`server/index.js`

## Code Explanation

```javascript
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');
const feedbackRoutes = require('./routes/feedback');
```
- Imports required dependencies:
  - `express`: Web framework
  - `mongoose`: MongoDB ODM
  - `cors`: Cross-Origin Resource Sharing middleware
  - `morgan`: HTTP request logger
  - `dotenv`: Environment variable loader
  - Local feedback routes

```javascript
dotenv.config();
const app = express();
```
- Loads environment variables
- Creates Express application instance

```javascript
// Middleware Setup
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
```
- Configures middleware:
  - CORS for cross-origin requests
  - Morgan for request logging
  - JSON parser for request bodies
  - URL-encoded parser for form data

```javascript
app.use((req, res, next) => {
  console.log(`${req.method} ${req.path}`, req.body);
  next();
});
```
- Custom middleware for request logging
- Logs method, path, and request body
- Calls next() to continue request processing

```javascript
const MONGODB_URI = 'mongodb+srv://ankeshkr0921:kae8OXCW9x0Bgj5c@feebo.bttbi1o.mongodb.net/feebo?retryWrites=true&w=majority';

const connectDB = async () => {
  try {
    const options = {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      serverSelectionTimeoutMS: 30000,
      socketTimeoutMS: 45000
    };

    console.log('Attempting to connect to MongoDB Atlas...');
    const conn = await mongoose.connect(MONGODB_URI, options);
    console.log(`MongoDB Atlas Connected: ${conn.connection.host}`);
  } catch (error) {
    console.error('MongoDB connection error:', {
      name: error.name,
      message: error.message,
      code: error.code,
      codeName: error.codeName,
      stack: error.stack
    });
    
    console.log('Retrying connection in 5 seconds...');
    setTimeout(connectDB, 5000);
  }
};
```
- MongoDB connection setup:
  - Connection string for MongoDB Atlas
  - Connection options for reliability
  - Error handling with retry mechanism
  - Detailed error logging

```javascript
connectDB();

app.use('/api/feedback', feedbackRoutes);

app.get('/', (req, res) => {
  res.json({ message: 'FeeBo API is running' });
});
```
- Initiates database connection
- Sets up feedback routes under '/api/feedback'
- Basic health check endpoint

```javascript
app.use((err, req, res, next) => {
  console.error('Error details:', {
    message: err.message,
    name: err.name,
    code: err.code,
    stack: err.stack,
    body: req.body
  });
  
  res.status(500).json({ 
    message: 'Something went wrong!',
    error: err.message,
    details: process.env.NODE_ENV === 'development' ? err.stack : undefined
  });
});
```
- Global error handling middleware
- Detailed error logging
- Environment-aware error responses

```javascript
const PORT = process.env.PORT || 5001;

const server = app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```
- Server startup on specified port
- Default port: 5001

```javascript
mongoose.connection.on('connected', () => {
  console.log('Mongoose connected to MongoDB Atlas');
});

mongoose.connection.on('error', (err) => {
  console.error('Mongoose connection error:', {
    name: err.name,
    message: err.message,
    code: err.code,
    codeName: err.codeName
  });
});

mongoose.connection.on('disconnected', () => {
  console.log('Mongoose disconnected');
  setTimeout(connectDB, 5000);
});
```
- MongoDB connection event handlers:
  - Connected event logging
  - Error event logging
  - Disconnection handling with reconnection attempt

```javascript
process.on('SIGINT', async () => {
  try {
    await mongoose.connection.close();
    server.close(() => {
      console.log('Server closed. Database instance disconnected');
      process.exit(0);
    });
  } catch (err) {
    console.error('Error during shutdown:', err);
    process.exit(1);
  }
});
```
- Graceful shutdown handling:
  - Closes database connection
  - Shuts down server
  - Handles shutdown errors

## Key Points
1. Complete Express server setup
2. MongoDB Atlas connection with retry mechanism
3. Comprehensive middleware configuration
4. Robust error handling
5. Graceful shutdown implementation
6. Environment-aware configuration
7. Detailed logging throughout
8. RESTful API structure 