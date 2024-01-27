import azure.cognitiveservices.speech as speechsdk
import json

def extract_pronunciation_data(data, threshold=100):
    data = json.loads(data)

    result = {
        'display_text': data['DisplayText'],
        'snr': data['SNR'],
        'confidence': data['NBest'][0]['Confidence'],
        'pronunciation_scores': data['NBest'][0]['PronunciationAssessment'],
        'phonemes_below_threshold': [],
        'words_below_threshold': []
    }

    for word in data['NBest'][0]['Words']:
        word_score = word['PronunciationAssessment'].get('AccuracyScore', 100)
        if word_score < threshold:
            result['words_below_threshold'].append({'word': word['Word'], 'score': word_score})

        for phoneme in word['Phonemes']:
            phoneme_score = phoneme['PronunciationAssessment'].get('AccuracyScore', 100)
            if phoneme_score < threshold:
                result['phonemes_below_threshold'].append({'phoneme': phoneme['Phoneme'], 'score': phoneme_score})

    return result

def get_pronunciation_assessment():

    subscription_key, service_region = "a46aa1fcb8034f6087ff18d5c398a0f4", "eastus"
    # Set up the subscription info for the Speech Service:
    weatherfilename = "uploads/whatstheweatherlike.wav"
    reference_text = "What's the weather like?"

    # Create an instance of a speech config with specified subscription key and service region.
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

    # The language of the speech recognition.
    speech_config.speech_recognition_language="en-GB"

    # Create an audio configuration that points to your .wav file.
    audio_input = speechsdk.audio.AudioConfig(filename=weatherfilename)


    # Create a pronunciation assessment config, specifying the grading system, granularity, etc.
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(reference_text=reference_text, grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark, granularity=speechsdk.PronunciationAssessmentGranularity.Phoneme)

    # Creates a recognizer with the given settings
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_input)

    # Apply the pronunciation assessment configuration to the speech recognizer.
    pronunciation_config.apply_to(speech_recognizer)

    # Start pronunciation assessment.
    result = speech_recognizer.recognize_once()

    # Check the result
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print(f"Recognized: {result.text}")
        # print(f"Pronunciation assessment results: {result.properties[speechsdk.PropertyId.SpeechServiceResponse_JsonResult]}")
        print(extract_pronunciation_data(result.properties[speechsdk.PropertyId.SpeechServiceResponse_JsonResult], 90))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized")
    else:
        print(f"Speech Recognition canceled: {result.cancellation_details.reason}")
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print(f"Error details: {result.cancellation_details.error_details}")


get_pronunciation_assessment()