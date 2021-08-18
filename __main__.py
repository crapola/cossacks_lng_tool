from pathlib import Path
import re
import struct
import sys

ENCODING_TXT="ansi"
ENCODING_LNG="ansi"

def dict_from_txt_file(path):
	with open(path,"r",encoding=ENCODING_TXT,newline='\r\n') as file:
		pattern=r"@(?P<key>.+?)\r\n(?P<value>.+?)\r\n(?=\t|\Z)"
		lines=file.read()
		regex=re.compile(pattern,re.S)
		matches=regex.findall(lines)
	#print(matches)
	return dict(matches)

def bytes_from_dict(d):
	b=bytes()
	for k,v in d.items():
		item=k.encode(ENCODING_LNG)+b"="+v.encode(ENCODING_LNG)
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
	print(b)
	output_path=file_path.parent.joinpath(file_path.stem).with_suffix(".lng")
	with open(output_path,"wb",newline=None) as file:
		file.write(b)

if __name__=="__main__":
	main()