from ursina import *
from ursina.prefabs.tooltip import Tooltip

# ---------------------------------------------------------
# 1. 系統初始化 (System Setup)
# ---------------------------------------------------------
app = Ursina(antialiasing=True)       # 初始化引擎，開啟抗鋸齒讓畫面邊緣更平滑
camera.fov = 110               # 1. 拉遠視野 
Texture.default_filtering = 'mipmap'  # 預設過濾模式設為 mipmap，防止 360 圖片轉動時產生閃爍感



# 設定圖片讀取的根目錄資料夾
IMG_DIR = 'img/' 

# ---------------------------------------------------------
# 2. 場景資料庫 (Database)
# 邏輯：用字典管理所有資料。未來新增場景只需在這裡加一行，
#       並確保 img 資料夾有對應的編號圖檔。
# ---------------------------------------------------------
SCENE_DATA = {
    # 格式：'ID': {'img': '街景圖', 'next': '下一處', 'prev': '上一處', 'info': '說明圖', 'audio': '語音'}
    '000': {'img': '000.jpg', 'next': '001', 'prev': '012', 'info': 'info_000.png', 'audio': 'audio_000.mp3'},
    '001': {'img': '001.jpg', 'next': '002', 'prev': '000', 'info': 'info_001.png', 'audio': 'audio_001.mp3'},
    '002': {'img': '002.jpg', 'next': '003', 'prev': '001', 'info': 'info_002.png', 'audio': 'audio_002.mp3'},
    '003': {'img': '003.jpg', 'next': '004', 'prev': '002', 'info': 'info_003.png', 'audio': 'audio_003.mp3'},
    '004': {'img': '004.jpg', 'next': '005', 'prev': '003', 'info': 'info_004.png', 'audio': 'audio_004.mp3'},
    '005': {'img': '005.jpg', 'next': '006', 'prev': '004', 'info': 'info_005.png', 'audio': 'audio_005.mp3'},
    '006': {'img': '006.jpg', 'next': '007', 'prev': '005', 'info': 'info_006.png', 'audio': 'audio_006.mp3'},
    '007': {'img': '007.jpg', 'next': '008', 'prev': '006', 'info': 'info_007.png', 'audio': 'audio_007.mp3'},
    '008': {'img': '008.jpg', 'next': '009', 'prev': '007', 'info': 'info_008.png', 'audio': 'audio_008.mp3'},
    '009': {'img': '009.jpg', 'next': '010', 'prev': '008', 'info': 'info_009.png', 'audio': 'audio_009.mp3'},
    '010': {'img': '010.jpg', 'next': '011', 'prev': '009', 'info': 'info_010.png', 'audio': 'audio_010.mp3'},
    '011': {'img': '011.jpg', 'next': '012', 'prev': '010', 'info': 'info_011.png', 'audio': 'audio_011.mp3'},
    '012': {'img': '012-2.jpg', 'next': '000', 'prev': '011', 'info': 'info_012.png', 'audio': 'audio_012.mp3'},
}

# ---------------------------------------------------------
# 3. 核心 3D 實體 (Core Entities)
# ---------------------------------------------------------
# 建立街景球體，將照片貼在球體內側
panorama = Entity(
    model='sphere', 
    scale=-500,       # 負值 scale 會翻轉模型法線，讓貼圖朝向球心
    rotation_z=180,   # 修正 Ursina 載入球體時可能的上下顛倒問題
    unlit=True        # 關閉燈光計算，直接呈現原圖色彩（不發黑）
)

# 儲存目前所在位置的變數
current_scene = '000'

# ---------------------------------------------------------
# 4. UI 介面組件 (User Interface)
# 邏輯：parent=camera.ui 代表這些物體會「貼」在螢幕上，不隨滑鼠轉動
# ---------------------------------------------------------

# A. 當前場景編號顯示
scene_label_bg = Sprite(
    parent=camera.ui,
    texture=IMG_DIR + 'label_bg.png', 
    scale=(0.12, 0.05),
    position=(0.75, 0.45)
)
scene_text = Text(
    parent=scene_label_bg,
    text='000', scale=6, origin=(0, 0), z=-0.1
)

# B. 全螢幕平面地圖
map_overlay = Sprite(
    parent=camera.ui,
    texture=IMG_DIR + 'map.png', 
    scale=0.8, z=-2, enabled=False  # 初始設為 False 隱藏
)

# C. 說明圖彈出視窗
info_overlay = Sprite(parent=camera.ui, enabled=False, scale=0.6, z=-1)

# ---------------------------------------------------------
# 5. 地圖功能與點位 (Map System)
# ---------------------------------------------------------
def create_map_point(target_id, x, y):
    """
    邏輯：在地圖上產生小紅點。
    參數：target_id(跳轉目標ID), x/y(在地圖圖檔上的座標位置)
    """
    dot = Button(
        parent=map_overlay, model='circle', scale=(0.02, 0.035),
        position=(x, y), color=color.red, highlight_color=color.yellow,
        tooltip=Tooltip(f"前往 {target_id}") # 滑鼠移上去顯示提示
    )
    # 點擊紅點：執行切換場景，並同時關閉地圖選單
    dot.on_click = lambda: [switch_scene(target_id), toggle_map()]
    return dot

# 在地圖上手動新增景點位置
create_map_point('000', -0.2, 0.1)
create_map_point('005', 0.1, -0.2)
create_map_point('012', 0.3, 0.3)

# ---------------------------------------------------------
# 6. 控制函式 (Control Functions)
# ---------------------------------------------------------
def switch_scene(scene_id):
    """切換場景的主控制邏輯"""
    global current_scene
    if scene_id not in SCENE_DATA: return # 安全檢查：找不到 ID 就跳出

    current_scene = scene_id
    data = SCENE_DATA[scene_id]
    
    # 1. 更新球體貼圖
    panorama.texture = load_texture(IMG_DIR + data['img'])
    
    # 2. 更新畫面右上角的 ID 標籤
    scene_text.text = f"SCENE: {scene_id}"
    
    # 3. 確保換場景時，舊的 UI 會自動關閉
    info_overlay.enabled = False
    map_overlay.enabled = False
    print(f"目前導覽至：{scene_id}")

def toggle_map():
    """切換地圖的開關邏輯"""
    map_overlay.enabled = not map_overlay.enabled

def toggle_info():
    """讀取當前場景對應的 info 圖檔並顯示"""
    data = SCENE_DATA[current_scene]
    if data.get('info'):
        info_overlay.texture = load_texture(IMG_DIR + data['info'])
        info_overlay.enabled = not info_overlay.enabled

# ---------------------------------------------------------
# 7. 底部按鈕欄 (Nav Buttons)
# ---------------------------------------------------------
def create_ui_btn(label, x_pos, color_val, func):
    """快速生成導覽按鈕的模板"""
    return Button(
        text=label, scale=(.11, .05), x=x_pos, y=-0.42, 
        parent=camera.ui, color=color_val, on_click=func
    )

btn_home  = create_ui_btn('HOME', -0.6, color.dark_gray, lambda: switch_scene('000'))
btn_back  = create_ui_btn('BACK', -0.4, color.orange,    lambda: switch_scene(SCENE_DATA[current_scene]['prev']))
btn_next  = create_ui_btn('NEXT', -0.2, color.orange,    lambda: switch_scene(SCENE_DATA[current_scene]['next']))
btn_map   = create_ui_btn('MAP',  0.2,  color.magenta,   toggle_map)
btn_info  = create_ui_btn('INFO', 0.4,  color.azure,     toggle_info)

# ---------------------------------------------------------
# 8. 系統運作與測試 (Run)
# ---------------------------------------------------------
# 讓說明圖跟地圖在點擊背景時能自動關閉（使用者體驗更好）
info_overlay.add_script(Button(parent=info_overlay, color=color.clear, on_click=toggle_info))
map_overlay.add_script(Button(parent=map_overlay, color=color.clear, on_click=toggle_map))

# 啟用 EditorCamera，讓電腦使用者可以用滑鼠右鍵旋轉視角
EditorCamera()

# 程式啟動：自動進入第一個場景
switch_scene('000')

app.run()