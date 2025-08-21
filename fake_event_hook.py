import typing

# Step 1: Define EventHook type
EventHook = typing.Callable[..., typing.Any]

# Step 2: Define some hook functions
def log_event(data):
    print("📝 Logging event:", data)

def check_login(data):
    if data.get("username") == "admin" and data.get("password") == "123":
        print("✅ Login successful")
    else:
        print("❌ Invalid credentials")

# Step 3: Simple Fake Client with EventHooks
class FakeLoginClient:
    def __init__(self, event_hooks: dict[str, list[EventHook]] | None = None):
        self.event_hooks = event_hooks or {}

    def login(self, username, password):
        login_data = {"username": username, "password": password}

        # Trigger 'login' event hooks
        for hook in self.event_hooks.get("login", []):
            hook(login_data)

        print("🔐 Login process completed.")

# Step 4: Define hooks
hooks = {
    "login": [log_event, check_login]
}

# Step 5: Run it
client = FakeLoginClient(event_hooks=hooks)
client.login("admin", "123")  # Try correct login
print("----")
client.login("user", "wrongpass")  # Try wrong login
