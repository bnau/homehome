import {speech} from './tts.js';
import {getTrackUrls} from "./media-source.js";
import {play} from "./player.js";

import * as dotenv from 'dotenv'

dotenv.config()

play(await getTrackUrls("Chateaubriand"));

speech('salut! Ça va?')
