"""
Cart2Insights E-Commerce Analytics Platform
Run Launcher Script
"""
import os
import sys

# Ensure project root and streamlit directory are in Python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
STREAMLIT_DIR = os.path.join(ROOT_DIR, "streamlit")
APP_PATH = os.path.join(STREAMLIT_DIR, "app.py")

for p in [ROOT_DIR, STREAMLIT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

if __name__ == "__main__":
    import streamlit.web.cli as stcli
    print("==================================================")
    print("   Starting Cart2Insights Streamlit Platform...   ")
    print("==================================================")
    sys.argv = ["streamlit", "run", APP_PATH]
    sys.exit(stcli.main())
