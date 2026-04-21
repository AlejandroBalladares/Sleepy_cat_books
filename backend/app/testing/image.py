from random import randint, random
def image_url() -> str:
  width_image = 80 * randint(1, 10) # 80 - 800 px
  height_image = int(width_image * (random() + 1)) # 80 - 1600 px
  imagen_url = "https://picsum.photos/id/" + str(randint(1, 1000)) + "/" + str(width_image) + "/" + str(height_image)
  return imagen_url