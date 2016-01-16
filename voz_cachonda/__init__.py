import sensors

from time import sleep

from simpleaudio import WaveObject

from .constants import CRITICAL_FILE_NAME, ITER_TIME


def play_critical():
    wave_obj = WaveObject.from_wave_file(CRITICAL_FILE_NAME)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def process_temp():
    print("-" * 50)
    sensors.init()
    critical = False
    try:
        for chip in sensors.ChipIterator():
            for feature in sensors.FeatureIterator(chip):
                subs = list(sensors.SubFeatureIterator(chip, feature))
                critical = None
                current = None
                for sub in subs:
                    value = sensors.get_value(chip, sub.number)
                    if sub.name.endswith(b"input"):
                        current = value
                    if sub.name.endswith(b"crit"):
                        critical_value = value
                name = sensors.get_label(chip, feature)
                print("Current temp for {}: {} / {}".format(name, current,
                                                            critical_value))
                if current >= critical_value:
                    critical = True
        if critical:
            play_critical()
    finally:
        sensors.cleanup()


def main():
    try:
        while True:
            process_temp()
            sleep(ITER_TIME)
    except KeyboardInterrupt:
        print("\nBye")

if __name__ == '__main__':
    main()
