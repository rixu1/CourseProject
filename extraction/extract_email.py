import os,codecs,re

EMAIL_REGEX = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
def main(dir_,out_path):
	emails = []
	for i in range(6525):
		content = codecs.open(os.path.join(dir_,str(i)+'.txt'), 'r',encoding='utf-8',errors='ignore').readlines()
		for line in content:
			match = 0
			email = ''
			for re_match in re.finditer(EMAIL_REGEX, line):
				match += 1
				email = re_match.group()
				break
			emails.append(email)
	with codecs.open(out_path,'w',encoding='utf-8',errors='ignore') as f:
		for email in emails[:-1]:
			f.write(email+'\n')
		if emails[-1]=='':
			f.write('\n')
		else:
			f.write(emails[-1])

if __name__ == '__main__':
	main('../data/compiled_bios/','../data/emails_new')


