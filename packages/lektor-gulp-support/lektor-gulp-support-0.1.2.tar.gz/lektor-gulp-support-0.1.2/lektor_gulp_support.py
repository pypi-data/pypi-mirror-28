# -*- coding: utf-8 -*-

import os

from lektor.pluginsystem import Plugin, get_plugin
from lektor.reporter import reporter
from lektor.utils import locate_executable, portable_popen


class GulpSupportPlugin(Plugin):
    name = u'lektor-gulp-support'
    description = u'Simple plugin that runs gulp tasks.'

    def __init__(self, *args, **kwargs):
        Plugin.__init__(self, *args, **kwargs)
        self.gulp_task = None
        self.gulp_root = os.path.join(self.env.root_path, 'gulp')

    def is_enabled(self, extra_flags):
        return bool(extra_flags.get('gulp'))

    def run_task(self, watch=False):
        args = [os.path.join(self.gulp_root, 'node_modules', '.bin', 'gulp')]
        if watch:
            args.append('watch')
        return portable_popen(args, cwd=self.gulp_root)

    def install_node_dependencies(self):
        # Use yarn over npm if it's availabe and there is a yarn lockfile
        has_yarn_lockfile = os.path.exists(os.path.join(self.gulp_root, 'yarn.lock'))
        pkg_manager = 'npm'
        if locate_executable('yarn') is not None and has_yarn_lockfile:
            pkg_manager = 'yarn'

        reporter.report_generic('Running {} install'.format(pkg_manager))
        portable_popen([pkg_manager, 'install'], cwd=self.gulp_root).wait()

    def on_server_spawn(self, **extra):
        extra_flags = extra.get("build_flags") or {}
        if not self.is_enabled(extra_flags):
            return
        reporter.report_generic('Starting gulp watch task')
        self.gulp_task = self.run_task(watch=True)

    def on_server_stop(self, **extra):
        if self.gulp_task is not None:
            reporter.report_generic('Stopping gulp watch task')
            self.gulp_task.kill()

    def on_before_build_all(self, builder, **extra):
        extra_flags = getattr(builder, "build_flags", None)
        if not self.is_enabled(extra_flags) or self.gulp_task is not None:
            return
        self.install_node_dependencies()
        reporter.report_generic('Starting gulp default task')
        self.run_task().wait()
        reporter.report_generic('Gulp default task finished')
