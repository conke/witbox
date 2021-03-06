#!/usr/bin/python

import os,sys,re
import shutil
import platform
import pwd
from optparse import OptionParser
from xml.etree import ElementTree
from datetime import date

sys.path.append('configs')

curr_user = ''
conf_list = {}

def traverse(node, path):
	if not os.path.exists(path):
		print "creating \"%s\"" % path
		os.mkdir(path)
	#else:
	#	print "skipping \"%s\"" % path
	lst = node.getchildren()
	for n in lst:
		traverse(n, path + '/' + n.attrib['name'])

# population the target directory
def populate_tree(fn):
	tree = ElementTree.parse(fn)
	root = tree.getroot()

	top = '/' + root.attrib['name']

	mounted = False
	fd_chk = open('/proc/mounts')
	for line in fd_chk:
		mount = line.split(' ')
		if mount[1] == top:
			mounted = True
			break
	fd_chk.close()

	if mounted == False:
		print '"%s" NOT mounted!' % top
		exit()

	if not os.access(top, 7):
		print 'Fail to access "' + top + '", permission denied!'
		exit()
		#os.system('sudo chown $USER ' + top) # fixme!

	traverse(root, top)

def get_user_info():
	for struct_pwd in pwd.getpwall():
		if struct_pwd.pw_name == curr_user:
			full_name = struct_pwd.pw_gecos.split(',')[0].strip()
			return full_name


def do_install(curr_distrib, curr_version, curr_arch, install_list):
	upgrade  = ''
	install  = ''
	tree = ElementTree.parse(r'app/apps.xml')
	root = tree.getroot()
	dist_list = root.getchildren()
	for dist_node in dist_list:
		if dist_node.attrib['name'] == curr_distrib:
			upgrade = dist_node.attrib['upgrade']
			install = dist_node.attrib['install']

			#if upgrade != '':
			#	os.system('sudo ' + upgrade)

			os.system('sudo ' + install + ' ' + install_list)
			break
		#release_list = dist_node.getchildren()
		#for release in release_list:
		#	version = release.attrib['version']
		#	if version == 'all' or version == curr_version:
		#		app_list = release.getchildren()
		#		for pkg in install_list:
		#			for app_node in app_list:
		#				attr_class = app_node.get('class')
		#				attr_arch = app_node.get('arch', curr_arch)

		#				if attr_arch == curr_arch and attr_class == pkg:
		#					print 'Installing %s:\n  %s' % (attr_class, app_node.text)
		#					os.system('sudo ' + install + ' ' +  app_node.text)
	
		#					attr_post = app_node.get('post')
		#					if attr_post != None:
		#						os.system('cd app/%s && ./%s' % (attr_class, attr_post))
		#					print ''

		#		if version == curr_version:
		#			break

def parse_config():
	fd_rept = open('.config')
	for line in fd_rept:
		if re.match(r'^\s*[a-zA-Z].*=.*', line) != None:
			elem = re.split('\s*=\s*', line[:-1])
			if elem[0] != '' and elem[1] != '':
				conf_list[elem[0]] = elem[1]
	fd_rept.close()

def config(cfg):
	name = get_user_info()
	
	now = date.today()
	term = "cs%d%d" % (now.year % 100, (now.month + 1) / 2)

	if cfg == 'entrance':
		mail = '12345678@qq.com'
		mailto = 'success@maxwit.com'
		mailcc = 'devel@maxwit.com'
	else:
		mail = name.lower().replace(' ', '.') + '@maxwit.com'
		mailto = 'devel@maxwit.com'
		mailcc = term + '@maxwit.com'

	fd_rept = open('.config', 'w+')
	fd_rept.write('config = %s\n' % cfg)
	fd_rept.write('user.name = %s\n' % name)
	fd_rept.write('user.mail = %s\n' % mail)
	fd_rept.write('mail.pass = maxwit%s\n' % term) # fixme
	fd_rept.write('mail.to = %s\n' % mailto)
	fd_rept.write('mail.cc = %s\n' % mailcc)
	fd_rept.close()

def setup():
	if conf_list['config'] == 'entrance':
		from entrance import do_setup, do_report
	else:
		from onboard import do_setup, do_report

	apps = None

	fd_rept = open('configs/%s/setup' % conf_list['config'])
	for line in fd_rept:
		if re.match(r'^\s*[a-zA-Z].*=.*', line) != None:
			elem = re.split('\s*=\s*', line[:-1])
			#elem = line[:-1].split('=')
			if elem[0].strip() == 'apps':
				apps = elem[1]
	fd_rept.close()

	distrib = platform.dist()[0].lower()
	version = platform.dist()[2].lower()
	arch = platform.processor()

	if apps != None:
		do_install(distrib, version, arch, apps);

	do_setup(distrib, version, conf_list)

	#rep_fn = '/tmp/report'
	#rep_fd = open(rep_fn, 'w+')
	#rep_fd.write('from: "%s" <%s>\n' % (conf_list['user.name'], conf_list['user.mail']))
	#rep_fd.write('to: "%s\n' % conf_list['mail.to'])
	#rep_fd.write('subject: [report] init\n\n')
	#rep_fd.write('OS: %s, %s\n' % (platform.dist(), arch))
	#rep_fd.close()
	# os.system("msmtp %s < %s" % (conf_list['mail.to'],  rep_fn))

def check_command(fd_rept, conf_list):
	fd_rept.write('########################################\n')
	fd_rept.write("\tCommand History\n")
	fd_rept.write('########################################\n')

	fd_hist = open(os.getenv('HOME') + '/.bash_history')
	lines = fd_hist.readlines()
	start = 0
	if len(lines) > 100:
		start = len(lines) - 100
	n = start
	while n < len(lines):
		fd_rept.write("(%d): %s" % (n - start + 1, lines[n]))
		n += 1
	fd_hist.close()

	fd_rept.write('\n')

def report(rep):
	sys.path.append('configs')
	if conf_list['config'] == 'entrance':
		from entrance import do_setup, do_report
	else:
		from onboard import do_setup, do_report

	rep_dir = '/tmp/report-%s' % rep
	rep_fn = rep_dir + '/msg'
	rep_at = rep_dir + '/attach/'
	if os.path.exists(rep_dir) == False:
		os.mkdir(rep_dir)
	fd_rept = open(rep_fn, 'w+')

	#fd_rept.write('"%s" report:\n\n' % conf_list['config'].upper())

	if rep == 'command':
		check_command(fd_rept, conf_list)
	else:
		mail_info = (fd_rept, rep_at)
		if os.path.exists(rep_at) == False:
			os.mkdir(rep_at)
		ret = do_report(rep, mail_info, conf_list)
		if ret == False:
			fd_rept.close()
			return

	fd_rept.write('\n')

	### append system info ###
	fd_rept.write('########################################\n')
	fd_rept.write('\tSystem Information\n')
	fd_rept.write('########################################\n')
	fd_rept.write("%s\n%s\n" % (platform.dist(), os.uname()))
	fd_rept.write('\n')

	### end ###
	fd_rept.write('\n\n---\n%s\n' % conf_list['user.name'])
	fd_rept.close()

	### append command history ###

	###
	mutt_send = 'mutt -s "[Report] %s" %s' % (rep, conf_list['mail.to'])
	if conf_list.has_key('mail.cc'):
		mutt_send += ' -c %s' % conf_list['mail.cc']
	if os.path.isdir(rep_at):
		shutil.copyfile(os.getenv('HOME') + '/.bash_history', rep_at + 'command_history')
		mutt_send += ' -a %s/*' % rep_at
	mutt_send += ' < %s' % rep_fn

	os.system(mutt_send)
	#print mutt_send

def main():
	parser = OptionParser()
	parser.add_option('-c', '--config', dest='config',
					  default=False, action='store_true',
					  help="PowerTool configuration")
	parser.add_option('-r', '--report', dest='report',
					  default=False, action='store_true',
					  help="task report")
	parser.add_option('-v', '--version', dest='version',
					  default=False, action='store_true',
					  help="show PowerTool version and exit")

	(options, args) = parser.parse_args()

	if options.version:
		print "  MaxWit PowerTool %s (by MaxWit Software, http://www.maxwit.com)" % "v3.4-alpha2"
		exit()

	if options.config:
		if len(args) != 1:
			print 'Usage: ./powertool -c <help|arg>'
			exit()

		dl = os.listdir('./configs')
		for cfg in dl:
			if cfg == args[0]:
				config(cfg)
				try:
					config(cfg)
					print 'Finished.'
				except:
					print 'Fail to configure!'
				finally:
					exit()

		print "configs currently supported:"
		for dir in dl:
			if os.path.isdir('configs/' + dir):
				print '  ' + dir

		exit()

	parse_config()

	if len(args) == 0:
		setup()

		if conf_list['config'] == 'onboard':
			populate_tree('tree/tree.xml')

		exit()

	if options.report:
		if len(args) != 1:
			print 'Usage: ./powertool -r <...>'
			exit()

		report(args[0])
		exit()

	if len(args) > 0:
		parser.print_help()
		exit()

if __name__ == "__main__":
	curr_user = os.getenv('USER')
	if curr_user == 'root':
		print 'cannot run as root!'
		exit()

	main()
