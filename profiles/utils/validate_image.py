from PIL import Image


def validate_image(image):
    if not image.name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        return False, 'Invalid file type. This is not a image.'

    try:
        img = Image.open(image)
        img.verify()
    except Exception as e:
        return False, 'Upload error!'

    return True, ''
