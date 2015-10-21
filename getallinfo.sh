#!/bin/bash
cd /root/snowdata/
for stockcode in $(cat stocklist)
do
    if [[ $stockcode == 6* || $stockcode = 000001 ]];then
        code="SH"
    else
        code="SZ"
    fi
    stockname=$code$stockcode
    sleeps=500
    python snowball.py $stockname  > index.html
    vericode=`cat index.html | grep -i title | sed -e "s/<[^>]*>//g"  | cut -c 1-6`
    while [[ $vericode == "请输入验证码"  ]]
    do
        sleeps=$[sleeps+100]
        echo "+++++sleep $sleeps to avoid vericode...++++++"
        sleep $sleeps
        python snowball.py $stockname  > index.html
        vericode=`cat index.html | grep -i title | sed -e "s/<[^>]*>//g"  | cut -c 1-6`
    done
    python sparse.py
    echo "+spider $stockname to snowsocks finish +"
done
