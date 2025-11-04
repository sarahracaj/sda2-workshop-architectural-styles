"""
Layered Architecture Example: Library Management System (Test-Driven Development)
===============================================================================

This is a Test-Driven Development (TDD) exercise demonstrating layered architecture.
Your task is to make all the tests pass by implementing the required functions
following the layered architecture pattern.

ARCHITECTURAL CHARACTERISTICS:
- Clear separation of concerns across layers
- Each layer only communicates with adjacent layers
- Data flows through layers in a controlled manner
- Business logic is isolated from data access and presentation
- Each layer has a specific responsibility

LAYERS IN THIS SYSTEM:
1. DATA ACCESS LAYER: Direct database/storage operations
2. BUSINESS LOGIC LAYER: Core application rules and workflows
3. PRESENTATION LAYER: User interface and input/output formatting

TDD APPROACH:
1. Read and understand the tests (they define the requirements)
2. Run the tests (they will fail initially)
3. Implement just enough code to make tests pass
4. Follow layered architecture principles
5. Repeat until all tests pass

LEARNING OBJECTIVES:
- Understand layered architecture characteristics and benefits
- Practice proper layer separation and communication
- Learn how layers isolate concerns and dependencies
- See how business logic can be tested independently of UI/data
- Experience how layered design improves maintainability
"""

import unittest
import sys

# --- GLOBAL DATA STORAGE ---
# In layered architecture, data storage is isolated in the data layer
books_db = {}
users_db = {}
transactions_db = []


# --- DATA ACCESS LAYER ---
# This layer handles all direct data storage operations
# It should NOT contain business logic - only CRUD operations

def get_all_books():
    """
    TODO: Implement this data access function.

    Should return a copy of all books in the database.
    Look at test_data_layer_get_all_books() for requirements.
    """
    pass


def get_book_by_id(book_id):
    """
    TODO: Implement this data access function.

    Should return a specific book by ID or None if not found.
    Look at test_data_layer_get_book_by_id() for requirements.
    """
    pass


def save_book(book_id, book_data):
    """
    TODO: Implement this data access function.

    Should save/update a book in the database.
    Look at test_data_layer_save_book() for requirements.
    """
    pass


def get_user_borrowed_books(user_id):
    """
    TODO: Implement this data access function.

    Should return list of book IDs borrowed by a user.
    Look at test_data_layer_user_books() for requirements.
    """
    pass


def save_user_borrowed_book(user_id, book_id):
    """
    TODO: Implement this data access function.

    Should record that a user has borrowed a book.
    Look at test_data_layer_user_books() for requirements.
    """
    pass


def remove_user_borrowed_book(user_id, book_id):
    """
    TODO: Implement this data access function.

    Should remove a book from user's borrowed list.
    Look at test_data_layer_user_books() for requirements.
    """
    pass


def log_transaction(user_id, book_id, action, timestamp):
    """
    TODO: Implement this data access function.

    Should record a transaction (borrow/return) in the transaction log.
    Look at test_data_layer_transactions() for requirements.
    """
    pass


def clear_all_data():
    """
    TODO: Implement this data access function.

    Should clear all data from all databases (for testing).
    """
    pass


# --- BUSINESS LOGIC LAYER ---
# This layer contains all business rules and workflows
# It should ONLY call data access layer functions (not directly access global data)
# It should NOT handle user input/output (that's presentation layer)

def add_book_to_library(title, author, isbn, copies=1):
    """
    TODO: Implement this business logic function.

    Should add a new book to the library with proper validation.
    Must use data access layer functions only.
    Look at test_business_layer_add_book() for requirements.
    """
    pass


def is_book_available_for_borrowing(book_id):
    """
    TODO: Implement this business logic function.

    Should check if a book can be borrowed (exists and has available copies).
    Must use data access layer functions only.
    Look at test_business_layer_availability() for requirements.
    """
    pass


def borrow_book_workflow(user_id, book_id):
    """
    TODO: Implement this business logic function.

    Should handle the complete borrowing workflow with business rules.
    Must use data access layer functions only.
    Look at test_business_layer_borrow() for requirements.
    """
    pass


def return_book_workflow(user_id, book_id):
    """
    TODO: Implement this business logic function.

    Should handle the complete return workflow with validation.
    Must use data access layer functions only.
    Look at test_business_layer_return() for requirements.
    """
    pass


def get_user_borrowed_books_with_details(user_id):
    """
    TODO: Implement this business logic function.

    Should return detailed info about books borrowed by a user.
    Must use data access layer functions only.
    Look at test_business_layer_user_details() for requirements.
    """
    pass


def get_available_books_list():
    """
    TODO: Implement this business logic function.

    Should return list of books that are available for borrowing.
    Must use data access layer functions only.
    Look at test_business_layer_available_books() for requirements.
    """
    pass


# --- PRESENTATION LAYER ---
# This layer handles user interface, input validation, and output formatting
# It should ONLY call business logic layer functions (not data access directly)

def format_book_display(books_list):
    """
    TODO: Implement this presentation function.

    Should format a list of books for display to users.
    Must use business logic layer functions only.
    Look at test_presentation_layer_formatting() for requirements.
    """
    pass


def parse_user_input(input_string, expected_type):
    """
    TODO: Implement this presentation function.

    Should parse and validate user input.
    Look at test_presentation_layer_input_parsing() for requirements.
    """
    pass


def display_user_borrowed_books(user_id):
    """
    TODO: Implement this presentation function.

    Should display a user's borrowed books in a formatted way.
    Must use business logic layer functions only.
    Look at test_presentation_layer_user_display() for requirements.
    """
    pass


# --- TEST SUITE ---
class TestDataAccessLayer(unittest.TestCase):
    """
    Tests for the Data Access Layer - lowest level, direct data operations.
    These tests verify CRUD operations work correctly.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_data()

    def test_clear_all_data(self):
        """Test that clear_all_data removes all data."""
        # Add some test data first
        global books_db, users_db, transactions_db
        books_db[1] = {"title": "Test"}
        users_db["user1"] = [1]
        transactions_db.append({"test": "data"})

        # Clear all data
        clear_all_data()

        # All should be empty
        self.assertEqual(len(books_db), 0)
        self.assertEqual(len(users_db), 0)
        self.assertEqual(len(transactions_db), 0)

    def test_data_layer_get_all_books(self):
        """Test get_all_books returns correct data structure."""
        # Should return empty dict when no books
        result = get_all_books()
        self.assertEqual(result, {})
        self.assertIsInstance(result, dict)

        # Add a book directly to test
        books_db[1] = {"title": "Test Book", "author": "Test Author", "available_copies": 1}

        # Should return the book
        result = get_all_books()
        self.assertEqual(len(result), 1)
        self.assertIn(1, result)
        self.assertEqual(result[1]["title"], "Test Book")

    def test_data_layer_get_book_by_id(self):
        """Test get_book_by_id returns correct book or None."""
        # Should return None for non-existent book
        result = get_book_by_id(999)
        self.assertIsNone(result)

        # Add a book
        books_db[1] = {"title": "Test Book", "author": "Test Author"}

        # Should return the book
        result = get_book_by_id(1)
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Test Book")

        # Should still return None for different ID
        result = get_book_by_id(2)
        self.assertIsNone(result)

    def test_data_layer_save_book(self):
        """Test save_book stores book data correctly."""
        book_data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "123456789",
            "total_copies": 2,
            "available_copies": 2
        }

        # Save the book
        save_book(1, book_data)

        # Should be stored in database
        self.assertIn(1, books_db)
        self.assertEqual(books_db[1]["title"], "New Book")
        self.assertEqual(books_db[1]["total_copies"], 2)

        # Should be able to update existing book
        updated_data = book_data.copy()
        updated_data["available_copies"] = 1
        save_book(1, updated_data)

        self.assertEqual(books_db[1]["available_copies"], 1)

    def test_data_layer_user_books(self):
        """Test user borrowed books operations."""
        # Initially should return empty list
        result = get_user_borrowed_books("user1")
        self.assertEqual(result, [])

        # Save a borrowed book
        save_user_borrowed_book("user1", 1)
        save_user_borrowed_book("user1", 2)

        # Should return list of borrowed books
        result = get_user_borrowed_books("user1")
        self.assertEqual(len(result), 2)
        self.assertIn(1, result)
        self.assertIn(2, result)

        # Remove a borrowed book
        remove_user_borrowed_book("user1", 1)

        # Should have one less book
        result = get_user_borrowed_books("user1")
        self.assertEqual(len(result), 1)
        self.assertIn(2, result)
        self.assertNotIn(1, result)

    def test_data_layer_transactions(self):
        """Test transaction logging."""
        # Log a transaction
        log_transaction("user1", 1, "borrow", "2024-01-01T10:00:00")

        # Should be stored
        self.assertEqual(len(transactions_db), 1)
        transaction = transactions_db[0]
        self.assertEqual(transaction["user_id"], "user1")
        self.assertEqual(transaction["book_id"], 1)
        self.assertEqual(transaction["action"], "borrow")
        self.assertEqual(transaction["timestamp"], "2024-01-01T10:00:00")

        # Log another transaction
        log_transaction("user2", 2, "return", "2024-01-01T11:00:00")

        # Should have two transactions
        self.assertEqual(len(transactions_db), 2)


class TestBusinessLogicLayer(unittest.TestCase):
    """
    Tests for the Business Logic Layer - core application rules.
    These tests verify business workflows and rules are correctly implemented.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_data()

    def test_business_layer_add_book(self):
        """Test add_book_to_library creates book with correct structure."""
        result = add_book_to_library("Test Book", "Test Author", "123456789", 2)

        # Should return success message
        self.assertIsInstance(result, str)
        self.assertIn("added", result.lower())

        # Should create book with correct structure
        books = get_all_books()
        self.assertEqual(len(books), 1)

        book_id = list(books.keys())[0]
        book = books[book_id]
        self.assertEqual(book["title"], "Test Book")
        self.assertEqual(book["author"], "Test Author")
        self.assertEqual(book["isbn"], "123456789")
        self.assertEqual(book["total_copies"], 2)
        self.assertEqual(book["available_copies"], 2)

    def test_business_layer_add_book_validation(self):
        """Test add_book_to_library validates input."""
        # Should reject empty title
        result = add_book_to_library("", "Author", "123456789")
        self.assertIn("error", result.lower())

        # Should reject empty author
        result = add_book_to_library("Title", "", "123456789")
        self.assertIn("error", result.lower())

        # Should reject invalid copies
        result = add_book_to_library("Title", "Author", "123456789", 0)
        self.assertIn("error", result.lower())

    def test_business_layer_availability(self):
        """Test is_book_available_for_borrowing checks correctly."""
        # Non-existent book should not be available
        self.assertFalse(is_book_available_for_borrowing(999))

        # Add a book with available copies
        add_book_to_library("Available Book", "Author", "123456789", 2)
        book_id = list(get_all_books().keys())[0]

        # Should be available
        self.assertTrue(is_book_available_for_borrowing(book_id))

        # Manually set available copies to 0
        book = get_book_by_id(book_id)
        book["available_copies"] = 0
        save_book(book_id, book)

        # Should not be available
        self.assertFalse(is_book_available_for_borrowing(book_id))

    def test_business_layer_borrow(self):
        """Test borrow_book_workflow handles borrowing correctly."""
        # Add a book
        add_book_to_library("Borrowable Book", "Author", "123456789", 1)
        book_id = list(get_all_books().keys())[0]

        # Should successfully borrow
        result = borrow_book_workflow("user1", book_id)
        self.assertIn("borrowed", result.lower())
        self.assertIn("successfully", result.lower())

        # Book should have fewer available copies
        book = get_book_by_id(book_id)
        self.assertEqual(book["available_copies"], 0)

        # User should have the book in their list
        user_books = get_user_borrowed_books("user1")
        self.assertIn(book_id, user_books)

        # Should not be able to borrow the same book again
        result = borrow_book_workflow("user1", book_id)
        self.assertIn("not available", result.lower())

    def test_business_layer_return(self):
        """Test return_book_workflow handles returns correctly."""
        # Add and borrow a book first
        add_book_to_library("Returnable Book", "Author", "123456789", 1)
        book_id = list(get_all_books().keys())[0]
        borrow_book_workflow("user1", book_id)

        # Should successfully return
        result = return_book_workflow("user1", book_id)
        self.assertIn("returned", result.lower())
        self.assertIn("successfully", result.lower())

        # Book should have more available copies
        book = get_book_by_id(book_id)
        self.assertEqual(book["available_copies"], 1)

        # User should not have the book in their list
        user_books = get_user_borrowed_books("user1")
        self.assertNotIn(book_id, user_books)

        # Should not be able to return the same book again
        result = return_book_workflow("user1", book_id)
        self.assertIn("not borrowed", result.lower())

    def test_business_layer_user_details(self):
        """Test get_user_borrowed_books_with_details returns enriched data."""
        # Add books and have user borrow them
        add_book_to_library("Book One", "Author One", "111111111", 1)
        add_book_to_library("Book Two", "Author Two", "222222222", 1)

        books = get_all_books()
        book_ids = list(books.keys())

        borrow_book_workflow("user1", book_ids[0])
        borrow_book_workflow("user1", book_ids[1])

        # Should return detailed information
        result = get_user_borrowed_books_with_details("user1")
        self.assertEqual(len(result), 2)

        # Each item should have book details
        for item in result:
            self.assertIn("book_id", item)
            self.assertIn("title", item)
            self.assertIn("author", item)

    def test_business_layer_available_books(self):
        """Test get_available_books_list returns only available books."""
        # Add books with different availability
        add_book_to_library("Available Book", "Author", "111111111", 2)
        add_book_to_library("Unavailable Book", "Author", "222222222", 1)

        books = get_all_books()
        book_ids = list(books.keys())

        # Borrow one copy of the unavailable book
        borrow_book_workflow("user1", book_ids[1])

        # Should return only available books
        available = get_available_books_list()
        available_titles = [book["title"] for book in available]

        self.assertIn("Available Book", available_titles)
        self.assertNotIn("Unavailable Book", available_titles)


class TestPresentationLayer(unittest.TestCase):
    """
    Tests for the Presentation Layer - user interface and formatting.
    These tests verify proper formatting and input handling.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_data()

    def test_presentation_layer_formatting(self):
        """Test format_book_display creates proper user-friendly output."""
        books = [
            {"book_id": 1, "title": "Book One", "author": "Author One", "available_copies": 2},
            {"book_id": 2, "title": "Book Two", "author": "Author Two", "available_copies": 0}
        ]

        result = format_book_display(books)

        # Should return a string
        self.assertIsInstance(result, str)

        # Should contain book information
        self.assertIn("Book One", result)
        self.assertIn("Author One", result)
        self.assertIn("Book Two", result)

        # Should indicate availability
        self.assertIn("available", result.lower())

    def test_presentation_layer_input_parsing(self):
        """Test parse_user_input handles different input types."""
        # Should parse integers
        result = parse_user_input("123", int)
        self.assertEqual(result, 123)

        # Should parse strings
        result = parse_user_input("test string", str)
        self.assertEqual(result, "test string")

        # Should handle invalid integer input
        result = parse_user_input("not a number", int)
        self.assertIsNone(result)

        # Should strip whitespace
        result = parse_user_input("  test  ", str)
        self.assertEqual(result, "test")

    def test_presentation_layer_user_display(self):
        """Test display_user_borrowed_books formats user data correctly."""
        # Add and borrow books
        add_book_to_library("User Book", "Author", "123456789", 1)
        book_id = list(get_all_books().keys())[0]
        borrow_book_workflow("user1", book_id)

        # Should return formatted string
        result = display_user_borrowed_books("user1")
        self.assertIsInstance(result, str)
        self.assertIn("User Book", result)
        self.assertIn("Author", result)

        # Should handle user with no books
        result = display_user_borrowed_books("user_with_no_books")
        self.assertIsInstance(result, str)
        self.assertIn("no books", result.lower())


class TestLayeredArchitecture(unittest.TestCase):
    """
    Tests that verify proper layered architecture implementation.
    These tests ensure layers are properly separated and communicate correctly.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_data()

    def test_layer_separation_business_uses_data_only(self):
        """Test that business layer functions only call data layer functions."""
        # This is more of a code review test, but we can test behavior
        # Business layer should not directly access global variables

        # Add a book using business layer
        add_book_to_library("Test Book", "Test Author", "123456789", 1)

        # The book should be accessible through data layer
        books = get_all_books()
        self.assertEqual(len(books), 1)

        # Business layer operations should work through data layer
        book_id = list(books.keys())[0]
        available = is_book_available_for_borrowing(book_id)
        self.assertTrue(available)

    def test_complete_workflow_through_layers(self):
        """Test a complete workflow that goes through all layers."""
        # Data layer: Add book directly to test data flow
        save_book(1, {
            "title": "Workflow Book",
            "author": "Workflow Author",
            "isbn": "999999999",
            "total_copies": 1,
            "available_copies": 1
        })

        # Business layer: Check availability and borrow
        self.assertTrue(is_book_available_for_borrowing(1))
        result = borrow_book_workflow("workflow_user", 1)
        self.assertIn("successfully", result.lower())

        # Presentation layer: Display user's books
        display_result = display_user_borrowed_books("workflow_user")
        self.assertIn("Workflow Book", display_result)

        # Business layer: Return the book
        return_result = return_book_workflow("workflow_user", 1)
        self.assertIn("successfully", return_result.lower())

        # Verify final state through data layer
        self.assertTrue(is_book_available_for_borrowing(1))


def run_tests():
    """
    Run all tests and provide detailed feedback for layered architecture.
    """
    print("🧪 Running Test Suite for Layered Architecture Library System")
    print("=" * 70)
    print()
    print("These tests verify proper layered architecture implementation:")
    print("📊 DATA ACCESS LAYER: Direct database operations")
    print("🧠 BUSINESS LOGIC LAYER: Application rules and workflows")
    print("🖥️  PRESENTATION LAYER: User interface and formatting")
    print("🏗️  ARCHITECTURE TESTS: Layer separation and communication")
    print()

    # Run tests with detailed output
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromModule(sys.modules[__name__])

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print("🎉 Congratulations! All tests pass!")
        print("Your layered architecture implementation is complete!")
        print()
        print("🏗️  Layered Architecture Characteristics Demonstrated:")
        print("✅ Clear separation of concerns")
        print("✅ Each layer has specific responsibilities")
        print("✅ Controlled communication between layers")
        print("✅ Business logic isolated from data and UI")
        print("✅ Easier to test and maintain")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        print()
        print("💡 Tips for layered architecture success:")
        print("1. Data layer: Only CRUD operations, no business logic")
        print("2. Business layer: Only call data layer functions")
        print("3. Presentation layer: Only call business layer functions")
        print("4. Each layer should have a single responsibility")
        print("5. Test each layer independently")
        print()
        print("Start with the data access layer functions first!")

    return result.wasSuccessful()


if __name__ == "__main__":
    print("🎯 Layered Architecture - Test-Driven Development Exercise")
    print()
    print("📚 Layer Responsibilities:")
    print("📊 DATA ACCESS: get_all_books(), save_book(), log_transaction(), etc.")
    print("🧠 BUSINESS LOGIC: add_book_to_library(), borrow_book_workflow(), etc.")
    print("🖥️  PRESENTATION: format_book_display(), parse_user_input(), etc.")
    print()

    # Run the tests
    success = run_tests()

    if not success:
        print("\n🚀 Implementation Strategy:")
        print("1. Start with Data Access Layer (simplest CRUD operations)")
        print("2. Move to Business Logic Layer (use only data access functions)")
        print("3. Finish with Presentation Layer (use only business logic functions)")
        print("4. Run tests frequently to verify layer separation")
        print()
        print("Remember: Each layer should only communicate with adjacent layers!")