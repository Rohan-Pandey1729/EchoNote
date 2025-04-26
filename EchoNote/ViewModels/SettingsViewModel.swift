import Foundation

class SettingsViewModel: ObservableObject {
    @AppStorage("selectedLanguage") var selectedLanguage: String = Locale.current.identifier
    @AppStorage("isDarkMode") var isDarkMode: Bool = false
}

// File: Services/LLMService.swift
import Foundation

class LLMService {
    static let shared = LLMService()
    private init() {}

    func summarize(text: String) async -> String {
        // TODO: integrate local LLM via CoreML or llama.cpp
        // Placeholder stub returns first sentence
        let sentences = text.split(separator: ".")
        return sentences.first.map { String($0) + "." } ?? text
    }
}

