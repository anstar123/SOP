# FeedbackForm.tsx - Feedback Submission Component

## File Location
`client/src/components/feedback/FeedbackForm.tsx`

## Code Explanation

```typescript
import { useState, FormEvent } from 'react';
import { CATEGORIES } from '../../types/feedback';
```
- Imports React hooks for state management
- Imports predefined categories from types file

```typescript
const API_URL = 'http://localhost:5000/api/feedback';
```
- Defines backend API endpoint for feedback submission

```typescript
const FeedbackForm = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedMainCategory, setSelectedMainCategory] = useState(CATEGORIES[0].name);
  const [selectedSubCategory, setSelectedSubCategory] = useState(CATEGORIES[0].subCategories[0].name);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
```
- Form state management using useState hooks
- Tracks form fields: title, description, categories
- Manages form submission state and errors
- Initializes with first category and subcategory

```typescript
  const currentCategory = CATEGORIES.find(cat => cat.name === selectedMainCategory);

  const handleMainCategoryChange = (categoryName: string) => {
    setSelectedMainCategory(categoryName);
    const category = CATEGORIES.find(cat => cat.name === categoryName);
    if (category) {
      setSelectedSubCategory(category.subCategories[0].name);
    }
  };
```
- Finds current category object based on selection
- Handles main category changes
- Automatically updates subcategory when main category changes

```typescript
  const clearForm = () => {
    setTitle('');
    setDescription('');
    setSelectedMainCategory(CATEGORIES[0].name);
    setSelectedSubCategory(CATEGORIES[0].subCategories[0].name);
    setError(null);
  };
```
- Utility function to reset form state
- Called after successful submission

```typescript
  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
```
- Form submission handler
- Prevents default form behavior
- Resets error state and sets loading state

```typescript
    // Client-side validation
    if (title.length < 3) {
      setError('Title must be at least 3 characters long');
      setIsSubmitting(false);
      return;
    }

    if (description.length < 10) {
      setError('Description must be at least 10 characters long');
      setIsSubmitting(false);
      return;
    }
```
- Client-side validation rules
- Checks minimum length requirements
- Sets appropriate error messages

```typescript
    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          title,
          description,
          category: selectedMainCategory,
          subCategory: selectedSubCategory
        }),
      });
```
- Makes POST request to backend API
- Sends form data as JSON
- Includes all form fields in request body

```typescript
      const data = await response.json();

      if (response.ok) {
        clearForm();
        alert('Feedback submitted successfully!');
        window.location.reload();
      } else {
        setError(data.message || 'Failed to submit feedback. Please try again.');
      }
```
- Handles API response
- Clears form and shows success message on success
- Sets error message on failure

```typescript
    } catch (error) {
      console.error('Error submitting feedback:', error);
      setError('Network error. Please check your connection and try again.');
    } finally {
      setIsSubmitting(false);
    }
```
- Error handling for network failures
- Always resets submission state

## Form Render Section
The form includes:
1. Category dropdowns
   - Main category selector
   - Dynamic subcategory selector
2. Title input
   - Character count display
   - Minimum length validation
3. Description textarea
   - Character count display
   - Minimum length validation
4. Submit button
   - Disabled during submission
   - Shows loading state

## Key Points
1. Uses TypeScript for type safety
2. Implements form validation
3. Handles API integration
4. Manages loading and error states
5. Dynamic category selection
6. Character count tracking
7. Form state management with React hooks
``` 