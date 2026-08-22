const bing = require('bing-image-search-api-scraper')

var search = bing.search('nodejs').then(res => console.log(res))
