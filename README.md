# 🚦 Traffic Flow Analysis Using YOLOv8 and SORT

This project analyzes traffic flow by detecting, tracking, and counting vehicles across three distinct lanes in a video. It uses YOLOv8 for object detection and a pure Python implementation of SORT for multi-object tracking. The system overlays lane boundaries and live vehicle counts on the video, exports detailed results to CSV, and visualizes traffic flow over time.

---

## 🎯 Objective

To develop a Python-based traffic analysis system that:
- Detects vehicles using a pre-trained COCO model
- Tracks vehicles across frames to avoid duplicate counts
- Counts vehicles per lane in real time
- Exports results to CSV and annotated video
- Visualizes lane-wise traffic flow over time

---

## 🧰 Technologies Used

- **YOLOv8** – Object detection (Ultralytics)
- **SORT** – Multi-object tracking (pure Python)
- **OpenCV** – Video processing and drawing
- **NumPy** – Array operations
- **Matplotlib & Pandas** – Data visualization
- **Python** – Core scripting language

---

## 📁 Project Structure
traffic-flow-analysis/
├── detect_vehicles.py          # Main detection and lane-wise counting script
├── sort.py                     # Pure Python SORT tracker for multi-object tracking
├── visualize_counts.py         # Script to visualize lane-wise traffic flow from CSV
├── traffic_video.mp4           # Input traffic video
├── output.avi                  # Annotated output video with overlays
├── lane_counts.csv             # Frame-wise vehicle count data per lane
├── lane_counts_plot.png        # Line chart showing traffic flow per lane
├── README.md                   # Project documentation and setup instructions
└── requirements.txt            # Python dependencies list
*   vehicle_log.csv             # Displayed Vehicle ID, Lane number, Frame count, Timestamp
*   lane_selector.py            # To seclect polygon coordinates from frame.



📄 Technical Summary
This project uses YOLOv8 for vehicle detection and a custom Python implementation of SORT for tracking. Vehicles are assigned unique IDs and counted only once per lane using polygon-based lane mapping. The system processes video in near real-time, overlays visual annotations, and exports results to CSV for analysis. A Matplotlib chart visualizes traffic flow over time.
Challenges included installing sort-tracker, which failed due to C++ build issues. This was resolved by implementing SORT manually in Python. The system is modular, efficient, and ready for deployment or further enhancement.


#System Architecture

Video Input → YOLOv8 Detection → SORT Tracking → Lane Mapping → Counting → CSV Export → Visualization



# video can not be uploaded to git because it is exceeeding maximum limit of 100 mb.