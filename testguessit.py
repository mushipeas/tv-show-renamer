from collections import Counter
from guessit import guessit

#: Subtitle extensions
SUBTITLE_EXTENSIONS = [
    "srt",
    "sub",
    "smi",
    "txt",
    "ssa",
    "ass",
    "mpl",
]
VIDEO_EXTENSIONS = [
    "3gp",
    "3g2",
    "asf",
    "wmv",
    "avi",
    "divx",
    "evo",
    "f4v",
    "flv",
    "mkv",
    "mk3d",
    "mp4",
    "mpg",
    "mpeg",
    "m2p",
    "ps",
    "ts",
    "m2ts",
    "mxf",
    "ogg",
    "mov",
    "qt",
    "rmvb",
    "vob",
    "webm",
]


def det_type(info):
    # determines file_info "media_type" to file for later sorting
    if "container" in info:
        if info["type"] == "episode":
            if "season" in info and "episode" in info:
                if info["container"] in VIDEO_EXTENSIONS:
                    return "tvepisode"
                elif info["container"] in SUBTITLE_EXTENSIONS:
                    return "tvepisode_sub"

            elif "season" in info or "episode" in info:
                if "episode_title" in info:
                    if info["container"] in VIDEO_EXTENSIONS:
                        return "tvanime"
                    elif info["container"] in SUBTITLE_EXTENSIONS:
                        return "tvanime_sub"

        if info["type"] == "movie":
            if info["container"] in VIDEO_EXTENSIONS:
                return "movie"
            elif info["container"] in SUBTITLE_EXTENSIONS:
                return "movie_sub"
        return "misc_video"
    return "unknown"


fileinfos = []
with open("testfile.txt", "r", encoding="utf-8") as filenames:
    for name in filenames:
        info = guessit(name.strip("\n"))
        fileinfos.append((info, name))

attributeCount = Counter()
typeCount = Counter()
mediaTypeCount = Counter()

for fileinfo, filename in fileinfos:
    attributeCount["total"] += 1
    for attr in fileinfo:
        attributeCount[attr] += 1

    typeCount[fileinfo["type"]] += 1
    media_type = det_type(fileinfo)
    mediaTypeCount[media_type] += 1
    # print("TYPE: ", media_type, "      ", filename)

# print(attributeCount)
# print(typeCount)
print(mediaTypeCount)
