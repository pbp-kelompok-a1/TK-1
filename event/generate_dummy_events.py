import datetime
import uuid
from django.contrib.auth import get_user_model
from django.utils import timezone
# Note: Ensure your Django app is correctly named 'event' for this import to work.
from event.models import Event, EventType

# --- CONFIGURATION ---
NUM_GLOBAL_EVENTS = 2
NUM_COMMUNITY_EVENTS = 3
# ---------------------

def create_dummy_data():
    """
    Creates a basic Admin user, a regular User, and several sample events 
    for testing the event list page and filtering logic.
    """
    try:
        # 1. Get the correct User model dynamically (best practice)
        User = get_user_model()
    except Exception as e:
        print("Error: Could not retrieve Django User Model. Is settings.py configured correctly?")
        print(f"Error details: {e}")
        return

    # 2. Create sample users (Admin and Regular)
    try:
        admin_user, created = User.objects.get_or_create(username='admin_user', defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        })
        if created:
            # Note: set_password is required for the admin user to log in
            admin_user.set_password('adminpassword')
            admin_user.save()
            print(f"Created Admin User: {admin_user.username}")

        community_user, created = User.objects.get_or_create(username='john_doe', defaults={
            'email': 'john@example.com',
            'is_staff': False
        })
        if created:
            community_user.set_password('userpassword')
            community_user.save()
            print(f"Created Community User: {community_user.username}")

    except Exception as e:
        print(f"Error creating users. Have you run initial user migrations? Error: {e}")
        return

    # 3. Create Global Events (Admin Only)
    print("\n--- Creating Global Events ---")
    for i in range(1, NUM_GLOBAL_EVENTS + 1):
        # The UUID field will be generated automatically, no need to pass it explicitly
        Event.objects.create(
            title=f"Global Tennis Open {i}",
            description=f"Major international tennis tournament, Round {i}. Watch the best athletes compete!",
            start_time=timezone.now() + datetime.timedelta(days=7 * i),
            location=f"Venue City {i}, International Arena",
            official_link=f"http://global-open-{i}.com",
            event_type=EventType.GLOBAL,
            creator=admin_user
        )
        print(f"Created Global Event {i}")

    # 4. Create Community Events (User Created)
    print("\n--- Creating Community Events ---")
    for i in range(1, NUM_COMMUNITY_EVENTS + 1):
        Event.objects.create(
            title=f"Local Basketball League Match {i}",
            description=f"A small, local tournament organized by the community. Come cheer for your neighbors!",
            start_time=timezone.now() + datetime.timedelta(days=i * 2),
            location=f"Local Gym {i}, Community Center",
            official_link="",
            event_type=EventType.COMMUNITY,
            creator=community_user
        )
        print(f"Created Community Event {i}")
    
    print("\n--- Dummy Data Generation Complete ---")

# Only run if the script is executed directly (via exec in the shell)
# We don't use if __name__ == '__main__': because this file is executed via exec() inside the shell.
# create_dummy_data() is intended to be called explicitly.
