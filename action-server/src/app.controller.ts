import {Body, Controller, Post, RequestMapping} from '@nestjs/common';
import { AppService } from './app.service';
import { ActionDto } from './action.dto';
import { ActionResponseDto } from './action-response.dto';

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Post("*")
  async getHello(@Body() action: ActionDto): Promise<ActionResponseDto> {
    console.log(JSON.stringify(action));
    return {
      events: [
        {
          event: 'bot',
          text: await this.appService.getHello(action),
        },
      ],
    };
  }
}
