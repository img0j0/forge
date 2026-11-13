# Forgelings for iPhone and Android

This folder turns the Forgelings web app into real iPhone and Android apps with [Capacitor](https://capacitorjs.com).
The app itself is the same single page as the web version (`forgelings.html`). Inside the apps it:

- keeps every save in the phone's own storage as well as web storage, so clearing web data doesn't lose a collection
  (extra protection, not a guarantee: deleting the app removes its local copy)
- **iPhone:** keeps a quiet copy in the player's own iCloud (Apple's key-value storage), so a new iPhone brings the
  Forgelings back. Forgelings can never see it. Players can turn it off in Settings, which removes the copy.
- **Android:** Android's own app backup keeps a copy when the phone's backup is on (`allowBackup` is on)
- sends one gentle reminder a day (only if today's card is still waiting) and a note when a wanderer is back
- uses haptics and the share sheet; on Android, the back button closes what's open, then goes to Today
- **iPhone:** a home-screen widget (today's card, the companion or latest postcard) and a Live Activity counting down a
  wanderer's return; **Android:** an app widget and an ongoing countdown notification
- runs in English or Japanese (the phone's language, or Settings > Look and feel > Language); the permission sentences
  (camera and photos for postcards, saving pictures) are in both languages
- hides tester-only pieces (feedback questions, pilot report, prototype tools) and says "First Edition" on cards

App ID: `com.forgelings.app` on both stores. It can be changed until the first upload, never after.

## No Mac needed to check a build

Every push to this branch runs **Native builds** on GitHub (`.github/workflows/native.yml`):

- **Android:** builds a debug app. Open the run under the repo's **Actions** tab, download
  `forgelings-android-debug` from **Artifacts**, unzip it, and open `app-debug.apk` on an Android phone (allow
  "install unknown apps" for your browser or Files app when asked).
- **iPhone:** compiles the Xcode project for the simulator, unsigned, and checks Forgelings' own Swift code
  (the iCloud copy) and the widget extension are inside the app. It can't make a TestFlight build; that needs signing (below).

## Android: first time

1. Install [Android Studio](https://developer.android.com/studio) on any Windows, Mac or Linux computer.
2. Get this project, then:
   ```
   npm install
   npm run sync:android
   npm run open:android
   ```
   `sync:android` copies the app into the Android project and re-applies the icons, notification icon, launch screen
   and portrait setting (`android-setup.py`).
3. Press Run with a phone plugged in (Developer options and USB debugging on), or use an emulator.
4. **Google Play:** a developer account costs $25 once. A **personal** account created after November 13, 2023 must
   run a closed test with at least 12 testers opted in for 14 days in a row before the app can go public. An
   **organization** account (for example the LLC, with a D-U-N-S number) skips that rule.
5. Release builds need an upload key: in Android Studio, **Build > Generate Signed App Bundle**, create a keystore,
   and keep it and its passwords safe (Play App Signing holds the real signing key).

## iPhone: first time on the Mac (about an afternoon)

1. **Update macOS** to Tahoe 26.2 or later: Settings > General > Software Update.
2. **Install Xcode** from the Mac App Store (it's large, so leave it downloading). Open it once and let it install
   its components. Then in Xcode > Settings > Accounts, sign in with the Apple ID you'll use for the
   Apple Developer Program.
3. **Install Node.js** (the LTS version) from https://nodejs.org.
4. **Get this project.** In Terminal:
   ```
   git clone -b ios-app https://github.com/img0j0/forge forgelings-app
   cd forgelings-app
   npm install
   npm run sync
   npm run open
   ```
   `npm run sync` copies the app into the iPhone project and re-applies the settings. `npm run open` opens it in Xcode.
5. **In Xcode**, click **App** in the left sidebar, then **Signing & Capabilities**. Tick
   "Automatically manage signing" and choose your team (your Apple ID). **iCloud** should be listed with
   **Key-value storage** ticked (it comes from `App/App.entitlements`). If it isn't, click **+ Capability**, add
   iCloud and tick Key-value storage.
6. **Run it on your iPhone.** Plug the iPhone in, trust the Mac, and turn on Developer Mode on the
   iPhone if asked (Settings > Privacy & Security > Developer Mode). Pick the iPhone at the top of Xcode and press the
   Play button.
7. **Widget and wandering countdown (0.62).** Still under Signing & Capabilities, the **App** target should also list
   **App Groups** with `group.com.forgelings.app` ticked (from `App/App.entitlements`). Click the **ForgelingsWidget**
   target in the left column of the same screen, choose the same team, and check it lists App Groups with the same
   group ticked. If Xcode says the group isn't registered, click the refresh button next to it or the + to add
   `group.com.forgelings.app`; automatic signing registers it with Apple. Then on the iPhone: long-press the home
   screen > + > Forgelings, and send a Forgeling wandering to see the countdown on the Lock Screen (Settings >
   Forgelings > Live Activities must be on). The widget needs iOS 16.2 or later; the app itself still runs on iOS 15.
8. **Check the iCloud copy** (on a real iPhone signed in to iCloud): find a Forgeling, wait a few seconds, then look in
   Settings > Your collection > iCloud: it should say "Last saved just now". Delete the app, install it again, and the
   journal should come back without the welcome.

## Updating the apps after a new Forgelings version

```
cp /path/to/new/forgelings.html forgelings.html
npm run sync            # iPhone
npm run sync:android    # Android
```
Then press Play again. To rebuild a native project from scratch: delete `ios/` (or `android/`), run
`npx cap add ios` (or `android`), then `python3 ios-setup.py` (or `android-setup.py`).

## Sending a build to TestFlight

1. In Xcode, set the target device to **Any iOS Device (arm64)**.
2. **Product > Archive**. When it finishes, the Organizer opens: **Distribute App > App Store Connect > Upload**.
3. In App Store Connect, the build appears under TestFlight after processing (about 15 to 30 minutes).
   Add testers by email.
4. For each new upload, raise **Build** (`CURRENT_PROJECT_VERSION`) by one in Xcode.

## What's in here

| Path | What it is |
|---|---|
| `forgelings.html` | The app: a copy of the dev branch's `app.html` (English and Japanese), updated by `tools/ship.sh` on every release |
| `build-www.py` | Makes `www/index.html` from it, marked as the store edition |
| `capacitor.config.json` | App name, app ID, colours, the Android notification icon |
| `ios-setup.py` | Applies the icon, launch screen, portrait-only, iPhone-only, the encryption answer, the camera, photo-library and photo-save permission sentences (English and Japanese `InfoPlist.strings`), the privacy manifest (`PrivacyInfo.xcprivacy`), and the iCloud copy (`CloudSavePlugin.swift`, `MainViewController.swift`, `App.entitlements`) |
| `ios/` | The Xcode project (generated by Capacitor, then adjusted by `ios-setup.py`) |
| `android-setup.py` | Applies the Android icons (adaptive wax seal), notification icon, launch screen and portrait setting |
| `android/` | The Android Studio project (generated by Capacitor, then adjusted by `android-setup.py`). Its widget and wandering countdown: `ForgelingsWidgetProvider.java`, `WidgetBridgePlugin.java`, `res/layout/forgelings_widget.xml` |
| `ios/App/ForgelingsWidget/` | The iPhone widget extension: the home-screen widget and the wandering Live Activity (`ForgelingsWidget.swift`). The app feeds it through `App/WidgetBridgePlugin.swift` and the App Group; `App/WanderAttributes.swift` is shared by both |
| `tools/add-widget.cjs` | Added the widget extension target to the Xcode project (already done; safe to run again) |
| `.github/workflows/native.yml` | Builds the Android app and compiles the iPhone app on GitHub, checking the plugin and widget extension are inside |
| `store/` | App Store listing (`listing.md`), screenshots (`screens/` English, `screens-ja/` Japanese, from 0.73.1) and the scripts that make them (`shots.py`, `compose.py`) |
