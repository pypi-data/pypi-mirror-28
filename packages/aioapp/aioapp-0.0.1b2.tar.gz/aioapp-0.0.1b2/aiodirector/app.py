import asyncio
import signal
import logging
from typing import Dict
import aiozipkin as az
from .error import PrepareError, GracefulExit
from .tracer import Tracer, TracerTransport


logger = logging.getLogger('aiodirector')


def _raise_graceful_exit():
    raise GracefulExit()


class Component(object):
    def __init__(self):
        super(Component, self).__init__()
        self.loop = None
        self.app = None

    async def prepare(self):
        raise NotImplementedError()

    async def start(self):
        raise NotImplementedError()

    async def stop(self):
        raise NotImplementedError()


class Application(object):
    def __init__(self, loop=None) -> None:
        super(Application, self).__init__()
        self.loop = loop or asyncio.get_event_loop()
        self._components: Dict[str, Component] = {}
        self._stop_deps: dict = {}
        self._stopped: list = []
        self._tracer: Tracer = None

    def add(self, name: str, comp: Component,
            stop_after: list = None):
        if not isinstance(comp, Component):
            raise UserWarning()
        if name in self._components:
            raise UserWarning()
        comp.loop = self.loop
        comp.app = self
        self._components[name] = comp
        self._stop_deps[name] = stop_after

    def __getattr__(self, item: str) -> Component:
        if item not in self._components:
            raise AttributeError
        return self._components[item]

    def log_err(self, err):
        if isinstance(err, BaseException):
            logging.exception(err)
        else:
            logging.error(err)

    def log_warn(self, warn):
        logging.warning(warn)

    def log_info(self, info):
        logging.info(info)

    def log_debug(self, debug):
        logging.debug(debug)

    def setup_logging(self, tracer_driver=None, tracer_addr=None,
                      tracer_name=None, tracer_sample_rate=1.0,
                      tracer_send_inteval=3,
                      metrics_driver=None, metrics_addr=None,
                      metrics_name=None):
        endpoint = az.create_endpoint(tracer_name)
        sampler = az.Sampler(sample_rate=tracer_sample_rate)
        transport = TracerTransport(self, tracer_driver, tracer_addr,
                                    metrics_driver, metrics_addr, metrics_name,
                                    send_inteval=tracer_send_inteval,
                                    loop=self.loop)
        self._tracer = Tracer(transport, sampler, endpoint)

    async def _shutdown_tracer(self):
        if self._tracer:
            self.log_info("Shutting down tracer")
            await self._tracer.close()

    def run(self):
        try:
            self.loop.run_until_complete(self.run_prepare())
        except PrepareError as e:
            self.log_err(e)
            return 1
        self.run_loop()
        self.loop.run_until_complete(self.run_shutdown())
        print("Bye")
        self.loop.close()

    async def run_prepare(self):
        self.log_info('Prepare for start')

        await asyncio.gather(*[comp.prepare()
                               for comp in self._components.values()],
                             loop=self.loop)

        self.log_info('Starting...')
        await asyncio.gather(*[comp.start()
                               for comp in self._components.values()],
                             loop=self.loop)

        self.log_info('Running...')

    def run_loop(self):
        try:
            self.loop.add_signal_handler(signal.SIGINT, _raise_graceful_exit)
            self.loop.add_signal_handler(signal.SIGTERM, _raise_graceful_exit)
        except NotImplementedError:  # pragma: no cover
            # add_signal_handler is not implemented on Windows
            pass
        try:
            self.loop.run_forever()
        except GracefulExit:  # pragma: no cover
            pass

    async def run_shutdown(self):
        self.log_info('Shutting down...')
        for comp_name in self._components:
            await self._stop_comp(comp_name)
        await self._shutdown_tracer()

    async def _stop_comp(self, name):
        if name not in self._components:
            raise UserWarning('Unknown component %s' % name)
        if name in self._stopped:
            return
        if name in self._stop_deps and self._stop_deps[name]:
            for dep_name in self._stop_deps[name]:
                await self._stop_comp(dep_name)
        await self._components[name].stop()
        self._stopped.append(name)
