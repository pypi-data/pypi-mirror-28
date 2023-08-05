import asyncio
import logging
from typing import Set, Optional

from aiolifxc import Lights, Light, Color, LightOffline

from robotica.plugins.outputs import Output
from robotica.types import Action, Config

logger = logging.getLogger(__name__)


class LifxOutput(Output):
    def __init__(
            self, *,
            name: str,
            loop: asyncio.AbstractEventLoop,
            config: Config) -> None:
        super().__init__(
            name=name,
            loop=loop,
            config=config,
        )
        self._disabled = self._config['disabled']
        self._lights = Lights(loop=self._loop)
        self._locations = self._config.get('locations', {}) or {}

    def start(self) -> None:
        if not self._disabled:
            logger.debug("LIFX enabled.")
            self._lights.start_discover()

    def stop(self) -> None:
        pass

    def _get_labels_for_location(self, location: str) -> Set[str]:
        labels = set(self._locations.get(location, []))
        return labels

    def is_action_required_for_location(self, location: str, action: Action) -> bool:
        if self._disabled:
            return False

        labels = self._get_labels_for_location(location)
        if len(labels) == 0:
            return False

        if 'lights' in action:
            return True

        return False

    async def execute(self, location: str, action: Action) -> None:
        if 'lights' in action:
            lights = action['lights']

            lights_action = lights['action']
            if lights_action == "flash":
                await self.flash(location=location)
            elif lights_action == "wake_up":
                await self.wake_up(location=location)
            elif lights_action == "turn_off":
                await self.turn_off(location=location)
            elif lights_action == "turn_on":
                color = None
                if 'color' in lights:
                    try:
                        color = Color(
                            hue=int(lights['color']['hue']),
                            saturation=int(lights['color']['saturation']),
                            brightness=int(lights['color']['brightness']),
                            kelvin=int(lights['color']['kelvin'])
                        )
                    except IndexError:
                        logger.error("Ignoring invalid color %s.", lights['color'])

                await self.turn_on(location=location, color=color)
            else:
                logger.error("Unknown action '%s'.", action)

    def _get_lights_from_location(self, location: str) -> Lights:
        labels = self._get_labels_for_location(location)
        lights = self._lights.get_by_lists(labels=list(labels))  # type: Lights
        return lights

    async def wake_up(self, location: str) -> None:
        async def single_light(light: Light) -> None:
            try:
                power = await light.get_power()
                if not power:
                    await light.set_color(
                        Color(hue=0, saturation=0, brightness=0, kelvin=2500))
                await light.set_power(True)
                await light.set_color(
                    Color(hue=0, saturation=0, brightness=100, kelvin=2500),
                    duration=60000)
            except LightOffline:
                logger.error("Light is offline %s.", light)

        lights = self._get_lights_from_location(location)
        logger.info("Lifx wakeup for lights %s.", lights)
        await lights.do_for_every_light(single_light)

    async def flash(self, location: str) -> None:
        lights = self._get_lights_from_location(location)
        logger.info("Lifx flash for lights %s.", lights)
        await lights.set_waveform(
            color=Color(hue=0, saturation=100, brightness=100, kelvin=3500),
            transient=1,
            period=1000,
            cycles=2,
            duty_cycle=0,
            waveform=0,
        )

    async def turn_off(self, location: str) -> None:
        lights = self._get_lights_from_location(location)
        logger.info("Lifx turn off lights %s.", lights)
        await lights.set_light_power(False)

    async def turn_on(self, location: str, color: Optional[Color]) -> None:
        lights = self._get_lights_from_location(location)
        logger.info("Lifx turn on lights %s.", lights)
        if color is not None:
            await lights.set_color(color)
        await lights.set_light_power(True)
