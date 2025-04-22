# Duration-based Smart Attendance System (DSAS)

## Table of Contents
1. [Introduction](#introduction)
2. [Motivation](#motivation)
3. [Innovation/Uniqueness](#innovationuniqueness)
4. [Hardware Requirements](#hardware-requirements)
5. [Project Workflow](#project-workflow)
6. [Circuit Diagram](#circuit-diagram)
7. [Code Details](#code-details)
8. [Project Outcome](#project-outcome)
9. [Potential System Exploits and Vulnerabilities](#potential-system-exploits-and-vulnerabilities)
10. [Individual Contributions](#individual-contributions)

## Introduction
The Duration-based Smart Attendance System (DSAS) is an automated attendance management system based on Bluetooth Low Energy (BLE) technology that captures the presence of students. It is comprised of an ESP32 microcontroller and a Real-Time Clock (RTC) module that collaborate to record student attendance on the basis of their physical presence in the class for a determined period of time.

## Motivation
- **Manual Attendance Problems**: Conventional roll-call procedures are time-consuming, particularly in big classes (100+ students), and susceptible to proxy attendance.
- **Digital Attendance Drawbacks**: Although digital means such as Google Forms are quicker, they are susceptible to proxy attendance since students can easily forward form links.
- **Project Objectives**:
  - Automate the attendance process to conserve time
  - Employ BLE detection to confirm real student presence
- Adopt duration-based attendance (students have to attend at least 80% of class time)
- Offer real-time attendance tracking and reporting

## Innovation/Uniqueness
- **Duration-Based Tracking**: Students are recorded present only when they are identified for a minimum of 80% of class duration
- **Real-Time Monitoring**: System scans every 5 seconds to confirm uninterrupted presence
- **Offline Time Accuracy**: RTC module provides accurate timekeeping regardless of network connectivity
- **Firebase Integration**: Real-time attendance data storage and retrieval
- **Cost-Effective**: Utilizes very few hardware components (ESP32 + RTC module)
- **Scalable**: Can be deployed with ease on multiple classrooms

## Hardware Requirements
- **ESP32 Dev Module**: For BLE scanning and WiFi connectivity
- **DS3231 RTC Module**: For precise timekeeping
- **Power Supply**:
  - USB power for ESP32
  - 3V coin cell battery for RTC backup
- **Wires Connection**: To enable I2C communication from ESP32 to RTC

## Project Workflow
1. **Initialization**:
   - WiFi connection by ESP32
   - Current time set by RTC
   - Firebase authentication process
   - BLE scanner initiation

2. **Class Setup**:
   - Instructor fills course code, lecture number, and duration
   - Time tracking begins in the system

3. **Attendance Tracking**:
   - BLE scanning takes place every 5 seconds
- Uses UUID to detect student devices
- Logs entry and last seen timestamps
- Updates Firebase real-time

4. **Marking Attendance**:
   - Upon class duration completion
   - Calculates attendance duration for individual students
   - Marks presence based on 80% condition
   - Updates attendance counts

## Circuit Diagram
``` 
ESP32 <--I2C--> DS3231 RTC
  |
  |--USB Power
```
|--WiFi Connection
  |--BLE Scanning
```

## Code Details
The system employs a few important components:

1. **RTC Time Management**:
   - System automatic time setting
   - Timestamping with precision
   - Calculation of duration

2. **BLE Scanning**:
   - 5-second scan interval
   - UUID-based student detection
   - Ongoing presence tracking

3. **Firebase Integration**:
   - Updating the real-time database
- Attendance statistics tracking
   - Secure authentication

4. **Attendance Logic**:
   - Entry time recording
   - Duration calculation
   - 80% presence threshold
   - Automatic status updates

## Project Outcome
- **Successful Implementation**:
  - Accurate BLE device detection
  - Reliable time tracking
  - Real-time Firebase updates
  - Duration-based attendance marking

- **Technical Specifications**:
- BLE range of detection: ~10 meters
  - Scan interval: 5 seconds
  - Minimum duration of attendance: 80% of class time
  - Updates of real-time data

- **Challenges Overcome**:
  - Stability of BLE signal
  - Synchronization of RTC time
  - Management of Firebase connection
  - Memory optimization

## Potential System Exploits and Vulnerabilities
1. **Device Sharing**: Students can share devices to record proxy attendance
- Mitigation: Periodic physical checks by teachers

2. **Bluetooth Disabling**: Students may disable Bluetooth to evade detection
   - Mitigation: Mandatory use of Bluetooth for attendance

3. **Signal Range**: BLE signals can be impacted by physical barriers
   - Mitigation: Careful positioning of ESP32 in classroom

4. **Battery Issues**: RTC backup battery failure may impact timekeeping
   - Mitigation: Periodic battery checks and replacement

5. **Network Dependence**: Firebase connectivity loss
- Mitigation: Local storage with syncing once connection is regained

## Individual Contributions
[Place holder for team member contributions]
