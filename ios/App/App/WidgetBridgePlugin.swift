import Foundation
import Capacitor
import WidgetKit
#if canImport(ActivityKit)
import ActivityKit
#endif

// Lets the web app feed the home-screen widget and the wandering Live Activity.
// update: the Forgeling to show, its lines (already translated), today's date and, while it wanders, when it is back.
// wanderStart / wanderEnd: the Live Activity (iOS 16.2+, and only if the person allows Live Activities).
@objc(WidgetBridgePlugin)
public class WidgetBridgePlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "WidgetBridgePlugin"
    public let jsName = "Widget"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "update", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "wanderStart", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "wanderEnd", returnType: CAPPluginReturnPromise)
    ]

    @objc func update(_ call: CAPPluginCall) {
        guard let d = FLShared.defaults else { call.resolve(["ok": false]); return }
        d.set(call.getString("name") ?? "", forKey: "fl.name")
        d.set(call.getString("line") ?? "", forKey: "fl.line")
        d.set(call.getString("fresh") ?? "", forKey: "fl.fresh")
        d.set(call.getString("wline") ?? "", forKey: "fl.wline")
        d.set(call.getString("back") ?? "", forKey: "fl.back")
        d.set(call.getString("day") ?? "", forKey: "fl.day")
        d.set(call.getDouble("until") ?? 0, forKey: "fl.until")
        if let b = call.getString("png"), let data = Data(base64Encoded: b) { d.set(data, forKey: "fl.png") }
        // 0.66: the latest photo postcard ("" when there is none)
        if let b = call.getString("post") {
            if b.isEmpty { d.removeObject(forKey: "fl.post") } else if let data = Data(base64Encoded: b) { d.set(data, forKey: "fl.post") }
        }
        WidgetCenter.shared.reloadAllTimelines()
        call.resolve(["ok": true])
    }

    @objc func wanderStart(_ call: CAPPluginCall) {
        #if canImport(ActivityKit)
        if #available(iOS 16.2, *) {
            guard ActivityAuthorizationInfo().areActivitiesEnabled else { call.resolve(["ok": false]); return }
            let until = Date(timeIntervalSince1970: (call.getDouble("until") ?? 0) / 1000)
            let name = call.getString("name") ?? ""
            let state = WanderAttributes.ContentState(until: until, title: call.getString("title") ?? "", back: call.getString("back") ?? "", done: false)
            Task {
                for a in Activity<WanderAttributes>.activities { await a.end(nil, dismissalPolicy: .immediate) }
                do {
                    _ = try Activity.request(attributes: WanderAttributes(name: name),
                                             content: ActivityContent(state: state, staleDate: until.addingTimeInterval(3600)),
                                             pushType: nil)
                    call.resolve(["ok": true])
                } catch {
                    call.resolve(["ok": false, "error": error.localizedDescription])
                }
            }
            return
        }
        #endif
        call.resolve(["ok": false])
    }

    @objc func wanderEnd(_ call: CAPPluginCall) {
        #if canImport(ActivityKit)
        if #available(iOS 16.2, *) {
            let back = call.getString("back") ?? ""
            Task {
                for a in Activity<WanderAttributes>.activities {
                    var s = a.content.state; s.done = true; if !back.isEmpty { s.back = back }
                    await a.end(ActivityContent(state: s, staleDate: nil), dismissalPolicy: .after(Date().addingTimeInterval(15 * 60)))
                }
                call.resolve(["ok": true])
            }
            return
        }
        #endif
        call.resolve(["ok": false])
    }
}
