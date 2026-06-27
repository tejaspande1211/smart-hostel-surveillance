import os
os.environ["TF_USE_LEGACY_KERAS"] = "0"

from deepface import DeepFace

result = DeepFace.verify(
    img1_path="data/known/Me.jpg",
    img2_path="data/unknown/JW.jpg",
    detector_backend="opencv"   # 🔥 force OpenCV
)

print(result)