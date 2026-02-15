# Master Platform: Unified Application Ecosystem

**Author:** Audrey Evans

This repository contains the source code for the Master Platform, a unified subscription application that integrates all of Audrey Evans's digital products and services.

### Modules
This project is built on a microservices architecture. Each of the following modules is a self-contained service:

-   `affiliate_engine.py`: Automatically generates Amazon affiliate links.
-   `procedure_finder.py`: Finds and ranks cosmetic/medical procedures.
-   `makeup_advisor.py`: AI-powered makeup recommendations.
-   `selling_space.py`: Self-service ad platform for business.
-   `subscription_manager.py`: Manages user subscriptions and tokens with Stripe.
-   `clinical_trials_finder.py`: Matches users with clinical trials.
-   `daily_weather_skincare.py`: Provides daily skincare routines based on local weather.
-   And many more...

### Deployment
-   The `/deploy` directory contains the automated CI/CD pipeline for publishing to the Apple App Store, Google Play Store, and for creating desktop executables.
