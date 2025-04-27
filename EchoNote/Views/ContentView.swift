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

// at the bottom of ContentView.swift

#if DEBUG
struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
            .environmentObject(ConversationViewModel())   // so you have live data
            .environmentObject(SettingsViewModel())
    }
}
#endif
