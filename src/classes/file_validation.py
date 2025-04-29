import filetype
from pdf2image import convert_from_path
from docx import Document
from PIL import Image
import imagehash
import pytesseract

class FileValidation:

    def __init__(self, templateFile, inputFile, required_keywords=[]):
        pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
        self.templateFile = templateFile
        self.inputFile = inputFile
        self.required_keywords = required_keywords

    @staticmethod
    def __docx_to_image(docx_path):
        doc = Document(docx_path)
        text = '\n'.join(p.text for p in doc.paragraphs)
        img = Image.new('RGB', (1200, 1600), color='white')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), text, fill='black')
        return [img]

    def __detect_file_type(self, filepath):
        kind = filetype.guess(filepath)
        if filepath.lower().endswith('.pdf'):
            return 'pdf'
        elif filepath.lower().endswith('.docx'):
            return 'docx'
        elif kind and kind.mime.startswith('image'):
            return 'image'
        return None

    def __convert_to_images(self, path):
        filetype_detected = self.__detect_file_type(path)
        poppler_path = r"C:\Users\water\OneDrive\Documents\poppler-24.08.0\Library\bin"

        if filetype_detected == 'pdf':
            return convert_from_path(path, poppler_path=poppler_path)
        elif filetype_detected == 'docx':
            return self.__docx_to_image(path)
        elif filetype_detected == 'image':
            return [Image.open(path)]
        else:
            raise ValueError("Unsupported file format")
        
    def __compare_documents(self, templateFile_path, user_path, hash_threshold=5):
        templateFile_imgs = self.__convert_to_images(templateFile_path)
        user_imgs = self.__convert_to_images(user_path)

        for i in range(min(len(templateFile_imgs), len(user_imgs))):
            templateFile_hash = imagehash.average_hash(templateFile_imgs[i])
            user_hash = imagehash.average_hash(user_imgs[i])
            diff = abs(templateFile_hash - user_hash)
            print(f"[Page {i+1}] Hash difference: {diff}")
            if diff > hash_threshold:
                return False
        return True

    @staticmethod
    def __contains_required_text(image, required_keywords):
        text = pytesseract.image_to_string(image)
        return all(keyword.lower() in text.lower() for keyword in required_keywords)
    
    def is_valid(self) -> int:
        try:
            if self.__compare_documents(self.templateFile, self.inputFile):
                user_images = self.__convert_to_images(self.inputFile)
                return 1 if self.__contains_required_text(user_images[0], self.required_keywords) else 0
            else:
                return -1
        except Exception as e:
            raise e