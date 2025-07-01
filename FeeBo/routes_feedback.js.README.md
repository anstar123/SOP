# feedback.js - Feedback Routes

## File Location
`server/routes/feedback.js`

## Code Explanation

```javascript
const express = require('express');
const router = express.Router();
const { getAllFeedback, createFeedback } = require('../controllers/feedback');
```
- Imports required dependencies:
  - Express router
  - Controller functions for feedback operations

```javascript
// Get all feedback
router.get('/', getAllFeedback);
```
- GET route for retrieving all feedback
- Path: `/api/feedback`
- Handled by `getAllFeedback` controller

```javascript
// Create new feedback
router.post('/', createFeedback);
```
- POST route for creating new feedback
- Path: `/api/feedback`
- Handled by `createFeedback` controller

```javascript
module.exports = router;
```
- Exports router for use in main application

## Key Points
1. RESTful route structure
2. Separation of concerns:
   - Routes only define endpoints
   - Logic handled in controllers
3. Two main endpoints:
   - GET for retrieving feedback
   - POST for creating feedback
4. Clean and minimal route definitions
5. Modular design pattern 