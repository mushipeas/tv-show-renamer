
class Defaults:
    # Old matching patterns:
    # pattern = r'(^[\w\._\-\s]+)(?:[\._\-\s]*)([(\d)]*)(?:[\._\-\s]*?[\w]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|m4v|srt|$)'
    # pattern = r'(^[\w\._\-\s]+)(?:[\._\-\s(]*?)(\d*)[)]*?(?:[\._\-\s]*?[\w]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|srt$)'
    # pattern = r'(^[\w\._\-\s]+?)(?:[\._\-\s(]*?)(\d*)[)]*?(?:[\._\-\s]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|srt$)'
    # pattern = r'(^[\w\._\-\s]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|srt$)'
    # pattern = r'(^[\w\._\-\s&!\')(]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\._\-\s][s](\d{1,2})[\._\-\s]*[e|(ep)](\d{1,2})(?:.*)\.(mp4|avi|mkv|m4v|webm|divx|idx|srt$)'
    # pattern = r'(^[\w\._\-\s&!\')(]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\[\._\-\ss](\d{1,2})[x\._\-\s]*[e|(ep)|x](\d{1,2})[^\-\d](?:.*)\.(mp4|avi|mkv|m4v|webm|divx|idx|srt$)'
    
    PATTERN = r'(^[\w\._\-\s&!\')(]+?)(?:[\._\-\s(]*?)(\d{4})*[)]*?(?:[\._\-\s]*?)[\[\._\-\ss](\d{1,2})[x\._\-\s]*[e|(ep)|x](\d{1,3})[^\d](?:.*)\.(mp4|avi|mkv|m4v|webm|divx|idx|srt$)'
    SEASON_DIR_FORMAT = 'Season {:02d}'
    OUTPUT_FORMAT_STRING = "{series_title} - S{s_no:02d}E{ep_no:02d} - {ep_name}.{ext}"
