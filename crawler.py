from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import os

def run_crawler(url):
    with sync_playwright() as p:
        # Change 'headless' to False to run in non-headless mode
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Navigate to the WhatsApp Web URL
        page.goto(url)

        # Add some time for the user to log in manually (WhatsApp Web requires manual login with QR code)
        input("Please log in manually using the QR code. Press Enter when ready...")

        # Wait for some time after logging in to ensure that the content is loaded
        time.sleep(5)
        while True:
            # Extract the entire HTML content of the page
            html_content = page.content()

            # Pass the HTML content to BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Search for elements containing the text "Click to view"
            click_to_view_elements = soup.find_all(lambda tag: tag.name == 'span' and 'Click to view' in tag.get_text())

            for idx, element in enumerate(click_to_view_elements):
                # Generate a unique filename based on the index
                filename = f'element_{idx}.html'

                # Check if the file already exists
                if os.path.exists(filename):
                    print(f"{filename} already exists.")
                else:
                    # Save the HTML content to a file in the same folder
                    with open(filename, 'w', encoding='utf-8') as html_file:
                        html_file.write(str(element))

                    print(f"Saved {filename}")

            # Wait a little to do it again
            time.sleep(5)


if __name__ == "__main__":
    # Specify the WhatsApp Web URL
    target_url = "https://web.whatsapp.com/"

    # Run the crawler
    run_crawler(target_url)

    # Add a sleep statement to keep the window open for 10 seconds (adjust as needed)
    time.sleep(10)
