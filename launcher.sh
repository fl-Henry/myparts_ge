#!/bin/bash

# Exit with waiting for type <enter> before exit
err_exit(){
  echo '[ERROR]'
  printf "%s " "Press enter to continue"
  read -r
  exit "$1"
}

# Get the option
r_key=false
update_key=false
str_param=""
pt="./app/app.py"

printf "%s " "Params: "
while [ "$#" -gt 0 ]
do
   case "$1" in

  # STDOUT pip freeze
   -f|--freeze)
      r_key=true
      printf "%s " " freeze;"
      ;;

  # Update key
   -u|--update)
      update_key='--update'
      str_param+="$update_key "
      printf "%s " " --update;"
      ;;

  # python file as entrypoint
   --pt)
      shift
      pt="$1"
      printf "%s " " python file to start='$pt';"
      ;;

#   --start-date)
#      shift
#      start_date="$1"
#      str_param+="--start-date $start_date "
#      printf "%s " " start-date='$start_date';"
#      ;;
#
#   --end-date)
#      shift
#      end_date="$1"
#      str_param+="--end-date $end_date "
#      printf "%s " " end-date='$end_date';"
#      ;;
#
#     --tests)
#      shift
#      tests="$1"
#      str_param+="--tests $tests "
#      printf "%s " " tests #'$tests';"
#      ;;
#
#     --force-url)
#      force_url="--force-url"
#      str_param+="$force_url "
#      printf "%s " " $force_url';"
#      ;;

     -h|--help)
      help="--help"
      str_param+="$help "
      printf "%s " " $help';"
      ;;

   -*)
      echo "Invalid option '$1'. Use -h or --help to see the valid options" >&2
      return 1
      ;;

   *)
      echo "Invalid option '$1'. Use -h or --help to see the valid options" >&2
      return 1
   ;;
   esac
   shift
done
echo

# STDOUT present working directory
echo "start_dir: $(pwd)"
start_dir=$(pwd)

# Changing directory to project root directory
echo "base_dir: $(dirname "$0")"
base_dir=$(dirname "$0")
if [ "$base_dir" != "." ]; then
  echo "Changing directory to: $base_dir"
  cd "$base_dir" || err_exit $?
  echo "pwd: $(pwd)"
fi

# Activating virtual environment
echo "Venv activating:"
source ./venv/bin/activate || err_exit $?
echo "Venv activated successful"

# pip freeze if -f or --freeze
if [ "$r_key" = true ]; then
    echo "pip freeze:"
    pip freeze
fi

# Start app // entrypoint
printf "\nStart app\n"
printf "%s\n" "python $pt $str_param > "
python ./app/app.py
# echo "$pt $str_param" | xargs python
printf "\n%s\n\n" "< python $pt $str_param"

# Starting bot with
# printf "\n%s\n" "Starting bot with args: $str_param "
# printf "python ./bot_logic.py > \n"
# while true ; do echo "$str_param" | xargs python ./bot_logic.py || sleep 5; done
# printf "< python ./bot_logic.py\n\n"

# Changing directory to initial directory
echo "Changing directory to: $start_dir"
cd "$start_dir" || err_exit $?
echo "pwd: $(pwd)"

# Deactivating virtual environment
deactivate