import asyncio
import functools

from govee_local_api import GoveeController, GoveeDevice


def update_device_callback(device: GoveeDevice):
    print(f"Goveee device update callback: {device}")


def discovered_callback(device: GoveeDevice, is_new: bool) -> bool:
    if is_new:
        print(f"Discovered: {device}. New: {is_new}")
        device.set_update_callback(update_device_callback)
    return True


async def print_status(controller: GoveeController):
    while True:
        for device in controller.devices:
            print(f"Status: {device}")
        await asyncio.sleep(5)


async def main(controller: GoveeController):
    await controller.start()
    await asyncio.sleep(5)

    device: GoveeDevice = controller.get_device_by_ip("10.0.0.183")
    # await device.turn_on()
    # await asyncio.sleep(5)
    await print_status(controller)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    controller: GoveeController = GoveeController(
        loop=loop,
        broadcast_address="10.0.0.228",
        listening_address="10.0.0.52",
        discovery_enabled=True,
        discovered_callback=discovered_callback,
        evicted_callback=lambda device: print(f"Evicted {device}"),
    )

    try:
        loop.run_until_complete(main(controller))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        controller.clenaup()
        loop.close()
