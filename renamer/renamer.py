import re
import os
import tvdb_api
import difflib
from .custom_objs import Cobjs
from .constants import Defaults

# pattern = r'(^[\w\._\-\s]+)(?:[\._\-\s]*)([(\d)]*)(?:[\._\-\s]*?[\w]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|m4v|srt|$)'
# pattern = r'(^[\w\._\-\s]+)(?:[\._\-\s(]*?)(\d*)[)]*?(?:[\._\-\s]*?[\w]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|srt$)'
# pattern = r'(^[\w\._\-\s]+?)(?:[\._\-\s(]*?)(\d*)[)]*?(?:[\._\-\s]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|srt$)'
# pattern = r'(^[\w\._\-\s]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|srt$)'
# pattern = r'(^[\w\._\-\s&!\')(]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|m4v|webm|divx|idx|srt$)'

#  . └─ ├ ├ ├ ├   for tree struc

class Renamer:
    def __init__(self,
                OUTPUT_FORMAT_STRING=Defaults.OUTPUT_FORMAT_STRING,
                pattern=Defaults.pattern,
                season_dir_format=Defaults.season_dir_format,
                MAKEWINSAFE=False
                ):
        self.MAKEWINSAFE = MAKEWINSAFE
        self.OUTPUT_FORMAT_STRING = OUTPUT_FORMAT_STRING
        self.season_dir_format = season_dir_format
        
        self.prog = re.compile(pattern, re.IGNORECASE)
        self.t = tvdb_api.Tvdb()

    def _get_regex_tv_info(self, video_filename: str):
        match = self.prog.match(video_filename)

        output = {
            'original_file_name' : match.string,
            'regex_show_title' : match.group(1).replace('.',' '),
            'regex_show_year' : match.group(2),
            'regex_season_no' : int(match.group(3)),
            'regex_episode_no' : int(match.group(4)),
            'regex_extension' : match.string.split('.')[-1]
         } if match else None

        return output

    def search_series_name(self, show_title: str, year: str=' '):
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

    def _best_match_show(self, show_title: str, year: str=' '):
        search_results = self.search_series_name(show_title, year)
        if search_results:
            for result in search_results:
                if self.t[result.id].data['seriesName']:
                    return result
        return None

    def get_episode_data(self, show_id,season_no,episode_no):
        try:
            ep = self.t[show_id][season_no][episode_no]
            return ep
        except:
            raise

    def get_ep_tvdb_info(self, regex_data):
        best_match = self._best_match_show(regex_data['regex_show_title'], regex_data['regex_show_year'])
        tvdb_episode = self.get_episode_data(best_match.id,regex_data['regex_season_no'],regex_data['regex_episode_no'])

        return {
            'tvdb_id' : best_match.id,
            'tvdb_show_title' : best_match.show_title,
            'tvdb_episode_title' : tvdb_episode['episodename'],
        }

    def format_filename(self, show_title: str, s_no: int, ep_no: int, ep_name: str, ext: str, format_str: str):
        return format_str.format(show_title, s_no, ep_no, ep_name, ext)

    def get_new_filename(self, regex_data, tvdb_ep_data):
        new_filename = self.format_filename(tvdb_ep_data['tvdb_show_title'],
                                            regex_data['regex_season_no'],
                                            regex_data['regex_episode_no'],
                                            tvdb_ep_data['tvdb_episode_title'],
                                            regex_data['regex_extension'],
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
                tvdb_ep_data = self.get_ep_tvdb_info(regex_data)
                show_dir = self.make_winsafe(tvdb_ep_data['tvdb_show_title'])
                season_dir = self.season_dir_format.format(regex_data['regex_season_no'])
                new_filename = self.get_new_filename(regex_data, tvdb_ep_data)
                return os.path.join(show_dir,season_dir,new_filename)
            except:
                print('Err      Show-name TVDB search returned zero results for "{}" from : {}'.format(regex_data['regex_show_title'],regex_data['original_file_name']))
                raise
        else:
            print('Err      Filename cannot be parsed for "{}"!'.format(orig_filename))
            #add ability to manually select show and season / episode number?
            return None
