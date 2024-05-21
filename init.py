import denoise
import sts
import stt
import pickle
import sys
import translate_file

def save(result, result2=None):
    with open('temp_list.pkl', 'wb') as f:
        pickle.dump(result+"\n"+"-"*300+"\n", f)
        pickle.dump(result2, f)

def main(args):
    if len(args) > 2:
        sys.exit("Wrong Arguments Numbers")

    print("Enter the input video file")
    video_path = input()
    
    print("\n Enter the input docx file")
    docx_path = input()

    print("\n Enter the name of wav file")
    audio_path = input()

    # open docx and wav
    path, docx = translate_file.main(video_file=video_path, audio_file=audio_path, docx_file=docx_path)

    print("\nDenoising is running...")
    first_path = denoise.main(path)

    print("\nSpeech To Text is running...")
    dialogues, dialoguesList = stt.main(first_path)

    if sys.argv[1]:
        if "-c" in sys.argv or "--check" in sys.argv:
            print("\nFor chekcing!")
            print(dialoguesList)
        elif "--saveoutput" in sys.argv or "-s" in sys.argv:
            print("\nStoring dialogues")
            save(dialogues)
        elif "--savedictionary" in sys.argv or "-sd" in sys.argv:
            print("\nStoring dialogues and dictionary")
            save(dialogues, result2=dialoguesList)

    print("\nChecking Similarities...")
    sts.main(dialogues, docx)

if __name__ == '__main__':
    main(sys.argv)