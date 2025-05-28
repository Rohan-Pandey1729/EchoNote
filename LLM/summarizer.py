import speech_recognition as sr
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# === Set up LangChain with Ollama ===
llm = Ollama(
    model="llama3",  # Or any other model you've pulled with `ollama pull`
    temperature=0.3
)

# === Prompt Template for summarization ===
prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following conversation in a concise paragraph:\n\n{text}\n\nSummary:"
)

summarizer = LLMChain(llm=llm, prompt=prompt)

# === Microphone Input ===
def transcribe_from_mic() -> str:
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    print("🎤 Listening... Speak clearly.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    print("📝 Transcribing...")
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "[Could not understand the audio]"
    except sr.RequestError as e:
        return f"[Google API error: {e}]"

# === Summary Function ===
def summarize(text: str) -> str:
    return summarizer.run(text=text).strip()

# === Main ===
if __name__ == "__main__":
    transcript = transcribe_from_mic()
    print("\n🗣️ Transcript:\n", transcript)

    if transcript and not transcript.startswith('['):
        summary = summarize(transcript)
        print("\n📌 Summary:\n", summary)
    else:
        print("⚠️ Skipping summarization due to transcription error.")
