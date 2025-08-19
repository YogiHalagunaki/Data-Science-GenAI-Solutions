import streamlit as st

def create_header(heading):
    # Custom CSS for the header
    st.markdown("""
    <style>
    .header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 5px 10px;
        background-color: black;
        color: white;
        margin-top: -60px;
        margin-left: -20px;
        margin-right: -20px;
    }
    .header-left, .header-center, .header-right {
        display: flex;
        align-items: center;
    }
    .header-right {
        gap: 20px;
    }
    .header-item {
        display: flex;
        align-items: center;
        gap: 5px;
    }
    .user-info {
        text-align: right;
        font-size: 16px;
    }
    .user-avatar {
        background-color: #3498db;
        color: white;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        font-size: 18px;
    }
    .banner {
        padding: 5px 10px;
        margin-right: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

     # Header content
    st.markdown(f"""
    <div class="header">
        <div class="header-left">
            <img src="data:image/png;base64,{get_image_base64("Images/bot.png")}" alt="BOT" width="180">
        </div>
        <div class="header-center">
            <h1 style="color: white; font-size: 34px; margin: 0;">{heading}</h1>
        </div>
        <div class="header-right">
            <div class="banner">
                <img src="data:image/png;base64,{get_image_base64("Images/preview.PNG")}" alt="BOT1" width="140">
            </div>
            <div class="user-info">
                <div>Yogi Halagunaki</div>
                <div>Data Scientist</div>
            </div>
            <div class="header-item user-avatar">YH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_image_base64(image_path):
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

