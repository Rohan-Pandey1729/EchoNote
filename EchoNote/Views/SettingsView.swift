import SwiftUI

struct SettingsView: View {
    @StateObject private var viewModel = SettingsViewModel()
    let supportedLanguages = ["en", "es", "fr", "de", "zh"]

    var body: some View {
        NavigationView {
            Form {
                Picker("Language", selection: $viewModel.selectedLanguage) {
                    ForEach(supportedLanguages, id: \.self) { lang in
                        Text(Locale.current.localizedString(forIdentifier: lang) ?? lang).tag(lang)
                    }
                }
                Toggle("Dark Mode", isOn: $viewModel.isDarkMode)
            }
            .navigationTitle("Settings")
        }
    }
}
