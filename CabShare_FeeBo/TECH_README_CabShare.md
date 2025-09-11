# CabShare - Technical Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Tech Stack](#tech-stack)
3. [Architecture](#architecture)
4. [Key Features Implementation](#key-features-implementation)
5. [Database Design](#database-design)
6. [Authentication System](#authentication-system)
7. [File Structure & Code Explanation](#file-structure--code-explanation)
8. [Interview Talking Points](#interview-talking-points)

---

## Project Overview

**CabShare** is a ride-sharing Android application designed for IIT Patna students to share cabs for travel between the campus and railway stations/airports. The app facilitates efficient transportation coordination among students.

### Core Features
- **Ride Management**: Create, join, and manage cab rides
- **Ride History**: Track completed rides with detailed information
- **In-Ride Chat**: Real-time messaging during rides
- **Microsoft Authentication**: Secure login using institutional email
- **Real-time Updates**: Live data synchronization across devices

---

## Tech Stack

### Frontend (Android)
- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Architecture**: MVVM (Model-View-ViewModel)
- **Navigation**: Navigation Compose
- **State Management**: StateFlow + Compose State

### Backend & Database
- **Database**: Firebase Firestore (NoSQL)
- **Authentication**: Microsoft Authentication Library (MSAL)
- **Real-time**: Firestore Real-time Listeners
- **Cloud Functions**: Firebase Functions (TypeScript)

### Development Tools
- **Build System**: Gradle
- **Dependency Injection**: Manual (Factory Pattern)
- **Local Storage**: DataStore Preferences
- **Background Tasks**: WorkManager

---

## Architecture

### MVVM Pattern Implementation

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  ViewModel Layer │    │  Data Layer     │
│   (Compose)     │◄──►│   (ViewModels)   │◄──►│  (Repositories) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Screens       │    │   StateFlow      │    │   Firebase      │
│   Components    │    │   Coroutines     │    │   Firestore     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Why This Architecture?

1. **Separation of Concerns**: UI logic separated from business logic
2. **Testability**: ViewModels can be unit tested independently
3. **Lifecycle Awareness**: ViewModels survive configuration changes
4. **Reactive Programming**: StateFlow provides reactive data streams
5. **Scalability**: Easy to add new features without affecting existing code

---

## Key Features Implementation

### 1. Ride History Feature

#### Purpose
Allows users to view their completed rides, track travel history, and manage past ride information.

#### Technical Implementation

**Data Model** (`RideHistory.kt`):
```kotlin
data class RideHistory(
    var rideId: String = "",
    val source: String = "",
    val destination: String = "",
    val dateTime: Date = Date(),
    val maxPassengers: Int = 4,
    val creator: String = "",
    val creatorEmail: String = "",
    val direction: RideDirection = RideDirection.FROM_IITP,
    val notes: String = "",
    val passengers: List<UserProfile> = emptyList(),
    val trainNumber: String = "",
    val trainName: String = "",
    val flightNumber: String = "",
    val flightName: String = "",
    val completionStatus: RideCompletionStatus = RideCompletionStatus.COMPLETED,
    val completedAt: Date = Date(),
    val deletedByUsers: List<String> = emptyList() // Soft delete mechanism
)
```

**Key Design Decisions**:
- **Soft Delete**: Instead of permanently deleting rides, we maintain a `deletedByUsers` list
- **Completion Status**: Tracks whether rides were completed or cancelled
- **Transportation Details**: Stores train/flight information for context

**Repository Pattern** (`RideHistoryRepository.kt`):
```kotlin
interface RideHistoryRepository {
    suspend fun getUserRideHistory(userEmail: String): Flow<List<RideHistory>>
    suspend fun addToHistory(rideHistory: RideHistory)
    suspend fun deleteFromHistory(rideId: String, userEmail: String)
    suspend fun getRideHistory(rideId: String): RideHistory?
    suspend fun getRideHistoryBetweenDates(startDate: Date, endDate: Date): List<RideHistory>
}
```

**Why Repository Pattern?**
- **Abstraction**: Hides data source implementation details
- **Testability**: Easy to mock for unit testing
- **Flexibility**: Can switch from Firestore to other databases
- **Single Responsibility**: Each repository handles one data domain

**ViewModel** (`RideHistoryViewModel.kt`):
```kotlin
class RideHistoryViewModel(
    private val repository: RideHistoryRepository,
    private val userEmail: String
) : ViewModel() {
    private val _rideHistory = MutableStateFlow<List<RideHistory>>(emptyList())
    val rideHistory: StateFlow<List<RideHistory>> = _rideHistory
    
    fun loadUserRideHistory() {
        viewModelScope.launch {
            repository.getUserRideHistory(userEmail)
                .catch { e -> _error.value = "Failed to load: ${e.message}" }
                .collect { history -> _rideHistory.value = history }
        }
    }
}
```

**Why StateFlow?**
- **Reactive**: Automatically updates UI when data changes
- **Lifecycle Aware**: Survives configuration changes
- **Type Safe**: Compile-time type checking
- **Hot Stream**: Always has a current value

**UI Implementation** (`RideHistoryScreen.kt`):
```kotlin
@Composable
fun RideHistoryScreen(navController: NavController, authViewModel: AuthViewModel) {
    val userInfo by authViewModel.userInfo.collectAsState()
    val rideHistoryViewModel = viewModel<RideHistoryViewModel>(
        factory = RideHistoryViewModel.provideFactory(userEmail = userInfo?.email ?: "")
    )
    val rideHistory by rideHistoryViewModel.rideHistory.collectAsState()
    
    LaunchedEffect(userInfo) {
        userInfo?.let { rideHistoryViewModel.loadUserRideHistory() }
    }
    
    LazyColumn {
        items(rideHistory) { ride ->
            RideHistoryCard(ride = ride, onDeleteClick = { /* ... */ })
        }
    }
}
```

**Key UI Features**:
- **Lazy Loading**: Uses LazyColumn for efficient scrolling
- **Real-time Updates**: Automatically reflects data changes
- **Error Handling**: Shows retry options on failures
- **Empty States**: User-friendly messages when no data exists

### 2. In-Ride Chat Feature

#### Purpose
Enables real-time communication between passengers during rides for coordination and updates.

#### Technical Implementation

**Data Model** (`ChatMessage.kt`):
```kotlin
data class ChatMessage(
    val messageId: String = "",
    val rideId: String = "",
    val senderEmail: String = "",
    val senderName: String = "",
    val message: String = "",
    val timestamp: Date = Date(),
    val deletedByUsers: List<String> = emptyList() // Soft delete
)
```

**Repository Implementation** (`FirestoreChatRepositoryImpl.kt`):
```kotlin
class FirestoreChatRepositoryImpl : ChatRepository {
    private val firestore = FirebaseFirestore.getInstance()
    private val chatCollection = firestore.collection("chats")
    
    override fun observeMessages(rideId: String, userEmail: String): Flow<List<ChatMessage>> {
        return chatCollection
            .whereEqualTo("rideId", rideId)
            .orderBy("timestamp", Query.Direction.ASCENDING)
            .snapshots() // Real-time listener
            .map { snapshot ->
                snapshot.documents.mapNotNull { doc ->
                    // Filter out deleted messages for this user
                    val deletedByUsers = doc.get("deletedByUsers") as? List<String> ?: emptyList()
                    if (deletedByUsers.contains(userEmail)) return@mapNotNull null
                    
                    ChatMessage(/* convert document to ChatMessage */)
                }
            }
    }
}
```

**Why Real-time Listeners?**
- **Instant Updates**: Messages appear immediately across all devices
- **Offline Support**: Firestore handles offline scenarios automatically
- **Efficient**: Only sends changed data, not full snapshots
- **Scalable**: Handles multiple concurrent users

**ViewModel** (`ChatViewModel.kt`):
```kotlin
class ChatViewModel(
    private val repository: ChatRepository,
    private val userEmail: String,
    private val userName: String
) : ViewModel() {
    private val _messages = MutableStateFlow<List<ChatMessage>>(emptyList())
    val messages: StateFlow<List<ChatMessage>> = _messages
    
    fun startObservingMessages(rideId: String) {
        viewModelScope.launch {
            repository.observeMessages(rideId, userEmail)
                .collect { messages -> _messages.value = messages }
        }
    }
    
    fun sendMessage(text: String) {
        viewModelScope.launch {
            val message = ChatMessage(
                rideId = currentRideId,
                senderEmail = userEmail,
                senderName = userName,
                message = text,
                timestamp = Date()
            )
            repository.sendMessage(message)
        }
    }
}
```

**UI Implementation** (`ChatScreen.kt`):
```kotlin
@Composable
fun ChatScreen(ride: Ride, userEmail: String, userName: String) {
    val viewModel: ChatViewModel = viewModel(factory = ChatViewModel.Factory(userEmail, userName))
    val messages by viewModel.messages.collectAsState()
    val listState = rememberLazyListState()
    
    LaunchedEffect(ride.rideId) {
        viewModel.startObservingMessages(ride.rideId)
    }
    
    // Auto-scroll to bottom when new messages arrive
    LaunchedEffect(messages) {
        if (messages.isNotEmpty()) {
            listState.animateScrollToItem(messages.size - 1)
        }
    }
    
    LazyColumn(state = listState) {
        items(messages) { message ->
            MessageBubble(message = message, isCurrentUser = message.senderEmail == userEmail)
        }
    }
}
```

**Key Features**:
- **Real-time Messaging**: Instant message delivery
- **Auto-scroll**: Automatically scrolls to new messages
- **Message Bubbles**: Different styling for sent vs received messages
- **Soft Delete**: Users can delete messages for themselves
- **Pagination**: Loads messages in batches for performance

---

## Database Design

### Firestore Collections

#### 1. `rideHistory` Collection
```json
{
  "rideId": "auto-generated-id",
  "source": "IIT Patna",
  "destination": "Patna Junction",
  "dateTime": "2024-01-15T10:30:00Z",
  "maxPassengers": 4,
  "creator": "John Doe",
  "creatorEmail": "john@iitp.ac.in",
  "direction": "FROM_IITP",
  "notes": "Near gate 2",
  "passengers": [
    {
      "email": "jane@iitp.ac.in",
      "displayName": "Jane Smith",
      "rollNumber": "2301CS16"
    }
  ],
  "trainNumber": "12345",
  "trainName": "Rajdhani Express",
  "completionStatus": "COMPLETED",
  "completedAt": "2024-01-15T12:00:00Z",
  "deletedByUsers": []
}
```

#### 2. `chats` Collection
```json
{
  "messageId": "auto-generated-id",
  "rideId": "ride-id-reference",
  "senderEmail": "john@iitp.ac.in",
  "senderName": "John Doe",
  "message": "I'm at the gate",
  "timestamp": "2024-01-15T10:35:00Z",
  "deletedByUsers": []
}
```

### Why Firestore?

1. **Real-time Updates**: Built-in real-time listeners
2. **Offline Support**: Works offline and syncs when online
3. **Scalability**: Handles millions of documents
4. **Security**: Built-in security rules
5. **NoSQL**: Flexible schema for evolving requirements
6. **Integration**: Seamless integration with other Firebase services

### Security Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /rideHistory/{document} {
      allow read, write: if request.auth != null && 
        (resource.data.creatorEmail == request.auth.token.email ||
         resource.data.passengers[].email == request.auth.token.email);
    }
    
    match /chats/{document} {
      allow read, write: if request.auth != null;
    }
  }
}
```

---

## Authentication System

### Microsoft Authentication Library (MSAL)

**Why MSAL?**
- **Institutional Integration**: Works with IIT Patna's Microsoft 365
- **Security**: Enterprise-grade authentication
- **Single Sign-On**: Users don't need separate passwords
- **Compliance**: Meets institutional security requirements

**Implementation** (`AuthService.kt`):
```kotlin
class AuthService(private val context: Context) {
    private var msalApp: ISingleAccountPublicClientApplication? = null
    
    suspend fun signIn(activity: Activity): Result<UserInfo> {
        val result = suspendCancellableCoroutine<IAuthenticationResult?> { continuation ->
            val authCallback = object : AuthenticationCallback {
                override fun onSuccess(result: IAuthenticationResult) {
                    continuation.resume(result)
                }
                override fun onError(exception: MsalException) {
                    continuation.resume(null)
                }
            }
            
            val parameters = AcquireTokenParameters.Builder()
                .startAuthorizationFromActivity(activity)
                .withScopes(listOf("User.Read"))
                .withCallback(authCallback)
                .withPrompt(Prompt.SELECT_ACCOUNT)
                .build()
            
            msalApp?.acquireToken(parameters)
        }
        
        // Extract user info and validate domain
        val email = result.account.username.lowercase()
        if (!email.endsWith("@iitp.ac.in")) {
            return Result.failure(Exception("Only IIT Patna accounts allowed"))
        }
        
        return Result.success(UserInfo(email = email, displayName = displayName))
    }
}
```

**Key Features**:
- **Domain Restriction**: Only allows @iitp.ac.in emails
- **Roll Number Extraction**: Automatically extracts roll numbers from email
- **Persistent Storage**: Uses DataStore for offline authentication state
- **Error Handling**: Comprehensive error handling for auth failures

---

## File Structure & Code Explanation

### Project Structure
```
app/src/main/java/com/project/cabshare/
├── auth/                          # Authentication module
│   ├── AuthConfig.kt             # MSAL configuration
│   ├── AuthService.kt            # Authentication logic
│   ├── AuthViewModel.kt          # Auth state management
│   └── UserInfo.kt               # User data model
├── data/                          # Data layer
│   ├── ChatRepository.kt         # Chat data interface
│   ├── FirestoreChatRepositoryImpl.kt  # Chat Firestore implementation
│   ├── RideHistoryRepository.kt  # Ride history interface
│   ├── FirestoreRideHistoryRepositoryImpl.kt  # Ride history implementation
│   └── FirebaseInitializer.kt    # Firebase setup
├── models/                        # Data models
│   ├── ChatMessage.kt            # Chat message model
│   ├── Ride.kt                   # Active ride model
│   └── RideHistory.kt            # Completed ride model
├── ui/                           # UI layer
│   ├── navigation/               # Navigation setup
│   │   ├── AppNavHost.kt         # Main navigation
│   │   └── AppRoutes.kt          # Route definitions
│   ├── screens/                  # UI screens
│   │   ├── ChatScreen.kt         # Chat interface
│   │   ├── RideHistoryScreen.kt  # Ride history interface
│   │   └── ...                   # Other screens
│   ├── viewmodels/               # ViewModels
│   │   ├── ChatViewModel.kt      # Chat state management
│   │   └── RideHistoryViewModel.kt  # Ride history state management
│   └── theme/                    # UI theming
└── workers/                      # Background tasks
    └── RideCleanupWorker.kt      # Cleanup old rides
```

### Key Code Patterns

#### 1. Dependency Injection (Factory Pattern)
```kotlin
class RideHistoryViewModel(
    private val repository: RideHistoryRepository,
    private val userEmail: String
) : ViewModel() {
    
    companion object {
        fun provideFactory(
            userEmail: String,
            repository: RideHistoryRepository = FirestoreRideHistoryRepositoryImpl()
        ): ViewModelProvider.Factory = object : ViewModelProvider.Factory {
            override fun <T : ViewModel> create(modelClass: Class<T>): T {
                if (modelClass.isAssignableFrom(RideHistoryViewModel::class.java)) {
                    return RideHistoryViewModel(repository, userEmail) as T
                }
                throw IllegalArgumentException("Unknown ViewModel class")
            }
        }
    }
}
```

**Why Factory Pattern?**
- **Parameterized Construction**: ViewModels need user-specific data
- **Testability**: Easy to inject mock dependencies
- **Lifecycle Management**: Proper ViewModel lifecycle handling

#### 2. Coroutines for Async Operations
```kotlin
fun loadUserRideHistory() {
    viewModelScope.launch {
        _isLoading.value = true
        try {
            repository.getUserRideHistory(userEmail)
                .catch { e -> _error.value = "Failed to load: ${e.message}" }
                .collect { history -> _rideHistory.value = history }
        } finally {
            _isLoading.value = false
        }
    }
}
```

**Why Coroutines?**
- **Non-blocking**: Doesn't block UI thread
- **Structured Concurrency**: Automatic cancellation on ViewModel destruction
- **Error Handling**: Built-in exception handling
- **Readable**: Sequential code for async operations

#### 3. Compose State Management
```kotlin
@Composable
fun RideHistoryScreen(navController: NavController) {
    val rideHistory by rideHistoryViewModel.rideHistory.collectAsState()
    val isLoading by rideHistoryViewModel.isLoading.collectAsState()
    
    when {
        isLoading -> CircularProgressIndicator()
        rideHistory.isEmpty() -> EmptyState()
        else -> LazyColumn { items(rideHistory) { RideHistoryCard(it) } }
    }
}
```

**Why Compose State?**
- **Reactive UI**: Automatically recomposes on state changes
- **Performance**: Only recomposes changed components
- **Declarative**: UI describes what should be shown, not how
- **Type Safe**: Compile-time type checking

---

## Interview Talking Points

### Technical Decisions & Trade-offs

#### 1. Why Jetpack Compose over XML?
- **Declarative UI**: Easier to reason about and maintain
- **Less Boilerplate**: No need for findViewById or manual state management
- **Better Performance**: Compose compiler optimizations
- **Modern**: Future of Android development
- **Reactive**: Built-in state management

#### 2. Why MVVM over MVP or MVC?
- **Separation of Concerns**: Clear separation between UI and business logic
- **Testability**: ViewModels can be unit tested without UI
- **Lifecycle Awareness**: ViewModels survive configuration changes
- **Reactive**: StateFlow provides reactive data streams
- **Google Recommended**: Official Android architecture pattern

#### 3. Why Firestore over SQLite or Room?
- **Real-time**: Built-in real-time synchronization
- **Offline Support**: Works offline and syncs when online
- **Scalability**: Handles millions of users
- **No Backend**: No need to maintain server infrastructure
- **Security**: Built-in security rules

#### 4. Why Repository Pattern?
- **Abstraction**: Hides data source implementation
- **Testability**: Easy to mock for unit testing
- **Flexibility**: Can switch data sources without changing ViewModels
- **Single Responsibility**: Each repository handles one domain

### Performance Optimizations

#### 1. Lazy Loading
```kotlin
LazyColumn {
    items(rideHistory) { ride ->
        RideHistoryCard(ride = ride)
    }
}
```
- **Memory Efficient**: Only renders visible items
- **Smooth Scrolling**: Handles large datasets
- **Recomposition**: Only recomposes changed items

#### 2. Pagination
```kotlin
fun loadMoreMessages() {
    val olderMessages = repository.getMessages(rideId, PAGE_SIZE, lastMessageTimestamp, userEmail)
    _messages.value = _messages.value + olderMessages
}
```
- **Performance**: Loads data in chunks
- **Memory**: Prevents loading too much data at once
- **User Experience**: Faster initial load

#### 3. Soft Delete
```kotlin
// Instead of deleting, mark as deleted
docRef.update("deletedByUsers", FieldValue.arrayUnion(userEmail))
```
- **Data Integrity**: Preserves data for other users
- **Audit Trail**: Maintains history
- **Performance**: Faster than actual deletion

### Error Handling Strategy

#### 1. Repository Level
```kotlin
suspend fun getUserRideHistory(userEmail: String): Flow<List<RideHistory>> = flow {
    try {
        val snapshot = historyCollection.get().await()
        emit(convertToRideHistory(snapshot))
    } catch (e: Exception) {
        Log.e(TAG, "Error getting ride history: ${e.message}")
        emit(emptyList()) // Graceful degradation
    }
}
```

#### 2. ViewModel Level
```kotlin
fun loadUserRideHistory() {
    viewModelScope.launch {
        repository.getUserRideHistory(userEmail)
            .catch { e -> _error.value = "Failed to load: ${e.message}" }
            .collect { history -> _rideHistory.value = history }
    }
}
```

#### 3. UI Level
```kotlin
when {
    error != null -> {
        Text("Error: $error")
        Button(onClick = { viewModel.retry() }) { Text("Retry") }
    }
    isLoading -> CircularProgressIndicator()
    else -> Content()
}
```

### Security Considerations

#### 1. Authentication
- **Domain Restriction**: Only IIT Patna emails allowed
- **Token Validation**: MSAL handles token validation
- **Secure Storage**: DataStore for sensitive data

#### 2. Data Access
- **Firestore Rules**: Server-side validation
- **User Context**: All operations require authentication
- **Data Filtering**: Users only see their own data

#### 3. Input Validation
- **Client-side**: Immediate feedback
- **Server-side**: Firestore rules validation
- **Sanitization**: Proper data sanitization

### Scalability Considerations

#### 1. Database Design
- **Denormalization**: Trade storage for read performance
- **Indexing**: Proper Firestore indexes
- **Pagination**: Handle large datasets

#### 2. Real-time Updates
- **Selective Listening**: Only listen to relevant data
- **Connection Management**: Proper listener cleanup
- **Offline Handling**: Graceful offline behavior

#### 3. Memory Management
- **ViewModel Scope**: Proper lifecycle management
- **Lazy Loading**: Load data as needed
- **Image Optimization**: Efficient image handling

---

## Common Interview Questions & Answers

### Q: "Walk me through the ride history feature implementation."

**A:** "The ride history feature allows users to view their completed rides. Here's how I implemented it:

1. **Data Model**: Created a `RideHistory` data class with fields like source, destination, dateTime, passengers, and completion status.

2. **Repository Pattern**: Implemented `RideHistoryRepository` interface with `FirestoreRideHistoryRepositoryImpl` for data access. This abstracts the data source and makes testing easier.

3. **ViewModel**: Created `RideHistoryViewModel` that uses StateFlow to manage the ride history state. It handles loading, error states, and user interactions.

4. **UI**: Built `RideHistoryScreen` using Jetpack Compose with LazyColumn for efficient scrolling. The UI automatically updates when data changes through StateFlow.

5. **Key Features**: 
   - Soft delete mechanism (users can delete rides from their view without affecting others)
   - Real-time updates when new rides are completed
   - Error handling with retry functionality
   - Empty state handling for new users

The architecture follows MVVM pattern with proper separation of concerns, making it testable and maintainable."

### Q: "How does the real-time chat feature work?"

**A:** "The in-ride chat feature enables real-time communication between passengers:

1. **Real-time Listeners**: Uses Firestore's `snapshots()` to listen for new messages in real-time. This automatically updates the UI when new messages arrive.

2. **Message Model**: Each message contains rideId, sender info, message content, timestamp, and a deletedByUsers list for soft delete.

3. **Repository Implementation**: The `FirestoreChatRepositoryImpl` uses Firestore queries to filter messages by rideId and handles soft delete by checking the deletedByUsers array.

4. **ViewModel**: `ChatViewModel` manages the message state using StateFlow and handles sending messages, loading initial messages, and real-time updates.

5. **UI Features**:
   - Auto-scroll to new messages
   - Different message bubble styling for sent vs received
   - Real-time message delivery
   - Soft delete (users can delete messages for themselves)

6. **Performance**: Uses pagination to load messages in batches and only listens to messages for the current ride to minimize bandwidth usage."

### Q: "Why did you choose this tech stack?"

**A:** "I chose this tech stack based on several factors:

1. **Jetpack Compose**: It's the future of Android development, offers better performance, less boilerplate code, and declarative UI that's easier to maintain.

2. **Firebase Firestore**: Provides real-time capabilities out of the box, handles offline scenarios, scales automatically, and integrates well with other Firebase services. For a ride-sharing app, real-time updates are crucial.

3. **MVVM Architecture**: It's the recommended Android architecture pattern that provides good separation of concerns, makes testing easier, and handles configuration changes properly.

4. **Microsoft Authentication**: Since this is for IIT Patna students, using MSAL integrates with their existing Microsoft 365 accounts, providing seamless authentication without requiring separate credentials.

5. **Kotlin Coroutines**: For handling asynchronous operations in a clean, readable way without blocking the UI thread.

The combination provides a modern, scalable, and maintainable solution that handles the specific requirements of a real-time ride-sharing application."

### Q: "How do you handle offline scenarios?"

**A:** "Firebase Firestore provides excellent offline support:

1. **Automatic Caching**: Firestore automatically caches data locally, so users can view previously loaded data even when offline.

2. **Offline Writes**: Users can send messages or perform actions while offline. These are queued and automatically synced when connectivity is restored.

3. **Conflict Resolution**: Firestore handles conflicts automatically using last-write-wins strategy, which works well for chat messages and ride updates.

4. **UI Feedback**: The app shows loading states and error messages to inform users about connectivity issues.

5. **Data Persistence**: Critical user data like authentication state is stored locally using DataStore, so users don't need to re-authenticate when the app restarts.

This ensures a smooth user experience even with poor network connectivity, which is important for a transportation app where users might be in areas with limited connectivity."

---

This comprehensive documentation should help you confidently explain your project to interviewers, demonstrating deep understanding of the technical decisions, architecture patterns, and implementation details.
