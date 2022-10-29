import sources
from sources.source import Source


class DirectInputSource(Source):
	def __init__(self, txt=None, args=None):
		super().__init__(source_type='direct-input-source', description="Entered on the command line, for direct downloading.")
		self.data['txt'] = txt or ''
		self.data['args'] = args or {}
		self.src = None

	def get_elements(self):
		txt = self.data['txt']
		args = self.data['args']
		if 'u/' in txt:
			self.src = sources.PushShiftUserSourceSource()
			args['users'] = self._sanitize('u', txt)

		if 'r/' in txt:
			self.src = sources.PushShiftSubmissionSource()
			args['subreddit'] = self._sanitize('r', txt)

		for s in self.src.get_settings():
			if s.name in args:
				s.set(args[s.name])  # Forces type conversion.
				self.src.insert_data(s.name, s.val())

		yield from self.src.get_elements()

	def _sanitize(self, tag, txt):
		return txt.replace(f'/{tag}/', '').replace(f'{tag}/', '').strip('/')

	def get_config_summary(self):
		return self.src.get_config_summary() if self.src else self.data
