import os
import whisper
from datetime import timedelta
from tqdm import tqdm
from deep_translator import GoogleTranslator, LingueeTranslator, PonsTranslator

def format_timestamp(seconds):
    """将秒数转换为 SRT 时间戳格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def create_srt_content(segments):
    """生成 SRT 格式的字幕内容"""
    srt_content = ""
    for i, segment in enumerate(segments, 1):
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        
        srt_content += f"{i}\n"
        srt_content += f"{start_time} --> {end_time}\n"
        srt_content += f"{text}\n\n"
    
    return srt_content

def map_language_code(code):
    """将Whisper语言代码映射到翻译引擎支持的语言代码"""
    language_map = {
        'nn': 'no',  # 挪威语
        'ja': 'ja',  # 日语
        'en': 'en',  # 英语
        'zh': 'zh-CN',  # 中文
        # 添加更多语言映射...
    }
    return language_map.get(code, 'auto')

def translate_text(text, source_lang='auto', target_lang='zh'):
    """使用多种翻译引擎尝试翻译文本"""
    # 映射语言代码
    mapped_source_lang = map_language_code(source_lang)
    
    # 尝试使用不同的翻译引擎
    translators = [
        # 首先尝试 Google 翻译 (最稳定)
        lambda: GoogleTranslator(source=mapped_source_lang, target='zh-CN').translate(text),
        # 尝试使用 Linguee (不需要API密钥)
        lambda: LingueeTranslator(source=mapped_source_lang if mapped_source_lang in ['en', 'de', 'fr', 'es'] else 'en', target='zh-CN').translate(text),
        # 尝试使用 Pons (不需要API密钥)
        lambda: PonsTranslator(source=mapped_source_lang if mapped_source_lang in ['en', 'de', 'fr', 'es'] else 'en', target='zh-CN').translate(text)
    ]
    
    # 依次尝试每个翻译引擎
    for translator_func in translators:
        try:
            result = translator_func()
            if result:
                print(f"翻译成功: {text[:30]}... -> {result[:30]}...")
                return result
        except Exception as e:
            print(f"翻译引擎失败: {str(e)}")
            continue
    
    # 如果所有翻译引擎都失败，返回原文
    print(f"所有翻译引擎都失败，保留原文: {text[:30]}...")
    return text

def generate_subtitle(video_path):
    """生成字幕文件"""
    try:
        print(f"\n正在处理视频字幕: {os.path.basename(video_path)}")
        
        # 加载 Whisper 模型（首次运行会下载模型）
        print("加载语音识别模型...")
        model = whisper.load_model("medium")
        
        # 识别视频语音
        print("正在识别视频语音...")
        result = model.transcribe(video_path)
        
        # 检测语言，如果不是中文则翻译
        if result["language"] != "zh":
            print(f"检测到语言: {result['language']}, 正在翻译为中文...")
            
            # 翻译每个片段
            for segment in result["segments"]:
                try:
                    translated = translate_text(segment["text"], 
                                              source_lang=result["language"], 
                                              target_lang='zh')
                    if translated:
                        segment["text"] = translated
                except Exception as e:
                    print(f"翻译片段失败，保留原文: {str(e)}")
        
        # 生成 SRT 文件
        srt_content = create_srt_content(result["segments"])
        
        # 保存 SRT 文件
        base_name = os.path.splitext(video_path)[0]
        srt_path = f"{base_name}.srt"
        
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write(srt_content)
        
        print(f"字幕文件已保存: {srt_path}")
        return True
        
    except Exception as e:
        print(f"生成字幕失败: {str(e)}")
        return False

def is_video_file(filename):
    """检查是否为视频文件"""
    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')
    return filename.lower().endswith(video_extensions)

def process_directory(directory):
    """处理目录下的所有视频文件"""
    print("\n开始处理视频字幕...")
    
    # 首先统计视频文件总数
    video_files = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if is_video_file(filename):
                video_path = os.path.join(root, filename)
                video_files.append(video_path)
    
    total_videos = len(video_files)
    if total_videos == 0:
        print("未找到任何视频文件")
        return
    
    print(f"共找到 {total_videos} 个视频文件")
    
    # 使用tqdm创建进度条
    for video_path in tqdm(video_files, desc="处理进度"):
        generate_subtitle(video_path)

def main():
    # 获取用户输入的目录路径
    directory = input("请输入要处理的视频文件目录路径: ")
    
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print("错误：指定的目录不存在")
        return
    
    # 处理视频文件
    process_directory(directory)
    print("\n处理完成！")

if __name__ == '__main__':
    main()