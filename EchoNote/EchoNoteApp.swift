import SwiftUI

@main
struct EchoNoteApp: App {
    @AppStorage("isDarkMode") private var isDarkMode: Bool = false

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.locale, Locale(identifier: UserDefaults.standard.string(forKey: "selectedLanguage") ?? Locale.current.identifier))
                .preferredColorScheme(isDarkMode ? .dark : .light)
        }
    }
}