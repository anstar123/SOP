# CabShare - Cab Sharing App for IIT Patna

CabShare is a modern Android application designed to help IIT Patna students find and share cab rides with each other. The app facilitates ride sharing between the campus and various the most frequent destinations including Patna Junction, Patna Airport and Bihta Railway Station.

## Features

- 🔐 **Secure Authentication**
  - Microsoft Authentication with @iitp.ac.in email restriction
  - Secure user profile management
  - Automatic session management

- 🚗 **Ride Management**
  - Create and join cab rides
  - Real-time ride status updates
  - Ride request and approval system

- 📱 **User Interface**
  - Intuitive navigation
  - Real-time notifications tab

- 🔄 **Real-time Features**
  - Live ride updates
  - Real-time passenger list updates
  - Automatic ride cleanup for past rides

## Tech Stack

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose
- **Architecture**: MVVM (Model-View-ViewModel)
- **Authentication**: Microsoft Authentication Library (MSAL)
- **Backend**: Firebase
- **Background Tasks**: WorkManager
- **State Management**: Kotlin Flow
- **Minimum SDK**: 26 (Android 8.0)
- **Target SDK**: 34 (Android 14)

## Prerequisites

- Android Studio Hedgehog (2023.1.1) or newer
- JDK 17 or newer
- Android SDK 34
- Google Services configuration
- Microsoft Azure account for authentication

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/EshanBhaskar/CabShare.git
   cd CabShare
   ```

2. **Microsoft Authentication Setup**
   - Go to [Azure Portal](https://portal.azure.com)
   - Navigate to "Microsoft Entra ID" (formerly Azure Active Directory)
   - Create a new app registration:
     - Name: "CabShare"
     - Supported account types: "Accounts in any organizational directory"
     - Redirect URI: `msauth://com.project.cabshare/callback`
   - Copy the Application (client) ID
   - Update `app/src/main/java/com/project/cabshare/auth/AuthConfig.kt` with your client ID

3. **Firebase Setup**
   - Create a new Firebase project
   - Add your Android app to the Firebase project
   - Download `google-services.json` and place it in the `app` directory
   - Enable Firestore Database
   - Set up Firestore security rules

4. **Build and Run**
   - Open the project in Android Studio
   - Sync project with Gradle files
   - Run the app on an emulator or physical device

## Project Structure

```
app/
├── src/
│   ├── main/
│   │   ├── java/com/project/cabshare/
│   │   │   ├── auth/           # Authentication related code
│   │   │   ├── data/           # Data layer and repositories
│   │   │   ├── models/         # Data models
│   │   │   ├── ui/             # UI components
│   │   │   │   ├── screens/    # App screens
│   │   │   │   ├── theme/      # UI theme
│   │   │   │   └── viewmodels/ # ViewModels
│   │   │   ├── workers/        # Background workers
│   │   │   └── utils/          # Utility classes
│   │   └── res/                # Resources
│   └── test/                   # Unit tests
└── build.gradle                # App-level build configuration
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

If you encounter dependency resolution issues:

1. Make sure your project includes JitPack repository in `settings.gradle.kts`
2. Use MSAL version 2.3.5 or newer
3. Ensure you have explicitly added the required dependencies:
   - `com.microsoft.device:display-mask:0.4.0`
   - `io.opentelemetry:opentelemetry-api:1.18.0`
   - `io.opentelemetry:opentelemetry-sdk:1.18.0`
