from PIL import Image, ImageDraw
import numpy as np

def generate_image():
    """
    Gera uma imagem baseada em características aleatórias.
    """
    width, height = 500, 500
    img = Image.new("RGB", (width, height), "green")
    draw = ImageDraw.Draw(img)
    
    # Definir cores aleatórias baseadas em características musicais
    energy, valence, danceability = np.random.randint(0, 256, 3)
    
    for x in range(width):
        for y in range(height):
            draw.point((x, y), (energy, valence, danceability))
    
    img_path = "generated_image.png"
    img.save(img_path)
    return img_path
