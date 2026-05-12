# Project Planner

A comprehensive project planning and management app for Frappe/ERPNext that streamlines project plan creation, approval workflows, and task execution tracking.

## Features

- **Project Plan Management**: Create and manage detailed project plans with task breakdowns
- **Task Synchronization**: Automatic status synchronization between Tasks, Plan Tasks, and Project Plans
- **Approval Workflow**: Built-in workflow for project plan review and approval
- **Email Notifications**: Automated email notifications for status changes (In Review, Approved, Rejected, Completed)
- **Role-Based Access**: Granular permissions for Projects Manager and Project Member roles
- **Team Management**: Enhanced Project doctype with team member management
- **Custom Field Integration**: Seamless integration with existing Task and Project doctypes

## Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app project_planner
```

## Configuration

### Roles and Permissions

The app automatically creates the following roles upon installation:

- **Projects Manager**: Full access to create, edit, delete, submit, and amend project plans
- **Project Member**: Read and write access to project plans (no delete/submit permissions)
- **System Manager**: Full administrative access

### Custom Fields

The app adds the following custom fields:

**Task Doctype:**
- `custom_assigned_to`: Link to User for task assignment
- `custom_project_plan`: Link to Project Plan for task-plan association

**Project Doctype:**
- `custom_team_members`: Table field for managing project team members
- `Team Tab`: New section for team management

## Usage

### Creating a Project Plan

1. Navigate to Project Planner → Project Plan
2. Click "New" to create a new project plan
3. Fill in the required fields:
   - Project: Select the project
   - Plan Title: Enter a descriptive title
   - Start Date & End Date: Auto-fetched from project dates
   - Assigned To: Select the responsible user
4. Add tasks in the Task Plan tab:
   - Task Title: Name of the task
   - Start Date & End Date: Task timeline
   - Assigned To: Task assignee
   - Priority: Task priority level
5. Submit the plan for review

### Approval Workflow

1. **Draft**: Initial state when creating a project plan
2. **In Review**: Automatically set when plan is submitted for review
3. **Approved**: Projects Manager can approve the plan
4. **Completed**: Automatically set when all tasks are completed

### Task Status Synchronization

When a Task's status changes:
- "Working" → Plan Task status updates to "In Progress"
- "Completed" → Plan Task status updates to "Completed"
- Project Plan status updates based on child task completion:
  - All tasks completed → "Completed"
  - Some tasks completed → "In Review"
  - No tasks completed → "Approved"

### Email Notifications

The app sends automatic email notifications:
- **In Review**: Sent to Projects Managers when plan is submitted
- **Approved/Rejected**: Sent to assigned user when plan is approved/rejected
- **Completed**: Sent to assigned user when all tasks are completed
- **Daily Reminders**: Sent to Projects Managers for plans pending review

## Architecture

### Key Components

- **Project Plan Doctype**: Main document for project plans
- **Plan Task Doctype**: Child table for task breakdown
- **API Hooks**: Task update hooks for status synchronization
- **Notification System**: Email notification handlers
- **Permissions Module**: Role-based access control
- **Installation Script**: Automated setup of roles and permissions

### File Structure

```
project_planner/
├── project_planner/
│   ├── doctype/
│   │   ├── project_plan/
│   │   └── plan_task/
│   ├── api.py              # Task synchronization hooks
│   ├── notification.py     # Email notification handlers
│   ├── permissions.py      # Permission query conditions
│   ├── install.py          # Installation setup script
│   └── custom/             # Custom field definitions
├── fixtures/               # Workflow and workflow state fixtures
└── hooks.py               # App hooks configuration
```

## Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/project_planner
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

## License

MIT
