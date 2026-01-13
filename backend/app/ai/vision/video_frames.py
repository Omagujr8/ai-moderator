try:
    from moviepy import VideoFileClip

    def extract_frames(video_path: str, interval: int = 2):
        clip = VideoFileClip(video_path)
        frames = []

        for t in range(0, int(clip.duration), interval):
            frame = clip.get_frame(t)
            frames.append(frame)

        clip.close()
        return frames
except Exception:
    # Fallback stub for environments without moviepy
    def extract_frames(video_path: str, interval: int = 2):
        return []

