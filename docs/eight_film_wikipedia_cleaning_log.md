# Wikipedia Dataset Cleaning Log

- Input rows: 8
- Output rows: 8
- Rows removed: 0

## Cleaning actions

- Removed 0 duplicate film records.
- Records with unsuccessful API status: 0.
- Standardized text fields by trimming whitespace and converting empty strings to missing values.
- Converted pageid to numeric where the field was available.
- Missing article extracts: 0.

## Missing-value summary

| Column | Missing values |
|---|---:|
| type | 0 |
| title | 0 |
| displaytitle | 0 |
| wikibase_item | 0 |
| pageid | 0 |
| lang | 0 |
| dir | 0 |
| revision | 0 |
| tid | 0 |
| timestamp | 0 |
| description | 0 |
| description_source | 0 |
| extract | 0 |
| extract_html | 0 |
| namespace_id | 0 |
| namespace_text | 8 |
| titles_canonical | 0 |
| titles_normalized | 0 |
| titles_display | 0 |
| thumbnail_source | 0 |
| thumbnail_width | 0 |
| thumbnail_height | 0 |
| originalimage_source | 0 |
| originalimage_width | 0 |
| originalimage_height | 0 |
| content_urls_desktop_page | 0 |
| content_urls_desktop_revisions | 0 |
| content_urls_desktop_edit | 0 |
| content_urls_desktop_talk | 0 |
| content_urls_mobile_page | 0 |
| content_urls_mobile_revisions | 0 |
| content_urls_mobile_edit | 0 |
| content_urls_mobile_talk | 0 |
| film_id | 0 |
| film_name | 0 |
| requested_title | 0 |
| collection_status | 0 |
| api_url | 0 |

## Data handling decisions

- Original API JSON is preserved separately.
- Flattened API fields are retained in the cleaned CSV.
- Missing descriptions or extracts are not fabricated.
- Article extracts are retained as text for later analysis.
