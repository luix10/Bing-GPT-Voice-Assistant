import asyncio
import re
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
from google.cloud import texttospeech
from playsound import playsound
import os
import json

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'service-account.json'

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
    
async def main2():
    while True:
        user_input = input("Digite o que quer do Edge: ")
        bot = Chatbot(cookie_path='cookies.json')
        response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)
        # Select only the bot response from the response dictionary
        for message in response["item"]["messages"]:
            if message["author"] == "bot":
                bot_response = message["text"]
        # Remove [^#^] citations in response
        bot_response = re.sub('\[\^\d+\^\]', '', bot_response)
        print("Bot's response:", bot_response)
        reproduzir_audio_cloud(bot_response)
        await bot.close()

async def main():
    user_input = input("Digite o que quer do Edge: ")
	
    bot = await Chatbot.create() # Passing cookies is "optional", as explained above
    bot_response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise, simplify_response=True)
    # print(json.dumps(bot_response, indent=4)) # Returns
    """
{
    "text": str,
    "author": str,
    "sources": list[dict],
    "sources_text": str,
    "suggestions": list[str],
    "messages_left": int
}
    """
    # Remove [^#^] citations in response
    bot_response = re.sub('\[\^\d+\^\]', '', bot_response['text'])
    print("Bot's response:", bot_response)
    reproduzir_audio_cloud(bot_response)
    await bot.close()
	
if __name__ == "__main__":
    asyncio.run(main())