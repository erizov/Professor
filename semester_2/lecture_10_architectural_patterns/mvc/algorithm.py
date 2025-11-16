#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Model-View-Controller (MVC) Design Pattern.

Separates application into three interconnected components:
- Model: Data and business logic
- View: User interface
- Controller: Handles user input and coordinates Model and View
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
    """User model - represents data."""
    
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email
    
    def __str__(self) -> str:
        return f"User(id={self.user_id}, name='{self.name}', email='{self.email}')"


class UserModel:
    """User model - business logic and data access."""
    
    def __init__(self):
        self.users: List[User] = []
        self.next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        """Create a new user."""
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
    
    def update_user(self, user_id: int, name: str = None, 
                   email: str = None) -> bool:
        """Update user."""
        user = self.get_user(user_id)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            return True
        return False
    
    def delete_user(self, user_id: int) -> bool:
        """Delete user."""
        user = self.get_user(user_id)
        if user:
            self.users.remove(user)
            return True
        return False


# View
class UserView:
    """User view - displays data to user."""
    
    def display_user(self, user: User) -> None:
        """Display single user."""
        logger.info(f"User Details:")
        logger.info(f"  ID: {user.user_id}")
        logger.info(f"  Name: {user.name}")
        logger.info(f"  Email: {user.email}")
        logger.info()
    
    def display_users(self, users: List[User]) -> None:
        """Display list of users."""
        logger.info("Users List:")
        for user in users:
            logger.info(f"  {user}")
        logger.info()
    
    def display_message(self, message: str) -> None:
        """Display message."""
        logger.info(f"Message: {message}")
        logger.info()
    
    def display_error(self, error: str) -> None:
        """Display error."""
        logger.info(f"Error: {error}")
        logger.info()


# Controller
class UserController:
    """User controller - handles user input and coordinates Model/View."""
    
    def __init__(self, model: UserModel, view: UserView):
        self.model = model
        self.view = view
    
    def create_user(self, name: str, email: str) -> None:
        """Handle create user request."""
        try:
            user = self.model.create_user(name, email)
            self.view.display_message(f"User created: {user.name}")
        except Exception as e:
            self.view.display_error(str(e))
    
    def show_user(self, user_id: int) -> None:
        """Handle show user request."""
        user = self.model.get_user(user_id)
        if user:
            self.view.display_user(user)
        else:
            self.view.display_error(f"User {user_id} not found")
    
    def show_all_users(self) -> None:
        """Handle show all users request."""
        users = self.model.get_all_users()
        if users:
            self.view.display_users(users)
        else:
            self.view.display_message("No users found")
    
    def update_user(self, user_id: int, name: str = None, 
                   email: str = None) -> None:
        """Handle update user request."""
        if self.model.update_user(user_id, name, email):
            self.view.display_message(f"User {user_id} updated")
        else:
            self.view.display_error(f"User {user_id} not found")
    
    def delete_user(self, user_id: int) -> None:
        """Handle delete user request."""
        if self.model.delete_user(user_id):
            self.view.display_message(f"User {user_id} deleted")
        else:
            self.view.display_error(f"User {user_id} not found")


# Example 2: Task MVC
class Task:
    """Task model."""
    
    def __init__(self, task_id: int, title: str, completed: bool = False):
        self.task_id = task_id
        self.title = title
        self.completed = completed
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"{status} [{self.task_id}] {self.title}"


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
        """Toggle task completion."""
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = not task.completed
                return True
        return False


class TaskView:
    """Task view."""
    
    def render_tasks(self, tasks: List[Task]) -> None:
        """Render tasks."""
        logger.info("Tasks:")
        for task in tasks:
            logger.info(f"  {task}")
        logger.info()


class TaskController:
    """Task controller."""
    
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view
    
    def add_task(self, title: str) -> None:
        """Add task."""
        self.model.add_task(title)
        self.refresh_view()
    
    def toggle_task(self, task_id: int) -> None:
        """Toggle task."""
        self.model.toggle_task(task_id)
        self.refresh_view()
    
    def refresh_view(self) -> None:
        """Refresh view."""
        tasks = self.model.get_tasks()
        self.view.render_tasks(tasks)


def main() -> None:
    """Demonstration of MVC Pattern."""
    logger.info("=" * 70)
    logger.info("MODEL-VIEW-CONTROLLER (MVC) PATTERN DEMONSTRATION")
    logger.info("=" * 70)
    logger.info()
    
    # Example 1: User MVC
    logger.info("Example 1: User Management MVC")
    logger.info("-" * 70)
    
    # Create MVC components
    user_model = UserModel()
    user_view = UserView()
    user_controller = UserController(user_model, user_view)
    
    # Use controller to handle requests
    user_controller.create_user("Alice", "alice@example.com")
    user_controller.create_user("Bob", "bob@example.com")
    user_controller.create_user("Charlie", "charlie@example.com")
    
    user_controller.show_all_users()
    user_controller.show_user(2)
    
    user_controller.update_user(2, name="Robert")
    user_controller.show_user(2)
    
    user_controller.delete_user(1)
    user_controller.show_all_users()
    
    # Example 2: Task MVC
    logger.info("Example 2: Task Management MVC")
    logger.info("-" * 70)
    
    task_model = TaskModel()
    task_view = TaskView()
    task_controller = TaskController(task_model, task_view)
    
    task_controller.add_task("Learn MVC Pattern")
    task_controller.add_task("Implement MVC in project")
    task_controller.add_task("Write MVC documentation")
    
    task_controller.toggle_task(1)
    task_controller.toggle_task(3)
    
    # Example 3: Performance measurement
    logger.info("Example 3: Performance Measurement")
    logger.info("-" * 70)
    
    timer = PerformanceTimer("MVC")
    
    def mvc_operation():
        model = UserModel()
        view = UserView()
        controller = UserController(model, view)
        controller.create_user("Test", "test@example.com")
        return controller
    
    result, metrics = timer.measure(mvc_operation)
    logger.info(f"Time to create MVC and perform operation: "
          f"{metrics['execution_time_ms']:.3f} ms")
    logger.info()
    
    logger.info("=" * 70)
    logger.info("\nPattern Summary:")
    logger.info("\nIntent:")
    logger.info("  Separate application into three interconnected components:")
    logger.info("  - Model: Data and business logic")
    logger.info("  - View: User interface")
    logger.info("  - Controller: Handles input and coordinates Model/View")
    logger.info("\nKey Advantages:")
    logger.info("  - Separation of concerns")
    logger.info("  - Multiple views for same model")
    logger.info("  - Easy to test")
    logger.info("  - Reusable components")
    logger.info("\nKey Disadvantages:")
    logger.info("  - Can be complex for simple applications")
    logger.info("  - Tight coupling between components")
    logger.info("  - View updates can be inefficient")
    logger.info("\nWhen to Use:")
    logger.info("  - Web applications")
    logger.info("  - Desktop GUI applications")
    logger.info("  - Applications with multiple views")
    logger.info("  - Need separation of concerns")
    logger.info("\nCommon Use Cases:")
    logger.info("  - Web frameworks (Spring MVC, ASP.NET MVC)")
    logger.info("  - Desktop applications")
    logger.info("  - Mobile applications")
    logger.info("  - RESTful APIs")
    logger.info("=" * 70)


if __name__ == "__main__":
    main()