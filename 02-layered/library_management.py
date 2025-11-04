"""
Layered Architecture Example: Library Management System (Test-Driven Development) - SOLUTION
==========================================================================================

This is the complete solution demonstrating layered architecture principles
with proper separation of concerns and controlled layer communication.

ARCHITECTURAL CHARACTERISTICS DEMONSTRATED:
- Clear separation of concerns across layers
- Each layer only communicates with adjacent layers
- Data flows through layers in a controlled manner
- Business logic is isolated from data access and presentation
- Each layer has a specific responsibility
- Easier to test, maintain, and modify individual layers

LAYERS IMPLEMENTED:
1. DATA ACCESS LAYER: Direct database/storage operations
2. BUSINESS LOGIC LAYER: Core application rules and workflows
3. PRESENTATION LAYER: User interface and input/output formatting
"""

import unittest
import sys
from datetime import datetime

# --- GLOBAL DATA STORAGE ---
# In layered architecture, data storage is isolated in the data layer
books_db = {}
users_db = {}
transactions_db = []


# --- DATA ACCESS LAYER ---
# This layer handles all direct data storage operations
# It contains NO business logic - only CRUD operations

def get_all_books():
    """
    Retrieves all books from the database.
    Returns a copy to prevent external modification of internal data.
    """
    return books_db.copy()


def get_book_by_id(book_id):
    """
    Retrieves a specific book by its ID.
    Returns None if book is not found.
    """
    return books_db.get(book_id, None)


def save_book(book_id, book_data):
    """
    Saves/updates a book in the database.
    Stores a copy to prevent external modification.
    """
    books_db[book_id] = book_data.copy()


def get_user_borrowed_books(user_id):
    """
    Retrieves list of book IDs borrowed by a user.
    Returns empty list if user has no borrowed books.
    """
    return users_db.get(user_id, []).copy()


def save_user_borrowed_book(user_id, book_id):
    """
    Records that a user has borrowed a book.
    Initializes user record if it doesn't exist.
    """
    if user_id not in users_db:
        users_db[user_id] = []
    if book_id not in users_db[user_id]:
        users_db[user_id].append(book_id)


def remove_user_borrowed_book(user_id, book_id):
    """
    Removes a book from user's borrowed list.
    Does nothing if user or book not found.
    """
    if user_id in users_db and book_id in users_db[user_id]:
        users_db[user_id].remove(book_id)


def log_transaction(user_id, book_id, action, timestamp):
    """
    Records a transaction in the transaction log.
    """
    transaction = {
        "user_id": user_id,
        "book_id": book_id,
        "action": action,
        "timestamp": timestamp
    }
    transactions_db.append(transaction)


def clear_all_data():
    """
    Clears all data from all databases.
    Used for testing and system reset.
    """
    global books_db, users_db, transactions_db
    books_db.clear()
    users_db.clear()
    transactions_db.clear()


# --- BUSINESS LOGIC LAYER ---
# This layer contains all business rules and workflows
# It ONLY calls data access layer functions (never accesses global data directly)
# It does NOT handle user input/output (that's presentation layer responsibility)

def add_book_to_library(title, author, isbn, copies=1):
    """
    Adds a new book to the library with business rule validation.

    Business rules:
    - Title and author cannot be empty
    - Copies must be positive
    - ISBN should be unique (simplified validation)
    - Auto-generates book ID
    """
    # Validate input according to business rules
    if not title or not title.strip():
        return "Error: Book title cannot be empty"

    if not author or not author.strip():
        return "Error: Book author cannot be empty"

    if copies <= 0:
        return "Error: Number of copies must be positive"

    # Generate new book ID (simple sequential ID)
    all_books = get_all_books()
    book_id = max(all_books.keys()) + 1 if all_books else 1

    # Create book data structure
    book_data = {
        "title": title.strip(),
        "author": author.strip(),
        "isbn": isbn,
        "total_copies": copies,
        "available_copies": copies
    }

    # Save using data access layer
    save_book(book_id, book_data)

    return f"Book '{title}' added successfully with ID {book_id}"


def is_book_available_for_borrowing(book_id):
    """
    Checks if a book is available for borrowing.

    Business rules:
    - Book must exist
    - Book must have available copies > 0
    """
    book = get_book_by_id(book_id)  # Use data access layer
    return book is not None and book.get("available_copies", 0) > 0


def borrow_book_workflow(user_id, book_id):
    """
    Handles the complete borrowing workflow.

    Business rules:
    - Book must be available
    - User cannot borrow the same book twice
    - Update available copies
    - Log the transaction
    """
    # Check if book is available
    if not is_book_available_for_borrowing(book_id):
        return "Error: Book is not available for borrowing"

    # Check if user already has this book
    user_books = get_user_borrowed_books(user_id)
    if book_id in user_books:
        return "Error: You have already borrowed this book"

    # Get book details for transaction
    book = get_book_by_id(book_id)

    # Update available copies
    book["available_copies"] -= 1
    save_book(book_id, book)

    # Record user borrowed the book
    save_user_borrowed_book(user_id, book_id)

    # Log transaction
    timestamp = datetime.now().isoformat()
    log_transaction(user_id, book_id, "borrow", timestamp)

    return f"Book '{book['title']}' borrowed successfully!"


def return_book_workflow(user_id, book_id):
    """
    Handles the complete return workflow.

    Business rules:
    - User must have borrowed the book
    - Update available copies
    - Log the transaction
    """
    # Check if user has borrowed this book
    user_books = get_user_borrowed_books(user_id)
    if book_id not in user_books:
        return "Error: You have not borrowed this book"

    # Get book details
    book = get_book_by_id(book_id)
    if book is None:
        return "Error: Book not found in system"

    # Update available copies
    book["available_copies"] += 1
    save_book(book_id, book)

    # Remove from user's borrowed list
    remove_user_borrowed_book(user_id, book_id)

    # Log transaction
    timestamp = datetime.now().isoformat()
    log_transaction(user_id, book_id, "return", timestamp)

    return f"Book '{book['title']}' returned successfully!"


def get_user_borrowed_books_with_details(user_id):
    """
    Returns detailed information about books borrowed by a user.
    Enriches book IDs with full book details.
    """
    user_book_ids = get_user_borrowed_books(user_id)
    detailed_books = []

    for book_id in user_book_ids:
        book = get_book_by_id(book_id)
        if book:
            detailed_book = book.copy()
            detailed_book["book_id"] = book_id
            detailed_books.append(detailed_book)

    return detailed_books


def get_available_books_list():
    """
    Returns list of all books that are available for borrowing.
    Applies business rule of available_copies > 0.
    """
    all_books = get_all_books()
    available_books = []

    for book_id, book in all_books.items():
        if book.get("available_copies", 0) > 0:
            book_copy = book.copy()
            book_copy["book_id"] = book_id
            available_books.append(book_copy)

    return available_books


# --- PRESENTATION LAYER ---
# This layer handles user interface, input validation, and output formatting
# It ONLY calls business logic layer functions (never data access directly)

def format_book_display(books_list):
    """
    Formats a list of books for display to users.
    Creates user-friendly output with proper formatting.
    """
    if not books_list:
        return "No books available."

    output = "📚 Library Books:\n"
    output += "=" * 60 + "\n"

    for book in books_list:
        book_id = book.get("book_id", "N/A")
        title = book.get("title", "Unknown Title")
        author = book.get("author", "Unknown Author")
        available = book.get("available_copies", 0)

        availability_status = f"✅ {available} available" if available > 0 else "❌ Not available"

        output += f"[{book_id}] {title}\n"
        output += f"     by {author}\n"
        output += f"     {availability_status}\n"
        output += "-" * 40 + "\n"

    return output


def parse_user_input(input_string, expected_type):
    """
    Parses and validates user input according to expected type.
    Returns None for invalid input.
    """
    if input_string is None:
        return None

    # Strip whitespace
    cleaned_input = input_string.strip()

    if expected_type == str:
        return cleaned_input if cleaned_input else None

    elif expected_type == int:
        try:
            return int(cleaned_input)
        except ValueError:
            return None

    return None


def display_user_borrowed_books(user_id):
    """
    Displays a user's borrowed books in a formatted way.
    Uses business logic layer to get data.
    """
    # Get detailed book information from business layer
    user_books = get_user_borrowed_books_with_details(user_id)

    if not user_books:
        return f"📚 User '{user_id}' has no books currently borrowed."

    output = f"📚 Books borrowed by '{user_id}':\n"
    output += "=" * 50 + "\n"

    for book in user_books:
        title = book.get("title", "Unknown Title")
        author = book.get("author", "Unknown Author")
        book_id = book.get("book_id", "N/A")

        output += f"[{book_id}] {title}\n"
        output += f"     by {author}\n"
        output += "-" * 30 + "\n"

    return output


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
        print("✅ Changes in one layer don't affect others")
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


def interactive_demo():
    """
    Interactive demo showing the layered architecture in action.
    """
    print("🚀 Interactive Demo - Layered Architecture Library System")
    print("=" * 60)

    clear_all_data()

    print("\n1. DATA ACCESS LAYER - Adding books directly to database:")
    save_book(1, {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "isbn": "978-0-7432-7356-5",
        "total_copies": 2,
        "available_copies": 2
    })
    print("✅ Book saved directly to database")

    print("\n2. BUSINESS LOGIC LAYER - Adding book with validation:")
    result = add_book_to_library("1984", "George Orwell", "978-0-452-28423-4", 1)
    print(f"✅ {result}")

    print("\n3. PRESENTATION LAYER - Formatting available books:")
    available_books = get_available_books_list()
    formatted_display = format_book_display(available_books)
    print(formatted_display)

    print("\n4. COMPLETE WORKFLOW - Borrowing through all layers:")
    print("   📊 Data Layer: Checking book availability...")
    book_exists = get_book_by_id(1) is not None
    print(f"   Book exists in database: {book_exists}")

    print("   🧠 Business Layer: Processing borrow request...")
    borrow_result = borrow_book_workflow("demo_user", 1)
    print(f"   {borrow_result}")

    print("   🖥️  Presentation Layer: Displaying user's books...")
    user_display = display_user_borrowed_books("demo_user")
    print(user_display)

    print("\n5. LAYER SEPARATION DEMONSTRATED:")
    print("   ✅ Data layer: Direct database operations")
    print("   ✅ Business layer: Called data layer functions only")
    print("   ✅ Presentation layer: Called business layer functions only")
    print("   ✅ Clean separation of concerns maintained")

    print("\n🎉 Demo completed!")


if __name__ == "__main__":
    print("🎯 Layered Architecture - Complete Solution")
    print()

    # Run the tests to prove everything works
    success = run_tests()

    if success:
        print("\n" + "=" * 70)
        print("Would you like to see an interactive demo? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response in ['y', 'yes']:
                print()
                interactive_demo()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")

    print("\n📚 Layered Architecture Learning Summary:")
    print("✅ Separation of concerns across layers")
    print("✅ Each layer has single responsibility")
    print("✅ Controlled communication between adjacent layers")
    print("✅ Business logic isolated from data access and UI")
    print("✅ Easier to test, maintain, and modify")
    print("✅ Changes in one layer don't ripple through others")