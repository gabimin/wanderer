import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_and_follow_links(initial_url, num_links_to_follow, output_file):
    """
    Parses a webpage, follows hyperlinks, and repeats the process for a given number of links.
    If a visited page has no more unvisited links, it goes back to previously visited pages 
    and tries to find a new unvisited link. It also goes back to further previous pages if necessary.
    
    Args:
        initial_url: The URL of the starting webpage.
        num_links_to_follow: The number of links to follow.
        output_file: The name of the Markdown file where outputs will be saved.
    """

    current_url = initial_url
    visited_urls = set()  # Set to store visited URLs
    history = []  # List to store the history of visited pages and their unvisited links

    # Open the Markdown file to log the outputs
    with open(output_file, 'w') as md_file:
        def log_output(output):
            """Helper function to log print outputs to the Markdown file."""
            print(output)  # Print to console as usual
            md_file.write(output + '\n')  # Write to the markdown file

        # Custom user-agent string
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36'
        }
        
        for _ in range(num_links_to_follow):
            try:
                # Get the content of the current page
                response = requests.get(current_url, headers=headers)
                response.raise_for_status()  # Raise an exception for HTTP errors

                # Parse the HTML content
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all hyperlinks (anchor tags with href attributes)
                links = soup.find_all('a', href=True)

                # Build full URLs and filter out already visited URLs
                unvisited_links = [urljoin(current_url, link['href']) for link in links if urljoin(current_url, link['href']) not in visited_urls]

                if not unvisited_links:
                    # If no unvisited links, go back in history
                    while history:
                        previous_page_data = history.pop()
                        previous_url, remaining_links = previous_page_data['url'], previous_page_data['remaining_links']
                        
                        # Check if this previous page has unvisited links
                        if remaining_links:
                            current_url = previous_url
                            unvisited_links = remaining_links
                            break
                    else:
                        log_output(f"No unvisited links available, and no more pages to return to. Stopping.")
                        break

                # Store the current page with remaining unvisited links in the history
                if unvisited_links:
                    # Store the current page with the rest of the unvisited links
                    history.append({
                        'url': current_url, 
                        'remaining_links': unvisited_links[1:]  # Save all but the first link
                    })
                    
                    # Follow the first unvisited link
                    next_link = unvisited_links[0]

                    log_output(f"Current page: {current_url}")
                    log_output(f"Following link: {next_link}\n")

                    # Add the followed link to visited URLs
                    visited_urls.add(current_url)  # Mark the current page as visited
                    visited_urls.add(next_link)  # Mark the followed link as visited

                    # Update the current URL to the next one
                    current_url = next_link

            except requests.exceptions.RequestException as e:
                # Handle any errors while accessing the current page
                log_output(f"Error accessing the page {current_url}: {e}")
                
                if history:
                    # Go back to a previous page if an error occurs
                    previous_page_data = history.pop()
                    current_url = previous_page_data['url']
                    remaining_links = previous_page_data['remaining_links']
                    log_output(f"Returning to previous page: {current_url}")
                else:
                    log_output("No previous page to return to. Stopping.")
                    break

# Example usage
initial_url = input("URL: ")  # Replace with the starting URL
num_links_to_follow = int(input("Number of links to follow: "))
output_file = 'navigation_history.md'  # Markdown file to log the outputs

parse_and_follow_links(initial_url, num_links_to_follow, output_file)
