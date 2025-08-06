from flask import Flask, request, send_file, render_template
from flask_cors import CORS
import imageio.v3 as iio
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Configure upload settings
UPLOAD_FOLDER = 'temp_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/create-gif', methods=['POST'])
def create_gif():
    try:
        # Check if both images are present
        if 'image1' not in request.files or 'image2' not in request.files:
            return {'error': 'Both images are required'}, 400
        
        image1 = request.files['image1']
        image2 = request.files['image2']
        
        # Check if files are selected
        if image1.filename == '' or image2.filename == '':
            return {'error': 'No files selected'}, 400
        
        # Check if files are allowed
        if not (allowed_file(image1.filename) and allowed_file(image2.filename)):
            return {'error': 'Invalid file type. Please use PNG, JPG, JPEG, GIF, BMP, or TIFF'}, 400
        
        # Get parameters
        duration = int(request.form.get('duration', 1000))
        loops = int(request.form.get('loops', 0))
        
        # Generate unique filenames
        unique_id = str(uuid.uuid4())
        image1_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_1_{secure_filename(image1.filename)}")
        image2_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_2_{secure_filename(image2.filename)}")
        gif_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_output.gif")
        
        # Save uploaded files
        image1.save(image1_path)
        image2.save(image2_path)
        
        # Create GIF
        images = []
        images.append(iio.imread(image1_path))
        images.append(iio.imread(image2_path))
        
        # Write GIF with specified parameters
        iio.imwrite(gif_path, images, duration=duration, loop=loops)
        
        # Clean up uploaded images
        os.remove(image1_path)
        os.remove(image2_path)
        
        # Return the GIF file
        return send_file(gif_path, as_attachment=True, download_name='animated.gif', mimetype='image/gif')
        
    except Exception as e:
        return {'error': f'Failed to create GIF: {str(e)}'}, 500

@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'GIF Creator API is running'}

if __name__ == '__main__':
    print("🎞️ Starting GIF Creator Server...")
    print("📝 Open http://localhost:5000 in your browser")
    app.run(debug=True, host='0.0.0.0', port=5000)
