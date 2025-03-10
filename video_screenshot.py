import os
import cv2
import glob
import numpy as np

def clean_screenshots(directory):
    """清理目录下的图片文件，保留与视频文件同名的图片"""
    # 首先获取所有视频文件名（不含扩展名）
    video_names = set()
    for root, _, files in os.walk(directory):
        for file in files:
            if is_video_file(file):
                name = os.path.splitext(file)[0]
                video_names.add(name)
    
    # 清理不在视频文件名列表中的图片
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    for root, _, _ in os.walk(directory):
        for ext in image_extensions:
            pattern = os.path.join(root, ext)
            for img_path in glob.glob(pattern):
                img_name = os.path.splitext(os.path.basename(img_path))[0]
                if img_name not in video_names:
                    try:
                        os.remove(img_path)
                        print(f"已删除: {img_path}")
                    except Exception as e:
                        print(f"删除文件失败 {img_path}: {str(e)}")

def create_grid_image(images, grid_size=(2, 2)):
    """将多张图片拼接成四宫格"""
    h, w = images[0].shape[:2]
    grid_h, grid_w = grid_size
    
    output = np.zeros((h * grid_h, w * grid_w, 3), dtype=np.uint8)
    
    for idx, image in enumerate(images):
        i = idx // grid_w
        j = idx % grid_w
        output[i * h:(i + 1) * h, j * w:(j + 1) * w] = image
    
    return output

def capture_screenshots(video_path, output_dir):
    """在视频四等分点位置截取图片，并排除片头片尾各5%的时长"""
    try:
        # 检查是否已存在同名预览图
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_path = os.path.join(output_dir, f"{base_name}.jpg")
        if os.path.exists(output_path):
            print(f"预览图已存在，跳过处理: {output_path}")
            return True

        duration = get_video_duration(video_path)
        if not duration:
            return False

        # 计算有效时长（去除首尾各5%）
        margin = duration * 0.05
        effective_duration = duration - (2 * margin)
        segment = effective_duration / 3  # 分成3段，得到4个点

        # 计算四个截图时间点
        capture_times = [margin + (segment * i) for i in range(4)]

        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False

        screenshots = []

        # 截取四张图片
        for i, time_point in enumerate(capture_times, 1):
            cap.set(cv2.CAP_PROP_POS_MSEC, time_point * 1000)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                screenshots.append(frame)
                print(f"已截取第 {i}/4 张图片 (在 {int(time_point/60)}分{int(time_point%60)}秒)")
            else:
                print(f"截取第 {i} 张图片失败")
                return False

        cap.release()

        # 创建四宫格图片
        if len(screenshots) == 4:
            grid_image = create_grid_image(screenshots, (2, 2))
            cv2.imwrite(output_path, grid_image)
            print(f"已保存四宫格预览图: {output_path}")
            return True
        return False

    except Exception as e:
        print(f"截图失败 {video_path}: {str(e)}")
        return False

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