# Track That Dough - Expense Tracking Web App

## Overview

**Track That Dough** is a comprehensive expense tracking web application designed to help users manage their personal and team finances effectively. The app provides a user-friendly interface and robust features tailored to three distinct user roles: **User**, **Manager**, and **Admin**. Each role comes with specific permissions and functionalities to ensure a seamless experience.

### Key Features

#### User
- **Dashboard**: Displays an overview of personal expenses with statistics on total, yearly, monthly, and weekly spending.
- **Visualizations**:
  - **Line Graph**: Tracks monthly spending trends over time.
  - **Radar Graph**: Shows the distribution of expenses by category.
- **Expense Management**:
  - Create, edit, and delete personal expenses (name, amount, date, and category).

#### Manager
- **Team Overview**: View a list of team members and their total spending.
- **Reports**: Generate and download Excel reports summarizing team expenses.

#### Admin
- **User Management**:
  - Approve new user registrations.
  - Promote or demote users between **User** and **Manager** roles.
  - Delete users.
- **Team Management**:
  - Create, edit, and delete teams.
  - Assign managers to teams (each team can have only one manager).
- **Category Management**:
  - Create, edit, and delete expense categories (category names must be unique).

---

## Screenshots

### Dashboard
![Dashboard](/screenshots/user_dashboard.png)

### Expense Management
![Expenses](/screenshots/user_expenses.png)
![Add Expense](/screenshots/user_add_expense.png)

### Team Overview (Manager Role)
![Team Overview](/screenshots/manager_my_team.png)

### Admin Panel
![User Management](/screenshots/admin_users.png)
![Team Management](/screenshots/admin_teams.png)
![Category Management](/screenshots/admin_categories.png)

---

## Installation and Setup

### Requirements
- **Docker**
- **Make**

### Steps to Install and Run the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/Matios102/WebAppProject
   cd WebAppProject
   ```

2. Build and start the application using Docker:
   ```bash
   docker-compose up --build
   ```

3. Access the application in your browser at `http://localhost:3000`.

### Running Unit Tests

To run the unit tests, use the following command:
```bash
make unit-test
```

---

## Usage Flow

### 1. Registering New Users
- New users can register through the app.
- Admins must approve new registrations before users can log in and start using the app.

### 2. Expense Management (User Role)
- Users can manage their expenses by adding, editing, or deleting entries.
- Each expense includes:
  - **Name**: A short description of the expense.
  - **Amount**: The cost of the expense.
  - **Date**: The date the expense was incurred.
  - **Category**: A predefined category assigned by the Admin.

### 3. Team Management (Manager Role)
- Managers can view their team’s expenses and download detailed reports in Excel format.

### 4. Administration (Admin Role)
Admins are responsible for:
- Approving new users.
- Managing teams and assigning managers.
- Creating and managing categories.

---

## Testing the App

You can log in as different roles using the following credentials:

- **Admin**: `admin@admin.com`, password: `admin`
- **Manager**: `manager@manager.com`, password: `manager`
- **User**: `user@user.com`, password: `user`

These accounts come preloaded with sample data for testing purposes.

---

## Project Structure

```
.
├── backend/
│   ├── Dockerfile.backend
│   ├── requirements.txt
│   ├── wait-for-it.sh
│   └── app/
│       ├── __init__.py
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── core/
│       ├── repositories/
│       ├── routers/
│       ├── schemas/
│       └── utils/
├── frontend/
├── tests/
│   ├── test_auth.py
│   ├── test_category.py
│   ├── test_expense.py
│   ├── test_team.py
│   └── test_user.py
├── docker-compose.yml
├── Makefile
└── README.md
```

---