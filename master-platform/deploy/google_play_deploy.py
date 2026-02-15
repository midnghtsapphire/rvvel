"""Google Play Store Automated Deployment
Automates APK/AAB building, signing, and upload to Google Play Console.
Author: Audrey Evans
"""
import subprocess
import os
from pathlib import Path

class GooglePlayDeployer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.keystore_path = self.project_path / "android" / "app" / "release.keystore"
    
    def build_release_bundle(self) -> str:
        """Build the Android App Bundle (.aab) for release."""
        print("Building release AAB...")
        subprocess.run([
            "./gradlew", "bundleRelease"
        ], cwd=self.project_path / "android", check=True)
        
        aab_path = self.project_path / "android/app/build/outputs/bundle/release/app-release.aab"
        return str(aab_path)
    
    def upload_to_play_console(self, aab_path: str, track: str = "internal"):
        """Upload AAB to Google Play Console using Fastlane."""
        print(f"Uploading to Play Console ({track} track)...")
        subprocess.run([
            "fastlane", "supply",
            "--aab", aab_path,
            "--track", track,
            "--json_key", os.environ.get("GOOGLE_PLAY_JSON_KEY"),
        ], check=True)
    
    def deploy(self, track: str = "internal"):
        """Full deployment pipeline."""
        aab_path = self.build_release_bundle()
        self.upload_to_play_console(aab_path, track)
        print(f"Deployment to {track} track complete!")

if __name__ == "__main__":
    deployer = GooglePlayDeployer("/path/to/project")
    deployer.deploy(track="internal")
