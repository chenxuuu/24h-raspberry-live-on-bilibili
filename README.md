# 24h-raspberry-live-on-bilibili
树莓派驱动的b站直播点歌台

demo:http://live.bilibili.com/16703

注意这个是新项目，查看旧版的代码请打开“old”分支查看（旧版为网页点歌版）

本项目正在编写中，预计需要的功能为：

- 弹幕点歌 已完成
- 接收弹幕 已完成
- 弹幕反馈（发送弹幕） 已完成
- 旧版实现的视频推流功能 已完成
- 自定义介绍字幕 已完成

已知问题：

- 树莓派渲染速度过慢
- 换歌时会闪断

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
git clone git://source.ffmpeg.org/ffmpeg.git
cd ffmpeg
sudo ./configure --arch=armel --target-os=linux --enable-gpl --enable-libx264 --enable-nonfree --enable-libass --enable-libfreetype
make -j4
sudo make install
cd ..
rm -rf ffmpeg
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