import re
import os
import tvdb_api
import difflib
from functools import lru_cache
from .custom_objs import Cobjs

#  . └─ ├ ├ ├ ├   for tree struc

class Renamer:
    def __init__(self,
                OUTPUT_FORMAT_STRING,
                PATTERN,
                APIKEY,
                SEASON_DIR_FORMAT,
                MAKEWINSAFE=False,
                ):
        self.MAKEWINSAFE = MAKEWINSAFE
        self.OUTPUT_FORMAT_STRING = OUTPUT_FORMAT_STRING
        self.SEASON_DIR_FORMAT = SEASON_DIR_FORMAT
        
        self.prog = re.compile(PATTERN, re.IGNORECASE)
        self.t = tvdb_api.Tvdb(apikey=APIKEY)

    def _get_regex_tv_info(self, video_filename: str):
        match = self.prog.match(video_filename)

        output = {
            'original_file_name' : match.string,
            'show_title' : match.group(1).replace('.',' '),
            'show_year' : match.group(2),
            'season_no' : int(match.group(3)),
            'episode_no' : int(match.group(4)),
            'extension' : match.string.split('.')[-1]
         } if match else None

        return output

    def search_series_name(self, show_title: str, year: str=' ') -> list:
        try:
            search_term = show_title + year
            search_res = self.t.search(search_term)
        except:
            try:
                search_term = show_title
                search_res = self.t.search(show_title)
            except:
                print('Err     Show-name search returned zero results for {}.'.format(search_term))
                raise

        result_list = []
        
        for item in search_res:
            diff = [li for li in difflib.ndiff(search_term.lower(), item['seriesName'].lower()) if li[0] != ' ']
            result_list.append(Cobjs.SearchResult(
                show_title = item['seriesName'],
                id = item['id'],
                search_difference = len(diff)
                ))


        return sorted(result_list, key=lambda x: x.search_difference)

    @lru_cache(maxsize=128)
    def _best_match_series(self, show_title: str, year: str=' ') -> 'TVDB Show obj':
        search_results = self.search_series_name(show_title, year)
        if search_results:
            for result in search_results:
                if self.t[result.id].data['seriesName']: # ensure a real show (not garbage) is being autoselected
                    return self.t[result.id]
        return None

    def get_ep_tvdb_info(self, regex_data: dict) -> 'TVDB Show obj, Episode obj': 
        bm_tvdb_series = self._best_match_series(regex_data['show_title'], regex_data['show_year'])
        tvdb_episode = bm_tvdb_series[regex_data['season_no']][regex_data['episode_no']]

        return bm_tvdb_series, tvdb_episode

    def format_filename(self, series_title: str, s_no: int, ep_no: int, ep_name: str, ext: str, format_str: str):
        return format_str.format(series_title=series_title,
                                s_no=s_no,
                                ep_no=ep_no,
                                ep_name=ep_name,
                                ext=ext)

    def get_new_filename(self, tvdb_series, tvdb_episode, extension):
        new_filename = self.format_filename(tvdb_series.data['seriesName'],
                                            tvdb_episode['airedSeason'],
                                            tvdb_episode['airedEpisodeNumber'],
                                            tvdb_episode['episodeName'],
                                            extension,
                                            self.OUTPUT_FORMAT_STRING
                                            )
        if self.MAKEWINSAFE:
            return self.make_winsafe(new_filename)
        else:
            return new_filename
        
    def make_winsafe(self, unsafe_filename: str):
        unsafe_char_sp = r"\/<>|"
        repl_sp = " "
        unsafe_char_rm = r":*?\""
        repl_rm = ""

        safe_filename_interm = re.sub('[{}]'.format(re.escape(unsafe_char_sp)),repl_sp,unsafe_filename)
        safe_filename = re.sub('[{}]'.format(re.escape(unsafe_char_rm)),repl_rm,safe_filename_interm)

        return safe_filename

    def get_relative_pathname(self, orig_filename: str):
        regex_data = self._get_regex_tv_info(orig_filename)
        if regex_data:
            try:
                bm_tvdb_series, tvdb_episode = self.get_ep_tvdb_info(regex_data)
                show_dir = self.make_winsafe(bm_tvdb_series.data['seriesName'])
                season_dir = self.SEASON_DIR_FORMAT.format(tvdb_episode['airedSeason'])
                new_filename = self.get_new_filename(bm_tvdb_series, tvdb_episode, regex_data['extension'])
                return os.path.join(show_dir,season_dir,new_filename)
            except:
                print('Err      Show-name TVDB search returned zero results for "{}" from : {}'.format(regex_data['show_title'],regex_data['original_file_name']))
                return None
        else:
            print('Err      Filename cannot be parsed for "{}"!'.format(orig_filename))
            #add ability to manually select show and season / episode number?
            return None
