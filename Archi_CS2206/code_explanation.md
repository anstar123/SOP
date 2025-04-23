# Duration-based Smart Attendance System - Code Explanation

## Header Files and Libraries
```cpp
#include <WiFi.h>                // For WiFi connectivity
#include <Wire.h>                // For I2C communication with RTC
#include <RTClib.h>             // For RTC module functions
#include <BLEDevice.h>          // Core BLE functionality
#include <BLEScan.h>            // For BLE scanning operations
#include <BLEAdvertisedDevice.h> // For handling found BLE devices
#include <Firebase_ESP_Client.h> // For Firebase connectivity
#include <Arduino.h>            // Core Arduino functions
#include <BLEUtils.h>           // Additional BLE utilities
```

## Configuration Constants
```cpp
// WiFi Configuration
#define wifi_ssid "ARYABHATTA"
#define wifi_pswd "iitp@123"

// Firebase Configuration
#define fb_host "https://dsas-c7bc9-default-rtdb.firebaseio.com/"
#define fb_apikey "AIzaSyAvVYL3opBDF4xT5UZWsyt6o091NlPqPJk"
#define fb_email "ankeshkr0921@gmail.com"
#define fb_pswd "@Aa45654"
```
These define the connection parameters for WiFi and Firebase.

## Global Objects
```cpp
FirebaseData fbdo;      // Firebase data object for operations
FirebaseAuth auth;      // Firebase authentication object
FirebaseConfig config;  // Firebase configuration object
RTC_DS3231 rtc;        // RTC module object
```

## System Parameters
```cpp
const int scan_time = 1;     // Duration of each BLE scan (1 second)
const int scan_interval = 5; // Time between scans (5 seconds)
const int stud_cnt = 4;     // Total number of students to track
```

## Class Configuration Variables
```cpp
String course_code = "";          // Stores current course code
int lec_num = 0;                 // Current lecture number
String lec_date = "";            // Current date
unsigned long class_duration = 0; // Total class duration in seconds
unsigned long req_duration = 0;   // Required attendance duration (80% of total)
unsigned long last_scan_time = 0; // Timestamp of last BLE scan
```

## Student Data Structure
```cpp
struct Student {
    String name;  // Student's name
    String uuid;  // Unique BLE identifier
    String roll;  // Roll number
};

// Student array initialization
Student students[stud_cnt] = {
    {"Ankesh", "4da64075-887a-4eea-9121-1b0438ce4f89", "2301CS06"},
    {"Eshan", "88fe8911-8a91-4673-bf1c-f04360531436", "2301CS16"},
    {"Krishan", "bfb8e01f-c86e-4716-9c83-be0619d1daf1", "2301CS25"},
    {"Chaitanya", "8cdbd53a-1b57-4b09-b955-5f6ce441e1bf", "2301CS77"}
};
```

## Utility Functions
```cpp
// Formats lecture key as "LecX:YYYY-MM-DD"
String get_lecture_key(int lec_num, String date) {
    return "Lec" + String(lec_num) + ":" + date;
}

// Converts Unix timestamp to HH:MM:SS format
String time_to_string(unsigned long timestamp) {
    DateTime t(timestamp);
    char buffer[10];
    sprintf(buffer, "%02d:%02d:%02d", t.hour(), t.minute(), t.second());
    return String(buffer);
}
```

## Setup Function Explanation
```cpp
void setup() {
    // Initialize serial communication
    Serial.begin(115200);
    Wire.begin();  // Initialize I2C

    // RTC Setup
    if (!rtc.begin()) {
        Serial.println("❌ Couldn't find RTC");
        while (1);  // Halt if RTC not found
    }
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); // Set RTC time

    // WiFi Connection
    WiFi.begin(wifi_ssid, wifi_pswd);
    // Connection attempt with timeout
    // Prints dots while connecting

    // Firebase Initialization
    config.api_key = fb_apikey;
    config.database_url = fb_host;
    auth.user.email = fb_email;
    auth.user.password = fb_pswd;
    Firebase.begin(&config, &auth);

    // BLE Scanner Setup
    BLEDevice::init("DSAS_Scanner");
    pBLEScan = BLEDevice::getScan();
    pBLEScan->setActiveScan(true);
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);
}
```

## Main Loop Function Explanation
```cpp
void loop() {
    // Phase 1: Configuration Input
    if (!config_received) {
        // Wait for and process course details input
        // Format: CS2201,4,60 (course,lecture,duration)
        // Validates input and sets up class parameters
    }

    // Phase 2: BLE Scanning
    if (current_time - last_scan_time >= scan_interval) {
        // Perform BLE scan
        // Check each found device
        // Match UUIDs with student list
        // Record entry times for new detections
        // Update last seen times for present students
    }

    // Phase 3: Attendance Marking
    if (!attendance_marked && (current_time - class_start_time >= class_duration)) {
        // Calculate attendance for each student
        // Check if duration meets 80% requirement
        // Update Firebase with attendance status
        // Update cumulative statistics
    }
}
```

## Attendance Calculation Logic
```cpp
// For each student:
duration = last_seen_timestamps[i] - entry_timestamps[i];
if (duration >= req_duration) status = 1;  // Present
else status = 0;  // Absent
```

## Firebase Data Update Process
```cpp
// 1. Update individual lecture attendance
Firebase.RTDB.setInt(&fbdo, lec_path, status);

// 2. Update statistics
if (status == 1) attended++;
total++;
percentage = (attended * 100.0) / total;

// 3. Update all statistics in Firebase
Firebase.RTDB.setFloat(&fbdo, base_path + "/percentage", percent);
Firebase.RTDB.setInt(&fbdo, base_path + "/attended", attended);
Firebase.RTDB.setInt(&fbdo, base_path + "/total", total);
```

## Key C++ Features Used
1. **Object-Oriented Programming**
   - Classes for Firebase, RTC, and BLE operations
   - Custom Student structure

2. **Memory Management**
   - Static array for student data
   - Dynamic memory for BLE scanning

3. **String Operations**
   - String concatenation for paths
   - Format specifiers for logging

4. **Error Handling**
   - Connection timeout checks
   - Firebase operation verification
   - RTC initialization check

5. **Type Safety**
   - Appropriate use of unsigned long for timestamps
   - Proper type casting where needed

## Performance Considerations
1. **Timing**
   - 5-second scan interval
   - 1-second scan duration
   - 2-second loop delay

2. **Memory**
   - Fixed-size student array
   - Efficient string handling
   - BLE scan result clearing

3. **Error Recovery**
   - WiFi reconnection handling
   - Firebase operation retry
   - RTC battery backup 