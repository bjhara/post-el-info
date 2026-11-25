# Post El Info

This is a simple program to show information about electrical prices,
the next delivery day for Post Nord and today's name day on a 
Raspberry Pi Zero with a Waveshare 1.44inch LCD HAT.

## Requirements

Written for current Raspberry Pi OS (Bookworm or later), which uses the
character device GPIO interface (`/dev/gpiochip*`) instead of the old
sysfs/`/dev/gpiomem` access that `RPi.GPIO` relied on.

1. Enable SPI, e.g. with `sudo raspi-config` (Interface Options → SPI) or by
   adding `dtparam=spi=on` to `/boot/firmware/config.txt`, then reboot.
   `/dev/spidev0.0` should now exist.
2. Install the dependencies (`python3-rpi-lgpio` provides the `RPi.GPIO`
   module on top of lgpio and replaces `python3-rpi.gpio`):

   ```sh
   sudo apt install python3-rpi-lgpio python3-spidev python3-numpy python3-pil python3-requests
   ```

   If installing with pip instead, `spidev` must be version 3.4 or newer
   (for `writebytes2`).

3. Make sure the user running the program is a member of the `gpio` and `spi`
   groups (`sudo usermod -aG gpio,spi $USER`).

Then run `python3 main.py`. `python3 WaveshareLcd.py` shows a test pattern.
