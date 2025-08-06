# Gator - RSS Feed Aggregator CLI

Gator is a command-line RSS feed aggregator built in Go that allows you to collect, follow, and browse RSS feeds from across the internet. The name comes from "aggreGATOR" 🐊.

## Features

- **Multi-user Support**: Register and manage multiple users
- **Feed Management**: Add RSS feeds and follow/unfollow feeds added by other users  
- **Automatic Collection**: Continuously scrape RSS feeds at specified intervals
- **Post Storage**: Store all collected posts in a PostgreSQL database
- **Browse Posts**: View summaries of aggregated posts with links to full articles
- **User Authentication**: Simple login system to manage your personal feed collection

## Prerequisites

Before installing Gator, make sure you have the following installed on your system:

- **Go 1.21+**: Download and install from [golang.org](https://golang.org/downloads/)
- **PostgreSQL**: Download and install from [postgresql.org](https://www.postgresql.org/download/)
  - Make sure PostgreSQL is running and you have database connection details

## Installation

Install Gator using Go's built-in package manager:

```bash
go install github.com/akhdanfadh/bootdev-guided/07-gator-go@latest
```

This will download, compile, and install the `gator` binary to your `$GOPATH/bin` directory. Make sure `$GOPATH/bin` is in your system's `PATH` so you can run `gator` from anywhere.

## Configuration

Before using Gator, you need to create a configuration file in your home directory:

1. **Create the config file** at `~/.gatorconfig.json`:

```json
{
  "db_url": "postgres://username:password@localhost:5432/gator?sslmode=disable",
  "current_user_name": ""
}
```

2. **Update the database URL** with your PostgreSQL connection details:
   - Replace `username` with your PostgreSQL username
   - Replace `password` with your PostgreSQL password  
   - Replace `localhost:5432` if your database is on a different host/port
   - Replace `gator` with your desired database name

3. **Create the database** (if it doesn't exist):

```sql
CREATE DATABASE gator;
```

The `current_user_name` field will be automatically updated when you log in.

## Quick Start

1. **Register a new user**:

```bash
gator register yourusername
```

2. **Add your first RSS feed**:

```bash
gator addfeed "Tech Blog" "https://example.com/feed.xml"
```

3. **Start collecting posts**:

```bash
gator agg 30s
```

This will fetch new posts every 30 seconds. You can use any duration format (1m, 5m, 1h, etc.).

4. **Browse collected posts**:

```bash
gator browse 10
```

## Available Commands

User Management:

- `gator register <username>` - Register a new user and log in
- `gator login <username>` - Log in as an existing user  
- `gator users` - List all registered users (current user marked with *)
- `gator reset` - Delete all users (destructive operation)

Feed Management:

- `gator addfeed <name> <url>` - Add a new RSS feed (requires login)
- `gator feeds` - List all available feeds with their URLs and creators
- `gator follow <url>` - Follow an existing feed (requires login)  
- `gator following` - Show feeds you're currently following (requires login)
- `gator unfollow <url>` - Unfollow a feed (requires login)

Content Browsing:

- `gator agg <duration>` - Start continuous feed aggregation (e.g., "30s", "5m", "1h")
- `gator browse [limit]` - Browse recent posts (default limit: 2)

## Development

If you want to modify or contribute to Gator:

1. **Clone the repository**:

```bash
git clone https://github.com/akhdanfadh/bootdev-guided/07-gator-go.git
cd 07-gator-go
```

2. **Run in development mode**:

```bash
go run . <command> [args]
```

3. **Build the binary**:

```bash
go build -o gator
./gator <command> [args]
```

## Technical Details

Gator is built using:

- **[sqlc](https://sqlc.dev/)** for type-safe SQL queries
- **[goose](https://github.com/pressly/goose)** for database migrations

The application uses PostgreSQL to store users, feeds, feed follows, and posts with proper relational constraints.
