import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            ConversationsView()
                .tabItem { Label("Conversations", systemImage: "bubble.left.and.bubble.right") }
            SettingsView()
                .tabItem { Label("Settings", systemImage: "gear") }
        }
    }
}