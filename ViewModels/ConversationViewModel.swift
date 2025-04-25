import Foundation

class ConversationViewModel: ObservableObject {
    @Published var conversations: [Conversation] = []

    private let storageURL: URL = {
        let url = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]
            .appendingPathComponent("conversations.json")
        return url
    }()

    init() {
        loadConversations()
    }

    func loadConversations() {
        guard let data = try? Data(contentsOf: storageURL) else { return }
        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        if let loaded = try? decoder.decode([Conversation].self, from: data) {
            conversations = loaded
        }
    }

    func saveConversations() {
        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        if let data = try? encoder.encode(conversations) {
            try? data.write(to: storageURL)
        }
    }

    func addConversation(transcript: String) async {
        let summary = await LLMService.shared.summarize(text: transcript)
        let convo = Conversation(id: UUID(), date: Date(), transcript: transcript, summary: summary)
        DispatchQueue.main.async {
            self.conversations.append(convo)
            self.saveConversations()
        }
    }

    var todaysConversations: [Conversation] {
        let calendar = Calendar.current
        return conversations.filter { calendar.isDateInToday($0.date) }
    }
}