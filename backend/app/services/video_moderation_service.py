from app.ai.vision.video_frames import extract_frames
from app.ai.vision.nsfw import analyze_image

def moderate_video(video_path: str) -> bool:
    frames = extract_frames(video_path)
    for frame in frames:
        if analyze_image(frame):
            return False

    return True
