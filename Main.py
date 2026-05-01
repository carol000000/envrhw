from ursina import *
from ursina.prefabs.tooltip import Tooltip
import os

# ---------------------------------------------------------
# 1. 系統初始化
# ---------------------------------------------------------
app = Ursina(antialiasing=True)
Texture.default_filtering = 'mipmap'
camera.fov = 110 
IMG_DIR = 'img/'.replace('\\', '/') 

# ---------------------------------------------------------
# 2. 全域資料庫 (自訂每一頁的地圖與 Info)
# ---------------------------------------------------------
SCENE_DATA = {
    '000': {
        'img': '000.jpg', 
        'map_img': 'mmap.png', 
        'info_img': 'info_000.png',
        'label_img': 'label_000.png',
        'next': '001', 'prev': '012'
    },
    '001': {
        'img': '001.jpg', 
        'map_img': 'map_001.png', 
        'info_img': 'info_001.png',
        'label_img': 'label_000.png',
        'next': '002', 'prev': '000'
    },
    '002': {
        'img': '002.jpg', 
        'map_img': 'map_002.png', 
        'info_img': 'info_002.png',
        'label_img': 'label_000.png',
        'next': '003', 'prev': '001'
    },
    '003': {
        'img': '003.jpg', 
        'map_img': 'map_003.png', 
        'info_img': 'info_003.png',
        'label_img': 'label_000.png',
        'next': '004', 'prev': '002'
    },
    '004': {
        'img': '004.jpg', 
        'map_img': 'map_004.png', 
        'info_img': 'info_004.png',
        'label_img': 'label_000.png',
        'next': '005', 'prev': '003'
    },
    '005': {
        'img': '005.jpg', 
        'map_img': 'map_005.png', 
        'info_img': 'info_005.png',
        'label_img': 'label_000.png',
        'next': '006', 'prev': '004'
    },
    '006': {
        'img': '006.jpg', 
        'map_img': 'map_006.png', 
        'info_img': 'info_006.png',
        'label_img': 'label_000.png',
        'next': '007', 'prev': '005'
    },
    '007': {
        'img': '007.jpg', 
        'map_img': 'map_007.png', 
        'info_img': 'info_007.png',
        'label_img': 'label_000.png',
        'next': '008', 'prev': '006'
    },
    '008': {
        'img': '008.jpg', 
        'map_img': 'map_008.png', 
        'info_img': 'info_008.png',
        'label_img': 'label_000.png',
        'next': '009', 'prev': '007'
    },
    '009': {
        'img': '009.jpg', 
        'map_img': 'map_009.png', 
        'info_img': 'info_009.png',
        'label_img': 'label_000.png',
        'next': '010', 'prev': '008'
    },
    '010': {
        'img': '010.jpg', 
        'map_img': 'map_010.png', 
        'info_img': 'info_010.png',
        'label_img': 'label_000.png',
        'next': '011', 'prev': '009'
    },
    '011': {
        'img': '011.jpg', 
        'map_img': 'map_011.png', 
        'info_img': 'info_011.png',
        'label_img': 'label_000.png',
        'next': '012', 'prev': '010'
    },
    '012': {
        'img': '012-2.jpg', 
        'map_img': 'map_012.png', 
        'info_img': 'info_012.png',
        'label_img': 'label_000.png',
        'next': '000', 'prev': '011' # 回到首頁，形成迴圈
    },
}
# ---------------------------------------------------------
# 3. 核心物件
# ---------------------------------------------------------
panorama = Entity(model='sphere', scale=-1000, rotation_z=180, unlit=True)
current_scene = '000'

# A. 右上角標籤
scene_label_bg = Sprite(
    parent=camera.ui, 
    scale=(.16, .08),    # 維持長方形比例
    position=(0.75, 0.43),
    color=color.white     # 顯示圖片原始質感
)
# B. UI 覆蓋層 (地圖與說明)
map_overlay = Sprite(parent=camera.ui, scale=1, z=-2, enabled=False)
info_overlay = Sprite(parent=camera.ui, scale=5, z=-1, enabled=False)

# ---------------------------------------------------------
# 4. 核心功能邏輯
# ---------------------------------------------------------

def switch_scene(scene_id):
    global current_scene
    if scene_id not in SCENE_DATA: return
    current_scene = scene_id
    data = SCENE_DATA[scene_id]
    
    # 1. 換背景全景圖
    panorama.texture = load_texture(IMG_DIR + data['img'])
    
    # 2. 【關鍵】根據 SCENE_DATA 匯入標籤圖片
    if 'label_img' in data:
        label_path = IMG_DIR + data['label_img']
        if os.path.exists(label_path):
            scene_label_bg.texture = load_texture(label_path)
            scene_label_bg.enabled = True
        else:
            scene_label_bg.enabled = False
            
    # 3. 換景時關閉地圖與資訊彈窗
    map_overlay.enabled = False
    info_overlay.enabled = False

def toggle_ui(ui_element, data_key):
    """根據當前場景資料動態顯示圖片"""
    data = SCENE_DATA[current_scene]
    if data_key in data:
        path = IMG_DIR + data[data_key]
        if os.path.exists(path):
            ui_element.texture = load_texture(path)
            ui_element.enabled = not ui_element.enabled

# ---------------------------------------------------------
# 5. UI 按鈕樣式 (半透明灰色)
# ---------------------------------------------------------
# 第一步：替換按鈕生成函式
def create_img_btn(img_name, x_pos, func):
    full_path = IMG_DIR + img_name
    btn = Button(
        model='quad',
        scale=(.06, .06),      # 正方形圖標比例
        x=x_pos, 
        y=-0.42, 
        parent=camera.ui,
        # 載入自訂圖片
        icon=full_path if os.path.exists(full_path) else None,
        # 180 是透明度 (0-255)，數值愈小愈透明
        color=color.rgba(255, 255, 255, 180),  
        highlight_color=color.white,           # 滑鼠移上去時變亮（不透明）
        pressed_color=color.gray,
        on_click=func
    )
    return btn

# 布建所有按鈕
# 加入了 go_home 功能，直接切換回 '000'
btn_home = create_img_btn('btn_home.png', -0.6, lambda: switch_scene('000'))
btn_back = create_img_btn('btn_back.png', -0.4, lambda: switch_scene(SCENE_DATA[current_scene]['prev']))
btn_next = create_img_btn('btn_next.png', -0.2, lambda: switch_scene(SCENE_DATA[current_scene]['next']))
btn_map  = create_img_btn('btn_map.png',   0.2, lambda: toggle_ui(map_overlay, 'map_img'))
btn_info = create_img_btn('btn_info.png',  0.4, lambda: toggle_ui(info_overlay, 'info_img'))

# ---------------------------------------------------------
# 6. 互動與運行
# ---------------------------------------------------------
# 點擊圖片關閉
map_overlay.add_script(Button(parent=map_overlay, color=color.clear, on_click=lambda: setattr(map_overlay, 'enabled', False)))
info_overlay.add_script(Button(parent=info_overlay, color=color.clear, on_click=lambda: setattr(info_overlay, 'enabled', False)))

EditorCamera()

def update():
    if held_keys['scroll up']: camera.fov -= 2
    if held_keys['scroll down']: camera.fov += 2

switch_scene('000')
app.run()