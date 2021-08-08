while [ 0 -le 1 ]
do
	SSHNAME="CHANGEME"  # eg "mfox"
	WEBHOST="CHANGEME"  # eg "www.example.net"
	WEBPATH="CHANGEME"  # eg "/var/www/html"  (no trailing /)
	scp /home/pi/python/24hr.png $SSHNAME@$WEBHOST:$WEBPATH && ssh $SSHNAME@$WEBHOST chmod a+r $WEBPATH/24hr.png;
	sleep 4m;
done
