import Foundation
import Capacitor

// Keeps a copy of the player's save in their own iCloud (key-value storage), so a new or replaced iPhone
// gets its Forgelings back. Apple holds this data in the player's private iCloud; Forgelings never sees it.
// Limits: 1 MB per app in total; a compressed save is about 13 KB a year.
@objc(CloudSavePlugin)
public class CloudSavePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "CloudSavePlugin"
    public let jsName = "CloudSave"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "status", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "get", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "set", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "remove", returnType: CAPPluginReturnPromise)
    ]
    private let store = NSUbiquitousKeyValueStore.default
    private let maxBytes = 900_000

    override public func load() {
        NotificationCenter.default.addObserver(self, selector: #selector(changedExternally(_:)),
            name: NSUbiquitousKeyValueStore.didChangeExternallyNotification, object: store)
        store.synchronize()
    }

    @objc func changedExternally(_ note: Notification) {
        let keys = (note.userInfo?[NSUbiquitousKeyValueStoreChangedKeysKey] as? [String]) ?? []
        let reason = (note.userInfo?[NSUbiquitousKeyValueStoreChangeReasonKey] as? Int) ?? -1
        notifyListeners("change", data: ["keys": keys, "reason": reason])
    }

    // available: the person is signed in to iCloud on this device (iCloud Drive need not be on).
    @objc func status(_ call: CAPPluginCall) {
        call.resolve(["available": FileManager.default.ubiquityIdentityToken != nil])
    }

    @objc func get(_ call: CAPPluginCall) {
        guard let key = call.getString("key") else { call.reject("key is required"); return }
        store.synchronize()
        if let value = store.string(forKey: key) { call.resolve(["value": value]) } else { call.resolve([:]) }
    }

    @objc func set(_ call: CAPPluginCall) {
        guard let key = call.getString("key"), let value = call.getString("value") else { call.reject("key and value are required"); return }
        if value.utf8.count > maxBytes { call.reject("The save is too large for iCloud key-value storage", "TOO_BIG"); return }
        store.set(value, forKey: key)
        store.synchronize()
        call.resolve()
    }

    @objc func remove(_ call: CAPPluginCall) {
        guard let key = call.getString("key") else { call.reject("key is required"); return }
        store.removeObject(forKey: key)
        store.synchronize()
        call.resolve()
    }
}
