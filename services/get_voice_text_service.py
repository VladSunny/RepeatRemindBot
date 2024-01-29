import speech_recognition as sr
from pydub import AudioSegment
from icecream import ic

recognizer = sr.Recognizer()

converted_voices_path = "converted_voices/converted_voices.wav"


def get_text_from_voice(audio_file: str, lang: str) -> str:
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
    converted_voice_path = audio.export(audio_file, format="wav")

    with sr.AudioFile(converted_voice_path) as source:
        # Записываем данные из файла
        audio_data = recognizer.record(source)

        # Пытаемся распознать речь используя Google Web Speech API
        try:
            text = recognizer.recognize_google(audio_data, language=lang)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Google Speech Recognition could not understand audio"
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
