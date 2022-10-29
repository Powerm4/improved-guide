import re
from processing.wrappers import http_downloader

tag = 'gfycat'
order = 1

""" 
	This Handler attempts to convert Gyfcat links into direct video links.
"""

format_opts = ["webmUrl", "mp4Url", "gifUrl"]


def handle(task, progress):
	url = task.url
	if 'gfycat.com/' not in url:
		return False
	progress.set_status("Checking for direct gfycat url...")
	uid = re.findall(r"com/([a-zA-Z]+)", url)
	if not uid:
		return False
	uid = uid[0]

	files = http_downloader.page_text(
		f'https://api.gfycat.com/v1/gfycats/{uid}', True
	)

	if not files:
		return False
	files = files["gfyItem"]

	opt = next((fm for fm in format_opts if fm in files and files[fm]), None)
	if not opt:
		return False

	progress.set_status(f"Downloading gfycat {opt}...")
	return http_downloader.download_binary(files[opt], task.file, prog=progress, handler_id=tag)
