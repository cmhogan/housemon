while [ 0 -le 1 ]
do
	SSHNAME="CHANGEME"  # eg "mfox"
	WEBHOST="CHANGEME"  # eg "www.example.net"
	WEBPATH="CHANGEME"  # eg "/var/www/html"  (no trailing /)
	scp /home/pi/image.png $SSHNAME@$WEBHOST:$WEBPATH && ssh $SSHNAME@$WEBHOST chmod a+r $WEBPATH/image.png;

	sleep 3m;
done
