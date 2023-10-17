from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import pytesseract
from PIL import Image
import tempfile 
import io

app = FastAPI()

@app.post('/image-to-text')
def ocr(image: UploadFile = File(...)):
    filePath='textFile'
    with open(filePath, 'w+b') as buffer:
        shutil.copyfileobj(image.file, buffer)
    return pytesseract.image_to_string(filePath, lang='eng')

@app.post('/image-to-pdf')
async def ocr(image: UploadFile = File(...)):
    image_contents = await image.read()
    pil_image = Image.open(io.BytesIO(image_contents))
    text = pytesseract.image_to_string(pil_image)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(text.encode('utf-8'))
        temp_file_path = temp_file.name
    response = FileResponse(temp_file_path, media_type='application/pdf')
    response.headers['Content-Disposition'] = 'attachment; filename="ocr_result.pdf"'
    
    return response