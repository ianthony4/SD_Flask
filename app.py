import os
from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps
import imghdr

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB
app.config['UPLOAD_FOLDER_ORIGINAL'] = 'uploads/default'
app.config['UPLOAD_FOLDER_BORDES'] = 'uploads/border'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'bmp'}

# Crear directorios si no existen
# ---------(PRIMERA EXCEPCION DE CONTROL)
os.makedirs(app.config['UPLOAD_FOLDER_ORIGINAL'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_BORDES'], exist_ok=True)
# --------- 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')
# ------------------Agregar Bordes
# Tambien cuenta con control de excepción
def agregar_bordes(imagen_path, output_path, border_size=15, border_color='orange'):
    try:
        with Image.open(imagen_path) as img:
            # Convertir a RGB si es necesario (para BMP)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Agregar bordes
            bordered = ImageOps.expand(
                img, 
                border=border_size, 
                fill=border_color
            )
            bordered.save(output_path)
            return True
    except Exception as e:
        # Indicara el nombre del error
        print(f"Error procesando imagen: {e}")
        return False

@app.route('/')
def index():
    originales = os.listdir(app.config['UPLOAD_FOLDER_ORIGINAL'])
    bordes = os.listdir(app.config['UPLOAD_FOLDER_BORDES'])
    return render_template('index.html', 
                         originales=originales, 
                         bordes=bordes)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No hay parte del Archivo!!!'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Archivo NO Seleccionado!!!'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_path = os.path.join(app.config['UPLOAD_FOLDER_ORIGINAL'], filename)
            bordered_path = os.path.join(app.config['UPLOAD_FOLDER_BORDES'], filename)
            
            # Guardar original
            file.save(original_path)
            
            # Procesar y guardar con bordes
            if not agregar_bordes(original_path, bordered_path):
                return jsonify({'error': 'Error Procesando la Imagen'}), 500
            
            return jsonify({
                'original': filename,
                'bordered': filename
            }), 200
        else:
            return jsonify({'error': 'Tipo de Archivo no Permitido!!!!'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/default/<filename>')
def serve_original(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_ORIGINAL'], filename)

@app.route('/uploads/border/<filename>')
def serve_bordered(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER_BORDES'], filename)

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'Archivo Demasiado Grande (Maximo 2MB)'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
