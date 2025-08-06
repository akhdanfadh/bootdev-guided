package main

import (
	"context"
	"database/sql"
	"encoding/xml"
	"fmt"
	"html"
	"io"
	"log"
	"net/http"
	"time"

	"github.com/akhdanfadh/bootdev-guided/07-gator-go/internal/database"
	"github.com/google/uuid"
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

func scrapeFeeds(s *state, ctx context.Context) error {
	// get next feed to fetch
	feedToFetch, err := s.db.GetNextFeedToFetch(ctx)
	if err != nil {
		return err
	}

	// mark feed as fetched
	args := database.MarkFeedFetchedByIdParams{
		ID:        feedToFetch.ID,
		UpdatedAt: time.Now(),
	}
	err = s.db.MarkFeedFetchedById(ctx, args)
	if err != nil {
		return err
	}

	// now fetch the feed
	rssFeed, err := fetchFeed(ctx, feedToFetch.Url)
	if err != nil {
		return err
	}

	// process every scraping
	log.Printf("Processing %s", rssFeed.Channel.Title)
	for _, item := range rssFeed.Channel.Item {

		// parse published date
		var publishedAt sql.NullTime
		if item.PubDate != "" {
			// try common RSS date formats
			layouts := []string{
				time.RFC1123,  // "Mon, 02 Jan 2006 15:04:05 MST"
				time.RFC1123Z, // "Mon, 02 Jan 2006 15:04:05 -0700"
				time.RFC822,   // "02 Jan 06 15:04 MST"
				time.RFC822Z,  // "02 Jan 06 15:04 -0700"
				time.RFC850,   // "Monday, 02-Jan-06 15:04:05 MST"
				time.RFC3339,  // "2006-01-02T15:04:05Z07:00"
			}
			for _, layout := range layouts {
				if parsedTime, err := time.Parse(layout, item.PubDate); err == nil {
					publishedAt = sql.NullTime{Time: parsedTime, Valid: true}
					break
				}
			}
		}

		// create post params
		postParams := database.CreatePostParams{
			ID:          uuid.New(),
			CreatedAt:   time.Now(),
			UpdatedAt:   time.Now(),
			Title:       item.Title,
			Url:         item.Link,
			Description: sql.NullString{String: item.Description, Valid: item.Description != ""},
			PublishedAt: publishedAt,
			FeedID:      feedToFetch.ID,
		}

		// save post to database
		_, err := s.db.CreatePost(ctx, postParams)
		if err != nil {
			// check if it's a unique constraint violation (URL already exists)
			if err.Error() == "UNIQUE constraint failed: posts.url" ||
				err.Error() == "pq: duplicate key value violates unique constraint \"posts_url_key\"" {
				// ignore duplicate URLs
				continue
			}
			// log other errors but don't stop processing
			log.Printf("Error saving post %q: %v", item.Title, err)
			continue
		}
		fmt.Println("*", item.Title)
	}
	return nil
}
