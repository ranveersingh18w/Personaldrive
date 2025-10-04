# Personal Cloud Storage - API Documentation

## Base URL
```
http://localhost:5000
```

---

## Endpoints

### 1. Get API Information
**GET** `/`

Returns API information and available endpoints.

**Response:**
```json
{
  "name": "Personal Cloud Storage API",
  "version": "1.0",
  "endpoints": {
    "POST /upload": "Upload a file",
    "GET /files": "List all files",
    "GET /file/<id>": "Download file by ID",
    "GET /thumbnail/<id>": "Get file thumbnail",
    "DELETE /file/<id>": "Delete file by ID",
    "GET /stats": "Get storage statistics",
    "GET /search?q=<query>": "Search files"
  }
}
```

---

### 2. Upload File
**POST** `/upload`

Upload a photo or video file.

**Headers:**
```
Content-Type: multipart/form-data
Authorization: Bearer <token>  (if auth is enabled)
```

**Body:**
```
file: <binary file data>
```

**Response (Success):**
```json
{
  "message": "File uploaded successfully",
  "file_id": 123,
  "filename": "vacation.jpg",
  "size": 2048576,
  "type": "image"
}
```

**Response (Duplicate):**
```json
{
  "message": "File already exists (duplicate detected)",
  "file_id": 45,
  "duplicate": true
}
```

**Example (curl):**
```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@/path/to/photo.jpg"
```

**Example (Python):**
```python
import requests

with open('photo.jpg', 'rb') as f:
    files = {'file': ('photo.jpg', f)}
    response = requests.post('http://localhost:5000/upload', files=files)
    print(response.json())
```

---

### 3. List Files
**GET** `/files`

Get list of all uploaded files with metadata.

**Query Parameters:**
- `limit` (int, optional): Maximum number of files to return
- `offset` (int, optional): Number of files to skip (for pagination)
- `type` (string, optional): Filter by type ('image' or 'video')

**Response:**
```json
{
  "files": [
    {
      "id": 1,
      "filename": "20250104_123456_photo.jpg",
      "original_filename": "photo.jpg",
      "file_path": "C:\\Users\\...\\photo.jpg",
      "file_size": 2048576,
      "file_type": "image",
      "mime_type": "image/jpeg",
      "upload_date": "2025-10-04T12:34:56",
      "created_date": "2025-10-04T12:34:56",
      "thumbnail_path": "thumb_20250104_123456_photo.jpg",
      "width": 1920,
      "height": 1080,
      "duration": null,
      "checksum": "abc123def456..."
    }
  ],
  "count": 1
}
```

**Examples:**
```bash
# Get all files
curl http://localhost:5000/files

# Get only images
curl http://localhost:5000/files?type=image

# Get first 10 files
curl http://localhost:5000/files?limit=10

# Pagination (skip first 10, get next 10)
curl http://localhost:5000/files?limit=10&offset=10
```

---

### 4. Download File
**GET** `/file/<id>`

Download a file by its ID.

**Parameters:**
- `id` (int): File ID

**Response:**
- Binary file data with appropriate headers

**Example:**
```bash
# Download file with ID 123
curl -O http://localhost:5000/file/123
```

**JavaScript:**
```javascript
async function downloadFile(fileId) {
  const response = await fetch(`http://localhost:5000/file/${fileId}`);
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'file.jpg';
  a.click();
}
```

---

### 5. Get Thumbnail
**GET** `/thumbnail/<id>`

Get thumbnail image for a file (images only).

**Parameters:**
- `id` (int): File ID

**Response:**
- JPEG image (300x300 max)

**Example:**
```html
<img src="http://localhost:5000/thumbnail/123" alt="Thumbnail" />
```

---

### 6. Delete File
**DELETE** `/file/<id>`

Delete a file and its metadata.

**Headers:**
```
Authorization: Bearer <token>  (if auth is enabled)
```

**Parameters:**
- `id` (int): File ID

**Response:**
```json
{
  "message": "File deleted successfully"
}
```

**Example:**
```bash
curl -X DELETE http://localhost:5000/file/123
```

**JavaScript:**
```javascript
async function deleteFile(fileId) {
  const response = await fetch(`http://localhost:5000/file/${fileId}`, {
    method: 'DELETE'
  });
  const result = await response.json();
  console.log(result.message);
}
```

---

### 7. Get Statistics
**GET** `/stats`

Get storage statistics.

**Response:**
```json
{
  "total_files": 150,
  "total_size": 5242880000,
  "total_size_formatted": "4.88 GB",
  "image_count": 120,
  "video_count": 30
}
```

**Example:**
```bash
curl http://localhost:5000/stats
```

---

### 8. Search Files
**GET** `/search`

Search files by filename.

**Query Parameters:**
- `q` (string, required): Search query

**Response:**
```json
{
  "files": [
    {
      "id": 5,
      "original_filename": "vacation_beach.jpg",
      ...
    }
  ],
  "count": 1
}
```

**Example:**
```bash
# Search for files containing "vacation"
curl "http://localhost:5000/search?q=vacation"
```

---

## Error Responses

All error responses follow this format:

```json
{
  "error": "Description of the error"
}
```

**Common HTTP Status Codes:**
- `200` - Success
- `201` - Created (file uploaded)
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (invalid or missing auth token)
- `404` - Not Found (file doesn't exist)
- `500` - Internal Server Error

---

## Authentication

If authentication is enabled (`REQUIRE_AUTH = True` in config):

**Header:**
```
Authorization: Bearer your-secret-token-here
```

**Example:**
```bash
curl -X POST http://localhost:5000/upload \
  -H "Authorization: Bearer your-secret-token" \
  -F "file=@photo.jpg"
```

**Python:**
```python
headers = {'Authorization': 'Bearer your-secret-token'}
response = requests.post(url, files=files, headers=headers)
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production use, consider adding:
- Flask-Limiter for rate limiting
- Maximum file size enforcement (default: 500MB)
- Maximum concurrent uploads

---

## CORS

CORS is enabled for all origins by default. To restrict:

```python
# In app.py
CORS(app, origins=['http://localhost:3000'])
```

---

## WebSocket Support (Future)

For real-time upload progress, consider implementing WebSocket support:

```javascript
const ws = new WebSocket('ws://localhost:5000/ws');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Upload progress:', data.progress);
};
```

---

## Best Practices

1. **Always check file size before uploading**
2. **Use checksum for duplicate detection** (automatic)
3. **Handle errors gracefully**
4. **Use pagination for large file lists**
5. **Cache thumbnail responses**
6. **Compress images before upload if possible**

---

## Integration Examples

### React/JavaScript
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:5000';

// Upload file
const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await axios.post(`${API_URL}/upload`, formData, {
    onUploadProgress: (progressEvent) => {
      const progress = (progressEvent.loaded / progressEvent.total) * 100;
      console.log(`Upload progress: ${progress}%`);
    }
  });
  
  return response.data;
};

// Get files
const getFiles = async () => {
  const response = await axios.get(`${API_URL}/files`);
  return response.data.files;
};
```

### Python Client
```python
import requests

API_URL = 'http://localhost:5000'

def upload_file(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f)}
        response = requests.post(f'{API_URL}/upload', files=files)
        return response.json()

def get_files():
    response = requests.get(f'{API_URL}/files')
    return response.json()['files']
```

### Mobile (Flutter)
```dart
import 'package:http/http.dart' as http;

Future<void> uploadFile(File file) async {
  var request = http.MultipartRequest(
    'POST',
    Uri.parse('http://192.168.1.100:5000/upload')
  );
  
  request.files.add(await http.MultipartFile.fromPath('file', file.path));
  
  var response = await request.send();
  var responseData = await response.stream.toBytes();
  var responseString = String.fromCharCodes(responseData);
  
  print(responseString);
}
```

---

## Testing

Use tools like:
- **Postman** - GUI for testing API endpoints
- **curl** - Command-line testing
- **pytest** - Automated testing

Example test:
```python
def test_upload():
    response = requests.post('http://localhost:5000/upload', 
                           files={'file': open('test.jpg', 'rb')})
    assert response.status_code == 201
    assert 'file_id' in response.json()
```
