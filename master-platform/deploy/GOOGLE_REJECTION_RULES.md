# Google Play Store Rejection Rules: The Definitive Guide

**Author:** Manus AI
**Date:** 2026-02-15

> This document provides a guide to the most common Google Play Store rejection reasons, with a focus on technical compliance.

## 1. Policy: Target API Level Requirements

Google requires that new apps and app updates target a recent Android API level. Typically, this is within one year of the latest major Android release.

- **Requirement:** As of August 2023, new apps must target API level 33 (Android 13) or higher.

### Wrong Way (Gets Rejected)

Setting an old `targetSdkVersion` in your `build.gradle` file.

```groovy
// WRONG: build.gradle
android {
    defaultConfig {
        applicationId "com.myapp"
        minSdkVersion 21
        targetSdkVersion 30 // This is too old and will be rejected
        versionCode 1
        versionName "1.0"
    }
}
```

### Right Way (Passes Review)

Update your `targetSdkVersion` to the required level.

```groovy
// RIGHT: build.gradle
android {
    defaultConfig {
        applicationId "com.myapp"
        minSdkVersion 21
        targetSdkVersion 34 // Target a recent API level (Android 14)
        versionCode 1
        versionName "1.0"
    }
}
```

## 2. Policy: Data Safety Section

You must accurately fill out the Data safety form in the Play Console, declaring what data your app collects, why, and whether it's shared.

- **Requirement:** Your app's privacy policy and your Data safety form must be consistent.

### How to Comply

1.  **Audit Data Usage:** Identify all data collected by your app and any third-party SDKs (Firebase, AdMob, etc.).
2.  **Complete the Form:** In the Play Console, go to `App content > Data safety` and answer the questionnaire accurately.
3.  **Provide a Privacy Policy:** Your app must have a publicly accessible privacy policy.

## 3. Policy: Permissions

Only request permissions that are necessary for your app's core functionality.

### Wrong Way (Gets Rejected)

Requesting broad permissions like `READ_SMS` or `ACCESS_FINE_LOCATION` for a simple utility app that doesn't need them.

```xml
<!-- WRONG: AndroidManifest.xml -->
<uses-permission android:name="android.permission.READ_SMS" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### Right Way (Passes Review)

Only declare permissions you absolutely need. For Android 13+, you must request the `POST_NOTIFICATIONS` permission at runtime to send notifications.

```java
// RIGHT: Requesting notification permission at runtime
if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
    if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) !=
        PackageManager.PERMISSION_GRANTED) {
        requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, 101);
    }
}
```

## 4. Policy: Deceptive Behavior (Background Location)

Accessing background location is highly restricted. You must justify it as essential to your app's core feature, and it must be obvious to the user.

### How to Comply

- **Justify:** Your feature must provide clear value to the user from background location access.
- **Get Approval:** You must declare it in the Play Console and may need to submit your app for review.
- **In-app Disclosure:** You must show a prominent disclosure to the user before requesting background location.

---

*This is a condensed guide. For the full list, always refer to the official [Google Play Developer Policy Center](https://play.google.com/about/developer-policy-center/).*
