"""Source/immutability and actual FFmpeg contracts for the editable tour."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
from robofrontier import factory_bundle as bundle, factory_editorial as editorial, factory_server as server
from robofrontier.cli import main
from test_factory_bundle import tour_fixture


class EditorialTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.data = tour_fixture(self.root)
        self.project = Path(editorial.create(self.data, self.root/'project')['project'])

    def test_full_project_has_source_bound_english_task_captions_and_editable_cameras(self):
        loaded = editorial.load(self.project, self.data)
        self.assertEqual(loaded['project']['duration_s'], 210.5)
        self.assertEqual((loaded['camera_plan'][0]['t'], loaded['camera_plan'][-1]['t']), (0,210.5))
        self.assertEqual(len(loaded['titles']), 5)
        text = ' '.join(x[2] for x in loaded['subtitles'])
        for family in ('relay','transport','mosaic','dial'):
            self.assertIn(family+'-a', text)
        self.assertIn('Level 3', text)
        self.assertIn('arms', text)
        self.assertNotIn('successfully', text)
        self.assertTrue((self.project.parent/'fonts/OFL.txt').is_file())
        self.assertEqual(len(loaded['files']), 6)

    def test_shipped_project_matches_the_release_lock_and_loads_without_local_recordings(self):
        root = Path(__file__).resolve().parents[1]
        shipped = editorial.load(root/'assets/robo_factory/tour-project.json')
        lock = bundle.read(root/'configs/factory-assets.json')
        self.assertEqual(shipped['project']['source']['bundle_sha256'],lock['bundle_sha256'])
        self.assertEqual(shipped['project']['duration_s']*shipped['project']['fps'],6315)
        self.assertIn('Multi-Robot World',shipped['titles'][0][2])

    def test_frozen_project_is_independent_and_changed_prepared_captions_block_execution(self):
        result = server.prepare(self.data,self.root/'render',mode='promo',device='CPU',project=self.project)
        plan_path = Path(result['plan'])
        plan = server.load_plan(plan_path)[1]
        titles = self.project.parent/'titles.srt'
        titles.write_text(titles.read_text().replace('RoboFrontier','Edited locally'))
        self.assertEqual(server.load_plan(plan_path)[1],plan)
        frozen = plan_path.parent/'editorial/titles.srt'
        frozen.write_text(frozen.read_text().replace('RoboFrontier','Changed after freeze'))
        with self.assertRaisesRegex(ValueError,'editorial inputs changed'):
            server.load_plan(plan_path)

    def test_wrong_source_or_bad_edit_is_rejected_before_output(self):
        project = bundle.read(self.project)
        original = json.dumps(project)
        for change in ({'source':dict(project['source'],scene_sha256='0'*64)},
                       {'fps':25}, {'duration_s':float('inf')}, {'duration_s':.01}, {'unknown':'typo'},
                       {'titles':'../outside.srt'}):
            with self.subTest(change=list(change)):
                edited = json.loads(original); edited.update(change)
                bundle.write(self.project,edited)
                with self.assertRaises(ValueError):
                    server.prepare(self.data,self.root/'bad',mode='promo',project=self.project)
                self.assertFalse((self.root/'bad').exists())
        self.project.write_text(original)
        keys = bundle.read(self.project.parent/'camera-plan.json')
        keys[1]['t'] = 0
        bundle.write(self.project.parent/'camera-plan.json',keys)
        with self.assertRaisesRegex(ValueError,'increase strictly'):
            editorial.load(self.project)

    def test_srt_overlap_and_unknown_camera_fields_are_not_silently_ignored(self):
        subtitles = self.project.parent/'subtitles.srt'
        original = subtitles.read_text()
        subtitles.write_text('1\n00:00:00,000 --> 00:00:03,000\nOne\n\n2\n00:00:02,000 --> 00:00:04,000\nTwo\n')
        with self.assertRaisesRegex(ValueError,'ordered English'):
            editorial.load(self.project)
        subtitles.write_text(original)
        keys = bundle.read(self.project.parent/'camera-plan.json')
        keys[0]['camera']['unknown_option'] = True
        bundle.write(self.project.parent/'camera-plan.json',keys)
        with self.assertRaisesRegex(ValueError,'position, target and FOV only'):
            editorial.load(self.project)

    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'Requires local FFmpeg/libass')
    def test_real_cli_text_only_edit_preserves_source_and_media_shape_and_retains_project(self):
        video = self.root/'raw.mp4'
        subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','color=c=blue:s=640x360:r=30',
                        '-t','1','-c:v','libx264','-pix_fmt','yuv420p',str(video)],check=True)
        checksum = bundle.digest(video)
        result_text = io.StringIO()
        with contextlib.redirect_stdout(result_text):
            code = main(['factory','edit-video','--project',str(self.project),
                         '--input',str(video),'--output',str(self.root/'edited')])
        self.assertEqual(code,0)
        result = json.loads(result_text.getvalue())
        report = bundle.read(result['report'])
        self.assertEqual(report['media'],{'width':640,'height':360,'fps':30.,'frames':30})
        self.assertTrue(report['full_decode_passed'])
        self.assertEqual(bundle.digest(video),checksum)
        self.assertEqual(editorial.load(result['project'])['files'],editorial.load(self.project)['files'])
        def pixels(path):
            return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
                '-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-']),dtype=np.uint8).reshape(360,640,3)
        before, after = pixels(video), pixels(result['video'])
        self.assertGreater(np.sum(np.any(abs(after[:160].astype(int)-before[:160].astype(int))>30,axis=2)),200)
        self.assertGreater(np.sum(np.any(abs(after[240:].astype(int)-before[240:].astype(int))>30,axis=2)),200)
        with self.assertRaises(ValueError):
            editorial.render(self.project,video,self.root/'edited')

    def test_completion_requires_both_raw_and_editorial_evidence(self):
        job = self.root/'job'; attempt = job/'attempt-test'; (attempt/'render').mkdir(parents=True)
        (attempt/'editorial').mkdir()
        (attempt/'render/factory.mp4').write_bytes(b'raw')
        (attempt/'editorial/factory.mp4').write_bytes(b'captioned')
        bundle.write(attempt/'render/report.json',{'animation':{'full_decode_passed':True}})
        bundle.write(attempt/'editorial/report.json',{'full_decode_passed':True,
                     'video_sha256':bundle.digest(attempt/'editorial/factory.mp4')})
        marker = {'attempt':'attempt-test','video_sha256':bundle.digest(attempt/'render/factory.mp4'),
                  'report_sha256':bundle.digest(attempt/'render/report.json'),
                  'editorial':{'video':'editorial/factory.mp4','report':'editorial/report.json',
                   'video_sha256':bundle.digest(attempt/'editorial/factory.mp4'),
                   'report_sha256':bundle.digest(attempt/'editorial/report.json')}}
        bundle.write(job/'complete.json',marker)
        self.assertIsNotNone(server.completed(job))
        (attempt/'editorial/factory.mp4').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'editorial output changed'):
            server.completed(job)
        marker.pop('editorial'); bundle.write(job/'complete.json',marker)
        self.assertIsNotNone(server.completed(job))  # Legacy markers retain their contract.
        with self.assertRaisesRegex(ValueError,'missing its required editorial'):
            server.completed(job,plan={'editorial':{'files':{}}})

    def test_new_promo_execution_needs_matching_editorial_before_sealing(self):
        # Exercise the real attempt/stop/stage-out path. Only the external pose
        # and Cycles executables are synthetic here; actual FFmpeg is tested above.
        def fake_process(argv, **kwargs):
            output = Path(argv[argv.index('--output')+1])
            output.mkdir(parents=True)
            if 'scripts.promo_preview' in argv:
                bundle.write(output/'animation.json',{'frames':[{}, {}, {}]})
            else:
                (output/'factory.mp4').write_bytes(b'raw')
                bundle.write(output/'report.json',{'animation':{
                    'full_decode_passed':True,'frames':3,'fps':30}})
            class Process:
                def wait(self, timeout=None): return 0
            return Process()

        for mode in ('success','compositor_failure','changed_during_render'):
            with self.subTest(mode=mode):
                plan = Path(server.prepare(self.data,self.root/mode,mode='promo',
                    device='CPU',duration_s=.1,project=self.project)['plan'])
                def composite(project, video, output, **kwargs):
                    if mode == 'compositor_failure':
                        raise ValueError('Synthetic caption encoding failure')
                    output.mkdir()
                    (output/'factory.mp4').write_bytes(b'captioned')
                    loaded = editorial.load(project)
                    editorial.freeze(project,output/'project')
                    bundle.write(output/'report.json',{'full_decode_passed':True,
                        'video_sha256':bundle.digest(output/'factory.mp4'),
                        'source_video_sha256':bundle.digest(video),
                        'media':{'width':1920,'height':1080,'fps':30,'frames':3},
                        'project_files':loaded['files']})
                    if mode == 'changed_during_render':
                        file = Path(project).parent/'titles.srt'
                        file.write_text(file.read_text().replace('RoboFrontier','Changed mid-render'))
                with patch.object(server.subprocess,'Popen',side_effect=fake_process), \
                        patch.object(server,'blender_path',return_value='/fake/blender'), \
                        patch.object(editorial,'render',side_effect=composite):
                    if mode == 'success':
                        self.assertEqual(server.run_job(plan,0)['status'],'complete')
                    else:
                        with self.assertRaisesRegex(ValueError,'encoding failure|editorial inputs changed'):
                            server.run_job(plan,0)
                job = plan.parent/'jobs/promo'
                self.assertFalse((job/'running.json').exists())
                self.assertEqual((job/'complete.json').exists(),mode=='success')
                attempt = next(job.glob('attempt-*/attempt.json'))
                self.assertEqual(bundle.read(attempt)['status'],'complete' if mode=='success' else 'failed')
                if mode == 'success':
                    state = server.status(plan)['jobs'][0]
                    self.assertTrue(state['video'].endswith('/editorial/factory.mp4'))
                    self.assertTrue(state['source_video'].endswith('/render/factory.mp4'))
                    retained = attempt.parent/'editorial/project/titles.srt'
                    original = retained.read_bytes()
                    retained.write_bytes(original.replace(b'RoboFrontier',b'Changed after seal'))
                    with self.assertRaisesRegex(ValueError,'project differs'):
                        server.status(plan)
                    retained.write_bytes(original)
                    marker = bundle.read(job/'complete.json'); marker.pop('editorial')
                    bundle.write(job/'complete.json',marker)
                    with self.assertRaisesRegex(ValueError,'missing its required editorial'):
                        server.status(plan)
