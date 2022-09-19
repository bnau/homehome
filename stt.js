import speech from "@google-cloud/speech";
import fs from "fs";

const client = new speech.SpeechClient();
export async function listen(filePath) {
    const audio = {
        content: fs.readFileSync(filePath).toString('base64'),
    };
    const config = {
        encoding: 'OGG_OPUS',
        sampleRateHertz: 48000,
        languageCode: 'fr-FR',
    };
    const request = {
        audio,
        config,
    };

    // Detects speech in the audio file
    const [response] = await client.recognize(request);
    const transcription = response.results
        .map(result => result.alternatives[0].transcript)
        .join('\n');
    console.log(`Transcription: ${transcription}`);
    console.log(`Response: ${JSON.stringify(response)}`);
}
