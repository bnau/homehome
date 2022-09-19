import {spawn} from "child_process";

export function speech(message) {
    const python = spawn('python', ['tts/main.py', message]);

    let uint8arrayToString = function(data){
        return String.fromCharCode.apply(null, data);
    };

    python.stdout.on('data', (data) => {
        console.log(uint8arrayToString(data));
    });

// Handle error output
    python.stderr.on('data', (data) => {
        // As said before, convert the Uint8Array to a readable string.
        console.log(uint8arrayToString(data));
    });

}
