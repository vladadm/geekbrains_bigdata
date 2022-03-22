#!/bin/bash
set -x

cmd="hdfs dfs"
declare -a test_files_name=("test_file_1" "test_file_2" "test_file_3")
dir=task_2

# Create files

echo 'Hello' > ${test_files_name[0]}
echo 'hdfs'  > ${test_files_name[1]}
echo '!'     > ${test_files_name[2]}

for i in "${test_files_name[@]}";
  do
    echo Create file:$i
    $cmd  -put ./$i
    $cmd -setrep -w 2 $i
  done

$cmd -mkdir $dir
$cmd -mv test_file_* $dir/

for i in "${test_files_name[@]}";
  do
   $cmd -ls $dir/$i |awk -v date="$(date +"%Y-%m-%d %r")" '{print date, "file_name:"$8, "replica_factor:"$2, "size:" $5}' >> log.txt
   $cmd -rm -skipTrash $dir/$i
   rm -f $i
  done

$cmd -rm -r -skipTrash $dir
