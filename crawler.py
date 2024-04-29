from playwright.async_api import async_playwright
import asyncio
import yaml
import box
import warnings 

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Import config vars
with open('config.yaml', 'r', encoding='utf-8') as yamlfile:
	cfg = box.Box(yaml.safe_load(yamlfile))


async def scroll_page_down(page):
	dims = await page.evaluate('() => { return { width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight }; }')
	print(dims)
	width = dims["width"]
	height = dims["height"]

	# Scroll vertically
	await page.mouse.move(width // 2, height)
	await page.mouse.down()
	await asyncio.sleep(1) # allow the page to load new content


def save_links(links):
	# File name
	file_name = "links.txt"

	# Open the file in write mode
	with open(file_name, "w") as file:
			# Iterate through the list of links
			for link in links:
					# Write the link to the file, followed by a newline character
					file.write(f"{link}\n")

	print(f"Links saved to {file_name}")


async def main():
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=False)
		page = await browser.new_page()
		await page.goto(cfg.BASE_URL[1], timeout=60000)

		
		# scroll down until links = 200
		links = []
		while len(links) < 2:

			# Scroll to the bottom of the page
			await scroll_page_down(page)

			# Find the "Veja mais" link
			veja_mais_link = await page.query_selector('a:has-text("Veja mais")')

			if veja_mais_link:
				# Click the link
				await veja_mais_link.click()
				await page.wait_for_timeout(1000) # wait for 1s to laod new content

			# Find all items within the class 'bastian-page'
			#links = await page.query_selector_all('.bastian-page a')
	 
	 		# find divs containing the desired links  'feed-post-body-title'
			divs_with_link = await page.query_selector_all('div[class*="feed-post-body-title"]')
			
			for div in divs_with_link:
				# Find the link within the div
				link = await div.query_selector('a')
				links.append(link)
			
			print(len(links))

		href_list = []
		for i, link in enumerate(links):

			href = await link.get_attribute('href')
			href_list.append(href)
			#news_page = await browser.new_page().goto(href)
	 
		save_links(href_list)



		# wrapp up
		await page.wait_for_timeout(1000)
		await browser.close()

if __name__ == '__main__':
	asyncio.run(main())