
ffmpeg -y -i C:\Workspaces\EOS\eoside\sikuli_movies\movies\installing\installing_raw.mp4 -vf "fade=in:0:25" -c:v libx264 -crf 23  -pix_fmt yuv420p -movflags faststart C:\Workspaces\EOS\eoside\sikuli_movies\movies\installing\installing_faded.mp4
ffmpeg -y -f concat -safe 0 -i concat_list.txt -c copy ../../../docs/_static/C:\Workspaces\EOS\eoside\sikuli_movies\movies\installing\installing.mp4
    