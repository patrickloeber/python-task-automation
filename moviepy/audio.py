from moviepy.editor import AudioFileClip

def extract_audio():
    audio = AudioFileClip("test.mp4")
    audio.write_audiofile("test.mp3", 44100)  # fps


if __name__ == '__main__':
    extract_audio()
