file='links/lkac'
while IFS=',' read -r DOMAIN URL; do
	mkdir ./out/$DOMAIN
	URL=$(echo $URL | tr -d '\r')
	DOMAIN=$(echo $DOMAIN | tr -d '\r')
	timeout 180 bash -c "FOLDER="./out/$DOMAIN" scrapy crawl flexnews -a domain="$DOMAIN" -a url="$URL
	wc=$(ls out/$DOMAIN | wc -w)
	request='http://localhost:8081/feedback?folder='$DOMAIN'&url='$URL'&wc='$wc
	echo $request
	curl -X GET $request
done <$file
