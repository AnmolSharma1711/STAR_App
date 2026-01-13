import re

# Test CORS regex patterns
test_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://192.168.198.127:8000",
    "http://192.168.56.1:5173",
    "http://10.0.2.2:8000",
    "capacitor://localhost",
    "ionic://localhost"
]

patterns = [
    r"^http://localhost:\d+$",
    r"^http://127\.0\.0\.1:\d+$",
    r"^http://192\.168\.\d{1,3}\.\d{1,3}:\d+$",
    r"^http://10\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+$",
    r"^http://172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}:\d+$",
    r"^capacitor://.*$",
    r"^ionic://.*$",
]

print("Testing CORS regex patterns:\n")
for origin in test_origins:
    matched = False
    for pattern in patterns:
        if re.match(pattern, origin):
            print(f"✓ {origin} -> MATCHED by {pattern}")
            matched = True
            break
    if not matched:
        print(f"✗ {origin} -> NO MATCH")
