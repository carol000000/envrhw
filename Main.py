from ursina import *

# 初始化 Ursina
app = Ursina(antialiasing=True)
Texture.default_filtering = 'mipmap'

# --- [設定區：統一資料夾路徑] ---
# 確保你的程式檔旁邊有一個資料夾叫做 img
IMG_DIR = 'img/'

# --- [1. 場景資料庫] ---
# 字典內的檔名不需要再寫 img/，系統會自動拼接
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
    # 接下來的 12 個場景依此類推填寫...
}

# --- [2. 核心實體建立] ---

# 街景球體：處理旋轉與反轉法線
panorama = Entity(
    model='sphere', 
    scale=-500, 
    rotation_z=180, 
    unlit=True
)

current_scene = 'home'

# 說明圖片實體
info_overlay = Sprite(
    parent=camera.ui,
    enabled=False,
    scale=0.6,
    z=-1 
)

# --- [3. 核心功能函式] ---

def switch_scene(scene_id):
    """跳轉場景邏輯"""
    global current_scene
    if scene_id not in SCENE_DATA:
        print(f"錯誤：找不到場景 {scene_id}")
        return

    current_scene = scene_id
    data = SCENE_DATA[scene_id]
    
    # 自動拼接路徑載入街景：img/xxx.jpg
    panorama.texture = load_texture(IMG_DIR + data['img'])
    
    # 切換場景時隱藏說明圖
    info_overlay.enabled = False
    print(f"目前場景：{scene_id}")

def toggle_info():
    """顯示或隱藏說明圖"""
    data = SCENE_DATA[current_scene]
    img_name = data.get('info')
    if img_name:
        # 自動拼接路徑載入說明圖：img/info_xxx.png
        info_overlay.texture = load_texture(IMG_DIR + img_name)
        info_overlay.enabled = not info_overlay.enabled

def play_audio():
    """語音播放預留位"""
    audio_name = SCENE_DATA[current_scene].get('audio')
    if audio_name:
        # 未來實作可改為：Audio(IMG_DIR + audio_name)
        print(f"系統：準備播放語音 {IMG_DIR + audio_name}")

# --- [4. 平面 UI 按鈕區 (camera.ui)] ---

button_y = -0.4

# 建立按鈕的捷徑函式，節省重複代碼
def create_ui_button(label, x_pos, color_val, func):
    b = Button(
        text=label, 
        scale=(.12, .05), 
        x=x_pos, 
        y=button_y, 
        parent=camera.ui, 
        color=color_val
    )
    b.on_click = func
    return b

# 生成五個功能按鈕
btn_home = create_ui_button('HOME', -0.6, color.dark_gray, lambda: switch_scene('home'))
btn_prev = create_ui_button('PREV', -0.4, color.orange, lambda: switch_scene(SCENE_DATA[current_scene]['prev']))
btn_next = create_ui_button('NEXT', -0.2, color.orange, lambda: switch_scene(SCENE_DATA[current_scene]['next']))
btn_info = create_ui_button('INFO', 0.4, color.azure, toggle_info)
btn_audio = create_ui_button('VOICE', 0.6, color.green, play_audio)

# --- [5. 測試輔助與啟動] ---

# 點擊說明圖本身可以關閉它
info_overlay.add_script(Button(parent=info_overlay, color=color.clear, on_click=toggle_info))

# 電腦開發測試輔助：點擊畫面輸出座標 (幫你快速找未來要放方塊的位置)
def input(key):
    if key == 'left mouse down':
        if mouse.world_point:
            print(f"點擊座標：{mouse.world_point}")

# 開發者相機
EditorCamera()

# 初始場景
switch_scene('home')

app.run()