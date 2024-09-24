# Media Conversion Script

This Python script recursively converts images and videos from an input folder to optimized WebP images and GIFs in an output folder. The script uses multiprocessing to process multiple files in parallel, ensuring efficient conversion.

## Features
- Converts image files (`.png`, `.jpg`, `.jpeg`) to WebP format.
- Converts video files (`.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, `.wmv`) to GIF format.
- Allows specifying a target size for images and videos to control the output file size.
- Automatically adjusts WebP quality and GIF frame rate to meet the size requirements.
- Supports batch processing of files using multiprocessing.

## Requirements

To run the script, you'll need the following Python packages:

- `Pillow` (Python Imaging Library)
- `moviepy`
- `imageio`

You can install the required packages using:

```bash
pip install Pillow moviepy imageio
```

## Usage

1. Place the image and video files you want to convert in the `img` folder (or another folder of your choice).
2. Run the script:

```bash
python media.py
```

By default, the script converts files from the `img` directory and saves the converted files in the `converted_img` directory. You can modify the input/output paths and target sizes.

### Example:

```bash
python media.py
```

This will:
- Convert all `.png`, `.jpg`, and `.jpeg` files to WebP format with a target size of 100KB.
- Convert all `.mp4`, `.avi`, `.mov`, `.mkv`, `.flv`, and `.wmv` files to GIF format with a target size of 1000KB.

## Parameters

You can customize the conversion process by modifying the function arguments in the `convert_all()` function:

```python
convert_all(
    input_path="img",            # Input folder path
    output_path="converted_img", # Output folder path
    image_size_kb=100,           # Target image size in KB
    video_size_kb=1000           # Target video size in KB
)
```

### Function Breakdown

- **`convert_to_webp()`**: Converts images to WebP format and adjusts the quality to meet the target size.
- **`convert_video_to_gif()`**: Converts videos to GIF format, resizing the video and adjusting frame rates to meet the size limit.
- **`process_file()`**: Identifies the file type and calls the appropriate conversion function.
- **`convert_all()`**: Recursively finds all supported image and video files in the input directory and processes them using multiprocessing.

## Notes

- The script automatically creates the necessary output directories.
- Ensure that the input files are in the supported formats for conversion.

## License

This project is licensed under the MIT License.

## Acknowledgements

This script uses `Pillow` for image processing, `moviepy` for video to GIF conversion, and `imageio` for further GIF optimization.