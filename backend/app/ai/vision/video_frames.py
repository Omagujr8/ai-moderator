from moviepy import VideoFileClip

def extract_frames(video_path: str, interval: int = 2):
    clip = VideoFileClip(video_path)
    frames = []

    for t in range(0, (clip.duration), interval):
        frame = clip.get_frame(t)
        frames.append(frame)

    clip.close()
    return frames

