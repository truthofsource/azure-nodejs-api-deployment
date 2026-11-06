import copy,json,pathlib,tempfile,unittest,zipfile,stat
from reference.release_package import package,verify
SHA='a'*40
def fixture(root):
    for name in ['dist/src/functions','node_modules/example-runtime','migrations','form-templates']:(root/name).mkdir(parents=True)
    for name,value in [('host.json','{"version":"2.0"}'),('package.json','{"main":"dist/src/functions/*.js"}'),('package-lock.json','{}'),('dist/src/functions/health.js','app.http("health", {handler:health});'),('node_modules/example-runtime/index.js','// fictional dependency'),('migrations/README.md','fixture'),('form-templates/README.md','fixture')]: (root/name).write_text(value)
    return root
class PackagingTests(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=pathlib.Path(self.temp.name);self.source=fixture(self.root/'source');self.output=self.root/'out'
    def tearDown(self):self.temp.cleanup()
    def test_actual_packager_roundtrip_and_deterministic_bytes(self):
        a=package('api',self.source,self.output,SHA);self.assertEqual(verify('api',self.output,SHA),a);b=package('api',self.source,self.root/'second',SHA);self.assertEqual(a,b)
    def test_tests_and_maps_are_not_shipped(self):
        (self.source/'dist/src/functions/health.test.js').write_text('test');(self.source/'dist/src/functions/health.js.map').write_text('map');package('api',self.source,self.output,SHA)
        with zipfile.ZipFile(self.output/'release.zip') as z:self.assertFalse(any('.test.' in n or n.endswith('.map') for n in z.namelist()))
    def test_changed_bytes_are_rejected(self):
        package('api',self.source,self.output,SHA);p=self.output/'release.zip';p.write_bytes(p.read_bytes()+b'changed')
        with self.assertRaises(RuntimeError):verify('api',self.output,SHA)
    def test_wrong_source_is_rejected(self):
        package('api',self.source,self.output,SHA)
        with self.assertRaises(RuntimeError):verify('api',self.output,'b'*40)
    def test_missing_entrypoint_is_rejected(self):
        (self.source/'dist/src/functions/health.js').unlink()
        with self.assertRaises(RuntimeError):package('api',self.source,self.output,SHA)
    def test_unreviewed_function_is_rejected(self):
        (self.source/'dist/src/functions/health.js').write_text('app.http("unreviewed", {});');package('api',self.source,self.output,SHA)
        with self.assertRaises(RuntimeError):verify('api',self.output,SHA)
    def test_dynamic_registration_is_rejected(self):
        (self.source/'dist/src/functions/health.js').write_text('app.http(name, {});');package('api',self.source,self.output,SHA)
        with self.assertRaises(RuntimeError):verify('api',self.output,SHA)
