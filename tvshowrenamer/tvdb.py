import collections
import difflib
from functools import lru_cache
import tvdb_api


SearchResult = collections.namedtuple("SearchResult", "show_title id search_difference")


class TVDB:
    """Handles all TVDB queries for the module."""

    def __init__(self, apikey=None):
        self.t = tvdb_api.Tvdb(apikey=apikey, username=" ", userkey=" ")

    def get_ep_tvdb_info(self, file_info: dict) -> "obj, obj":
        """Returns the series and episode info as two objects."""
        year = file_info["year"] if "year" in file_info else " "
        tvdb_series_gen = self._best_match_series(file_info["title"], year)
        while 1:
            try:
                tvdb_series = next(tvdb_series_gen)
            except StopIteration:
                # log: no non-garbage series data found matching x
                break
            except:
                raise
            else:
                try:
                    tvdb_episode = tvdb_series[file_info["season"]][
                        file_info["episode"]
                    ]
                except:
                    # log: trying next series in list
                    continue
                else:
                    return tvdb_series, tvdb_episode
        return None, None

    @lru_cache(maxsize=128)
    def search_series_name(self, show_title: str, year: str = "") -> list:
        """Returns re-sorted list of series that match the query items.
        Items are sorted by closeness to search query.
        """
        search_term = show_title + year
        try:
            search_res = self.t.search(search_term)
        except:
            search_term = show_title
            try:
                search_res = self.t.search(show_title)
            except:
                search_res = []
        finally:
            return _sorted_by_diff(search_res, search_term)

    def _best_match_series(self, show_title: str, year: str = " ") -> "obj":
        # passes one non-empty series objects to caller
        search_results = self.search_series_name(show_title, str(year))
        if search_results:
            for result in search_results:
                if self.t[result.id].data["seriesName"]:
                    yield self.t[result.id]


def _sorted_by_diff(search_res, search_term):
    # sorts the search_res list based on closeness to search term, with it appended
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
