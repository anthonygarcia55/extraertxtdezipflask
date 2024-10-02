import sys
sys.stdout.reconfigure(encoding='utf-8')

from flask import Flask, render_template, request, send_from_directory, Response
from zipfile import ZipFile
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('zip_files')
        extracted_files = []
        
        for file in files:
            if file.filename.endswith('.zip'):
                zip_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(zip_path)
                
                with ZipFile(zip_path, 'r') as zip_ref:
                    for member in zip_ref.namelist():
                        if member.endswith('.txt'):
                            zip_ref.extract(member, app.config['UPLOAD_FOLDER'])
                            extracted_files.append(member)  # Agregar el archivo a la lista
                            print(f"Extraído: {member}")
                
                # Eliminar el archivo zip después de extraer los archivos
                os.remove(zip_path)

        if extracted_files:
            return render_template('index.html', message="Archivos procesados.", extracted_files=extracted_files)
        else:
            return render_template('index.html', message="No se encontraron archivos .txt en los archivos zip.")

    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)