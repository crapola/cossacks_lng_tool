from pathlib import Path
import re
import struct
import sys

ENCODING="ansi"

def dict_from_txt_file(path):
	with open(path,"r",encoding=ENCODING) as file:
		pattern=r"@(?P<key>.+?)\n(?P<value>.+?)\n(?:\t|\Z)"
		lines=file.read()
		regex=re.compile(pattern)
		matches=regex.findall(lines)		
	return dict(matches)

def bytes_from_dict(d):
	b=bytes()
	for k,v in d.items():
		item=k.encode("ansi")+b"="+v.encode("ansi")
		item_length=len(item)
		b=b+struct.pack("i",item_length)+item+struct.pack("b",3)
	b=struct.pack("i",len(d))+b
	return b

def main():
	argv=sys.argv
	try:
		file_path=Path(argv[1])
	except IndexError:
		sys.stderr.write("You must provide a file path.")
		return
	b=bytes_from_dict(dict_from_txt_file(file_path))
	output_path=file_path.parent.joinpath(file_path.stem).with_suffix(".lng")
	with open(output_path,"wb") as file:
		file.write(b)

if __name__=="__main__":
	main()