import logging
import pymel.core as pmc
from pymel.core.system import Path


log = logging.getLogger(__name__)


class SceneFile(object):
    """An abstract representation of a Scene file."""
    def __init__(self, path):
        self._init_from_path(path)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task,
                              ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name.stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        """saves the scene file.

        returns:
            path: the file to the scene file if successful
        """
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directories in path. Creating directories...")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)

# scene_file = scenefile.SceneFile("D:\\School Files\\spring 2021\\sandbox\\tank_model_v001.ma")
# paste to maya
