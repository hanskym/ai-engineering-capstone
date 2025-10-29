# Vehicle Detection Dataset

This dataset is sourced from [Roboflow Universe](https://universe.roboflow.com/personal-project-kej16/vehicle-detection-vznzd-dkl8g) and contains approximately 9,000 items for vehicle detection tasks.

## Dataset Structure

```
dataset/
├── train/
│   ├── images/         # Training images
│   └── labels/         # YOLO format annotations for training
├── valid/
│   ├── images/         # Validation images
│   └── labels/         # YOLO format annotations for validation
└── test/
    ├── images/         # Test images
    └── labels/         # YOLO format annotations for test
```

## Dataset Information

-   **Total Images**: ~9,000
-   **Classes**: Various vehicle types
-   **Annotation Format**: YOLO format (\*.txt files)
-   **Image Format**: JPG/JPEG

## Note

Due to the large size of the dataset (9,000 items), it is not included in the Git repository. Please download it directly from the [Roboflow Universe](https://universe.roboflow.com/personal-project-kej16/vehicle-detection-vznzd-dkl8g).

## Dataset Usage

1. Download the dataset from Roboflow Universe
2. Extract the files into this directory
3. The dataset is ready to be used for training your vehicle detection model
