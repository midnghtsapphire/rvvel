# Apple App Store Rejection Rules: The Definitive Guide

**Author:** Manus AI
**Date:** 2026-02-15

> This document provides a comprehensive guide to the most common Apple App Store rejection reasons, complete with code examples of what to do and what not to do. Following these guidelines is critical to avoid lengthy and frustrating rejection cycles.

## 1. Guideline 3.1.1: In-App Purchases

This is the most common reason for rejection. If you sell digital goods or services, you **MUST** use Apple's In-App Purchase (IAP) system. This includes subscriptions, premium features, and in-app currency.

### Wrong Way (Gets Rejected)

Using a third-party payment system like Stripe or PayPal for digital goods.

```swift
// WRONG: Using a Stripe checkout for a digital subscription
func purchaseSubscription() {
    let checkoutURL = URL(string: "https://my-site.com/buy-subscription")!
    // This opens a web view to a Stripe payment page
    let webViewController = SFSafariViewController(url: checkoutURL)
    present(webViewController, animated: true)
}
```

### Right Way (Passes Review)

Using Apple's `StoreKit` framework to handle the purchase.

```swift
// RIGHT: Using StoreKit for an in-app purchase
import StoreKit

func purchaseSubscription() async {
    guard let product = try? await Product.products(for: ["com.myapp.pro_subscription"]).first else {
        print("Product not found")
        return
    }

    do {
        let result = try await product.purchase()
        switch result {
        case .success(let verification):            
            // Unlock content
            print("Purchase successful!")
        case .userCancelled:
            print("User cancelled purchase")
        case .pending:
            print("Purchase is pending approval")
        @unknown default:
            break
        }
    } catch {
        print("Purchase failed: \(error)")
    }
}
```

## 2. Guideline 5.1.1: Data Collection and Storage (Privacy Manifest)

As of iOS 17, you **MUST** include a `PrivacyInfo.xcprivacy` file (Privacy Manifest) in your app, declaring what data you collect and why.

### Wrong Way (Gets Rejected)

Not including a `PrivacyInfo.xcprivacy` file, or collecting data without declaring it.

### Right Way (Passes Review)

Create a `PrivacyInfo.xcprivacy` file and declare all data collection.

**Example `PrivacyInfo.xcprivacy` content:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>NSPrivacyCollectedDataTypes</key>
    <array>
        <dict>
            <key>NSPrivacyCollectedDataType</key>
            <string>NSPrivacyCollectedDataTypeName</string>
            <key>NSPrivacyCollectedDataTypeLinked</key>
            <true/>
            <key>NSPrivacyCollectedDataTypeTracking</key>
            <false/>
            <key>NSPrivacyCollectedDataTypePurposes</key>
            <array>
                <string>NSPrivacyCollectedDataTypePurposeAppFunctionality</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
```

## 3. Guideline 4.2: Minimum Functionality (No Web Wrappers)

Your app must provide more than just a repackaged website. It needs to feel like a native app.

### Wrong Way (Gets Rejected)

An app that is just a single `WKWebView` loading your website.

```swift
// WRONG: Just a web view
import WebKit

class ViewController: UIViewController, WKNavigationDelegate {
    override func viewDidLoad() {
        super.viewDidLoad()
        let webView = WKWebView(frame: view.bounds)
        webView.navigationDelegate = self
        view.addSubview(webView)
        let url = URL(string: "https://www.my-website.com")!
        webView.load(URLRequest(url: url))
    }
}
```

### Right Way (Passes Review)

Integrate native UI components and device features.

```swift
// RIGHT: Native UI with web content integrated
class ViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        // Native tab bar, navigation bar, etc.
        let tabBarController = UITabBarController()
        let nativeVC = NativeFeatureViewController()
        let webVC = WebcontentViewController() // This can contain a web view
        tabBarController.viewControllers = [nativeVC, webVC]
        present(tabBarController, animated: false)
    }
}
```

## 4. Guideline: Sign in with Apple

If your app uses third-party social login (e.g., Google, Facebook), you **MUST** also offer "Sign in with Apple".

### Wrong Way (Gets Rejected)

Only offering Google and Facebook login buttons.

### Right Way (Passes Review)

Adding the `ASAuthorizationAppleIDButton`.

```swift
// RIGHT: Including Sign in with Apple
import AuthenticationServices

func setupLoginButtons() {
    let appleButton = ASAuthorizationAppleIDButton()
    appleButton.addTarget(self, action: #selector(handleSignInWithApple), for: .touchUpInside)
    // Add this button alongside Google/Facebook buttons
    view.addSubview(appleButton)
}

@objc func handleSignInWithApple() {
    // ... handle Apple Sign In flow
}
```

---

*This is a condensed guide. For the full list, always refer to the official [App Store Review Guidelines](https://developer.apple.com/app-store/review/guidelines/).*
