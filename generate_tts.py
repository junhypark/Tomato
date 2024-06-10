import tts
import sys
import preprocess
import pickle


def main(args):
    with open('scene.pkl', 'rb') as f:
        scene = pickle.load(f)
    with open('dialogues.pkl', 'rb') as f:
        dialogues = pickle.load(f)
    with open('comment.pkl', 'rb') as f:
        comment = pickle.load(f)
    with open('blank.pkl', 'rb') as f:
        blank = pickle.load(f)

    video_path, audio_path = args[1], args[2]
    
    print("\nChecking Blank...")
    final = preprocess.check_blank(scene, dialogues, comment, blank)

    for f in final:
        print(f, '\n')

    print("\nMaking Speech for Comment...")
    tts.main(final, 'output/'+audio_path, 'input/'+video_path)

if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)

