import os
import io
from PIL import Image
from moviepy.editor import VideoFileClip
import imageio
import multiprocessing
from functools import partial


def convert_to_webp(filename, input_path, output_path, target_size_kb=100):
    try:
        input_file = os.path.join(input_path, filename)
        fname, _ = os.path.splitext(filename)
        output_file = os.path.join(output_path, f"{fname}.webp")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with Image.open(input_file) as img:
            quality = 90
            while True:
                output = io.BytesIO()
                img.save(output, "webp", quality=quality)
                if len(output.getvalue()) <= target_size_kb * 1024 or quality < 20:
                    break
                quality -= 5

            with open(output_file, "wb") as f:
                f.write(output.getvalue())

        print(
            f"Converted {filename} to WebP. Final size: {len(output.getvalue()) / 1024:.2f} KB"
        )
    except Exception as e:
        print(f"Error converting {filename}: {str(e)}")


def convert_video_to_gif(
    filename, input_path, output_path, target_size_kb=1000, fps=10
):
    try:
        input_file = os.path.join(input_path, filename)
        fname, _ = os.path.splitext(filename)
        output_file = os.path.join(output_path, f"{fname}.gif")

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with VideoFileClip(input_file) as clip:
            clip = clip.resize(height=360)  # Resize for reasonable file size
            clip.write_gif(output_file, fps=fps, opt="nq")

        # Optimize GIF size
        with Image.open(output_file) as img:
            img.save(output_file, optimize=True, quality=85)

        # Further optimize if needed
        while os.path.getsize(output_file) > target_size_kb * 1024:
            with imageio.get_reader(output_file) as reader:
                frames = [frame for frame in reader]

            frames = frames[::2]  # Remove every other frame

            if len(frames) <= 2:
                break

            imageio.mimsave(output_file, frames, fps=fps / 2)

        print(
            f"Converted {filename} to GIF. Final size: {os.path.getsize(output_file) / 1024:.2f} KB"
        )
    except Exception as e:
        print(f"Error converting {filename}: {str(e)}")


def process_file(file, input_path, output_path, image_size_kb, video_size_kb):
    rel_path = os.path.relpath(os.path.dirname(file), input_path)
    current_output_path = os.path.join(output_path, rel_path)

    if file.lower().endswith((".png", ".jpg", ".jpeg")):
        convert_to_webp(
            os.path.basename(file),
            os.path.dirname(file),
            current_output_path,
            image_size_kb,
        )
    elif file.lower().endswith((".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv")):
        convert_video_to_gif(
            os.path.basename(file),
            os.path.dirname(file),
            current_output_path,
            video_size_kb,
        )


def convert_all(
    input_path="img",
    output_path="converted_img",
    image_size_kb=100,
    video_size_kb=1000,
):
    files_to_process = []
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.lower().endswith(
                (
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".mp4",
                    ".avi",
                    ".mov",
                    ".mkv",
                    ".flv",
                    ".wmv",
                )
            ):
                files_to_process.append(os.path.join(root, file))

    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        func = partial(
            process_file,
            input_path=input_path,
            output_path=output_path,
            image_size_kb=image_size_kb,
            video_size_kb=video_size_kb,
        )
        pool.map(func, files_to_process)


if __name__ == "__main__":
    convert_all()
