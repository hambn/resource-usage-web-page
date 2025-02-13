from flask import Flask, render_template_string
import datetime
import random
import psutil
from tzlocal import get_localzone
import platform
import os

app = Flask(__name__)

# Three specific colors for background
BACKGROUND_COLORS = [
    "#FF6B6B",  # Coral Red
    "#4ECDC4",  # Turquoise
    "#45B7D1",  # Sky Blue
]

# HTML template with inline CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DevOps Test App</title>
    <style>
        body {
            background-color: {{ background_color }};
            font-family: Arial, sans-serif;
            color: white;
            height: 100vh;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
        }
        .section {
            margin: 1rem 0;
        }
        .resource-bar {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 0.5rem;
            margin: 0.5rem 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hello World</h1>

        <div class="section">
            <h2>Time Information</h2>
            <p>Host Time: {{ host_time }}</p>
            <p>Your Local Time: <span id="localTime"></span></p>
        </div>

        <!-- Added Application Usage section -->
        <div class="section">
            <h2>Application Usage</h2>
            <div class="resource-bar">
                App CPU Usage: {{ app_cpu }}%
            </div>
            <div class="resource-bar">
                App RAM Usage: {{ app_ram_used }} MB
            </div>
        </div>

        <div class="section">
            <h2>System Resources</h2>
            <div class="resource-bar">
                RAM Usage: {{ ram_used }}/{{ ram_total }} GB
            </div>
            <div class="resource-bar">
                Overall CPU Usage: {{ overall_cpu }}%
            </div>
            {% for cpu in cpu_percents %}
            <div class="resource-bar">
                CPU Core {{ loop.index }}: {{ cpu }}%
            </div>
            {% endfor %}
        </div>
    </div>

    <script>
        // Function to update local date and time
        function updateLocalTime() {
            const options = {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            };
            const localTime = new Date().toLocaleString(undefined, options);
            document.getElementById('localTime').textContent = localTime;
        }

        // Update date and time immediately and then every second
        updateLocalTime();
        setInterval(updateLocalTime, 1000);
    </script>
</body>
</html>
'''

def get_system_info():
    """Get system resource information."""
    # RAM information
    ram = psutil.virtual_memory()
    ram_total = round(ram.total / (1024.0 ** 3), 1)  # Convert to GB
    ram_used = round(ram.used / (1024.0 ** 3), 1)    # Convert to GB

    # Overall CPU usage
    overall_cpu = round(psutil.cpu_percent(interval=1), 1)

    # Per-core CPU information
    cpu_percents = [round(x, 1) for x in psutil.cpu_percent(interval=1, percpu=True)]

    return ram_used, ram_total, overall_cpu, cpu_percents

# New function to get current application (process) usage information
def get_application_info():
    process = psutil.Process(os.getpid())
    # Get CPU usage for this process
    app_cpu = round(process.cpu_percent(interval=0.1), 1)
    # Get memory usage in MB
    mem_info = process.memory_info()
    app_ram_used = round(mem_info.rss / (1024.0 ** 2), 1)
    return app_cpu, app_ram_used

@app.route('/')
def home():
    # Randomly select one color from the predefined colors
    background_color = random.choice(BACKGROUND_COLORS)

    # Get system information
    ram_used, ram_total, overall_cpu, cpu_percents = get_system_info()

    # Get application usage information
    app_cpu, app_ram_used = get_application_info()

    # Get host date and time
    host_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return render_template_string(
        HTML_TEMPLATE,
        background_color=background_color,
        host_time=host_time,
        ram_used=ram_used,
        ram_total=ram_total,
        overall_cpu=overall_cpu,
        cpu_percents=cpu_percents,
        app_cpu=app_cpu,
        app_ram_used=app_ram_used
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)