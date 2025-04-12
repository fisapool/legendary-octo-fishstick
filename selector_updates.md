# Instant Data Scraper Selector Updates

## Current Selectors (as of 2024)

### Table Selection
```css
.tablescraper-selected-table {
    border: 3px solid red !important;
}

.tablescraper-selected-row {
    background-color: rgba(225,227,107,.54) !important;
}

.tablescraper-hover {
    background-color: rgba(159,238,155,.44) !important;
}

.tablescraper-next-button {
    background-color: green !important;
}
```

### UI Elements
- Table Selection: `#wrongTable`
- Next Button: `#nextButton`
- Start Crawling: `#startScraping`
- Stop Crawling: `#stopScraping`
- Infinite Scroll: `#infinateScroll`
- Delay Controls: `#crawlDelay`, `#maxWait`

## Update History
- 2024-01-29: Initial selector documentation
- 2024-01-29: Verified all selectors are working with current Instant Data Scraper version

## Notes
- All selectors use `!important` to ensure they override page styles
- Selectors are designed to be visually distinct for easy identification
- UI element IDs are stable and unlikely to change unless the extension is updated 