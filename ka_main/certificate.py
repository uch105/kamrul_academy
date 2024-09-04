from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.core.files import File
from .models import Cert

def create_cretificate(name,course_name,d,id,tn,tp):
    image = Image.open("ka_main/cert_template.png")
    draw = ImageDraw.Draw(image)

    consolas_font = ImageFont.truetype("ka_main/consolab.ttf",size=200)
    LiAdor_semibold = ImageFont.truetype("ka_main/liador_semibold.ttf",size=130)
    LiAdor_semibold_tn = ImageFont.truetype("ka_main/liador_semibold.ttf",size=90)
    LiAdor_regular = ImageFont.truetype("ka_main/liador_regular.ttf",size=80)
    LiAdor_light = ImageFont.truetype("ka_main/liador_light.ttf",size=100)

    image_width , image_height = image.size
    name_width = draw.textlength(name,font=consolas_font)
    course_name_width = draw.textlength(course_name,font=LiAdor_semibold)
    tn_width = draw.textlength(tn,font=LiAdor_semibold_tn)
    tp_width = draw.textlength(tp,font=LiAdor_regular)

    name_position = ((image_width - name_width)//2,1120)
    course_name_position = ((image_width - course_name_width)//2,1425)
    date_position = (1800,1560)
    id_position = (780,1870)
    tn_position = ((image_width - tn_width)//2,2000)
    tp_position = ((image_width - tp_width)//2,2090)

    draw.text(name_position,name,fill="black",font=consolas_font)
    draw.text(course_name_position,course_name,fill="black",font=LiAdor_semibold)
    draw.text(date_position,d,fill="black",font=LiAdor_light)
    draw.text(id_position,id,fill="black",font=LiAdor_regular)
    draw.text(tn_position,tn,fill="black",font=LiAdor_semibold_tn)
    draw.text(tp_position,tp,fill="black",font=LiAdor_regular)

    image_io = BytesIO()
    image.save(image_io,format="PNG")
    image_io.seek(0)

    try:
        certificate = Cert(id=id,name=name,d=d,course_name=course_name)
        certificate.image.save(f'{id}.png',File(image_io))
        certificate.save()

        return "Success"
    except:
        return "Failed"