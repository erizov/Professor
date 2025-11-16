#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model-View-ViewModel (MVVM) Design Pattern.

Separates the development of the graphical user interface from the
development of the business logic or back-end logic. The view model
of MVVM is a value converter.
"""

import sys
from pathlib import Path
from abc import ABC, abstractmethod
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from framework.performance_timer import PerformanceTimer
from framework.logging_utils import get_logger
logger = get_logger(__name__)


# Model
class User:
    """User model - data."""
    
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def __str__(self) -> str:
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"


class UserModel:
    """User model - business logic."""
    
    def __init__(self):
        self.users: List[User] = []
        self.next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        """Create user."""
        user = User(self.next_id, name, email)
        self.next_id += 1
        self.users.append(user)
        return user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return self.users.copy()


# ViewModel
class UserViewModel:
    """User ViewModel - presentation logic."""
    
    def __init__(self, model: UserModel):
        self.model = model
        self.selected_user: Optional[User] = None
        self.users: List[User] = []
        self.error_message: str = ""
    
    def load_users(self) -> None:
        """Load users from model."""
        self.users = self.model.get_all_users()
        self.error_message = ""
    
    def create_user(self, name: str, email: str) -> bool:
        """Create user via ViewModel."""
        if not name or not email:
            self.error_message = "Name and email are required"
            return False
        
        if "@" not in email:
            self.error_message = "Invalid email format"
            return False
        
        try:
            self.model.create_user(name, email)
            self.load_users()
            self.error_message = ""
            return True
        except Exception as e:
            self.error_message = str(e)
            return False
    
    def select_user(self, user_id: int) -> None:
        """Select user."""
        self.selected_user = self.model.get_user(user_id)
        if not self.selected_user:
            self.error_message = f"User {user_id} not found"
        else:
            self.error_message = ""
    
    def get_selected_user_name(self) -> str:
        """Get selected user name for view."""
        return self.selected_user.name if self.selected_user else ""
    
    def get_selected_user_email(self) -> str:
        """Get selected user email for view."""
        return self.selected_user.email if self.selected_user else ""
    
    def get_user_count(self) -> int:
        """Get user count for view."""
        return len(self.users)
    
    def has_error(self) -> bool:
        """Check if there's an error."""
        return bool(self.error_message)


# View
class UserView:
    """User view - UI representation."""
    
    def __init__(self, view_model: UserViewModel):
        self.view_model = view_model
    
    def render(self) -> None:
        """Render the view."""
        logger.info("=" * 70)
        logger.info("USER MANAGEMENT VIEW")
        logger.info("=" * 70)
        logger.info()
        
        # Display users
        logger.info(f"Total Users: {self.view_model.get_user_count()}")
        if self.view_model.users:
            logger.info("\nUsers List:")
            for user in self.view_model.users:
                logger.info(f"  {user}")
        else:
            logger.info("\nNo users yet.")
        logger.info()
        
        # Display selected user
        if self.view_model.selected_user:
            logger.info("Selected User:")
            logger.info(f"  Name: {self.view_model.get_selected_user_name()}")
            logger.info(f"  Email: {self.view_model.get_selected_user_email()}")
            logger.info()
        
        # Display errors
        if self.view_model.has_error():
            logger.info(f"Error: {self.view_model.error_message}")
            logger.info()
    
    def show_create_user_form(self, name: str, email: str) -> None:
        """Show create user form (simulated)."""
        logger.info(f"Creating user: {name} ({email})")
        success = self.view_model.create_user(name, email)
        if success:
            logger.info("User created successfully!")
        else:
            logger.info(f"Failed: {self.view_model.error_message}")
        logger.info()
    
    def show_user_details(self, user_id: int) -> None:
        """Show user details (simulated)."""
        self.view_model.select_user(user_id)
        if self.view_model.selected_user:
            logger.info(f"User Details (ID: {user_id}):")
            logger.info(f"  Name: {self.view_model.get_selected_user_name()}")
            logger.info(f"  Email: {self.view_model.get_selected_user_email()}")
        else:
            logger.info(f"User {user_id} not found")
        logger.info()


# Example 2: Task MVVM
class Task:
    """Task model."""
    
    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.task_id = task_id
        self.title = title
        self.completed = completed


class TaskModel:
    """Task model."""
    
    def __init__(self):
        self.tasks: List[Task] = []
        self.next_id = 1
    
    def add_task(self, title: str) -> Task:
        """Add task."""
        task = Task(self.next_id, title)
        self.next_id += 1
        self.tasks.append(task)
        return task
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self.tasks.copy()
    
    def toggle_task(self, task_id: int) -> bool:
        """Toggle task."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = not task.completed
                return True
        return False


class TaskViewModel:
    """Task ViewModel."""
    
    def __init__(self, model: TaskModel):
        self.model = model
        self.tasks: List[Task] = []
        self.filter: str = "all"  # all, active, completed
    
    def load_tasks(self) -> None:
        """Load tasks."""
        self.tasks = self.model.get_tasks()
    
    def add_task(self, title: str) -> None:
        """Add task."""
        self.model.add_task(title)
        self.load_tasks()
    
    def toggle_task(self, task_id: int) -> None:
        """Toggle task."""
        self.model.toggle_task(task_id)
        self.load_tasks()
    
    def set_filter(self, filter_type: str) -> None:
        """Set filter."""
        self.filter = filter_type
        self.load_tasks()
    
    def get_filtered_tasks(self) -> List[Task]:
        """Get filtered tasks."""
        if self.filter == "active":
            return [t for t in self.tasks if not t.completed]
        elif self.filter == "completed":
            return [t for t in self.tasks if t.completed]
        return self.tasks
    
    def get_completed_count(self) -> int:
        """Get completed count."""
        return sum(1 for t in self.tasks if t.completed)
    
    def get_active_count(self) -> int:
        """Get active count."""
        return sum(1 for t in self.tasks if not t.completed)


class TaskView:
    """Task view."""
    
    def __init__(self, view_model: TaskViewModel):
        self.view_model = view_model
    
    def render(self) -> None:
        """Render view."""
        tasks = self.view_model.get_filtered_tasks()
        logger.info(f"Tasks ({self.view_model.filter}):")
        for task in tasks:
            status = "✓" if task.completed else "○"
            logger.info(f"  {status} [{task.task_id}] {task.title}")
        logger.info(f"Active: {self.view_model.get_active_count()}, "
              f"Completed: {self.view_model.get_completed_count()}")
        logger.info()


def main() -> None:
    """Demonstration of MVVM Pattern."""
    logger.info("=" * 70)
    logger.info("MODEL-VIEW-VIEWMODEL (MVVM) PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: User MVVM
    logger.info("Example 1: User Management MVVM")
    logger.info("-" * 70)
    
    # Create MVVM components
    user_model = UserModel()
    user_view_model = UserViewModel(user_model)
    user_view = UserView(user_view_model)
    
    # Load and display
    user_view_model.load_users()
    user_view.render()
    
    # Create users through view
    user_view.show_create_user_form("Alice", "alice@example.com")
    user_view.show_create_user_form("Bob", "bob@example.com")
    user_view.show_create_user_form("Charlie", "invalid-email")  # Error
    
    user_view.render()
    
    # Select user
    user_view.show_user_details(1)
    logger.info()
    
    # Example 2: Task MVVM
    logger.info("Example 2: Task Management MVVM")
    logger.info("-" * 70)
    
    task_model = TaskModel()
    task_view_model = TaskViewModel(task_model)
    task_view = TaskView(task_view_model)
    
    task_view_model.add_task("Learn MVVM")
    task_view_model.add_task("Implement MVVM")
    task_view_model.add_task("Test MVVM")
    
    task_view_model.toggle_task(1)
    task_view_model.toggle_task(3)
    
    task_view.render()
    
    # Filter tasks
    task_view_model.set_filter("active")
    logger.info("Active tasks:")
    task_view.render()
    
    task_view_model.set_filter("completed")
    logger.info("Completed tasks:")
    task_view.render()
    logger.info()
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("MVVM")
    
    def mvvm_operations():
        model = UserModel()
        view_model = UserViewModel(model)
        view = UserView(view_model)
        
        for i in range(10):
            view_model.create_user(f"User{i}", f"user{i}@example.com")
        view_model.load_users()
        return view_model.get_user_count()
    
    result, metrics = timer.measure(mvvm_operations)
    logger.info(f"Time to create 10 users via MVVM: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Separate the development of the graphical user interface")
    logger.info("  from the development of the business logic. The ViewModel")
    logger.info("  acts as a value converter and presentation logic.")
    logger.info("\nKey Advantages:")
    logger.info("  - Clear separation of concerns")
    logger.info("  - Testable ViewModel")
    logger.info("  - View is independent of Model")
    logger.info("  - Two-way data binding support")
    logger.info("\nKey Disadvantages:")
    logger.info("  - More complex than MVC")
    logger.info("  - Can be overkill for simple UIs")
    logger.info("  - ViewModel can become large")
    logger.info("\nWhen to Use:")
    logger.info("  - Rich client applications")
    logger.info("  - Need two-way data binding")
    logger.info("  - Complex presentation logic")
    logger.info("  - Want to test UI logic separately")
    logger.info("\nCommon Use Cases:")
    logger.info("  - WPF applications (.NET)")
    logger.info("  - Angular applications")
    logger.info("  - Vue.js applications")
    logger.info("  - Mobile applications (Xamarin)")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()