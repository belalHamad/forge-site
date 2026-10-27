#!/usr/bin/env python3
"""Builds Forge's offline world mosque index (mosque detection v3, layer 2).

Input: an OpenStreetMap extract of every amenity=place_of_worship +
religion=muslim (nodes, ways and relations, as points), downloaded from the
Overpass API as tab-separated values:

    [out:csv(::type,::id,::lat,::lon,"name","name:en","name:ar","name:tr";true;"\\t")];
    nwr["amenity"="place_of_worship"]["religion"="muslim"];
    out center;

Output: `Forge/Resources/WorldMosques.bin`, read by `OfflineMosqueIndex`:

    "FMQ1"                     4 bytes
    count, tileCount           u32, u32 (little endian)
    tiles[tileCount]           (key u32, firstPoint u32), sorted by key
    points[count]              (lat i32 µdeg, lon i32 µdeg, nameOffset u32), grouped by tile
    names                      UTF-8, each prefixed by its byte length (u8); offset 0xFFFFFFFF = no name

A tile is 0.1° × 0.1°: key = (floor(lat*10)+900) * 3600 + (floor(lon*10)+1800).
Data © OpenStreetMap contributors, ODbL 1.0 (https://www.openstreetmap.org/copyright).

Usage: python3 scripts/build_mosque_index.py mosques.tsv Forge/Resources/WorldMosques.bin
"""
import math
import struct
import sys

MAX_NAME = 60  # bytes: longer names are cut on a character boundary


def tile_key(lat, lon):
    return (math.floor(lat * 10) + 900) * 3600 + (math.floor(lon * 10) + 1800)


def short(name):
    data = name.strip().encode("utf-8")
    if len(data) <= MAX_NAME:
        return data
    cut = data[:MAX_NAME]
    while cut and (cut[-1] & 0xC0) == 0x80:  # don't split a character
        cut = cut[:-1]
    return cut[:-1] if cut and cut[-1] >= 0xC0 else cut


def main(src, dst):
    points = []
    with open(src, encoding="utf-8") as f:
        next(f)
        for line in f:
            cols = line.rstrip("\n").split("\t")
            if len(cols) < 4 or not cols[2] or not cols[3]:
                continue
            lat, lon = float(cols[2]), float(cols[3])
            names = [c for c in cols[4:8] if c.strip()]
            points.append((tile_key(lat, lon), round(lat * 1e6), round(lon * 1e6), names[0] if names else ""))
    points.sort()
    names = bytearray()
    name_offsets = {}
    packed = bytearray()
    tiles = []
    for key, lat, lon, name in points:
        if not tiles or tiles[-1][0] != key:
            tiles.append((key, len(packed) // 12))
        if name:
            data = short(name)
            if data not in name_offsets:
                name_offsets[data] = len(names)
                names += bytes([len(data)]) + data
            offset = name_offsets[data]
        else:
            offset = 0xFFFFFFFF
        packed += struct.pack("<iiI", lat, lon, offset)
    with open(dst, "wb") as out:
        out.write(b"FMQ1")
        out.write(struct.pack("<II", len(points), len(tiles)))
        for key, first in tiles:
            out.write(struct.pack("<II", key, first))
        out.write(packed)
        out.write(names)
    size = 12 + len(tiles) * 8 + len(packed) + len(names)
    print(f"{len(points)} mosques, {len(tiles)} tiles, {size / 1e6:.1f} MB "
          f"(points {len(packed) / 1e6:.1f} MB, names {len(names) / 1e6:.1f} MB)")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
