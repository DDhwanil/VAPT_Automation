#!/bin/bash
cd ./git
CUR_DIR=$(pwd)

for path in $(find . -name ".git" |cut -c 3-); do
	cd "$path" && cd ..;
	UPD_PATH=$(pwd)
	echo "Updating the $UPD_PATH directory..."
	BRANCH=$(git branch |awk -F" " '{print $2}')
	echo "Updateing the $BRANCH branch"
	git pull origin $BRANCH;
	cd $CUR_DIR
done

echo "DONE!!"
