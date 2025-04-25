import Foundation

struct Conversation: Identifiable, Codable {
    let id: UUID
    let date: Date
    let transcript: String
    var summary: String
}