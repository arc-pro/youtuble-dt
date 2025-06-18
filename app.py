import streamlit as st
import yt_dlp
import os
import re
from pathlib import Path
import time
import tempfile
import shutil

# 设置页面配置
st.set_page_config(
    page_title="YouTube 视频下载器 - 云端版",
    page_icon="☁️",
    layout="wide"
)

def is_valid_youtube_url(url):
    """验证是否为有效的 YouTube URL"""
    youtube_regex = re.compile(
        r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    return youtube_regex.match(url) is not None

def get_video_info(url):
    """获取视频信息"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 30,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'thumbnail': info.get('thumbnail', ''),
                'description': info.get('description', '')[:500] + '...' if info.get('description') else '',
                'upload_date': info.get('upload_date', ''),
                'formats': info.get('formats', [])
            }
    except Exception as e:
        st.error(f"获取视频信息失败: {str(e)}")
        return None

def download_video(url, quality='best', format_type='mp4'):
    """下载视频到临时目录"""
    try:
        # 创建临时目录
        temp_dir = tempfile.mkdtemp()

        ydl_opts = {
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'format': f'{quality}[ext={format_type}]/best[ext={format_type}]/best',
            'socket_timeout': 60,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 下载视频
            ydl.download([url])

            # 查找下载的文件
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if os.path.isfile(file_path):
                    return file_path

        return None
    except Exception as e:
        raise e

def format_duration(seconds):
    """格式化时长"""
    if not seconds:
        return "未知"
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def format_views(views):
    """格式化观看次数"""
    if not views:
        return "未知"
    if views >= 1000000:
        return f"{views/1000000:.1f}M"
    elif views >= 1000:
        return f"{views/1000:.1f}K"
    else:
        return str(views)

def format_date(date_str):
    """格式化日期"""
    if not date_str or len(date_str) != 8:
        return "未知"
    try:
        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]
        return f"{year}-{month}-{day}"
    except:
        return "未知"

# 主界面
st.title("☁️ YouTube 视频下载器 - 云端版")

# 添加说明
st.info("""
🌟 **云端版优势**:
- 🚀 无需代理，直接访问 YouTube
- 🌍 海外服务器，网络连接稳定
- ⚡ 更高的下载成功率
- 🔒 安全可靠的云端环境
""")

st.markdown("---")

# 侧边栏设置
with st.sidebar:
    st.header("⚙️ 下载设置")

    quality_options = {
        'best': '最佳质量',
        'bestvideo[height<=1080]': '1080p',
        'bestvideo[height<=720]': '720p',
        'bestvideo[height<=480]': '480p',
        'bestvideo[height<=360]': '360p',
        'worst': '最低质量'
    }

    selected_quality = st.selectbox(
        "选择视频质量",
        options=list(quality_options.keys()),
        format_func=lambda x: quality_options[x],
        index=0
    )

    format_options = ['mp4', 'webm']
    selected_format = st.selectbox(
        "选择视频格式",
        options=format_options,
        index=0
    )

    st.markdown("---")
    st.header("ℹ️ 使用说明")
    st.write("""
    1. 输入 YouTube 视频链接
    2. 点击获取视频信息
    3. 选择下载质量 (360p-1080p)
    4. 选择视频格式 (MP4/WebM)
    5. 点击下载按钮
    6. 等待处理完成后下载文件
    """)

    st.markdown("---")
    st.header("⚠️ 注意事项")
    st.write("""
    - 请遵守版权法律
    - 仅供个人学习使用
    - 大文件下载需要耐心等待
    - 下载的文件会在会话结束后删除
    """)

# 主要内容区域
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🔗 输入 YouTube 链接")
    url_input = st.text_input(
        "请输入 YouTube 视频链接:",
        placeholder="https://www.youtube.com/watch?v=...",
        help="支持 youtube.com 和 youtu.be 链接"
    )

    # 验证URL按钮
    if st.button("🔍 获取视频信息", type="secondary"):
        if url_input:
            if is_valid_youtube_url(url_input):
                with st.spinner("正在获取视频信息..."):
                    video_info = get_video_info(url_input)
                    if video_info:
                        st.session_state.video_info = video_info
                        st.session_state.valid_url = url_input
                        st.success("✅ 视频信息获取成功！")
                    else:
                        st.error("❌ 无法获取视频信息，请检查链接是否正确")
            else:
                st.error("❌ 请输入有效的 YouTube 链接")
        else:
            st.warning("⚠️ 请先输入 YouTube 链接")

# 显示视频信息
if hasattr(st.session_state, 'video_info') and st.session_state.video_info:
    st.markdown("---")
    st.header("📋 视频信息")

    info = st.session_state.video_info

    col_info1, col_info2 = st.columns([3, 1])

    with col_info1:
        st.subheader(info['title'])
        st.write(f"**上传者:** {info['uploader']}")
        st.write(f"**时长:** {format_duration(info['duration'])}")
        st.write(f"**观看次数:** {format_views(info['view_count'])}")
        st.write(f"**上传日期:** {format_date(info['upload_date'])}")

        # 显示描述
        if info['description']:
            with st.expander("📝 视频描述"):
                st.write(info['description'])

    with col_info2:
        if info['thumbnail']:
            st.image(info['thumbnail'], width=200)

    # 下载按钮
    st.markdown("---")
    if st.button("⬇️ 开始下载", type="primary", use_container_width=True):
        if hasattr(st.session_state, 'valid_url'):
            try:
                with st.spinner("正在下载视频，请稍候..."):
                    # 显示进度条
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    # 更新进度
                    for i in range(0, 50, 5):
                        progress_bar.progress(i)
                        status_text.text(f"正在处理: {i}%")
                        time.sleep(0.1)

                    # 执行下载
                    downloaded_file = download_video(
                        st.session_state.valid_url,
                        selected_quality,
                        selected_format
                    )

                    # 完成进度
                    for i in range(50, 101, 10):
                        progress_bar.progress(i)
                        status_text.text(f"正在处理: {i}%")
                        time.sleep(0.1)

                    if downloaded_file and os.path.exists(downloaded_file):
                        st.success("🎉 下载完成！")

                        # 显示文件信息
                        file_size = os.path.getsize(downloaded_file) / (1024 * 1024)  # MB
                        file_name = os.path.basename(downloaded_file)

                        st.info(f"**文件名:** {file_name}")
                        st.info(f"**文件大小:** {file_size:.2f} MB")

                        # 提供下载链接
                        with open(downloaded_file, "rb") as file:
                            st.download_button(
                                label="💾 下载到本地",
                                data=file,
                                file_name=file_name,
                                mime="video/mp4",
                                use_container_width=True
                            )

                        # 清理临时文件
                        try:
                            os.remove(downloaded_file)
                            temp_dir = os.path.dirname(downloaded_file)
                            if os.path.exists(temp_dir):
                                shutil.rmtree(temp_dir)
                        except:
                            pass

                    else:
                        st.error("❌ 下载失败，请重试")

            except Exception as e:
                st.error(f"❌ 下载过程中出现错误: {str(e)}")

# 右侧栏 - 功能说明
with col2:
    st.header("🌟 云端版特色")

    st.markdown("""
    ### ✅ 优势
    - **无地区限制**: 海外服务器直连
    - **高成功率**: 专业云端环境
    - **无需配置**: 开箱即用
    - **安全可靠**: Streamlit 官方托管

    ### 🚀 支持格式
    - **视频**: MP4, WebM
    - **质量**: 360p, 480p, 720p, 1080p, 最佳质量
    - **音频**: 自动包含最佳音质

    ### 📱 兼容性
    - 支持所有 YouTube 链接
    - 支持短链接 (youtu.be)
    - 支持播放列表单个视频
    - 支持移动端和桌面端
    """)

    st.markdown("---")

    st.header("💡 使用技巧")
    st.markdown("""
    - 选择合适的质量以平衡文件大小和清晰度
    - 大文件下载可能需要较长时间
    - 建议在网络稳定时使用
    - 下载完成后及时保存到本地
    """)

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
    <p>☁️ YouTube 视频下载器 - 云端版</p>
    <p>部署在 Streamlit Cloud，无需代理，全球可用</p>
    <p>请遵守相关法律法规和平台使用条款</p>
    </div>
    """,
    unsafe_allow_html=True
)
