import WidgetKit
import SwiftUI
import ActivityKit

// Forgelings' home-screen widget and the wandering Live Activity. Everything shown comes from the app's last
// snapshot (FLShared), already in the player's language; the widget only works out whether a new day has begun.

private let ink = Color(red: 0.14, green: 0.10, blue: 0.25)
private let gold = Color(red: 1.0, green: 0.83, blue: 0.42)
private let soft = Color(red: 0.85, green: 0.82, blue: 0.96)
private var isJA: Bool { (Locale.preferredLanguages.first ?? "").hasPrefix("ja") }

struct FLEntry: TimelineEntry {
    let date: Date
    let name: String
    let line: String
    let fresh: String
    let wline: String
    let back: String
    let day: String
    let until: Date?
    let png: Data?
}

private func todayKey(_ d: Date) -> String {
    let f = DateFormatter(); f.calendar = Calendar(identifier: .gregorian); f.locale = Locale(identifier: "en_US_POSIX")
    f.timeZone = .current; f.dateFormat = "yyyy-MM-dd"; return f.string(from: d)
}

struct FLProvider: TimelineProvider {
    func load(_ at: Date = Date()) -> FLEntry {
        let d = FLShared.defaults
        let u = d?.double(forKey: "fl.until") ?? 0
        return FLEntry(date: at,
                       name: d?.string(forKey: "fl.name") ?? "Forgelings",
                       line: d?.string(forKey: "fl.line") ?? "",
                       fresh: d?.string(forKey: "fl.fresh") ?? "",
                       wline: d?.string(forKey: "fl.wline") ?? "",
                       back: d?.string(forKey: "fl.back") ?? "",
                       day: d?.string(forKey: "fl.day") ?? "",
                       until: u > 0 ? Date(timeIntervalSince1970: u / 1000) : nil,
                       png: d?.data(forKey: "fl.png"))
    }
    func placeholder(in context: Context) -> FLEntry {
        FLEntry(date: Date(), name: "Forgelings", line: isJA ? "一日ひとつ、小さなこと。" : "One small thing a day.", fresh: "", wline: "", back: "", day: "", until: nil, png: nil)
    }
    func getSnapshot(in context: Context, completion: @escaping (FLEntry) -> Void) { completion(load()) }
    func getTimeline(in context: Context, completion: @escaping (Timeline<FLEntry>) -> Void) {
        let now = Date(), e = load(now)
        var entries = [e]
        if let u = e.until, u > now { entries.append(load(u)) }
        let midnight = Calendar.current.startOfDay(for: now.addingTimeInterval(86_400))
        entries.append(load(midnight.addingTimeInterval(1)))
        completion(Timeline(entries: entries, policy: .after(midnight.addingTimeInterval(60))))
    }
}

struct Sprite: View {
    let png: Data?
    var body: some View {
        if let p = png, let ui = UIImage(data: p) {
            Image(uiImage: ui).interpolation(.none).resizable().aspectRatio(contentMode: .fit)
        } else {
            Image(systemName: "flame.fill").resizable().aspectRatio(contentMode: .fit).foregroundColor(gold).padding(8)
        }
    }
}

extension View {
    @ViewBuilder func flBackground(_ c: Color) -> some View {
        if #available(iOSApplicationExtension 17.0, *) { self.containerBackground(for: .widget) { c } } else { self.background(c) }
    }
}

struct FLView: View {
    let e: FLEntry
    @Environment(\.widgetFamily) var family
    var wandering: Bool { if let u = e.until { return u > e.date } else { return false } }
    var back: Bool { if let u = e.until { return u <= e.date && !e.back.isEmpty } else { return false } }
    // a new day has begun since the app last spoke: today's card is waiting again
    var line: String { if !e.day.isEmpty && e.day != todayKey(e.date) && !e.fresh.isEmpty { return e.fresh }; return e.line }
    @ViewBuilder var words: some View {
        if wandering, let u = e.until {
            Text(e.wline).font(.system(size: 12, weight: .medium, design: .rounded)).foregroundColor(soft).lineLimit(2)
            Text(timerInterval: e.date...max(e.date, u), countsDown: true)
                .font(.system(size: 20, weight: .bold, design: .rounded)).monospacedDigit().foregroundColor(gold)
        } else if back {
            Text(e.back).font(.system(size: 13, weight: .semibold, design: .rounded)).foregroundColor(gold).lineLimit(3)
        } else {
            Text(line).font(.system(size: 13, weight: .medium, design: .rounded)).foregroundColor(soft).lineLimit(3)
        }
    }
    var body: some View {
        Group {
            if family == .systemSmall {
                VStack(alignment: .leading, spacing: 4) {
                    Sprite(png: e.png).frame(width: 52, height: 52)
                    Text(e.name).font(.system(size: 15, weight: .bold, design: .rounded)).foregroundColor(.white).lineLimit(1)
                    words
                    Spacer(minLength: 0)
                }.frame(maxWidth: .infinity, alignment: .leading)
            } else {
                HStack(spacing: 14) {
                    Sprite(png: e.png).frame(width: 96, height: 96)
                    VStack(alignment: .leading, spacing: 5) {
                        Text(e.name).font(.system(size: 18, weight: .bold, design: .rounded)).foregroundColor(.white).lineLimit(1)
                        words
                    }
                    Spacer(minLength: 0)
                }
            }
        }
        .padding(family == .systemSmall ? 2 : 4)
        .flBackground(ink)
    }
}

struct ForgelingsWidget: Widget {
    let kind = "ForgelingsWidget"
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: kind, provider: FLProvider()) { e in FLView(e: e) }
            .configurationDisplayName("Forgelings")
            .description(isJA ? "あなたのフォージリングと、今日のカード。" : "Your Forgeling, and today's card.")
            .supportedFamilies([.systemSmall, .systemMedium])
    }
}

// ---- the wandering Live Activity ----
private var sharedPNG: Data? { FLShared.defaults?.data(forKey: "fl.png") }

struct WanderTimer: View {
    let s: WanderAttributes.ContentState
    var body: some View {
        if s.done || s.until <= Date() {
            Image(systemName: "checkmark.circle.fill").foregroundColor(gold)
        } else {
            Text(timerInterval: Date()...s.until, countsDown: true).monospacedDigit().foregroundColor(gold)
        }
    }
}

struct WanderLiveActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: WanderAttributes.self) { ctx in
            HStack(spacing: 14) {
                Sprite(png: sharedPNG).frame(width: 56, height: 56)
                VStack(alignment: .leading, spacing: 4) {
                    Text(ctx.state.done ? ctx.state.back : ctx.state.title)
                        .font(.system(size: 15, weight: .semibold, design: .rounded)).foregroundColor(.white).lineLimit(2)
                    WanderTimer(s: ctx.state).font(.system(size: 22, weight: .bold, design: .rounded))
                }
                Spacer(minLength: 0)
            }
            .padding(16)
            .activityBackgroundTint(ink)
            .activitySystemActionForegroundColor(.white)
        } dynamicIsland: { ctx in
            DynamicIsland {
                DynamicIslandExpandedRegion(.leading) { Sprite(png: sharedPNG).frame(width: 40, height: 40) }
                DynamicIslandExpandedRegion(.trailing) { WanderTimer(s: ctx.state).font(.system(size: 20, weight: .bold, design: .rounded)) }
                DynamicIslandExpandedRegion(.bottom) {
                    Text(ctx.state.done ? ctx.state.back : ctx.state.title).font(.system(size: 14, design: .rounded)).foregroundColor(soft).lineLimit(1)
                }
            } compactLeading: {
                Sprite(png: sharedPNG).frame(width: 20, height: 20)
            } compactTrailing: {
                WanderTimer(s: ctx.state).frame(maxWidth: 52)
            } minimal: {
                Sprite(png: sharedPNG).frame(width: 20, height: 20)
            }
        }
    }
}

@main
struct ForgelingsWidgets: WidgetBundle {
    var body: some Widget {
        ForgelingsWidget()
        WanderLiveActivity()
    }
}
