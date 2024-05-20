from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

def main(path):
    input_path = './input/'+path

    ans = pipeline(
        Tasks.acoustic_noise_suppression,
        model='damo/speech_frcrn_ans_cirm_16k')
    
    result = ans(
        input_path,
        output_path='./output/denoise_'+path)
    
    return './output/denoise_'+path