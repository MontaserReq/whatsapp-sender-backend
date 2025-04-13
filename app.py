from flask import Flask, request, render_template, jsonify
import pywhatkit as kit
import time
import re

app = Flask(__name__)

def format_number(number):
    number = number.strip()

    # لو الرقم فيه +962 مسبقًا، نتركه
    if number.startswith('+962'):
        return number

    # لو بدأ بـ 962 بدون + نضيف +
    if number.startswith('962'):
        return '+' + number

    # لو بدأ بـ 0 نحذفها ونضيف +962
    if number.startswith('0'):
        return '+962' + number[1:]

    # أي رقم آخر، نعتبره محلي ونضيف +962 على طوله
    return '+962' + number

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_whatsapp():
    data = request.get_json()
    numbers = data.get('numbers', [])
    message = data.get('message', '')
    delay = 2

    results = []

    try:
        for raw_number in numbers:
            number = format_number(raw_number)
            kit.sendwhatmsg_instantly(number, message)
            results.append(f"تم الإرسال إلى {number}")
            time.sleep(delay)

        return jsonify({"status": "success", "results": results})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
