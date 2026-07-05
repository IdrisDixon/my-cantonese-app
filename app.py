import os
import streamlit as st

# 1. 页面基本配置：宽屏、隐藏侧边栏
st.set_page_config(page_title="粤语香港话自学助手", layout="wide", initial_sidebar_state="collapsed")

# 优化边距
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 1rem; padding-left: 2rem; padding-right: 2rem; }
    iframe { border: none; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    </style>
""", unsafe_allow_html=True)

# 2. 【完整书籍目录数据配置】
# 根据目录截图完美还原：课程名 -> {chapter_num: 用于匹配音频的数字, page: PDF页码}
CHAPTER_DATA = {
    # --- 上编 ---
    "01 介绍 Gai3xiu6": {"chapter_num": 1, "page": 2},
    "02 問候 Men6heo6": {"chapter_num": 2, "page": 13},
    "03 打電話 Da2 din6wa2": {"chapter_num": 3, "page": 26},
    "04 約會 Yeg3wui6": {"chapter_num": 4, "page": 39},
    "05 問路 Men6lou6": {"chapter_num": 5, "page": 54},
    "06 購物 Geo3med6": {"chapter_num": 6, "page": 67},
    "07 交通 Gao1tung1": {"chapter_num": 7, "page": 80},
    "08 天氣 Tin1hei3": {"chapter_num": 8, "page": 92},
    "09 飲食 Yem2xig6": {"chapter_num": 9, "page": 103},
    "10 香港 Heng1gong2": {"chapter_num": 10, "page": 114},
    # --- 中编 ---
    "11 開戶口 Hoi1 wu6heo2": {"chapter_num": 11, "page": 128},
    "12 買餸 Mai5sung3": {"chapter_num": 12, "page": 139},
    "13 外出旅遊 Ngoi6cêd1 lâu5yeo4": {"chapter_num": 13, "page": 150},
    "14 睇醫生 Tei2 yi1seng1": {"chapter_num": 14, "page": 161},
    "15 清潔香港 Qing1gid3 Hêng1gong2": {"chapter_num": 15, "page": 173},
    "16 搵學校 Wen2 hog6hao6": {"chapter_num": 16, "page": 184},
    "17 晨運 Sen4wen6": {"chapter_num": 17, "page": 196},
    "18 搵工跳槽 Wen2gung1 tiu3cou4": {"chapter_num": 18, "page": 209},
    "19 打“九九九” Da2 “geo2-geo2-geo2”": {"chapter_num": 19, "page": 222},
    "20 香港話 Hêng1gong2wa2": {"chapter_num": 20, "page": 235},
    # --- 下编 ---
    "21 報紙 Bou3ji2": {"chapter_num": 21, "page": 252},
    "22 交通運輸 Gao1tung1 wen6xu1": {"chapter_num": 22, "page": 264},
    "23 海洋公園 Hoi2yêng4 gung1yun2": {"chapter_num": 23, "page": 276},
    "24 黃大仙 Wong4dai6xin1": {"chapter_num": 24, "page": 288},
    "25 電視文化 Din6xi6 men4fa3": {"chapter_num": 25, "page": 299},
    "26 食在香港 Xig6 zoi6 Hêng1gong2": {"chapter_num": 26, "page": 311},
    "27 “女人街” “Nêu5yen2gai1”": {"chapter_num": 27, "page": 323},
    "28 “居者有其屋” “Gêu1zé2 yeo5 kéi4 ug1”": {"chapter_num": 28, "page": 335},
    "29 貪字變貧字 Tam1 ji6 bin3 pen4 ji6": {"chapter_num": 29, "page": 346},
    "30 話說移民 Wa6xud3 yi4men4": {"chapter_num": 30, "page": 358},
    # --- 附录 ---
    "附录一：常見姓氏粵語音節表": {"chapter_num": "附录1", "page": 372},
    "附录二：粵語多音字舉例": {"chapter_num": "附录2", "page": 373},
    "附录三：本書練習答案": {"chapter_num": "附录3", "page": 374},
    "附录四：本書詞彙音序索引": {"chapter_num": "附录4", "page": 378},
}

st.title("粤语（香港话）多媒体阅读器～")
st.write("---")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🗂️ 章节目录")
    selected_chapter = st.selectbox("选择你要学习的课文：", list(CHAPTER_DATA.keys()))
    
    current_info = CHAPTER_DATA[selected_chapter]
    target_page = current_info["page"]
    ch_num = current_info["chapter_num"]
    
    st.write("")
    st.markdown(f"📍 本课起始页：第 **{target_page}** 页")
    st.write("")
    
    st.subheader("🎵 课文音频")
    
    audio_dir = "audio"
    available_audios = []
    
    if os.path.exists(audio_dir):
        # 精准匹配不带前导 0 的文件名。例如：ch_num 为 1 时匹配 1-1.mp3，不匹配 01-1.mp3
        available_audios = [
            f for f in os.listdir(audio_dir) 
            if f.startswith(f"{ch_num}-") and f.lower().endswith(".mp3")
        ]
        # 对文件名数字排序（如 1-1, 1-2）
        available_audios.sort()

    if available_audios:
        if len(available_audios) > 1:
            selected_audio = st.selectbox("选择音频片段：", available_audios)
        else:
            selected_audio = available_audios[0]
            st.caption(f"正在播放：{selected_audio}")
            
        audio_path = os.path.join(audio_dir, selected_audio)
        try:
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")
        except Exception as e:
            st.error(f"音频读取失败: {e}")
    else:
        st.warning(f"⚠️ 未找到以 `{ch_num}-` 开头的音频文件")
        
    st.write("---")
    st.text_area("📝 随堂笔记：", height=200, placeholder="在此输入你的粤语拼音或笔记...")

with col2:
    st.subheader("📖 PDF 课本正文")
    
    # 1. 你的纯英文 PDF 绝对路径
    pdf_url = f"https://huaaan.streamlit.app/static/cantonese_book.pdf"
    
    # 2. 借用 Mozilla 官方的公共 PDF.js 预览流，并把页码传过去
    # pdf.js 会把 PDF 极其丝滑地在云端解析好吐给 iPad，瞬间秒开不转圈！
    pdf_js_viewer = f"https://mozilla.github.io/pdf.js/web/viewer.html?file={pdf_url}#page={target_page}"
    
    # 3. 渲染内嵌框
    pdf_display = f'<iframe src="{pdf_js_viewer}" width="100%" height="900px" style="border:none; border-radius:8px;"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
