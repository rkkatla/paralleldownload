# import aioboto3
import asyncio
import aiohttp

import aiofiles


url="https://mirrors.utkarsh2102.org/ubuntu-releases/24.04.1/ubuntu-24.04.1-desktop-amd64.iso"


async def download_parts(session,start,end,i):
	print("starting download for part ",i)
	headers = {'Range': f'bytes={start}-{end}'}
	print(headers)
	async with session.get(url,headers=headers) as response:
			print(response.status)
			async with aiofiles.open("ubuntu_"+str(i), mode='wb') as f:
				async for chunk in response.content.iter_chunked(8192):  # Adjust chunk size if needed
					await f.write(chunk)
	print(f"part {i} downloaded")



async def download_function(parts):
	timeout=aiohttp.ClientTimeout(total=None)
	async with aiohttp.ClientSession(timeout=timeout) as session:
		response = await session.head(url)
		size=int(response.headers['Content-Length'])
		print(f"{size=}")
		chunk_size=size//parts
		if size%parts==0:
			pass
		else:
			parts+=1
		print("divided in parts: ",parts)
		tasks=[]
		for i in range(parts):
			start=i*chunk_size
			end=(i+1)*chunk_size
			tasks.append(download_parts(session,start,end,i))
		await asyncio.gather(*tasks)



if __name__=="__main__":
	parts=10
	asyncio.run(download_function(parts))
