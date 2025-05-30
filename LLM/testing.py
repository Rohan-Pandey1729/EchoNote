import sounddevice as sd

devices = sd.query_devices()
for idx, d in enumerate(devices):
    print(f"[{idx}] {d['name']} — Input Channels: {d['max_input_channels']}")
