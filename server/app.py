from flask import Flask, jsonify
from flask_cors import CORS
import psutil
import platform

app = Flask(__name__)
CORS(app)

@app.route('/api/stats')
def stats():
    # Wait for 1 second to get real CPU usage readings
    cpu_per_core = psutil.cpu_percent(interval=1, percpu=True)
    cpu_percent = round(sum(cpu_per_core) / len(cpu_per_core), 1)

    # Memory usage
    memory = psutil.virtual_memory()
    memory_stats = {
        'used': round(memory.used / (1024**3), 2),
        'available': round(memory.available / (1024**3), 2),
        'percent': memory.percent
    }

    # Disk space usage
    disk_path = 'C:\\' if platform.system() == 'Windows' else '/'
    disk = psutil.disk_usage(disk_path)
    disk_stats = {
        'used': round(disk.used / (1024**3), 2),
        'total': round(disk.total / (1024**3), 2),
        'percent': disk.percent
    }

    # Disk I/O activity
    io = psutil.disk_io_counters()
    disk_io = {
        'read_mb': round(io.read_bytes / (1024**2), 2),
        'write_mb': round(io.write_bytes / (1024**2), 2)
    }

    return jsonify({
        'cpu_percent': cpu_percent,
        'cpu_per_core': cpu_per_core,
        'memory': memory_stats,
        'disk': disk_stats,
        'disk_io': disk_io
    })

if __name__ == '__main__':
    app.run(debug=True)
