# UI Automation learning process in mobly

A documentation of my journey learning Python, specifically focused on **Test Automation Engineering**. Below is the roadmap I follow:

---

### Stage 1: Python Foundational Infrastructure
**Status: Completed**

Skills Learned:
* In-depth Lists/Dictionaries & Data Structures
* File Handling (I/O)
* Error Handling (try/except)

**Practical Goal:** Built a "Number Guessing Game" with robust error handling & score persistence.

---

### Stage 2: Python Intermediate & Developer Tools
**Status: Completed**

Skills Learned:
* Object-Oriented Programming (OOP)
* Virtual Environments (venv) & Package Management (pip)
* Git Basics (Personal Version Control & GitHub)

**Practical Goal:** Refactored the "Number Guessing Game" using OOP principles, managed dependencies with venv, and pushed the project to GitHub.

---

### Stage 3: Introduction to Android Automation (Mobly)
**Status: Completed**

Skills to Learn:
* **Google Mobly Framework:** Understanding the lifecycle (`setup_class`, `teardown_class`, `test_*`).
* **ADB (Android Debug Bridge):** Controlling devices via command line and Python `subprocess`.
* **YAML Configuration:** Managing testbeds and user parameters externally.

**Practical Goal:** Write a basic Mobly script to automatically toggle Wi-Fi on an Android emulator and verify the state via ADB.

---

### Stage 4: Modularization & Logic Encapsulation
**Status: Completed**

Skills to Learn:
* **Controller Pattern:** Separating test logic (Script) from device operations (Lib).
* **Snippet Interaction:** Using Mobly Bundled Snippets (`mbs`) for stable RPC calls.
* **Defensive Programming:** Using `hasattr` and error handling for robust device control.

**Practical Goal:** Refactor the Wi-Fi test to use a `WifiController` class, decoupling the ADB/Snippet commands from the test case.

---

### Stage 5: Enterprise Mobly Architecture (Current Focus)
**Status: Completed**

Skills to Learn:
* **Layered Architecture:** Designing `config`, `common`, `libs`, `datamodels`, and `tests` layers.
* **Data Models (Proto-style):** Using Python `dataclasses` to create strict contracts between Config and Controllers.
* **Dependency Injection (DI):** Injecting device objects into Controllers via `BaseTest` to improve testability.
* **Robust Data Mapping:** Safely parsing external YAML data into internal Type-safe objects.

**Practical Goal:** Build a scalable **Wi-Fi & Bluetooth Automation Framework** featuring:
- [x] **Datamodels:** `WifiConfig` & `BluetoothConfig` for strict type checking.
- [x] **Dependency Injection:** Injecting controllers in `EnterpriseBaseTest`.
- [x] **Abstraction:** High-level test scripts that read like English instructions.

---

### Stage 6: CI/CD & Pipeline Integration
**Status: Completed**

Skills to Learn:
* Git for Teams (Branching & Merging)
* CI/CD Concepts (GitLab CI / GitHub Actions)
* Automated Reporting (Generating Test Summaries)

**Practical Goal:** Set up a GitHub Actions pipeline to automatically run the Mobly test suite (using Emulators) on every code push.

---

### Stage 7: Containerization & Advanced Analysis
**Status: In progress**

Skills to Learn:
* Docker Core Concepts (Running tests in isolated containers)
* Log Analysis (Parsing Mobly logs with Pandas)
* Visualization (Matplotlib for pass/fail trends)

**Practical Goal:** Dockerize the test environment and create a dashboard to visualize test stability over time.

---

### Stage 8: Flaky Test Governance & Quarantine Mechanism
**Status: Planned**

Skills to Learn:
* **Custom Python Decorators:** Building `@retry_on_flaky` to gracefully capture transient execution failures (`ADBTimeout`, `RuntimeError`).
* **Test Telemetry & Tagging:** Tracking retried tests, tagging them as `FLAKY`, and exporting execution metrics to JSON reports.
* **Bazel Target Quarantine:** Utilizing Bazel tags (`tags = ["flaky", "quarantine"]`) to physically isolate unstable test suites from the CI mainline.

**Practical Goal:** Implement a global retry decorator in `base_test.py`, generate telemetry metrics for quality tracking, and configure Bazel targets to prevent flaky tests from blocking CI builds.

---

### Stage 9: Custom Developer CLI & Developer Enablement
**Status: Planned**

Skills to Learn:
* **CLI Tool Development:** Building a `mobly-cli` tool using Python `click`/`argparse` to abstract complex Bazel and Mobly commands.
* **Sanity Pre-flight Engine:** Automating environment pre-checks (`adb devices` connectivity, MBS Snippet APK installation, `PATH` verification).
* **Developer Codelabs:** Writing production-grade Codelabs and developer guides to improve Engineering Productivity.

**Practical Goal:** Develop a single-command `mobly-cli` tool that validates local environment readiness and allows SWEs (Software Engineers) to execute tests locally within seconds.

---

### Stage 10: Logcat Triage Parser & Android System Mocking
**Status: Planned**

Skills to Learn:
* **Logcat Automated Triage:** Parsing logcat outputs upon test failure to extract `FATAL EXCEPTION`, `NullPointerException`, and `ANR` stack traces.
* **Android System Mocking:** Using `adb shell am broadcast` and `cmd` to simulate extreme system states (Low Memory Killer, battery overheating, network drops).
* **Root Cause Analysis (RCA):** Attaching extracted crash logs and telemetry directly to automated test report summaries.

**Practical Goal:** Integrate a Logcat Triage Parser into the `on_fail` lifecycle hook to automatically extract crash root causes, and write edge-case test cases using Android system mocking.
