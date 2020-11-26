import os,codecs,re

def main(dir_,out_path):
	phone_numbers = []
	for i in range(6525):
		content = codecs.open(os.path.join(dir_,str(i)+'.txt'), 'r',encoding='utf-8',errors='ignore').readlines()
		for line in content:
			match = re.findall(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', line)
			if len(match) > 0:
				phone_numbers.append(match[0].lower().strip())
			else:
				phone_numbers.append('')

	with codecs.open(out_path,'w',encoding='utf-8',errors='ignore') as f:
		for phone in phone_numbers[:-1]:
			f.write(phone+'\n')
		if phone_numbers[-1]=='':
			f.write('\n')
		else:
			f.write(phone_numbers[-1])

if __name__ == '__main__':
	main('../data/compiled_bios/','../data/phone_numbers')

