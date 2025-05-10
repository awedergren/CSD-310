# Team Blue
# Module 11.1 - Milestone #3
# TEAM MEMBERS:
# Amanda Wedergren
# Miguel Fernandez
# Jonah Aney
# Justin Marucci

# This program provides the user tables and reports for the Bacchus Winery database.

# The tables include: Wine, Distributor, Suppliers, Supplies, Orders, as well as,
# Department, Employees, Hours, and Manager

# The reports include: Low selling wine, delivery analysis, and employee hours.
# These are generated using SQL queries.

# Import connection to mysql database
import mysql.connector
# Database connection
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="winery_user",
    password="your_password",
    database="bacchuswinery"
)

# Function to show tables in the mysql database
def show_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("\nTables in bacchuswinery database:")
    for table in tables:
        print(table[0])
    cursor.close()

# Function to generate reports
def show_reports(connection):
    cursor = connection.cursor()

# Code block for generating low selling wines report.  Report covers last 12 months showing the lowest selling wine first.
    print("\n=== Low Selling Wines Report ===")
    low_selling_query = """
    SELECT 
        w.Wine_ID, 
        w.Wine_Name, 
        COUNT(d.Shipment_ID) as number_of_shipments, 
        SUM(d.Case_Quantity) as total_cases_shipped
    FROM wine w
    LEFT JOIN distributor d ON w.Wine_ID = d.Wine_ID
    WHERE d.Shipment_Date >= DATE_SUB(CURRENT_DATE, INTERVAL 12 MONTH)
    GROUP BY w.Wine_ID, w.Wine_Name
    ORDER BY total_cases_shipped ASC; 
    """
# Running the mysql query and getting all the rows of data.
    cursor.execute(low_selling_query)
    results = cursor.fetchall()
    for row in results:
        print(f"Wine ID: {row[0]}, Name: {row[1]}, Shipments: {row[2]}, Total Cases: {row[3]}")

# Code block for generating delivery analysis report. Report covers orders with categories of 'on time', 'delayed', and 'early' delivery.
    print("\n=== Delivery Time Analysis Report ===")
    delivery_query = """
    SELECT 
        Order_ID, 
        Expected_delivery_date, 
        Actual_delivery_date, 
        DATEDIFF(Actual_delivery_date, Expected_delivery_date) as delivery_delay_days, 
        CASE 
            WHEN DATEDIFF(Actual_delivery_date, Expected_delivery_date) > 0 
            THEN 'Delayed' 
            WHEN DATEDIFF(Actual_delivery_date, Expected_delivery_date) = 0 
            THEN 'On Time' 
            ELSE 'Early' 
        END as delivery_status
    FROM orders
    WHERE Actual_delivery_date IS NOT NULL
    ORDER BY delivery_delay_days DESC; 
    """
# Running the mysql query and getting all the rows of data.
    cursor.execute(delivery_query)
    results = cursor.fetchall()
    for row in results:
        print(f"Order ID: {row[0]}, Expected: {row[1]}, Actual: {row[2]}, Delay Days: {row[3]}, Status: {row[4]}")

# Code block for calculating employee hours report. Report output has employee hours by quarter and the total for the year.
    print("\n=== Employee Quarterly Hours Report ===")
    hours_query = """
    SELECT 
        e.Employee_ID, 
        e.Employee_F_Name, 
        e.Employee_L_Name, 
        YEAR(h.Month_Year) as year,
        MAX(CASE WHEN QUARTER(h.Month_Year) = 1 THEN h.Total_Hours ELSE 0 END) as Q1_hours,
        MAX(CASE WHEN QUARTER(h.Month_Year) = 2 THEN h.Total_Hours ELSE 0 END) as Q2_hours,
        MAX(CASE WHEN QUARTER(h.Month_Year) = 3 THEN h.Total_Hours ELSE 0 END) as Q3_hours,
        MAX(CASE WHEN QUARTER(h.Month_Year) = 4 THEN h.Total_Hours ELSE 0 END) as Q4_hours

    FROM employees e
    JOIN hours h ON e.Employee_ID = h.Employee_ID
    GROUP BY
        e.Employee_ID,
        e.Employee_F_Name,
        e.Employee_L_Name,
        YEAR (h.Month_Year)
    ORDER BY
        YEAR(h.Month_Year) DESC,
        e.Employee_L_Name; 
     """
# Running the mysql query and getting all the rows of data.
    cursor.execute(hours_query)
    results = cursor.fetchall()
    current_year = None
# For loop to run through the data and create a variable for each row.
    for row in results:
        employee_id, f_name, l_name, year, q1_hours, q2_hours, q3_hours, q4_hours = row
        total_hours = sum(0 if q is None or q == 0 else q for q in [q1_hours, q2_hours, q3_hours, q4_hours])
# Printing the year and the dashes. Dashes used as seperator lines for clear and organized output.
        if year != current_year:
            if current_year is not None:
                print("-" * 91)
            print(f"\nYear: {year}")
            print("-" * 91)
# Setting up spacing between each variable for clean and readable output.
            print(
                f"| {'Employee ID':^10} | {'Employee Name':<25} | {'Q1':^8} | {'Q2':^8} | {'Q3':^8} | {'Q4':^8} | {'Total Hours':^8} |")
            print("-" * 91)
            current_year = year

        name = f"{f_name} {l_name}"
        print(f"| {employee_id:^10} | {name:<25} | {q1_hours or '-':^8} | {q2_hours or '-':^8} | "
              f"{q3_hours or '-':^8} | {q4_hours or '-':^8} | {total_hours:^8} |")

    if results:
        print("-" * 91)

    cursor.close()

# While loop for program options and user input.
while True:
    print("\nBacchus Winery Database Management")
    print("1. Show Tables")
    print("2. Run Reports")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        show_tables(connection)
    elif choice == '2':
        show_reports(connection)
    elif choice == '3':
        print("Exiting program...")
        if connection.is_connected():
            connection.close()
            print("Database connection closed.")
        break

    else:
        print("Invalid choice. Please try again.")

