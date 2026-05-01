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
        'map_img': 'mmap000.png', 
        'info_img': '000info.png',
        'label_img': 'school.png',
        'next': '001', 'prev': '012'
        'audio',
    },
    '001': {
        'img': '001.jpg', 
        'map_img': 'mmap001.png', 
        'info_img': '001info.png',
        'label_img': 'Campher Boulevard.png',
        'next': '002', 'prev': '000'
        'audio',
    },
    '002': {
        'img': '002.jpg', 
        'map_img': 'mmap002.png', 
        'info_img': '002info.png',
        'label_img': 'The Old Red Cedar.png',
        'next': '003', 'prev': '001'
        'audio',
    },
    '003': {
        'img': '003.jpg', 
        'map_img': 'mmap003.png', 
        'info_img': '003info.png',
        'label_img': 'Government Building.png',
        'next': '004', 'prev': '002'
        'audio',
    },
    '004': {
        'img': '004.jpg', 
        'map_img': 'mmap004.png', 
        'info_img': '004info.png',
        'label_img': 'Village Archway.png',
        'next': '005', 'prev': '003'
        'audio',
    },
    '005': {
        'img': '005.jpg', 
        'map_img': 'mmap005.png', 
        'info_img': '005info.png',
        'label_img': 'Fulong Temple.png',
        'next': '006', 'prev': '004'
        'audio',
    },
    '006': {
        'img': '006.jpg', 
        'map_img': 'mmap006.png', 
        'info_img': '006info.png',
        'label_img': 'Bodhi Boulevard.png',
        'next': '007', 'prev': '005'
        'audio',
    },
    '007': {
        'img': '007.jpg', 
        'map_img': 'mmap007.png', 
        'info_img': '007info.png',
        'label_img': 'Cheng Yuan Tzuen.png',
        'next': '008', 'prev': '006'
        'audio',
    },
    '008': {
        'img': '008.jpg', 
        'map_img': 'mmap008.png', 
        'info_img': '008info.png',
        'label_img': 'Chung Hsing Botanical Garden.png',
        'next': '009', 'prev': '007'
        'audio',
    },
    '009': {
        'img': '009.jpg', 
        'map_img': 'mmap009.png', 
        'info_img': '009info.png',
        'label_img': 'Chung Hsing Hall.png',
        'next': '010', 'prev': '008'
        'audio',
    },
    '010': {
        'img': '010.jpg', 
        'map_img': 'mmap010.png', 
        'info_img': '010info.png',
        'label_img': 'Central Taiwan Science Park.png',
        'next': '011', 'prev': '009'
        'audio',
    },
    '011': {
        'img': '011.jpg', 
        'map_img': 'mmap011.png', 
        'info_img': '011info.png',
        'label_img': 'Taiwan Historica.png',
        'next': '012', 'prev': '010'
        'audio',
    },
    '012': {
        'img': '012-2.jpg', 
        'map_img': 'mmap012.png', 
        'info_img': '012info.png',
        'label_img': 'Traditional Market.png',
        'next': '000', 'prev': '011' # 回到首頁，形成迴圈
        'audio',
    },
    '121': {
        'img': '012-1.jpg', 
        'map_img': 'mmap121.png', 
        'info_img': '121info.png',
        'label_img': 'Traditional Market1.png',
        'next': '012', 'prev': '012' 
        'audio',
    },
    '123': {
        'img': '012-3.jpg', 
        'map_img': 'mmap123.png', 
        'info_img': '123info.png',
        'label_img': 'Traditional Market3.png',
        'next': '012', 'prev': '012' 
        'audio',
    },
}
# ---------------------------------------------------------
# 3. 核心物件
# ---------------------------------------------------------
panorama = Entity(model='sphere', scale=-1000, rotation_z=180, unlit=True)
current_scene = '000'
current_audio = None  # 用來追蹤目前正在播放的聲音 換場景時切斷前一個聲音，避免聲音重疊

# A. 右上角標籤
scene_label_bg = Sprite(
    parent=camera.ui, 
    scale=(.16, .08),    # 維持長方形比例
    position=(0.75, 0.43),
    color=color.white     # 顯示圖片原始質感
)
# B. UI 覆蓋層 (地圖與說明)
# map_overlay 建議稍微大一點，position 放在中間 (0,0)
map_overlay = Sprite(parent=camera.ui, scale=(.7, .7), position=(0,0), z=-2, enabled=False)

# info_overlay 設定為佔螢幕 80% 高度與寬度
info_overlay = Sprite(
    parent=camera.ui, 
    scale=(.8, .8),      # <--- 在這裡調整 Info 圖片的大小
    position=(0,0),      # 確保在螢幕正中間
    z=-1, 
    enabled=False
)

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
    
    # 2. 更新標籤圖片
    if 'label_img' in data:
        label_path = IMG_DIR + data['label_img']
        if os.path.exists(label_path):
            scene_label_bg.texture = load_texture(label_path)
            scene_label_bg.enabled = True
    
    # 3. 【核心邏輯】判斷是否顯示分支按鈕
    if scene_id == '012':
        btn_to_121.enabled = True
        btn_to_123.enabled = True
    else:
        btn_to_121.enabled = False
        btn_to_123.enabled = False
            
    # 4. 換景時關閉地圖與資訊彈窗
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
            # 如果開啟時想確保地圖跟資訊圖不會同時重疊，可以加這兩行：
            if ui_element == info_overlay: map_overlay.enabled = False
            if ui_element == map_overlay: info_overlay.enabled = False

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
         
        highlight_color=color.white,           # 滑鼠移上去時變亮（不透明）
        pressed_color=color.gray,
        on_click=func
    )
    return btn

# 建立前往 121 的分支按鈕
btn_to_121 = Button(
    
    icon=IMG_DIR + 'First Market.png', # 放入你的圖標檔名
    scale=(.06, .06),
    x=0.8, y=-0.4,
    parent=camera.ui,
    enabled=False,
    color=color.white,
    on_click=lambda: switch_scene('121')
)

# 建立前往 123 的分支按鈕
btn_to_123 = Button(
    
    icon=IMG_DIR + 'Third Market.png', 
    scale=(.06, .06),
    x=0.8, y=-0.2,       # 位置可以自己調
    parent=camera.ui,
    enabled=False,    # 預設隱藏
    color=color.white,
    on_click=lambda: switch_scene('123')
)

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