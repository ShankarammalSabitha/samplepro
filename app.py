from flask import Flask, render_template
import requests
import os

AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = 'ToiletStatus'

app = Flask(__name__)

# Function to get data from Airtable (with sorting and limiting)
def get_data():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}

    params = {
        'sort[0][field]': 'Timestamp',
        'sort[0][direction]': 'desc',
        'maxRecords': 5
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch data from Airtable", "status_code": response.status_code}


@app.route('/')
def user():
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{TABLE_NAME}?sort[0][field]=Timestamp&sort[0][direction]=desc&maxRecords=5"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    response = requests.get(url, headers=headers)

    print("Status Code:", response.status_code)
    print("Raw Response:", response.text)

    if response.status_code != 200:
        return f"❌ API Error: {response.status_code} - {response.text}", 500

    data = response.json()

    if 'records' in data and len(data['records']) > 0:
        records = data['records']
        return render_template('user.html', records=records)
    else:
        return "No data found or records are empty", 500


@app.route('/staff')
def staff():
    data = get_data()
    records = data.get('records', [])
    return render_template('staff.html', records=records)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)