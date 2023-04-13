#!/usr/bin/zsh


err_exit(){
  echo '[ERROR]'
  printf "%s " "Closing connect_vnc.sh"
#  read -r
  exit "$1"
}


echo "start_dir: $(pwd)"
start_dir=$(pwd)

echo "base_dir: $(dirname "$0")"
base_dir=$(dirname "$0")
if [ "$base_dir" != "." ]; then
  echo "Changing directory to: $base_dir"
  cd "$base_dir" || err_exit $?
  echo "pwd: $(pwd)"
fi

echo "Venv activating:"
source ./venv/bin/activate || err_exit $?
echo "Venv activated successful"

echo "sleep 2 :"
sleep 2

echo "xtightvncviewer 172.17.0.1:5900 :"
loop_key=true
exception_key=false
counter=0
while loop_key ; do
  xtightvncviewer 172.17.0.1:5900 || sleep 3 && exception_key=true && counter+=1;
  if [ ! $exception_key ]; then
    loop_key=false
  fi
  if [ $counter == 4 ]; then
      err_exit 1
  fi
done

exit 0