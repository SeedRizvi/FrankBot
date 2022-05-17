import asyncio


async def items():
    items = []
    # Adding Ultra Rares
    items.append(dict(name="Reuben's Plushie", value=100000))
    items.append(dict(name="Flynn's Grinder", value=100000))
    items.append(dict(name="Shower Cereal", value=100000))
    items.append(dict(name="Fresh Microphone", value=100000))
    items.append(dict(name="Asad's Groutfit", value=100000))

    # Adding Rares
    items.append(dict(name="Frank's Webcam", value=20000))
    items.append(dict(name="10 in One", value=20000))

    # TO DO: Add uncommon / common items as filler
    return items
