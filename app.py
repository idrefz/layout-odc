import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

TEMPLATE_PATH = "template.png"  # Pastikan ukurannya 1181x1535 px (10x13 cm @ 300dpi)

def generate_qr_image(odc_name, link):
    # Load template
    template = Image.open(TEMPLATE_PATH).convert("RGBA")

    # Buat QR Code
    qr = qrcode.make(link)
    qr = qr.resize((400, 400))  # Ukuran QR Code, bisa disesuaikan

    # Tempelkan QR ke template
    qr_x = 390  # Kira-kira tengah horizontal
    qr_y = 508  # Sekitar 4.3 cm dari atas
    template.paste(qr, (qr_x, qr_y))

    # Tambahkan Nama ODC
  # Tambahkan Nama ODC (lebih besar, posisi lebih turun)
draw = ImageDraw.Draw(template)
try:
    font = ImageFont.truetype("arialbd.ttf", 140)  # Lebih besar dari sebelumnya
except:
    font = ImageFont.load_default()

text = odc_name.upper()
text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]
text_x = (template.width - text_width) // 2
text_y = 340  # Digeser ke bawah agar tidak terlalu atas

draw.text((text_x, text_y), text, font=font, fill="black")


    return template

st.title("QR Code Generator ODC - Telkom Akses")

odc_name = st.text_input("Masukkan Nama ODC", "ODC-LKG-FBQ")
link = st.text_input("Masukkan Link Akses", "https://contoh-link.com")

if st.button("Generate QR Code"):
    result_img = generate_qr_image(odc_name, link)
    st.image(result_img)

    # Simpan hasil ke buffer untuk diunduh
    buffer = io.BytesIO()
    result_img.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Download Gambar",
        data=buffer,
        file_name=f"{odc_name}.png",
        mime="image/png"
    )
