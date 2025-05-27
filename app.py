# from flask import Flask, request, render_template, jsonify
# from pdf2image import convert_from_path
# import pytesseract
# import os
# from werkzeug.utils import secure_filename

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"})
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"})
#     filename = secure_filename(file.filename)
#     filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     file.save(filepath)

#     images = convert_from_path(filepath, dpi=300)
#     full_text = ""
#     for img in images:
#         text = pytesseract.image_to_string(img, lang='hin')
#         full_text += text + " "
#     word_count = len(full_text.split())
#     os.remove(filepath)
#     return jsonify({"word_count": word_count})

# if __name__ == '__main__':
#     app.run(debug=True)


# import os
# from flask import Flask, render_template, request, jsonify
# from pdf2image import convert_from_path
# import pytesseract

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         file = request.files['file']
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)

#         images = convert_from_path(filepath, dpi=300)
#         total_text = ''
#         for img in images:
#             total_text += pytesseract.image_to_string(img, lang='hin+eng')

#         word_count = len(total_text.split())

#         return jsonify({"success": True, "word_count": word_count})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)


# import os
# from flask import Flask, render_template, request, jsonify
# from pdf2image import convert_from_path
# import pytesseract

# app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     try:
#         file = request.files['file']
#         is_hindi = request.args.get('hindi', 'true').lower() == 'true'

#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
#         file.save(filepath)

#         # Convert PDF to images
#         images = convert_from_path(filepath, dpi=300)

#         # OCR each image
#         total_text = ''
#         lang_code = 'hin' if is_hindi else 'eng'

#         for img in images:
#             total_text += pytesseract.image_to_string(img, lang=lang_code)

#         # Count words
#         word_count = len(total_text.split())

#         return jsonify({"success": True, "word_count": word_count})

#     except Exception as e:
#         return jsonify({"success": False, "error": str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)


import os
from flask import Flask, render_template, request, jsonify
from pdf2image import convert_from_path
import pytesseract
import fitz  # PyMuPDF

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        is_hindi = request.args.get('hindi', 'true').lower() == 'true'

        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        if is_hindi:
            # Use OCR for scanned Hindi PDFs
            images = convert_from_path(filepath, dpi=300)
            total_text = ''
            for img in images:
                total_text += pytesseract.image_to_string(img, lang='hin')
        else:
            # Use direct text extraction for English PDFs
            total_text = ''
            with fitz.open(filepath) as doc:
                for page in doc:
                    total_text += page.get_text()

        word_count = len(total_text.split())

        return jsonify({"success": True, "word_count": word_count})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
