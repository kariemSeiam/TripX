import os
import uuid
from werkzeug.utils import secure_filename
from app.config import Config

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_vehicle_photo(file):
    filename = secure_filename(file.filename)
    unique_filename = str(uuid.uuid4()) + "_" + filename
    file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
    file.save(file_path)
    return file_path
