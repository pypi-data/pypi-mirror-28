__author__ = 'churas'

import unittest
import tempfile
import os.path
import stat
import signal

"""
test_evaluation
--------------------------------

Tests for `evaluation` module.
"""
import shutil
import os

from mock import Mock

from d3r.celpp.task import D3RParameters
from d3r.celpp.task import D3RTask
from d3r.celpp.dataimport import DataImportTask
from d3r.celpp.blastnfilter import BlastNFilterTask
from d3r.celpp.evaluation import EvaluationTaskFactory
from d3r.celpp.evaluation import EvaluationTask
from d3r.celpp.challengedata import ChallengeDataTask
from d3r.celpp.glide import GlideTask
from d3r.celpp.evaluation import PathNotDirectoryError
from d3r.celpp.participant import ParticipantDatabaseFromCSVFactory
from d3r.celpp.participant import ParticipantDatabase
from d3r.celpp.participant import Participant
from d3r.celpp.task import SmtpEmailer
from d3r.celpp.evaluation import EvaluationEmailer


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_uploadable_files(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()

            task = EvaluationTask(temp_dir, 'glide',
                                  GlideTask(temp_dir, params), params)
            # try with no dir
            self.assertEqual(task.get_uploadable_files(), [])

            # try with empty dir
            task.create_dir()
            self.assertEqual(task.get_uploadable_files(), [])

            # try with final log
            final_log = os.path.join(task.get_dir(),
                                     EvaluationTask.FINAL_LOG)
            open(final_log, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 1)
            flist.index(final_log)

            # try with RMSD.txt
            rmsd = os.path.join(task.get_dir(),
                                EvaluationTask.RMSD_TXT)
            open(rmsd, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 2)
            flist.index(rmsd)

            # try with RMSD.json
            rmsdjson = os.path.join(task.get_dir(),
                                    EvaluationTask.RMSD_JSON)
            open(rmsdjson, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 3)
            flist.index(rmsd)
            flist.index(final_log)
            flist.index(rmsdjson)

            # try with evaluate.exitcode
            evalexit = os.path.join(task.get_dir(),
                                    EvaluationTask.EVAL_EXITCODEFILE)
            open(evalexit, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 4)
            flist.index(rmsd)
            flist.index(final_log)
            flist.index(rmsdjson)
            flist.index(evalexit)

            # try with empty pbdid dir
            pbdid = os.path.join(task.get_dir(), '8www')
            os.mkdir(pbdid)
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 4)
            flist.index(rmsd)

            # try with score/rot-LMCSS_doc_pv_complex1.pdb
            score = os.path.join(pbdid, 'score')
            os.mkdir(score)
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 4)

            LMCSS = os.path.join(score, 'LMCSS-1fcz_1fcz_docked_complex.pdb')
            open(LMCSS, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 5)
            flist.index(LMCSS)

            # try with score/rot-SMCSS_doc_pv_complex1.pdb
            SMCSS = os.path.join(score, 'SMCSS-1fcz_2lbd_docked_complex.pdb')
            open(SMCSS, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 6)
            flist.index(SMCSS)

            # try with score/rot-hiResApo_doc_pv_complex1.pdb
            hiResApo = os.path.join(score,
                                    'hiResHolo-1fcz_1fcy_docked_complex.pdb')
            open(hiResApo, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 7)
            flist.index(hiResApo)

            # try with score/rot-hiResHolo_doc_pv_complex1.pdb
            hiResHolo = os.path.join(score,
                                     'hiTanimoto-1fcz_1fcz_docked_complex.pdb')
            open(hiResHolo, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 8)
            flist.index(hiResHolo)

            # try with score/crystal.pdb
            crystal = os.path.join(score, 'crystal.pdb')
            open(crystal, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 9)
            flist.index(crystal)

            # try with RMSD.pickle
            rmsdpickle = os.path.join(task.get_dir(),
                                      EvaluationTask.RMSD_PICKLE)
            open(rmsdpickle, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 10)
            flist.index(rmsdpickle)

            # try with stderr/stdout files
            errfile = os.path.join(task.get_dir(), 'evaluate.py.stderr')
            open(errfile, 'a').close()
            outfile = os.path.join(task.get_dir(), 'evaluate.py.stdout')
            open(outfile, 'a').close()
            flist = task.get_uploadable_files()
            self.assertEqual(len(flist), 12)
            flist.index(crystal)
            flist.index(hiResHolo)
            flist.index(hiResApo)
            flist.index(SMCSS)
            flist.index(LMCSS)
            flist.index(errfile)
            flist.index(outfile)
            flist.index(final_log)
            flist.index(rmsd)
            flist.index(rmsdpickle)
            flist.index(rmsdjson)
            flist.index(evalexit)
        finally:
            shutil.rmtree(temp_dir)

    def test_evaluationtaskfactory_update_priorities_of_tasks(self):
        params = D3RParameters()
        params.hi = True
        etf = EvaluationTaskFactory('/foo', params)

        plist = [Participant('1name', '1d3rusername', '12345',
                             '1email@email.com',
                             priority=4),
                 Participant('4name', '4d3rusername', '5678_foo',
                             '4email@email.com',
                             priority=9)]

        pdb = ParticipantDatabase(plist)

        # one task not updated
        dtask = D3RTask('/foo', params)
        dtask.set_name('33' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        task = EvaluationTask('/foo', dtask.get_name(),
                              dtask, params)
        self.assertEqual(task.get_priority(), 0)
        etasks = etf._update_priorities_of_tasks([task], pdb)
        self.assertEqual(len(etasks), 1)
        self.assertEqual(etasks[0].get_priority(), 0)

        # two tasks both updated
        dtask = D3RTask('/foo', params)
        dtask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        taskone = EvaluationTask('/foo', dtask.get_name(),
                                 dtask, params)
        self.assertEqual(taskone.get_priority(), 0)

        dtask = D3RTask('/foo', params)
        dtask.set_name('5678_foo' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        tasktwo = EvaluationTask('/foo', dtask.get_name(),
                                 dtask, params)
        self.assertEqual(tasktwo.get_priority(), 0)

        etasks = etf._update_priorities_of_tasks([taskone, tasktwo], pdb)
        self.assertEqual(len(etasks), 2)
        self.assertEqual(etasks[0].get_priority(), 4)
        self.assertEqual(etasks[1].get_priority(), 9)

    def test_evaluationtaskfactory_sort_tasks_by_participant_priority(self):
        params = D3RParameters()
        params.hi = True
        etf = EvaluationTaskFactory('/foo', params)

        # test with no tasks
        self.assertEqual(etf._sort_tasks_by_participant_priority(None, None),
                         None)

        # test with NO participant database
        self.assertEqual(etf._sort_tasks_by_participant_priority([params],
                                                                 None),
                         [params])

        plist = [Participant('1name', '1d3rusername', '12345',
                             '1email@email.com',
                             priority=4),
                 Participant('4name', '4d3rusername', '5678_foo',
                             '4email@email.com',
                             priority=9)]

        pdb = ParticipantDatabase(plist)
        # two tasks both updated
        dtask = D3RTask('/foo', params)
        dtask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        taskone = EvaluationTask('/foo', dtask.get_name(),
                                 dtask, params)
        self.assertEqual(taskone.get_priority(), 0)

        dtask = D3RTask('/foo', params)
        dtask.set_name('5678_foo' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        tasktwo = EvaluationTask('/foo', dtask.get_name(),
                                 dtask, params)
        self.assertEqual(tasktwo.get_priority(), 0)

        etasks = etf._sort_tasks_by_participant_priority([taskone, tasktwo],
                                                         pdb)
        self.assertEqual(len(etasks), 2)
        self.assertEqual(etasks[0].get_priority(), 9)
        self.assertEqual(etasks[0].get_name(), '5678_foo' +
                         EvaluationTask.EXT_SUBMISSION_SUFFIX)

        self.assertEqual(etasks[1].get_priority(), 4)
        self.assertEqual(etasks[1].get_name(), '12345' +
                         EvaluationTask.EXT_SUBMISSION_SUFFIX)

    def test_evaluationtaskfactory_constructor(self):
        params = D3RParameters()
        params.hi = True
        stf = EvaluationTaskFactory('/foo', params)
        self.assertEquals(stf.get_args().hi, True)
        self.assertEquals(stf.get_path(), '/foo')

    def test_get_evaluation_tasks_invalid_path(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            path = os.path.join(temp_dir, 'doesnotexist')
            stf = EvaluationTaskFactory(path, params)
            try:
                stf.get_evaluation_tasks()
                self.fail('Expected PathNotDirectoryError')
            except PathNotDirectoryError:
                pass

        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_empty_dir(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 0)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_dir_with_lower_stages_dirs(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            dataimport = DataImportTask(temp_dir, params)
            blast = BlastNFilterTask(temp_dir, params)
            os.mkdir(os.path.join(temp_dir, dataimport.get_dir_name()))
            os.mkdir(os.path.join(temp_dir, blast.get_dir_name()))

            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 0)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_dir_with_webdata_dir(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            os.mkdir(os.path.join(temp_dir,
                                  EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                  EvaluationTaskFactory.WEB_DATA_SUFFIX))

            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 0)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_with_valid_completed_algo_dir(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()

            glidetask = GlideTask(temp_dir, params)
            glidetask.create_dir()

            open(os.path.join(glidetask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()

            etask = EvaluationTask(temp_dir,
                                   glidetask.get_name() + '.' +
                                   EvaluationTaskFactory.SCORING_SUFFIX,
                                   glidetask,
                                   params)
            etask.create_dir()
            open(os.path.join(etask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 0)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_with_valid_algo_dir(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            glidedir = os.path.join(temp_dir,
                                    EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                    'glide')
            os.mkdir(glidedir)
            open(os.path.join(glidedir, D3RTask.COMPLETE_FILE), 'a').close()
            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 1)
            self.assertEquals(task_list[0].get_name(), 'glide.evaluation')
        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_with_two_valid_algo_dir(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()

            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()

            glidedir = os.path.join(temp_dir,
                                    EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                    'glide')
            os.mkdir(glidedir)
            open(os.path.join(glidedir, D3RTask.COMPLETE_FILE), 'a').close()

            freddir = os.path.join(temp_dir,
                                   EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                   'fred')
            os.mkdir(freddir)
            open(os.path.join(freddir, D3RTask.COMPLETE_FILE), 'a').close()

            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 2)
            self.assertNotEquals(task_list[0].get_name(),
                                 task_list[1].get_name())

        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_with_one_invalid_algo(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()

            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()

            glidedir = os.path.join(temp_dir,
                                    EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                    'glide')
            os.mkdir(glidedir)
            open(os.path.join(glidedir, D3RTask.ERROR_FILE), 'a').close()

            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 0)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_tasks_on_with_one_valid_and_one_invalid_algo(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()

            glidedir = os.path.join(temp_dir,
                                    EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                    'glide')
            os.mkdir(glidedir)
            open(os.path.join(glidedir, D3RTask.ERROR_FILE), 'a').close()
            freddir = os.path.join(temp_dir,
                                   EvaluationTaskFactory.DOCKSTAGE_PREFIX +
                                   'fred')
            os.mkdir(freddir)
            open(os.path.join(freddir, D3RTask.COMPLETE_FILE), 'a').close()

            stf = EvaluationTaskFactory(temp_dir, params)
            task_list = stf.get_evaluation_tasks()
            self.assertEquals(len(task_list), 1)
            self.assertEquals(task_list[0].get_name(), 'fred.evaluation')
        finally:
            shutil.rmtree(temp_dir)

    def test_evaluationtask_constructor(self):
        params = D3RParameters()
        # no dock task found so it cannot run
        docktask = D3RTask('/blah', params)
        docktask.set_name('foo')
        docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)

        evaluation = EvaluationTask('/blah', 'foo.evaluation',
                                    docktask, params)
        self.assertEquals(evaluation.get_name(), 'foo.evaluation')
        self.assertEquals(evaluation.get_stage(), 7)
        self.assertEqual(evaluation.get_priority(), 0)
        evaluation.set_priority(4)
        self.assertEqual(evaluation.get_priority(), 4)

    def test_write_evaluate_exitcode_file(self):
        # test where no directory exists so an error
        # should be thrown
        params = D3RParameters()
        # no dock task found so it cannot run
        evaluation = EvaluationTask('/blah', 'foo.evaluation',
                                    None, params)
        evaluation._write_evaluate_exitcode_file(0)
        self.assertTrue('exception trying to write exit code file' in
                        evaluation.get_email_log())

        # try with various values
        temp_dir = tempfile.mkdtemp()
        try:
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        None, params)
            evaluation.create_dir()

            # try with None
            evaluation._write_evaluate_exitcode_file(None)
            efile = os.path.join(evaluation.get_dir(),
                                 EvaluationTask.EVAL_EXITCODEFILE)
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, 'None')
            self.assertEqual(evaluation.get_email_log(), None)

            # try with 0
            evaluation._write_evaluate_exitcode_file(0)
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, '0')
            self.assertEqual(evaluation.get_email_log(), None)

            # try with foo
            evaluation._write_evaluate_exitcode_file('foo')
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, 'foo')
            self.assertEqual(evaluation.get_email_log(), None)

        finally:
            shutil.rmtree(temp_dir)

    def test_can_run(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            # no dock task found so it cannot run
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)

            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            self.assertEqual(evaluation.can_run(), False)
            self.assertEqual(evaluation.get_error(),
                             'foo task has notfound status')

            # docktask  running
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.START_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            self.assertEqual(evaluation.can_run(), False)
            self.assertEqual(evaluation.get_error(),
                             'foo task has start status')

            # docktask failed
            error_file = os.path.join(docktask.get_dir(),
                                      D3RTask.ERROR_FILE)
            open(error_file, 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            self.assertEqual(evaluation.can_run(), False)
            self.assertEqual(evaluation.get_error(),
                             'foo task has error status')

            # docktask success and blasttask missing
            os.remove(error_file)
            open(os.path.join(docktask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            self.assertEqual(evaluation.can_run(), False)
            blasttask = BlastNFilterTask(temp_dir, params)
            self.assertEqual(evaluation.get_error(),
                             blasttask.get_name() + ' task has ' +
                             D3RTask.NOTFOUND_STATUS + ' status')

            # create blast task success
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()

            # docktask and blastnfilter success
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            self.assertEqual(evaluation.can_run(), True)
            self.assertEqual(evaluation.get_error(), None)

            # evaluation task exists already
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.create_dir()
            self.assertEqual(evaluation.can_run(), False)
            self.assertEqual(evaluation.get_error(),
                             evaluation.get_dir_name() +
                             ' already exists and status is unknown')

            # evaluation task already complete
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            open(os.path.join(evaluation.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            self.assertEqual(evaluation.can_run(), False)
            self.assertEqual(evaluation.get_error(), None)

        finally:
            shutil.rmtree(temp_dir)

    def test_run_fails_cause_can_run_is_false(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            # return immediately cause can_run is false
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(),
                             'foo task has notfound status')
        finally:
            shutil.rmtree(temp_dir)

    def test_run_fails_cause_evaluation_not_set(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(),
                             'evaluation not set')
            # test files get created
            self.assertEqual(os.path.isdir(evaluation.get_dir()),
                             True)
            errfile = os.path.join(evaluation.get_dir(),
                                   D3RTask.ERROR_FILE)
            self.assertEqual(os.path.isfile(errfile), True)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_fails_cause_pdbdb_not_set(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            params.evaluation = 'true'
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(),
                             'pdbdb not set')
            # test files get created
            self.assertEqual(os.path.isdir(evaluation.get_dir()),
                             True)
            errfile = os.path.join(evaluation.get_dir(),
                                   D3RTask.ERROR_FILE)
            self.assertEqual(os.path.isfile(errfile), True)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_fails_cause_evaluation_fails(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()

            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()

            params.evaluation = 'false'
            params.pdbdb = '/data/pdb'
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(), None)
            # test file gets created
            compfile = os.path.join(evaluation.get_dir(),
                                    D3RTask.COMPLETE_FILE)
            self.assertEqual(os.path.isfile(compfile), True)

            stderr = os.path.join(evaluation.get_dir(),
                                  'false.stderr')
            self.assertEqual(os.path.isfile(stderr), True)
            stdout = os.path.join(evaluation.get_dir(),
                                  'false.stdout')
            self.assertEqual(os.path.isfile(stdout), True)
        finally:
            shutil.rmtree(temp_dir)

    def test_run_fails_cause_evaluation_is_not_found(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            params.evaluation = '/bin/doesnotexist'
            params.pdbdb = '/data/pdb'
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()

            challenge = ChallengeDataTask(temp_dir, params)
            cdir = os.path.join(challenge.get_dir(),
                                challenge.get_celpp_challenge_data_dir_name())

            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertTrue('/bin/doesnotexist --pdbdb /data/pdb '
                            in evaluation.get_error())
            self.assertTrue(' --dockdir ' + docktask.get_dir()
                            in evaluation.get_error())
            self.assertTrue(' --outdir ' + evaluation.get_dir()
                            in evaluation.get_error())
            self.assertTrue(' --challengedir ' + cdir
                            in evaluation.get_error())
            self.assertTrue(' --blastnfilterdir ' + blasttask.get_dir()
                            in evaluation.get_error())
            self.assertTrue(' : [Errno 2] No such file or directory'
                            in evaluation.get_error())

            # test files get created
            errfile = os.path.join(evaluation.get_dir(),
                                   D3RTask.ERROR_FILE)
            self.assertEqual(os.path.isfile(errfile), True)

            efile = os.path.join(evaluation.get_dir(),
                                 EvaluationTask.EVAL_EXITCODEFILE)
            self.assertTrue(os.path.isfile(efile))
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, '1')

        finally:
            shutil.rmtree(temp_dir)

    def test_run_succeeds_no_emailer(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            params.evaluation = 'true'
            params.pdbdb = '/data/pdb'
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(), None)
            # test files get created
            errfile = os.path.join(evaluation.get_dir(),
                                   D3RTask.ERROR_FILE)
            self.assertEqual(os.path.isfile(errfile), False)

            compfile = os.path.join(evaluation.get_dir(),
                                    D3RTask.COMPLETE_FILE)
            self.assertEqual(os.path.isfile(compfile), True)
            stderr = os.path.join(evaluation.get_dir(),
                                  'true.stderr')
            self.assertEqual(os.path.isfile(stderr), True)
            stdout = os.path.join(evaluation.get_dir(),
                                  'true.stdout')
            self.assertEqual(os.path.isfile(stdout), True)
            efile = os.path.join(evaluation.get_dir(),
                                 EvaluationTask.EVAL_EXITCODEFILE)
            self.assertTrue(os.path.isfile(efile))
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, '0')
        finally:
            shutil.rmtree(temp_dir)

    def test_run_succeeds_no_emailer_withtimeout(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            params.evaluation = 'true'
            params.evaluationtimeout = 100
            params.evaluationtimeoutkilldelay = 10
            params.pdbdb = '/data/pdb'
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(), None)
            # test files get created
            errfile = os.path.join(evaluation.get_dir(),
                                   D3RTask.ERROR_FILE)
            self.assertEqual(os.path.isfile(errfile), False)

            compfile = os.path.join(evaluation.get_dir(),
                                    D3RTask.COMPLETE_FILE)
            self.assertEqual(os.path.isfile(compfile), True)
            stderr = os.path.join(evaluation.get_dir(),
                                  'true.stderr')
            self.assertEqual(os.path.isfile(stderr), True)
            stdout = os.path.join(evaluation.get_dir(),
                                  'true.stdout')
            self.assertEqual(os.path.isfile(stdout), True)

            efile = os.path.join(evaluation.get_dir(),
                                 EvaluationTask.EVAL_EXITCODEFILE)
            self.assertTrue(os.path.isfile(efile))
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, '0')
        finally:
            shutil.rmtree(temp_dir)

    def test_run_fails_due_to_timeout_no_emailer(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            foo_script = os.path.join(temp_dir, 'foo.py')
            params.evaluation = foo_script
            params.evaluationtimeout = 1
            params.evaluationtimeoutkilldelay = 2
            params.pdbdb = '/data/pdb'

            # create fake blastnfilter script that makes csv files
            f = open(foo_script, 'w')
            f.write('#! /usr/bin/env python\n\n')
            f.write('import time\n')
            f.write('time.sleep(360)\n')
            f.flush()
            f.close()
            os.chmod(foo_script, stat.S_IRWXU)

            docktask = D3RTask(temp_dir, params)
            docktask.set_name('foo')
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, 'foo.evaluation',
                                        docktask, params)
            evaluation.run()
            self.assertEqual(evaluation.get_error(), None)

            # test files get created
            compfile = os.path.join(evaluation.get_dir(),
                                    D3RTask.COMPLETE_FILE)
            self.assertEqual(os.path.isfile(compfile), True)
            stderr = os.path.join(evaluation.get_dir(),
                                  'foo.py.stderr')
            self.assertEqual(os.path.isfile(stderr), True)
            stdout = os.path.join(evaluation.get_dir(),
                                  'foo.py.stdout')
            self.assertEqual(os.path.isfile(stdout), True)

            efile = os.path.join(evaluation.get_dir(),
                                 EvaluationTask.EVAL_EXITCODEFILE)
            self.assertTrue(os.path.isfile(efile))
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, str(-signal.SIGTERM))
        finally:
            shutil.rmtree(temp_dir)

    def test_run_succeeds_with_emailer(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            params.evaluation = 'true'
            params.pdbdb = '/data/pdb'
            docktask = D3RTask(temp_dir, params)
            docktask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
            docktask.set_stage(EvaluationTaskFactory.DOCKSTAGE)
            docktask.create_dir()
            open(os.path.join(docktask.get_dir(), D3RTask.COMPLETE_FILE),
                 'a').close()
            evaluation = EvaluationTask(temp_dir, docktask.get_name(),
                                        docktask, params)
            plist = [Participant('1name', '1d3rusername', '12345',
                                 'bob@bob.com,joe@joe.com')]
            smtpemailer = SmtpEmailer()
            mockserver = D3RParameters()
            mockserver.sendmail = Mock()
            mockserver.quit = Mock()
            smtpemailer.set_alternate_smtp_server(mockserver)
            emailer = EvaluationEmailer(ParticipantDatabase(plist),
                                        smtpemailer)
            evaluation.set_evaluation_emailer(emailer)
            evaluation.run()
            self.assertEqual(evaluation.get_error(), None)
            # test files get created
            errfile = os.path.join(evaluation.get_dir(),
                                   D3RTask.ERROR_FILE)
            self.assertEqual(os.path.isfile(errfile), False)

            compfile = os.path.join(evaluation.get_dir(),
                                    D3RTask.COMPLETE_FILE)
            self.assertEqual(os.path.isfile(compfile), True)
            stderr = os.path.join(evaluation.get_dir(),
                                  'true.stderr')
            self.assertEqual(os.path.isfile(stderr), True)
            stdout = os.path.join(evaluation.get_dir(),
                                  'true.stdout')
            self.assertEqual(os.path.isfile(stdout), True)
            res = evaluation.get_email_log().endswith('\nSent evaluation '
                                                      'email to: bob@bob.com,'
                                                      ' joe@joe.com\n')
            self.assertTrue(res)

            efile = os.path.join(evaluation.get_dir(),
                                 EvaluationTask.EVAL_EXITCODEFILE)
            self.assertTrue(os.path.isfile(efile))
            with open(efile, 'r') as f:
                data = f.read().rstrip()
            self.assertEqual(data, '0')

        finally:
            shutil.rmtree(temp_dir)

    def test_get_evaluation_summary(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            task = EvaluationTask(temp_dir, 'foo', None, params)
            # test where no RMSD.txt file is found
            val = task.get_evaluation_summary()
            self.assertEqual(val,
                             '\nEvaluation of docking\n'
                             '=====================\nNo ' +
                             task.get_rmsd_txt() + ' file found.\n')

            # test with valid RMSD.txt file
            task.create_dir()
            f = open(task.get_rmsd_txt(), 'w')
            f.write('LMCSS\n1fcz 0.465\n')
            f.flush()
            f.close()
            val = task.get_evaluation_summary()
            self.assertEqual(val,
                             '\nEvaluation of docking\n'
                             '=====================\n'
                             'LMCSS\n1fcz 0.465\n\n')

            # test where reading RMSD.txt throws exception
            os.chmod(task.get_rmsd_txt(), 0)
            val = task.get_evaluation_summary()
            self.assertTrue(val.startswith('\nEvaluation of docking\n'
                                           '=====================\n'
                                           'Unable to generate evaluation'
                                           ' summary ('))
        finally:
            shutil.rmtree(temp_dir)

    def test_generate_external_submission_email_body(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            blasttask = BlastNFilterTask(temp_dir, params)
            blasttask.create_dir()
            open(os.path.join(blasttask.get_dir(),
                              D3RTask.COMPLETE_FILE), 'a').close()
            dtask = D3RTask('/foo', params)
            dtask.set_name('foo')
            task = EvaluationTask(temp_dir, dtask.get_name(), dtask, params)
            task.create_dir()
            emailer = EvaluationEmailer(None, None)
            task.set_evaluation_emailer(emailer)
            rmsd = task.get_rmsd_txt()
            f = open(rmsd, 'w')
            f.write('  LMCSS  XXX\n1fcz  0.2  0.4\n')
            f.flush()
            f.close()
            subject, body = emailer\
                ._generate_external_submission_email_body(task)
            self.assertEqual(subject,
                             '[d3rcelpp] Week 0 evaluation results for foo')
            self.assertEqual(body, 'Dear CELPP Participant,\n\nHere are your '
                                   'docking evaluation results as '
                                   'RMSD in Angstroms '
                                   'for CELPP week 0\n\n'
                                   'Note: The value in (parentheses) by each '
                                   'RMSD is the distance, in Angstroms, '
                                   'between submitted ligand center of mass '
                                   'and the crystal ligand center of mass. '
                                   'The final column is the distance between '
                                   'CELPP-provided pocket center and the '
                                   'crystal ligand center of mass.\n\n'
                                   '\nEvaluation of docking'
                                   '\n=====================\n  LMCSS  XXX\n'
                                   '1fcz  0.2  0.4\n\n\n\nSincerely,\n\n'
                                   'CELPP Automation ')
        finally:
            shutil.rmtree(temp_dir)

    def test_get_rmsd_txt(self):
        params = D3RParameters()
        task = EvaluationTask('/ha', 'foo', None, params)
        self.assertEqual(task.get_rmsd_txt(),
                         os.path.join('/ha', task.get_dir_name(),
                                      EvaluationTask.RMSD_TXT))

    def test_get_rmsd_pickle(self):
        params = D3RParameters()
        task = EvaluationTask('/ha', 'foo', None, params)
        self.assertEqual(task.get_rmsd_pickle(),
                         os.path.join('/ha', task.get_dir_name(),
                                      EvaluationTask.RMSD_PICKLE))

    def test_is_external_submission(self):
        params = D3RParameters()
        dtask = D3RTask('/ha', params)
        task = EvaluationTask('/ha', 'foo', dtask, params)
        dtask.set_name('blah')
        self.assertEqual(task.is_external_submission(), False)
        dtask.set_name('blah' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        self.assertEqual(task.is_external_submission(), True)

    def test_get_participant_database_no_csv_file_found(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            etf = EvaluationTaskFactory(temp_dir, params)
            pdb = etf._get_participant_database()
            self.assertEqual(pdb, None)
        finally:
            shutil.rmtree(temp_dir)

    def test_get_participant_database_with_valid_csvfile(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            dimport = DataImportTask(temp_dir, params)
            dimport.create_dir()
            csvfile = dimport.get_participant_list_csv()
            f = open(csvfile, 'w')
            f.write('name,d3rusername,guid,email\n')
            f.write('joe,jj,123,j@j.com\n')
            f.flush()
            f.close()
            etf = EvaluationTaskFactory(temp_dir, params)
            pdb = etf._get_participant_database()
            p = pdb.get_participant_by_guid('123')
            self.assertEqual(p.get_email(), 'j@j.com')
        finally:
            shutil.rmtree(temp_dir)

    def test_get_guid_for_task_dock_is_none(self):
        params = D3RParameters()
        task = EvaluationTask('/foo', 'blah' +
                              EvaluationTask.EXT_SUBMISSION_SUFFIX,
                              None,
                              params)
        self.assertEqual(task.get_guid_for_task(),
                         None)

    def test_get_guid_for_task(self):
        params = D3RParameters()
        dtask = D3RTask('/foo', params)
        dtask.set_name('123' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        task = EvaluationTask('/foo', dtask.get_name(),
                              dtask,
                              params)
        self.assertEqual(task.get_guid_for_task(),
                         '123')

    def test_eval_emailer_append_to_message_log(self):
        emailer = EvaluationEmailer(None, None)
        self.assertEqual(emailer.get_message_log(), None)
        emailer._append_to_message_log('hi\n')
        self.assertEqual(emailer.get_message_log(), 'hi\n')
        emailer._append_to_message_log('how\n')
        self.assertEqual(emailer.get_message_log(), 'hi\nhow\n')

    def test_eval_emailer_get_external_submitter_email_none_from_guid(self):
        emailer = EvaluationEmailer(None, None)
        params = D3RParameters()
        task = EvaluationTask('/foo', None, None, params)
        self.assertEqual(emailer._get_external_submitter_email(task), None)
        self.assertEqual(emailer.get_message_log(),
                         '\nUnable to extract guid\n')

    def test_get_external_submitter_email_participant_not_found(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            dimport = DataImportTask(temp_dir, params)
            dimport.create_dir()
            csvfile = dimport.get_participant_list_csv()
            f = open(csvfile, 'w')
            f.write('name,d3rusername,guid,email\n')
            f.write('joe,jj,123,j@j.com\n')
            f.flush()
            f.close()
            fac = ParticipantDatabaseFromCSVFactory(csvfile)
            params = D3RParameters()
            dtask = D3RTask('/foo', params)
            dtask.set_name('444' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
            task = EvaluationTask(temp_dir,
                                  dtask.get_name(),
                                  dtask, params)
            emailer = EvaluationEmailer(fac.get_participant_database(), None)
            self.assertEqual(emailer._get_external_submitter_email(task),
                             None)
            self.assertEqual(emailer.get_message_log(),
                             '\nNo participant found with guid: 444\n')
        finally:
            shutil.rmtree(temp_dir)

    def test_get_external_submitter_email_no_participant_email(self):

        params = D3RParameters()
        dtask = D3RTask('/foo', params)
        dtask.set_name('444' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        task = EvaluationTask('/foo',
                              dtask.get_name(),
                              dtask, params)
        plist = [Participant('1name', '1d3rusername', '444',
                             None)]
        emailer = EvaluationEmailer(ParticipantDatabase(plist), None)
        self.assertEqual(emailer._get_external_submitter_email(task), None)
        self.assertEqual(emailer.get_message_log(),
                         '\nEmail not set for participant\n')

    def test_get_external_submitter_email_valid(self):

        params = D3RParameters()
        dtask = D3RTask('/foo', params)
        dtask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        task = EvaluationTask('/foo',
                              dtask.get_name(),
                              dtask, params)
        plist = [Participant('1name', '1d3rusername', '12345',
                             'bob@bob.com')]
        # try single email address
        emailer = EvaluationEmailer(ParticipantDatabase(plist), None)
        emails = emailer._get_external_submitter_email(task)
        self.assertEqual(emails[0], 'bob@bob.com')
        self.assertEqual(len(emails), 1)
        self.assertEqual(emailer.get_message_log(), None)

        # try multiple email address
        plist = [Participant('1name', '1d3rusername', '12345',
                             'bob@bob.com,joe@joe.com')]
        # try single email address
        emailer = EvaluationEmailer(ParticipantDatabase(plist), None)
        emails = emailer._get_external_submitter_email(task)
        self.assertEqual(emails[0], 'bob@bob.com')
        self.assertEqual(emails[1], 'joe@joe.com')
        self.assertEqual(len(emails), 2)
        self.assertEqual(emailer.get_message_log(), None)

    def test_send_evaluation_email_none_task(self):
        emailer = EvaluationEmailer(None, None)
        emailer.send_evaluation_email(None)
        self.assertEqual(emailer.get_message_log(),
                         '\nTask passed in is None\n')

    def test_send_evaluation_email_clears_its_logs(self):
        emailer = EvaluationEmailer(None, None)
        emailer.send_evaluation_email(None)
        emailer.send_evaluation_email(None)

        self.assertEqual(emailer.get_message_log(),
                         '\nTask passed in is None\n')

    def test_send_evaluation_email_not_external_task(self):
        emailer = EvaluationEmailer(None, None)
        task = EvaluationTask('/foo', 'blah' +
                              EvaluationTask.EXT_SUBMISSION_SUFFIX,
                              None,
                              D3RParameters())
        emailer.send_evaluation_email(task)
        self.assertEqual(emailer.get_message_log(),
                         '\nNot an external submission\n')

    def test_send_evaluation_email_no_database(self):
        params = D3RParameters()
        dtask = D3RTask('/foo', params)
        dtask.set_name('444' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
        task = EvaluationTask('/foo',
                              dtask.get_name(),
                              dtask, params)
        emailer = EvaluationEmailer(None, None)
        emailer.send_evaluation_email(task)
        self.assertEqual(emailer.get_message_log(),
                         '\nParticipant database is None cannot send docking '
                         'evaluation email!!!\n')

    def test_send_external_submission_email_success(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            params.program = 'foo'
            params.version = '1'
            dtask = D3RTask('/foo', params)
            dtask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
            task = EvaluationTask(temp_dir,
                                  dtask.get_name(),
                                  dtask, params)
            task.create_dir()
            f = open(task.get_rmsd_txt(), 'w')
            f.write('hi\n')
            f.flush()
            f.close()
            plist = [Participant('1name', '1d3rusername', '12345',
                                 'bob@bob.com')]
            # try single email address
            smtpemailer = SmtpEmailer()
            mockserver = D3RParameters()
            mockserver.sendmail = Mock()
            mockserver.quit = Mock()
            smtpemailer.set_alternate_smtp_server(mockserver)
            emailer = EvaluationEmailer(ParticipantDatabase(plist),
                                        smtpemailer)

            emailer.send_evaluation_email(task)
            mockserver.quit.assert_any_call()
            self.assertEqual(emailer.get_message_log(),
                             '\nSent evaluation email to: bob@bob.com\n')
            self.assertEqual(mockserver.sendmail.call_count, 1)

        finally:
            shutil.rmtree(temp_dir)

    def test_send_external_submission_email_sendmail_exception(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            params.program = 'foo'
            params.version = '1'
            dtask = D3RTask('/foo', params)
            dtask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
            task = EvaluationTask(temp_dir,
                                  dtask.get_name(),
                                  dtask, params)
            plist = [Participant('1name', '1d3rusername', '12345',
                                 'bob@bob.com')]
            # try single email address
            smtpemailer = SmtpEmailer()
            mockserver = D3RParameters()
            mockserver.sendmail = Mock(side_effect=IOError('ha'))
            mockserver.quit = Mock()
            smtpemailer.set_alternate_smtp_server(mockserver)
            emailer = EvaluationEmailer(ParticipantDatabase(plist),
                                        smtpemailer)
            emailer.send_evaluation_email(task)
            mockserver.quit.assert_any_call()
            self.assertEqual(emailer.get_message_log(),
                             '\nCaught exception trying to email '
                             'participant : Caught exception ha\n')

        finally:
            shutil.rmtree(temp_dir)

    def test_send_external_submission_email_no_submitter_email(self):
        temp_dir = tempfile.mkdtemp()
        try:
            params = D3RParameters()
            params.program = 'foo'
            params.version = '1'
            dtask = D3RTask('/foo', params)
            dtask.set_name('12345' + EvaluationTask.EXT_SUBMISSION_SUFFIX)
            task = EvaluationTask(temp_dir,
                                  dtask.get_name(),
                                  dtask, params)
            plist = [Participant('1name', '1d3rusername', '1234',
                                 'bob@bob.com')]
            # try single email address
            smtpemailer = SmtpEmailer()
            emailer = EvaluationEmailer(ParticipantDatabase(plist),
                                        smtpemailer)
            emailer.send_evaluation_email(task)
            self.assertEqual(emailer.get_message_log(),
                             '\nNo participant found with guid: 12345\n')
        finally:
            shutil.rmtree(temp_dir)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
