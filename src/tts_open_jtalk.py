#/usr/bin/env python
#coding: utf-8

import rospy
import subprocess

from geometry_msgs.msg import *

# -- Global変数 --
Speech_word = String()
Speech_flag = False


# /speech_word トピックのsubscribe
def Speech_word_sub(msg):
	global Speech_word
	global Speech_flag
	Speech_word = msg.data
	Speech_flag = True

"""
# 発話flagの制御
def Speech_flag_ctrl(msg):
	global Speech_flag
	Speech_flag = True
"""	
	
# open_jtalkの設定と発話
def open_jtalk(speech_word):
	global Speech_word
	global Speech_flag
	
	#もろもろの引数を、変数に格納する。
	open_jtalk=['open_jtalk']
	mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
	all_pass=['-a', '0.5'] 
	post_filter=['-b', '0.3']
	speed=['-r', '1.0']
	
	#声の選択
	htsvoice=['-m', '/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice']
	#htsvoice=['-m', '/home/ohishikouta/catkin_ws/src/open_jtalk/voice/mei/mei_angry.thsvoice']
	#htsvoice=['-m', '/home/ohishikouta/catkin_ws/src/open_jtalk/voice/mei/mei_bashful.htsvoice']
	#htsvoice=['-m', '/home/ohishikouta/catkin_ws/src/open_jtalk/voice/mei/mei_happy.htsvoice']
	#htsvoice=['-m', '/home/ohishikouta/catkin_ws/src/open_jtalk/voice/mei/mei_normal.htsvoice']
	#htsvoice=['-m', '/home/ohishikouta/catkin_ws/src/open_jtalk/voice/mei/mei_sad.htsvoice']
	#htsvoice=['-m', '/home/ohishikouta/catkin_ws/src/open_jtalk/voice/slt/cmu_us_arctic_slt.htsvoice']
	
	#音声ファイルとログの保存場所を設定
	out_wav=['-ow', 'open_jtalk.wav']
	out_log=['-ot', 'open_jtalk.log']
	
	#上で記述したすべての設定・引数を一つの変数にまとめる
	cmd=open_jtalk+mech+htsvoice+speed+out_wav+out_log+all_pass+post_filter
	
	#コマンドの実行
	c=subprocess.Popen(cmd, stdin=subprocess.PIPE)
	c.stdin.write(speech_word)
	c.stdin.close()
	c.wait()
	
	#生成された音声データの再生
	aplay=['aplay', '-q', 'open_jtalk.wav']
	wr=subprocess.Popen(aplay)
	
	Speech_flag = False
	
def main():
	global Speech_word
	global Speech_flag
	
	Speech_flag = False
	
	sub_speech_word = rospy.Subscriber("/speech_word", String, Speech_word_sub)
		
	while not rospy.is_shutdown():
		if Speech_flag == True:
			open_jtalk(Speech_word)
			Speech_flag = False
			
		else:
			pass
			
if __name__ == "__main__":
	main()

