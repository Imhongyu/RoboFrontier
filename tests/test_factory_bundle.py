import io
import json
import os
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest

import numpy as np

from robofrontier import factory_bundle as bundle
from robofrontier import factory_server as server


def fixture(root):
    source=root/'original'
    motion=source/'run/motion';(motion/'source').mkdir(parents=True)
    scene=motion/'source/scene.xml';scene.write_text('<mujoco/>')
    bundle.write(motion/'source/workstation.json',dict(scene_sha256=bundle.digest(scene),case=dict(id='transport-a04-d1')))
    bundle.write(motion/'source/task.json',dict(family='transport',level=1))
    bundle.write(motion/'source/environment.json',{})
    (motion/'source/assets').mkdir();(motion/'source/assets/shared.bin').write_bytes(b'asset'*1000)
    (motion/'events.jsonl').write_text('')
    for name in ('actions.json','process.jsonl'):(motion.parent/name).write_text('{}\n')
    times=np.array([0.,.1,.2]);states=np.zeros((3,1),dtype='<u4')
    np.savez_compressed(motion/'chunk-000000.npz',base=states[0],xor=states,time_s=times)
    bundle.write(motion/'stream.json',dict(schema='robofrontier.motion.v1',case_id='transport-a04-d1',
        source_scene_sha256=bundle.digest(scene),sample_hz=10,nq=1,frames=3,
        chunks=[dict(file='chunk-000000.npz',sha256=bundle.digest(motion/'chunk-000000.npz'),frames=3)]))
    edit=source/'edit/edit.json'
    edit.parent.mkdir()
    np.savez_compressed(edit.parent/'selection.npz',source_time_s=times,keep=np.ones(3,dtype=bool))
    bundle.write(edit,dict(schema='robofrontier.station-edit.v2',case_id='transport-a04-d1',
        source_scene_sha256=bundle.digest(scene),source_stream_sha256=bundle.digest(motion/'stream.json'),
        events_sha256=bundle.digest(motion/'events.jsonl'),source_end_frame=2,source_hz=10,
        input_evidence_sha256={n:bundle.digest(motion.parent/n) for n in ('actions.json','process.jsonl')},
        selection_file='selection.npz',selection_sha256=bundle.digest(edit.parent/'selection.npz')))
    factory=source/'factory/scene.xml';factory.parent.mkdir();factory.write_text('<mujoco/>')
    bundle.write(factory.parent/'manifest.json',dict(scene_sha256=bundle.digest(factory)))
    asset=source/'asset';asset.mkdir()
    bundle.write(asset/'scene.json',dict(source_scene_sha256=bundle.digest(factory),source_scene='/old/computer/scene.xml'))
    (asset/'shared.bin').write_bytes(b'asset'*1000)
    cameras=source/'cameras.json'
    bundle.write(cameras,[dict(id='transport-a04-d1--'+view) for view in ('front','side')])
    release=source/'release.json'
    bundle.write(release,dict(schema='test',presentation=dict(fps=30),families=dict(transport=dict(speedup=1,fps=30,oracle=[dict(
        id='transport-a04-d1',directory=str(scene.parent),recording=str(motion),edit=str(edit),edit_sha256=bundle.digest(edit))]))))
    output=root/'bundle'
    bundle.export(output,factory,release,cameras,asset,source)
    return output


class FactoryBundleTests(unittest.TestCase):
    def test_portable_roundtrip_preserves_motion_edits_and_semantic_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data=fixture(root)
            result=bundle.pack(data,root/'factory.tar.gz')
            restored=root/'other-machine/data'
            bundle.restore(root/'factory.tar.gz',restored,result['archive_sha256'])
            shutil.rmtree(root/'original');shutil.rmtree(data)
            verified=bundle.verify(restored)
            self.assertEqual(verified['stations'],1)
            plan=server.prepare(restored,root/'batch',duration_s=.1,device='CPU')
            self.assertEqual(plan['jobs'],2)
            self.assertEqual(bundle.read(root/'batch/plan.json')['jobs'][0]['frames'],3)
            release=bundle.resolved_release(restored)
            spec=release['families']['transport']['oracle'][0]
            self.assertTrue((Path(spec['recording']).parent/'actions.json').is_file())
            self.assertTrue(Path(spec['directory']).is_relative_to(restored.resolve()))
            # Identical assets share disk blocks after archive restore.
            shared=[p for p in restored.rglob('shared.bin')]
            self.assertEqual(len({p.stat().st_ino for p in shared}),1)

    def test_corruption_is_rejected_before_installation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data=fixture(root)
            bundle.pack(data,root/'factory.tar.gz')
            with self.assertRaisesRegex(ValueError,'SHA-256'):
                bundle.restore(root/'factory.tar.gz',root/'restored','0'*64)
            self.assertFalse((root/'restored').exists())
            (data/'asset/shared.bin').write_bytes(b'changed')
            with self.assertRaisesRegex(ValueError,'checksum'):
                bundle.verify(data)

    def test_archive_traversal_and_symlinks_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);archive=root/'bad.tar.gz'
            for kind in ('traversal','symlink'):
                with tarfile.open(archive,'w:gz') as tar:
                    info=tarfile.TarInfo('../outside' if kind=='traversal' else 'link')
                    if kind=='symlink':info.type=tarfile.SYMTYPE;info.linkname='/etc/passwd';tar.addfile(info)
                    else:info.size=1;tar.addfile(info,io.BytesIO(b'x'))
                with self.assertRaises(ValueError):bundle.restore(archive,root/'installed',bundle.digest(archive))
                self.assertFalse((root/'outside').exists())
                self.assertFalse((root/'installed').exists())

    def test_frozen_plan_refuses_changed_inputs_and_slurm_is_explicit(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data=fixture(root)
            plan=Path(server.prepare(data,root/'batch',device='OPTIX')['plan'])
            with patch.object(server,'blender_path',return_value='/software/blender'):
                cmd=server.submit(plan,'example',parallel=2,dry_run=True)['command']
            self.assertIn('0-1%2',cmd);self.assertIn('--gres=gpu:1',cmd)
            self.assertIn('--signal=B:TERM@180',cmd)
            bundle.write(root/'batch/release.json',{})
            with self.assertRaisesRegex(ValueError,'release changed'):server.load_plan(plan)

    def test_download_parts_reassemble_the_checked_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data=fixture(root)
            bundle.pack(data,root/'factory.tar.gz')
            config=bundle.split_archive(root/'factory.tar.gz',data,root.as_uri(),part_bytes=1000)
            self.assertGreater(len(config['parts']),1)
            bundle.write(root/'download.json',config)
            installed=root/'installed'
            result=bundle.setup(root/'download.json',installed)
            self.assertEqual(result['bundle_sha256'],config['bundle_sha256'])
            self.assertEqual(bundle.setup(root/'download.json',installed)['status'],'verified')

    def test_failed_render_preserves_attempt_and_has_no_completion_marker(self):
        import subprocess
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data=fixture(root)
            plan=Path(server.prepare(data,root/'batch',device='CPU')['plan'])
            with self.assertRaises(subprocess.CalledProcessError):
                server.run_job(plan,0,blender=shutil.which('true'),scratch=root)
            job=root/'batch/jobs/transport-a04-d1--front'
            self.assertFalse((job/'complete.json').exists())
            attempts=list(job.glob('attempt-*/attempt.json'))
            self.assertEqual(len(attempts),1)
            self.assertEqual(bundle.read(attempts[0])['status'],'failed')
            self.assertTrue((attempts[0].parent/'render.log').is_file())
            self.assertEqual(server.status(plan)['jobs'][0]['status'],'failed')

    def test_plan_parameter_edits_are_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);data=fixture(root)
            plan=Path(server.prepare(data,root/'batch',device='CPU')['plan'])
            changed=bundle.read(plan);changed['samples']=999;bundle.write(plan,changed)
            with self.assertRaisesRegex(ValueError,'plan changed'):server.load_plan(plan)


if __name__=='__main__':unittest.main()
