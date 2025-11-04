"""
Monolithic Architecture Example: Todo Manager (Test-Driven Development)
======================================================================

This is a Test-Driven Development (TDD) exercise demonstrating monolithic architecture.
Your task is to make all the tests pass by implementing the required functions.

ARCHITECTURAL CHARACTERISTICS:
- Single file/module containing all functionality
- Direct access to global data structures
- Simple procedural programming approach
- Tight coupling between all components
- Easy to understand and develop initially
- Single point of deployment

TDD APPROACH:
1. Read and understand the tests (they define the requirements)
2. Run the tests (they will fail initially)
3. Implement just enough code to make tests pass
4. Refactor if needed
5. Repeat until all tests pass

LEARNING OBJECTIVES:
- Understand monolithic architecture characteristics
- Practice Test-Driven Development
- Learn Python unit testing best practices
- See how tests can drive design and requirements
"""

import unittest
import sys

# --- Global Data Storage ---
# In a monolith, we typically use global variables for data storage
tasks = []


# --- Core Functions (TO BE IMPLEMENTED) ---
# Your job is to implement these functions to make the tests pass

def add_task(description, priority):
    """
    TODO: Implement this function to make the tests pass.

    The tests will tell you exactly what this function should do.
    Look at test_add_task() to understand the requirements.
    """
    pass


def list_all_tasks():
    """
    TODO: Implement this function to make the tests pass.

    Look at test_list_all_tasks() to understand the requirements.
    """
    pass


def mark_task_done(task_id):
    """
    TODO: Implement this function to make the tests pass.

    Look at test_mark_task_done() to understand the requirements.
    """
    pass


def remove_task(task_id):
    """
    TODO: Implement this function to make the tests pass.

    Look at test_remove_task() to understand the requirements.
    """
    pass


def get_task_by_id(task_id):
    """
    TODO: Implement this helper function to make the tests pass.

    Look at test_get_task_by_id() to understand the requirements.
    """
    pass


def clear_all_tasks():
    """
    TODO: Implement this function to make the tests pass.

    This is used for testing - it should remove all tasks.
    """
    pass


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
    print("Implement the functions to make these tests pass!")
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
        print("Your monolithic architecture implementation is complete!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        print()
        print("💡 Tips for success:")
        print("1. Read the test names and assertions carefully")
        print("2. Implement one function at a time")
        print("3. Run tests frequently to get immediate feedback")
        print("4. Look at the test setup and expected return values")
        print()
        print("Start with the simplest functions like clear_all_tasks() and add_task()")

    return result.wasSuccessful()


# --- Simple Demo Functions ---
def demo_tdd_process():
    """
    Demonstrate the TDD process for educational purposes.
    """
    print("📚 Test-Driven Development (TDD) Process:")
    print("1. 🔴 RED: Write a test that fails")
    print("2. 🟢 GREEN: Write minimal code to make it pass")
    print("3. 🔵 REFACTOR: Improve the code while keeping tests green")
    print("4. Repeat!")
    print()
    print("In this exercise:")
    print("- Tests are already written (they define requirements)")
    print("- Your job is to make them pass")
    print("- Tests give you immediate feedback")
    print("- Tests document expected behavior")
    print()


if __name__ == "__main__":
    print("🎯 Monolithic Architecture - Test-Driven Development Exercise")
    print()

    # Show the TDD process
    demo_tdd_process()

    # Run the tests
    success = run_tests()

    if not success:
        print("\n🚀 Ready to start? Here's your roadmap:")
        print("1. Look at the failing tests to understand requirements")
        print("2. Implement clear_all_tasks() first (simplest)")
        print("3. Then add_task() - check test_add_task_creates_correct_structure")
        print("4. Continue with list_all_tasks(), get_task_by_id(), etc.")
        print("5. Run tests after each implementation: python3 this_file.py")
        print()
        print("Good luck! The tests will guide you! 🎉")