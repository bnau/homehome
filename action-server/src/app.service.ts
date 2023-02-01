import { Injectable } from '@nestjs/common';
import { ActionDto } from './action.dto';
import { MediaSourceService } from './media-source.service';
import { PlayerService } from './player.service';

@Injectable()
export class AppService {
  constructor(
    private readonly mediaSourceService: MediaSourceService,
    private readonly playerService: PlayerService,
  ) {}
  async getHello(action: ActionDto): Promise<string> {
    const author = action.tracker.latest_message.entities.filter(
      (e) => e.entity === 'author',
    )[0]?.value;

    this.playerService.play(await this.mediaSourceService.getTrackUrls(author));

    return `D'accord, je lance un livre ${author ? 'de ' + author : ''}`;
  }
}
