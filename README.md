# 🚀 一键部署到 Streamlit Cloud

## 📦 部署包文件

为了部署到 Streamlit Cloud，你需要以下文件：

### 必需文件
1. `app.py` - 主应用文件（已创建）
2. `requirements.txt` - 依赖包列表
3. `README.md` - 项目说明

## 🔧 快速部署步骤

### 步骤 1: 创建 GitHub 仓库

1. 登录 [GitHub](https://github.com)
2. 点击右上角的 "+" → "New repository"
3. 仓库名称: `youtube-downloader`
4. 设置为 **Public**（重要！）
5. 勾选 "Add a README file"
6. 点击 "Create repository"

### 步骤 2: 上传文件

有两种方法上传文件：

#### 方法 A: 网页上传（推荐）
1. 在仓库页面点击 "uploading an existing file"
2. 拖拽或选择以下文件：
   - `app.py`
   - 将 `requirements.txt` 上传
3. 在底部写提交信息: "Add YouTube downloader app"
4. 点击 "Commit changes"

#### 方法 B: Git 命令行
```bash
git clone https://github.com/你的用户名/youtube-downloader.git
cd youtube-downloader
# 复制 app.py 和 requirements.txt 到这个目录
cp /path/to/app.py .
cp /path/to/requirements_cloud.txt requirements.txt
git add .
git commit -m "Add YouTube downloader app"
git push
```

### 步骤 3: 部署到 Streamlit Cloud

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 选择你的仓库: `youtube-downloader`
5. 主文件路径: `app.py`
6. 点击 "Deploy!"

### 步骤 4: 等待部署完成

- 部署通常需要 2-5 分钟
- 你会看到构建日志
- 成功后会得到一个 URL，如: `https://youtube-downloader-xxx.streamlit.app`

## 📋 部署检查清单

- [ ] GitHub 仓库已创建且为 Public
- [ ] `app.py` 文件已上传
- [ ] `requirements.txt` 文件已上传（注意文件名）
- [ ] Streamlit Cloud 账号已创建
- [ ] 应用已成功部署
- [ ] 可以通过 URL 访问应用

## 🎯 部署后的优势

### ✅ **无地区限制**
```
本地环境（中国）          云端环境（海外）
     ❌                      ✅
需要代理才能访问          直接访问 YouTube
成功率较低               成功率很高
网络配置复杂             无需任何配置
```

### ✅ **全球可用**
- 任何人都可以通过 URL 访问
- 24/7 在线服务
- 无需本地安装任何软件

### ✅ **更稳定**
- 专业的云端基础设施
- 自动处理服务器维护
- 高可用性保证

## 🔧 自定义配置

### 修改应用标题
在 `app.py` 中修改：
```python
st.set_page_config(
    page_title="你的自定义标题",
    page_icon="🎬",  # 可以改成其他 emoji
)
```

### 添加自定义域名（付费功能）
Streamlit Cloud 的付费版本支持自定义域名

## 📊 使用统计

部署后，你可以在 Streamlit Cloud 控制台查看：
- 应用访问次数
- 用户地理分布
- 错误日志
- 性能指标

## 🔄 更新应用

当你需要更新应用时：
1. 在 GitHub 仓库中修改代码
2. 提交更改
3. Streamlit Cloud 会自动检测并重新部署

## 💡 成功案例

部署成功后，你的应用将：
- 解决中国大陆用户的访问问题
- 提供稳定的 YouTube 下载服务
- 无需用户进行任何复杂配置
- 支持全球用户访问

---

**现在就开始部署，让全世界的用户都能使用你的 YouTube 下载器！**
