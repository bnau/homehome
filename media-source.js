import apiClient from "./emby-api/apiclient.js";
import storage from "./emby-api/appstorage-memory.js";
import wakeonlan from "./emby-api/wakeonlan.js";
import * as dotenv from 'dotenv'
dotenv.config()


const emby = new apiClient(
    new storage(),
    wakeonlan,
    `http://${process.env.EMBY_IP}:8096`,
    "test",
    "1.0.0",
    "device",
    "1"
);

const auth = await emby.authenticateUserByName(process.env.EMBY_USER, process.env.EMBY_PASSWORD);
emby.setAuthenticationInfo(auth.AccessToken, auth.User.Id);

let currentUserId = emby.getCurrentUserId();
export const getTrackUrls = async (authorName) => {
    const artists = await emby.getItems(currentUserId, {
        searchTerm: authorName,
        includeItemTypes: "MusicArtist",
        recursive: true,
    });

    const albums = await emby.getItems(currentUserId, {
        ListItemIds: artists.Items[0].Id,
        includeItemTypes: "Playlist",
        recursive: true,
    });

    const tracks = await emby.getItems(currentUserId, {
        ParentId: albums.Items[0].Id,
        recursive: true,
    });

    return Promise.all(
        tracks.Items.map(async (it) => emby.getAudioStreamUrl({ Id: it.Id }, {}))
    );
};
