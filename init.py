import denoise
import sts
import stt
import pickle
import sys

def save(result, result2=None):
    with open('temp_list.pkl', 'wb') as f:
        pickle.dump(result+"\n"+"-"*300+"\n", f)
        pickle.dump(result2, f)

def main(args):
    if len(args) > 2:
        sys.exit("Wrong Arguments Numbers")

    print("Enter the input file")
    path = input()

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
    sts.__main__(dialogues)

if __name__ == '__main__':
    main(sys.argv)