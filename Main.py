from ursina import *

# 初始化 Ursina 並優化畫質
app = Ursina(antialiasing=True)
Texture.default_filtering = 'mipmap'

# --- [1. 場景資料庫] ---
# 你可以在這裡輕鬆擴展到 15 個場景
SCENE_DATA = {
    'home': {
        'img': '000.jpg',
        'next': 'garden',
        'prev': 'office',
        'info': 'info_home.png',
        'audio': 'audio_home.mp3'
    },
    'garden': {
        'img': '001.jpg',
        'next': 'office',
        'prev': 'home',
        'info': 'info_garden.png',
        'audio': 'audio_garden.mp3'
    },
    'office': {
        'img': '002.jpg',
        'next': 'home',
        'prev': 'garden',
        'info': 'info_office.png',
        'audio': 'audio_office.mp3'
    },
    # 這裡繼續往下寫到 15 個...
}

# --- [2. 核心實體建立] ---

# 街景球體：scale 使用負值來翻轉法線，rotation_z 修正上下顛倒
panorama = Entity(
    model='sphere', 
    scale=-500, 
    rotation_z=180, 
    unlit=True
)

# 當前場景 ID
current_scene = 'home'

# 說明圖片實體：使用 Sprite 並固定在 camera.ui
info_overlay = Sprite(
    parent=camera.ui,
    enabled=False,
    scale=0.6,
    z=-1  # 確保在最前方
)

# --- [3. 核心功能函式] ---

def switch_scene(scene_id):
    """切換場景的主邏輯"""
    global current_scene
    if scene_id not in SCENE_DATA:
        print(f"錯誤：找不到場景 {scene_id}")
        return

    current_scene = scene_id
    data = SCENE_DATA[scene_id]
    
    # 更換背景圖並確保畫質
    new_tex = load_texture(data['img'])
    panorama.texture = new_tex
    if panorama.texture:
        panorama.texture.filtering = 'mipmap'
    
    # 切換場景時自動隱藏上一個場景的說明圖
    info_overlay.enabled = False
    print(f"目前位置：{scene_id}")

def toggle_info():
    """顯示或隱藏當前場景的說明圖片"""
    img_path = SCENE_DATA[current_scene].get('info')
    if img_path:
        info_overlay.texture = load_texture(img_path)
        info_overlay.enabled = not info_overlay.enabled

def play_audio():
    """播放當前場景的語音 (預留位)"""
    audio_path = SCENE_DATA[current_scene].get('audio')
    if audio_path:
        print(f"系統：正在播放語音檔案 {audio_path}")
        # 未來實作：Audio(audio_path, loop=False, autoplay=True)

# --- [4. 平面 UI 按鈕區 (camera.ui)] ---

# 設定按鈕通用樣式
button_y = -0.4  # 按鈕統一高度

# 回首頁
btn_home = Button(text='HOME', scale=(.12, .05), x=-0.6, y=button_y, parent=camera.ui, color=color.dark_gray)
btn_home.on_click = lambda: switch_scene('home')

# 上一個景點
btn_prev = Button(text='PREV', scale=(.12, .05), x=-0.4, y=button_y, parent=camera.ui, color=color.orange)
btn_prev.on_click = lambda: switch_scene(SCENE_DATA[current_scene]['prev'])

# 下一個景點
btn_next = Button(text='NEXT', scale=(.12, .05), x=-0.2, y=button_y, parent=camera.ui, color=color.orange)
btn_next.on_click = lambda: switch_scene(SCENE_DATA[current_scene]['next'])

# 顯示圖片說明
btn_info = Button(text='INFO', scale=(.12, .05), x=0.4, y=button_y, parent=camera.ui, color=color.azure)
btn_info.on_click = toggle_info

# 播放語音
btn_audio = Button(text='VOICE', scale=(.12, .05), x=0.6, y=button_y, parent=camera.ui, color=color.green)
btn_audio.on_click = play_audio

# --- [5. 測試輔助與啟動] ---

# 讓圖片說明點擊後可以消失
info_overlay.add_script(Button(parent=info_overlay, color=color.clear, on_click=toggle_info))

# 電腦測試攝影機：滑鼠右鍵旋轉，左鍵點擊按鈕
EditorCamera()

# 初始進入第一個場景
switch_scene('home')

app.run()