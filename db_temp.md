# Indian Railway Ticket Reservation System

## Database Objects Documentation

### Procedures

#### 1. book_ticket
```sql
CREATE PROCEDURE book_ticket(
    IN p_train_no INT,
    IN p_class VARCHAR(20),
    IN p_journey_date DATE,
    IN p_boarding_station VARCHAR(50),
    IN p_destination_station VARCHAR(50),
    IN p_passenger_name VARCHAR(100),
    IN p_age INT,
    IN p_gender VARCHAR(10),
    IN p_berth_preference VARCHAR(20)
)
BEGIN
    -- Implementation details
    -- Handles ticket booking process including:
    -- - Seat availability check
    -- - PNR generation
    -- - Passenger details insertion
    -- - Payment processing
    -- - Status updates (CNF/RAC/WL)
END;
```

#### 2. calculate_cancellation_refund
```sql
CREATE PROCEDURE calculate_cancellation_refund(
    IN p_pnr_no INT,
    OUT p_refund_amount DECIMAL(10,2),
    OUT p_refund_status VARCHAR(20)
)
BEGIN
    -- Implementation details
    -- Calculates refund amount based on:
    -- - Time of cancellation
    -- - Ticket status (CNF/RAC/WL)
    -- - Journey date
    -- Updates payment and booking history
END;
```

#### 3. cancel_ticket
```sql
CREATE PROCEDURE cancel_ticket(
    IN p_pnr_no INT,
    OUT p_success BOOLEAN,
    OUT p_message VARCHAR(200)
)
BEGIN
    -- Implementation details
    -- Handles ticket cancellation including:
    -- - Status validation
    -- - Refund calculation
    -- - Seat release
    -- - RAC/WL promotion
END;
```

#### 4. check_seat_availability
```sql
CREATE PROCEDURE check_seat_availability(
    IN p_train_no INT,
    IN p_class VARCHAR(20),
    IN p_journey_date DATE,
    OUT p_available_seats INT,
    OUT p_available_rac INT,
    OUT p_waitlist_count INT
)
BEGIN
    -- Implementation details
    -- Checks current availability status:
    -- - Confirmed seats
    -- - RAC seats
    -- - Waitlist count
END;
```

#### 5. generate_pnr
```sql
CREATE PROCEDURE generate_pnr(
    OUT p_pnr_no INT
)
BEGIN
    -- Implementation details
    -- Generates unique PNR number
    -- Updates PNR sequence
END;
```

#### 6. get_train_schedule
```sql
CREATE PROCEDURE get_train_schedule(
    IN p_train_no INT,
    IN p_journey_date DATE
)
BEGIN
    -- Implementation details
    -- Retrieves complete train schedule:
    -- - Station list
    -- - Arrival/departure times
    -- - Platform numbers
END;
```

#### 7. update_seat_status
```sql
CREATE PROCEDURE update_seat_status(
    IN p_train_no INT,
    IN p_coach_no VARCHAR(10),
    IN p_seat_no INT,
    IN p_journey_date DATE,
    IN p_status VARCHAR(20),
    IN p_pnr_no INT
)
BEGIN
    -- Implementation details
    -- Updates seat status:
    -- - Marks seat as booked/available
    -- - Updates occupancy details
END;
```

#### 8. validate_booking
```sql
CREATE PROCEDURE validate_booking(
    IN p_train_no INT,
    IN p_class VARCHAR(20),
    IN p_journey_date DATE,
    OUT p_valid BOOLEAN,
    OUT p_message VARCHAR(200)
)
BEGIN
    -- Implementation details
    -- Validates booking parameters:
    -- - Train existence
    -- - Class availability
    -- - Journey date validity
END;
```

### Functions

#### 1. calculate_fare
```sql
CREATE FUNCTION calculate_fare(
    p_base_fare DECIMAL(10,2),
    p_distance INT,
    p_class VARCHAR(20)
) RETURNS DECIMAL(10,2)
BEGIN
    -- Implementation details
    -- Calculates final fare based on:
    -- - Base fare
    -- - Distance
    -- - Class multiplier
    RETURN calculated_fare;
END;
```

#### 2. get_rac_number
```sql
CREATE FUNCTION get_rac_number(
    p_train_no INT,
    p_class VARCHAR(20),
    p_journey_date DATE
) RETURNS INT
BEGIN
    -- Implementation details
    -- Returns next available RAC number
    RETURN rac_number;
END;
```

#### 3. get_waitlist_number
```sql
CREATE FUNCTION get_waitlist_number(
    p_train_no INT,
    p_class VARCHAR(20),
    p_journey_date DATE
) RETURNS INT
BEGIN
    -- Implementation details
    -- Returns next available waitlist number
    RETURN waitlist_number;
END;
```

#### 4. is_booking_window_open
```sql
CREATE FUNCTION is_booking_window_open(
    p_journey_date DATE
) RETURNS BOOLEAN
BEGIN
    -- Implementation details
    -- Checks if booking is allowed for given date
    RETURN is_open;
END;
```

#### 5. validate_passenger_age
```sql
CREATE FUNCTION validate_passenger_age(
    p_age INT
) RETURNS BOOLEAN
BEGIN
    -- Implementation details
    -- Validates passenger age
    RETURN is_valid;
END;
```

### Triggers

#### 1. update_seat_status_after_ticket_insert
```sql
CREATE TRIGGER update_seat_status_after_ticket_insert
AFTER INSERT ON tickets
FOR EACH ROW
BEGIN
    -- Implementation details
    -- Updates seat status when new ticket is inserted:
    -- - Marks seat as booked for CNF
    -- - Updates RAC count
    -- - Updates waitlist count
END;
```

#### 2. after_ticket_insert
```sql
CREATE TRIGGER after_ticket_insert
AFTER INSERT ON tickets
FOR EACH ROW
BEGIN
    -- Implementation details
    -- Handles post-insert operations:
    -- - Seat status updates
    -- - Availability updates
    -- - Status tracking
END;
```

#### 3. handleCancellation
```sql
CREATE TRIGGER handleCancellation
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    -- Implementation details
    -- Manages cancellation process:
    -- - Refund calculation
    -- - Seat release
    -- - RAC/WL promotion
    -- - Payment updates
END;
```

#### 4. after_ticket_cancel
```sql
CREATE TRIGGER after_ticket_cancel
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    -- Implementation details
    -- Handles post-cancellation operations:
    -- - Seat status updates
    -- - RAC/WL management
    -- - Payment processing
END;
```

#### 5. after_ticket_cancellation
```sql
CREATE TRIGGER after_ticket_cancellation
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    -- Implementation details
    -- Updates booking history after cancellation:
    -- - Cancellation status
    -- - Refund amount
    -- - Refund status
END;
```

## Setup Instructions

1. Import the database schema:
```bash
mysql -u root -p < irctc_db_final.sql
```

2. Configure database connection:
- Update connection parameters in your application
- Ensure proper permissions are set

3. Test the system:
- Run sample queries
- Test procedures and functions
- Verify trigger operations

## Notes
- All procedures, functions, and triggers are implemented in the `mini_irctc1` schema
- The system uses MySQL 8.0 or higher
- Proper error handling is implemented in all database objects
- Transaction management is handled at the application level 
