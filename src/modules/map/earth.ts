import * as THREE from 'three';
import { feature } from 'topojson-client';
import type { FeatureCollection, MultiPolygon } from 'geojson';
import type { Topology, GeometryCollection } from 'topojson-specification';
import land from 'world-atlas/land-110m.json';
import type { MapSnapshot } from './snapshots';

export function spherePoint([lon, lat]: readonly [number, number], radius = 1) {
  const longitude = lon * Math.PI / 180;
  const latitude = lat * Math.PI / 180;
  return new THREE.Vector3(Math.cos(latitude) * Math.cos(longitude), Math.sin(latitude),
    -Math.cos(latitude) * Math.sin(longitude)).multiplyScalar(radius);
}

export function earthTexture(snapshot?: MapSnapshot, color = '#c69559', level = 0) {
  const canvas = document.createElement('canvas');
  canvas.width = 2048;
  canvas.height = 1024;
  const context = canvas.getContext('2d')!;
  context.fillStyle = '#143440';
  context.fillRect(0, 0, canvas.width, canvas.height);
  // world-atlas supplies a static neutral land outline, never political boundaries.
  const topology = land as unknown as Topology<{ land: GeometryCollection }>;
  const shape = feature(topology, topology.objects.land) as FeatureCollection<MultiPolygon>;
  context.fillStyle = '#4f8072';
  context.strokeStyle = '#80a991';
  context.lineWidth = 0.8;
  for (const polygon of shape.features.flatMap(item => item.geometry.coordinates)) {
    context.beginPath();
    for (const ring of polygon) {
      ring.forEach(([lon, lat], index) => {
        const x = (lon + 180) / 360 * canvas.width;
        const y = (90 - lat) / 180 * canvas.height;
        if (index === 0) context.moveTo(x, y);
        else context.lineTo(x, y);
      });
      context.closePath();
    }
    context.fill('evenodd');
    context.stroke();
  }
  context.strokeStyle = '#6ca4a224';
  context.lineWidth = 1;
  for (let lon = 0; lon < 360; lon += 15) {
    const x = lon / 360 * canvas.width;
    context.beginPath(); context.moveTo(x, 0); context.lineTo(x, canvas.height); context.stroke();
  }
  for (let lat = 0; lat < 180; lat += 15) {
    const y = lat / 180 * canvas.height;
    context.beginPath(); context.moveTo(0, y); context.lineTo(canvas.width, y); context.stroke();
  }
  if (snapshot) {
    context.beginPath();
    snapshot.ring.forEach(([lon, lat], index) => {
      const x = (lon + 180) / 360 * canvas.width;
      const y = (90 - lat) / 180 * canvas.height;
      if (index === 0) context.moveTo(x, y); else context.lineTo(x, y);
    });
    context.closePath();
    context.fillStyle = color;
    context.fill();
    context.strokeStyle = '#fff0bd'; context.lineWidth = 3; context.stroke();
    if (level === 2) {
      context.save(); context.clip();
      // An explicit test subdivision, never a modern province boundary.
      context.beginPath();
      context.moveTo((112 + 180) / 360 * canvas.width, (90 - 42) / 180 * canvas.height);
      context.lineTo((114 + 180) / 360 * canvas.width, (90 - 24) / 180 * canvas.height);
      context.setLineDash([5, 4]); context.lineWidth = 2; context.stroke();
      context.restore();
    }
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.colorSpace = THREE.SRGBColorSpace;
  return texture;
}
