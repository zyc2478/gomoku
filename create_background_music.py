import os
import numpy as np
from synthesizer import Player, Synthesizer, Waveform
from scipy.io import wavfile

def create_note(frequency, duration, sample_rate=44100, amplitude=0.3):
    """创建一个音符"""
    t = np.linspace(0, duration, int(sample_rate * duration))
    # 添加更多泛音以丰富音色
    harmonics = [1.0, 0.5, 0.3, 0.2, 0.15, 0.1]
    wave = np.zeros_like(t)
    for i, weight in enumerate(harmonics, 1):
        wave += weight * np.sin(2 * np.pi * frequency * i * t)
    # 添加更自然的ADSR包络
    attack = int(0.1 * len(wave))
    decay = int(0.2 * len(wave))
    sustain = int(0.5 * len(wave))
    release = len(wave) - attack - decay - sustain
    
    envelope = np.ones_like(wave)
    envelope[:attack] = np.linspace(0, 1, attack)
    envelope[attack:attack+decay] = np.linspace(1, 0.7, decay)
    envelope[attack+decay:attack+decay+sustain] = 0.7
    envelope[attack+decay+sustain:] = np.linspace(0.7, 0, release)
    
    return wave * envelope * amplitude

def create_chord(frequencies, duration, sample_rate=44100, amplitude=0.3):
    """创建和弦"""
    wave = np.zeros(int(sample_rate * duration))
    for freq in frequencies:
        wave += create_note(freq, duration, sample_rate, amplitude/len(frequencies))
    return wave

def note_to_freq(note):
    """将音符转换为频率"""
    notes = {
        'C': 0, 'C#': 1, 'Db': 1,
        'D': 2, 'D#': 3, 'Eb': 3,
        'E': 4,
        'F': 5, 'F#': 6, 'Gb': 6,
        'G': 7, 'G#': 8, 'Ab': 8,
        'A': 9, 'A#': 10, 'Bb': 10,
        'B': 11
    }
    # 处理音符名称和八度
    if len(note) == 2:
        note_name, octave = note[0], int(note[1])
    else:
        note_name, octave = note[:-1], int(note[-1])
    
    semitones = notes[note_name]
    return 440 * 2**((octave - 4) + (semitones - 9)/12)

def create_peaceful_music(duration=60, sample_rate=44100):
    """创建平静的背景音乐"""
    # 和弦进行
    chord_progression = [
        ['C4', 'E4', 'G4'],  # C major
        ['A3', 'C4', 'E4'],  # A minor
        ['F3', 'A3', 'C4'],  # F major
        ['G3', 'B3', 'D4']   # G major
    ]
    
    # 将音符转换为频率
    chord_freqs = [[note_to_freq(note) for note in chord] for chord in chord_progression]
    
    # 创建音乐
    music = np.array([])
    chord_duration = 4.0
    for _ in range(int(duration // (chord_duration * len(chord_progression)))):
        for chord in chord_freqs:
            # 添加和弦
            chord_wave = create_chord(chord, chord_duration, sample_rate, 0.3)
            # 添加简单的旋律
            melody_note = create_note(chord[0] * 2, chord_duration, sample_rate, 0.2)
            combined = chord_wave + melody_note
            music = np.append(music, combined)
    
    return music

def create_energetic_music(duration=60, sample_rate=44100):
    """创建充满活力的背景音乐"""
    # 更快的节奏和更丰富的和弦
    chord_progression = [
        ['C4', 'E4', 'G4', 'B4'],  # Cmaj7
        ['F4', 'A4', 'C5', 'E5'],  # Fmaj7
        ['G4', 'B4', 'D5', 'F5'],  # G7
        ['A4', 'C5', 'E5', 'G5']   # Am7
    ]
    
    chord_freqs = [[note_to_freq(note) for note in chord] for chord in chord_progression]
    
    music = np.array([])
    chord_duration = 2.0
    for _ in range(int(duration // (chord_duration * len(chord_progression)))):
        for chord in chord_freqs:
            chord_wave = create_chord(chord, chord_duration, sample_rate, 0.25)
            # 添加快速的旋律
            melody_notes = [
                create_note(freq * 2, chord_duration/4, sample_rate, 0.15)
                for freq in chord
            ]
            melody = np.concatenate(melody_notes)
            combined = chord_wave + melody[:len(chord_wave)]
            music = np.append(music, combined)
    
    return music

def create_mysterious_music(duration=60, sample_rate=44100):
    """创建神秘的背景音乐"""
    # 使用不常见的和弦进行
    chord_progression = [
        ['D4', 'F4', 'B4'],      # Dim
        ['E4', 'G#4', 'B4'],     # E
        ['C4', 'Eb4', 'G4'],     # Cm
        ['B3', 'D4', 'F4']       # Bdim
    ]
    
    chord_freqs = [[note_to_freq(note) for note in chord] for chord in chord_progression]
    
    music = np.array([])
    chord_duration = 3.0
    for _ in range(int(duration // (chord_duration * len(chord_progression)))):
        for chord in chord_freqs:
            # 添加颤音效果
            t = np.linspace(0, chord_duration, int(sample_rate * chord_duration))
            vibrato = np.sin(2 * np.pi * 5 * t) * 0.1
            
            chord_wave = create_chord(chord, chord_duration, sample_rate, 0.3)
            # 添加神秘的旋律
            melody_freq = chord[0] * 2
            melody = create_note(melody_freq, chord_duration, sample_rate, 0.2)
            # 应用颤音
            melody = melody * (1 + vibrato[:len(melody)])
            
            combined = chord_wave + melody
            music = np.append(music, combined)
    
    return music

def create_victory_music(duration=10, sample_rate=44100):
    """创建胜利音乐"""
    # 使用明亮的和弦进行
    chord_progression = [
        ['C4', 'E4', 'G4', 'C5'],  # C major
        ['G4', 'B4', 'D5', 'G5'],  # G major
        ['C5', 'E5', 'G5', 'C6']   # C major (高八度)
    ]
    
    chord_freqs = [[note_to_freq(note) for note in chord] for chord in chord_progression]
    
    music = np.array([])
    chord_duration = 1.0
    
    # 添加上升的音阶
    scale_notes = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
    scale_freqs = [note_to_freq(note) for note in scale_notes]
    
    # 生成上升音阶
    for freq in scale_freqs:
        note = create_note(freq, chord_duration/2, sample_rate, 0.3)
        music = np.append(music, note)
    
    # 添加和弦进行
    for chord in chord_freqs:
        chord_wave = create_chord(chord, chord_duration, sample_rate, 0.4)
        music = np.append(music, chord_wave)
    
    return music

def create_place_sound(duration=0.2, sample_rate=44100):
    """创建落子音效"""
    # 使用两个音符的组合
    freq1 = note_to_freq('C5')
    freq2 = note_to_freq('E5')
    
    # 创建两个音符
    note1 = create_note(freq1, duration/2, sample_rate, 0.3)
    note2 = create_note(freq2, duration/2, sample_rate, 0.2)
    
    # 组合音符
    sound = np.concatenate([note1, note2])
    return sound

def create_invalid_sound(duration=0.3, sample_rate=44100):
    """创建无效移动音效"""
    # 使用下降的音阶
    freqs = [note_to_freq('E4'), note_to_freq('D4'), note_to_freq('C4')]
    sound = np.array([])
    
    for freq in freqs:
        note = create_note(freq, duration/3, sample_rate, 0.2)
        sound = np.append(sound, note)
    
    return sound

def create_undo_sound(duration=0.3, sample_rate=44100):
    """创建撤销音效"""
    # 使用上升的音阶
    freqs = [note_to_freq('C4'), note_to_freq('D4'), note_to_freq('E4')]
    sound = np.array([])
    
    for freq in freqs:
        note = create_note(freq, duration/3, sample_rate, 0.2)
        sound = np.append(sound, note)
    
    return sound

def create_meditative_music(duration=60, sample_rate=44100):
    """创建冥想风格的背景音乐"""
    # 使用五声音阶
    pentatonic = ['C4', 'D4', 'E4', 'G4', 'A4']
    freqs = [note_to_freq(note) for note in pentatonic]
    
    music = np.array([])
    note_duration = 4.0
    
    for _ in range(int(duration // (note_duration * len(freqs)))):
        for freq in freqs:
            # 创建长音
            note = create_note(freq, note_duration, sample_rate, 0.2)
            # 添加渐变效果
            fade = np.linspace(0, 1, len(note))
            note = note * fade
            music = np.append(music, note)
    
    return music

def create_epic_music(duration=60, sample_rate=44100):
    """创建史诗风格的背景音乐"""
    # 使用大调和弦进行
    chord_progression = [
        ['C4', 'E4', 'G4', 'B4'],  # Cmaj7
        ['F4', 'A4', 'C5', 'E5'],  # Fmaj7
        ['G4', 'B4', 'D5', 'F5'],  # G7
        ['C5', 'E5', 'G5', 'B5']   # Cmaj7 (高八度)
    ]
    
    chord_freqs = [[note_to_freq(note) for note in chord] for chord in chord_progression]
    
    music = np.array([])
    chord_duration = 2.0
    
    for _ in range(int(duration // (chord_duration * len(chord_progression)))):
        for chord in chord_freqs:
            # 创建和弦
            chord_wave = create_chord(chord, chord_duration, sample_rate, 0.3)
            # 添加低音
            bass = create_note(chord[0]/2, chord_duration, sample_rate, 0.4)
            # 添加高音旋律
            melody = create_note(chord[-1]*2, chord_duration, sample_rate, 0.2)
            
            combined = chord_wave + bass + melody
            music = np.append(music, combined)
    
    return music

def create_jazz_music(duration=60, sample_rate=44100):
    """创建爵士风格的背景音乐"""
    # 使用爵士和弦进行
    chord_progression = [
        ['C4', 'E4', 'G4', 'Bb4'],  # C7
        ['F4', 'A4', 'C5', 'Eb5'],  # Fm7
        ['G4', 'B4', 'D5', 'F5'],   # G7
        ['Ab4', 'C5', 'Eb5', 'Gb5'] # Abmaj7
    ]
    
    chord_freqs = [[note_to_freq(note) for note in chord] for chord in chord_progression]
    
    music = np.array([])
    chord_duration = 2.0
    
    for _ in range(int(duration // (chord_duration * len(chord_progression)))):
        for chord in chord_freqs:
            # 创建和弦
            chord_wave = create_chord(chord, chord_duration, sample_rate, 0.25)
            # 添加摇摆节奏
            t = np.linspace(0, chord_duration, int(sample_rate * chord_duration))
            swing = np.sin(2 * np.pi * 2 * t) * 0.1
            chord_wave = chord_wave * (1 + swing)
            
            # 添加即兴旋律
            melody_freq = chord[0] * 2
            melody = create_note(melody_freq, chord_duration/4, sample_rate, 0.2)
            melody = np.tile(melody, 4)
            
            combined = chord_wave + melody[:len(chord_wave)]
            music = np.append(music, combined)
    
    return music

def save_wave(data, filename, sample_rate=44100):
    """保存音频文件"""
    # 归一化
    normalized = np.int16(data * 32767)
    wavfile.write(filename, sample_rate, normalized)

def main():
    # 创建音乐目录
    sounds_dir = os.path.join('assets', 'sounds')
    os.makedirs(sounds_dir, exist_ok=True)
    
    print("生成平静的背景音乐...")
    peaceful = create_peaceful_music()
    save_wave(peaceful, os.path.join(sounds_dir, 'background_peaceful.wav'))
    
    print("生成充满活力的背景音乐...")
    energetic = create_energetic_music()
    save_wave(energetic, os.path.join(sounds_dir, 'background_energetic.wav'))
    
    print("生成神秘的背景音乐...")
    mysterious = create_mysterious_music()
    save_wave(mysterious, os.path.join(sounds_dir, 'background_mysterious.wav'))
    
    print("生成冥想风格的背景音乐...")
    meditative = create_meditative_music()
    save_wave(meditative, os.path.join(sounds_dir, 'background_meditative.wav'))
    
    print("生成史诗风格的背景音乐...")
    epic = create_epic_music()
    save_wave(epic, os.path.join(sounds_dir, 'background_epic.wav'))
    
    print("生成爵士风格的背景音乐...")
    jazz = create_jazz_music()
    save_wave(jazz, os.path.join(sounds_dir, 'background_jazz.wav'))
    
    print("生成胜利音乐...")
    victory = create_victory_music()
    save_wave(victory, os.path.join(sounds_dir, 'victory.wav'))
    
    print("生成落子音效...")
    place = create_place_sound()
    save_wave(place, os.path.join(sounds_dir, 'place.wav'))
    
    print("生成无效移动音效...")
    invalid = create_invalid_sound()
    save_wave(invalid, os.path.join(sounds_dir, 'invalid.wav'))
    
    print("生成撤销音效...")
    undo = create_undo_sound()
    save_wave(undo, os.path.join(sounds_dir, 'undo.wav'))

if __name__ == '__main__':
    main() 