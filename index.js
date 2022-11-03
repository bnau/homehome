import * as dotenv from 'dotenv'

dotenv.config()

import {getTrackUrls} from "./media-source.js";
import {play} from "./player.js";
import {
    RasaNodeActionServer,
    RasaActionEvent,
} from "rasa-node-action-server";

const rnas = new RasaNodeActionServer();

rnas.define("play_audio_book_action", async (action, res) => {
    console.log(JSON.stringify(action))
    const author = action.tracker.latest_message.entities.filter(e=>e.entity==="author")[0]?.value;

    play(await getTrackUrls(author));

    res.addEvent(
            RasaActionEvent.bot(
                `D'accord, je lance un livre ${author ? 'de ' +author : ''}`
            )
        )
        .send();
});

rnas.start();

