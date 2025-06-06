
import streamlit as st
import yt_dlp

st.title("🎬 YouTube 구간 다운로드")

video_url = st.text_input("YouTube 영상 URL을 입력하세요:")
start_time = st.text_input("시작 시간 (예: 00:01:23):")
end_time = st.text_input("끝 시간 (예: 00:02:34):")

if st.button("클립 다운로드"):
    if video_url and start_time and end_time:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloaded_clip.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'download_ranges': {
                'start_time': start_time,
                'end_time': end_time,
            },
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            with open("downloaded_clip.mp4", "rb") as f:
                st.success("다운로드 완료! 아래에서 저장하세요.")
                st.download_button("클립 다운로드", f, file_name="clip.mp4")
        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.warning("모든 입력란을 채워주세요.")
