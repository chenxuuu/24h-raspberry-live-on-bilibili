--直播码
local rtmpUrl = "rtmp://js.live-send.acg.tv/live-js/"
local liveCode = "?streamname=live_xxxxxxxxxxxxxxxx&key=xxxxxxxxxxxxxx"
--最大码率
local maxRate = 2200

--随机数表代码来自http://www.cnblogs.com/slysky/p/5954053.html
--产生1~~m,若有n的则m~~n的数字表
function table.fillNum(m,n)
    local j,k
    if n then
        j=m
        k=n
    else
        j=1
        k=m
    end
    local t={}
    for i=j,k do
        table.insert(t,i)
    end
    return t
end
--产生不相同的从m到n，一共cnt个随机数表
function math.randomx(m,n,cnt,seed)
    local tmp=table.fillNum(m,n)
    math.randomseed(seed)
    local t={}
    while cnt>0 do
        x=math.random(1,n-m+1)
        table.insert(t,tmp[x])
        table.remove(tmp,x)
        cnt=cnt-1
        m=m+1
    end
    return t
end

print("run loop")

while true do
    local files = {}
    for i=1,10 do
        files[i] = math.randomx(12,19,4,os.time()+i)
    end
    local flist = {}
    for i=1,4 do
        local fl = {}
        for j=1,10 do
            table.insert(fl,tostring(files[j][i])..".mp4")
        end
        flist[i] = "-i \"concat:"..table.concat(fl,"|").."\""
    end
    local cmd = "ffmpeg -threads 0 -re "..table.concat(flist," ").." "..
    [[-filter_complex "[0:v]pad=iw*2:ih*2[a];[a][1:v]overlay=w[b];[b][2:v]overlay=0:h[c];[c][3:v]overlay=w:h;amix=inputs=4:duration=first:dropout_transition=4" ]]..
    "-pix_fmt yuv420p -c:v libx264 -preset ultrafast -b:v "..tostring(maxRate).."K -tune fastdecode -acodec aac -b:a 192k -strict -2 "..
    [[-f flv "]]..rtmpUrl..liveCode..[["]]
    print(cmd)
    os.execute(cmd)
end


