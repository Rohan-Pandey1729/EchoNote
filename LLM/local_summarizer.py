import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import tempfile
from faster_whisper import WhisperModel
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# === Step 1: Record audio ===
def record_audio(duration=20, samplerate=16000):
    print(f"🎙️ Recording for {duration} seconds...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("✅ Recording complete.")
    
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_wav.name, samplerate, audio)
    return temp_wav.name

# === Step 2: Transcribe using Whisper ===
def transcribe_whisper(audio_path):
    print("🔍 Transcribing using Whisper...")
    model = WhisperModel("base.en", compute_type="int8")  # You can use "medium", "small", etc.
    segments, _ = model.transcribe(audio_path)
    transcript = " ".join([segment.text for segment in segments])
    return transcript.strip()

# === Step 3: Summarize using Ollama (LLaMA3) ===
llm = Ollama(model="llama3", temperature=0.3)
prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following conversation in a concise paragraph:\n\n{text}\n\nSummary:"
)
summarizer = LLMChain(llm=llm, prompt=prompt)

def summarize(text: str) -> str:
    return summarizer.run(text=text).strip()

# === Main ===
if __name__ == "__main__":
    # Change below duration as needed
    wav_path = record_audio(duration=10)
    transcript = transcribe_whisper(wav_path)
    
    print("\n🗣️ Transcript:\n", transcript)
    
    if transcript:
        summary = summarize(transcript)
        print("\n📌 Summary:\n", summary)
    else:
        print("⚠️ Could not transcribe audio.")
