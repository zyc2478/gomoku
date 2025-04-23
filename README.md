# 五子棋游戏 (Gomoku)

这是一个具有图形界面的五子棋游戏实现，支持鼠标操作，具有完整的游戏功能和自动测试。游戏采用 PyQt5 开发，具有美观的界面和流畅的操作体验。

## 功能特点

- 15x15 标准棋盘
- 精美的木纹背景
- 鼠标操作，简单直观
- 支持两人对战
- 自动判断胜负
- 支持撤销操作
- 支持新游戏
- 棋子放置预览
- 完整的单元测试

## 系统要求

- Python 3.8 或更高版本
- 支持的操作系统：Windows, macOS, Linux

## 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/[your-username]/gomoku.git
cd gomoku
```

2. 创建虚拟环境（可选但推荐）：
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\\Scripts\\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行游戏

### 图形界面版本（推荐）
```bash
python main.py
```

### 命令行版本
```bash
python game_ui.py
```

## 游戏操作说明

### 图形界面版本
1. 使用鼠标点击棋盘位置放置棋子
2. 鼠标悬停时会显示半透明的预览棋子
3. 点击"撤销"按钮可以撤销上一步
4. 点击"新游戏"按钮可以开始新的对局
5. 界面顶部显示当前回合信息和游戏状态

### 命令行版本
1. 输入行号(0-14)和列号(0-14)来放置棋子，例如：`7 7`
2. 使用 `u` 命令撤销上一步
3. 使用 `q` 命令退出游戏
4. ●表示黑子，○表示白子

## 运行测试

```bash
pytest test_gomoku.py
```

## 项目结构

```
gomoku/
├── assets/
│   └── wood_texture.jpg    # 棋盘背景图
├── gomoku.py              # 游戏核心逻辑
├── gomoku_gui.py          # 图形界面实现
├── game_ui.py            # 命令行界面实现
├── main.py               # 启动脚本
├── test_gomoku.py        # 单元测试
├── create_texture.py     # 背景图生成脚本
├── requirements.txt      # 项目依赖
└── README.md            # 项目说明
```

## 开发说明

1. 游戏逻辑位于 `gomoku.py`，包含了核心的游戏规则和状态管理
2. 图形界面使用 PyQt5 实现，代码位于 `gomoku_gui.py`
3. 提供了完整的单元测试，覆盖了所有核心功能
4. 使用 NumPy 进行棋盘状态管理
5. 支持自定义棋盘背景（通过修改 `create_texture.py`）

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情 