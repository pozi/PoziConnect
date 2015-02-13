# Spatial Output

## Find non-contiguous/fragmented properties.

The new layer, called `Audit - Vicmap Property Address.TAB` contains a field called `cohesion`. Properties that are nice and rectangular have a cohesion value that is close to 1. Properties with a value close to 0 are likely to be fragmented and may require further attention.

Open up the table in MapInfo, and sort by the cohesion field. Select the first record, and click Ctrl-A to locate it on the map. If a property is really fragmented, you may not even see it, because MapInfo will zoom to the middle where they may not be anything to see. You may have to zoom out or add the selection to the map window as its own layer and give it a really thick colourful border so you can find it.
