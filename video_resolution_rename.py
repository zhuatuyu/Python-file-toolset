import os
import cv2


def count_video_files(directory):
    # 统计目录下的视频文件总数
    total_count = 0
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if is_video_file(filename):
                total_count += 1
    return total_count

def get_video_resolution(video_path):
    try:
        # 打开视频文件
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        # 获取视频宽度和高度
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # 释放视频对象
        cap.release()
        
        # 返回分辨率
        return width, height
    except Exception as e:
        print(f"Error processing {video_path}: {str(e)}")
        return None

def get_resolution_category(width, height):
    # 获取较大的边作为判断标准
    max_dimension = max(width, height)
    
    # 判断分辨率类别
    if max_dimension <= 240:
        return '240'
    elif max_dimension <= 360:
        return '360'
    elif max_dimension <= 480:
        return '480'
    elif max_dimension <= 560:
        return '560'
    elif max_dimension <= 720:
        return '720'
    elif max_dimension <= 1080:
        return '1080'
    elif max_dimension <= 2160:
        return '2160'
    elif max_dimension <= 4320:
        return '4320'
    else:
        return None

def is_video_file(filename):
    # 视频文件扩展名列表
    video_extensions = ('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')
    return filename.lower().endswith(video_extensions)

def is_already_renamed(filename):
    # 检查文件名是否已经符合规范格式（例如：240px_filename.mp4）
    resolution_categories = ['240', '360', '480', '560', '720', '1080', '2160', '4320']
    name, ext = os.path.splitext(filename)
    for category in resolution_categories:
        if name.startswith(f"{category}px_"):
            return True
    return False

def process_videos(directory):
    # 首先统计视频文件总数
    total_videos = count_video_files(directory)
    if total_videos == 0:
        print("未找到任何视频文件")
        return

    print(f"共找到 {total_videos} 个视频文件")
    processed_count = 0
    renamed_count = 0
    skipped_count = 0
    error_count = 0

    # 遍历目录下的所有文件和子目录
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if is_video_file(filename):
                processed_count += 1
                print(f"\n正在处理第 {processed_count}/{total_videos} 个视频: {filename}")

                # 检查文件名是否已经符合规范格式
                if is_already_renamed(filename):
                    print(f"跳过 {filename}: 已经是正确格式")
                    skipped_count += 1
                    continue
                    
                file_path = os.path.join(root, filename)
                
                # 获取视频分辨率
                resolution = get_video_resolution(file_path)
                if resolution:
                    width, height = resolution
                    resolution_category = get_resolution_category(width, height)
                    
                    if resolution_category:
                        # 构建新的文件名
                        name, ext = os.path.splitext(filename)
                        new_filename = f"{resolution_category}px_{name}{ext}"
                        new_file_path = os.path.join(root, new_filename)
                        
                        # 如果新文件名不存在，则重命名
                        if not os.path.exists(new_file_path):
                            try:
                                os.rename(file_path, new_file_path)
                                print(f"已重命名: {filename} -> {new_filename}")
                                renamed_count += 1
                            except Exception as e:
                                print(f"重命名 {filename} 时出错: {str(e)}")
                                error_count += 1
                        else:
                            print(f"跳过重命名 {filename}: 目标文件已存在")
                            skipped_count += 1
                else:
                    error_count += 1

    # 显示处理完成的统计信息
    print(f"\n处理完成！统计信息：")
    print(f"总视频数: {total_videos}")
    print(f"成功重命名: {renamed_count}")
    print(f"已跳过: {skipped_count}")
    print(f"处理出错: {error_count}")

def main():
    # 获取用户输入的目录路径
    directory = input("请输入要处理的视频文件目录路径: ")
    
    # 检查目录是否存在
    if not os.path.isdir(directory):
        print("错误：指定的目录不存在")
        return
    
    # 处理视频文件
    process_videos(directory)

if __name__ == '__main__':
    main()