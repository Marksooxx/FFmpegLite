# 用于调用ffmpeg的工具
# v1.0.0

import os
import subprocess

# 这里修改想要的参数
# ["-c:a", "copy"] 复制音频流
# ["-ac", "2"] 声道
# ["-ar", "44100"] 采样率 sample_rate
# ["-b:a", "192k"] 比特率 bit_rate
# ["-c:a", "pcm_s16le"] 位深率 bite_deapth 参数：16 24 32
# ["-sample_fmt", "s24"] 改变成指定位深 ffmpeg自行决定codec
# ["-af", "volume=-3dB"] 调整音量，-3dB表示降低3分贝

# ["-af", "loudnorm=I=-16:TP=-1.5:LRA=11"] 音频标准化，设置目标响度-16 LUFS，真峰值-1.5 dBTP，响度范围11 LU
# -如果未指定 lra 参数，它会使用默认值 7.0 LU (Loudness Units)。
# -响度范围（LRA）衡量的是一段时间内音频响度的变化量。指定一个较低的 LRA 值会使得音频的动态范围更小，
# -即最响和最安静部分之间的差异更小。反之，较高的 LRA 值则允许更大的动态范围。
# -因此，如果不指定 lra，FFmpeg 会尝试将音频的响度范围调整到 7.0 LU。这个值是一个比较通用的设定，
# -但具体效果是否符合您的预期，可能还需要根据您的音频内容和最终的听感来判断。

# ["-af", "highpass=f=200:q=1"] 高通滤波器，去除200Hz以下的低频，Q值为1
# ["-af", "lowpass=f=3000:q=1"] 低通滤波器，去除3000Hz以上的高频，Q值为1
# ["-af", "equalizer=f=1000:width_type=h:width=200:g=-10"] 均衡器，在1000Hz处降低10dB
# ["-af", "compand=attacks=0.05:decays=0.5:points=-80/-80|-45/-45|-27/-25|0/-10:soft-knee=6"] 动态范围压缩
# ["-af", "silenceremove=start_periods=1:start_duration=1:start_threshold=-50dB:detection=peak"] 去除静音段

FFMPEG_OPTS = ["-c:a", "pcm_s24le"]

# ANSI 颜色代码
class Colors:
    GREEN = '\033[37;42;1m'
    RED = '\033[37;41;1m'
    RESET = '\033[0m'

# 支持的音频后缀
EXTS = {".wav", ".mp3", ".flac", ".aac", ".m4a", ".ogg"}

for fn in os.listdir("."):
    name, ext = os.path.splitext(fn)
    if ext.lower() in EXTS:
        tmp = f"{name}_tmp{ext}"
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", fn,] + FFMPEG_OPTS + [tmp]
        print("→ 运行", " ".join(cmd))
        if subprocess.call(cmd) == 0:
            os.replace(tmp, fn)
            print(f"{Colors.GREEN}√ 処理成功：{Colors.RESET}{Colors.GREEN}{fn}{Colors.RESET}")
            print()
        else:
            print(f"{Colors.RED}× 処理失敗：{Colors.RESET}{Colors.RED}{fn}{Colors.RESET}")
            print()