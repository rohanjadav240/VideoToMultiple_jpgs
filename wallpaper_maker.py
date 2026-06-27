"""
WallpaperMaker — Extract high-resolution wallpapers from any video file.

Reads a video frame-by-frame, samples every Nth frame, upscales it to
the target resolution, and saves the result as a JPEG wallpaper.

Usage:
    python wallpaper_maker.py video.mp4
    python wallpaper_maker.py video.mp4 --resolution 2560x1440 --interval 60 --quality 95
"""

import argparse
import os
import sys

import cv2


def parse_resolution(value: str) -> tuple[int, int]:
    """Parse a 'WIDTHxHEIGHT' string into (width, height)."""
    try:
        w, h = value.lower().split("x")
        return int(w), int(h)
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError(
            f"Invalid resolution '{value}'. Use WIDTHxHEIGHT format, e.g. 3840x2160"
        )


def extract_wallpapers(
    video_path: str,
    output_dir: str = "wallpapers",
    resolution: tuple[int, int] = (3840, 2160),
    interval: int = 30,
    quality: int = 90,
) -> int:
    """
    Extract wallpapers from a video file.

    Args:
        video_path:  Path to the source video.
        output_dir:  Directory where wallpapers will be saved.
        resolution:  Target (width, height) for the output images.
        interval:    Save one frame every *interval* frames.
        quality:     JPEG quality (1–100).

    Returns:
        The number of wallpapers saved.
    """
    if not os.path.isfile(video_path):
        print(f"Error: Video file not found — {video_path}")
        sys.exit(1)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video — {video_path}")
        sys.exit(1)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = total_frames / fps if fps else 0

    print(f"Video  : {video_path}")
    print(f"Frames : {total_frames}  |  FPS: {fps:.1f}  |  Duration: {duration:.1f}s")
    print(f"Output : {output_dir}/  @  {resolution[0]}×{resolution[1]}  (every {interval} frames)")
    print()

    os.makedirs(output_dir, exist_ok=True)

    saved = 0
    frame_no = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_no % interval == 0:
            frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_LANCZOS4)
            filename = os.path.join(output_dir, f"wp_{saved:04d}.jpg")
            cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, quality])
            saved += 1
            print(f"\r  Saved {saved} wallpapers …", end="", flush=True)

        frame_no += 1

    cap.release()
    print(f"\r  Saved {saved} wallpapers.       ")
    return saved


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Extract high-resolution wallpapers from a video file.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python wallpaper_maker.py video.mp4\n"
               "  python wallpaper_maker.py video.mp4 -r 2560x1440 -i 60 -q 95\n"
               "  python wallpaper_maker.py video.mp4 -o my_walls --interval 15",
    )
    parser.add_argument("video", help="Path to the source video file")
    parser.add_argument(
        "-o", "--output",
        default="wallpapers",
        help="Output directory (default: wallpapers)",
    )
    parser.add_argument(
        "-r", "--resolution",
        type=parse_resolution,
        default="3840x2160",
        help="Target resolution as WIDTHxHEIGHT (default: 3840x2160)",
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=30,
        help="Extract one frame every N frames (default: 30)",
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=90,
        help="JPEG quality 1–100 (default: 90)",
    )

    args = parser.parse_args()

    extract_wallpapers(
        video_path=args.video,
        output_dir=args.output,
        resolution=args.resolution,
        interval=args.interval,
        quality=args.quality,
    )


if __name__ == "__main__":
    main()
