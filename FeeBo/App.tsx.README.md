# App.tsx - Main Application Component

## File Location
`client/src/App.tsx`

## Code Explanation

```typescript
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
```
- Imports necessary routing components from react-router-dom
- `Router`: Main routing component that enables routing functionality
- `Routes`: Container for all Route components
- `Route`: Individual route component for path matching

```typescript
import Navbar from './components/layout/Navbar';
import HomePage from './pages/HomePage';
import FeedbackPage from './pages/FeedbackPage';
import ExplorePage from './pages/ExplorePage';
```
- Imports all required components and pages
- `Navbar`: Navigation component
- Three main pages: Home, Feedback, and Explore

```typescript
function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
```
- Main App component using functional component syntax
- `Router` wraps entire application to enable routing
- `min-h-screen`: Tailwind class for minimum height of 100vh
- `bg-gray-50`: Light gray background color

```typescript
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/feedback" element={<FeedbackPage />} />
          <Route path="/explore" element={<ExplorePage />} />
        </Routes>
```
- `Navbar` is placed outside Routes to show on all pages
- `Routes` contains all route definitions
- Three routes defined:
  - `/`: Home page (default route)
  - `/feedback`: Feedback submission page
  - `/explore`: Feedback exploration page

```typescript
      </div>
    </Router>
  );
}

export default App;
```
- Closes the main div container
- Exports App component as default export

## Key Points
1. Uses React Router v6 for navigation
2. Implements a basic layout with Navbar and content area
3. Three main routes in the application
4. Tailwind CSS for styling
5. TypeScript for type safety 