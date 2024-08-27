from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
from io import BytesIO

app = Flask(__name__)

API_ENDPOINT = "https://html2pdf.app?Secret=zBYnyZy7nKNHtT0xJgu2CIbHgUuxzOQFXPj76Ne7wkdr09by2NExCOxKv15J2sC4"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        page_size = request.form.get('page_size')
        orientation = request.form.get('orientation')

        # Basic URL validation
        if not url or not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Please enter a valid URL.'}), 400

        # Prepare API request payload
        payload = {
            'html': url,
            'page_size': page_size,
            'orientation': orientation
        }

        try:
            # Make request to HTML2PDF API
            response = requests.post(API_ENDPOINT, json=payload)
            response.raise_for_status()

            # Convert response to a PDF file
            pdf_data = BytesIO(response.content)
            pdf_filename = 'converted.pdf'

            return send_file(pdf_data, as_attachment=True, download_name=pdf_filename, mimetype='application/pdf')

        except requests.exceptions.RequestException as e:
            return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=5000)