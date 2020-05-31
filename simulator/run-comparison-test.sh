#!/bin/bash
# to kill multiple runaway processes, use 'pkill runaway_process_name'
# For the Java implementation, use the following format: ./tests1.sh your_client.class [-n]

algorithm=$1
configfile=$2
trap "kill 0" EXIT

echo "Running their implementation and logging output in theirs.txt..."

sleep 1
../ds-sim/ds-server -c $configfile -v all > theirs.txt&

sleep 1
../ds-sim/ds-client -a $algorithm
echo "Testing Complete!"
echo "  "
echo "Running our implementation and logging output in ours.txt..."
echo "# client.py 15-May-2020, 2020 Authored by: Avi.R, Cooper.T, Tom.T
# Client started with '../src/client.py -a $algorithm'"

sleep 2
./ds-server -c $configfile -v all > ours.txt&

sleep 1
python3 ../src/client.py -a $algorithm

sleep 1
echo "Testing Complete!"

TEST_OUTPUT=$false
OUT=$(diff ours.txt theirs.txt)

sleep 1
echo "  "
echo "Checking Difference..."

EXPECTED_DIFF="2c2
< # Server-side simulator started with './ds-server -c $configfile -v all'
---
> # Server-side simulator started with '../ds-sim/ds-server -c $configfile -v all'"

TEST_OUTPUT=$(diff <(echo "$OUT") <(echo "$EXPECTED_DIFF"))
echo "  "

sleep 1
if [$TEST_OUTPUT != $false]
then 
	cat success.txt
	echo "You can the confirm results via log files -> theirs.txt and ours.txt files"
else
	cat fail.txt
	echo "You can the confirm the results via log files -> theirs.txt and ours.txt files"
fi

