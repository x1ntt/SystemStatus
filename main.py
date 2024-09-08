import os
from flask import Flask, render_template, request, jsonify, send_file
from status import status
from ssd_oled import oled_display
import json
import threading

app = Flask(__name__, static_folder='web', template_folder='web/html')

@app.route('/api/get/all_node')
def getall_node():
    return jsonify(status.getall_node())

@app.route('/api/update/node', methods=['POST'])
def update_node():
    node = request.form.get('node')
    if not node:
        return "0"
    status.update_node(json.loads(node), str(request.remote_addr))
    return "0"

@app.route('/api/update/oled', methods=['GET'])
def update_oled_status():
	active = request.args.get('active')
	if active not in ['true', 'false']:
		return "1"

	if active == "true":
		active = True
	else:
		active = False
	oled_display.switch_active(active)
	return "0";

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
	oled_display.start()
	app.run(debug=False, host='0.0.0.0')
	oled_display.stop()
