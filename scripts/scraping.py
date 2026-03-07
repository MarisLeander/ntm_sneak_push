import requests
import time
from bs4 import BeautifulSoup

def get_parser(url: str) -> (BeautifulSoup or None, str):
    """ Fetches the HTML content of the given URL and parses it with BeautifulSoup.
    :param url: The URL of the webpage to fetch and parse.
    :return: A tuple containing the BeautifulSoup object (or None if fetching/parsing failed) and a status message ("Success" or error message).
    """
    try:
        response = requests.get(url)

        # Raise an exception if the request failed (e.g., 404 Not Found, 500 Server Error)
        response.raise_for_status()

        html_content = response.text

        # Pass to BeautifulSoup parser
        soup = BeautifulSoup(html_content, 'html.parser')

    except requests.exceptions.RequestException as e:
        # This catches any connection errors, timeouts, or bad HTTP statuses
        print(f"Something went wrong while fetching the page: {e}")
        return None, e

    return BeautifulSoup(html_content, 'html.parser'), "Success"

def get_sneak_performances(soup: BeautifulSoup) -> list:
    """ Scrapes the sneak performances from the NTM website, including date, location, ticket link, and iCal link.
    :param soup: A BeautifulSoup object containing the parsed HTML of the NTM performances page.
    :return: A list of dictionaries, each containing details about a sneak performance (date, location, ticket link, iCal link).
    """
    # Find all the performance items
    # Notice how we can just search for the specific child items directly!
    performance_items = soup.find_all('div', class_='productionnextperformances__item')

    scraped_data = []

    for item in performance_items:
        # Extract Date
        date_div = item.find('div', class_='productionnextperformances__date')
        date_str = date_div.text.strip() if date_div else None

        # Extract Location
        location_tag = item.find('a', class_='productionnextperformances__location')
        location = location_tag.text.strip() if location_tag else None

        # Extract Ticket Link (checking if it exists first to avoid errors)
        ticket_tag = item.find('a', class_='ticketbutton')
        ticket_link = ticket_tag['href'] if ticket_tag else None

        # Extract iCal Link
        ical_tag = item.find('a', class_='performancemini__ical')
        ical_link = ical_tag['href'] if ical_tag else None

        # Store the data in a dictionary
        scraped_data.append({
            'date': date_str,
            'location': location,
            'ticket_link': ticket_link,
            'ical_link': ical_link
        })
    # Print the results
    for data in scraped_data:
        print(data)

def get_premiere_performances(location: str) -> list:
    """ Scrapes the premiere performances from the NTM website, including details from the individual performance pages.
    :param location: The location for which to scrape premiere performances (e.g., "OPAL", "Altes Kino Franklin", etc.)
    :return: A list of dictionaries, each containing details about a premiere performance (date, location, title, writer, length, description, etc.)
    """
    location_filters = {
        "OPAL":"opal-filter",
        "Altes Kino Franklin":"franklin-filter",
        "NTM Tanzhaus":"ntm-tanzhaus-filter",
        "Junges NTM":"junges-ntm-filter",
        "Studio Werkhaus":"studio-werkhaus-filter",
        "Schlosstheater":"schlosstheater-filter",
        "Rosengarten":"rosengarten-filter",
        "Weitere Spielorte":"weitere-spielorte-filter"
    }
    location_filter = location_filters[location]
    # The URL pattern for the premiere page with location filter
    url = f"https://www.nationaltheater-mannheim.de/spielplan/{location_filter}/premiere"
    soup, result = get_parser(url) #@TODO: Handle the case where the parser fails (result != "Success")

    performance_wrappers = soup.find_all('div', class_='schedule__performancewrapper')

    scraped_performances = []

    for wrapper in performance_wrappers:
        # Extract Date and Time
        date_meta = wrapper.find('meta', itemprop='startDate')
        datetime_str = date_meta['content'] if date_meta else None

        # Extract Title and Details Link from the same tag
        link_tag = wrapper.find('a', class_='performance__link')

        if link_tag:
            # This grabs the text inside the <a> tag, ignoring the span completely
            list_title = link_tag.text.strip()
            details_link = "https://www.nationaltheater-mannheim.de" + link_tag['href']
        else:
            title = None
            details_link = None

        # Extract Location
        location_tag = wrapper.find(class_='performance__location')
        location = location_tag.text.strip() if location_tag else Non

        # Store in dictionary
        perf_data = {
            'datetime': datetime_str,
            'location': location,
            'details_link': details_link,
            'title': list_title,  # Fallback title
            'writer': None,
            'length': None,
            'description': None
        }

        # --- GET DATA FROM DETAIL PAGE ---
        if details_link:
            try:
                # Pause for 5 second to avoid being rate-limited or blocked by the server.
                time.sleep(5)

                detail_resp = requests.get(details_link)
                detail_resp.raise_for_status()
                detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')

                # Overwrite with Detail Title (often more accurate/complete)
                title_tag = detail_soup.find('h1', class_='productionhead__headline')
                if title_tag:
                    perf_data['title'] = title_tag.text.strip()

                # Extract Writer
                writer_tags = detail_soup.find_all('div', class_='productionhead__text')
                for tag in writer_tags:
                    if "von " in tag.text:
                        perf_data['writer'] = tag.text.strip()
                        break

                # Extract Length
                metainfos = detail_soup.find_all('div', class_='productionhead__metainfo')
                for info in metainfos:
                    label = info.find('span', class_='productionhead__metainfolabel')
                    if label and "Dauer" in label.text:
                        # Grab the full text and remove the label word "Dauer "
                        perf_data['length'] = info.text.replace(label.text, '').strip()
                        break

                # Extract Description
                # Grabs all richtext divs, filter out short empty ones, and join them with line breaks
                richtext_divs = detail_soup.find_all('div', class_='richtext')
                desc_paragraphs = [div.text.strip() for div in richtext_divs if len(div.text.strip()) > 10]
                perf_data['description'] = "\n\n".join(desc_paragraphs)

            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch details for {list_title}: {e}")

        # Append the fully populated dictionary to list
        scraped_performances.append(perf_data)

    return scraped_performances