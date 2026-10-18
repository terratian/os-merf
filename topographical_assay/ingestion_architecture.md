# OS-MERF System Architecture: Open-Source Citizen-Science Data Ingestion App
# Protected under GNU GPL v3 | Copyright (C) 2026 Joshua Sultan (terratian)

## I. System Overview & Edge Client Ingestion
To bypass institutional gatekeeping, the ingestion app operates as a decentralized client node that handles local spatial processing on consumer mobile hardware (e.g., Crostini/Linux local nodes, Android/iOS edge devices) prior to database syncing.

1. Edge Client Capture: Multi-Angle Photogrammetry / Mobile LiDAR (.e57 format)
2. Integrity Check: Metadata verification loop (EXIF/GPS tamper audit checks)
3. Processing Engine: Automatic filtration via OpenCV Laplacian variance metrics
4. Storage Layer: Hashed asset indexing via decentralized IPFS distribution nodes
5. State Registry: Permanent, immutable coordination logging via a public global ledger

---

## II. Data Payload & Telemetry Structure
Every crowdsourced field submission must bundle spatial, geographical, and hardware sensor telemetry into a single unified JSON metadata schema prior to blockchain/IPFS submission:

```json
{
  "submission_metadata": {
    "node_public_key": "ed25519_pubkey_bytes_here",
    "timestamp_utc": "2026-10-18T06:27:00Z",
    "client_software_version": "v1.0.4-beta"
  },
  "geospatial_telemetry": {
    "coordinate_latitude": -13.5079,
    "coordinate_longitude": -71.9822,
    "elevation_ellipsoidal_meters": 3701.4,
    "gps_hardware_precision_index_hdop": 0.85
  },
  "hardware_sensor_array": {
    "capture_device_model": "iPhone 16 Pro / Custom iPad LiDAR Array",
    "sensor_type": "Solid-State LiDAR Time-of-Flight / CMOS raw photogrammetry",
    "exif_tamper_signature_valid": true
  },
  "payload_manifest": {
    "spatial_point_cloud_hash_sha256": "8f3a9e...e7b2",
    "raw_mesh_format": ".e57",
    "total_vertices_count": 8459200
  }
}
```

---

## III. Automated Pipeline & Counter-Poisoning Protocols
To insulate the database against malicious institutional poisoning, targeted data scrubbing, or fake generation arrays, the backend orchestration engine subjects every payload to three sequential verification states:

### 1. Cryptographic and Metadata Sanitization
* EXIF Tamper Check: Compares internal frame sensor data arrays with absolute system clock arrays. Any mismatch between device file compilation and upload timestamps flags the package.
* Hardware Profile Matching: Correlates the depth map matrix arrays against known solid-state hardware noise profiles. Fake or procedurally generated synthetic point clouds will lack real-world optical noise vectors.

### 2. Edge-Dissonance Processing (joint_classifier.py Linkage)
* The automated system pipes the raw .e57 spatial point cloud or imagery array directly through our local JointClassifier script.
* Filter Rule: If polygonal_vertex_complexity records standard rectangular values (<= 12), yet the user manually categorizes the asset as a "megalithic 3D interlocking matrix," the entry is auto-triangulated down to lower-priority human validation queues.

### 3. Decentralized Database Ledger Sync
* Validated entries bypass traditional server databases. The structural coordinates and spatial meshes are hashed and committed to IPFS (InterPlanetary File System).
* The immutable IPFS pointer addresses are logged onto a publicly auditable ledger, ensuring the physical spatial records can never be erased, modified, or hidden by central authorities.
