#!/bin/bash
DATABASEFILE='/tmp/isar.db';
TIMESTAMP=`date +%s`

NAMES=(`sqlite3 $DATABASEFILE  "select name from vmachine"`)
echo ${#NAMES[@]} Datenbankeinträge

for i in "${NAMES[@]}"  ; do
    echo $i
    # Date of creating
    CREATEDATE=`sqlite3 $DATABASEFILE  "select createdate from vmachine WHERE name='${i}'"`
    # how long best befor
    LIVETIMEDAYS=`sqlite3 $DATABASEFILE  "select lifetimedays from vmachine WHERE name='${i}'"`
    # in seconds
    LIVETIMESEC=`echo $[86400 * ${LIVETIMEDAYS}]`
    # differenc or offset to now
    DIFF=`echo $[${TIMESTAMP} - ${CREATEDATE}]`
#     echo $DIFF DIFF
#     echo $LIVETIMESEC LIVETIMESEC
    # if exhausted
    if [ $DIFF -gt $LIVETIMESEC ]; then
        # get the mail-address of the owner
        MAILADDRESS=`sqlite3 $DATABASEFILE  "select mail from vmachine WHERE name='${i}'"`
        echo send mail to $MAILADDRESS...
        SUBJECT="Deine virtuelle Maschiene ${i}"
        # Email To ?
        EMAIL="admin@somewhere.com"
        # Email text/message
        EMAILMESSAGE="/tmp/isar-emailmessage.txt"
        echo "Hi!"> $EMAILMESSAGE
        echo "Das verfallsdatum deiner Virtuellen Maschiene ${i} " >>$EMAILMESSAGE
        echo "ist erreicht. Bitte überprüfe ob sie jetzt gelöscht " >>$EMAILMESSAGE
        echo "werden kann. Vergiss nicht auch den Datenkankeintrag zu Löschen. " >>$EMAILMESSAGE
        # send an email to owner
        mail -s "$SUBJECT" "$MAILADDRESS" < $EMAILMESSAGE
    fi

done

