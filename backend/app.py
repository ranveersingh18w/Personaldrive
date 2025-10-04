"""
Personal Cloud Storage - Backend Server
Flask-based REST API for file upload, storage, and management
"""
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import hashlib
import mimetypes
from datetime import datetime
from PIL import Image
import config
from database import Database

app = Flask(__name__)
# Enable CORS for frontend access (localhost + Vercel)
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:3000",
            "https://*.vercel.app",
            "https://vercel.app"
        ],
        "methods": ["GET", "POST", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database
db = Database()


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS


def get_file_checksum(file_stream):
    """Calculate MD5 checksum of file"""
    md5 = hashlib.md5()
    file_stream.seek(0)
    for chunk in iter(lambda: file_stream.read(8192), b''):
        md5.update(chunk)
    file_stream.seek(0)
    return md5.hexdigest()


def get_file_type(mime_type):
    """Determine if file is image or video"""
    if mime_type and mime_type.startswith('image'):
        return 'image'
    elif mime_type and mime_type.startswith('video'):
        return 'video'
    return 'other'


def create_thumbnail(image_path, thumbnail_path, size=(300, 300)):
    """Create thumbnail for image"""
    try:
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            img.thumbnail(size, Image.Resampling.LANCZOS)
            img.save(thumbnail_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        return False


def get_image_dimensions(image_path):
    """Get image width and height"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except:
        return None, None


@app.route('/')
def index():
    """API information"""
    return jsonify({
        'name': 'Personal Cloud Storage API',
        'version': '1.0',
        'endpoints': {
            'POST /upload': 'Upload a file',
            'GET /files': 'List all files',
            'GET /file/<id>': 'Download file by ID',
            'GET /thumbnail/<id>': 'Get file thumbnail',
            'DELETE /file/<id>': 'Delete file by ID',
            'GET /stats': 'Get storage statistics',
            'GET /search?q=<query>': 'Search files'
        }
    })


@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Upload a file
    
    Form data:
        file: The file to upload
    
    Returns:
        JSON with file ID and metadata
    """
    # Check authentication if enabled
    if config.REQUIRE_AUTH:
        token = request.headers.get('Authorization')
        if token != f'Bearer {config.AUTH_TOKEN}':
            return jsonify({'error': 'Unauthorized'}), 401
    
    # Check if file is in request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Calculate checksum to detect duplicates
        checksum = get_file_checksum(file.stream)
        
        # Check for duplicate
        existing_file = db.get_file_by_checksum(checksum)
        if existing_file:
            return jsonify({
                'message': 'File already exists (duplicate detected)',
                'file_id': existing_file['id'],
                'duplicate': True
            }), 200
        
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{original_filename}"
        
        # Determine file path
        file_path = os.path.join(config.STORAGE_PATH, filename)
        
        # Save file
        file.save(file_path)
        file_size = os.path.getsize(file_path)
        
        # Get MIME type
        mime_type = mimetypes.guess_type(file_path)[0]
        file_type = get_file_type(mime_type)
        
        # Create thumbnail for images
        thumbnail_path = None
        width, height = None, None
        
        if file_type == 'image':
            thumbnail_filename = f"thumb_{filename}"
            thumbnail_path = os.path.join(config.THUMBNAILS_PATH, thumbnail_filename)
            if create_thumbnail(file_path, thumbnail_path):
                thumbnail_path = thumbnail_filename
            else:
                thumbnail_path = None
            
            width, height = get_image_dimensions(file_path)
        
        # Store metadata in database
        file_data = {
            'filename': filename,
            'original_filename': original_filename,
            'file_path': file_path,
            'file_size': file_size,
            'file_type': file_type,
            'mime_type': mime_type,
            'created_date': datetime.now().isoformat(),
            'thumbnail_path': thumbnail_path,
            'width': width,
            'height': height,
            'duration': None,
            'checksum': checksum
        }
        
        file_id = db.add_file(file_data)
        
        return jsonify({
            'message': 'File uploaded successfully',
            'file_id': file_id,
            'filename': original_filename,
            'size': file_size,
            'type': file_type
        }), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/files', methods=['GET'])
def list_files():
    """
    List all files with optional pagination and filtering
    
    Query params:
        limit: Max number of files to return
        offset: Number of files to skip
        type: Filter by type ('image' or 'video')
    """
    try:
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)
        file_type = request.args.get('type')
        
        files = db.get_all_files(limit=limit, offset=offset, file_type=file_type)
        
        return jsonify({
            'files': files,
            'count': len(files)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/file/<int:file_id>', methods=['GET'])
def download_file(file_id):
    """Download file by ID"""
    try:
        file_record = db.get_file_by_id(file_id)
        
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        file_path = file_record['file_path']
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found on disk'}), 404
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=file_record['original_filename']
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/thumbnail/<int:file_id>', methods=['GET'])
def get_thumbnail(file_id):
    """Get thumbnail for file"""
    try:
        file_record = db.get_file_by_id(file_id)
        
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        if not file_record['thumbnail_path']:
            return jsonify({'error': 'No thumbnail available'}), 404
        
        thumbnail_path = os.path.join(config.THUMBNAILS_PATH, file_record['thumbnail_path'])
        
        if not os.path.exists(thumbnail_path):
            return jsonify({'error': 'Thumbnail not found on disk'}), 404
        
        return send_file(thumbnail_path, mimetype='image/jpeg')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/file/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete file by ID"""
    # Check authentication if enabled
    if config.REQUIRE_AUTH:
        token = request.headers.get('Authorization')
        if token != f'Bearer {config.AUTH_TOKEN}':
            return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        file_record = db.get_file_by_id(file_id)
        
        if not file_record:
            return jsonify({'error': 'File not found'}), 404
        
        # Delete physical file
        file_path = file_record['file_path']
        if os.path.exists(file_path):
            os.remove(file_path)
        
        # Delete thumbnail if exists
        if file_record['thumbnail_path']:
            thumbnail_path = os.path.join(config.THUMBNAILS_PATH, file_record['thumbnail_path'])
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
        
        # Delete database record
        db.delete_file(file_id)
        
        return jsonify({'message': 'File deleted successfully'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get storage statistics"""
    try:
        stats = db.get_stats()
        
        # Add formatted sizes
        total_size = stats.get('total_size', 0) or 0
        stats['total_size_formatted'] = format_file_size(total_size)
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/search', methods=['GET'])
def search_files():
    """Search files by filename"""
    try:
        query = request.args.get('q', '')
        
        if not query:
            return jsonify({'error': 'Search query required'}), 400
        
        files = db.search_files(query)
        
        return jsonify({
            'files': files,
            'count': len(files)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def format_file_size(size_bytes):
    """Format bytes to human readable size"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"


if __name__ == '__main__':
    print("=" * 60)
    print("Personal Cloud Storage Server")
    print("=" * 60)
    print(f"Storage location: {config.STORAGE_PATH}")
    print(f"Server address: http://{config.HOST}:{config.PORT}")
    print(f"Authentication: {'Enabled' if config.REQUIRE_AUTH else 'Disabled'}")
    print("=" * 60)
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG
    )
