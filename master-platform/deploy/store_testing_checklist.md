# App Store & Google Play: Pre-Submission Testing Checklist

**Author:** Manus AI
**Date:** 2026-02-15

> This checklist covers the essential tests required to ensure your app meets the quality and compliance standards of both the Apple App Store and Google Play Store. Run through this list before every submission to minimize the risk of rejection.

## Phase 1: Core Functionality & Stability

- [ ] **Crash-Free Operation:** Test all major user flows. The app must not crash or hang.
- [ ] **Broken Links:** Tap every button, link, and navigation item. Ensure there are no dead ends.
- [ ] **Placeholder Content:** Remove all `lorem ipsum`, placeholder images, and empty sections.
- [ ] **Login & Authentication:**
    - [ ] Test login/logout with all providers (Email, Google, Facebook, Apple).
    - [ ] Test the registration flow.
    - [ ] Test password reset functionality.
    - [ ] If social logins are used, "Sign in with Apple" **must** be present.
- [ ] **In-App Purchases:**
    - [ ] Test the entire purchase flow in a sandbox environment (TestFlight for iOS, Internal Testing for Android).
    - [ ] Verify that content is unlocked after purchase.
    - [ ] Test subscription renewals and cancellations.
    - [ ] Test the "Restore Purchases" functionality.

## Phase 2: Platform Compliance & Metadata

### Apple App Store

- [ ] **Human Interface Guidelines (HIG):** Does the app look and feel like a native iOS app? (e.g., uses standard navigation, tab bars, etc.)
- [ ] **Accurate Metadata:**
    - [ ] Screenshots and previews accurately represent the current app version.
    - [ ] App description is honest and not misleading.
- [ ] **Privacy Manifest (`PrivacyInfo.xcprivacy`):**
    - [ ] File is included in the project.
    - [ ] All data collection (including third-party SDKs) is declared.
- [ ] **App Tracking Transparency (ATT):** If you track users, the ATT prompt must be shown.
- [ ] **IPv6 Compatibility:** Test the app on an IPv6-only network.

### Google Play Store

- [ ] **Target API Level:** `targetSdkVersion` in `build.gradle` is set to the required level (e.g., 34).
- [ ] **Data Safety Form:** The form in the Play Console is filled out accurately and matches your privacy policy.
- [ ] **Permissions:** `AndroidManifest.xml` only requests permissions essential for the app.
- [ ] **Notification Permission:** For Android 13+, the `POST_NOTIFICATIONS` permission is requested at runtime.
- [ ] **Privacy Policy:** A link to a valid privacy policy is provided in the Play Console and within the app.

## Phase 3: Performance & User Experience

- [ ] **Launch Time:** The app should launch quickly (ideally under 2 seconds).
- [ ] **Responsiveness:** The UI should be smooth and not lag on supported devices.
- [ ] **Device & OS Testing:**
    - [ ] Test on a range of physical devices (different screen sizes).
    - [ ] Test on the oldest and newest supported OS versions (e.g., iOS 16 and iOS 18).
- [ ] **Accessibility (WCAG):**
    - [ ] Test with VoiceOver (iOS) and TalkBack (Android).
    - [ ] Ensure sufficient color contrast.
    - [ ] All controls should have accessible labels.
- [ ] **Offline Support:** The app should handle loss of network connectivity gracefully (e.g., show a message instead of crashing).
- [ ] **Battery & Memory Usage:** Profile the app to ensure it doesn't cause excessive battery drain or memory consumption.

---
