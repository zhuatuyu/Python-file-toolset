import os
import cv2
import glob

def clean_screenshots(directory):
    """清理目录下的所有图片文件"""
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    for ext in image_extensions:
        files = glob.glob(os.path.join(directory, ext))
        for file in files:
            try:
                os.remove(file)
                print(f"已删除: {file}")
            except Exception as e:
                print(f"删除文件失败 {file}: {str(e)}")

def get_video_duration(video_path):
    """获取视频时长（秒）"""
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        # 获取视频总帧数和帧率
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        
        # 释放视频对象
        cap.release()
        
        # 计算视频时长（秒）
        duration = total_frames / fps
        return duration
    except Exception as e:
        print(f"获取视频时长失败 {video_path}: {str(e)}")
        return None

def capture_screenshots(video_path, output_dir):
    """在视频四等分点位置截取图片，并排除片头片尾各5%的时长"""
    try:
        duration = get_video_duration(video_path)
        if not duration:
            return False

        # 计算有效时长（去除首尾各5%）
        margin = duration * 0.05  # 5%的时长
        effective_duration = duration - (2 * margin)  # 去除首尾后的有效时长
        segment = effective_duration / 4  # 每段时长

        # 计算四个截图时间点（加上起始的margin）
        capture_times = [
            margin + (segment * 1),  # 第一个25%位置
            margin + (segment * 2),  # 第二个50%位置
            margin + (segment * 3),  # 第三个75%位置
            margin + (segment * 4)   # 第四个100%位置
        ]

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False

        # 获取视频文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(video_path))[0]

        # 截取四张图片
        for i, time_point in enumerate(capture_times, 1):
            # 设置视频位置
            cap.set(cv2.CAP_PROP_POS_MSEC, time_point * 1000)
            
            # 读取帧
            ret, frame = cap.read()
            if ret:
                # 构建输出文件名
                output_path = os.path.join(output_dir, f"{base_name}_screenshot_{i}.jpg")
                # 保存图片
                cv2.imwrite(output_path, frame)
                print(f"已保存截图 {i}/4: {output_path} (在 {int(time_point/60)}分{int(time_point%60)}秒)")
            else:
                print(f"截取第 {i} 张图片失败")

        cap.release()
        return True
    except Exception as e:
        print(f"截图失败 {video_path}: {str(e)}")
        return False

def is_video_file(filename):
    """检查是否为视频文件"""
    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')
    return filename.lower().endswith(video_extensions)

def process_directory(directory):
    """处理目录下的所有视频文件"""
    # 首先清理已有的截图
    print("\n清理已有截图...")
    clean_screenshots(directory)

    # 处理视频文件
    print("\n开始处理视频文件...")
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if is_video_file(filename):
                video_path = os.path.join(root, filename)
                print(f"\n处理视频: {filename}")
                capture_screenshots(video_path, root)

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