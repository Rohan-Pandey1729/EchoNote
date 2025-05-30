import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import tempfile
import queue
from faster_whisper import WhisperModel
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# === Configuration ===
BLUETOOTH_MIC_INDEX = 0  # Based on your output: Jib True
SAMPLERATE = 16000
CHANNELS = 1

# === Record from Bluetooth mic ===
def record_from_bluetooth(device_index: int, samplerate=16000, channels=1):
    print("🎙️ Recording... Press Ctrl+C to stop.")

    audio_q = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            pass  # Silence warnings
        audio_q.put(indata.copy())

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        dtype='int16',
        callback=callback,
        device=device_index
    )
    stream.start()

    all_audio = []

    try:
        while True:
            data = audio_q.get()
            all_audio.append(data)
    except KeyboardInterrupt:
        stream.stop()
        stream.close()

    audio_np = np.concatenate(all_audio, axis=0)
    temp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    write(temp_wav.name, samplerate, audio_np)
    return temp_wav.name

# === Transcribe audio with Whisper ===
def transcribe_whisper(audio_path):
    model = WhisperModel("base.en", compute_type="int8")
    segments, _ = model.transcribe(audio_path)
    transcript = " ".join([segment.text for segment in segments])
    return transcript.strip()

# === Summarize with Ollama (LLaMA3) ===
llm = Ollama(model="llama3", temperature=0.3)
prompt = PromptTemplate(
    input_variables=["text"],
    template="Summarize the following conversation in a concise paragraph especially taking note of any important points:\n\n{text}\n\nSummary:"
)
summarizer = LLMChain(llm=llm, prompt=prompt)

def summarize(text: str) -> str:
    return summarizer.invoke({"text": text})["text"].strip()

# === Main ===
if __name__ == "__main__":
    wav_path = record_from_bluetooth(device_index=BLUETOOTH_MIC_INDEX, samplerate=SAMPLERATE, channels=CHANNELS)
    transcript = transcribe_whisper(wav_path)
    if transcript:
        summary = summarize(transcript)
        print("\n📌 Summary:", summary)
    else:
        print("⚠️ No transcript detected.")
