from gtts import gTTS

def main(comment):
    for cm in comment:
        for t in cm["fi_com"]:
            tts = gTTS(text=t, lang='ko')
            tts.save("comment"+t+".wav")