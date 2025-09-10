# GEMINI.md: Intent Solutions Inc. Blog

## Project Overview

This directory contains the source code for the Intent Solutions Inc. company blog, located at [startaitools.com](https://startaitools.com).

It is a static website built with the [Hugo](https://gohugo.io/) static site generator. The site's purpose is to serve as the company's public-facing blog and showcase its expertise in deploying AI solutions. The configuration indicates it uses the "archie" theme.

## Building and Running

The project's `netlify.toml` file provides the commands for running and building the site.

### Running the Development Server

To run a local development server with live reloading, use the following command:

```bash
hugo server -D --bind 0.0.0.0
```

### Building for Production

To generate a production-ready build in the `public/` directory, use the command specified for Netlify:

```bash
hugo --gc --minify --cleanDestinationDir
```

## Development Conventions

### Creating New Content

New blog posts can be created using the `hugo new` command. New posts should be created in the `posts` content directory.

```bash
hugo new posts/your-new-post-title.md
```

### Project Structure

The project follows a standard Hugo layout:

*   `content/`: Contains all Markdown content for the site, including pages and blog posts.
*   `themes/`: Contains the Hugo theme used for styling and layout (`archie`).
*   `static/`: Holds static assets like images and CSS.
*   `public/`: The output directory where the generated static site is placed (this directory is not tracked by Git).
*   `hugo.toml`: The main configuration file for the Hugo site.
*   `netlify.toml`: Configuration file for deploying the site on Netlify.
