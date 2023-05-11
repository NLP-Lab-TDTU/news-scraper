file='check.txt'
while IFS=',' read -r DOMAIN URL; do
	mkdir ./$DOMAIN
	timeout 300 bash -c "FOLDER="$DOMAIN" scrapy crawl flexnews -a domain="$DOMAIN" -a url="$URL
	wc=$(ls ./$DOMAIN | wc -w)
	request='http://localhost:8080/feedback?folder='$DOMAIN'&url='$URL'&wc='$wc
	echo $request
	curl -X GET $request
done <$file
