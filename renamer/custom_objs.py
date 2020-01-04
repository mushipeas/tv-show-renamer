import collections


class Cobjs:
    # Episode = collections.namedtuple('Episode','original_file_name id text_show_title tvdb_show_title show_year season_no episode_no episode_title extension')
    SearchResult = collections.namedtuple(
        "SearchResult", "show_title id search_difference"
    )
