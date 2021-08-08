while [ 0 -le 1 ];
do
	/usr/bin/fswebcam -d /dev/video0 -S 20 -r "1920x1080" --save /home/pi/image.jpg;
	sleep 4m;
done


