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

Steps to do the projects:

1. Video Input & Preprocessing
- Load traffic video using OpenCV.
- Resize or crop if needed for consistent frame dimensions.
2. Lane Polygon Definition
- Manually define lane regions using polygon coordinates.
- Store lane polygons in a config file or directly in the script for flexibility.
3. Vehicle Detection
- Use YOLOv8 for real-time object detection.
- Filter detections to include only relevant classes (e.g., cars, trucks, buses, bikes).
4. Object Tracking
- Apply SORT (Simple Online and Realtime Tracking) to assign unique IDs to vehicles across frames.
- Maintain tracking consistency even with partial occlusions.
5. Lane Assignment
- Check if the vehicle’s centroid lies within a defined polygon using OpenCV’s pointPolygonTest.
- Assign each vehicle to a lane based on its position.
6. CSV Export
- Log each vehicle’s:
- ID
- Lane number
- Frame number
- Timestamp (calculated from FPS)
- Export logs to a structured CSV file for downstream analysis.
7. Annotated Video Output
- Overlay bounding boxes, lane polygons, and vehicle IDs on each frame.
- Save annotated video using OpenCV’s VideoWriter.
8. Video Compression
- Use FFmpeg to compress annotated video for GitHub compatibility.
- Reduce file size while preserving visual clarity.
9. GitHub Repo Management
- Add .gitignore to exclude large files and cache.
- Use git lfs or FFmpeg compression to stay under GitHub’s 100 MB limit.
- Structure repo with clear folders: src/, data/, output/, docs/.


🔍 Approach
- Combined YOLOv8 detection with SORT tracking to maintain vehicle identity across frames.
- Used polygon-based lane mapping to assign vehicles to specific lanes.
- Exported structured logs and annotated videos for reproducibility and analysis.
⚠️ Challenges
- Lane accuracy: Ensuring polygon coordinates matched real-world lanes.
- Tracking drift: SORT occasionally lost track during occlusions.
- File size limits: Annotated videos exceeded GitHub’s 100 MB limit.
- Repo clarity: Needed clean structure and documentation for open-source publishing.
✅ Solutions
- Refined polygon coordinates through visual inspection and iterative tuning.
- Tuned SORT parameters and filtered noisy detections.
- Integrated FFmpeg for efficient video compression.
- Created a clean repo structure with a professional README.md, .gitignore, and sample outputs.


📄 Technical Summary
This project uses YOLOv8 for vehicle detection and a custom Python implementation of SORT for tracking. Vehicles are assigned unique IDs and counted only once per lane using polygon-based lane mapping. The system processes video in near real-time, overlays visual annotations, and exports results to CSV for analysis. A Matplotlib chart visualizes traffic flow over time.
Challenges included installing sort-tracker, which failed due to C++ build issues. This was resolved by implementing SORT manually in Python. The system is modular, efficient, and ready for deployment or further enhancement.


#System Architecture

Video Input → YOLOv8 Detection → SORT Tracking → Lane Mapping → Counting → CSV Export → Visualization



# video can not be uploaded to git because it is exceeeding maximum limit of 100 mb but used git config --global http.postBuffer 524288000 which is used to increase Git’s buffer size for HTTP POST requests — specifically to help with pushing large files to remote repositories like GitHub and successfully uploaded files.
