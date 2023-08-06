#
# coding=utf-8
import unittest
import sys
import os
import logging

from pptx_template.cli import main

BASE_DIR = os.getcwd()

FORMAT = '%(filename)s[%(lineno)-3d] %(levelname)-2s [%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class MyTest(unittest.TestCase):
    def tearDown(self):
        os.chdir(BASE_DIR)

    def test_simple(self):
        os.chdir(os.path.join(BASE_DIR, 'test', 'data'))
        sys.argv = ['myprog', '--out', 'out.pptx', '--template', 'in.pptx', '--model', 'model.json', '--debug']
        main()

    def test_skip_model_not_found(self):
        os.chdir(os.path.join(BASE_DIR, 'test', 'data'))
        sys.argv = ['myprog', '--out', 'out.pptx', '--template', 'in.pptx', '--model', 'model-error.json', '--debug',
                    '--skip-model-not-found']
        main()

    def test_not_skip_model_not_found(self):
        os.chdir(os.path.join(BASE_DIR, 'test', 'data'))
        sys.argv = ['myprog', '--out', 'out.pptx', '--template', 'in.pptx', '--model', 'model-error.json', '--debug']
        try:
            main()
        except:
            pass
        else:
            raise Error("Exception should be raised")

    def test_xlsx_mode(self):
        os.chdir(os.path.join(BASE_DIR, 'test', 'data2'))
        sys.argv = ['myprog', '--out', 'out.pptx', '--template', 'in.pptx', '--model', 'in.xlsx', '--debug']
        main()


if __name__ == '__main__':
    unittest.main()
