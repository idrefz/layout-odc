
import streamlit as st
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io

TEMPLATE_PATH = "template.png"

def generate_qr_image(odc_name, link):
    # Load template
    template = Image.open(TEMPLATE_PATH).convert("RGBA")

    # Buat QR Code
    qr = qrcode.make(link)
    qr = qr.resize((400, 400))  # Ukuran QR Code, bisa disesuaikan

    # Tempelkan QR ke template
    template.paste(qr, (150, 300))  # Koordinat QR di gambar, sesuaikan

    # Tambahkan Nama ODC
    draw = ImageDraw.Draw(template)
    try:
        font = ImageFont.truetype("arialbd.ttf", 60)  # Pastikan font ini ada
    except:
        font = ImageFont.load_default()
    draw.text((150, 220), odc_name, font=font, fill="black")

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
