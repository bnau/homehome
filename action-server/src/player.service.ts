import * as player from 'chromecast-player';
import { Injectable } from '@nestjs/common';

@Injectable()
export class PlayerService {
  private player;

  constructor() {
    this.player = player();
    this.player.use((ctx, next) => {
      ctx.on('status', (status, memo) => {
        console.log(`Status: ${status}`);
        console.log(`Memo: ${memo}`);
      });
      next();
    });

    this.player.use((ctx, next) => {
      ctx.options = { ...ctx.options, ...ctx.options.playlist[0] };
      let file = ctx.options.playlist.shift();
      ctx.options.playlist_history = [file];
      next();
    });
  }

  play(trackUrls) {
    this.player.launch(
      {
        address: process.env.CHROMECAST_IP,
        myip: process.env.SERVER_IP,
        playlist: trackUrls.map((path) => ({ path, type: "audio/mpeg" })),
      },
      (err, p, ctx) => {
        if (err) {
          console.error('player error', err);
        }

        let playlist = ctx.options.playlist;
        let playlist_history = ctx.options.playlist_history;

        ctx.once('closed', () => {
          console.log('closed');
        });

        p.on('position', (pos) => {
          console.log(`Position: ${JSON.stringify(pos)}`);
        });

        let updateTitle = () => {
          p.getStatus((err, status) => {
            console.log(`Status: ${status}`);
          });
        };

        let initialSeek = () => {
          // let seconds = 0;
          // p.seek(seconds);
        };

        p.on('playing', updateTitle);

        p.once('playing', initialSeek);

        updateTitle();

        let nextInPlaylist = () => {
          if (playlist.length) {
            p.stop(() => {
              p.load(playlist[0], () => {});
              let file = playlist.shift();
              if (ctx.options.loop) {
                playlist.push(file);
              } else {
                playlist_history.push(file);
              }
            });
          }
        };

        let l;
        p.on('status', (status, memo) => {
          console.log(`status: ${status}`);
          console.log(`memo: ${memo}`);
          if (status.playerState !== 'IDLE') return;
          if (status.idleReason !== 'FINISHED') return;
          if (memo && memo.playerState === 'IDLE') return;
          nextInPlaylist();
          return status;
        });
      },
    );
  }
}
