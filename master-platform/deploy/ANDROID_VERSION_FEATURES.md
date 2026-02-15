# Android Version-Specific Features & API Level Matrix

**Author:** Manus AI
**Date:** 2026-02-15

> This document outlines key features introduced in recent Android versions and provides a strategy for implementing them while maintaining backward compatibility.

## Feature Matrix by API Level

| Android Version | API Level | Key Features                                                                                             |
| :-------------- | :-------- | :------------------------------------------------------------------------------------------------------- |
| **Android 15**  | 35        | **Private Space:** Create a secure, separate space for sensitive apps. <br> **Partial Screen Sharing:** Record or share just an app window, not the whole screen. <br> **Satellite Connectivity:** Support for direct satellite messaging. |
| **Android 14**  | 34        | **Predictive Back Gesture:** Animate back to the home screen. <br> **Credential Manager:** Unified API for passwords and passkeys. <br> **Health Connect:** Standardized API for health and fitness data. |
| **Android 13**  | 33        | **Per-App Language:** Users can set language on a per-app basis. <br> **Photo Picker:** A new, privacy-preserving way to select media. <br> **Notification Permission:** Apps must request permission to send notifications. |
| **Android 12**  | 31        | **Material You:** Dynamic color theming based on wallpaper. <br> **Splash Screens API:** Standardized splash screen implementation. <br> **Approximate Location:** Users can grant approximate location instead of precise. |

## Implementation Strategy: Feature Flags & Graceful Degradation

Never assume a user is on the latest Android version. Use a feature flag system based on the device's SDK version to enable or disable features.

### Example: Photo Picker (API 33+)

If the user is on Android 13 or newer, use the modern Photo Picker. If they are on an older version, fall back to the legacy `ACTION_GET_CONTENT` intent.

#### Wrong Way (Crashes on Older Devices)

```java
// WRONG: This will crash on Android 12 and below
Intent intent = new Intent(MediaStore.ACTION_PICK_IMAGES);
startActivityForResult(intent, REQUEST_CODE);
```

#### Right Way (With Fallback)

```java
// RIGHT: Check the SDK version before calling the API
void openPhotoPicker() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        // Use the modern Photo Picker on API 33+
        Intent intent = new Intent(MediaStore.ACTION_PICK_IMAGES);
        startActivityForResult(intent, REQUEST_CODE);
    } else {
        // Fallback for older versions
        Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
        intent.setType("image/*");
        startActivityForResult(intent, REQUEST_CODE);
    }
}
```

### Example: Notification Permission (API 33+)

On Android 13+, you must request the `POST_NOTIFICATIONS` permission at runtime. On older versions, this permission doesn't exist, and you can send notifications by default.

```java
// RIGHT: Conditionally request the notification permission
void requestNotificationPermission() {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS) !=
            PackageManager.PERMISSION_GRANTED) {
            // The system will show a dialog to the user
            requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, 101);
        }
    }
    // On older versions, no action is needed.
}
```

---
