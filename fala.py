from google.cloud import texttospeech
from playsound import playsound
import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account.json'

def listar_vozes_cloud():
    # Cria um cliente do Text-to-Speech
    client = texttospeech.TextToSpeechClient()
    
    # Lista as vozes disponíveis
    response = client.list_voices(language_code='pt-BR')
    print(response)
    
    # Itera sobre as vozes em português do Brasil
    for voice in response.voices:
        print(f"Nome: {voice.name}")
        print(f"Linguagem: {voice.language_codes[0]}")
        print(f"Tipo: {voice.ssml_gender.name}")
        print(f"ID: {voice.name}\n")

def reproduzir_audio_cloud(texto):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=texto)

    voice = texttospeech.VoiceSelectionParams(
        language_code='pt-BR', name='pt-BR-Neural2-B', ssml_gender=texttospeech.SsmlVoiceGender.MALE
		#language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    arquivo_audio = "cloud.mp3"
	
    with open(arquivo_audio, 'wb') as out:
        out.write(response.audio_content)
        #print(f'Áudio salvo em: {arquivo_audio}')

    playsound(arquivo_audio)

def main():
    # listar_vozes_cloud();
	
    texto = input("Digite o texto que deseja reproduzir: ")
    reproduzir_audio_cloud(texto)

if __name__ == '__main__':
    main()
