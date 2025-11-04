# Layered Architecture - Test-Driven Development Guide

## 🎯 Learning Objectives

This exercise teaches layered architecture through hands-on implementation:
1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Controlled Communication**: Layers only talk to adjacent layers
3. **Testability**: Each layer can be tested independently
4. **Maintainability**: Changes in one layer don't affect others
5. **Business Logic Isolation**: Core rules separated from data and UI

## 🏗️ Architecture Overview

### The Three Layers

```
🖥️  PRESENTATION LAYER    ← User Interface & Formatting
     ↕️  (only calls business layer)
🧠 BUSINESS LOGIC LAYER   ← Application Rules & Workflows  
     ↕️  (only calls data layer)
📊 DATA ACCESS LAYER      ← Database Operations (CRUD)
     ↕️
💾 DATA STORAGE           ← Database/Files/Memory
```

### Layer Responsibilities

| Layer | Responsibility | What it Contains | What it CANNOT Do |
|-------|---------------|------------------|-------------------|
| **Presentation** | User interface, formatting, input validation | `format_book_display()`, `parse_user_input()` | Access database directly, contain business rules |
| **Business Logic** | Application rules, workflows, domain logic | `borrow_book_workflow()`, `add_book_to_library()` | Access database directly, handle user input |
| **Data Access** | CRUD operations, data persistence | `get_book_by_id()`, `save_book()` | Contain business rules, format output |

## 🧪 TDD Approach for Layered Architecture

### Why TDD Works Well for Layers

1. **Layer Isolation**: Tests verify each layer works independently
2. **Interface Definition**: Tests define how layers communicate
3. **Dependency Direction**: Tests enforce proper layer communication
4. **Refactoring Safety**: Changes in one layer don't break others

### Test Categories

1. **Data Access Layer Tests**: Pure CRUD operations
2. **Business Logic Layer Tests**: Application rules and workflows
3. **Presentation Layer Tests**: Formatting and input handling
4. **Architecture Tests**: Verify proper layer separation

## 🚀 Implementation Strategy

### Phase 1: Data Access Layer (Bottom-Up)

Start with the foundation - pure data operations:

```python
def test_data_layer_get_book_by_id(self):
    """Test get_book_by_id returns correct book or None."""
    # Should return None for non-existent book
    result = get_book_by_id(999)
    self.assertIsNone(result)
```

**Implementation Tips:**
- Focus only on data storage/retrieval
- No business logic (no validation, no formatting)
- Return raw data structures
- Handle edge cases (empty, not found)

**Functions to Implement:**
1. `clear_all_data()` - Simplest, clears everything
2. `get_all_books()` - Returns dictionary of books
3. `get_book_by_id()` - Returns single book or None
4. `save_book()` - Stores book data
5. `get_user_borrowed_books()` - Returns list of book IDs
6. `save_user_borrowed_book()` - Records borrowing
7. `remove_user_borrowed_book()` - Removes borrowing record
8. `log_transaction()` - Records transaction

### Phase 2: Business Logic Layer (Middle-Out)

Build application rules that use only data access functions:

```python
def test_business_layer_borrow(self):
    """Test borrow_book_workflow handles borrowing correctly."""
    # Add a book
    add_book_to_library("Borrowable Book", "Author", "123456789", 1)
    book_id = list(get_all_books().keys())[0]
    
    # Should successfully borrow
    result = borrow_book_workflow("user1", book_id)
    self.assertIn("borrowed", result.lower())
```

**Implementation Tips:**
- Only call data access layer functions
- Never access global variables directly
- Implement business rules and validation
- Return user-friendly messages
- Handle error conditions

**Functions to Implement:**
1. `add_book_to_library()` - Validates and creates books
2. `is_book_available_for_borrowing()` - Checks availability
3. `borrow_book_workflow()` - Complete borrowing process
4. `return_book_workflow()` - Complete return process
5. `get_user_borrowed_books_with_details()` - Enriched user data
6. `get_available_books_list()` - Filtered book list

### Phase 3: Presentation Layer (Top-Down)

Create user interface that uses only business logic functions:

```python
def test_presentation_layer_formatting(self):
    """Test format_book_display creates proper user-friendly output."""
    books = [
        {"book_id": 1, "title": "Book One", "author": "Author One", "available_copies": 2}
    ]
    
    result = format_book_display(books)
    self.assertIsInstance(result, str)
    self.assertIn("Book One", result)
```

**Implementation Tips:**
- Only call business logic layer functions
- Focus on user experience and formatting
- Handle input parsing and validation
- Create readable, formatted output
- No business rules or data access

**Functions to Implement:**
1. `format_book_display()` - User-friendly book list
2. `parse_user_input()` - Input validation and conversion
3. `display_user_borrowed_books()` - Formatted user book display

## 🎓 Key Learning Points

### 1. Layer Communication Rules

**✅ ALLOWED:**
```python
# Presentation calls Business
def display_user_books(user_id):
    books = get_user_borrowed_books_with_details(user_id)  # ✅ OK
    return format_books(books)

# Business calls Data  
def borrow_book_workflow(user_id, book_id):
    book = get_book_by_id(book_id)  # ✅ OK
    if book and book["available_copies"] > 0:
        # ... business logic
```

**❌ FORBIDDEN:**
```python
# Presentation calling Data directly
def display_user_books(user_id):
    books = get_all_books()  # ❌ WRONG - skips business layer
    
# Business accessing global data
def borrow_book_workflow(user_id, book_id):
    if books_db[book_id]["available_copies"] > 0:  # ❌ WRONG - skips data layer
```

### 2. Single Responsibility Principle

Each layer has ONE job:
- **Data Layer**: Store and retrieve data
- **Business Layer**: Implement application rules
- **Presentation Layer**: Handle user interaction

### 3. Dependency Direction

```
Presentation depends on Business
Business depends on Data
Data depends on Storage

Changes flow UP, dependencies point DOWN
```

### 4. Testing Benefits

```python
# Test business logic without database
def test_borrow_workflow_with_mock_data():
    # Can mock data layer functions
    # Test pure business logic
    
# Test data layer without business rules  
def test_save_book():
    # Test pure CRUD operations
    # No business validation needed
```

## 🔧 Common Implementation Patterns

### Data Layer Pattern: Simple CRUD
```python
def get_book_by_id(book_id):
    """Pure data access - no business logic"""
    return books_db.get(book_id, None)

def save_book(book_id, book_data):
    """Pure data storage - no validation"""
    books_db[book_id] = book_data.copy()
```

### Business Layer Pattern: Rules + Data Calls
```python
def borrow_book_workflow(user_id, book_id):
    """Business logic using only data layer"""
    # Business rule: Check availability
    if not is_book_available_for_borrowing(book_id):
        return "Error: Book not available"
    
    # Business rule: Check if already borrowed
    user_books = get_user_borrowed_books(user_id)  # Data layer call
    if book_id in user_books:
        return "Error: Already borrowed"
    
    # Business workflow: Update data
    book = get_book_by_id(book_id)  # Data layer call
    book["available_copies"] -= 1
    save_book(book_id, book)  # Data layer call
    save_user_borrowed_book(user_id, book_id)  # Data layer call
    
    return f"Book '{book['title']}' borrowed successfully!"
```

### Presentation Layer Pattern: Format + Business Calls
```python
def display_user_borrowed_books(user_id):
    """Presentation using only business layer"""
    # Get data through business layer
    user_books = get_user_borrowed_books_with_details(user_id)  # Business call
    
    # Format for user display
    if not user_books:
        return f"User '{user_id}' has no books borrowed."
    
    output = f"Books borrowed by '{user_id}':\n"
    for book in user_books:
        output += f"[{book['book_id']}] {book['title']} by {book['author']}\n"
    
    return output
```

## 🎯 Success Criteria

You've mastered layered architecture when:

### ✅ Technical Implementation
- All tests pass
- Each layer only calls adjacent layers
- No direct access to global data from business/presentation layers
- Proper error handling at each layer

### ✅ Architectural Understanding
- Can explain the responsibility of each layer
- Understand why layers shouldn't be skipped
- Can identify which layer a new feature belongs in
- Appreciate the benefits of separation of concerns

### ✅ Design Thinking
- Recognize when requirements would affect which layers
- Understand how changes can be isolated to specific layers
- See how testing becomes easier with proper separation
- Appreciate the trade-offs (complexity vs. maintainability)

## 🚧 Common Pitfalls and Solutions

### Pitfall 1: Layer Skipping
**Problem:** Presentation layer calling data layer directly
**Solution:** Always go through business layer, even for simple operations

### Pitfall 2: Business Logic in Wrong Layer
**Problem:** Validation in data layer or business rules in presentation
**Solution:** Remember each layer's single responsibility

### Pitfall 3: God Objects
**Problem:** One function doing everything across layers
**Solution:** Break down into smaller, layer-specific functions

### Pitfall 4: Tight Coupling
**Problem:** Layers knowing too much about each other's internals
**Solution:** Use well-defined interfaces and return values

## 🔄 Comparison with Monolithic Architecture

| Aspect | Monolithic | Layered |
|--------|------------|---------|
| **Complexity** | Simple | More complex |
| **Testing** | Test everything together | Test layers independently |
| **Maintenance** | Changes affect everything | Changes isolated to layers |
| **Understanding** | Everything visible | Clear separation of concerns |
| **Development** | Fast initial development | Slower setup, faster long-term |
| **Debugging** | One place to look | May need to trace through layers |

## 💡 Real-World Applications

### When to Use Layered Architecture
- **Medium to large applications**
- **Multiple developers/teams**
- **Complex business logic**
- **Need for testability**
- **Frequent requirement changes**

### Examples in Industry
- **Web Applications**: Controller → Service → Repository → Database
- **Enterprise Systems**: UI → Business Logic → Data Access → Storage
- **APIs**: Routes → Services → Models → Database

## 🚀 Next Steps

After completing this exercise:
1. **Compare implementations** - How does this differ from monolithic?
2. **Consider variations** - What about 4-layer or 5-layer architectures?
3. **Think about trade-offs** - When is this overkill?
4. **Prepare for event-driven** - How might loose coupling change things?

Remember: Layered architecture is about **managing complexity through separation of concerns**. Each layer has a clear job, and the interfaces between layers are well-defined.

Good luck building your layered library system! 📚