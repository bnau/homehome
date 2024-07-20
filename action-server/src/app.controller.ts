import { Body, Controller, Post } from '@nestjs/common';
import { AppService } from './app.service';
import { ActionDto } from './action.dto';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post('*')
  async getHello(@Body() action: ActionDto): Promise<string> {
    const nextAction = action.next_action;
    console.log(JSON.stringify(action));
    if (nextAction === 'action_play_audio_book') {
      return await this.appService.readBook(action.author);
    }
    if (nextAction === 'action_store_audio_input') {
      return `Je switch sur ${action.audio_input}`;
    }
  }
}
