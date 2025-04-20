import streamlit as st
from PIL import Image
import io
import os

import zipfile

from localtinyimg.process.tiny_image import *

def readable_size(size_in_bytes):
    for unit in ['B', 'KB', 'MB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f}{unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f}GB"

st.title("本地端 圖片壓縮與尺寸縮放 工具")

uploaded_files = st.file_uploader("上傳圖片 (可多選)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

quality = st.slider("JPG 壓縮品質 (數值越低檔案越小)", 10, 95, 80)
scale_percent = st.slider("縮放比例 (%)", 10, 100, 100)

if uploaded_files:
    zip_buffer = io.BytesIO()
    progress_bar = st.progress(0)
    total_files = len(uploaded_files)

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for idx, uploaded_file in enumerate(uploaded_files):
            ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
            original_size = uploaded_file.size

            if ext in ["jpg", "jpeg"]:
                compressed_img = compress_jpg(uploaded_file, quality=quality, scale_percent=scale_percent)
                file_name = uploaded_file.name.rsplit(".", 1)[0] + "_compressed.jpg"
            elif ext == "png":
                compressed_img = compress_png(uploaded_file, scale_percent=scale_percent)
                file_name = uploaded_file.name.rsplit(".", 1)[0] + "_compressed.png"
            else:
                st.warning(f"不支援的格式：{uploaded_file.name}")
                continue

            compressed_size = len(compressed_img.getvalue())

            # 顯示原始與壓縮後大小
            st.write(f"📷 {uploaded_file.name}")
            st.write(f"原始大小：{readable_size(original_size)} → 壓縮後大小：{readable_size(compressed_size)}")

            # 加入到zip
            zip_file.writestr(file_name, compressed_img.read())

            progress_bar.progress((idx + 1) / total_files)

    zip_buffer.seek(0)
    st.success(f"✅ 壓縮完成！共處理 {total_files} 張圖片。")
    st.download_button(
        label="下載所有壓縮後的圖片 (ZIP)",
        data=zip_buffer,
        file_name="compressed_images.zip",
        mime="application/zip"
    )
