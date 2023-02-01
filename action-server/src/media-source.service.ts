import * as dotenv from 'dotenv';

dotenv.config();

import apiClient from '../emby-api/apiclient.js';
import storage from '../emby-api/appstorage-memory.js';
import wakeonlan from '../emby-api/wakeonlan.js';
import { Injectable } from '@nestjs/common';

@Injectable()
export class MediaSourceService {
  private emby;

  constructor() {
    this.emby = new apiClient(
      new storage(),
      wakeonlan,
      `http://${process.env.EMBY_IP}:8096`,
      'test',
      '1.0.0',
      'device',
      '1',
    );
    this.authentificate().finally();
  }

  private async authentificate() {
    const auth = await this.emby.authenticateUserByName(
      process.env.EMBY_USER,
      process.env.EMBY_PASSWORD,
    );
    this.emby.setAuthenticationInfo(auth.AccessToken, auth.User.Id);
  }

  async getTrackUrls(authorName) {
    let currentUserId = this.emby.getCurrentUserId();
    const artists = await this.emby.getItems(currentUserId, {
      searchTerm: authorName,
      includeItemTypes: 'MusicArtist',
      recursive: true,
    });

    const albums = await this.emby.getItems(currentUserId, {
      ListItemIds: artists.Items[0].Id,
      includeItemTypes: 'Playlist',
      recursive: true,
    });

    const tracks = await this.emby.getItems(currentUserId, {
      ParentId: albums.Items[0].Id,
      recursive: true,
    });

    return Promise.all(
      tracks.Items.map(async (it) =>
        this.emby.getAudioStreamUrl({ Id: it.Id }, {}),
      ),
    );
  }
}
