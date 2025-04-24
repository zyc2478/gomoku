import os
import pygame
import random

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)  # 设置背景音乐默认音量
        self.sounds = {}
        self.enabled = True
        self.background_music_enabled = True
        self.background_music_styles = [
            'peaceful', 'energetic', 'mysterious',
            'meditative', 'epic', 'jazz'
        ]
        self.current_style = 'peaceful'
        self._load_sounds()
        self._load_background_music()

    def _load_sounds(self):
        """加载所有音效"""
        sound_dir = os.path.join(os.path.dirname(__file__), 'assets', 'sounds')
        sound_files = {
            'place': 'place.wav',
            'win': 'victory.wav',
            'invalid': 'invalid.wav',
            'undo': 'undo.wav'
        }
        
        for sound_name, filename in sound_files.items():
            path = os.path.join(sound_dir, filename)
            if os.path.exists(path):
                self.sounds[sound_name] = pygame.mixer.Sound(path)
            else:
                print(f"警告：找不到音效文件 {path}")

    def _load_background_music(self):
        """加载背景音乐"""
        self._load_style_music(self.current_style)

    def _load_style_music(self, style):
        """加载指定风格的背景音乐"""
        music_path = os.path.join(os.path.dirname(__file__), 'assets', 'sounds', f'background_{style}.wav')
        if os.path.exists(music_path):
            try:
                pygame.mixer.music.load(music_path)
                self.current_style = style
                if self.background_music_enabled:
                    self.play_background_music()
            except Exception as e:
                print(f"加载背景音乐时出错：{e}")
                self.background_music_enabled = False

    def play(self, sound_name):
        """播放指定音效"""
        if self.enabled and sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"播放音效时出错：{e}")

    def play_background_music(self):
        """播放背景音乐"""
        if self.background_music_enabled:
            try:
                pygame.mixer.music.play(-1)  # -1表示循环播放
            except Exception as e:
                print(f"播放背景音乐时出错：{e}")
                self.background_music_enabled = False

    def stop_background_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()

    def toggle_background_music(self):
        """切换背景音乐开关"""
        self.background_music_enabled = not self.background_music_enabled
        if self.background_music_enabled:
            self.play_background_music()
        else:
            self.stop_background_music()
        return self.background_music_enabled

    def switch_background_music(self, style=None):
        """切换背景音乐风格
        Args:
            style: 指定的风格，如果为None则随机选择
        Returns:
            当前播放的风格
        """
        if style is None:
            # 随机选择一个不同于当前风格的风格
            available_styles = [s for s in self.background_music_styles if s != self.current_style]
            if available_styles:
                style = random.choice(available_styles)
            else:
                style = self.current_style
        
        if style in self.background_music_styles:
            was_playing = pygame.mixer.music.get_busy()
            self._load_style_music(style)
            if was_playing:
                self.play_background_music()
            return style
        return self.current_style

    def toggle(self):
        """切换音效开关"""
        self.enabled = not self.enabled
        return self.enabled

    def set_volume(self, volume):
        """设置音效音量（0.0 到 1.0）"""
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def set_background_music_volume(self, volume):
        """设置背景音乐音量（0.0 到 1.0）"""
        pygame.mixer.music.set_volume(volume)

    def cleanup(self):
        """清理资源"""
        pygame.mixer.quit() 