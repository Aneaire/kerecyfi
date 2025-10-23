from flask import Flask, request, redirect, make_response, render_template_string, url_for
import os
import time
import uuid
import json

app = Flask(__name__)

VOUCHERS_FILE = 'vouchers.json'
LOGS_FILE = '../logs/transactions.log'

# Ensure files exist
if not os.path.exists(VOUCHERS_FILE):
    with open(VOUCHERS_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(LOGS_FILE):
    with open(LOGS_FILE, 'w') as f:
        pass

def log_transaction(action, user_id, details=''):
    print(f"LOG: {action} by {user_id} - {details}")  # Console feedback
    with open(LOGS_FILE, 'a') as f:
        f.write(f"{time.time()},{user_id},{action},{details}\n")

@app.route('/')
def index():
    # Pre-insertion interface
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>RecyFi Kiosk</title></head>
    <body>
    <h1>Welcome to RecyFi</h1>
    <p>Insert plastic to get 5 minutes of Wi-Fi!</p>
    <button onclick="simulateInsert()">Simulate Insert Plastic</button>
    <script>
    function simulateInsert() {
        fetch('/insert', {method: 'POST'}).then(() => location.reload());
    }
    </script>
    </body>
    </html>
    ''')

@app.route('/insert', methods=['POST'])
def insert():
    print("LED: Green - Plastic accepted")  # Simulate LED feedback
    # Simulate insertion: generate voucher
    voucher = str(uuid.uuid4())[:8]  # Short voucher
    expiry = time.time() + 300  # 5 min
    with open(VOUCHERS_FILE, 'r+') as f:
        vouchers = json.load(f)
        vouchers[voucher] = expiry
        f.seek(0)
        json.dump(vouchers, f)
    user_id = str(uuid.uuid4())[:8]
    log_transaction('insert', user_id, f'voucher:{voucher}')
    return render_template_string(f'''
    <!DOCTYPE html>
    <html>
    <head><title>Voucher Generated</title></head>
    <body>
    <h1>Plastic Accepted!</h1>
    <p>Your voucher: {voucher}</p>
    <p>Use it to access Wi-Fi for 5 minutes.</p>
    <a href="/portal">Go to Portal</a>
    </body>
    </html>
    ''')

@app.route('/portal')
def portal():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head><title>Captive Portal</title></head>
    <body>
    <h1>Enter Voucher</h1>
    <form action="/validate" method="post">
      <input type="text" name="voucher" required>
      <button type="submit">Submit</button>
    </form>
    </body>
    </html>
    ''')

@app.route('/validate', methods=['POST'])
def validate():
    voucher = request.form.get('voucher')
    with open(VOUCHERS_FILE, 'r') as f:
        vouchers = json.load(f)
    if voucher in vouchers and time.time() < vouchers[voucher]:
        print("LED: Blue - Access granted")  # Simulate LED feedback
        user_id = str(uuid.uuid4())[:8]
        log_transaction('access_granted', user_id, f'voucher:{voucher}')
        resp = make_response(redirect('http://example.com/success'))  # Redirect to success
        resp.set_cookie('authenticated', 'true', max_age=300)  # 5 min cookie
        return resp
    print("LED: Red - Access denied")  # Simulate LED feedback
    log_transaction('access_denied', 'unknown', f'voucher:{voucher}')
    return "Invalid or expired voucher", 403

@app.route('/success')
def success():
    return "Internet access granted for 5 minutes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)