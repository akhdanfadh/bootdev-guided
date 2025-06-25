package main

import (
	"context"
	"encoding/xml"
	"html"
	"io"
	"net/http"
)

type RSSItem struct {
	Title       string `xml:"title"`
	Link        string `xml:"link"`
	Description string `xml:"description"`
	PubDate     string `xml:"pubDate"`
}

type RSSFeed struct {
	Channel struct {
		Title       string    `xml:"title"`
		Link        string    `xml:"link"`
		Description string    `xml:"description"`
		Item        []RSSItem `xml:"item"`
	} `xml:"channel"`
}

func printFeed(rssFeed *RSSFeed) {
	// print feed title, link, and description
	println("Feed Title:", rssFeed.Channel.Title)
	println("Feed Link:", rssFeed.Channel.Link)
	println("Feed Description:", rssFeed.Channel.Description)
	println()

	// print each item in the feed
	for _, item := range rssFeed.Channel.Item {
		println("Title:", item.Title)
		println("Link:", item.Link)
		println("Description:", item.Description)
		println("Published:", item.PubDate)
		println()
	}
}

func fetchFeed(ctx context.Context, feedURL string) (*RSSFeed, error) {
	// create request object with context
	req, err := http.NewRequestWithContext(ctx, "GET", feedURL, nil)
	if err != nil {
		return &RSSFeed{}, err
	}
	req.Header.Set("User-Agent", "gator") // identify the client to the server

	// send the request
	client := &http.Client{}
	res, err := client.Do(req)
	if err != nil {
		return &RSSFeed{}, err
	}
	defer res.Body.Close()

	// read the response body
	data, err := io.ReadAll(res.Body)
	if err != nil {
		return &RSSFeed{}, err
	}

	// decode the XML data into RSSFeed struct
	var rssFeed RSSFeed
	if err := xml.Unmarshal(data, &rssFeed); err != nil {
		return &RSSFeed{}, err
	}

	// decode escaped HTML entities in the tile and description
	rssFeed.Channel.Title = html.UnescapeString(rssFeed.Channel.Title)
	rssFeed.Channel.Description = html.UnescapeString(rssFeed.Channel.Description)
	for i := range rssFeed.Channel.Item {
		rssFeed.Channel.Item[i].Title = html.UnescapeString(rssFeed.Channel.Item[i].Title)
		rssFeed.Channel.Item[i].Description = html.UnescapeString(rssFeed.Channel.Item[i].Description)
	}

	return &rssFeed, nil
}
