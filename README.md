# Audioset Downloader

Download google [AudioSet](https://research.google.com/audioset/)

### Requriement

* python
* [moviepy](https://pypi.org/project/moviepy/)
* [pytube](https://pypi.org/project/pytube/)

### Usage

```
python download.py /path/to/input/csv --output_wav_path --output_video_path --save_video
```

Example:
```
python download.py eval_segments.csv ./wav ./video False
```
or
```
python download.py eval_segments.csv
```



