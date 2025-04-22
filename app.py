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
    draw = ImageDraw.Draw(template)
    try:
        font = ImageFont.truetype("arialbd.ttf", 87)  # 21.1 pt ≈ 87 px
    except:
        font = ImageFont.load_default()

    # Posisi teks ODC di sekitar 2.5 cm dari atas
    text = odc_name.upper()
    text_x = 390  # Sesuaikan supaya rata tengah QR
    text_y = 295
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
