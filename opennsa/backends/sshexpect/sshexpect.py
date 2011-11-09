from pexpect import *
import pexpect

class SSHException(ExceptionPexpect):
	"""General errors for SSHExpect"""
	pass

class SSHConnectionException(SSHException):
	"""Error during ssh connection setup/login"""
	pass

class SSHExpect(spawn): 
	"""Wrapper for pexpect.spawn to facilitate ssh sessions

	   by default this invokes a /bin/sh session on the remote host
	   and sets the prompt for easy recognition.
	   You can change this behaviour by modifying the prompt or shellcmd
	   variables."""

	def __init__(self):
		self.prompt="psshex% "
		self.shellcmd='PS1=\"%s\" /bin/sh' % self.prompt
		pass

	def connect(self, user, password, host, options="-t", timeout=5):
		"""Invokes spawn and sets up a connection to the server 
		   and logs in"""
		cmd="ssh %s -l %s %s '%s'" % (options, user,\
						host, self.shellcmd)	
		spawn.__init__(self, cmd)
		self.login(password)

	def login(self, password, count=0,  timeout=20):
		"""Does the actual ssh login procedure"""
		qkey=".*Are you sure you want to continue connecting (yes/no)?."
		qpass='password:'
		try: 
			result=self.expect([qkey,qpass,self.prompt],timeout)

			if result==0:
			#Host key check prompt
				raise SSHConnectionException("\
					InvalidHostKey" % host)
			elif result==1: 
			#Password prompt
				if count>0:
					raise SSHConnectionException(\
						"InvalidPassword")
				self.sendline(password)
				self.login(password, count=1)
				pass
			elif result==2:
			#Command prompt
				self.sendline("")
				pass
			else:
				pass
		except pexpect.EOF:
			raise SSHConnectionException ("ConnectionClosed")
		except pexpect.TIMEOUT:
			raise SSHConnectionException ("ConnectionTimeout")
		pass

	def hasPrompt(self, timeout=2):
		"""Check if we have a prompt or not (non blocking)"""
		try:
			result=self.expect([self.prompt],timeout)
			if result==0:
				return True
			else: 
				return False
		except pexpect.TIMEOUT:
			return False

	def waitPrompt(self):
		"""Waits for a prompt (blocking)"""
		self.hasPrompt(timeout=-1)
		
	def sendBreak(self):
		"""Sends CTRL-C over the ssh connection"""
		self.send(chr(3))

	def logout(self):
		"""Sends CTRL-D over the ssh connection"""
		self.send(chr(ord("d")-ord("a")+1))
		pass

