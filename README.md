# RC Crawler — SCX30

A browser rock-crawling simulator built with Three.js. It runs on custom crawler physics: four swept-cylinder tyres on a heightfield, a soft solid-axle-style suspension, locked diffs and a brushed motor with drag brake. The six terrains are procedural: Rocky Canyon, Pine Forest, Mud Trail, Desert Ridge, Creek Crossing and Ultimate Rock Course.

## Run

```bash
python3 server.py 5190
```

Then open http://localhost:5190. Three.js r160 is vendored in `node_modules`, so `npm install` restores it if needed.

URL options: `?level=forest` (canyon, forest, mud, desert, creek, ultimate) and `?q=low|medium|high|ultra`.

## Controls

| Key | Action |
| --- | --- |
| W / ↑ | Throttle |
| S / ↓ | Brake, then reverse |
| A D / ← → | Steer |
| Space | Hand brake |
| Shift | Feather throttle (half) |
| G | Low / high range |
| X | Diff locks: Locked → Front open → Open |
| V | Dig: lock the rear driveshaft so the truck pivots on its rear wheels |
| R | Recover vehicle |
| C | Camera: Chase, Close RC, Low Ground, Cinematic, Free |
| L | Lights |
| Mouse drag / wheel | Orbit / zoom |
| Esc | Menu: terrains, challenges, settings |

On touch devices, on-screen steer, gas, reverse and brake controls appear automatically.

## Structure

```
src/
  main.js                 game state, loop, effects wiring
  core/        noise.js (seeded RNG, simplex, fbm), input.js (keyboard/mouse/touch)
  physics/     vehicle.js (rigid body, suspension, tyre friction, drivetrain, chassis contacts)
  vehicles/    crawlerModel.js (procedural SCX30 Jeep JLU with articulating axles, shocks, links)
  terrain/     heightfield.js, textures.js (procedural PBR layers), terrainMaterial.js (splat + triplanar),
               rocks.js (instanced rock prototypes rasterized into physics), vegetation.js, water.js
  levels/      levelBuilder.js (trails, three-line obstacles, creeks, mud, backdrop, markers), levels.js (6 terrains)
  camera/      cameraRig.js
  env/         environment.js (sky, clouds, sun, fog, IBL, 4 weather presets)
  effects/     post.js (DOF, bloom, grade), particles.js, tracks.js, contactShadow.js
  audio/       audio.js (fully synthesized Web Audio engine)
  challenges/  challenges.js
  ui/          ui.js
```

Rocks and logs are rasterized into the physics heightfield, so the crawler climbs exactly the shapes it renders.

`?capture=1` re-renders the terrain-card previews into `assets/previews/`. The save endpoint only accepts requests from localhost.
