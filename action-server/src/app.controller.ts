import { Body, Controller, Post } from '@nestjs/common';
import { AppService } from './app.service';
import { ActionDto } from './action.dto';
import { ActionResponseDto } from './action-response.dto';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post('*')
  async getHello(@Body() action: ActionDto): Promise<ActionResponseDto> {
    const nextAction = action.next_action;
    console.log(JSON.stringify(action));
    if (nextAction === 'action_play_audio_book') {
      return {
        events: [
          {
            event: 'bot',
            text: await this.appService.readBook(
              action.tracker.latest_message.entities.filter(
                (e) => e.entity === 'author',
              )[0]?.value,
            ),
          },
        ],
      };
    }
    if (nextAction === 'action_store_audio_input') {
      return {
        events: [
          {
            event: 'reset_slots',
          },
          {
            event: 'bot',
            text: `Je switch sur ${action.tracker.slots.audio_input}`,
          },
        ],
      };
    }
    if (nextAction === 'action_annuler') {
      return {
        events: [
          {
            event: 'restart',
          },
        ],
      };
    }
  }
}
