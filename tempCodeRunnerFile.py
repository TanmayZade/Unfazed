API_KEY = "12345-ABCDE-DUMMY-API-KEY"

@app.route('/report', methods=['POST'])
def report():
    # Example use of API key (optional logging)
    print("Using API key:", API_KEY)

    # Handle file upload for pothole reporting
    pincode = request.form['Pin_Code']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Handle file upload
    photo = request.files['photo']
    if photo and photo.filename.endswith('.jpg'):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
        photo.save(image_path)
    else:
        return jsonify({'success': False, 'message': "Please upload a JPG file."}), 400

    # Get current timestamp and set status
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "Pending"  # Default status

    # Write the pothole report data to report_potholes.xlsx
    workbook = load_workbook(REPORT_FILE)
    sheet = workbook.active
    sheet.append([timestamp, image_path, pincode, latitude, longitude, status])
    workbook.save(REPORT_FILE)

    return jsonify({'success': True, 'message': "Pothole report submitted successfully!"})
