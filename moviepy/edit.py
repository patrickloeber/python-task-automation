import moviepy.editor as mpy

vcodec =   "libx264"

videoquality = "24"

# slow, ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
compression = "slow"

title = "test"
loadtitle = title + '.mov'
savetitle = title + '.mp4'

# modify these start and end times for your subclips
cuts = [('00:00:02.949', '00:00:04.152'),
        ('00:00:06.328', '00:00:13.077')]


def edit_video(loadtitle, savetitle, cuts):
    # load file
    video = mpy.VideoFileClip(loadtitle)

    # cut file
    clips = []
    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        clips.append(clip)

    final_clip = mpy.concatenate_videoclips(clips)

    # add text
    txt = mpy.TextClip('Please Subscribe!', font='Courier',
                       fontsize=120, color='white', bg_color='gray35')
    txt = txt.set_position(('center', 0.6), relative=True)
    txt = txt.set_start((0, 3)) # (min, s)
    txt = txt.set_duration(4)
    txt = txt.crossfadein(0.5)
    txt = txt.crossfadeout(0.5)

    final_clip = mpy.CompositeVideoClip([final_clip, txt])

    # save file
    final_clip.write_videofile(savetitle, threads=4, fps=24,
                               codec=vcodec,
                               preset=compression,
                               ffmpeg_params=["-crf",videoquality])

    video.close()


if __name__ == '__main__':
    edit_video(loadtitle, savetitle, cuts)
