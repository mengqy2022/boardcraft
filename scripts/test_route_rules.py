import copy, hashlib, json, tempfile, unittest
from pathlib import Path
from route_rules import select, validate_plan, FEATURES

class RoutingTests(unittest.TestCase):
    def base(self):
        return {'project':'test','revision':'R1','source_sha256':hashlib.sha256(b'board').hexdigest(),'layers':2,
                'components':[{'ref':'J1','role':'input','evidence':'fixture:connector'}],
                'nets':[{'name':'P5V','class':'power','evidence':'fixture:pinmap'}],
                'features':{k:{'state':'present' if k=='power' else 'absent','evidence':'fixture:full inventory'} for k in FEATURES}}
    def test_simple_board_excludes_rf_and_fpc(self):
        r=select(self.base(),'routing'); self.assertEqual(set(r['modules']),{'common','pcb','power','silkscreen'});self.assertEqual(r['routing_status'],'classified')
    def test_mixed_board_combines_modules(self):
        b=self.base();b['layers']=4
        for k in ('rf','fpc','differential','switching_power'):b['features'][k]['state']='present'
        r=select(b,'final');self.assertTrue({'rf','fpc','high-speed','switching-power','multilayer'}<=r['modules'].keys())
    def test_unknown_does_not_become_absent(self):
        b=self.base();b['features'].pop('rf');r=select(b,'routing');self.assertEqual(r['routing_status'],'needs_review');self.assertTrue(any('rf:' in s for s in r['unresolved']))
    def test_absent_requires_evidence(self):
        b=self.base();b['features']['rf'].pop('evidence')
        with self.assertRaises(ValueError):select(b,'layout')
    def test_net_name_does_not_infer_usb(self):
        b=self.base();b['nets']=[{'name':'USB_D+','class':'unknown'}];r=select(b,'routing');self.assertNotIn('high-speed',r['modules']);self.assertEqual(r['routing_status'],'needs_review')
    def test_stale_and_tampered_plan_rejected(self):
        b=self.base();p=select(b,'final');p['modules'].pop('power')
        with tempfile.TemporaryDirectory() as t:
            f=Path(t)/'board';f.write_bytes(b'changed');e=validate_plan(p,b,f)
        self.assertIn('Stale source snapshot',e);self.assertIn('Routing mismatch: modules',e)
    def test_schematic_profile(self):
        self.assertIn('schematic',select(self.base(),'schematic')['modules'])
    def test_empty_identity_rejected(self):
        b=self.base();b['revision']=''
        with self.assertRaises(ValueError):select(b,'routing')
    def test_confirmed_network_cannot_be_silently_excluded(self):
        b=self.base();b['nets']=[{'name':'RF_PORT','class':'rf','evidence':'fixture:datasheet'}]
        r=select(b,'routing');self.assertIn('rf',r['modules']);self.assertEqual(r['routing_status'],'needs_review')
    def test_invalid_class_and_duplicates_rejected(self):
        b=self.base();b['nets'][0]['class']='guess'
        with self.assertRaises(ValueError):select(b,'routing')
        b=self.base();b['components']*=2
        with self.assertRaises(ValueError):select(b,'routing')

if __name__=='__main__':unittest.main()
