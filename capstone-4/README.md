## Capstone 4 Deployment

Proyek **Capstone 4** telah berhasil dideploy menggunakan **Streamlit Cloud**.

-   **Repository (Streamlit App):** [https://github.com/hanskym/streamlit-vehicle-detection](https://github.com/hanskym/streamlit-vehicle-detection)
-   **Aplikasi Live:** [https://vehicle-detection-hsky.streamlit.app](https://vehicle-detection-hsky.streamlit.app)

Repository ini berisi `notebook.ipynb` yang dijalankan menggunakan **Google Colab** untuk menghasilkan output **model detection** (`best_vehicle_detector.pt`), yang kemudian digunakan oleh aplikasi **Streamlit** yang dihosting pada repository Streamlit App.

## Dataset

Dataset digunakan untuk **vehicle detection** dan diambil melalui **Roboflow API** di Google Colab.

-   **Sumber Dataset:** [Roboflow Universe – Vehicle Detection](https://universe.roboflow.com/personal-project-kej16/vehicle-detection-vznzd-dkl8g)
-   **Total Gambar:** ~9,000
-   **Kelas:** Berbagai jenis kendaraan
-   **Format Anotasi:** YOLO (`*.txt`)
-   **Format Gambar:** JPG/JPEG

### Struktur Dataset

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

### Contoh Pengambilan Dataset di Google Colab

```python
from roboflow import Roboflow

# ⚠️ Ganti dengan API Key Anda
ROBOFLOW_API_KEY = userdata.get('ROBOFLOW_API_KEY')

rf = Roboflow(api_key=ROBOFLOW_API_KEY)
project = rf.workspace("personal-project-kej16").project("vehicle-detection-vznzd-dkl8g")
dataset = project.version(1).download("yolov8")

DATASET_PATH = dataset.location
print(f"✓ Dataset berhasil didownload! Lokasi: {DATASET_PATH}")
```

Dataset ini digunakan di notebook Colab untuk melatih model YOLO dan menghasilkan file model `best_vehicle_detector.pt` yang selanjutnya digunakan oleh aplikasi Streamlit.
