# Forgelings on TestFlight, from an iPhone (no Mac)

GitHub's Mac machines build, sign and upload the app (the `testflight` job in `.github/workflows/native.yml`). It is
off until the four secrets below exist. Everything here is done on an iPhone, in the Apple Developer app or Safari.
About 30 minutes of tapping, plus Apple's wait for enrollment.

Only the account holder can do these steps: they involve identity, payment, Apple's agreements and a private key.
Never paste the key into a chat or an issue. It goes straight into GitHub's secrets, where only the build can read it.

## 1. Join the Apple Developer Program (99 USD a year)

In the **Apple Developer** app: Account, then Enroll. As an individual, your name is the seller on the store. As the
LLC, the company's name is, and you need its D-U-N-S number first (Apple's lookup page; about a week). Wait for the
"Welcome" email before going on.

## 2. Register the app's identifiers (Safari: developer.apple.com/account, then Identifiers)

Tap **+** each time:

1. **App Groups**: description `Forgelings`, identifier `group.com.forgelings.app`.
2. **App IDs**, App: description `Forgelings`, Bundle ID (explicit) `com.forgelings.app`. Capabilities: tick
   **App Groups** (Configure: choose `group.com.forgelings.app`) and **iCloud** (with CloudKit off is fine; the app
   uses key-value storage).
3. **App IDs**, App: description `Forgelings Widget`, Bundle ID `com.forgelings.app.ForgelingsWidget`. Capability:
   **App Groups** with the same group.

While here, note your **Team ID**: Account, then Membership details (10 letters and digits).

## 3. Create the app (Safari: appstoreconnect.apple.com)

Apps, **+**, New App: platform iOS, name `Forgelings`, primary language English (U.S.), bundle ID `com.forgelings.app`,
SKU `forgelings-1`, full access. The store text and screenshots can wait; `store/listing.md` has them.

## 4. Make the upload key (App Store Connect)

Users and Access, **Integrations**, App Store Connect API. If asked, Request Access and accept. Then **Team Keys**,
**+**: name `GitHub builds`, access **Admin** (needed so the build can make its own signing certificate). Note the
**Key ID** and the **Issuer ID** shown above the list, then **Download** the key. It can be downloaded only once; it
lands in Files as `AuthKey_XXXXXXXXXX.p8`.

To copy its text: in Files, long-press it, Rename to end in `.txt`, open it, Select All, Copy. It starts with
`-----BEGIN PRIVATE KEY-----`.

## 5. Give the key to GitHub (Safari: github.com/img0j0/forge)

Settings, Secrets and variables, **Actions**, New repository secret, four times:

| Name | Value |
|---|---|
| `ASC_KEY_ID` | the Key ID |
| `ASC_ISSUER_ID` | the Issuer ID |
| `APPLE_TEAM_ID` | the Team ID |
| `ASC_PRIVATE_KEY` | the whole text of the key file, BEGIN and END lines included |

Then delete the `.txt` copy from Files.

## 6. Build, and install

Tell Claude the key is in (or: Actions, Native builds, Run workflow, branch `ios-app`). The `testflight` job uploads
build 100 + the run number. After Apple processes it (5 to 30 minutes): App Store Connect, the app, **TestFlight**,
Internal Testing, **+** a group, add yourself. Install **TestFlight** from the App Store and accept the invite. Each
later ship to `ios-app` uploads a new build.

If the first run fails at "Archive" naming a capability or an App Group, check step 2's ticks. Export compliance is
already answered in the app (`ITSAppUsesNonExemptEncryption` is NO: it uses no encryption beyond the system's).

## What to try on the phone first

The README's device checklist, especially: iCloud copy across two devices (qa_52 can only be settled here), the
widget and the wandering Live Activity, the daily reminder, haptics, VoiceOver through Today, the book and the
Hearth, and an older iPhone if one is around.
