from typing import Union, Tuple
from reportlab.lib import units
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdfrw import PdfReader, PdfWriter, PageMerge
import os
from PIL import Image
from pdf2image.pdf2image import convert_from_path
from reportlab.lib.pagesizes import A4

'''

用于生成包含content文字内容的水印pdf文件

content: 水印文本内容
filename: 导出的水印文件名
width: 画布宽度，单位：mm
height: 画布高度，单位：mm
font: 对应注册的字体代号
fontsize: 字号大小
angle: 旋转角度
text_stroke_color_rgb: 文字轮廓rgb色
text_fill_color_rgb: 文字填充rgb色
text_fill_alpha: 文字透明度
'''


def create_water_mark(content: str,
                      filename: str,
                      width: Union[int, float],
                      height: Union[int, float],
                      font: str,
                      fontsize: int,
                      angle: Union[int, float] = 45,
                      text_stroke_color_rgb: Tuple[int, int, int] = (0, 0, 0),
                      text_fill_color_rgb: Tuple[int, int, int] = (0, 0, 0),
                      text_fill_alpha: Union[int, float] = 1) -> None:
    pdfmetrics.registerFont(TTFont("SimSun", "SimSun.ttf"))
    # 创建PDF文件，指定文件名及尺寸，以像素为单位
    c = canvas.Canvas(filename, pagesize=(width * units.mm, height * units.mm))
    # 画布平移保证文字完整性
    c.translate(0.1 * width * units.mm, 0.1 * height * units.mm)
    # 设置旋转角度
    c.rotate(angle)
    # 设置字体大小
    c.setFont(font, fontsize)
    # 设置字体轮廓彩色
    c.setStrokeColorRGB(*text_stroke_color_rgb)
    # 设置填充色
    c.setFillColorRGB(*text_fill_color_rgb)
    # 设置字体透明度
    c.setFillAlpha(text_fill_alpha)
    # 绘制字体内容
    c.drawString(0, 0, content)
    # 保存文件
    c.save()


def add_watermark(pdf_file, output_file, watermark, ncol, nrow):
    trailer = PdfReader(pdf_file)
    for page in trailer.pages:  # pyright: ignore[reportOptionalIterable, reportGeneralTypeIssues]
        width, height = float(page.MediaBox[2]), float(page.MediaBox[3])
        for x in range(ncol):
            for y in range(nrow):
                wmark: PageMerge = PageMerge().add(PdfReader(  # pyright: ignore[reportOptionalSubscript]
                    os.path.join(os.path.dirname(__file__), watermark)
                ).pages[0])[0]  # pyright: ignore[reportGeneralTypeIssues]
                wmark.x = width * (x) / ncol  # pyright: ignore[reportGeneralTypeIssues]
                wmark.y = height * ((x % 2) * 0.5 + y) / nrow  # pyright: ignore[reportGeneralTypeIssues]
                PageMerge(page).add(wmark, prepend=False).render()

    PdfWriter(output_file, trailer=trailer).write()


def image2pdf(input):
    # Open the image file
    img = Image.open(input)
    # If the image is in a different mode (like 'RGBA', 'L'), convert it to 'RGB'
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Use the reportlab canvas and PIL to calculate the new image size
    img_width, img_height = img.size
    aspect = img_height / float(img_width)

    # Standard dimension of A4 paper size
    pdf_width, pdf_height = A4  # (595.274, 841.890)

    # If image aspect ratio is greater than the aspect ratio of A4 paper,
    # adjust the width of img otherwise adjust the height
    if aspect > pdf_height / pdf_width:
        new_width = pdf_height / aspect
        new_height = pdf_height
    else:
        new_width = pdf_width
        new_height = pdf_width * aspect

    # Create a new canvas with the size of an A4 paper
    c = canvas.Canvas(input + '.pdf', pagesize=A4)

    # Draw image to canvas, centering the image
    c.drawImage(input, (pdf_width - new_width) / 2, (pdf_height - new_height) / 2, width=new_width, height=new_height)

    # Save the canvas as PDF
    c.save()


def image_watermark(name='Nebula Synth Lab', water='watermark_image.pdf'):
    root_dir = os.path.dirname(__file__)
    os.makedirs(os.path.join(root_dir, 'input_file'), exist_ok=True)  # 创建 output 文件夹，如果已存在则不会报错
    input_dir = os.path.join(root_dir, 'input_file')

    os.makedirs(os.path.join(root_dir, 'output_file'), exist_ok=True)  # 创建 output 文件夹，如果已存在则不会报错
    output_dir = os.path.join(root_dir, 'output_file')  # 新建文件路径指向 output 文件夹

    create_water_mark(content=name, filename=water, width=115, height=115, font='SimSun', fontsize=20,
                      text_fill_alpha=0.2)

    for _, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('jpg'):
                file_path = os.path.join(input_dir, filename)
                new_file_path = os.path.join(output_dir, filename)

                image2pdf(file_path)

                file_path += '.pdf'
                new_file_path += '.pdf'

                add_watermark(
                    file_path,
                    new_file_path,
                    water,
                    4, 5
                )

    for _, _, filenames in os.walk(output_dir):
        for filename in filenames:
            if filename.endswith('.jpg.pdf'):
                new_file_path = os.path.join(output_dir, filename)
                images = convert_from_path(new_file_path)
                for i, image in enumerate(images):
                    # 将图片保存为 png
                    image.save(new_file_path + '.jpg', 'PNG')


def trans_to_watermark_file(name, input_dir, output_dir, water='watermark.pdf', new_watermark: bool = False):
    os.makedirs(input_dir, exist_ok=True)  # 创建 output 文件夹，如果已存在则不会报错

    os.makedirs(output_dir, exist_ok=True)  # 创建 output 文件夹，如果已存在则不会报错
    if new_watermark:
        create_water_mark(content=name, filename=water, width=115, height=115, font='SimSun', fontsize=13,
                          text_fill_alpha=0.2)

    for _, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('pdf'):
                file_path = os.path.join(input_dir, filename)
                new_file_path = os.path.join(output_dir, filename)

                add_watermark(
                    file_path,
                    new_file_path,
                    water,
                    ncol=4,
                    nrow=5
                )

# if __name__ == '__main__':
#     image_watermark()
