import tempfile,pathlib,hashlib,zipfile
from reference.release_package import package,verify
from tests.test_packaging import fixture,SHA
def demo():
    checks=[]
    with tempfile.TemporaryDirectory() as tmp:
        root=pathlib.Path(tmp);source=fixture(root/'source');receipt=package('api',source,root/'first',SHA)
        checks.append({'name':'Actual package verifier accepts the fixture archive','passed':verify('api',root/'first',SHA)==receipt,'detail':'Original package/verify functions; fictional build inputs'})
        second=package('api',source,root/'second',SHA)
        checks.append({'name':'Identical inputs produce identical ZIP bytes','passed':receipt==second,'detail':'Sorted paths and fixed ZIP metadata'})
        (source/'dist/src/functions/health.test.js').write_text('fixture test');(source/'dist/src/functions/health.js.map').write_text('fixture map');package('api',source,root/'filtered',SHA)
        with zipfile.ZipFile(root/'filtered/release.zip') as z:clean=not any('.test.' in n or n.endswith('.map') for n in z.namelist())
        checks.append({'name':'Application tests and source maps stay out of the package','passed':clean,'detail':'Actual archive filter'})
        try:verify('api',root/'first','b'*40);blocked=False
        except RuntimeError:blocked=True
        checks.append({'name':'Wrong selected source is rejected','passed':blocked,'detail':'Receipt source mismatch'})
        p=root/'first/release.zip';p.write_bytes(p.read_bytes()+b'changed')
        try:verify('api',root/'first',SHA);blocked=False
        except RuntimeError:blocked=True
        checks.append({'name':'Modified artifact bytes are rejected','passed':blocked,'detail':'Archive digest mismatch'})
        (source/'dist/src/functions/health.js').write_text('app.http("unreviewed", {});');package('api',source,root/'unreviewed',SHA)
        try:verify('api',root/'unreviewed',SHA);blocked=False
        except RuntimeError:blocked=True
        checks.append({'name':'A function without its commissioning shield is rejected','passed':blocked,'detail':'Public health-only isolation profile'})
    return {'checks':checks,'metrics':[{'label':'Runtime','value':'Node 22','detail':'Actual Flex source setting'},{'label':'Package path','value':'TypeScript → ZIP','detail':'No ACR image required'},{'label':'Azure operations','value':'0','detail':'Offline package validation'},{'label':'Artifact identity','value':'SHA-256','detail':'Selected source and bytes'}],'records':[['Fixture package','Verified',receipt['sha256'][:16]],['Wrong source','Rejected','Receipt must match selection'],['Changed archive','Rejected','Same artifact required'],['New function','Rejected','Missing explicit shield']]}
