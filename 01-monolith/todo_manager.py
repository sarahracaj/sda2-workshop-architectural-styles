"""
Monolithic Architecture Example: Todo Manager (Test-Driven Development) - SOLUTION
=================================================================================

This is the complete solution that passes all tests, demonstrating both:
1. Monolithic architecture characteristics
2. Test-driven development best practices

ARCHITECTURAL CHARACTERISTICS DEMONSTRATED:
- Single file/module containing all functionality
- Direct access to global data structures
- Simple procedural programming approach
- Tight coupling between all components
- Easy to understand and develop initially
- Single point of deployment

TDD LESSONS LEARNED:
- Tests drive the design and requirements
- Tests provide immediate feedback
- Tests document expected behavior
- Tests prevent regressions
- Red-Green-Refactor cycle
"""

import unittest
import sys

# --- Global Data Storage ---
# In a monolith, we typically use global variables for data storage
tasks = []


# --- Core Functions (IMPLEMENTED TO PASS TESTS) ---

def add_task(description, priority):
    """
    Adds a new task to the global tasks list.

    Implementation driven by test requirements:
    - Must generate unique, sequential IDs
    - Must create task with correct structure
    - Must return success message
    """
    task_id = len(tasks) + 1  # Simple sequential ID generation

    task = {
        "id": task_id,
        "description": description,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    return f"Task {task_id} added successfully!"


def list_all_tasks():
    """
    Returns all tasks sorted by priority.

    Implementation driven by test requirements:
    - Must return empty list when no tasks
    - Must sort by priority (ascending)
    - Must return actual task objects
    """
    if not tasks:
        return []

    # Sort by priority (1 = highest, 5 = lowest)
    return sorted(tasks, key=lambda task: task["priority"])


def mark_task_done(task_id):
    """
    Marks a task as completed.

    Implementation driven by test requirements:
    - Must find task by ID
    - Must set completed = True
    - Must return appropriate messages
    - Must handle non-existent tasks
    """
    task = get_task_by_id(task_id)

    if task is None:
        return f"Task {task_id} not found!"

    if task["completed"]:
        return f"Task {task_id} is already completed!"

    task["completed"] = True
    return f"Task {task_id} marked as completed!"


def remove_task(task_id):
    """
    Removes a task from the global tasks list.

    Implementation driven by test requirements:
    - Must remove task with matching ID
    - Must handle non-existent tasks
    - Must return appropriate messages
    """
    global tasks

    original_length = len(tasks)
    tasks = [task for task in tasks if task["id"] != task_id]

    if len(tasks) < original_length:
        return f"Task {task_id} removed successfully!"
    else:
        return f"Task {task_id} not found!"


def get_task_by_id(task_id):
    """
    Helper function to find a task by ID.

    Implementation driven by test requirements:
    - Must return task object if found
    - Must return None if not found
    - Used by other functions for DRY principle
    """
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def clear_all_tasks():
    """
    Removes all tasks from the global list.

    Implementation driven by test requirements:
    - Needed for test isolation
    - Must completely empty the tasks list
    """
    global tasks
    tasks.clear()


# --- Test Suite ---
class TestTodoManager(unittest.TestCase):
    """
    Test suite that defines the requirements for our monolithic todo manager.

    These tests serve as:
    1. Requirements specification
    2. Design documentation
    3. Acceptance criteria
    4. Regression protection

    Read these tests carefully - they tell you exactly what to implement!
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_tasks()

    def test_clear_all_tasks(self):
        """Test that we can clear all tasks (needed for test isolation)."""
        # First add some tasks
        add_task("Test task", 1)
        add_task("Another task", 2)

        # Then clear them
        clear_all_tasks()

        # Should have no tasks
        self.assertEqual(len(tasks), 0)

    def test_add_task_creates_correct_structure(self):
        """Test that add_task creates a task with the correct structure."""
        result = add_task("Buy groceries", 2)

        # Should return a success message
        self.assertIn("Task", result)
        self.assertIn("added", result.lower())

        # Should add exactly one task
        self.assertEqual(len(tasks), 1)

        # Task should have correct structure
        task = tasks[0]
        self.assertIn("id", task)
        self.assertIn("description", task)
        self.assertIn("priority", task)
        self.assertIn("completed", task)

        # Task should have correct values
        self.assertEqual(task["description"], "Buy groceries")
        self.assertEqual(task["priority"], 2)
        self.assertEqual(task["completed"], False)
        self.assertIsInstance(task["id"], int)
        self.assertGreater(task["id"], 0)

    def test_add_task_generates_unique_ids(self):
        """Test that add_task generates unique, sequential IDs."""
        add_task("First task", 1)
        add_task("Second task", 2)
        add_task("Third task", 3)

        # Should have 3 tasks
        self.assertEqual(len(tasks), 3)

        # IDs should be unique and sequential
        ids = [task["id"] for task in tasks]
        self.assertEqual(ids, [1, 2, 3])

    def test_list_all_tasks_empty(self):
        """Test list_all_tasks returns empty list when no tasks exist."""
        result = list_all_tasks()
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)

    def test_list_all_tasks_sorted_by_priority(self):
        """Test that list_all_tasks returns tasks sorted by priority."""
        add_task("Low priority", 5)
        add_task("High priority", 1)
        add_task("Medium priority", 3)

        result = list_all_tasks()

        # Should return all 3 tasks
        self.assertEqual(len(result), 3)

        # Should be sorted by priority (1, 3, 5)
        priorities = [task["priority"] for task in result]
        self.assertEqual(priorities, [1, 3, 5])

        # Should be the actual task objects
        self.assertEqual(result[0]["description"], "High priority")
        self.assertEqual(result[1]["description"], "Medium priority")
        self.assertEqual(result[2]["description"], "Low priority")

    def test_get_task_by_id_existing(self):
        """Test get_task_by_id returns correct task for existing ID."""
        add_task("Find me", 1)
        add_task("Not me", 2)

        result = get_task_by_id(1)

        self.assertIsNotNone(result)
        self.assertEqual(result["description"], "Find me")
        self.assertEqual(result["id"], 1)

    def test_get_task_by_id_nonexistent(self):
        """Test get_task_by_id returns None for non-existent ID."""
        add_task("Only task", 1)

        result = get_task_by_id(999)

        self.assertIsNone(result)

    def test_mark_task_done_existing_task(self):
        """Test marking an existing task as done."""
        add_task("Complete me", 1)

        result = mark_task_done(1)

        # Should return success message
        self.assertIn("completed", result.lower())
        self.assertIn("1", result)

        # Task should be marked as completed
        task = get_task_by_id(1)
        self.assertTrue(task["completed"])

    def test_mark_task_done_nonexistent_task(self):
        """Test marking a non-existent task as done."""
        result = mark_task_done(999)

        # Should return error message
        self.assertIn("not found", result.lower())
        self.assertIn("999", result)

    def test_mark_task_done_already_completed(self):
        """Test marking an already completed task as done."""
        add_task("Already done", 1)
        mark_task_done(1)  # Mark it once

        result = mark_task_done(1)  # Mark it again

        # Should handle gracefully (either success or already completed message)
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_remove_task_existing(self):
        """Test removing an existing task."""
        add_task("Remove me", 1)
        add_task("Keep me", 2)

        result = remove_task(1)

        # Should return success message
        self.assertIn("removed", result.lower())
        self.assertIn("1", result)

        # Should have only one task left
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]["description"], "Keep me")

    def test_remove_task_nonexistent(self):
        """Test removing a non-existent task."""
        add_task("Only task", 1)

        result = remove_task(999)

        # Should return error message
        self.assertIn("not found", result.lower())
        self.assertIn("999", result)

        # Should still have the original task
        self.assertEqual(len(tasks), 1)

    def test_monolithic_characteristics(self):
        """Test that our implementation demonstrates monolithic characteristics."""
        # All functions should work with the same global data
        add_task("Test task", 1)

        # Direct access to global tasks list
        self.assertEqual(len(tasks), 1)

        # Functions should directly modify global state
        original_task = tasks[0]
        mark_task_done(original_task["id"])

        # The same object should be modified (reference equality)
        self.assertIs(tasks[0], original_task)
        self.assertTrue(tasks[0]["completed"])


class TestIntegration(unittest.TestCase):
    """
    Integration tests that verify the complete workflow.
    These test realistic usage scenarios.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_tasks()

    def test_complete_workflow(self):
        """Test a complete user workflow."""
        # Add several tasks
        add_task("Buy groceries", 3)
        add_task("Study for exam", 1)
        add_task("Call dentist", 2)

        # List tasks (should be sorted by priority)
        all_tasks = list_all_tasks()
        self.assertEqual(len(all_tasks), 3)
        self.assertEqual(all_tasks[0]["priority"], 1)  # Study first
        self.assertEqual(all_tasks[1]["priority"], 2)  # Call second
        self.assertEqual(all_tasks[2]["priority"], 3)  # Groceries last

        # Complete the most important task
        mark_task_done(2)  # Study for exam (ID 2)

        # Verify it's marked as done
        study_task = get_task_by_id(2)
        self.assertTrue(study_task["completed"])

        # Remove a task
        remove_task(1)  # Remove groceries

        # Should have 2 tasks left
        remaining_tasks = list_all_tasks()
        self.assertEqual(len(remaining_tasks), 2)

        # Groceries should be gone
        groceries_task = get_task_by_id(1)
        self.assertIsNone(groceries_task)

    def test_edge_cases(self):
        """Test edge cases and error conditions."""
        # Operations on empty list
        self.assertEqual(list_all_tasks(), [])
        self.assertIsNone(get_task_by_id(1))
        self.assertIn("not found", mark_task_done(1).lower())
        self.assertIn("not found", remove_task(1).lower())

        # Add task and test boundary conditions
        add_task("Test", 1)

        # Valid operations
        self.assertIsNotNone(get_task_by_id(1))

        # Invalid operations
        self.assertIsNone(get_task_by_id(0))
        self.assertIsNone(get_task_by_id(-1))


def run_tests():
    """
    Run all tests and provide detailed feedback.
    This helps students understand what they need to implement.
    """
    print("🧪 Running Test Suite for Monolithic Todo Manager")
    print("=" * 60)
    print()
    print("These tests define exactly what your functions should do.")
    print("All tests should pass in this solution file!")
    print()

    # Capture test output
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromModule(sys.modules[__name__])

    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 Congratulations! All tests pass!")
        print("This demonstrates a complete monolithic architecture implementation!")
        print()
        print("🏗️  Monolithic Architecture Characteristics Demonstrated:")
        print("✅ Single file with all functionality")
        print("✅ Global data structures (tasks list)")
        print("✅ Direct function calls and tight coupling")
        print("✅ Simple procedural programming")
        print("✅ Easy to understand and develop")
        print("✅ Single deployment unit")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        print("This shouldn't happen in the solution file!")

    return result.wasSuccessful()


# --- Interactive Demo Functions ---
def display_tasks():
    """Display all tasks in a user-friendly format."""
    all_tasks = list_all_tasks()

    if not all_tasks:
        print("\n📝 No tasks available!")
        return

    print(f"\n📋 Todo List ({len(all_tasks)} task(s)):")
    print("-" * 65)

    for task in all_tasks:
        status_icon = "✅" if task["completed"] else "❌"
        priority_icon = ["🔴", "🟠", "🟡", "🟢", "🔵"][task["priority"] - 1]

        print(f"{status_icon} [{task['id']:2d}] {task['description']:<35} "
              f"{priority_icon} P{task['priority']}")

    print("-" * 65)


def interactive_demo():
    """
    Interactive demo showing the monolithic architecture in action.
    """
    print("🚀 Interactive Demo - Monolithic Todo Manager")
    print("=" * 50)

    clear_all_tasks()

    # Add some sample tasks
    print("\n1. Adding sample tasks...")
    print(add_task("Learn Python", 1))
    print(add_task("Build a project", 2))
    print(add_task("Deploy to production", 3))
    print(add_task("Write documentation", 2))

    # Show all tasks
    print("\n2. Listing all tasks (sorted by priority):")
    display_tasks()

    # Mark one as done
    print("\n3. Marking 'Learn Python' as completed...")
    print(mark_task_done(1))
    display_tasks()

    # Remove a task
    print("\n4. Removing 'Deploy to production'...")
    print(remove_task(3))
    display_tasks()

    # Show final state
    print("\n5. Final state - remaining tasks:")
    remaining = list_all_tasks()
    print(f"Total tasks: {len(remaining)}")
    for task in remaining:
        status = "✅ Completed" if task["completed"] else "❌ Pending"
        print(f"  Task {task['id']}: {task['description']} - {status}")

    print("\n🎉 Demo completed!")
    print("\nThis demonstrates key monolithic characteristics:")
    print("- All functions access the same global 'tasks' list")
    print("- Direct function calls with no abstraction layers")
    print("- Simple, tightly-coupled design")
    print("- Everything in one file/module")


if __name__ == "__main__":
    print("🎯 Monolithic Architecture - Complete Solution")
    print()

    # Run the tests to prove everything works
    success = run_tests()

    if success:
        print("\n" + "=" * 60)
        print("Would you like to see an interactive demo? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response in ['y', 'yes']:
                print()
                interactive_demo()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")

    print("\n📚 Learning Summary:")
    print("✅ Test-Driven Development guides implementation")
    print("✅ Tests serve as requirements and documentation")
    print("✅ Monolithic architecture: simple but tightly coupled")
    print("✅ Global state makes everything easily accessible")
    print("✅ Perfect for small applications and rapid prototyping")