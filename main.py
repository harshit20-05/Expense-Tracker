import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
import json

# Global Data

expenses = []
users = {"user1": {"password": "pass123", "expenses": [], "spending_limit": 0}}
admins = {"admin1": {"password": "admin123"}}

def save_expenses_to_file():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file)

def load_expenses_from_file():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# When the app starts, load expenses
expenses = load_expenses_from_file()

# When exiting the app, save expenses
save_expenses_to_file()

def register():
    """Register a new User or Admin."""
    role = register_role.get()
    username = register_username.get().strip()
    password = register_password.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password cannot be empty!")
        return

    if role == "User":
        if username in users:
            messagebox.showwarning("Registration Error", "Username already exists!")
        else:
            users[username] = {"password": password, "expenses": [], "spending_limit": 0}
            messagebox.showinfo("Success", "User registered successfully!")
            switch_frame(landing_page)
    elif role == "Admin":
        if username in admins:
            messagebox.showwarning("Registration Error", "Admin username already exists!")
        else:
            admins[username] = {"password": password}
            messagebox.showinfo("Success", "Admin registered successfully!")
            switch_frame(landing_page)

def login():
    role = login_role.get()
    username = login_username.get().strip()
    password = login_password.get().strip()

    if role == "User":
        if username in users and users[username]["password"] == password:
            messagebox.showinfo("Success", "Login successful!")
            switch_frame(user_page)
        else:
            messagebox.showwarning("Login Error", "Invalid User credentials!")
    elif role == "Admin":
        if username in admins and admins[username]["password"] == password:
            messagebox.showinfo("Success", "Login successful!")
            switch_frame(admin_page)
        else:
            messagebox.showwarning("Login Error", "Invalid Admin credentials!")

# Functions
def switch_frame(frame):
    frame.tkraise()

def open_add_expense_window():
    add_window = tk.Toplevel(root)  # This line must be indented
    add_window.title("Add Expense")
    add_window.geometry("400x300")
    
    tk.Label(add_window, text="Add New Expense", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(add_window, text="Enter Expense Description:").pack(pady=5)
    desc_entry = tk.Entry(add_window, width=30)
    desc_entry.pack()

    tk.Label(add_window, text="Enter Expense Amount:").pack(pady=5)
    amount_entry = tk.Entry(add_window, width=30)
    amount_entry.pack()

    def add_expense_to_list():
        """Adds the expense to the list from the pop-up."""
        try:
            description = desc_entry.get()
            amount = float(amount_entry.get())
            if description and amount > 0:
                expenses.append({'amount': amount, 'description': description})
                messagebox.showinfo("Success", "Expense added!")
                add_window.destroy()  # Close the window after successful addition
            else:
                messagebox.showwarning("Input Error", "Please enter valid data.")
        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a valid number.")

    tk.Button(add_window, text="Add Expense", command=add_expense_to_list, width=20).pack(pady=20)
    tk.Button(add_window, text="Cancel", command=add_window.destroy, width=20).pack()


def view_expenses():
    view_window = tk.Toplevel(root)
    view_window.title("View Expenses")
    view_window.geometry("500x400")
    tk.Label(view_window, text="Expense List", font=("Arial", 14, "bold")).pack(pady=10)
    for i, expense in enumerate(expenses, start=1):
        tk.Label(view_window, text=f"{i}. {expense['description']} - ₹{expense['amount']}").pack()
    tk.Button(view_window, text="Show Graph", command=show_graph, width=20).pack(pady=10)

def show_graph():
    if expenses:
        amounts = [expense['amount'] for expense in expenses]
        descriptions = [expense['description'] for expense in expenses]
        plt.figure(figsize=(10, 6))
        plt.bar(descriptions, amounts, color='skyblue')
        plt.xlabel('Descriptions')
        plt.ylabel('Amount (₹)')
        plt.title('Expense Graph')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Info", "No expenses to display!")

def open_delete_expense_window():
    # Create a new window for deleting expense
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Expense")

    # Label asking for the index
    label = tk.Label(delete_window, text="Enter Index to Delete Expense:")
    label.pack(pady=10)

    # Entry to enter the index
    expense_index = tk.StringVar()  # StringVar for the index
    index_entry = tk.Entry(delete_window, textvariable=expense_index)
    index_entry.pack(pady=10)

    # Function to delete the expense
    def delete_expense():
        try:
            index = int(expense_index.get()) - 1  # Convert to 0-based index
            if 0 <= index < len(expenses):  # Validate index
                deleted = expenses.pop(index)  # Delete the expense from the list
                messagebox.showinfo("Deleted", f"Deleted Expense: {deleted['description']} - ₹{deleted['amount']}")
                expense_index.set("")  # Clear the input field
            else:
                messagebox.showwarning("Error", "Invalid Index!")  # Invalid index entered
        except ValueError:
            messagebox.showwarning("Error", "Please enter a valid index!")  # Invalid input type

        delete_window.destroy()  # Close the window after deletion

    # Button to trigger expense deletion
    delete_button = tk.Button(delete_window, text="Delete", command=delete_expense)
    delete_button.pack(pady=5)

def open_update_expense_window():
    """Opens a pop-up window to update an expense based on index."""
    update_window = tk.Toplevel(root)
    update_window.title("Update Expense")
    update_window.geometry("400x300")
    
    tk.Label(update_window, text="Update Expense", font=("Arial", 14, "bold")).pack(pady=10)

    # Ask for Expense Index
    tk.Label(update_window, text="Enter Expense Index:").pack(pady=5)
    index_entry = tk.Entry(update_window, width=30)
    index_entry.pack(pady=5)

    # Ask for Expense Description and Amount (Initially Empty)
    tk.Label(update_window, text="Enter Expense Description:").pack(pady=5)
    updated_description = tk.Entry(update_window, width=30)
    updated_description.pack(pady=5)

    tk.Label(update_window, text="Enter Expense Amount:").pack(pady=5)
    updated_amount = tk.Entry(update_window, width=30)
    updated_amount.pack(pady=5)

    def update_expense_in_list():
        try:
            # Get index and validate
            index = int(index_entry.get()) - 1
            if 0 <= index < len(expenses):
                # Get the new description and amount
                new_description = updated_description.get()
                new_amount = float(updated_amount.get())

                if new_description and new_amount > 0:
                    # Update the expense data
                    expenses[index] = {'amount': new_amount, 'description': new_description}
                    messagebox.showinfo("Success", "Expense updated successfully!")
                    update_window.destroy()  # Close the window after updating
                else:
                    messagebox.showwarning("Error", "Enter valid description and amount!")
            else:
                messagebox.showwarning("Error", "Invalid index entered!")
        except ValueError:
            messagebox.showwarning("Error", "Please enter valid data (index and amount)!")

    # Update Button (When clicked, it updates the expense)
    update_button = tk.Button(update_window, text="Update Expense", command=update_expense_in_list, width=20)
    update_button.pack(pady=20)

    # Cancel button to close the window without saving
    tk.Button(update_window, text="Cancel", command=update_window.destroy, width=20).pack()

def filter_options():
    filter_window = tk.Toplevel(root)
    filter_window.title("Filter Options")
    filter_window.geometry("400x300")

    tk.Label(filter_window, text="Select Filter Option", font=("Arial", 14, "bold")).pack(pady=20)

    filter_choice = tk.StringVar(value="alphabetical")

    tk.Radiobutton(filter_window, text="Alphabetical", variable=filter_choice, value="alphabetical").pack(anchor="w", padx=20)
    tk.Radiobutton(filter_window, text="Low to High (Amount)", variable=filter_choice, value="low_to_high").pack(anchor="w", padx=20)
    tk.Radiobutton(filter_window, text="High to Low (Amount)", variable=filter_choice, value="high_to_low").pack(anchor="w", padx=20)

    def apply_filter():
        key = filter_choice.get()
        if key == "alphabetical":
            filtered = sorted(expenses, key=lambda x: x['description'])
        elif key == "low_to_high":
            filtered = sorted(expenses, key=lambda x: x['amount'])
        elif key == "high_to_low":
            filtered = sorted(expenses, key=lambda x: -x['amount'])

        display_filter_result(filtered)

    tk.Button(filter_window, text="Apply Filter", command=apply_filter, width=20).pack(pady=20)

def display_filter_result(filtered):
    filter_result_window = tk.Toplevel(root)
    filter_result_window.title("Filtered Expenses")
    filter_result_window.geometry("400x400")
    tk.Label(filter_result_window, text="Filtered Expense List", font=("Arial", 14, "bold")).pack(pady=10)
    for i, expense in enumerate(filtered, start=1):
        tk.Label(filter_result_window, text=f"{i}. {expense['description']} - ₹{expense['amount']}").pack()


def set_limit():
    try:
        limit = float(expense_limit.get())
        total = sum(exp['amount'] for exp in expenses)
        if total > limit:
            messagebox.showwarning("Limit Exceeded", f"Total Expenses ₹{total} exceed the limit ₹{limit}")
        else:
            messagebox.showinfo("Within Limit", f"Total Expenses ₹{total} are within the limit ₹{limit}")
        expense_limit.set("")
    except ValueError:
        messagebox.showwarning("Error", "Please enter a valid number!")

def view_recent():
    recent_window = tk.Toplevel(root)
    recent_window.title("Recent Transactions")
    recent_window.geometry("400x300")
    tk.Label(recent_window, text="Recent Transactions", font=("Arial", 14, "bold")).pack(pady=10)
    for i, expense in enumerate(reversed(expenses[-5:]), start=1):
        tk.Label(recent_window, text=f"{i}. {expense['description']} - ₹{expense['amount']}").pack()

    

def admin_view_data():
    if expenses:
        amounts = [expense['amount'] for expense in expenses]
        descriptions = [expense['description'] for expense in expenses]
        plt.figure(figsize=(10, 6))
        plt.bar(descriptions, amounts, color='orange')
        plt.xlabel('Descriptions')
        plt.ylabel('Amount (₹)')
        plt.title('All User Expenses')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    else:
        messagebox.showinfo("Info", "No expenses available to display!")

# Dummy user data
users = {"user1": {"password": "pass123", "expenses": [], "spending_limit": 0}}

# GUI Setup
root = tk.Tk()

# Variables for registration and login
register_username = tk.StringVar()
register_password = tk.StringVar()
register_role = tk.StringVar(value="User")
login_username = tk.StringVar()
login_password = tk.StringVar()
login_role = tk.StringVar(value="User")

# Variables
expense_amount = tk.StringVar()
expense_description = tk.StringVar()
expense_index = tk.StringVar()
update_index = tk.StringVar()
expense_limit = tk.StringVar()

# Frames
landing_page = tk.Frame(root, bg="white")
login_frame = tk.Frame(root, bg="white")
register_frame = tk.Frame(root, bg="white")
admin_page = tk.Frame(root, bg="white")
user_page = tk.Frame(root, bg="white")
for frame in (landing_page,login_frame,register_frame,admin_page,user_page):
    frame.grid(row=0, column=0, sticky='nsew')



# Styles
button_style = {"font": ("Arial", 12), "relief": "ridge", "bd": 3, "width": 15, "height": 1}
label_style = {"font": ("Arial", 12), "anchor": "w"}
root.title("Expense Tracker")
# Landing Page
tk.Label(landing_page, text="Welcome to Expense Tracker", font=("Arial", 18,"bold"),fg='dark blue',bg='white').grid(row=0, column=0, columnspan=2, pady=30)
tk.Label(landing_page, text="Username:",bg='white',font=("Arial",16,'bold')).grid(row=1, column=0, pady=5, sticky="e")
tk.Entry(landing_page, textvariable=login_username).grid(row=1, column=1, pady=5)
tk.Label(landing_page, text="Password:",bg='white',font=("Arial",16,'bold')).grid(row=2, column=0, pady=5, sticky="e")
tk.Entry(landing_page, textvariable=login_password, show="*").grid(row=2, column=1, pady=5)
tk.Label(landing_page, text="Role:",bg='white',font=("Arial",16,'bold')).grid(row=3, column=0, pady=5, sticky="e")
tk.Radiobutton(landing_page, text="User", variable=login_role, value="User",bg='white',font=("Arial",16,'bold')).grid(row=3, column=1, sticky="w")
tk.Radiobutton(landing_page, text="Admin", variable=login_role, value="Admin",bg='white',font=("Arial",16,'bold')).grid(row=4, column=1, sticky="w")
tk.Button(landing_page, text="Login", command=login,  width=20,bg='red',fg='white').grid(row=5, column=0, columnspan=2, pady=10)

# tk.Button(landing_page, text="Login", command=lambda: switch_frame(login_frame), width=20,bg='blue',fg='white').grid(row=1, column=0, pady=40)
tk.Button(landing_page, text="Register", command=lambda: switch_frame(register_frame), width=20,bg='green',fg='white').grid(row=6, column=0,columnspan=2, pady=40)

# Login Frame
tk.Label(login_frame, text="Login", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)
tk.Label(login_frame, text="Username:").grid(row=1, column=0, pady=5, sticky="e")
tk.Entry(login_frame, textvariable=login_username).grid(row=1, column=1, pady=5)
tk.Label(login_frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
tk.Entry(login_frame, textvariable=login_password, show="*").grid(row=2, column=1, pady=5)
tk.Label(login_frame, text="Role:").grid(row=3, column=0, pady=5, sticky="e")
tk.Radiobutton(login_frame, text="User", variable=login_role, value="User").grid(row=3, column=1, sticky="w")
tk.Radiobutton(login_frame, text="Admin", variable=login_role, value="Admin").grid(row=4, column=1, sticky="w")
tk.Button(login_frame, text="Login", command=login, width=15).grid(row=5, column=0, columnspan=2, pady=10)

# Register Frame
tk.Label(register_frame, text="Register", font=("Arial", 18)).grid(row=0, column=0, columnspan=2, pady=20)
tk.Label(register_frame, text="Username:").grid(row=1, column=0, pady=5, sticky="e")
tk.Entry(register_frame, textvariable=register_username).grid(row=1, column=1, pady=5)
tk.Label(register_frame, text="Password:").grid(row=2, column=0, pady=5, sticky="e")
tk.Entry(register_frame, textvariable=register_password, show="*").grid(row=2, column=1, pady=5)
tk.Label(register_frame, text="Role:").grid(row=3, column=0, pady=5, sticky="e")
tk.Radiobutton(register_frame, text="User", variable=register_role, value="User").grid(row=3, column=1, sticky="w")
tk.Radiobutton(register_frame, text="Admin", variable=register_role, value="Admin").grid(row=4, column=1, sticky="w")
tk.Button(register_frame, text="Register", command=register, width=15).grid(row=5, column=0, columnspan=2, pady=10)
#tk.Button(user_page, text="Back", command=lambda: switch_frame(landing_page), width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)


# Run the application

tk.Button(user_page, text="Add Expense", command=open_add_expense_window, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# View, Update, Delete Section
tk.Button(user_page, text="View Expenses", command=view_expenses, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(user_page, text="Update Expense", command=open_update_expense_window, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=5)
tk.Button(user_page, text="Delete Expense", command=open_delete_expense_window, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

# Filter Section
tk.Button(user_page, text="Filter Expenses", command=filter_options, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
tk.Label(user_page, text="Set Expense Limit:", width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack()
tk.Entry(user_page, textvariable=expense_limit, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack()
tk.Button(user_page, text="Set Limit", command=set_limit, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(user_page, text="View Recent Transactions", command=view_recent, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
#back button
tk.Button(user_page, text="Back", command=lambda: switch_frame(landing_page), width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

# Updated Admin Page
tk.Label(admin_page, text="Admin Page", font=("Arial", 16)).pack(pady=20)
tk.Button(admin_page, text="View User Data (Graph)", command=admin_view_data, width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
tk.Button(admin_page, text="Back", command=lambda: switch_frame(landing_page), width=20, bg="blue", fg="white", font=("Arial", 12, "bold")).pack(pady=10)


#show landing page initially
switch_frame(landing_page)
root.resizable(False,False)
root.config(bg="white")
# Finalize and Run
root.mainloop()