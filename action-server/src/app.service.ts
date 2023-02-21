import { Injectable } from '@nestjs/common';
import { MediaSourceService } from './media-source.service';
import { PlayerService } from './player.service';

@Injectable()
export class AppService {
  constructor(
    private readonly mediaSourceService: MediaSourceService,
    private readonly playerService: PlayerService,
  ) {}
  async readBook(author: String): Promise<string> {
    this.playerService.play(await this.mediaSourceService.getTrackUrls(author));

    return `D'accord, je lance un livre ${author ? 'de ' + author : ''}`;
  }
}
