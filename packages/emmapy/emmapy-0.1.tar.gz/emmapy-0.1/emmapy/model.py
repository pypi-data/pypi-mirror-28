# -*- coding: utf-8 -*-
# model.py

"""
 A simple python SMTP wrapper.
 Uses sane defaults.
 Supports attachments.

API

Required   Notes
 to
 fro       Please do NOT use 'from', which is a reserved word under python
 body
 subject   Technically should be optional according to SMTP, but that's silly

Default values
 mime_type defaults to 'text/plain' if 'attachments' are given

cc_addr (opt)
bcc_add (opt)
reply_to (opt)
mime_type (defaults to text/plain - opt)
attachments (opt) - list of one or more filepaths

Usage

 Define the message first.
 A body must be provided.

 Example 1.

 body = '''
  This is a test message.
 '''

 msg = EmailMessage(body)

 msg.send(to="toaddr", from="fromaddr")

 # alternatively, can specify all other properties
 # using keywords.

 Example 2.

 msg = EmailMessage(body, to="toaddr", from="fromaddr")
 msg.send()

 or even this:

 EmailMessage(body, to="addr", from="fromaddr").send()

 
"""
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders
import os
from os.path import basename
import pprint
pp = pprint.PrettyPrinter(indent=4)

DEBUGGING = True

DEFAULT_SMTP_SERVER = 'localhost'

class EmailMessage(object):
	"""
	 exposes the API operations
	"""

	def __init__(self, body, **kwargs):

		self.body = body
		for key in kwargs:
			setattr(self, key, kwargs[key])

		if not hasattr(self, 'server'):
			self.server = DEFAULT_SMTP_SERVER
		if not hasattr(self, 'body'):
			raise ValueError("'body' is required")
		if not hasattr(self, 'to'):
			raise ValueError("'to' is required")
		if not hasattr(self, 'fro'):
			raise ValueError("'fro' is required")
		if hasattr(self, 'subj') and not hasattr(self,'subject'):
			self.subject = self.subj
			delattr(self, 'subj')
		if not hasattr(self, 'subject'):
			raise ValueError("'subject' is required")
		if not hasattr(self, 'attachments'):
			self.attachments = []
		if hasattr(self, 'mime_type'):
			""" parse mimetype string into mtype and subtype """
			try:
				self.mtype, self.msubtype = self.mime_type.split('/',1)
			except Exception, e:
				raise ValueError('failed to split mimetype into main type/subtype: %s' \
					% (self.mime_type))
				print str(e)
		if not hasattr(self, 'mime_type'):
			self.mtype = 'text'
			self.msubtype ='plain'

	def __repr__(self):

		s = '\n'
		s += 'EmailMessage Object\n'
		for k in self.__dict__:
			s += "%5s%20s: %s\n" % (' ',k, self.__dict__[k])

		return s

	def is_valid_mime_type_for_no_attachments(self):

		if self.mtype == 'text' \
		and self.msubtype == 'plain' or self.msubtype == 'html':
			return True

		return False


	def get_message_object(self):

		if len(self.attachments) == 0:
			if not self.is_valid_mime_type_for_no_attachments():
				raise ValueError('mime type only supported with attachment(s): %s' 
					% (self.mime_type))	

			return MIMEText(self.mtype, self.msubtype)

		""" 
		otherwise, dealing with attachments 
		need a big honkin switch case
		for the time being, assume text/plain 
		and raise exception if otherwise
		"""

		if not self.mtype == 'text' and self.msubtype == 'plain':

			raise ValueError('mime type not yet supported: %s' % (self.mime_type))
			return None

		return MIMEMultipart()

	def create_envelope(self):

		envelope = MIMEMultipart()
		envelope['Subject'] = self.subject
		envelope['To'] = self.to
		envelope['From'] = self.fro
		envelope.preamble = "this is the preamble"
		return envelope

	def deal_with_attachments(self, envelope):

		for a in self.attachments:
			if not self.mtype == 'text' and self.msubtype == 'plain':
				raise ValueError('mime type not yet supported: %s' % (self.mime_type))
				continue
			with open(a, 'rb') as fh:
				part = MIMEText(
					fh.read(),
					_subtype=self.msubtype
					)
			part.add_header('Content-Disposition','attachment', filename=basename(a))
			envelope.attach(part)

		return envelope

	def send(self, **kwargs):

		for key in kwargs:
			setattr(self, key, kwargs[key])

		if not hasattr(self, 'body'):
			raise ValueError("'body' is required")
		if not hasattr(self, 'to'):
			raise ValueError("'to' is required")
		if not hasattr(self, 'fro'):
			raise ValueError("'fro' is required")
		if hasattr(self, 'subj') and not hasattr(self,'subject'):
			self.subject = self.subj
			delattr(self, 'subj')
		if not hasattr(self, 'subject'):
			raise ValueError("'subject' is required")

		""" 
		defaulting to self.mtype = 'text', self.msubtype = 'plain'
		means it ought to be impossible for these to be unset
		"""

		envelope = self.create_envelope()
		envelope.attach(MIMEText(self.body))
		envelope = self.deal_with_attachments(envelope)

		smtp = smtplib.SMTP(self.server)
		smtp.sendmail(self.fro, self.to, envelope.as_string())

if __name__ == "__main__":

	"""
		em = EmailMessage(subj="something", body="hello there", to="recipient@domain", fro="sender@domain")
		em.send()
	"""

	em = EmailMessage(
		subj="test3", 
		body="see attachment", 
		to="recipient@domain", 
		fro="sender@domain",
		attachments=[ 'file.txt' ]
		).send()
