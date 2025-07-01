# Feedback.js - MongoDB Feedback Model

## File Location
`server/models/Feedback.js`

## Code Explanation

```javascript
const mongoose = require('mongoose');

const feedbackSchema = new mongoose.Schema({
```
- Imports Mongoose
- Creates new schema for feedback

```javascript
  title: {
    type: String,
    required: [true, 'Title is required'],
    trim: true,
    minlength: [3, 'Title must be at least 3 characters long'],
    maxlength: [100, 'Title cannot exceed 100 characters']
  },
```
- Title field configuration:
  - String type
  - Required field with error message
  - Trims whitespace
  - Length validation (3-100 characters)

```javascript
  description: {
    type: String,
    required: [true, 'Description is required'],
    trim: true,
    minlength: [10, 'Description must be at least 10 characters long'],
    maxlength: [1000, 'Description cannot exceed 1000 characters']
  },
```
- Description field configuration:
  - String type
  - Required field
  - Length validation (10-1000 characters)

```javascript
  category: {
    type: String,
    required: [true, 'Category is required'],
    trim: true
  },
  subCategory: {
    type: String,
    required: [true, 'Sub-category is required'],
    trim: true
  },
  metaCategory: {
    type: String,
    required: [true, 'Meta-category is required'],
    trim: true
  },
```
- Category fields:
  - Main category
  - Sub-category
  - Meta-category
  - All required and trimmed

```javascript
  status: {
    type: String,
    enum: ['open', 'in-progress', 'resolved', 'closed'],
    default: 'open'
  },
```
- Status field:
  - Enumerated values
  - Default value: 'open'
  - Restricted to specific statuses

```javascript
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  }
}, {
  timestamps: true,
  toJSON: { virtuals: true },
  toObject: { virtuals: true }
});
```
- Timestamp fields:
  - Automatic creation timestamp
  - Last update timestamp
- Schema options:
  - Automatic timestamps
  - Virtual field support

```javascript
feedbackSchema.index({ category: 1, subCategory: 1, metaCategory: 1 });
feedbackSchema.index({ createdAt: -1 });
```
- Database indexes for performance:
  - Compound index on categories
  - Descending index on creation date

```javascript
feedbackSchema.pre('save', function(next) {
  this.updatedAt = Date.now();
  next();
});

feedbackSchema.pre('save', function(next) {
  // Additional validation can be added here
  next();
});
```
- Pre-save middleware:
  - Updates timestamp
  - Hook for additional validation

```javascript
feedbackSchema.post('save', function(error, doc, next) {
  if (error.name === 'ValidationError') {
    next(new Error(Object.values(error.errors).map(val => val.message).join(', ')));
  } else if (error.code === 11000) {
    next(new Error('Duplicate entry found'));
  } else {
    next(error);
  }
});
```
- Post-save error handling:
  - Formats validation errors
  - Handles duplicate entries
  - Passes through other errors

```javascript
const Feedback = mongoose.model('Feedback', feedbackSchema);

module.exports = Feedback;
```
- Creates Feedback model
- Exports model for use in application

## Key Points
1. Comprehensive data validation
2. Automatic timestamp management
3. Database indexing for performance
4. Error handling middleware
5. Status management with enum
6. Field length restrictions
7. Required field enforcement
8. Middleware hooks for custom logic 