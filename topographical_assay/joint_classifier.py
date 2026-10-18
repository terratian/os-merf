# ==============================================================================
# OS-MERF: Open-Source Megalithic & Evolutionary Research Framework
# Copyright (C) 2026 Joshua Sultan (GitHub: terratian)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MANDATORY ATTRIBUTION REQUIRED: All derivative code modifications must 
# prominently credit Joshua Sultan (terratian) as the framework architect.
# ==============================================================================
import cv2
import numpy as np

class JointClassifier:
    """
    Extracts structural edge profiles from megalithic joints using Laplacian 
    convolution matrices, Hough linear vectors, and localized contour spatial variance arrays.
    """
    def __init__(self, blur_ksize=5, canny_low=50, canny_high=150):
        self.blur_ksize = (blur_ksize, blur_ksize)
        self.canny_low = canny_low
        self.canny_high = canny_high

    def analyze_joint_matrix(self, image_path):
        """
        Processes a raw input image array, isolates structural seams, and 
        extracts the 3D interlocking complexity and edge variance threshold metrics.
        """
        # 1. Ingest target matrix in grayscale format
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return {"status": "ERROR", "reason": "Failed to read target image matrix"}

        # 2. Extract surface texture noise utilizing a Gaussian filter kernel
        blurred = cv2.GaussianBlur(img, self.blur_ksize, 0)

        # 3. Compute the second-order derivative spatial gradient using a Laplacian convolution matrix
        laplacian_matrix = cv2.Laplacian(blurred, cv2.CV_64F, ksize=3)
        global_variance_score = laplacian_matrix.var()

        # 4. Map geometric discontinuities via Canny edge isolation loops
        edges = cv2.Canny(blurred, self.canny_low, self.canny_high)

        # 5. Extract structural linear trajectories using Probabilistic Hough Transform
        lines = cv2.HoughLinesP(
            edges, 
            rho=1, 
            theta=np.pi/180, 
            threshold=50, 
            minLineLength=30, 
            maxLineGap=10
        )
        linear_segments_count = len(lines) if lines is not None else 0

        # 6. Quantify localized structural edge variances along geometric contours
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        polygonal_complexity_score = 0
        contour_variances = []
        
        for cnt in contours:
            # Measure perimeter arc length to calculate precision epsilon tolerances
            epsilon = 0.015 * cv2.arcLength(cnt, True)
            approx_polygon = cv2.approxPolyDP(cnt, epsilon, True)
            polygonal_complexity_score += len(approx_polygon)

            # Extract localized coordinate deviation metrics across individual edge points
            if len(cnt) > 5:
                # Reshape to a 2D float array to calculate coordinate distances
                points = cnt.reshape(-1, 2).astype(np.float32)
                # Compute centroid of the active segment
                centroid = np.mean(points, axis=0)
                # Calculate distances from every edge point to the local structural centroid
                distances = np.sqrt(np.sum((points - centroid) ** 2, axis=1))
                # Append standard deviation as the segment's structural edge variance
                contour_variances.append(np.std(distances))

        # Calculate mean structural variance across all extracted joint interfaces
        mean_edge_variance = np.mean(contour_variances) if contour_variances else 0.0

        # 7. Evaluate geomechanical classification matrix thresholds
        # High polygonal complexity combined with high micro-edge variance highlights 3D puzzle joints
        if polygonal_complexity_score > 12 and mean_edge_variance > 15.0:
            verdict = "Verified High-Complexity 3D Polygonal Interlocking Masonry"
        elif polygonal_complexity_score <= 12 and linear_segments_count > 0:
            verdict = "Standard Rectilinear/Coursed Masonry Matrix"
        else:
            verdict = "Indeterminate spatial parameters or heavily weathered interface face"

        return {
            "status": "PROFILED",
            "laplacian_variance_density": round(global_variance_score, 4),
            "structural_edge_variance": round(float(mean_edge_variance), 4),
            "isolated_linear_vectors": linear_segments_count,
            "polygonal_vertex_complexity": polygonal_complexity_score,
            "structural_classification": verdict
        }

if __name__ == "__main__":
    classifier = JointClassifier()
    print("OS-MERF Joint Classifier: Edge Variance Parsing Loops Active.")
