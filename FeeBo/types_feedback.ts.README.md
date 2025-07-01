# feedback.ts - Type Definitions and Categories

## File Location
`client/src/types/feedback.ts`

## Code Explanation

```typescript
export interface Feedback {
  _id: string;
  title: string;
  description: string;
  category: string;
  subCategory: string;
  status: 'open' | 'in-progress' | 'resolved' | 'closed';
  createdAt: string;
  updatedAt: string;
}
```
- Defines the Feedback interface
- Properties:
  - `_id`: MongoDB document ID
  - `title`: Feedback title
  - `description`: Detailed feedback content
  - `category`: Main category
  - `subCategory`: Sub-category
  - `status`: Union type for feedback status
  - `createdAt`: Timestamp of creation
  - `updatedAt`: Timestamp of last update

```typescript
export const CATEGORIES = [
  {
    name: "Electronics & Gadgets",
    subCategories: [
      { name: "Mobile Phones" },
      { name: "Laptops" },
      { name: "Tablets" },
      { name: "Wearables" },
      { name: "Audio Devices" }
    ]
  },
```
- First category group: Electronics & Gadgets
- Contains 5 sub-categories related to electronic devices

```typescript
  {
    name: "Reading & Learning",
    subCategories: [
      { name: "Books" },
      { name: "Online Courses" },
      { name: "Tutorials" },
      { name: "Documentation" },
      { name: "Learning Platforms" }
    ]
  },
```
- Second category group: Reading & Learning
- Contains 5 sub-categories related to educational content

```typescript
  {
    name: "Entertainment",
    subCategories: [
      { name: "Movies" },
      { name: "Web Series" },
      { name: "TV Shows" },
      { name: "Music" },
      { name: "Games" }
    ]
  },
```
- Third category group: Entertainment
- Contains 5 sub-categories related to entertainment media

```typescript
  {
    name: "Tools & Apps",
    subCategories: [
      { name: "Mobile Apps" },
      { name: "Desktop Software" },
      { name: "Web Apps" },
      { name: "AI Tools" },
      { name: "Browser Extensions" }
    ]
  },
```
- Fourth category group: Tools & Apps
- Contains 5 sub-categories related to software applications

```typescript
  {
    name: "General Suggestions",
    subCategories: [
      { name: "Website Feedback" },
      { name: "Service Feedback" },
      { name: "Feature Requests" },
      { name: "Bug Reports" },
      { name: "Other" }
    ]
  }
];
```
- Fifth category group: General Suggestions
- Contains 5 sub-categories for general feedback types

## Key Points
1. TypeScript interface defines the shape of feedback data
2. Status field uses union type for strict value control
3. Hierarchical category structure
   - 5 main categories
   - Each main category has 5 sub-categories
4. Categories are exported as a constant array
5. Each category and sub-category has a name property
6. Structure allows for easy extension of categories
7. Used throughout the application for type safety and data structure 