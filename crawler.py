from playwright.async_api import async_playwright
import asyncio
import yaml


config_path = "config.yaml"
def load_config(config_path):
  with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
    return config
  
config = load_config(config_path)

async def scroll_page_down(page):
	dims = await page.evaluate('() => { return { width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight }; }')
	print(dims)
	width = dims["width"]
	height = dims["height"]

	# Scroll vertically
	await page.mouse.move(width // 2, height)
	await page.mouse.down()
	await asyncio.sleep(1) # allow the page to load new content



async def main():
	async with async_playwright() as p:
		browser = await p.chromium.launch(headless=False)
		page = await browser.new_page()
		await page.goto(config['BASE_URL'][1], timeout=60000)

		
		# scroll down until links = 200
		links = []
		while len(links) < 200:

			# Scroll to the bottom of the page
			await scroll_page_down(page)

			# Find all items within the class 'bastian-page'
			links = await page.query_selector_all('.bastian-page a')
			print(len(links))

		for i, link in enumerate(links):
			href = await link.get_attribute('href')
			print(f"{1}: {link} - {href}")


		# wrapp up
		await page.wait_for_timeout(1000)
		await browser.close()

if __name__ == '__main__':
	asyncio.run(main())