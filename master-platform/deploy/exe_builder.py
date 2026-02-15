"""Desktop Executable Builder
Build .exe (Windows), .dmg (macOS), and .AppImage (Linux) from web apps.
Author: Audrey Evans
"""
import subprocess
from pathlib import Path

class DesktopExecutableBuilder:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def build_windows_exe(self):
        """Build Windows .exe using Electron Builder."""
        print("Building Windows .exe...")
        subprocess.run([
            "npm", "run", "build:win"
        ], cwd=self.project_path, check=True)
        print("Windows .exe built successfully!")
    
    def build_macos_dmg(self):
        """Build macOS .dmg using Electron Builder."""
        print("Building macOS .dmg...")
        subprocess.run([
            "npm", "run", "build:mac"
        ], cwd=self.project_path, check=True)
        print("macOS .dmg built successfully!")
    
    def build_linux_appimage(self):
        """Build Linux .AppImage using Electron Builder."""
        print("Building Linux .AppImage...")
        subprocess.run([
            "npm", "run", "build:linux"
        ], cwd=self.project_path, check=True)
        print("Linux .AppImage built successfully!")
    
    def build_all(self):
        """Build for all platforms."""
        self.build_windows_exe()
        self.build_macos_dmg()
        self.build_linux_appimage()

if __name__ == "__main__":
    builder = DesktopExecutableBuilder("/path/to/project")
    builder.build_all()
