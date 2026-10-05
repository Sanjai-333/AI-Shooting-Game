import wave
import math
import struct
import os

SAMPLE_RATE = 44100


def create_sound(filename, duration, start_freq, end_freq):
    folder = os.path.join("assets", "sounds")
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    samples = int(SAMPLE_RATE * duration)

    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)

        for i in range(samples):
            progress = i / samples

            frequency = (
                start_freq
                + (end_freq - start_freq) * progress
            )

            envelope = 1.0 - progress

            value = int(
                16000
                * envelope
                * math.sin(
                    2 * math.pi
                    * frequency
                    * i
                    / SAMPLE_RATE
                )
            )

            wav.writeframes(
                struct.pack("<h", value)
            )

    print("Created:", path)


# Player shooting sound
create_sound(
    "player_shoot.wav",
    0.12,
    900,
    180
)

# Enemy shooting sound
create_sound(
    "enemy_shoot.wav",
    0.15,
    500,
    100
)

# Hit sound
create_sound(
    "hit.wav",
    0.10,
    250,
    80
)

print("\nAll sound files created successfully!")