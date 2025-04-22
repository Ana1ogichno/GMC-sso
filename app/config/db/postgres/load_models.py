import os
import pkgutil
from pathlib import Path


def get_subfolder_paths(folder_path):
    subfolder_paths = []
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        subfolder_paths.append(item_path)
    return subfolder_paths


def load_all_models() -> None:
    path = "app.modules"
    models_folder = "models"

    modules = []
    modules_path = Path("app/modules").resolve()
    subfolders = get_subfolder_paths(modules_path)

    for subfolder in subfolders:
        separator = "/"
        if "/" not in subfolder:
            separator = "\\"
        module = subfolder.split(separator)[-1]
        walked_modules = pkgutil.walk_packages(
            path=[f"{subfolder}/models"], prefix=f"{path}.{module}.{models_folder}."
        )
        for module_info in walked_modules:
            modules.append(module_info.name)

    for module in modules:
        __import__(module)  # noqa: WPS421
