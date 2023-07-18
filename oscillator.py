import numpy as np
import sounddevice as sd


# Defined Variables

mid_c_frequency = 261.625565

default_sample_rate = 44100

# Helper Functions


def direction(start, end):
    """Return 1 if end > start, -1 if end < start. (Keeps values consistent instead of sliding up or down)"""
    return 1 if end > start else -1


def pitch_to_frequency(pitch):
    """Frequency of pitch relative to Middle C"""
    return mid_c_frequency * 2 ** (pitch / 12)


def decibels_to_amplitude_ratio(decibels):
    """Ratio between two amplitudes given a decibel change"""
    return 2 ** (decibels / 10)


def interval_to_frequency_ratio(interval):
    return 2 ** (interval / 12)


def frames_to_time(frames, framerate):
    """Convert frame count to time"""
    return frames / framerate


def frames_to_time_array(start_frame, frames, framerate):
    """Convert frame information into time array"""

    # Frame info to time info
    start_time = frames_to_time(start_frame, framerate)
    end_time = frames_to_time(start_frame + frames, framerate)

    # Create time array with one entry for each frame
    time_array = np.linspace(start_time, end_time, frames, endpoint=False)
    return time_array

class Oscillator():
    """Generates continious sine wave data"""

    def __init__(
        self, pitch=0, decibels=1, decibels_per_second=1, samplerate=default_sample_rate
    ):
        self.frequency = pitch_to_frequency(pitch)
        self.phase = 0
        self.amplitude = decibels_to_amplitude_ratio(decibels)

        self.pitch_per_second = 12
        self.decibels_per_second = 1
        self.goal_frequency = self.frequency
        self.goal_amplitude = self.amplitude
        self.samplerate = samplerate

        # Create the output stream
        self.output_stream = sd.OutputStream(
            channels=1,
            callback=lambda *args: self._callback(*args),
            samplerate=samplerate,
        )

    def set_pitch(self, value):
        """Changes pitch of the oscillator"""
        self.frequency = pitch_to_frequency(value)
        self.goal_frequency = self.frequency

    def new_frequency_array(self, time_array):
        """Calculate the frequency values for the next chunk of data"""
        dir = direction(self.frequency, self.goal_frequency)
        new_frequency = self.frequency * interval_to_frequency_ratio(
            dir * self.pitch_per_second * time_array
        )
        return new_frequency

    def new_amplitude_array(self, time_array):
        """Calculate amiplitude values for next chunck of data"""
        dir = direction(self.amplitude, self.goal_amplitude)
        new_amplitude = self.amplitude * decibels_to_amplitude_ratio(
            dir * self.decibels_per_second * time_array
        )
        return new_amplitude

    def new_phase_array(self, new_frequency_array, delta_time):
        """Calculate phase values for next chunk of data"""
        return self.phase + np.cumsum(new_frequency_array * delta_time)

    def next_data(self, frames):
        """Get the next pressure array for the given number of frames"""

        # Convert frame information to time information
        time_array = frames_to_time_array(0, frames, self.samplerate)
        # delta time = elapsed time
        delta_time = time_array[1] - time_array[0]

        # Calculate the frequencies, phases, and amplitudes of this batch of data
        new_frequency_array = self.new_frequency_array(time_array)
        new_phase_array = self.new_phase_array(new_frequency_array, delta_time)
        new_amplitude_array = self.new_amplitude_array(time_array)

        # Create the sinewave array
        sinewave_array = new_amplitude_array * np.sin(2 * np.pi * new_phase_array)

        # Update phase to prevent overflow error
        self.phase = new_phase_array[-1] % 1

        return sinewave_array

    def _callback(self, outdata, frames, time, status):
        """Callback function for the output stream"""
        if status:
            print(status, file=sys.stderr)

        # Get and use the sinewave's next batch of data
        data = self.next_data(frames)
        outdata[:] = data.reshape(-1, 1)

    def play(self):
        """Plays the sinewave"""
        self.output_stream.start()

    def stop(self):
        """Stops playing wave"""
        self.output_stream.stop()