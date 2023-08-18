import * as bsp from 'bluetooth-serial-port';

import { Injectable } from '@nestjs/common';
import * as process from 'process';

@Injectable()
export class SwitchAudioService {
  constructor() {
    const btSerial = new bsp.BluetoothSerialPort();
    const address = process.env.SWITCH_AUDIO_ADDRESS;
    try {
        btSerial.findSerialPortChannel(
            address,
            function (channel) {
                btSerial.connect(
                    address,
                    channel,
                    function () {
                        console.log('connected');

                        btSerial.write(Buffer.from('my data', 'utf-8'), function (err) {
                            if (err) console.log(err);
                        });

                        btSerial.on('data', function (buffer) {
                            console.log(buffer.toString('utf-8'));
                        });
                    },
                    function () {
                        console.log('cannot connect');
                    },
                );

                btSerial.close();
            },
            function () {
                console.log('found nothing');
            },
        );
    } catch (error) {
        console.error(error);
    }
  }
}
