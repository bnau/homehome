import {MiddlewareConsumer, Module, NestModule} from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { MediaSourceService } from './media-source.service';
import { PlayerService } from './player.service';
import {AppLoggerMiddleware} from './app-logger.middleware';

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService, MediaSourceService, PlayerService],
})
export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer): void {
    consumer.apply(AppLoggerMiddleware).forRoutes('*');
  }
}
