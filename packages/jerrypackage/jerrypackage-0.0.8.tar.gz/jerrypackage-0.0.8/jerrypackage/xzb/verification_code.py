from .xzb_api import logger

def file_path_verification_code_reader(path):
    def reader(image):
        with open(path, 'wb') as output:
            output.write(image)
        print('Verification code picture is saved to %s, please open it manually and enter what you see.' % path)
        code = input('Verification code: ')
        return code
    return reader

# def tesseract_verification_code_reader(image_data):
#     from PIL import Image
#
#     import pytesseract
#     import io
#
#     with open('./vcode.jpg', 'wb') as output:
#         output.write(image_data)
#
#     image = Image.open(io.BytesIO(image_data))
#     vcode = pytesseract.image_to_string(image)
#     logger.info("vcode:", vcode)
#     return vcode

def default_verification_code_reader(reader_type, vcode_image_path):
    # if reader_type == 'tesseract':
    #     return tesseract_verification_code_reader

    if not vcode_image_path:
        vcode_image_path = './vcode.jpg'
    return file_path_verification_code_reader(vcode_image_path)

