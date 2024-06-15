import tts
import sys
import preprocess
import pickle


def main(args):
    video_path, audio_path, root = args[1], args[2], args[3]

    with open(root+'/scene.pkl', 'rb') as f:
        scene = pickle.load(f)
    with open(root+'/dialogues.pkl', 'rb') as f:
        dialogues = pickle.load(f)
    with open(root+'/comment.pkl', 'rb') as f:
        comment = pickle.load(f)
    with open(root+'/blank.pkl', 'rb') as f:
        blank = pickle.load(f)
    
    print("\nChecking Blank...")
    final = preprocess.check_blank(scene, dialogues, comment, blank)

    for f in final:
        print(f, '\n')

    print("\nMaking Speech for Comment...")
    tts.main(final, root+'/output/'+audio_path, root+'/input/'+video_path, path=root)

if __name__ == '__main__':
    print(sys.argv)
    main(sys.argv)

