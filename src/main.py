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
    DELETE_SAVED         = 4

SAVED_FOLDER: str = "saved"

def print_skins(skins: list[str]) -> None:
    for i in range(len(skins)):
        print(f"{i + 1}: {skins[i]}")
    print()

def print_saved(saved: list[str]) -> None:
    if len(saved) == 0:
        print("No sounds saved")
        print()
    else:
        for i in range(len(saved)):
            print(f"{i + 1}: {saved[i]}")
            print()

# passing "a/b/c.txt" would return "c.txt"
def get_last_part_of_path(path: str) -> str:
    return os.path.basename(os.path.normpath(path))

def copy_sounds_from_folder(src_folder: str, dst_folder: str) -> None:
    src_skin_name: str = get_last_part_of_path(src_folder)
    dst_skin_name: str = get_last_part_of_path(dst_folder)
    print(f"Copying hitsounds from {src_skin_name} to {dst_skin_name}")

    # delete all the hitsounds in the destination skin
    for hitsound_set in HITSOUND_SETS:
        for filename in hitsound_set.filenames:
            for format in hitsound_set.formats:
                src_file_path: str = os.path.join(dst_folder, f"{filename}.{format}")
                if os.path.exists(src_file_path):
                    os.remove(src_file_path)
                    break

    # copy the sounds over
    for hitsound_set in HITSOUND_SETS:
        for filename in hitsound_set.filenames:
            for format in hitsound_set.formats:
                src_file_path: str = os.path.join(src_folder, f"{filename}.{format}")
                dst_file_path: str = os.path.join(dst_folder, f"{filename}.{format}")
                if os.path.exists(src_file_path):
                    shutil.copy(src_file_path, dst_file_path)
                    break

def save_sounds(src_folder: str) -> None:
    SAVED_FOLDER: str = "saved"

    if not os.path.exists(SAVED_FOLDER):
        os.mkdir(SAVED_FOLDER)

    skin_name: str = get_last_part_of_path(src_folder)
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

def delete_saved(target_folder: str) -> None:
    target_folder_name: str = get_last_part_of_path(target_folder)
    print(f"Deleting {target_folder_name}")

    # need to delete everything inside the folder before deleting the directory
    for hitsound_set in HITSOUND_SETS:
        for filename in hitsound_set.filenames:
            for format in hitsound_set.formats:
                file_path: str = os.path.join(target_folder, f"{filename}.{format}")
                if os.path.exists(file_path):
                    os.remove(file_path)
                    break

    os.removedirs(target_folder)

def main() -> None:
    actions: list[str] = [
        "copy sounds from skin to another",
        "copy sounds from saved to a skin",
        "save sounds from a skin",
        "delete a saved folder"
    ]

    for i in range(len(actions)):
        print(f"{i + 1}: {actions[i]}")
    action: int = int(input("\nSelect an action or press 0 to exit: "))
    print(LINE_SEPERATOR)
    if action == 0:
        exit()

    with open("skins-folder-path.txt", 'r') as f:
        skins_folder_path: str = f.read()

    skins: list[str] = []
    for item in os.listdir(skins_folder_path):
        if os.path.isdir(skins_folder_path + "/" + item):
            skins.append(item)

    if not os.path.exists(SAVED_FOLDER):
        os.mkdir(SAVED_FOLDER)

    saved: list[str] = os.listdir(SAVED_FOLDER)

    match Skin_action(action):
        case Skin_action.COPY_TO_OTHER_SKIN:
            print_skins(skins)
            src_skin: str = skins[int(input("Select the source skin: ")) - 1]
            dst_skin: str = skins[int(input("Select the destination skin: ")) - 1]
            print(LINE_SEPERATOR)

            src_skin_path: str = os.path.join(skins_folder_path, src_skin)
            dst_skin_path: str = os.path.join(skins_folder_path, dst_skin)
            copy_sounds_from_folder(src_skin_path, dst_skin_path)
            return
        case Skin_action.COPY_FROM_SAVED:
            if len(os.listdir(SAVED_FOLDER)) == 0:
                print("No sounds saved. Quitting program.")
                exit()

            print_saved(saved)
            saved_selection: str = saved[int(input("Select the saved sounds folder: ")) - 1]
            saved_folder_path: str = os.path.join(SAVED_FOLDER, saved_selection)
            print(LINE_SEPERATOR)

            print_skins(skins)
            dst_skin: str = skins[int(input("Select the destination skin: ")) - 1]
            dst_skin_path: str = os.path.join(skins_folder_path, dst_skin)
            print(LINE_SEPERATOR)
            copy_sounds_from_folder(saved_folder_path, dst_skin_path)
            return
        case Skin_action.SAVE_FROM_SKIN:
            print_skins(skins)
            selected_skin: str = skins[int(input("Select a skin: ")) - 1]
            skin_path: str = os.path.join(skins_folder_path, selected_skin)
            print(LINE_SEPERATOR)

            print_saved(saved)
            user_input: str = input("Enter the name of new folder or select a saved folder: ")
            if user_input.isnumeric():
                dst_folder: str = os.path.join(SAVED_FOLDER, saved[int(user_input)])
            else:
                dst_folder: str = os.path.join(SAVED_FOLDER, user_input)
                if os.path.exists(dst_folder):
                    override: bool = input(f"{user_input} already exists. Override (y/n)?: ") == "y"
                    if override:
                        for file in os.listdir(dst_folder):
                            os.remove(os.path.join(dst_folder, file))
                else:
                    os.mkdir(dst_folder)

            copy_sounds_from_folder(skin_path, dst_folder)
            return
        case Skin_action.DELETE_SAVED:
            print_saved(saved)
            selected_saved: str = saved[int(input("Select the saved sounds folder: ")) - 1]
            print(LINE_SEPERATOR)
            full_path: str = os.path.join(SAVED_FOLDER, selected_saved)
            delete_saved(full_path)
            return

if __name__ == "__main__":
    main()