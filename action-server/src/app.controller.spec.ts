import { Test, TestingModule } from '@nestjs/testing';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MediaSourceService } from './media-source.service';

describe('AppController', () => {
  let appController: AppController;

  beforeEach(async () => {
    const app: TestingModule = await Test.createTestingModule({
      controllers: [AppController],
      providers: [AppService, MediaSourceService],
    }).compile();

    appController = app.get<AppController>(AppController);
  });

  describe('root', () => {
    it.skip('should return "Hello World!"', () => {
      expect(appController.getHello({
        domain: {
          config: undefined,
          session_config: undefined,
          intents: [],
          entities: [],
          slots: undefined,
          responses: undefined,
          actions: [],
          forms: undefined,
          e2e_actions: []
        },
        next_action: '',
        tracker: {
          sender_id: '',
          slots: undefined,
          latest_message: {
            intent: undefined,
            entities: [],
            text: '',
            message_id: '',
            metadata: undefined,
            intent_ranking: [],
            response_selector: undefined
          },
          latest_event_time: 0,
          followup_action: undefined,
          paused: false,
          events: [],
          latest_input_channel: '',
          active_loop: undefined,
          latest_action: {
            action_name: ''
          },
          latest_action_name: ''
        },
        sender_id: '',
        version: ''
      })).toBe('Hello World!');
    });
  });
});
