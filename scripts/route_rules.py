"""Select evidence-backed hardware rule modules; never edit an EDA design."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEATURES = {'power', 'high_speed', 'differential', 'crystal', 'analog', 'switching_power', 'rf', 'fpc'}
NET_CLASSES = {'power','ground','low_speed','high_speed','differential','crystal','analog','switching_power','rf','unknown'}
STAGES = {'inspect', 'schematic', 'layout', 'routing', 'final'}

def select(inventory, stage):
    if stage not in STAGES:
        raise ValueError('Unknown stage')
    for k in ('project', 'revision', 'source_sha256', 'components', 'nets', 'features'):
        if k not in inventory:
            raise ValueError(f'Missing inventory field: {k}')
    if not inventory['project'] or not inventory['revision']:
        raise ValueError('Project and revision are required')
    if not isinstance(inventory['components'],list) or not inventory['components']:
        raise ValueError('Need the complete component inventory')
    if not isinstance(inventory['nets'],list) or not inventory['nets']:
        raise ValueError('Need the complete net inventory')
    for field,key in [('components','ref'),('nets','name')]:
        names=[x.get(key) for x in inventory[field]]
        if len(names)!=len(set(names)):raise ValueError(f'Duplicate {field} identity')
    if len(inventory['source_sha256']) != 64 or any(c not in '0123456789abcdef' for c in inventory['source_sha256']):
        raise ValueError('Inventory must identify a SHA-256 source snapshot')
    registry = json.loads((ROOT/'profiles/catalog.json').read_text(encoding='utf-8'))
    enabled, unresolved, reasons = {'common'}, [], {}
    is_pcb = stage in {'layout', 'routing', 'final'}
    if stage == 'schematic': enabled.add('schematic')
    if is_pcb: enabled.update({'pcb', 'silkscreen', 'power'})
    layers = inventory.get('layers')
    if is_pcb and (not isinstance(layers, int) or layers < 1): unresolved.append('Actual copper layer count is unknown')
    elif is_pcb and layers > 2: enabled.add('multilayer')
    for feature in sorted(FEATURES):
        fact = inventory['features'].get(feature, {})
        state = fact.get('state', 'unknown')
        if state not in {'present','absent','unknown'}: raise ValueError(f'{feature}: invalid state')
        if state in {'present','absent'} and not fact.get('evidence'):
            raise ValueError(f'{feature}: classification requires evidence')
        reasons[feature] = fact
        if state == 'unknown': unresolved.append(f'{feature}: needs classification')
        elif state == 'present': enabled.add(registry['feature_modules'][feature])
    for obj in inventory['nets']:
        cls=obj.get('class','unknown')
        if cls not in NET_CLASSES:raise ValueError(f'Unknown net class: {cls}')
        if cls == 'unknown' or not obj.get('evidence'):
            unresolved.append(f"Net {obj.get('name','?')}: class/evidence missing")
        elif cls in FEATURES:
            enabled.add(registry['feature_modules'][cls])
            if inventory['features'].get(cls,{}).get('state')=='absent':
                unresolved.append(f"Net {obj.get('name')}: class conflicts with absent {cls}")
    for obj in inventory['components']:
        if not obj.get('ref') or not obj.get('role') or not obj.get('evidence'):
            unresolved.append(f"Component {obj.get('ref','?')}: role/evidence missing")
    for k in enabled:
        if k not in registry['modules']: raise ValueError(f'Unregistered module: {k}')
    modules = {k: registry['modules'][k] for k in sorted(enabled)}
    return {'schema_version': 1, 'skill_version': json.loads((ROOT/'provenance.json').read_text())['version'],
            'project':inventory['project'], 'revision':inventory['revision'], 'source_sha256':inventory['source_sha256'],
            'stage':stage, 'modules':modules, 'classification':reasons, 'unresolved':unresolved,
            'routing_status':'needs_review' if unresolved else 'classified',
            'evidence_status':'not_checked', 'note':'Classification is not electrical, DRC or stage approval.'}

def validate_plan(plan, inventory, source):
    errors=[]
    if hashlib.sha256(source.read_bytes()).hexdigest()!=inventory['source_sha256']: errors.append('Stale source snapshot')
    expected=select(inventory,plan['stage'])
    for k in ('schema_version','skill_version','project','revision','source_sha256','stage','modules','classification','unresolved','routing_status'):
        if plan.get(k)!=expected.get(k): errors.append(f'Routing mismatch: {k}')
    errors.extend(expected['unresolved'])
    return errors

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('inventory',type=Path);p.add_argument('--stage',choices=sorted(STAGES),default='inspect')
    p.add_argument('--output',type=Path);p.add_argument('--check',type=Path);p.add_argument('--source',type=Path)
    a=p.parse_args(); inv=json.loads(a.inventory.read_text(encoding='utf-8-sig'))
    if a.check:
        if not a.source:p.error('--check requires --source')
        errors=validate_plan(json.loads(a.check.read_text()),inv,a.source)
        if errors:p.exit(1,'\n'.join(errors)+'\n')
        print('Routing coverage and snapshot match; engineering checks remain separate.')
    else:
        plan=select(inv,a.stage); text=json.dumps(plan,ensure_ascii=False,indent=2)+'\n'
        if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text,encoding='utf-8')
        print(json.dumps({'modules':list(plan['modules']),'status':plan['routing_status'],'unresolved':plan['unresolved']},ensure_ascii=False))

if __name__=='__main__':main()
