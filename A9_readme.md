# Collaborative Filtering Implementation - Line by Line Explanation

This document provides a detailed explanation of the collaborative filtering implementation in `a9.py`.

## Code Explanation

### Import Statement
```python
import numpy as np
```
- Imports the NumPy library for numerical computations and matrix operations

### Main Function Definition
```python
def collaborative_filtering(ratings_matrix, latent_features=2, iterations=100, learning_rate=0.01, regularization=0.01):
```
- Defines the main function for collaborative filtering
- Parameters:
  - `ratings_matrix`: Input matrix containing user-item ratings
  - `latent_features`: Number of latent features (default: 2)
  - `iterations`: Number of training iterations (default: 100)
  - `learning_rate`: Learning rate for gradient descent (default: 0.01)
  - `regularization`: Regularization parameter (default: 0.01)

### Function Documentation
```python
"""
    Perform collaborative filtering using matrix factorization.
    
    Args:
        ratings_matrix: Input matrix of user-item ratings
        latent_features: Number of latent features (default: 2)
        iterations: Number of training iterations (default: 100)
        learning_rate: Learning rate for gradient descent (default: 0.01)
        regularization: Regularization parameter (default: 0.01)
    
    Returns:
        user_features: Matrix of user latent features
        item_features: Matrix of item latent features
    """
```
- Provides detailed documentation about the function's purpose, parameters, and return values

### Matrix Dimensions
```python
num_users, num_items = ratings_matrix.shape
```
- Extracts the dimensions of the input ratings matrix
- `num_users`: Number of users (rows)
- `num_items`: Number of items (columns)

### Create Observation Mask
```python
observed_mask = (ratings_matrix > 0).astype(float)
```
- Creates a binary mask where 1 represents observed ratings and 0 represents missing ratings
- Used to focus on known ratings during training

### Initialize Feature Matrices
```python
user_features = np.random.normal(0, 0.1, (num_users, latent_features))
item_features = np.random.normal(0, 0.1, (num_items, latent_features))
```
- Initializes user and item feature matrices with random values
- Uses normal distribution with mean 0 and standard deviation 0.1

### Training Loop
```python
for iteration in range(iterations):
```
- Main training loop that runs for specified number of iterations

### Compute Predicted Ratings
```python
predicted_ratings = np.dot(user_features, item_features.T)
```
- Computes predicted ratings by matrix multiplication of user and item features

### Calculate Error Matrix
```python
error_matrix = observed_mask * (ratings_matrix - predicted_ratings)
```
- Computes error between actual and predicted ratings
- Only considers observed ratings (using mask)

### Compute Total Error
```python
total_error = np.sum(error_matrix**2) + regularization * (np.sum(user_features**2) + np.sum(item_features**2))
```
- Calculates total error including regularization term
- First term: squared error of predictions
- Second term: L2 regularization on feature matrices

### Progress Printing
```python
if iteration % 10 == 0:
    print(f"Iteration {iteration}, Total Error: {total_error:.4f}")
```
- Prints progress every 10 iterations

### Update Feature Matrices
```python
user_gradient = learning_rate * (np.dot(error_matrix, item_features) - regularization * user_features)
item_gradient = learning_rate * (np.dot(error_matrix.T, user_features) - regularization * item_features)
user_features += user_gradient
item_features += item_gradient
```
- Computes gradients for both feature matrices
- Updates matrices using gradient descent with regularization

### Example Usage
```python
sample_ratings = np.array([
    [4, 0, 3, 5],
    [5, 4, 0, 2],
    [0, 5, 4, 1],
    [2, 0, 5, 3],
    [3, 2, 1, 0]
])
```
- Creates example ratings matrix
- 5 users × 4 items
- 0 represents missing ratings

### Model Training
```python
user_latent_features, item_latent_features = collaborative_filtering(sample_ratings, latent_features=2, iterations=100)
```
- Trains the model with example data
- Returns learned user and item feature matrices

### Results Display
```python
print("\nUser Latent Features Matrix:")
print(np.round(user_latent_features, 4))
print("\nItem Latent Features Matrix:")
print(np.round(item_latent_features, 4))
```
- Displays learned feature matrices rounded to 4 decimal places

### Matrix Reconstruction
```python
reconstructed_ratings = np.dot(user_latent_features, item_latent_features.T)
```
- Reconstructs the ratings matrix using learned features

### RMSE Calculation
```python
observed_mask = (sample_ratings > 0).astype(float)
error_squared = observed_mask * (sample_ratings - reconstructed_ratings)**2
rmse = np.sqrt(np.sum(error_squared) / np.sum(observed_mask))
```
- Calculates Root Mean Square Error for observed ratings
- Uses mask to consider only known ratings
- Provides measure of prediction accuracy

## Algorithm Overview
This implementation uses matrix factorization for collaborative filtering:
1. Decomposes the ratings matrix into user and item feature matrices
2. Uses gradient descent to learn these features
3. Includes regularization to prevent overfitting
4. Can predict missing ratings using learned features

## Usage
The code can be used to:
- Learn user and item features from ratings data
- Predict missing ratings
- Evaluate prediction accuracy using RMSE
- Handle sparse rating matrices 