import numpy as np
import wave
import os

def create_sound(filename, frequency, duration, volume=0.5):
    # 设置参数
    sample_rate = 44100
    t = np.linspace(0, duration, int(sample_rate * duration))
    samples = np.sin(2 * np.pi * frequency * t) * volume
    
    # 确保值在 -1 到 1 之间
    samples = np.clip(samples, -1, 1)
    
    # 转换为 16 位整数
    samples = (samples * 32767).astype(np.int16)
    
    # 创建 WAV 文件
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # 单声道
        wav_file.setsampwidth(2)  # 2 字节 (16 位)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())

def main():
    # 创建 sounds 目录
    sounds_dir = os.path.join('assets', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    # 创建落子音效
    create_sound(os.path.join(sounds_dir, 'stone_place.wav'), 800, 0.1, 0.3)
    
    # 创建胜利音效
    create_sound(os.path.join(sounds_dir, 'game_win.wav'), 440, 0.5, 0.5)
    
    # 创建无效移动音效
    create_sound(os.path.join(sounds_dir, 'invalid_move.wav'), 200, 0.2, 0.3)
    
    # 创建撤销音效
    create_sound(os.path.join(sounds_dir, 'undo.wav'), 600, 0.15, 0.3)

if __name__ == '__main__':
    main() 