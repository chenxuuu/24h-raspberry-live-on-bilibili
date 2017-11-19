# 24h-raspberry-live-on-bilibili
树莓派驱动的b站直播点歌台

demo:http://live.bilibili.com/16703

注意这个是新项目，查看旧版的代码请打开“old”分支查看（旧版为网页点歌版）

本项目基本编写完毕，已经有的功能为：

- 弹幕点歌
- 弹幕点MV
- 弹幕反馈（发送弹幕）
- 旧版实现的视频推流功能
- 自定义介绍字幕
- 基础的歌词显示
- 切歌
- 显示排队歌曲
- 下载时的cpu温度
- 闲时随机播放预留歌曲
- 播放音乐时背景图片随机选择

已知问题：

- 树莓派渲染速度过慢
- 换歌时会闪断 （预留图片换为统一的1280x720，可以在一定程度上缓解该问题）

## 食用方法：

我这里用的是树莓派3B，系统2017-09-07-raspbian-stretch.img，官方默认软件源

### 先安装依赖：

```Bash
sudo apt-get update
sudo apt-get -y install autoconf automake build-essential libass-dev libfreetype6-dev libtheora-dev libtool libvorbis-dev pkg-config texinfo wget zlib1g-dev
```

安装x264解码器（时间较长）：

```Bash
git clone git://git.videolan.org/x264
cd x264
./configure --host=arm-unknown-linux-gnueabi --enable-static --disable-opencl
make
sudo make install
cd ..
rm -rf x264
```

libmp3lame：
```
sudo apt-get install libmp3lame-dev
```
libopus:
```
sudo apt-get install libopus-dev
```
libvpx:
```
sudo apt-get install libvpx-dev
```

编译并安装ffmpeg（时间较长，半小时左右）：
```Bash
wget http://ffmpeg.org/releases/ffmpeg-3.3.2.tar.bz2
tar jxvf ffmpeg-3.3.2.tar.bz2
cd ffmpeg-3.3.2
sudo ./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree --enable-libass --enable-libfreetype  --enable-omx --enable-omx-rpi --enable-encoder=h264_omx --enable-mmal --enable-hwaccel=h264_mmal --enable-decoder=h264_mmal
make -j4
sudo make install
cd ..
```
（以上有一部分代码参考自[ffmpeg源码编译安装（Compile ffmpeg with source）  Part 2 ： 扩展安装 - 人脑之战 - 博客园](http://www.cnblogs.com/yaoz/p/6944942.html)）

安装python3的一个库：
```
sudo pip3 install mutagen
```

安装screen:
```
sudo apt-get install screen
```

安装中文字体
```Bash
apt install fontconfig
apt-get install ttf-mscorefonts-installer
apt-get install -y --force-yes --no-install-recommends fonts-wqy-microhei
apt-get install -y --force-yes --no-install-recommends ttf-wqy-zenhei
#可能有装不上的，应该问题不大

# 查看中文字体 --确认字体是否安装成功
fc-list :lang=zh-cn
```
（字体安装来自[ubuntu下 bilibili直播推流 ffmpeg rtmp推送](https://ppx.ink/2.ppx)）


### 下载&运行：
下载本项目：
```
git clone https://github.com/chenxuuu/24h-raspberry-live-on-bilibili.git
```
或
```
git clone https://gitee.com/Young_For_You/24h-raspberry-live-on-bilibili.git
```

请修改下载里的`var_set.py`文件中的各种变量
其中，`cookie`需要使用小号（大号也行）在直播间，打开浏览器审查元素，先发一条弹幕，再查看`network`选项卡，找到`name`为`send`的项目，`Request head`中的`Cookie`即为`cookie`变量的值。注意设置后，账号不能点击网页上的“退出登陆”按键，换账号请直接清除当前cookie再刷新

如有条件，请`务必`自己搭建php的下载链接解析服务，源码都在`php`文件夹内

`default_mp3`文件夹内放入mp3格式的音乐，在无人点歌时播放，请尽量保证文件名全英文

`default_pic`文件夹内放入jpg格式的音乐，用于做为放音乐时的背景，请尽量保证文件名全英文

所有配置完成后，开启直播，然后启动脚本即可：
```Bash
screen python3 post_dm.py
#按ctrl+a,按ctrl+d
screen python3 play.py
#按ctrl+a,按ctrl+d
```

如有不对的地方，请提交issue

本程序协议为GPL