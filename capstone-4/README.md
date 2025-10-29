# Vehicle Detection using YOLOv8

A deep learning project using **YOLOv8s** to detect and count **buses**, **cars**, and **vans** from images. Trained in **Google Colab** with data from **Roboflow Universe**, the resulting model (`best_vehicle_detector.pt`) powers an interactive **Streamlit web app** for real-time vehicle detection.

## Deployment

-   **Streamlit App Repository:** [https://github.com/hanskym/streamlit-vehicle-detection](https://github.com/hanskym/streamlit-vehicle-detection)
-   **Live App:** [https://vehicle-detection-hsky.streamlit.app](https://vehicle-detection-hsky.streamlit.app)

The **Streamlit App Repository** contains deployment files for the web application.

## Dataset

The dataset for the **vehicle detection** task was retrieved from **Roboflow Universe** using the **Roboflow API** in Google Colab.

-   **Dataset Source:** [Roboflow Universe – Vehicle Detection](https://universe.roboflow.com/personal-project-kej16/vehicle-detection-vznzd-dkl8g)
-   **Total Images:** ~9,000
-   **Classes:** 3 classes (bus, car, van)
-   **Annotation Format:** YOLO (\*.txt)
-   **Image Format:** JPG/JPEG

## Environment Setup

Before running the notebook in **Google Colab**, set your Roboflow API key in the environment:

```bash
# --- Roboflow API Key ---
# API key for accessing the dataset from Roboflow
ROBOFLOW_API_KEY=""
```
