# import denoise
import subprocess
import sts
import stt
import pickle
import sys
import translate_file
import timing
# import tts
import preprocess

def save(result, result2=None):
    with open('temp_list.pkl', 'wb') as f:
        pickle.dump(result, f)
        pickle.dump(result2, f)

def main(args):
    if len(args) > 4: # default len(args) == 1, because of args[0] == "init.py" 
        sys.exit("Wrong Arguments Numbers")

    # print("Enter the input video file")
    video_path, docx_path, audio_path = args[1], args[2], args[3]

    # open docx and wav
    path, docx = translate_file.main(video_file=video_path, docx_file=docx_path, audio_file=audio_path)

    # print("\nDenoising is running...")
    # audio_path = denoise.main(path)

    # print("\nPyannote is running...")
    subprocess.run(["echo", "\nPyannote is running..."])
    blank, re_time = timing.main('./output/'+audio_path)

    # print("\nSpeech To Text is running...")
    subprocess.run(["echo", "\nSpeech To Text is running..."])
    dialogues = stt.main('./output/'+audio_path, re_time)

    # try:
    #     if sys.argv[1]:
    #         if "-c" in sys.argv or "--check" in sys.argv:
    #             print("\nFor chekcing!")
    #             print(docx)
    #         elif "--saveoutput" in sys.argv or "-s" in sys.argv:
    #             print("\nStoring dialogues")
    #             save(dialogues)
    #         elif "--savedictionary" in sys.argv or "-sd" in sys.argv:
    #             print("\nStoring dialogues and dictionary")
    #             save(dialogues, result2=docx)
    #         else:
    #             pass
    # except IndexError:
    #     pass

    subprocess.run(["echo", "\nPreprocessing..."])
    scene = preprocess.main(docx)

    temp = ''
    for di in dialogues:
        temp += '\n'+di["text"]
    subprocess.run(["echo", "\nChecking similarity..."])

    comment = sts.main(docx, temp)
 
    with open("scene.pkl", 'wb') as f:
        pickle.dump(scene, f)

    with open("dialogues.pkl", 'wb') as f:
        pickle.dump(dialogues, f)
    
    with open("comment.pkl", "wb") as f:
        pickle.dump(comment, f)
    
    with open("blank.pkl", "wb") as f:
        pickle.dump(blank, f)

    # print("\nChecking Blank...")
    # final = preprocess.check_blank(scene, dialogues, comment, blank)

    # for f in final:
    #     print(f, '\n')

    # print("\nMaking Speech for Comment...")
    # tts.main(final, './output/'+audio_path, './input/'+video_path)

if __name__ == '__main__':
    main(sys.argv)