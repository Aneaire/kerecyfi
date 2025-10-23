#!/usr/bin/env python3
# Simple test script to simulate the flow without running the server

import json
import time
import uuid

VOUCHERS_FILE = '../server/vouchers.json'
LOGS_FILE = '../logs/transactions.log'

# Simulate insert
print("Simulating plastic insertion...")
voucher = str(uuid.uuid4())[:8]
expiry = time.time() + 300
vouchers = {}
vouchers[voucher] = expiry
with open(VOUCHERS_FILE, 'w') as f:
    json.dump(vouchers, f)
user_id = str(uuid.uuid4())[:8]
print(f"LOG: insert by {user_id} - voucher:{voucher}")
print("LED: Green - Plastic accepted")
print(f"Voucher generated: {voucher}")

# Simulate validation
print("Simulating voucher validation...")
if voucher in vouchers and time.time() < vouchers[voucher]:
    print("LED: Blue - Access granted")
    print(f"LOG: access_granted by {user_id} - voucher:{voucher}")
    print("Internet access granted for 5 minutes!")
else:
    print("LED: Red - Access denied")
    print("Invalid voucher")

print("End-to-end test completed.")