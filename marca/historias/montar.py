import subprocess,sys
def dur(f): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f]))
for name,n in [("about-us",5),("partner",4)]:
    vo=[f"historias/vo/{name}-{i}.wav" for i in range(1,n+1)]
    d=[max(4.0,dur(v)+1.3) for v in vo]
    starts=[0.0]
    for i in range(1,n): starts.append(starts[-1]+d[i-1]-0.5)
    total=starts[-1]+d[-1]
    args=["ffmpeg","-y","-loglevel","error"]
    for i in range(n): args+=["-loop","1","-t",f"{d[i]:.2f}","-i",f"historias/{name}-{i+1}.png"]
    for v in vo: args+=["-i",v]
    f="";prev="[0:v]";off=0
    for i in range(1,n):
        f+=f"{prev}[{i}:v]xfade=transition=slideleft:duration=0.5:offset={starts[i]:.2f}[v{i}];";prev=f"[v{i}]"
    for i in range(n):
        ms=int((starts[i]+0.4)*1000); f+=f"[{n+i}:a]adelay={ms}|{ms}[a{i}];"
    f+="".join(f"[a{i}]" for i in range(n))+f"amix=inputs={n}:normalize=0,apad=whole_dur={total:.2f},loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
    args+=["-filter_complex",f,"-map",prev,"-map","[aout]","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-crf","18","-c:a","aac","-b:a","192k","-ar","48000","-t",f"{total:.2f}",f"historias/AquaCore_{name}.mp4"]
    subprocess.run(args,check=True); print(name,round(total,1),"s")
