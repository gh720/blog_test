import lightning_logo as ll
import numpy
from PIL import Image
from blend_modes import blend_modes

image1 = ll.generate_lightning_image((256,256))
image2 = ll.load_image('../aux_resources/logo_letters.png')
image = blend_modes.addition(ll.image_to_blend(image1), ll.image_to_blend(image2), opacity=1)
ll.save_image(ll.image_from_blend(image))
