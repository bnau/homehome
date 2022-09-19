import {speech} from './tts.js';
import {getTrackUrls} from "./media-source.js";
import {play} from "./player.js";

import * as dotenv from 'dotenv'
dotenv.config()

let trackUrls = await getTrackUrls("Chateaubriand");

play(trackUrls);

speech('salut! Ça va?')
