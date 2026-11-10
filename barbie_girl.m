clear;
clc;

FS = 44100;
TOTAL_TIME = 15.0;
BPM = 130;
BEAT = 60 / BPM;

NOTES = containers.Map( ...
    {'си3', 'до#4', 'ре#4', 'ми4', 'фа#4', ...
     'соль#4', 'ля4', 'си4', 'до#5'}, ...
    [246.94, 277.18, 311.13, 329.63, 369.99, ...
     415.30, 440.00, 493.88, 554.37]);

MELODY = {
    % I'm a Barbie girl
    'соль#4', 0.5;
    'ми4',    0.5;
    'соль#4', 0.5;
    'до#5',   0.5;
    'ля4',    2.0;

    % In the Barbie world
    'фа#4',   0.5;
    'ре#4',   0.5;
    'фа#4',   0.5;
    'си4',    0.5;
    'соль#4', 1.0;
    'фа#4',   0.5;
    'ми4',    1.0;
    'до#4',   2.0;

    % Life in plastic
    'ми4',    0.5;
    'до#4',   0.5;
    'фа#4',   2.0;
    'до#4',   1.0;
    'си3',    2.0;

    % It's fantastic
    'фа#4',   0.5;
    'ми4',    0.5;
    'соль#4', 2.0;
    'си4',    1.0;
    'фа#4',   2.0;
};

target_samples = floor(FS * TOTAL_TIME);
signal = {};
note_names = {};
current_samples = 0;
p = 0.0;

while current_samples < target_samples
    for k = 1:size(MELODY, 1)
        note_name = MELODY{k, 1};
        beats = MELODY{k, 2};
        samples = floor(FS * beats * BEAT);
        time = (0:samples - 1)' / FS;

        frequency = NOTES(note_name);
        note = sin(2 * pi * frequency * time + p);
        p = mod(p + 2 * pi * frequency * samples / FS, 2 * pi);

        signal{end + 1, 1} = note;
        note_names{end + 1, 1} = note_name;
        current_samples = current_samples + samples;

        if current_samples >= target_samples
            break;
        end
    end
end

audio = vertcat(signal{:});
audio = audio(1:target_samples);  % Ровно 15 секунд

player = audioplayer(audio, FS);
playblocking(player);
