from flask import Flask, jsonify, render_template
import psutil
import platform
import time

app = Flask(__name__)

cpu_history = {
    'labels': [],
    'data': []
}

ram_history = {
    'labels': [],
    'data': []
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_system_data():
    global cpu_history, ram_history

    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent
    device_info = platform.uname()

    if len(cpu_history['data']) >= 10:
        cpu_history['data'].pop(0)
        ram_history['data'].pop(0)
        cpu_history['labels'].pop(0)
        ram_history['labels'].pop(0)

    cpu_history['data'].append(cpu_usage)
    ram_history['data'].append(ram_usage)
    cpu_history['labels'].append(time.strftime("%H:%M:%S"))
    ram_history['labels'].append(time.strftime("%H:%M:%S"))

    return jsonify({
        'cpu': cpu_usage,
        'ram': ram_usage,
        'device': f'{device_info.system} {device_info.node} {device_info.release}',
        'cpuHistory': cpu_history,
        'ramHistory': ram_history
    })

if __name__ == '__main__':
    app.run(debug=True)
