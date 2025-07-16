import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def run_streamlit_app():
    """Run the Streamlit application"""
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=localhost"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    print("🚀 Starting GCash Cash-In Application...")
    print("📦 Installing requirements...")
    
    if install_requirements():
        print("🌐 Starting web application...")
        print("📱 Open your browser and go to: http://localhost:8501")
        print("⏹️  Press Ctrl+C to stop the application")
        run_streamlit_app()
    else:
        print("❌ Failed to install requirements. Please check your Python environment.")

if __name__ == "__main__":
    main()
