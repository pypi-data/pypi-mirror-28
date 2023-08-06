# tonescale

# setup

```Bash
sudo apt install    \
    libasound-dev   \
    portaudio       \
    python-pyaudio  \
    python3-pyaudio

pip install tonescale
```

# usage

Tonescale provides various sound utilities and capabilities for Python in Linux. It provides a `Sound` class that can store a sound in a NumPy array, can load the sound from a file, can save the sound to a file, and can play the sound using `aplay` or by streaming the sound using PyAudio. Sounds can be added, summed and repeated symbolically. Tonescale includes some sounds.

A tonescale module sound can be accessed in the following way:

```Python
sound_1 = tonescale.access_sound(name = "199935__drzhnn__04-blip")
```

Sounds can be repeated:

```Python
sound_1.repeat(number = 2)
```

Sounds can be added:

```Python
sound_3 = sound_1 + sound_2
```

Sounds can be summed:

```Python
sound_3 = sum([sound_1, sound_2])
```

Sounds can be played:

```Python
sound_1.play()
```

Sounds can be played in the background too:

```Python
sound_1.play(background = True)
```

Sounds can also be played in a stream:

```Python
sound_1.play_stream()
```

Sounds can be saved to files:

```Python
sound_1.save_WAVE()
```

Sounds can be loaded from files:

```Python
sound_1.read_WAVE(filename = "199935__drzhnn__04-blip.wav")
```

See example code for more details.

Tonescale also provides `sound_search.py`, which can search recursively for sound files of a specified minimum duration.
