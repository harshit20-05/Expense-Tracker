##Expense Tracker

Overview
The Expense Tracker is a Python-based application designed to help users efficiently manage their daily expenses. 
It allows users to add, delete, and visualize their expenses, providing clear insights into their financial patterns. 
With features like real-time expense tracking, visualization through pie charts, and persistent data storage, the Expense Tracker simplifies financial management.

##Key Features


Expense Management:
Add and delete expenses with descriptions and amounts.
Calculate total expenses.


Data Persistence:
Save and load expense data using JSON files for future access.


Visualization:
Generate pie charts using Matplotlib to show the distribution of expenses.


User-Friendly Interface:
Built with Tkinter, offering an intuitive GUI for seamless interaction.


##Tools and Technologies:

Programming Language: Python
Chosen for its simplicity and robust support for libraries.

Libraries Used:
Tkinter: For creating the graphical user interface.
Matplotlib: For visualizing expenses through pie charts.
JSON: For lightweight and readable data storage.
os: For file handling.

Integrated Development Environment (IDE): PyCharm (recommended)


##System Design

1. Expense Management
Add Expense: Allows users to add an expense with a description and amount.
Delete Expense: Enables users to remove an expense by selecting it from the list.
Calculate Total: Provides the total amount of all recorded expenses.
2. Data Storage
Expense data is stored in a JSON file (expenses.json), ensuring persistence even after the application is closed.
3. Visualization
Pie charts provide a clear visual representation of expense categories, helping users understand their spending patterns.
4. Graphical User Interface
The application consists of:
A Display Frame for listing expenses.
A Control Frame for user inputs and actions.


##Interaction:
User Authentication: The Auth class validates credentials and redirects users to the appropriate interface (admin or user).
Financial Management: EarningsManager and SpendingsManager handle all data related to earnings and expenses.
Reports and Visualization: The ExpenseAnalysis class generates reports and visualizes financial data for better decision-making.
User Navigation: CashTrackApp coordinates the flow between different components and ensures a smooth user experience.


##Getting Started

Prerequisites:
To run this project, you need to have Python 3.x installed on your machine.
