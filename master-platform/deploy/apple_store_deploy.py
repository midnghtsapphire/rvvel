"""Apple App Store Automated Deployment
Automates IPA building, signing, and upload to App Store Connect.
Author: Audrey Evans
"""
import subprocess
from pathlib import Path

class AppleStoreDeployer:
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def build_archive(self) -> str:
        """Build the iOS app archive (.xcarchive)."""
        print("Building iOS archive...")
        subprocess.run([
            "xcodebuild", "archive",
            "-workspace", "ios/App.xcworkspace",
            "-scheme", "App",
            "-configuration", "Release",
            "-archivePath", "build/App.xcarchive"
        ], cwd=self.project_path, check=True)
        
        return str(self.project_path / "build/App.xcarchive")
    
    def export_ipa(self, archive_path: str) -> str:
        """Export the IPA from the archive."""
        print("Exporting IPA...")
        subprocess.run([
            "xcodebuild", "-exportArchive",
            "-archivePath", archive_path,
            "-exportPath", "build/",
            "-exportOptionsPlist", "ios/ExportOptions.plist"
        ], cwd=self.project_path, check=True)
        
        return str(self.project_path / "build/App.ipa")
    
    def upload_to_testflight(self, ipa_path: str):
        """Upload IPA to TestFlight using Fastlane."""
        print("Uploading to TestFlight...")
        subprocess.run([
            "fastlane", "pilot", "upload",
            "--ipa", ipa_path,
            "--skip_waiting_for_build_processing"
        ], check=True)
    
    def deploy(self):
        """Full deployment pipeline."""
        archive_path = self.build_archive()
        ipa_path = self.export_ipa(archive_path)
        self.upload_to_testflight(ipa_path)
        print("Deployment to TestFlight complete!")

if __name__ == "__main__":
    deployer = AppleStoreDeployer("/path/to/project")
    deployer.deploy()
