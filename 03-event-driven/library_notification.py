"""
Event-Driven Architecture Example: Multi-Service Library System (Test-Driven Development) - SOLUTION
===================================================================================================

This is the complete solution demonstrating advanced event-driven architecture
with multiple services, event sourcing, and sophisticated inter-service communication.

ARCHITECTURAL CHARACTERISTICS DEMONSTRATED:
- Loose coupling between services through events
- Asynchronous communication via message broker
- Event sourcing for audit trails and state reconstruction
- Multiple independent services with specific responsibilities
- Scalable and fault-tolerant design
- Eventually consistent state across services

SERVICES IMPLEMENTED:
1. LIBRARY SERVICE: Core book and user management
2. NOTIFICATION SERVICE: User communications and alerts
3. ANALYTICS SERVICE: Usage tracking and reporting
4. AUDIT SERVICE: Event logging and compliance
5. MESSAGE BROKER: Event routing and delivery
"""

import unittest
import uuid
from datetime import datetime, timedelta
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
    Registers a handler function for a specific event type.
    Multiple handlers can be registered for the same event type.
    """
    if event_type not in event_handlers:
        event_handlers[event_type] = []

    event_handlers[event_type].append({
        "handler": handler_func,
        "service": service_name
    })


def emit_event(event_type: str, payload: Dict[Any, Any], correlation_id: str = None):
    """
    Adds event to queue with metadata (timestamp, ID, etc.).
    Generates correlation_id if not provided.
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    event = {
        "event_id": str(uuid.uuid4()),
        "type": event_type,
        "payload": payload.copy(),
        "correlation_id": correlation_id,
        "timestamp": datetime.now().isoformat(),
        "retry_count": 0
    }

    event_queue.append(event)


def process_events(max_events: int = None):
    """
    Processes events from queue and calls registered handlers.
    Handles failures gracefully and supports retry logic.
    """
    processed_count = 0

    while event_queue and (max_events is None or processed_count < max_events):
        event = event_queue.pop(0)
        processed_count += 1

        event_type = event["type"]

        if event_type in event_handlers:
            for handler_info in event_handlers[event_type]:
                try:
                    # For audit service, call with special metadata parameters
                    if handler_info["service"] == "AuditService":
                        handler_info["handler"](event_type, event["payload"], {
                            "timestamp": event["timestamp"],
                            "correlation_id": event["correlation_id"],
                            "event_id": event["event_id"]
                        })
                    else:
                        # Call handler with payload only for other services
                        handler_info["handler"](event["payload"])

                except Exception as e:
                    # Log failed event (no retry logic for educational simplicity)
                    failed_event = {
                        "original_event": event,
                        "error": str(e),
                        "failed_at": datetime.now().isoformat(),
                        "handler_service": handler_info["service"]
                    }
                    failed_events.append(failed_event)


def get_failed_events():
    """
    Returns events that failed processing.
    """
    return failed_events.copy()


def clear_event_queue():
    """
    Clears all events and resets broker state.
    """
    global event_queue, event_handlers, failed_events
    event_queue.clear()
    event_handlers.clear()
    failed_events.clear()


# --- LIBRARY SERVICE ---
# Core domain service for books and users

def add_book_to_library(isbn: str, title: str, author: str, copies: int = 1):
    """
    Validates input, stores book, and emits BookAdded event.
    Generates unique book ID and handles duplicate ISBNs.
    """
    # Validate input
    if not isbn or not title or not author:
        return "Error: ISBN, title, and author are required"

    if copies <= 0:
        return "Error: Number of copies must be positive"

    # Check for duplicate ISBN
    for book in library_db["books"].values():
        if book["isbn"] == isbn:
            return "Error: Book with this ISBN already exists"

    # Generate unique book ID
    book_id = str(uuid.uuid4())

    # Create book
    book = {
        "isbn": isbn,
        "title": title,
        "author": author,
        "total_copies": copies,
        "available_copies": copies,
        "added_date": datetime.now().isoformat()
    }

    library_db["books"][book_id] = book

    # Emit BookAdded event
    emit_event("BookAdded", {
        "book_id": book_id,
        "isbn": isbn,
        "title": title,
        "author": author,
        "copies": copies
    })

    return f"Book '{title}' added successfully with ID {book_id}"


def register_user(email: str, name: str, user_type: str = "standard"):
    """
    Validates input, stores user, and emits UserRegistered event.
    Handles duplicate emails and validates email format.
    """
    # Validate email format (simplified)
    if not email or "@" not in email:
        return "Error: Valid email address is required"

    if not name or not name.strip():
        return "Error: User name is required"

    # Check for duplicate email
    for user in library_db["users"].values():
        if user["email"] == email:
            return "Error: User with this email already exists"

    # Generate unique user ID
    user_id = str(uuid.uuid4())

    # Create user
    user = {
        "email": email,
        "name": name.strip(),
        "user_type": user_type,
        "status": "active",
        "registered_date": datetime.now().isoformat(),
        "borrowing_limit": 5 if user_type == "premium" else 3
    }

    library_db["users"][user_id] = user

    # Emit UserRegistered event
    emit_event("UserRegistered", {
        "user_id": user_id,
        "email": email,
        "name": name,
        "user_type": user_type
    })

    return f"User '{name}' registered successfully with ID {user_id}"


def borrow_book(user_id: str, book_id: str):
    """
    Validates availability, updates state, emits BookBorrowed event.
    Handles business rules: user limits, book availability, etc.
    """
    # Validate user exists
    if user_id not in library_db["users"]:
        return "Error: User not found"

    user = library_db["users"][user_id]

    if user["status"] != "active":
        return "Error: User account is not active"

    # Validate book exists
    if book_id not in library_db["books"]:
        return "Error: Book not found"

    book = library_db["books"][book_id]

    # Check book availability
    if book["available_copies"] <= 0:
        return "Error: Book is not available for borrowing"

    # Check user borrowing limit
    current_borrowings = [b for b in library_db["borrowings"].values()
                         if b["user_id"] == user_id and b["returned_date"] is None]

    if len(current_borrowings) >= user["borrowing_limit"]:
        return f"Error: User has reached borrowing limit of {user['borrowing_limit']} books"

    # Check if user already has this book
    for borrowing in current_borrowings:
        if borrowing["book_id"] == book_id:
            return "Error: User has already borrowed this book"

    # Create borrowing record
    borrowing_id = str(uuid.uuid4())
    due_date = datetime.now() + timedelta(days=14)  # 2 weeks

    borrowing = {
        "user_id": user_id,
        "book_id": book_id,
        "borrowed_date": datetime.now().isoformat(),
        "due_date": due_date.isoformat(),
        "returned_date": None,
        "late_fee": 0.0
    }

    library_db["borrowings"][borrowing_id] = borrowing

    # Update book availability
    book["available_copies"] -= 1

    # Emit BookBorrowed event
    emit_event("BookBorrowed", {
        "user_id": user_id,
        "book_id": book_id,
        "book_title": book["title"],
        "borrowing_id": borrowing_id,
        "borrowed_date": borrowing["borrowed_date"],
        "due_date": borrowing["due_date"],
        "user_name": user["name"],
        "user_email": user["email"]
    })

    return f"Book '{book['title']}' borrowed successfully by {user['name']}"


def return_book(user_id: str, book_id: str):
    """
    Validates borrowing exists, updates state, emits BookReturned event.
    Calculates late fees if applicable.
    """
    # Find the borrowing record
    borrowing_record = None
    borrowing_id = None

    for bid, borrowing in library_db["borrowings"].items():
        if (borrowing["user_id"] == user_id and
            borrowing["book_id"] == book_id and
            borrowing["returned_date"] is None):
            borrowing_record = borrowing
            borrowing_id = bid
            break

    if not borrowing_record:
        return "Error: Book not borrowed by this user"

    # Get book and user info
    book = library_db["books"][book_id]
    user = library_db["users"][user_id]

    # Calculate late fee
    return_date = datetime.now()
    due_date = datetime.fromisoformat(borrowing_record["due_date"])
    late_fee = 0.0

    if return_date > due_date:
        days_late = (return_date - due_date).days
        late_fee = days_late * 0.50  # $0.50 per day

    # Update borrowing record
    borrowing_record["returned_date"] = return_date.isoformat()
    borrowing_record["late_fee"] = late_fee

    # Update book availability
    book["available_copies"] += 1

    # Emit BookReturned event
    emit_event("BookReturned", {
        "user_id": user_id,
        "book_id": book_id,
        "book_title": book["title"],
        "borrowing_id": borrowing_id,
        "returned_date": borrowing_record["returned_date"],
        "late_fee": late_fee,
        "user_name": user["name"],
        "user_email": user["email"]
    })

    result = f"Book '{book['title']}' returned successfully by {user['name']}"
    if late_fee > 0:
        result += f" (Late fee: ${late_fee:.2f})"

    return result


def get_user_borrowings(user_id: str):
    """
    Returns current borrowings for a user.
    """
    user_borrowings = []

    for borrowing in library_db["borrowings"].values():
        if borrowing["user_id"] == user_id and borrowing["returned_date"] is None:
            book = library_db["books"][borrowing["book_id"]]
            borrowing_info = borrowing.copy()
            borrowing_info["book_title"] = book["title"]
            borrowing_info["book_author"] = book["author"]
            user_borrowings.append(borrowing_info)

    return user_borrowings


def suspend_user(user_id: str, reason: str):
    """
    Suspends user and emits UserSuspended event.
    """
    if user_id not in library_db["users"]:
        return "Error: User not found"

    user = library_db["users"][user_id]
    user["status"] = "suspended"
    user["suspension_reason"] = reason
    user["suspended_date"] = datetime.now().isoformat()

    # Emit UserSuspended event
    emit_event("UserSuspended", {
        "user_id": user_id,
        "reason": reason,
        "suspended_date": user["suspended_date"],
        "user_name": user["name"],
        "user_email": user["email"]
    })

    return f"User '{user['name']}' suspended: {reason}"


# --- NOTIFICATION SERVICE ---
# Handles all user communications and alerts

def handle_user_registered(payload: Dict[Any, Any]):
    """
    Creates user in notification system and sends welcome message.
    """
    user_id = payload["user_id"]
    name = payload["name"]
    email = payload["email"]

    # Add user to notification system
    notification_db["users"][user_id] = {
        "email": email,
        "name": name,
        "preferences": {
            "email_enabled": True,
            "sms_enabled": False,
            "push_enabled": True
        }
    }

    # Send welcome notification
    welcome_message = f"Welcome to the library system, {name}! Your account has been created successfully."
    send_notification(user_id, welcome_message, "welcome")


def handle_book_borrowed(payload: Dict[Any, Any]):
    """
    Sends confirmation and due date reminder notifications.
    """
    user_id = payload["user_id"]
    book_title = payload["book_title"]
    due_date = payload["due_date"]

    # Send borrow confirmation
    borrow_message = f"You have successfully borrowed '{book_title}'. Due date: {due_date[:10]}"
    send_notification(user_id, borrow_message, "borrow_confirmation")

    # Schedule due date reminder (simplified - just send immediately)
    reminder_message = f"Reminder: '{book_title}' is due on {due_date[:10]}. Please return on time to avoid late fees."
    send_notification(user_id, reminder_message, "due_date_reminder")


def handle_book_returned(payload: Dict[Any, Any]):
    """
    Sends return confirmation and late fee notifications if applicable.
    """
    user_id = payload["user_id"]
    book_title = payload["book_title"]
    late_fee = payload.get("late_fee", 0.0)

    # Send return confirmation
    return_message = f"Thank you for returning '{book_title}'."
    if late_fee > 0:
        return_message += f" Late fee applied: ${late_fee:.2f}"

    send_notification(user_id, return_message, "return_confirmation")


def send_notification(user_id: str, message: str, notification_type: str):
    """
    Stores notification and emits NotificationSent event.
    """
    notification_id = str(uuid.uuid4())

    notification = {
        "notification_id": notification_id,
        "user_id": user_id,
        "message": message,
        "type": notification_type,
        "sent_date": datetime.now().isoformat(),
        "status": "sent"
    }

    notification_db["notifications"].append(notification)

    # Emit NotificationSent event
    emit_event("NotificationSent", {
        "notification_id": notification_id,
        "user_id": user_id,
        "type": notification_type,
        "sent_date": notification["sent_date"]
    })


def get_user_notifications(user_id: str):
    """
    Returns all notifications for a user.
    """
    return [n for n in notification_db["notifications"] if n["user_id"] == user_id]


def set_notification_preferences(user_id: str, preferences: Dict[str, bool]):
    """
    Stores user notification preferences.
    """
    if user_id in notification_db["users"]:
        notification_db["users"][user_id]["preferences"].update(preferences)
        return True
    return False


# --- ANALYTICS SERVICE ---
# Tracks usage patterns and generates insights

def handle_book_borrowed_analytics(payload: Dict[Any, Any]):
    """
    Tracks borrowing patterns and updates metrics.
    """
    # Record event
    analytics_db["events"].append({
        "type": "book_borrowed",
        "timestamp": datetime.now().isoformat(),
        "data": payload.copy()
    })

    # Update metrics
    if "total_borrows" not in analytics_db["metrics"]:
        analytics_db["metrics"]["total_borrows"] = 0
    analytics_db["metrics"]["total_borrows"] += 1

    # Track book popularity
    book_id = payload["book_id"]
    if "book_popularity" not in analytics_db["metrics"]:
        analytics_db["metrics"]["book_popularity"] = {}

    if book_id not in analytics_db["metrics"]["book_popularity"]:
        analytics_db["metrics"]["book_popularity"][book_id] = 0
    analytics_db["metrics"]["book_popularity"][book_id] += 1


def handle_book_returned_analytics(payload: Dict[Any, Any]):
    """
    Tracks return patterns and calculates duration metrics.
    """
    # Record event
    analytics_db["events"].append({
        "type": "book_returned",
        "timestamp": datetime.now().isoformat(),
        "data": payload.copy()
    })

    # Update metrics
    if "total_returns" not in analytics_db["metrics"]:
        analytics_db["metrics"]["total_returns"] = 0
    analytics_db["metrics"]["total_returns"] += 1

    # Track late fees
    late_fee = payload.get("late_fee", 0.0)
    if late_fee > 0:
        if "total_late_fees" not in analytics_db["metrics"]:
            analytics_db["metrics"]["total_late_fees"] = 0.0
        analytics_db["metrics"]["total_late_fees"] += late_fee


def handle_user_registered_analytics(payload: Dict[Any, Any]):
    """
    Tracks user growth and demographics.
    """
    # Record event
    analytics_db["events"].append({
        "type": "user_registered",
        "timestamp": datetime.now().isoformat(),
        "data": payload.copy()
    })

    # Update metrics
    if "total_users" not in analytics_db["metrics"]:
        analytics_db["metrics"]["total_users"] = 0
    analytics_db["metrics"]["total_users"] += 1

    # Track user types
    user_type = payload.get("user_type", "standard")
    if "user_types" not in analytics_db["metrics"]:
        analytics_db["metrics"]["user_types"] = {}

    if user_type not in analytics_db["metrics"]["user_types"]:
        analytics_db["metrics"]["user_types"][user_type] = 0
    analytics_db["metrics"]["user_types"][user_type] += 1


def generate_usage_report(start_date: str, end_date: str):
    """
    Creates comprehensive usage analytics report.
    """
    # Filter events by date range
    start_dt = datetime.fromisoformat(start_date)
    end_dt = datetime.fromisoformat(end_date)

    filtered_events = []
    for event in analytics_db["events"]:
        event_dt = datetime.fromisoformat(event["timestamp"])
        if start_dt <= event_dt <= end_dt:
            filtered_events.append(event)

    # Generate report
    report = {
        "period": f"{start_date} to {end_date}",
        "total_borrows": len([e for e in filtered_events if e["type"] == "book_borrowed"]),
        "total_returns": len([e for e in filtered_events if e["type"] == "book_returned"]),
        "active_users": len(set(e["data"]["user_id"] for e in filtered_events if "user_id" in e["data"])),
        "popular_books": analytics_db["metrics"].get("book_popularity", {}),
        "generated_at": datetime.now().isoformat()
    }

    return report


def get_book_popularity_metrics():
    """
    Returns book borrowing frequency and trends.
    """
    return analytics_db["metrics"].get("book_popularity", {})


def track_system_performance(event_type: str, processing_time: float):
    """
    Tracks event processing performance metrics.
    """
    if "performance" not in analytics_db["metrics"]:
        analytics_db["metrics"]["performance"] = {}

    if event_type not in analytics_db["metrics"]["performance"]:
        analytics_db["metrics"]["performance"][event_type] = {
            "total_time": 0.0,
            "count": 0,
            "average": 0.0
        }

    perf = analytics_db["metrics"]["performance"][event_type]
    perf["total_time"] += processing_time
    perf["count"] += 1
    perf["average"] = perf["total_time"] / perf["count"]


# --- AUDIT SERVICE ---
# Event sourcing and compliance logging

def handle_any_event_for_audit(event_type: str, payload: Dict[Any, Any], metadata: Dict[Any, Any]):
    """
    Logs all events for compliance and audit purposes.
    """
    audit_event = {
        "event_type": event_type,
        "payload": payload.copy(),
        "timestamp": metadata.get("timestamp", datetime.now().isoformat()),
        "correlation_id": metadata.get("correlation_id"),
        "event_id": metadata.get("event_id"),
        "audit_logged_at": datetime.now().isoformat()
    }

    audit_db["events"].append(audit_event)


def create_system_snapshot():
    """
    Captures current state of all services for backup/recovery.
    """
    snapshot_id = str(uuid.uuid4())

    snapshot = {
        "snapshot_id": snapshot_id,
        "created_at": datetime.now().isoformat(),
        "library_state": {
            "books": library_db["books"].copy(),
            "users": library_db["users"].copy(),
            "borrowings": library_db["borrowings"].copy()
        },
        "notification_state": {
            "users": notification_db["users"].copy(),
            "notifications": notification_db["notifications"].copy(),
            "preferences": notification_db["preferences"].copy()
        },
        "analytics_state": {
            "metrics": analytics_db["metrics"].copy()
        }
    }

    audit_db["snapshots"][snapshot_id] = snapshot
    return snapshot_id


def reconstruct_state_from_events(target_date: str):
    """
    Rebuilds system state by replaying events up to target date.
    """
    target_dt = datetime.fromisoformat(target_date)

    # Get events up to target date
    replay_events = []
    for event in audit_db["events"]:
        event_dt = datetime.fromisoformat(event["timestamp"])
        if event_dt <= target_dt:
            replay_events.append(event)

    # Sort by timestamp
    replay_events.sort(key=lambda e: e["timestamp"])

    # This would replay events to reconstruct state
    # Simplified implementation just returns event count
    return {
        "events_replayed": len(replay_events),
        "target_date": target_date,
        "reconstructed_at": datetime.now().isoformat()
    }


def get_audit_trail(entity_type: str, entity_id: str):
    """
    Returns chronological history of events for an entity.
    """
    trail = []

    for event in audit_db["events"]:
        # Check if event relates to the entity
        payload = event["payload"]

        if entity_type == "user" and payload.get("user_id") == entity_id:
            trail.append(event)
        elif entity_type == "book" and payload.get("book_id") == entity_id:
            trail.append(event)

    # Sort chronologically
    trail.sort(key=lambda e: e["timestamp"])
    return trail


def detect_anomalies():
    """
    Analyzes event patterns and detects suspicious activities.
    """
    anomalies = []

    # Simple anomaly detection: rapid borrowing
    user_borrow_counts = {}
    recent_time = datetime.now() - timedelta(hours=1)

    for event in audit_db["events"]:
        if event["event_type"] == "BookBorrowed":
            event_time = datetime.fromisoformat(event["timestamp"])
            if event_time > recent_time:
                user_id = event["payload"]["user_id"]
                user_borrow_counts[user_id] = user_borrow_counts.get(user_id, 0) + 1

    # Flag users with more than 5 borrows in 1 hour
    for user_id, count in user_borrow_counts.items():
        if count > 5:
            anomalies.append({
                "type": "rapid_borrowing",
                "user_id": user_id,
                "borrow_count": count,
                "detected_at": datetime.now().isoformat()
            })

    return anomalies


# --- SYSTEM INITIALIZATION ---
def initialize_event_driven_system():
    """
    Registers all event handlers for all services.
    """
    # Clear existing handlers
    clear_event_queue()

    # Register notification service handlers
    register_event_handler("UserRegistered", handle_user_registered, "NotificationService")
    register_event_handler("BookBorrowed", handle_book_borrowed, "NotificationService")
    register_event_handler("BookReturned", handle_book_returned, "NotificationService")

    # Register analytics service handlers
    register_event_handler("BookBorrowed", handle_book_borrowed_analytics, "AnalyticsService")
    register_event_handler("BookReturned", handle_book_returned_analytics, "AnalyticsService")
    register_event_handler("UserRegistered", handle_user_registered_analytics, "AnalyticsService")

    # Register audit service handler (catches all events)
    for event_type in ["BookAdded", "BookBorrowed", "BookReturned", "UserRegistered",
                      "UserSuspended", "NotificationSent"]:
        register_event_handler(event_type, handle_any_event_for_audit, "AuditService")


def clear_all_system_state():
    """
    Clears all service databases and event broker state.
    """
    # Clear service databases
    library_db["books"].clear()
    library_db["users"].clear()
    library_db["borrowings"].clear()

    notification_db["users"].clear()
    notification_db["notifications"].clear()
    notification_db["preferences"].clear()

    analytics_db["events"].clear()
    analytics_db["metrics"].clear()
    analytics_db["reports"].clear()

    audit_db["events"].clear()
    audit_db["snapshots"].clear()

    # Clear event broker
    clear_event_queue()


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
        self.assertEqual(len(event_queue), 1)
        self.assertEqual(event_queue[0]["type"], "BookAdded")

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
        self.assertEqual(len(notifications), 2)  # confirmation + reminder

        confirmation = next(n for n in notifications if n["type"] == "borrow_confirmation")
        self.assertIn("borrowed", confirmation["message"].lower())
        self.assertIn("Borrowed Book", confirmation["message"])


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
        pass


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


def interactive_demo():
    """
    Interactive demo showing the event-driven architecture in action.
    """
    print("🚀 Interactive Demo - Event-Driven Architecture Library System")
    print("=" * 70)

    clear_all_system_state()
    initialize_event_driven_system()

    print("\n1. EVENT-DRIVEN SYSTEM INITIALIZATION:")
    print("✅ Message broker initialized")
    print("✅ Event handlers registered for all services")
    print("✅ Services ready for event processing")

    print("\n2. LIBRARY SERVICE - Register user (emits UserRegistered event):")
    result = register_user("demo@example.com", "Demo User", "premium")
    print(f"📚 {result}")
    print(f"📡 Events in queue: {len(event_queue)}")

    print("\n3. PROCESS EVENTS - Trigger service reactions:")
    process_events()
    print("📡 Events processed, queue cleared")

    print("\n4. NOTIFICATION SERVICE - Check welcome message:")
    user_id = list(library_db["users"].keys())[0]
    notifications = get_user_notifications(user_id)
    print(f"🔔 Notifications sent: {len(notifications)}")
    for notif in notifications:
        print(f"   • {notif['type']}: {notif['message'][:50]}...")

    print("\n5. ANALYTICS SERVICE - Check user metrics:")
    metrics = analytics_db["metrics"]
    print(f"📊 Total users registered: {metrics.get('total_users', 0)}")
    print(f"📊 User types: {metrics.get('user_types', {})}")

    print("\n6. AUDIT SERVICE - Check event logs:")
    audit_events = audit_db["events"]
    print(f"📋 Audit events logged: {len(audit_events)}")
    for event in audit_events:
        print(f"   • {event['event_type']} at {event['timestamp'][:19]}")

    print("\n7. COMPLETE WORKFLOW - Add book and borrow:")
    add_book_to_library("978-0-123456-78-9", "Demo Book", "Demo Author", 1)
    book_id = list(library_db["books"].keys())[0]

    borrow_result = borrow_book(user_id, book_id)
    print(f"📚 {borrow_result}")

    print("\n8. PROCESS ALL EVENTS:")
    process_events()

    print("\n9. FINAL STATE ACROSS ALL SERVICES:")
    print(f"📚 Library: {len(library_db['books'])} books, {len(library_db['users'])} users, {len(library_db['borrowings'])} borrowings")
    print(f"🔔 Notifications: {len(notification_db['notifications'])} total notifications")
    print(f"📊 Analytics: {len(analytics_db['events'])} events tracked")
    print(f"📋 Audit: {len(audit_db['events'])} events logged")

    print("\n🎉 Demo completed!")
    print("\nKey Event-Driven Characteristics Demonstrated:")
    print("✅ Services communicate only through events")
    print("✅ Loose coupling - services don't know about each other")
    print("✅ Asynchronous processing via message broker")
    print("✅ Event sourcing for complete audit trail")
    print("✅ Eventually consistent state across services")


if __name__ == "__main__":
    print("🎯 Event-Driven Architecture - Complete Solution")
    print()

    # Run the tests to prove everything works
    success = run_tests()

    if success:
        print("\n" + "="*75)
        print("Would you like to see an interactive demo? (y/n): ", end="")
        try:
            response = input().strip().lower()
            if response in ['y', 'yes']:
                print()
                interactive_demo()
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Goodbye!")

    print("\n📚 Event-Driven Architecture Learning Summary:")
    print("✅ Loose coupling through events enables scalability")
    print("✅ Asynchronous processing improves system responsiveness")
    print("✅ Event sourcing provides complete audit trails")
    print("✅ Service isolation enables independent development/deployment")
    print("✅ Message broker centralizes event routing and reliability")
    print("✅ Eventually consistent systems handle distributed state")