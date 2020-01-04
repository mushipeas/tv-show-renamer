
class Defaults:
    PATTERN = r"(?:^[\w\[\]\.]*?)([\w\._\-\s&!\')(]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\[\._\-\ss](\d{1,2})[x\._\-\s]*[e|(ep)|x](\d{1,3})[^\d](?:.*)(mp4|avi|mkv|m4v|webm|divx|idx|srt$)"
    FILE_NAME_TEMPLATE = "{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}.{ext}"
    SEASON_DIR_TEMPLATE = "Season {0:02d}"
