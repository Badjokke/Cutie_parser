import os

from model.FileModel import FileModel


class Filesystem:

    @staticmethod
    def load_directory_names(directory_path: str) -> list[FileModel]:
        children = os.listdir(directory_path)
        result = []
        for i in range(len(children)):
            result.append(FileModel(children[i], f"{directory_path}/{children[i]}"))
        return result
