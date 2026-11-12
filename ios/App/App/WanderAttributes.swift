import Foundation
#if canImport(ActivityKit)
import ActivityKit

// The Live Activity for a Forgeling out wandering: a countdown on the Lock Screen and in the Dynamic Island.
// Compiled into both the app (which starts and ends it) and the widget extension (which draws it).
// The words come from the web app, already in the player's language.
@available(iOS 16.1, *)
public struct WanderAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        public var until: Date
        public var title: String
        public var back: String
        public var done: Bool
        public init(until: Date, title: String, back: String, done: Bool) {
            self.until = until; self.title = title; self.back = back; self.done = done
        }
    }
    public var name: String
    public init(name: String) { self.name = name }
}
#endif

// Shared between the app and the widget: where the web app's snapshot is kept.
public enum FLShared {
    public static let group = "group.com.forgelings.app"
    public static var defaults: UserDefaults? { UserDefaults(suiteName: group) }
}
