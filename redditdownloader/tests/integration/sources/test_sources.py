import os
from tests.mock import EnvironmentTest
import static.settings as settings
import sources


class SourceTest(EnvironmentTest):
	env = 'all_sources'

	def setUp(self):
		settings.load(self.settings_file)
		dfs = sources.DirectFileSource(file=os.path.join(self.dir, 'export.csv'), slow_fallback=True)
		settings.add_source(dfs, prevent_duplicate=True, save_after=False)

	def test_unique_types(self):
		""" Source types should be unqiue """
		types = []
		for s in sources.load_sources(None):
			self.assertTrue(s.type, "Source is missing a type! %s" % s.__class__.__name__)
			self.assertNotIn(s.type, types, msg="Source type %s is not unique! (%s)" % (s.type, s.__class__.__name__))
			types.append(s.type)

	def test_unique_description(self):
		""" Source descriptions should be unique """
		types = []
		for s in sources.load_sources(None):
			self.assertTrue(s.description, "Source is missing a description! %s" % s.__class__.__name__)
			self.assertNotIn(s.description, types, msg="Source desc %s is not unique! (%s)" % (s.description, s.__class__.__name__))
			types.append(s.description)

	def test_settings_sources(self):
		""" Should properly load Sources from settings  """
		self.assertGreater(len(sources.all_sources()), 0, "Failed to load any Sources from settings file!")

	def test_config_summaries(self):
		""" All config summaries should work once loaded """
		for s in settings.get_sources():
			print(s.get_alias())
			self.assertTrue(s.get_config_summary(), 'Source %s is missing a config summary!' % s.type)

	def test_load_elements(self):
		""" Loading elements should work for all Sources """
		for s in settings.get_sources():
			print(s)
			eles = [re for re in s.get_elements()]
			self.assertGreater(len(eles), 0, "Failed to load any elements from test Source: %s" % s.get_alias())
			self.assertTrue(all(e for e in eles), "Loaded invalid RedditElements: %s" % eles)

	def test_to_obj(self):
		""" All sources should convert to objects """
		for s in settings.get_sources():
			self.assertTrue(s.to_obj(), "Failed to decode Source: %s" % s.type)
			self.assertTrue(s.to_obj(for_webui=True), "Failed to decode webui-Source for: %s" % s.type)
