import difflib
from functools import lru_cache
import collections
import tvdb_api

SearchResult = collections.namedtuple("SearchResult", "show_title id search_difference")


class TVDBRenamer:
    def __init__(self, output_dir, templates, apikey=None):
        self.episode_template = templates.episode
        self.season_folder_templates = templates.season_folder
        self.output_dir = output_dir
        self.t = tvdb_api.Tvdb(apikey=apikey) if apikey else tvdb_api.Tvdb()

    def get_tvdb_info():
        pass

    def get_series_name(self, show_title: str, year: str) -> list:
        try:
            search_term = show_title.append(" ", year) if year else show_title
            search_res = self.t.search(search_term)
        except:
            raise

        result_list = []

        for item in search_res:
            diff = [
                li
                for li in difflib.ndiff(search_term.lower(), item["seriesName"].lower())
                if li[0] != " "
            ]
            result_list.append(
                SearchResult(
                    show_title=item["seriesName"],
                    id=item["id"],
                    search_difference=len(diff),
                )
            )

        return sorted(result_list, key=lambda x: x.search_difference)

    @lru_cache(maxsize=128)
    def _best_match_series(self, show_title: str, year: str) -> "TVDB Show obj":
        search_results = self.search_series_name(show_title, year)
        if search_results:
            for result in search_results:
                if self.t[result.id].data[
                    "seriesName"
                ]:  # ensure a real show (not garbage) is being autoselected
                    return self.t[result.id]
        return None

    def tvdb_episode_info(self, file_info: dict) -> "TVDB Show obj, Episode obj":
        try:
            bm_tvdb_series = self._best_match_series(
                file_info["show_title"], file_info["show_year"]
            )
        except:
            print(
                'Err      Show-name TVDB search returned zero results for "{}" parsed from file: "{}"'.format(
                    file_info["show_title"], file_info["original_file_name"]
                )
            )
        try:
            tvdb_episode = bm_tvdb_series[file_info["season_no"]][
                file_info["episode_no"]
            ]
        except:
            print(
                'Err      Episode Data does not exist on TVDB for TVDB_id={} "{} S{:02d}E{:02d}" parsed from file: "{}"'.format(
                    bm_tvdb_series["id"],
                    file_info["show_title"],
                    file_info["season_no"],
                    file_info["episode_no"],
                    file_info["original_file_name"],
                )
            )
        else:
            return bm_tvdb_series, tvdb_episode
        return None, None

    def new_ep_filename(self, file_, tvdb_info):
        pass
