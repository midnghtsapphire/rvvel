'''
# Skill: App Store Compliance Expert

**Author:** Manus AI
**Date:** 2026-02-15

## Description

This skill provides expert guidance on navigating the complex and ever-changing rules for submitting applications to the Apple App Store and Google Play Store. It is designed to prevent common rejections, streamline the submission process, and ensure compliance with platform-specific guidelines.

## Core Competencies

1.  **Rejection Rule Analysis:** Deep understanding of the most common rejection reasons for both Apple (App Store Review Guidelines) and Google (Developer Policy Center).
2.  **Technical Compliance:** Ability to identify and provide code-level solutions for critical compliance issues, including:
    *   **In-App Purchases (IAP):** Correctly implementing Apple's StoreKit and Google Play Billing.
    *   **Privacy:** Creating and managing Privacy Manifests (`PrivacyInfo.xcprivacy`) for Apple and completing Google's Data Safety form.
    *   **Permissions:** Requesting only necessary permissions and handling runtime permission flows.
    *   **Minimum Functionality:** Avoiding the "web wrapper" rejection by integrating native UI and features.
    *   **Authentication:** Implementing "Sign in with Apple" when other social logins are present.
    *   **API Level Targeting:** Ensuring the `targetSdkVersion` meets Google's requirements.
3.  **Deployment Strategy:** Advising on best practices for versioning, release tracks (alpha, beta, production), staged rollouts, and backward compatibility.
4.  **Documentation Mastery:** Ability to generate and reference comprehensive documentation, including rule guides, code examples, and links to official resources.

## How to Use This Skill

When tasked with building or deploying a mobile application, invoke this skill to perform a pre-submission compliance check. The process is as follows:

1.  **Analyze Project Scope:** Review the app's features, data collection practices, and monetization strategy.
2.  **Cross-Reference with Rejection Rules:** Compare the app against the knowledge bases located at:
    *   `/master-platform/deploy/APPLE_REJECTION_RULES.md`
    *   `/master-platform/deploy/GOOGLE_REJECTION_RULES.md`
3.  **Generate Compliance Report:** Produce a report detailing potential rejection risks and providing actionable recommendations with code examples.
4.  **Update Build Configuration:** Modify `build.gradle` (Android) and Xcode project settings (iOS) to ensure compliance with versioning, permissions, and privacy requirements.
5.  **Verify Implementation:** Ensure that the code for IAP, login, and data handling follows the best practices outlined in the documentation.

### Example Invocation

"Review the 'Project Face' mobile app for App Store and Google Play compliance before deployment. Generate a report of any potential rejection issues and provide the necessary code modifications to pass review."

---
'''
