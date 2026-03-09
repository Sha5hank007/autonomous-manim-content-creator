# tts_client.py
import asyncio
import os
import edge_tts


async def _synth(text: str, output_path: str, voice: str, rate: str):
    communicator = edge_tts.Communicate(text, voice, rate=rate)
    await communicator.save(output_path)


def synthesize_to_temp_mp3(text: str,
                           run_audio_dir: str,
                           filename: str,
                           voice: str = "en-US-JennyNeural",
                           rate: str = "+0%"):

    os.makedirs(run_audio_dir, exist_ok=True)
    output_path = os.path.join(run_audio_dir, filename)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(_synth(text, output_path, voice, rate))
    loop.close()

    return output_path
