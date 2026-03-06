# ntm_sneak_push

## Project Description
This project is a dedicated web scraper designed to monitor the Nationaltheater Mannheim (NTM) website for new "Theater Sneak" entries. The script runs on a weekly schedule to detect updates in the performance calendar.

When a new Sneak is identified, the logic cross-references the date with upcoming premieres to deduce the likely play or performance being showcased. Once a match is determined, the system automatically distributes the findings, including performance details and the deduced title, via email to a configured list of recipients.

## Core Features
* **Weekly Scraping:** Automated monitoring of the NTM website.
* **Premiere Matching:** Logic to link Sneak dates with the theater's premiere schedule.
* **Automated Notifications:** SMTP-based email alerts sent to specified users.
* **Data Persistence:** Uses a local database to track previously seen entries and avoid duplicate alerts.
* **Activity Logging:** Maintains a detailed log of check times, findings, and system status.
