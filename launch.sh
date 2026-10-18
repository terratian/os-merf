#!/bin/bash
# ==============================================================================
# OS-MERF Automated Shell Ingestion Launcher & Context Telemetry Engine
# Protected under GNU GPL v3 | Copyright (C) 2026 Joshua Sultan (terratian)
# ==============================================================================

clear
echo "=== INITIALIZING OS-MERF ENVIRONMENT CONTEXT BIND ==="
echo ""

# 1. Sync remote master nodes and verify git timeline variables
git pull origin main
echo ""

# 2. Fire up the unified structural unit testing engine
python3 run_tests.py
echo ""

# 3. Print the text-based console homepage directly into the shell stream
if [ -f ROADMAP.md ]; then
    cat ROADMAP.md
    echo ""
fi

# 4. Programmatically isolate current git telemetry strings to output direct web links
REMOTE_URL=$(git config --get remote.origin.url)
if [[ $REMOTE_URL == git@github.com:* ]]; then
    # Parse SSH remote string structures to generate public HTTPS arrays
    HTTP_BASE="https://github.com(echo $REMOTE_URL | sed 's/git@github.com://' | sed 's/\.git//')"
else
    HTTP_BASE=$(echo $REMOTE_URL | sed 's/\.git//')
fi

echo "================================================================================"
echo " [ DIRECT ECOSYSTEM WEB LINKS FOR EXTERNAL COPY-PASTE UTILITY ]"
echo "================================================================================"
echo " * Target Code Repository Loop : ${HTTP_BASE}"
echo " * System Project Manifesto    : ${HTTP_BASE}/blob/main/README.md"
echo " * Protective Legal License    : ${HTTP_BASE}/blob/main/LICENSE"
echo " * 50-Site Geomechanical Ledger: ${HTTP_BASE}/blob/main/topographical_assay/anomalous_structures_master.md"
echo " * Open Community Guide Rules : ${HTTP_BASE}/blob/main/COMMUNITY.md"
echo "================================================================================"
echo ""
