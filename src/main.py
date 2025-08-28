import os.path
import shutil

from enum import Enum

class Sound_set:
    def __init__(self, filenames: list[str], formats: list[str]):
        self.filenames = filenames
        self.formats = formats

DRUM_SET = Sound_set(
    [
        "drum-hitnormal",
        "drum-hitclap",
        "drum-hitfinish",
        "drum-hitwhistle",
        "drum-slidertick",
        "drum-sliderslide",
        "drum-sliderwhistle"
    ],
    [ "wav", "ogg" ]
)

NORMAL_SET = Sound_set(
    [
        "normal-hitnormal",
        "normal-hitclap",
        "normal-hitfinish",
        "normal-hitwhistle",
        "normal-slidertick",
        "normal-sliderslide",
        "normal-sliderwhistle"
    ],
    [ "wav", "ogg" ]
)

SOFT_SET = Sound_set(
    [
        "soft-hitnormal",
        "soft-hitclap",
        "soft-hitfinish",
        "soft-hitwhistle",
        "soft-slidertick",
        "soft-sliderslide",
        "soft-sliderwhistle"
    ],
    [ "wav", "ogg" ]
)

HITSOUND_SETS: list[Sound_set] = [ DRUM_SET, NORMAL_SET, SOFT_SET ]
LINE_SEPERATOR: str = "----------"

# looping_set = Sound_set(
#     [
#         "pause-loop"
#     ],
#     [ "wav", "ogg" ]
# )

# special_set = Sound_set(
#     [
#         "combobreak",
#         "failsound",
#         "sectionpass",
#         "sectionfail",
#         "applause",
#         "pause-loop"
#     ],
#     [ "wav", "ogg", "mp3" ]
# )

class Skin_action(Enum):
    COPY_TO_OTHER_SKIN   = 1
    COPY_FROM_SAVED      = 2
    SAVE_FROM_SKIN       = 3

def copy_sounds_from_skin(src_skin: str, dest_skin: str) -> None:
    return

def copy_sounds_to_skin(src_skin: str, dest_skin: str) -> None:
    return

def save_sounds(src_folder: str) -> None:
    SAVED_FOLDER: str = "saved"

    if not os.path.exists(SAVED_FOLDER):
        os.mkdir(SAVED_FOLDER)

    skin_name: str = os.path.basename(os.path.normpath(src_folder))
    print(f"Copying hitsounds from {skin_name}")
    print(LINE_SEPERATOR)

    # print out names of saved folders
    saved: list[str] = os.listdir(SAVED_FOLDER)
    if len(saved) == 0:
        print("No sounds saved")
        print()
    else:
        for i in range(len(saved)):
            print(f"{i + 1}: {saved[i]}")
        print()

    user_input: str = input("Name of new folder or input a number: ")
    if user_input.isnumeric():
        dst_folder: str = saved[int(user_input)]
    else:
        dst_folder: str = os.path.join(SAVED_FOLDER, user_input)
        if os.path.exists(dst_folder):
            override: bool = input(f"{user_input} already exists. Override (y/n)?: ") == "y"
            if override:
                for file in os.listdir(dst_folder):
                    os.remove(os.path.join(dst_folder, file))
        else:
            os.mkdir(dst_folder)

    for hitsound_set in HITSOUND_SETS:
        for filename in hitsound_set.filenames:
            for format in hitsound_set.formats:
                src_file_path: str = os.path.join(src_folder, f"{filename}.{format}")
                dst_file_path: str = os.path.join(dst_folder, f"{filename}.{format}")
                if os.path.exists(src_file_path):
                    shutil.copy(src_file_path, dst_file_path)
                    break

    return

def main() -> None:
    actions: list[str] = [
        "copy sounds from skin to another",
        "copy sounds from saved to a skin",
        "save sounds from a skin"
    ]

    for i in range(len(actions)):
        print(f"{i + 1}: {actions[i]}")
    user_input: int = int(input("\nSelect an action or press 0 to exit: "))
    print(LINE_SEPERATOR)
    if user_input == 0:
        exit()

    with open("skins-folder-path.txt", 'r') as f:
        skins_folder_path: str = f.read()

    skins: list[str] = []
    for item in os.listdir(skins_folder_path):
        if os.path.isdir(skins_folder_path + "/" + item):
            skins.append(item)

    match Skin_action(user_input):
        case Skin_action.COPY_TO_OTHER_SKIN:
            return
        case Skin_action.COPY_FROM_SAVED:
            return
        case Skin_action.SAVE_FROM_SKIN:
            for i in range(len(skins)):
                print(f"{i + 1}: {skins[i]}")
            print()
            selected_skin: str = skins[int(input("Select a skin or 0 to exit: ")) - 1]
            print(LINE_SEPERATOR)
            selected_skin_path: str = os.path.join(skins_folder_path, selected_skin)
            save_sounds(selected_skin_path)
            return

if __name__ == "__main__":
    main()