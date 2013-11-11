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

get_top() {
	while read artist; do
		echo $(tr '[:upper:]' '[:lower:]' < $FILE | tr -d ' :' | grep -c $artist) $artist
	done | sort -nr | head -$1
}

total_songs() {
	cat $FILE | wc -l
}

really_total_songs() {
	tr '[:upper:]' '[:lower:]' < $FILE | tr -d ' :-' | sort -u | wc -l
}

echo "Общее количество артистов в библиотеке: $(dirty_artists_count)"
echo "А если исключить разнописания, останется всего $(clean_artists_count)"
echo "Песен у них - $(total_songs)"
echo "Но это ложь - песни дублируются, по разному пишутся итд. На самом деле их около $(really_total_songs)"
echo
echo "Теперь немного фана. Исходя из того что в среднем альбом стоит 100 рублей, посчитаем сколько денег понаворовано."
echo "Будем считать что в альбоме в среднем 10 песен, и одна стоит 10 рублей"
echo "Итого мы напиратили/напокупали музыки на $(total_songs)0 рублей."
echo
echo "А теперь представим что мы злобные пираты и сидели на раздаче, и пока качали сами - с нас стянули в три раза больше"
echo "Тогда, по подсчётам копирастичных товарищей мы украли $(( $(total_songs) * 40 )) рублей"
echo
artists_list_clean | get_top 40
