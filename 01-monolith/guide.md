# Monolithic Architecture - Test-Driven Development Guide

## 🎯 Learning Objectives

This exercise combines two important concepts:
1. **Monolithic Architecture**: Understanding the characteristics and trade-offs
2. **Test-Driven Development (TDD)**: Using tests to drive design and implementation

## 🧪 The TDD Approach

### Why TDD for Teaching Architecture?

- **Tests define requirements** - No ambiguity about what to implement
- **Immediate feedback** - Know instantly if your implementation is correct
- **Real-world skill** - TDD is a professional development practice
- **Documentation** - Tests serve as living documentation of expected behavior

### The TDD Cycle

```
🔴 RED → 🟢 GREEN → 🔵 REFACTOR → 🔄 REPEAT
```

1. **🔴 RED**: Write a failing test (already done for you)
2. **🟢 GREEN**: Write minimal code to make the test pass
3. **🔵 REFACTOR**: Improve the code while keeping tests green
4. **🔄 REPEAT**: Move to the next test

## 📋 Exercise Structure

### Files in this Exercise

- **`todo_manager.py`** - Your starting point with failing tests
- **`guide.md`** - This guide (optional reading)

### Test Categories

1. **Unit Tests** (`TestTodoManager`)
   - Test individual functions in isolation
   - Define exact requirements for each function
   - Focus on single responsibility

2. **Integration Tests** (`TestIntegration`)
   - Test complete workflows
   - Verify functions work together correctly
   - Test realistic usage scenarios

## 🚀 Getting Started

### Step 1: Understand the Tests

Before writing any code, read through the test file:

```python
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
```

This test tells you exactly what `add_task()` should do:
- Return a string containing "Task" and "added"
- Add one task to the global `tasks` list
- Create a dictionary with specific keys
- Set correct values for each key

### Step 2: Run the Tests

```bash
python3 todo_manager.py
```

You'll see failing tests that tell you what to implement.

### Step 3: Implement Functions One by One

**Recommended Order:**

1. `clear_all_tasks()` - Simplest function
2. `add_task()` - Core functionality
3. `get_task_by_id()` - Helper function used by others
4. `list_all_tasks()` - Requires sorting
5. `mark_task_done()` - Uses helper function
6. `remove_task()` - Most complex logic

### Step 4: Test-Driven Implementation Example

Let's implement `clear_all_tasks()`:

```python
def test_clear_all_tasks(self):
    """Test that we can clear all tasks."""
    add_task("Test task", 1)
    add_task("Another task", 2)
    
    clear_all_tasks()
    
    self.assertEqual(len(tasks), 0)  # Should be empty
```

**Reading the test:**
- After calling `clear_all_tasks()`, the `tasks` list should be empty
- Length should be 0

**Implementation:**
```python
def clear_all_tasks():
    global tasks
    tasks.clear()  # or tasks = []
```

**Verify:** Run tests again - this test should now pass!

## 🏗️ Monolithic Architecture Characteristics

As you implement the functions, notice these monolithic patterns:

### 1. Global Shared State
```python
tasks = []  # Global variable accessed by all functions
```

### 2. Direct Function Calls
```python
def mark_task_done(task_id):
    task = get_task_by_id(task_id)  # Direct call, no abstraction
    if task is None:
        return f"Task {task_id} not found!"
```

### 3. Tight Coupling
- All functions depend on the global `tasks` structure
- Changes to data format affect all functions
- No abstraction layers or interfaces

### 4. Single Deployment Unit
- Everything in one file
- Easy to deploy and run
- Simple dependencies

## 🎓 Learning Tips

### For Students New to TDD

1. **Read error messages carefully** - They tell you exactly what's wrong
2. **Implement incrementally** - Don't try to write perfect code immediately
3. **Run tests frequently** - After each small change
4. **Focus on making tests pass** - Optimization comes later

### For Students New to Testing

1. **Tests are specifications** - They define what the code should do
2. **Green is good** - Passing tests mean working code
3. **Tests catch regressions** - They prevent you from breaking existing functionality
4. **Tests are documentation** - They show how to use your functions

### Common Pitfalls

1. **Don't overthink** - Implement exactly what the tests require
2. **Read assertions carefully** - `assertEqual(a, b)` means a must equal b
3. **Check return types** - Tests expect specific types (string, list, None)
4. **Handle edge cases** - Tests include empty lists, invalid IDs, etc.

## 🔄 The TDD Workflow in Practice

### Example: Implementing `add_task()`

1. **Read the test:**
   ```python
   def test_add_task_creates_correct_structure(self):
       result = add_task("Buy groceries", 2)
       self.assertIn("Task", result)  # Return string with "Task"
       self.assertEqual(len(tasks), 1)  # Add exactly one task
       # ... more assertions
   ```

2. **Implement minimal code:**
   ```python
   def add_task(description, priority):
       return "Task added"  # Just to pass first assertion
   ```

3. **Run test - see more failures**

4. **Add more code:**
   ```python
   def add_task(description, priority):
       task = {"id": 1, "description": description, 
               "priority": priority, "completed": False}
       tasks.append(task)
       return "Task added"
   ```

5. **Run test - see more failures about ID generation**

6. **Fix ID generation:**
   ```python
   def add_task(description, priority):
       task_id = len(tasks) + 1
       task = {"id": task_id, "description": description, 
               "priority": priority, "completed": False}
       tasks.append(task)
       return f"Task {task_id} added successfully!"
   ```

7. **Run test - should pass!**

## 🎉 Success Criteria

You've successfully completed the exercise when:

- ✅ All tests pass
- ✅ You understand why each function is implemented the way it is
- ✅ You can explain the monolithic architecture characteristics
- ✅ You appreciate how tests guided your implementation

## 🚀 Next Steps

After completing this exercise:

1. **Compare with solution** - See if your implementation differs
2. **Run the interactive demo** - See your code in action
3. **Reflect on the architecture** - What are the pros and cons?
4. **Prepare for layered architecture** - How might this be different?

## 💡 Discussion Questions

1. **Architecture**: What makes this a "monolithic" design?
2. **Scalability**: What problems might arise as this application grows?
3. **Testing**: How did TDD influence your implementation decisions?
4. **Maintainability**: What would happen if requirements changed?
5. **Coupling**: How are the functions dependent on each other?

**Remember:** the tests are your guide, and the goal is to understand both TDD and monolithic architecture principles.
