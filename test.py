from ultralytics import YOLO

model = YOLO("defect_8.pt")

model.predict(
    source = 0,  # video file
    show=True,       
    save=True,      
    conf=0.5
)
