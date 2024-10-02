from flask import Flask, request, send_file, render_template
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve the index.html from the templates directory
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            input_image = Image.open(file.stream)
            output_image = remove(input_image)
            
            img_io = io.BytesIO()
            output_image.save(img_io, 'PNG')
            img_io.seek(0)
            return send_file(img_io, mimetype='image/png')
    
    # Use render_template to serve index.html from the templates directory
    return render_template('index.html')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
