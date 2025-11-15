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
        print(f"User Details:")
        print(f"  ID: {user.user_id}")
        print(f"  Name: {user.name}")
        print(f"  Email: {user.email}")
        print()
    
    def display_users(self, users: List[User]) -> None:
        """Display list of users."""
        print("Users List:")
        for user in users:
            print(f"  {user}")
        print()
    
    def display_message(self, message: str) -> None:
        """Display message."""
        print(f"Message: {message}")
        print()
    
    def display_error(self, error: str) -> None:
        """Display error."""
        print(f"Error: {error}")
        print()


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
        print("Tasks:")
        for task in tasks:
            print(f"  {task}")
        print()


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
    print("=" * 70)
    print("MODEL-VIEW-CONTROLLER (MVC) PATTERN DEMONSTRATION")
    print("=" * 70)
    print()
    
    # Example 1: User MVC
    print("Example 1: User Management MVC")
    print("-" * 70)
    
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
    print("Example 2: Task Management MVC")
    print("-" * 70)
    
    task_model = TaskModel()
    task_view = TaskView()
    task_controller = TaskController(task_model, task_view)
    
    task_controller.add_task("Learn MVC Pattern")
    task_controller.add_task("Implement MVC in project")
    task_controller.add_task("Write MVC documentation")
    
    task_controller.toggle_task(1)
    task_controller.toggle_task(3)
    
    # Example 3: Performance measurement
    print("Example 3: Performance Measurement")
    print("-" * 70)
    
    timer = PerformanceTimer("MVC")
    
    def mvc_operation():
        model = UserModel()
        view = UserView()
        controller = UserController(model, view)
        controller.create_user("Test", "test@example.com")
        return controller
    
    result, metrics = timer.measure(mvc_operation)
    print(f"Time to create MVC and perform operation: "
          f"{metrics['execution_time_ms']:.3f} ms")
    print()
    
    print("=" * 70)
    print("\nPattern Summary:")
    print("\nIntent:")
    print("  Separate application into three interconnected components:")
    print("  - Model: Data and business logic")
    print("  - View: User interface")
    print("  - Controller: Handles input and coordinates Model/View")
    print("\nKey Advantages:")
    print("  - Separation of concerns")
    print("  - Multiple views for same model")
    print("  - Easy to test")
    print("  - Reusable components")
    print("\nKey Disadvantages:")
    print("  - Can be complex for simple applications")
    print("  - Tight coupling between components")
    print("  - View updates can be inefficient")
    print("\nWhen to Use:")
    print("  - Web applications")
    print("  - Desktop GUI applications")
    print("  - Applications with multiple views")
    print("  - Need separation of concerns")
    print("\nCommon Use Cases:")
    print("  - Web frameworks (Spring MVC, ASP.NET MVC)")
    print("  - Desktop applications")
    print("  - Mobile applications")
    print("  - RESTful APIs")
    print("=" * 70)


if __name__ == "__main__":
    main()
