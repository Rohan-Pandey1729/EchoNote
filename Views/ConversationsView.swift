import SwiftUI

struct ConversationsView: View {
    @StateObject private var viewModel = ConversationViewModel()
    @State private var newTranscript: String = ""

    var body: some View {
        NavigationView {
            VStack {
                List {
                    ForEach(viewModel.todaysConversations) { convo in
                        VStack(alignment: .leading) {
                            Text(convo.transcript)
                                .font(.body)
                                .lineLimit(2)
                            Text(convo.summary)
                                .font(.subheadline)
                                .foregroundColor(.gray)
                        }
                        .padding(.vertical, 4)
                    }
                }
                HStack {
                    TextField("New transcript...", text: $newTranscript)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                    Button(action: {
                        Task {
                            await viewModel.addConversation(transcript: newTranscript)
                            newTranscript = ""
                        }
                    }) {
                        Image(systemName: "plus.circle.fill")
                            .font(.title)
                    }
                    .disabled(newTranscript.isEmpty)
                }
                .padding()
            }
            .navigationTitle("Today's Conversations")
        }
    }
}
