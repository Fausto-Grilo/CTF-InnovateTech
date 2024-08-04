from flask import Flask, request, render_template, send_from_directory
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

# Landing Page
@app.route('/')
def index():
    return render_template('home.html', title='Home')

# Compromised Blog Page (LFI)
@app.route('/blog')
def blog():
    page = request.args.get('page', 'home')
    try:
        return render_template(f'{page}.html')
    except:
        return "Page not found", 404

# User Profiles Page (XSS)
@app.route('/profiles')
def profiles():
    profile = request.args.get('profile', 'Guest')
    return render_template('profiles.html', profile=profile)

# Admin Messages (XXE)
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        try:
            xml = request.data.decode('utf-8')
            root = ET.fromstring(xml)
            message = root.find('message').text
            return f"Message received: {message}"
        except ET.ParseError as e:
            return f"XML Parsing Error: {e}", 400
        except Exception as e:
            return f"An error occurred: {e}", 500
    return render_template('messages.html')

# File Repository (IDOR)
@app.route('/files')
def files():
    file_id = request.args.get('file_id', '1')
    file_path = f'static/files/{file_id}.txt'
    if os.path.exists(file_path):
        return send_from_directory('static/files', f'{file_id}.txt')
    else:
        return "File not found", 404

# Final Challenge (Incident Report)
@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        report = request.form.get('report', '')
        if all(vuln in report for vuln in ['LFI', 'XSS', 'XXE', 'IDOR']):
            return "Congratulations! You've found all vulnerabilities. Here's your final flag: FLAG{COMPLETE_REPORT}"
        else:
            return "Your report is incomplete. Keep investigating!"
    return render_template('report.html')

if __name__ == '__main__':
    app.run(debug=True)
