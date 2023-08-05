#! /bin/bash
### BEGIN INIT INFO
# Provides:          yourapp
# Required-Start:    nginx
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: The main django process
# Description:       The gunicorn process that receives HTTP requests
#                    from nginx
#
### END INIT INFO
#
# Author:       mle <geobi@makina-corpus.net>
#
APPNAME=remote_sge
USER=testuser
PATH=/bin:/usr/bin:/sbin:/usr/sbin
ACTIVATE=/home/
APPMODULE=sge_server:app
DAEMON=gunicorn
BIND=127.0.0.1:8000
PIDFILE=/var/run/gunicorn.pid
LOGFILE=/var/log/$DAEMON.log
WORKERS=2


if [ -e "/etc/default/$APPNAME" ]
then
    . /etc/default/$APPNAME
fi


case "$1" in
  start)
        # log_daemon_msg "Starting deferred execution scheduler" "$APPNAME"
        # source $ACTIVATE
        su -l testuser -c "/home/testuser/.pyenv/versions/remote_sge/bin/gunicorn --daemon -m 0007 -c /home/testuser/.config/remote_sge/gunicorn_config.py sge_server:app"
    ;;
  stop)
    killall gunicorn
    ;;
  force-reload|restart)
    $0 stop
    $0 start
    ;;
  status)
    status_of_proc -p $PIDFILE $DAEMON && exit 0 || exit $?
    ;;
  *)
    echo "Usage: /etc/init.d/$APPNAME {start|stop|restart|force-reload|status}"
    exit 1
    ;;
esac

exit 0

