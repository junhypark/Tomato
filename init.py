import subprocess
import sts
import stt
import pickle
import sys
import translate_file
import timing
import preprocess

def main(args):
    if len(args) > 5: # default len(args) == 1, because of args[0] == "init.py" 
        sys.exit("Wrong Arguments Numbers")

    # print("Enter the input video file")
    root, video_path, docx_path, audio_path= args[1], args[2], args[3], args[4]

    # open docx and wav
    path, docx = translate_file.main(video_file=video_path, docx_file=docx_path, audio_file=audio_path, path=root)

    # print("\nPyannote is running...")
    subprocess.run(["echo", "\nPyannote is running..."])
    blank, re_time = timing.main(root+'/output/'+audio_path, root=root)

    # print("\nSpeech To Text is running...")
    subprocess.run(["echo", "\nSpeech To Text is running..."])
    dialogues = stt.main(root+'/output/'+audio_path, re_time, root)

    subprocess.run(["echo", "\nPreprocessing..."])
    scene = preprocess.main(docx)

    temp = ''
    for di in dialogues:
        temp += '\n'+di["text"]
    subprocess.run(["echo", "\nChecking similarity..."])

    comment = sts.main(docx, temp)
 
    with open(root+"/scene.pkl", 'wb') as f:
        pickle.dump(scene, f)

    with open(root+"/dialogues.pkl", 'wb') as f:
        pickle.dump(dialogues, f)
    
    with open(root+"/comment.pkl", "wb") as f:
        pickle.dump(comment, f)
    
    with open(root+"/blank.pkl", "wb") as f:
        pickle.dump(blank, f)

if __name__ == '__main__':
    main(sys.argv)