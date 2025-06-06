import streamlit as st
import yt_dlp
import subprocess
import os

st.title("🎬 유튜브 구간 다운로드")

video_url = st.text_input("YouTube 영상 URL:")
start_time = st.text_input("시작 시간 (예: 00:01:00):")
end_time = st.text_input("끝 시간 (예: 00:01:20):")

if st.button("구간 다운로드"):
    if not video_url or not start_time or not end_time:
        st.warning("모든 입력란을 채워주세요.")
    else:
        try:
            # Step 1: 전체 영상 다운로드
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'full_video.%(ext)s',
                'merge_output_format': 'mp4'
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            # Step 2: ffmpeg로 구간 자르기
            input_file = "full_video.mp4"
            output_file = "clip.mp4"

            command = [
                "ffmpeg", "-y",
                "-i", input_file,
                "-ss", start_time,
                "-to", end_time,
                "-c", "copy",
                output_file
            ]

            subprocess.run(command, check=True)

            # Step 3: 다운로드 링크 제공
            with open(output_file, "rb") as f:
                st.success("✅ 구간 클립 생성 완료!")
                st.download_button("📥 다운로드", f, file_name="clip.mp4")

        except Exception as e:
            st.error(f"오류 발생: {e}")
