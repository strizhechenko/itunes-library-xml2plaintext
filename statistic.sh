#!/bin/bash

if [ -z "$1" ]; then
	echo "Usage: ${BASH_SOURCE[@]} <plaintexted file>"
	exit 0
fi

FILE="$1"

artists_list_dirty() {
	cut -d '-' -f1 $FILE | sort -u
}

artists_list_clean() {
	artists_list_dirty | tr '[:upper:]' '[:lower:]' | tr -d ' :-' | sort -u
}

dirty_artists_count() {
	artists_list_dirty | wc -l
}

clean_artists_count() {
	artists_list_clean | wc -l
}

echo "Общее количество артистов в библиотеке: $(dirty_artists_count)"
echo "А если исключить разнописания, останется всего $(clean_artists_count)"

get_top() {
	while read artist; do
		echo $(tr '[:upper:]' '[:lower:]' < $FILE | tr -d ' :' | grep -c $artist) $artist
	done | sort -nr | head -$1
}

artists_list_clean | get_top 40
