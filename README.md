Track That Dough - Expense Tracking Web App

Overview

Track That Dough is a web application designed to help users track their expenses and view statistics about their spending. The app supports three user roles: User, Manager, and Admin, each with different permissions.

  Users can create, edit, and delete their own expenses.
	Managers can do everything a User can, plus they can view an overview of team members and generate reports (Excel) for their team’s spending.
	Admins manage users, teams, and categories, and can promote/demote users between User and Manager roles.

User Roles and Login Information (for testing):

  Admin: a@a.aaa, password: a  
	Manager: m@m.mmm, password: m  
	User: u@u.uuu, password: u  

Features

User

  Dashboard: Displays an overview of your expenses with statistics on total, yearly, monthly, and weekly spending.
  Line Graph: Monthly spendings over time.
  Radar Graph: Distribution of expenses by category.
  Expenses: A list of your personal expenses where you can:
  Create a new expense (name, amount, date, and category).
  Edit or delete an existing expense.

Manager

  Team Overview: View a list of users assigned to your team, along with their total spendings.
	Reports: Download an Excel report of your team’s spending.

Admin

  Users Page: View all users, with actions to:
	Approve new users.
	Promote/demote users between User and Manager roles.
	Delete users.
	Teams Page: Manage teams (each team can have only one manager), with the ability to:
	Create, edit, or delete teams.
	Assign managers to teams.
	Categories Page: Manage categories (which are fixed for all users), including:
	Create, edit, or delete categories (category names must be unique).

## Installation and Setup

Requirements

  Docker  
	Make

1. Install and Run the App

In the root directory of the project, run the following commands to build and start the application using Docker:

docker-compose up --build

2. Run Unit Tests

To run the unit tests, use the following command:

make unit-test

3. Testing the App

You can log in as different roles using the following credentials:

  Admin: a@a.aaa, password: a
	Manager: m@m.mmm, password: m
	User: u@u.uuu, password: u

These accounts already have some sample data preloaded for testing.

Usage Flow

1. Registering New Users

When a new user registers, they will need to be approved by an Admin before they can log in and start using the app.

2. Expense Management

Users can create, edit, and delete expenses from the Expenses page. Expenses consist of a name, amount, date, and category. Categories are predefined by the Admin and are available to all users.

3. Team Management (Manager Role)

Managers can view their assigned team’s expenses and download reports in Excel format from the Team Page.

4. Administration (Admin Role)

Admins are responsible for:

  Approving new users
	Managing teams and categories
	Promoting and demoting users between User and Manager roles
