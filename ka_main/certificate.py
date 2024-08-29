from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files import File
from .models import Cert

def create_cretificate(name,course_name,d,id,tn,tp):
    image = Image.open("cert_template.png")
    draw = ImageDraw.Draw(image)

    consolas_font = ImageFont.truetype("consolab.ttf",size=200)
    LiAdor_semibold = ImageFont.truetype("liador_semibold.ttf",size=130)
    LiAdor_semibold_tn = ImageFont.truetype("liador_semibold.ttf",size=90)
    LiAdor_regular = ImageFont.truetype("liador_regular.ttf",size=80)
    LiAdor_light = ImageFont.truetype("liador_light.ttf",size=100)

    name_position = (1350,1120)
    course_name_position = (1200,1425)
    date_position = (1800,1560)
    id_position = (780,1870)
    tn_position = (1700,2000)
    tp_position = (1875,2090)

    draw.text(name_position,name,fill="black",font=consolas_font)
    draw.text(course_name_position,course_name,fill="black",font=LiAdor_semibold)
    draw.text(date_position,d,fill="black",font=LiAdor_light)
    draw.text(id_position,id,fill="black",font=LiAdor_regular)
    draw.text(tn_position,tn,fill="black",font=LiAdor_semibold_tn)
    draw.text(tp_position,tp,fill="black",font=LiAdor_regular)

    image_io = BytesIO()
    image.save(image_io,format="PNG")
    image_io.seek()

    certificate = Cert(id=id,name=name,d=d,course_name=course_name)
    certificate.image.save(f'{id}.png',File(image_io))
    certificate.save()

    return "Success"