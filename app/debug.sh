#!/bin/bash

trap "cleanup" 1 2 3 6 9 14 15

cleanup()
{
    echo "cleaning up" >> /tmp/out.log
    sleep 1;
    for pid in $(find /proc -maxdepth 1 -type d -printf "%P\n"); do
        if [[ ! $pid =~ '[0-9]*' ]]; then continue; fi

        if [ "$pid" != "$$" ] && [ "$pid" != "1" ]; then
            kill -15 $pid
        fi
    done;
    exit 0
}

checkChrome()
{
    local chrome_ok=false

    if [ $(command -v google-chrome) ]; then
        chrome_ok=true
        version=$(google-chrome --version);
        read -t 5 -p "[CHROME] version is $version. do you want to check for update? (timeout 5 seconds) [y/n]: " update
        if [ "$update" =~ "[yY]" ]; then
            chrome_ok=false
        fi

    else
        echo "[CHROME] this seems like your first run. Chrome needs to be installed ....  "; sleep 3
    fi
    if ! $chrome_ok; then
        DEBIAN_FRONTEND=noninteractive && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub > /usr/share/keyrings/chrome.pub \
            && echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/chrome.pub] http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google-chrome.list \
            && apt update -y && apt install -y google-chrome-stable
    fi

}

check_or_install()
{
    local name="$1"

    if [ ! $(command -v $name) ]; then
        echo "[X] no $name found on the system. we'll install it now..";
        sleep 1
        DEBIAN_FRONTEND=noninteractive apt install -y $name
    fi
    command -v $name > /dev/null
    return $?
}

sourced=false
if [ -n "$ZSH_VERSION" ]; then
    case $ZSH_EVAL_CONTEXT in *:file) sourced=true ;; esac
elif [ -n "$BASH_VERSION" ]; then
    (return 0 2> /dev/null) && sourced=true
else
    # All other shells: examine $0 for known shell binary filenames.
    # Detects `sh` and `dash`; add additional shell filenames as needed.
    case ${0##*/} in sh | -sh | dash | -dash) sourced=true ;; esac
fi

function keepUpScreen()
{
    echo "running keepUpScreen()"
    while true; do
        sleep 1
        if [ -z "$(pidof Xvfb)" ]; then
            Xvfb $DISPLAY -screen $DISPLAY 1280x1024x16 &
        fi
    done
}

startDesktop()
{
    check_or_install x11vnc || return 1
    check_or_install Xvfb || return 1
    check_or_install xvfb-run || return 1
    check_or_install fluxbox || return 1

    x11vnc -create -env FD_PROG=/usr/bin/fluxbox \
        -env X11VNC_FINDDISPLAY_ALWAYS_FAILS=1 \
        -env X11VNC_CREATE_GEOM=${1:-1280x1024x16} \
        -gone 'killall Xvfb' \
        -forever \
        -nopw \
        -quiet &

    localip="$(hostname -I)"
    remoteip=$(curl -s "https://httpbin.org/ip" \
        | grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)")

    echo "----------------------------------------------------------"
    echo "to conect to your desktop using vnc:"
    echo "depending on your setup"
    echo ""
    echo "${localip}:5900   (local)"
    echo "or"
    echo "${remoteip}:5900  (remote)"
    echo "----------------------------------------------------------"
    echo "in both cases, the container should have exposed port 5900"
    echo "like 'docker run ...  -P 5900:5900 .... '"
    echo "----------------------------------------------------------"
    xrdp &
}


if ! $sourced; then
    export DISPLAY=:1
    rm -f /tmp/.X1-lock &>/dev/null
#    checkChrome
    keepUpScreen &
#    echo "running: $@"
#    exec $@
fi

echo "sleep 2 && exit" | bash
x11vnc -display :1
