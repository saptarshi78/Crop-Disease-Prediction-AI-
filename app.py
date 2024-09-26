# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_session import Session  # For server-side session management
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# import os
# import numpy as np
# from PIL import Image

# app = Flask(__name__)

# # Configure session
# app.secret_key = os.getenv("SESSION_SECRET")  # Set a secret key for sessions
# app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in the filesystem
# Session(app)  # Initialize the session

# # Load your pre-trained AI model (adjust the path accordingly)
# # model = load_model('path_to_your_model.h5')

# def preprocess_image(image):
#     image = image.resize((224, 224))  # Adjust based on your model
#     image = np.array(image) / 255.0  # Normalize
#     image = np.expand_dims(image, axis=0)
#     return image

# @app.route('/')
# def index():
#     return render_template('index.html')  # Render your index.html page

# @app.route('/login')
# def login():
#     flow = Flow.from_client_secrets_file(
#         'client_secrets.json',
#         scopes=['https://www.googleapis.com/auth/userinfo.profile'],
#         redirect_uri=url_for('callback', _external=True)  # Ensure HTTPS if applicable
#     )
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true'
#     )
#     session['state'] = state
#     return redirect(authorization_url)

# @app.route('/callback')
# def callback():
#     state = session.get('state')
#     if not state:
#         return redirect(url_for('login'))

#     flow = Flow.from_client_secrets_file(
#         'client_secrets.json',
#         scopes=['https://www.googleapis.com/auth/userinfo.profile'],
#         state=state,
#         redirect_uri=url_for('callback', _external=True)
#     )
#     flow.fetch_token(authorization_response=request.url)

#     credentials = flow.credentials
#     session['credentials'] = credentials_to_dict(credentials)

#     try:
#         userinfo_service = build('oauth2', 'v2', credentials=credentials)
#         user_info = userinfo_service.userinfo().get().execute()
#         session['name'] = user_info.get('name', 'User')
#         session['email'] = user_info.get('email', '')
#     except Exception as e:
#         print(f"Error fetching user info: {e}")
#         return redirect(url_for('login'))

#     return redirect(url_for('index'))  # Redirect to index.html

# def credentials_to_dict(credentials):
#     return {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }

# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file uploaded"})

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"})

#     try:
#         image = Image.open(file)
#         preprocessed_image = preprocess_image(image)
#         # predictions = model.predict(preprocessed_image)  # Uncomment once model is loaded
#         # predicted_class = np.argmax(predictions[0])
#         # labels = ['Healthy', 'Disease 1', 'Disease 2', 'Disease 3']  # Adjust as necessary
#         # result = labels[predicted_class]
#         # return jsonify({"prediction": result})
#         return jsonify({"prediction": "Example Prediction"})  # Placeholder response
#     except Exception as e:
#         return jsonify({"error": str(e)})

# @app.route('/logout')
# def logout():
#     session.clear()  # Clear the session
#     return redirect(url_for('index'))  # Redirect to index.html

# if __name__ == '__main__':
#     app.run(port=int(os.getenv("PORT")), debug=True)
