# Items and assets

## Items
Items are an entry in the planet catalog, and represnt a single observation.
The standard set of properties for an item are
  - *acquired*: aquistion information
  - *geometry*: GeoJSON footprint
  - *published*: when added to API

Each `item_type` may have additional specific properties

## Scenes
Imagery is captured as a continous strip known as scenes.

Three types of scenes:
  - *Basic*
  - *Ortho*
  - *Ortho Tile*

### Basic
Basic scenes are sensor corrected and scaled to top of atmosphere.
It is not orthorectified or corrected for terrain.

### Ortho
Additional post processing applied.

### Ortho Tile
Consist of multiple orthorectified scenes that are merged and the divided.

## Item Type
Represent satellite and/or processing level.
Each `item_type` has additional list of `asset_types` which can be derived from item.
Each group has consistent schemas, and can even be shared across types.

| Available Item Types | Description                                                                                              |
|----------------------|----------------------------------------------------------------------------------------------------------|
| PSScene              | PlanetScope 3, 4, and 8 band scenes captured by the Dove satellite constellation                         |
| PSScene3Band         | PlanetScope 3 band scenes (red, green, blue) captured by the Dove satellite constellation                |
| PSScene4Band         | PlanetScope 4 band scenes (red, green, blue, near-infrared) captured by the Dove satellite constellation |
| PSOrthoTile          | PlanetScope ortho tiles captured by the Dove satellite constellation                                     |
| REOrthoTile          | RapidEye OrthoTiles captured by the RapidEye satellite constellation                                     |
| REScene              | Unorthorectified strips captured by the RapidEye satellite constellation                                 |
| SkySatScene          | SkySat Scenes captured by the SkySat satellite constellation                                             |
| SkySatCollect        | Orthorectified scene composite of a SkySat collection                                                    |
| SkySatVideo          | Full motion videos collected by a single camera from any of the active SkySats                           |
| Landsat8L1G          | Landsat8 Scenes provided by USGS Landsat8 satellite                                                      |
| Sentinel2L1C         | Copernicus Sentinel-2  Scenes provided by ESA Sentinel-2 satellite                                       |

