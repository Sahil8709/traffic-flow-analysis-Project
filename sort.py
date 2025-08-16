# sort.py — Pure Python SORT Tracker
import numpy as np
from collections import deque
from scipy.optimize import linear_sum_assignment

class KalmanBoxTracker:
    count = 0

    def __init__(self, bbox):
        self.bbox = bbox
        self.id = KalmanBoxTracker.count
        KalmanBoxTracker.count += 1
        self.hits = 0
        self.no_losses = 0
        self.trace = deque(maxlen=20)

    def update(self, bbox):
        self.bbox = bbox
        self.hits += 1
        self.trace.append(bbox)

class Sort:
    def __init__(self, max_age=20, min_hits=3, iou_threshold=0.3):
        self.trackers = []
        self.frame_count = 0
        self.max_age = max_age
        self.min_hits = min_hits
        self.iou_threshold = iou_threshold

    def update(self, dets):
        self.frame_count += 1
        updated_trackers = []

        for trk in self.trackers:
            trk.no_losses += 1

        for det in dets:
            matched = False
            for trk in self.trackers:
                iou_score = self.iou(det, trk.bbox)
                if iou_score > self.iou_threshold:
                    trk.update(det)
                    trk.no_losses = 0
                    matched = True
                    break
            if not matched:
                new_trk = KalmanBoxTracker(det)
                self.trackers.append(new_trk)

        self.trackers = [t for t in self.trackers if t.no_losses <= self.max_age]

        results = []
        for trk in self.trackers:
            if trk.hits >= self.min_hits:
                x1, y1, x2, y2 = trk.bbox
                results.append([x1, y1, x2, y2, trk.id])
        return np.array(results)

    def iou(self, bb_test, bb_gt):
        xx1 = max(bb_test[0], bb_gt[0])
        yy1 = max(bb_test[1], bb_gt[1])
        xx2 = min(bb_test[2], bb_gt[2])
        yy2 = min(bb_test[3], bb_gt[3])
        w = max(0., xx2 - xx1)
        h = max(0., yy2 - yy1)
        wh = w * h
        o = wh / ((bb_test[2] - bb_test[0]) * (bb_test[3] - bb_test[1])
                  + (bb_gt[2] - bb_gt[0]) * (bb_gt[3] - bb_gt[1]) - wh)
        return o