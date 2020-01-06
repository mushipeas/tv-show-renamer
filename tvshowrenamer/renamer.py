import os
import re


class Renamer:
    """Handles all renaming functionality of the module"""

    def __init__(self, episode_t, season_folder_t, winsafe):
        self.episode_t =episode_t
        self.season_folder_t = season_folder_t
        self.winsafe = winsafe

    def get_ep_filename(self, tvdb_series, tvdb_episode, extension):
        """Generate new filename using tvdb info provided.
        It uses the episode template assigned at Renamer.
        If winsafe was set to true in init, it will remove unsafe chars.
        """
        new_filename = self._format_filename(
            tvdb_series.data["seriesName"],
            tvdb_episode["airedSeason"],
            tvdb_episode["airedEpisodeNumber"],
            tvdb_episode["episodeName"],
            extension,
        )
        if self.winsafe:
            return self._make_winsafe(new_filename)
        else:
            return new_filename

    def get_relative_pathname(self, tvdb_series, tvdb_episode, extension):
        """Generates relative path for file with a folder structure matching
        the /SeriesName/SeasonNo/Episodes structure. The SeasonNo folder and 
        Episode filename are formatted according to the templates supplied to
        init
        """
        show_dir = self._make_winsafe(tvdb_series.data["seriesName"])
        season_dir = self.season_folder_t.format(tvdb_episode["airedSeason"])
        new_filename = self.get_ep_filename(tvdb_series, tvdb_episode, extension)
        return os.path.join(show_dir, season_dir, new_filename)

    def _format_filename(
        self, series_title: str, s_no: int, ep_no: int, ep_name: str, ext: str,
    ):  
        # generate filename using template
        return self.episode_t.format(
            series_title=series_title, s_no=s_no, ep_no=ep_no, ep_name=ep_name,
        ) + "".join(ext)

    def _make_winsafe(self, unsafe_name: str):
        # remove unsafe characters from name(str)
        unsafe_char_sp = r"\/<>|"
        repl_sp = " "
        unsafe_char_rm = r":*?\""
        repl_rm = ""

        safe_filename_interm = re.sub(
            "[{}]".format(re.escape(unsafe_char_sp)), repl_sp, unsafe_name
        )
        safe_name = re.sub(
            "[{}]".format(re.escape(unsafe_char_rm)), repl_rm, safe_filename_interm
        )

        return safe_name
