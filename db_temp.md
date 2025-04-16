Database Procedures, Functions, and Triggers
===========================================

1. Procedures
------------

a) book_ticket
Purpose: Handles the ticket booking process
```sql
CREATE PROCEDURE book_ticket(
    IN p_passenger_id INT,
    IN p_train_id INT,
    IN p_journey_date DATE,
    IN p_source_station_id INT,
    IN p_destination_station_id INT,
    IN p_class_id INT
)
BEGIN
    -- Handles complete ticket booking process
END;
```

b) calculate_cancellation_refund
Purpose: Calculates refund amount for cancellations
```sql
CREATE PROCEDURE calculate_cancellation_refund(
    IN p_ticket_id INT,
    IN p_cancellation_date DATE
)
BEGIN
    -- Calculates refund amount based on cancellation rules
END;
```

c) cancel_ticket
Purpose: Handles ticket cancellation process
```sql
CREATE PROCEDURE cancel_ticket(
    IN p_ticket_id INT,
    IN p_cancellation_reason VARCHAR(255)
)
BEGIN
    -- Handles complete ticket cancellation process
END;
```

d) check_pnr_status
Purpose: Checks PNR status for a ticket
```sql
CREATE PROCEDURE check_pnr_status(
    IN p_pnr_number VARCHAR(20)
)
BEGIN
    -- Returns current status of the ticket
END;
```

e) generate_ticket_bill
Purpose: Generates detailed bill for a ticket
```sql
CREATE PROCEDURE generate_ticket_bill(
    IN p_ticket_id INT
)
BEGIN
    -- Generates itemized bill for the ticket
END;
```

f) get_available_seats
Purpose: Gets available seats for a train
```sql
CREATE PROCEDURE get_available_seats(
    IN p_train_id INT,
    IN p_journey_date DATE,
    IN p_class_id INT
)
BEGIN
    -- Returns available seats information
END;
```

g) get_busiest_routes
Purpose: Identifies busiest train routes
```sql
CREATE PROCEDURE get_busiest_routes(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    -- Returns busiest routes based on passenger count
END;
```

h) get_cancellation_records
Purpose: Retrieves cancellation records
```sql
CREATE PROCEDURE get_cancellation_records(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    -- Returns cancellation records with refund status
END;
```

i) get_revenue_report
Purpose: Generates revenue reports
```sql
CREATE PROCEDURE get_revenue_report(
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    -- Generates revenue report for the period
END;
```

j) get_train_passengers
Purpose: Lists train passengers
```sql
CREATE PROCEDURE get_train_passengers(
    IN p_train_id INT,
    IN p_journey_date DATE
)
BEGIN
    -- Lists passengers for a specific train
END;
```

k) get_train_schedule
Purpose: Retrieves train schedule
```sql
CREATE PROCEDURE get_train_schedule(
    IN p_train_id INT
)
BEGIN
    -- Returns complete train schedule
END;
```

l) get_waitlisted_passengers
Purpose: Lists waitlisted passengers
```sql
CREATE PROCEDURE get_waitlisted_passengers(
    IN p_train_id INT,
    IN p_journey_date DATE
)
BEGIN
    -- Lists waitlisted passengers
END;
```

m) keep_first_7_running_dates
Purpose: Maintains running dates
```sql
CREATE PROCEDURE keep_first_7_running_dates()
BEGIN
    -- Keeps only next 7 days of running dates
END;
```

n) search_trains
Purpose: Searches available trains
```sql
CREATE PROCEDURE search_trains(
    IN p_source_station VARCHAR(100),
    IN p_dest_station VARCHAR(100),
    IN p_journey_date DATE
)
BEGIN
    -- Searches trains between stations
END;
```

o) show_table_counts
Purpose: Shows table record counts
```sql
CREATE PROCEDURE show_table_counts()
BEGIN
    -- Displays count of records in all tables
END;
```

p) update_train_schedules
Purpose: Updates train schedules
```sql
CREATE PROCEDURE update_train_schedules()
BEGIN
    -- Updates train schedules
END;
```

2. Functions
-----------

a) CalculateFare
Purpose: Calculates the ticket fare based on various factors
```sql
CREATE FUNCTION CalculateFare(
    p_distance INT,
    p_class_id INT,
    p_passenger_type VARCHAR(20)
) RETURNS DECIMAL(10,2)
BEGIN
    -- Function logic for fare calculation
    -- Considers distance, class, and passenger type
    RETURN calculated_fare;
END;
```

b) CheckSeatAvailability
Purpose: Checks seat availability for a given train and date
```sql
CREATE FUNCTION CheckSeatAvailability(
    p_train_id INT,
    p_journey_date DATE,
    p_class_id INT
) RETURNS INT
BEGIN
    -- Function logic for checking seat availability
    RETURN available_seats;
END;
```

c) calculate_fare
Purpose: Calculates the fare for a ticket based on distance and class
```sql
CREATE FUNCTION calculate_fare(
    distance INT,
    class_id INT
) RETURNS DECIMAL(10,2)
BEGIN
    -- Calculates ticket fare based on distance and class
    RETURN calculated_amount;
END;
```

d) calculate_refund
Purpose: Calculates refund amount for cancelled tickets
```sql
CREATE FUNCTION calculate_refund(
    ticket_id INT,
    cancellation_date DATE
) RETURNS DECIMAL(10,2)
BEGIN
    -- Calculates refund amount based on cancellation rules
    RETURN refund_amount;
END;
```

e) get_next_running_dates
Purpose: Gets the next running dates for a train
```sql
CREATE FUNCTION get_next_running_dates(
    train_id INT,
    start_date DATE
) RETURNS VARCHAR(255)
BEGIN
    -- Returns next running dates for the train
    RETURN running_dates;
END;
```

f) get_rac_number
Purpose: Generates RAC number for waitlisted tickets
```sql
CREATE FUNCTION get_rac_number(
    train_id INT,
    journey_date DATE
) RETURNS INT
BEGIN
    -- Generates next available RAC number
    RETURN rac_number;
END;
```

g) get_waitlist_number
Purpose: Generates waitlist number for tickets
```sql
CREATE FUNCTION get_waitlist_number(
    train_id INT,
    journey_date DATE
) RETURNS INT
BEGIN
    -- Generates next available waitlist number
    RETURN waitlist_number;
END;
```

3. Triggers
----------

a) update_seat_status_after_ticket_insert
Purpose: Updates seat status after ticket booking
```sql
CREATE TRIGGER update_seat_status_after_ticket_insert
AFTER INSERT ON tickets
FOR EACH ROW
BEGIN
    -- Updates seat status after new ticket booking
END;
```

b) after_ticket_insert
Purpose: Handles post-ticket insertion tasks
```sql
CREATE TRIGGER after_ticket_insert
AFTER INSERT ON tickets
FOR EACH ROW
BEGIN
    -- Performs tasks after ticket insertion
END;
```

c) handleCancellation
Purpose: Manages ticket cancellation process
```sql
CREATE TRIGGER handleCancellation
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    -- Handles ticket cancellation process
END;
```

d) after_ticket_cancel
Purpose: Performs post-cancellation tasks
```sql
CREATE TRIGGER after_ticket_cancel
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    -- Performs tasks after ticket cancellation
END;
```

e) after_ticket_cancellation
Purpose: Additional cancellation handling
```sql
CREATE TRIGGER after_ticket_cancellation
AFTER UPDATE ON tickets
FOR EACH ROW
BEGIN
    -- Additional cancellation handling tasks
END;
```

f) UpdateRACStatus
Purpose: Updates RAC (Reservation Against Cancellation) status
```sql
CREATE TRIGGER UpdateRACStatus
AFTER UPDATE ON seatavailability
FOR EACH ROW
BEGIN
    -- Trigger logic to update RAC status
    -- Handles RAC to confirmed conversion
END;
```

Note: These are the actual database objects found in the system. Each object serves a specific purpose in the IRCTC booking system, working together to ensure smooth ticket booking, cancellation, and management processes. The actual implementations contain detailed logic and error handling specific to the railway reservation system. 
