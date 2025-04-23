from PIL import Image, ImageDraw
import numpy as np
import os

def create_wood_texture(size=(600, 600)):
    # 创建基础图像
    base = Image.new('RGB', size, (210, 180, 140))
    draw = ImageDraw.Draw(base)
    
    # 生成随机木纹
    for y in range(0, size[1], 2):
        color = (
            np.random.randint(180, 200),
            np.random.randint(150, 170),
            np.random.randint(110, 130)
        )
        draw.line([(0, y), (size[0], y)], fill=color, width=2)
    
    # 添加一些随机的深色线条模拟木纹
    for _ in range(20):
        start_y = np.random.randint(0, size[1])
        color = (
            np.random.randint(160, 180),
            np.random.randint(130, 150),
            np.random.randint(90, 110)
        )
        for x in range(0, size[0], 2):
            y = start_y + np.random.randint(-2, 3)
            if 0 <= y < size[1]:
                draw.point((x, y), fill=color)
    
    # 保存图像
    if not os.path.exists('assets'):
        os.makedirs('assets')
    base.save('assets/wood_texture.jpg', quality=95)

if __name__ == "__main__":
    create_wood_texture() 