def validate_geom(geom):
    ...


def set_clip(aoi):
    validate_geom(aoi)
    tool = {"clip": {"aoi": aoi}}
    return tool


def set_coregistration(anchor_item):
    tool = {"coregister": {"anchor_item": anchor_item}}
    return tool


def set_fileformat(format=None):
    if format not in [None, "COG", "PL_NITF"]:
        raise ValueError(
            "Not an available file type chose either 'COG' or 'PL_NITF",
        )
    if format:
        return {"file_format": {"format": format}}


def set_harmonization(target=None):
    if target not in [None, "Sentinel-2", "PS2"]:
        raise ValueError("Not an available harmonization target")
    if target:
        return {"harmonize": {"target_sensor": target}}


def set_bandmath(*args: str):
    maths = list(*args)
    assert len(maths) < 16, "only 15 bands allowed"
    ids = [f"b{i}" for i in range(1, len(maths) + 1)]
    print(ids)
    band_names = {ids[i]: maths[i] for i in range(len(maths))}
    print(band_names)
    return {"bandmath": dict(band_names)}


def set_tools(
    *,
    clip_aoi=None,
    fileformat=None,
    coregister_item=None,
    harmonization_target=None,
    bandmath=None,
    composite=False,
):
    # What is best practice? Have tools defined at initialization as
    # parameters or call seperatly to update the request?
    # tools = {}
    # tools["tools"] = [{"clip": {"aoi": geom}}]
    tools = {}
    if clip_aoi:
        tools.update(set_clip(clip_aoi))
    if fileformat:
        tools.update(set_fileformat(fileformat))
    if coregister_item:
        tools.update(set_coregistration(coregister_item))
    if harmonization_target:
        tools.update(set_harmonization(harmonization_target))
    if bandmath:
        tools.update(set_bandmath(bandmath))
    if composite:
        tools.update({"composite": {}})
    print([tools])
    return [tools]
