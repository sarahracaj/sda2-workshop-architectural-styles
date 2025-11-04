"""
Event-Driven Architecture Example: Multi-Service Library System (Test-Driven Development)
========================================================================================

This is the most advanced TDD exercise demonstrating event-driven architecture.
Your task is to implement a sophisticated distributed system with multiple services
communicating through events, following event-driven architecture principles.

ARCHITECTURAL CHARACTERISTICS:
- Loose coupling between services through events
- Asynchronous communication via message broker
- Event sourcing for audit trails and state reconstruction
- Multiple independent services with specific responsibilities
- Scalable and fault-tolerant design
- Eventually consistent state across services

SERVICES IN THIS SYSTEM:
1. LIBRARY SERVICE: Core book and user management
2. NOTIFICATION SERVICE: User communications and alerts
3. ANALYTICS SERVICE: Usage tracking and reporting
4. AUDIT SERVICE: Event logging and compliance
5. MESSAGE BROKER: Event routing and delivery

EVENT TYPES:
- BookAdded, BookRemoved, BookBorrowed, BookReturned
- UserRegistered, UserSuspended, UserReactivated
- NotificationSent, AnalyticsUpdated, AuditLogged
- SystemAlert, MaintenanceScheduled

TDD APPROACH:
1. Read and understand the tests (they define the requirements)
2. Run the tests (they will fail initially)
3. Implement services and event handling step by step
4. Follow event-driven principles: loose coupling, async processing
5. Ensure eventual consistency across services

LEARNING OBJECTIVES:
- Understand event-driven architecture benefits and challenges
- Practice designing loosely coupled systems
- Learn event sourcing and CQRS concepts
- Experience asynchronous communication patterns
- See how distributed systems achieve consistency
- Handle complex inter-service dependencies
"""

import unittest
from typing import List, Dict, Any, Optional
import sys

# --- GLOBAL STATE ---
# Each service maintains its own state (simulating separate databases)
library_db = {
    "books": {},
    "users": {},
    "borrowings": {}
}

notification_db = {
    "users": {},
    "notifications": [],
    "preferences": {}
}

analytics_db = {
    "events": [],
    "metrics": {},
    "reports": {}
}

audit_db = {
    "events": [],
    "snapshots": {}
}

# Message broker state
event_queue = []
event_handlers = {}
failed_events = []


# --- MESSAGE BROKER ---
# Central event routing and delivery system

def register_event_handler(event_type: str, handler_func, service_name: str):
    """
    TODO: Implement event handler registration.

    Should register a handler function for a specific event type.
    Multiple handlers can be registered for the same event type.
    Look at test_message_broker_registration() for requirements.
    """
    pass


def emit_event(event_type: str, payload: Dict[Any, Any], correlation_id: str = None):
    """
    TODO: Implement event emission.

    Should add event to queue with metadata (timestamp, ID, etc.).
    Should generate correlation_id if not provided.
    Look at test_message_broker_emission() for requirements.
    """
    pass


def process_events(max_events: int = None):
    """
    TODO: Implement event processing.

    Should process events from queue and call registered handlers.
    Should handle failures gracefully and support retry logic.
    Look at test_message_broker_processing() for requirements.
    """
    pass


def get_failed_events():
    """
    TODO: Implement failed event retrieval.

    Should return events that failed processing.
    Look at test_message_broker_failure_handling() for requirements.
    """
    pass


def clear_event_queue():
    """
    TODO: Implement queue clearing.

    Should clear all events and reset broker state.
    """
    pass


# --- LIBRARY SERVICE ---
# Core domain service for books and users

def add_book_to_library(isbn: str, title: str, author: str, copies: int = 1):
    """
    TODO: Implement book addition with event emission.

    Should validate input, store book, and emit BookAdded event.
    Should generate unique book ID and handle duplicate ISBNs.
    Look at test_library_service_add_book() for requirements.
    """
    pass


def register_user(email: str, name: str, user_type: str = "standard"):
    """
    TODO: Implement user registration with event emission.

    Should validate input, store user, and emit UserRegistered event.
    Should handle duplicate emails and validate email format.
    Look at test_library_service_register_user() for requirements.
    """
    pass


def borrow_book(user_id: str, book_id: str):
    """
    TODO: Implement book borrowing with complex event emission.

    Should validate availability, update state, emit BookBorrowed event.
    Should handle business rules: user limits, book availability, etc.
    Look at test_library_service_borrow_book() for requirements.
    """
    pass


def return_book(user_id: str, book_id: str):
    """
    TODO: Implement book return with event emission.

    Should validate borrowing exists, update state, emit BookReturned event.
    Should calculate late fees if applicable.
    Look at test_library_service_return_book() for requirements.
    """
    pass


def get_user_borrowings(user_id: str):
    """
    TODO: Implement user borrowing retrieval.

    Should return current borrowings for a user.
    Look at test_library_service_user_borrowings() for requirements.
    """
    pass


def suspend_user(user_id: str, reason: str):
    """
    TODO: Implement user suspension with event emission.

    Should suspend user and emit UserSuspended event.
    Look at test_library_service_suspend_user() for requirements.
    """
    pass


# --- NOTIFICATION SERVICE ---
# Handles all user communications and alerts

def handle_user_registered(payload: Dict[Any, Any]):
    """
    TODO: Implement welcome notification handler.

    Should create user in notification system and send welcome message.
    Look at test_notification_service_user_registered() for requirements.
    """
    pass


def handle_book_borrowed(payload: Dict[Any, Any]):
    """
    TODO: Implement borrow notification handler.

    Should send confirmation and due date reminder notifications.
    Look at test_notification_service_book_borrowed() for requirements.
    """
    pass


def handle_book_returned(payload: Dict[Any, Any]):
    """
    TODO: Implement return notification handler.

    Should send return confirmation and late fee notifications if applicable.
    Look at test_notification_service_book_returned() for requirements.
    """
    pass


def send_notification(user_id: str, message: str, notification_type: str):
    """
    TODO: Implement notification sending.

    Should store notification and emit NotificationSent event.
    Look at test_notification_service_send() for requirements.
    """
    pass


def get_user_notifications(user_id: str):
    """
    TODO: Implement user notification retrieval.

    Should return all notifications for a user.
    Look at test_notification_service_get_notifications() for requirements.
    """
    pass


def set_notification_preferences(user_id: str, preferences: Dict[str, bool]):
    """
    TODO: Implement notification preferences.

    Should store user notification preferences.
    Look at test_notification_service_preferences() for requirements.
    """
    pass


# --- ANALYTICS SERVICE ---
# Tracks usage patterns and generates insights

def handle_book_borrowed_analytics(payload: Dict[Any, Any]):
    """
    TODO: Implement borrowing analytics handler.

    Should track borrowing patterns and update metrics.
    Look at test_analytics_service_book_borrowed() for requirements.
    """
    pass


def handle_book_returned_analytics(payload: Dict[Any, Any]):
    """
    TODO: Implement return analytics handler.

    Should track return patterns and calculate duration metrics.
    Look at test_analytics_service_book_returned() for requirements.
    """
    pass


def handle_user_registered_analytics(payload: Dict[Any, Any]):
    """
    TODO: Implement user registration analytics handler.

    Should track user growth and demographics.
    Look at test_analytics_service_user_registered() for requirements.
    """
    pass


def generate_usage_report(start_date: str, end_date: str):
    """
    TODO: Implement usage report generation.

    Should create comprehensive usage analytics report.
    Look at test_analytics_service_report_generation() for requirements.
    """
    pass


def get_book_popularity_metrics():
    """
    TODO: Implement book popularity metrics.

    Should return book borrowing frequency and trends.
    Look at test_analytics_service_popularity_metrics() for requirements.
    """
    pass


def track_system_performance(event_type: str, processing_time: float):
    """
    TODO: Implement system performance tracking.

    Should track event processing performance metrics.
    Look at test_analytics_service_performance_tracking() for requirements.
    """
    pass


# --- AUDIT SERVICE ---
# Event sourcing and compliance logging

def handle_any_event_for_audit(event_type: str, payload: Dict[Any, Any], metadata: Dict[Any, Any]):
    """
    TODO: Implement universal audit event handler.

    Should log all events for compliance and audit purposes.
    Look at test_audit_service_event_logging() for requirements.
    """
    pass


def create_system_snapshot():
    """
    TODO: Implement system state snapshot creation.

    Should capture current state of all services for backup/recovery.
    Look at test_audit_service_snapshot_creation() for requirements.
    """
    pass


def reconstruct_state_from_events(target_date: str):
    """
    TODO: Implement state reconstruction from events.

    Should rebuild system state by replaying events up to target date.
    Look at test_audit_service_state_reconstruction() for requirements.
    """
    pass


def get_audit_trail(entity_type: str, entity_id: str):
    """
    TODO: Implement audit trail retrieval.

    Should return chronological history of events for an entity.
    Look at test_audit_service_audit_trail() for requirements.
    """
    pass


def detect_anomalies():
    """
    TODO: Implement anomaly detection.

    Should analyze event patterns and detect suspicious activities.
    Look at test_audit_service_anomaly_detection() for requirements.
    """
    pass


# --- SYSTEM INITIALIZATION ---
def initialize_event_driven_system():
    """
    TODO: Implement system initialization.

    Should register all event handlers for all services.
    Look at test_system_initialization() for requirements.
    """
    pass


def clear_all_system_state():
    """
    TODO: Implement complete system reset.

    Should clear all service databases and event broker state.
    """
    pass


# --- TEST SUITE ---

class TestMessageBroker(unittest.TestCase):
    """
    Tests for the Message Broker - event routing and delivery.
    These tests verify the core event-driven infrastructure.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_system_state()

    def test_message_broker_registration(self):
        """Test event handler registration."""

        def test_handler(payload):
            pass

        register_event_handler("TestEvent", test_handler, "TestService")

        # Handler should be registered
        self.assertIn("TestEvent", event_handlers)
        self.assertEqual(len(event_handlers["TestEvent"]), 1)

        # Multiple handlers for same event
        register_event_handler("TestEvent", test_handler, "TestService2")
        self.assertEqual(len(event_handlers["TestEvent"]), 2)

    def test_message_broker_emission(self):
        """Test event emission with proper metadata."""
        emit_event("TestEvent", {"data": "test"}, "correlation-123")

        # Event should be in queue
        self.assertEqual(len(event_queue), 1)

        event = event_queue[0]
        self.assertEqual(event["type"], "TestEvent")
        self.assertEqual(event["payload"]["data"], "test")
        self.assertEqual(event["correlation_id"], "correlation-123")
        self.assertIn("event_id", event)
        self.assertIn("timestamp", event)

        # Auto-generate correlation ID
        emit_event("TestEvent2", {"data": "test2"})
        self.assertIsNotNone(event_queue[1]["correlation_id"])

    def test_message_broker_processing(self):
        """Test event processing and handler invocation."""
        processed_events = []

        def test_handler(payload):
            processed_events.append(payload)

        register_event_handler("ProcessTest", test_handler, "TestService")
        emit_event("ProcessTest", {"data": "process_me"})

        # Process events
        process_events()

        # Event should be processed
        self.assertEqual(len(event_queue), 0)
        self.assertEqual(len(processed_events), 1)
        self.assertEqual(processed_events[0]["data"], "process_me")

    def test_message_broker_failure_handling(self):
        """Test handling of failed event processing."""

        def failing_handler(payload):
            raise Exception("Handler failed")

        register_event_handler("FailTest", failing_handler, "TestService")
        emit_event("FailTest", {"data": "will_fail"})

        # Process events (should handle failure gracefully)
        process_events()

        # Failed event should be logged
        failed = get_failed_events()
        self.assertEqual(len(failed), 1)
        self.assertEqual(failed[0]["original_event"]["type"], "FailTest")


class TestLibraryService(unittest.TestCase):
    """
    Tests for the Library Service - core domain operations.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_system_state()
        initialize_event_driven_system()

    def test_library_service_add_book(self):
        """Test book addition with event emission."""
        result = add_book_to_library("978-0-123456-78-9", "Test Book", "Test Author", 2)

        # Should return success message with book ID
        self.assertIn("added", result.lower())
        self.assertIn("book", result.lower())

        # Book should be stored
        self.assertEqual(len(library_db["books"]), 1)
        book_id = list(library_db["books"].keys())[0]
        book = library_db["books"][book_id]

        self.assertEqual(book["isbn"], "978-0-123456-78-9")
        self.assertEqual(book["title"], "Test Book")
        self.assertEqual(book["author"], "Test Author")
        self.assertEqual(book["total_copies"], 2)
        self.assertEqual(book["available_copies"], 2)

        # BookAdded event should be emitted
        process_events()
        # Verify through audit trail that event was processed

    def test_library_service_register_user(self):
        """Test user registration with validation and event emission."""
        result = register_user("test@example.com", "Test User", "premium")

        # Should return success message with user ID
        self.assertIn("registered", result.lower())
        self.assertIn("user", result.lower())

        # User should be stored
        self.assertEqual(len(library_db["users"]), 1)
        user_id = list(library_db["users"].keys())[0]
        user = library_db["users"][user_id]

        self.assertEqual(user["email"], "test@example.com")
        self.assertEqual(user["name"], "Test User")
        self.assertEqual(user["user_type"], "premium")
        self.assertEqual(user["status"], "active")

        # Should reject duplicate email
        result2 = register_user("test@example.com", "Another User")
        self.assertIn("error", result2.lower())
        self.assertIn("email", result2.lower())

    def test_library_service_borrow_book(self):
        """Test book borrowing with business rules and events."""
        # Setup: Add book and user
        add_book_to_library("978-0-123456-78-9", "Borrowable Book", "Author", 1)
        register_user("borrower@example.com", "Borrower User")

        book_id = list(library_db["books"].keys())[0]
        user_id = list(library_db["users"].keys())[0]

        # Should successfully borrow
        result = borrow_book(user_id, book_id)
        self.assertIn("borrowed", result.lower())
        self.assertIn("successfully", result.lower())

        # Book availability should be updated
        book = library_db["books"][book_id]
        self.assertEqual(book["available_copies"], 0)

        # Borrowing should be recorded
        self.assertEqual(len(library_db["borrowings"]), 1)
        borrowing = list(library_db["borrowings"].values())[0]
        self.assertEqual(borrowing["user_id"], user_id)
        self.assertEqual(borrowing["book_id"], book_id)
        self.assertIsNotNone(borrowing["borrowed_date"])
        self.assertIsNone(borrowing["returned_date"])

        # Should not be able to borrow unavailable book
        result2 = borrow_book(user_id, book_id)
        self.assertIn("not available", result2.lower())

    def test_library_service_return_book(self):
        """Test book return with late fee calculation and events."""
        # Setup: Add book, user, and borrow
        add_book_to_library("978-0-123456-78-9", "Returnable Book", "Author", 1)
        register_user("returner@example.com", "Returner User")

        book_id = list(library_db["books"].keys())[0]
        user_id = list(library_db["users"].keys())[0]

        borrow_book(user_id, book_id)

        # Should successfully return
        result = return_book(user_id, book_id)
        self.assertIn("returned", result.lower())
        self.assertIn("successfully", result.lower())

        # Book availability should be updated
        book = library_db["books"][book_id]
        self.assertEqual(book["available_copies"], 1)

        # Borrowing should be marked as returned
        borrowing = list(library_db["borrowings"].values())[0]
        self.assertIsNotNone(borrowing["returned_date"])

        # Should not be able to return non-borrowed book
        result2 = return_book(user_id, book_id)
        self.assertIn("not borrowed", result2.lower())


class TestNotificationService(unittest.TestCase):
    """
    Tests for the Notification Service - user communications.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_system_state()
        initialize_event_driven_system()

    def test_notification_service_user_registered(self):
        """Test welcome notification on user registration."""
        payload = {
            "user_id": "user-123",
            "email": "new@example.com",
            "name": "New User"
        }

        handle_user_registered(payload)

        # User should be added to notification system
        self.assertIn("user-123", notification_db["users"])

        # Welcome notification should be sent
        notifications = get_user_notifications("user-123")
        self.assertEqual(len(notifications), 1)
        self.assertIn("welcome", notifications[0]["message"].lower())
        self.assertEqual(notifications[0]["type"], "welcome")

    def test_notification_service_book_borrowed(self):
        """Test borrow confirmation notification."""
        payload = {
            "user_id": "user-123",
            "book_id": "book-456",
            "book_title": "Borrowed Book",
            "due_date": "2024-02-01T00:00:00"
        }

        handle_book_borrowed(payload)

        # Borrow confirmation should be sent
        notifications = get_user_notifications("user-123")
        self.assertEqual(len(notifications), 1)
        self.assertIn("borrowed", notifications[0]["message"].lower())
        self.assertIn("Borrowed Book", notifications[0]["message"])
        self.assertEqual(notifications[0]["type"], "borrow_confirmation")


class TestAnalyticsService(unittest.TestCase):
    """
    Tests for the Analytics Service - usage tracking and insights.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_system_state()
        initialize_event_driven_system()

    def test_analytics_service_book_borrowed(self):
        """Test borrowing analytics tracking."""
        payload = {
            "user_id": "user-123",
            "book_id": "book-456",
            "borrowed_date": "2024-01-15T10:00:00"
        }

        handle_book_borrowed_analytics(payload)

        # Event should be tracked
        self.assertEqual(len(analytics_db["events"]), 1)

        # Metrics should be updated
        metrics = analytics_db["metrics"]
        self.assertIn("total_borrows", metrics)
        self.assertEqual(metrics["total_borrows"], 1)

    def test_analytics_service_report_generation(self):
        """Test usage report generation."""
        # Add some test events
        analytics_db["events"].append({
            "type": "book_borrowed",
            "timestamp": "2024-01-15T10:00:00",
            "data": {"user_id": "user-123", "book_id": "book-456"}
        })

        report = generate_usage_report("2024-01-01", "2024-01-31")

        # Report should contain key metrics
        self.assertIn("total_borrows", report)
        self.assertIn("active_users", report)
        self.assertIn("popular_books", report)
        self.assertEqual(report["total_borrows"], 1)


class TestAuditService(unittest.TestCase):
    """
    Tests for the Audit Service - event sourcing and compliance.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_system_state()
        initialize_event_driven_system()

    def test_audit_service_event_logging(self):
        """Test universal event logging for audit purposes."""
        handle_any_event_for_audit("BookBorrowed",
                                   {"user_id": "user-123", "book_id": "book-456"},
                                   {"timestamp": "2024-01-15T10:00:00", "correlation_id": "corr-123"})

        # Event should be logged
        self.assertEqual(len(audit_db["events"]), 1)

        audit_event = audit_db["events"][0]
        self.assertEqual(audit_event["event_type"], "BookBorrowed")
        self.assertEqual(audit_event["payload"]["user_id"], "user-123")
        self.assertIn("timestamp", audit_event)

    def test_audit_service_audit_trail(self):
        """Test audit trail retrieval for specific entities."""
        # Add multiple events for a user
        handle_any_event_for_audit("UserRegistered", {"user_id": "user-123"}, {})
        handle_any_event_for_audit("BookBorrowed", {"user_id": "user-123", "book_id": "book-456"}, {})
        handle_any_event_for_audit("BookReturned", {"user_id": "user-123", "book_id": "book-456"}, {})

        # Get audit trail for user
        trail = get_audit_trail("user", "user-123")

        # Should return chronological events for the user
        self.assertEqual(len(trail), 3)
        self.assertEqual(trail[0]["event_type"], "UserRegistered")
        self.assertEqual(trail[1]["event_type"], "BookBorrowed")
        self.assertEqual(trail[2]["event_type"], "BookReturned")


class TestEventDrivenArchitecture(unittest.TestCase):
    """
    Tests that verify proper event-driven architecture implementation.
    These tests ensure loose coupling and proper event flow.
    """

    def setUp(self):
        """Set up clean state before each test."""
        clear_all_system_state()
        initialize_event_driven_system()

    def test_system_initialization(self):
        """Test that all event handlers are properly registered."""
        # System should have handlers for all event types
        expected_events = [
            "BookAdded", "BookBorrowed", "BookReturned",
            "UserRegistered", "UserSuspended",
            "NotificationSent"
        ]

        for event_type in expected_events:
            self.assertIn(event_type, event_handlers)
            self.assertGreater(len(event_handlers[event_type]), 0)

    def test_end_to_end_workflow(self):
        """Test complete workflow across all services."""
        # 1. Register user (should trigger notifications and analytics)
        result = register_user("endtoend@example.com", "End To End User")
        self.assertIn("registered", result.lower())

        # 2. Add book
        add_book_to_library("978-0-123456-78-9", "E2E Book", "E2E Author", 1)

        # 3. Process all events
        process_events()

        # 4. Verify notifications were sent
        user_id = list(library_db["users"].keys())[0]
        notifications = get_user_notifications(user_id)
        self.assertGreater(len(notifications), 0)

        # 5. Verify analytics were updated
        self.assertGreater(len(analytics_db["events"]), 0)

        # 6. Verify audit logs were created
        self.assertGreater(len(audit_db["events"]), 0)

    def test_service_isolation(self):
        """Test that services are loosely coupled through events."""
        # Services should not directly call each other
        # They should only communicate through events

        # This is verified by the fact that each service handles
        # events independently and the system works through
        # the message broker only


def run_tests():
    """
    Run all tests and provide detailed feedback for event-driven architecture.
    """
    print("🧪 Running Test Suite for Event-Driven Architecture Library System")
    print("=" * 75)
    print()
    print("This tests verify proper event-driven architecture implementation:")
    print("📡 MESSAGE BROKER: Event routing and delivery infrastructure")
    print("📚 LIBRARY SERVICE: Core domain operations with event emission")
    print("🔔 NOTIFICATION SERVICE: User communications through event handling")
    print("📊 ANALYTICS SERVICE: Usage tracking through event processing")
    print("📋 AUDIT SERVICE: Event sourcing and compliance logging")
    print("🏗️  ARCHITECTURE TESTS: Service isolation and event flow")
    print()

    # Run tests with detailed output
    test_loader = unittest.TestLoader()
    test_suite = test_loader.loadTestsFromModule(sys.modules[__name__])

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(test_suite)

    print("\n" + "=" * 75)
    if result.wasSuccessful():
        print("🎉 Congratulations! All tests pass!")
        print("Your event-driven architecture implementation is complete!")
        print()
        print("🏗️  Event-Driven Architecture Characteristics Demonstrated:")
        print("✅ Loose coupling between services")
        print("✅ Asynchronous communication via events")
        print("✅ Event sourcing for audit and reconstruction")
        print("✅ Scalable and fault-tolerant design")
        print("✅ Eventually consistent distributed state")
        print("✅ Service isolation and independence")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        print()
        print("💡 Tips for event-driven architecture success:")
        print("1. Start with message broker infrastructure")
        print("2. Implement event emission in library service")
        print("3. Create event handlers in other services")
        print("4. Ensure services only communicate through events")
        print("5. Test event flow end-to-end")
        print()
        print("Remember: Services should be loosely coupled through events only!")

    return result.wasSuccessful()


if __name__ == "__main__":
    print("🎯 Event-Driven Architecture - Advanced Test-Driven Development Exercise")
    print()
    print("🏗️  System Architecture:")
    print("📡 Message Broker: Event routing and delivery")
    print("📚 Library Service: Books, users, borrowings")
    print("🔔 Notification Service: User communications")
    print("📊 Analytics Service: Usage tracking and insights")
    print("📋 Audit Service: Event sourcing and compliance")
    print()
    print("🎓 Advanced Concepts:")
    print("• Event sourcing and state reconstruction")
    print("• Eventually consistent distributed systems")
    print("• Fault-tolerant event processing")
    print("• Service isolation and loose coupling")
    print("• Correlation IDs and event tracing")
    print()

    # Run the tests
    success = run_tests()

    if not success:
        print("\n🚀 Implementation Strategy:")
        print("1. MESSAGE BROKER: Event registration, emission, processing")
        print("2. LIBRARY SERVICE: Core operations with event emission")
        print("3. EVENT HANDLERS: Notification, analytics, audit services")
        print("4. INTEGRATION: End-to-end workflows and event flow")
        print("5. TESTING: Verify loose coupling and event-driven patterns")
        print()
        print("Focus on loose coupling - services should only communicate through events!")